#!/usr/bin/env python3
"""Transfere somente luminância alinhada de um doador; preserva RGB fora da máscara."""
from pathlib import Path
import argparse, hashlib, json
import cv2
import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def polygon_mask(shape, points):
    mask=np.zeros(shape,np.uint8)
    cv2.fillPoly(mask,[np.asarray(points,np.int32)],255)
    return mask

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--config',type=Path,required=True); args=ap.parse_args()
    cfg=json.loads(args.config.read_text()); out=ROOT/cfg['workdir']; out.mkdir(parents=True,exist_ok=True)
    authority_path=ROOT/cfg['authority']; donor_path=ROOT/cfg['lighting_donor']; alpha_path=ROOT/cfg['vehicle_alpha']
    source=np.asarray(Image.open(authority_path).convert('RGB'),np.uint8); h,w=source.shape[:2]
    donor=np.asarray(Image.open(donor_path).convert('RGB').resize((w,h),Image.Resampling.LANCZOS),np.uint8)
    vehicle=np.asarray(Image.open(alpha_path).convert('L'),np.uint8)

    # Registro global robusto: o fundo comum e o próprio veículo estabilizam a doadora.
    orb=cv2.ORB_create(nfeatures=8000)
    k1,d1=orb.detectAndCompute(cv2.cvtColor(donor,cv2.COLOR_RGB2GRAY),None)
    k2,d2=orb.detectAndCompute(cv2.cvtColor(source,cv2.COLOR_RGB2GRAY),None)
    pairs=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(d1,d2,k=2)
    good=[m for pair in pairs if len(pair)==2 for m,n in [pair] if m.distance<.70*n.distance]
    src=np.float32([k1[m.queryIdx].pt for m in good]); dst=np.float32([k2[m.trainIdx].pt for m in good])
    H,inliers=cv2.findHomography(src,dst,cv2.RANSAC,2.0)
    if H is None: raise SystemExit('Falha no registro do doador')
    aligned=cv2.warpPerspective(donor,H,(w,h),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REFLECT)
    corners=np.float32([[[0,0],[w-1,0],[w-1,h-1],[0,h-1]]]); moved=cv2.perspectiveTransform(corners,H)
    registration={'matches':len(good),'inlier_fraction':float(inliers.mean()),'maximum_displacement_px':float(np.linalg.norm(moved-corners,axis=2).max()),'homography':H.tolist()}
    lim=cfg['registration']; registration['passed']=registration['matches']>=lim['minimum_matches'] and registration['inlier_fraction']>=lim['minimum_inlier_fraction'] and registration['maximum_displacement_px']<=lim['maximum_displacement_px']
    if not registration['passed']: raise SystemExit('Doador reprovado pelo gate de registro')

    mc=cfg['paint_mask']; mask=cv2.erode(vehicle,np.ones((mc['erode_px']*2+1,)*2,np.uint8))
    protected=np.zeros((h,w),np.uint8)
    for key in ['protect_windows_polygon','protect_front_light_polygon','protect_rear_light_polygon','protect_lower_trim_polygon']:
        protected=cv2.max(protected,polygon_mask((h,w),mc[key]))
    for x,y,r in mc['protect_wheels']: cv2.circle(protected,(x,y),r,255,-1)
    for x,y,r in mc.get('protect_badges',[]): cv2.circle(protected,(x,y),r,255,-1)
    lab=cv2.cvtColor(source,cv2.COLOR_RGB2LAB).astype(np.float32); chroma=np.hypot(lab[:,:,1]-128,lab[:,:,2]-128)
    if mc.get('protect_high_chroma_threshold') is not None:
        protected[chroma>=mc['protect_high_chroma_threshold']]=255
    mask[protected>0]=0
    mask=cv2.GaussianBlur(mask,(0,0),mc['feather_px']); mask=np.clip(mask.astype(np.float32)/255,0,1)

    donor_lab=cv2.cvtColor(aligned,cv2.COLOR_RGB2LAB).astype(np.float32); L=lab[:,:,0]; DL=donor_lab[:,:,0]
    t=cfg['transfer']; source_low=cv2.GaussianBlur(L,(0,0),t['low_sigma']); donor_low=cv2.GaussianBlur(DL,(0,0),t['low_sigma'])
    low=np.clip((donor_low-source_low)*t['low_gain'],-t['maximum_low_delta_L'],t['maximum_low_delta_L'])
    source_mid=cv2.GaussianBlur(L,(0,0),t['mid_sigma_inner'])-source_low
    donor_mid=cv2.GaussianBlur(DL,(0,0),t['mid_sigma_inner'])-donor_low
    mid=np.clip((donor_mid-source_mid)*t['mid_gain'],-t['maximum_mid_delta_L'],t['maximum_mid_delta_L'])
    if 'material_replace_gain' in t:
        material_sigma=float(t['material_replace_sigma'])
        source_micro=L-cv2.GaussianBlur(L,(0,0),material_sigma)
        donor_material=cv2.GaussianBlur(DL,(0,0),material_sigma)+source_micro*float(t['source_microtexture_gain'])
        material_delta=np.clip(donor_material-L,-t['maximum_material_delta_L'],t['maximum_material_delta_L'])
        low_mid=material_delta*float(t['material_replace_gain'])
    else:
        low_mid=low+mid
    source_clear=np.maximum(L-cv2.GaussianBlur(L,(0,0),t['source_clearcoat_sigma']),0)
    source_clear=np.clip(source_clear*t['source_clearcoat_gain'],0,t['maximum_source_clearcoat_L'])
    candidate_L=np.clip(L+(low_mid+source_clear)*mask,0,255)
    candidate_L[(L<240)&(candidate_L>=240)]=239
    target=lab.copy(); target[:,:,0]=candidate_L
    # A cor forte na metade inferior das portas é reflexo de faixa/piso externo,
    # não basecoat. Neutralize somente essa contaminação usando a própria parte
    # superior da porta como referência cromática; nunca use o RGB gerado.
    reflection_polygons=t.get('reflection_chroma_polygons')
    if reflection_polygons:
        reflection_region=np.zeros((h,w),bool)
        for points in reflection_polygons:
            reflection_region|=polygon_mask((h,w),points)>0
        reference_region=(polygon_mask((h,w),t['basecoat_reference_polygon'])>0)&(mask>.25)
        ref_a=float(np.median(lab[:,:,1][reference_region])); ref_b=float(np.median(lab[:,:,2][reference_region]))
        chroma_from_ref=np.hypot(lab[:,:,1]-ref_a,lab[:,:,2]-ref_b)
        chroma_weight=np.clip((chroma_from_ref-t['reflection_chroma_threshold'])/24.0,0,1)
        chroma_weight*=float(t['reflection_chroma_reduction'])*mask*reflection_region
        target[:,:,1]=lab[:,:,1]*(1-chroma_weight)+ref_a*chroma_weight
        target[:,:,2]=lab[:,:,2]*(1-chroma_weight)+ref_b*chroma_weight
    glass_mask=np.zeros((h,w),np.float32)
    if 'glass_polygon' in t:
        raw_glass=polygon_mask((h,w),t['glass_polygon'])
        raw_glass=cv2.GaussianBlur(raw_glass,(0,0),t.get('glass_feather_px',8.0))
        glass_mask=raw_glass.astype(np.float32)/255.0
        glass_delta=np.clip((donor_low-source_low)*t['glass_low_gain'],-t['glass_maximum_delta_L'],t['glass_maximum_delta_L'])
        target[:,:,0]=np.clip(target[:,:,0]+glass_delta*glass_mask,0,255)
        glass_reference=(polygon_mask((h,w),t['glass_polygon'])>0)
        glass_ref_a=float(np.median(lab[:,:,1][glass_reference])); glass_ref_b=float(np.median(lab[:,:,2][glass_reference]))
        glass_chroma=float(t.get('glass_chroma_reduction',0.0))*glass_mask
        target[:,:,1]=target[:,:,1]*(1-glass_chroma)+glass_ref_a*glass_chroma
        target[:,:,2]=target[:,:,2]*(1-glass_chroma)+glass_ref_b*glass_chroma
    result=cv2.cvtColor(target.astype(np.uint8),cv2.COLOR_LAB2RGB)
    union=np.maximum(mask,glass_mask)
    result[union==0]=source[union==0]

    changed=np.any(result!=source,axis=2); result_lab=cv2.cvtColor(result,cv2.COLOR_RGB2LAB).astype(np.float32)
    active=union>0; abs_delta=np.abs(result_lab[:,:,0]-L); src_chroma=np.hypot(lab[:,:,1]-128,lab[:,:,2]-128); out_chroma=np.hypot(result_lab[:,:,1]-128,result_lab[:,:,2]-128)
    new_near_white=(L<240)&(result_lab[:,:,0]>=240)&active
    metrics={'changed_pixels_outside_mask':int((changed&~active).sum()),'editable_pixels':int(active.sum()),'mean_absolute_delta_L':float(abs_delta[active].mean()),'p95_absolute_delta_L':float(np.percentile(abs_delta[active],95)),'new_near_white_percent_L240':float(new_near_white.sum()/max(active.sum(),1)*100),'chroma_ratio':float(out_chroma[active].mean()/max(src_chroma[active].mean(),1e-5))}
    acc=cfg['acceptance']; checks={'registration':registration['passed'],'changed_pixels_outside_mask':metrics['changed_pixels_outside_mask']==acc['changed_pixels_outside_mask'],'mean_absolute_delta_L':metrics['mean_absolute_delta_L']<=acc['mean_absolute_delta_L_max'],'p95_absolute_delta_L':metrics['p95_absolute_delta_L']<=acc['p95_absolute_delta_L_max'],'new_near_white':metrics['new_near_white_percent_L240']<=acc['near_white_percent_L240_max'],'chroma_ratio':acc['chroma_ratio'][0]<=metrics['chroma_ratio']<=acc['chroma_ratio'][1]}
    profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
    Image.fromarray(result).save(out/'candidato-perfil-v01.png',icc_profile=profile)
    Image.fromarray(aligned).save(out/'doador-alinhado-diagnostico.png',icc_profile=profile)
    Image.fromarray(np.round(mask*255).astype(np.uint8)).save(out/'mascara-pintura-efetiva.png')
    Image.fromarray(np.round(glass_mask*255).astype(np.uint8)).save(out/'mascara-vidros-efetiva.png')
    report={'status':'technical_pass_visual_approval_required' if all(checks.values()) else 'technical_targets_failed','authority_sha256':sha(authority_path),'donor_sha256':sha(donor_path),'generated_rgb_used':False,'generated_texture_used':False,'source_geometry_used':True,'source_chroma_used':True,'registration':registration,'metrics':metrics,'checks':checks}
    (out/'qa-perfil-v01.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
    if not all(checks.values()): raise SystemExit(2)

if __name__=='__main__': main()
