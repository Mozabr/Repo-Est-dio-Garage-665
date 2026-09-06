"""Align and reinsert a generated candidate only inside one reviewed mask."""
from pathlib import Path
import argparse,json
import cv2,numpy as np
from PIL import Image
from studio_common import load_srgb,save_rgb
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument("--original",type=Path,required=True);p.add_argument("--generated",type=Path,required=True);p.add_argument("--mask",type=Path,required=True);p.add_argument("--output",type=Path,required=True);p.add_argument("--report",type=Path,required=True);p.add_argument("--minimum-inlier-fraction",type=float,default=.6);p.add_argument("--maximum-displacement-px",type=float,default=12);a=p.parse_args()
 original=np.asarray(load_srgb(a.original));src_size=(original.shape[1],original.shape[0])
 generated_im=load_srgb(a.generated)
 if abs(generated_im.width/generated_im.height-src_size[0]/src_size[1])>.005:raise ValueError("Aspect ratio changed")
 generated=np.asarray(generated_im.resize(src_size,Image.Resampling.LANCZOS));mask=np.asarray(Image.open(a.mask).convert("L"))
 safe=np.where(mask==0,255,0).astype(np.uint8);orb=cv2.ORB_create(nfeatures=3500)
 k1,d1=orb.detectAndCompute(cv2.cvtColor(original,cv2.COLOR_RGB2GRAY),safe);k2,d2=orb.detectAndCompute(cv2.cvtColor(generated,cv2.COLOR_RGB2GRAY),safe)
 pairs=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(d1,d2,k=2);matches=[m for pair in pairs if len(pair)==2 for m,n in [pair] if m.distance<.7*n.distance]
 if len(matches)<40:raise ValueError("Insufficient registration evidence")
 target=np.float32([k1[m.queryIdx].pt for m in matches]);source=np.float32([k2[m.trainIdx].pt for m in matches])
 H,inliers=cv2.findHomography(source,target,cv2.RANSAC,2)
 if H is None:
  report={"status":"rejected_registration_failed","matches":len(matches),"changed_pixels_outside_mask":0}
  a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));raise SystemExit(2)
 aligned=cv2.warpPerspective(generated,H,src_size,flags=cv2.INTER_LANCZOS4)
 ys,xs=np.nonzero(mask>0);bounds=np.float32([[[xs.min(),ys.min()],[xs.max(),ys.min()],[xs.max(),ys.max()],[xs.min(),ys.max()]]])
 movement=np.linalg.norm(cv2.perspectiveTransform(bounds,H)-bounds,axis=2);fraction=float(inliers.mean())
 if fraction<a.minimum_inlier_fraction or float(movement.max())>a.maximum_displacement_px:
  report={"status":"rejected_registration_gate","matches":len(matches),"inlier_fraction":fraction,"maximum_registration_displacement_px":float(movement.max()),"gate":{"minimum_inlier_fraction":a.minimum_inlier_fraction,"maximum_displacement_px":a.maximum_displacement_px},"changed_pixels_outside_mask":0}
  a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));raise SystemExit(2)
 strength=mask.astype(float)/255;result=np.round(original*(1-strength[:,:,None])+aligned*strength[:,:,None]).astype(np.uint8);result[mask==0]=original[mask==0]
 assert np.array_equal(result[mask==0],original[mask==0])
 a.output.parent.mkdir(parents=True,exist_ok=True);save_rgb(a.output,Image.fromarray(result))
 report={"status":"contained_not_visually_approved","matches":len(matches),"inlier_fraction":fraction,"maximum_registration_displacement_px":float(movement.max()),"changed_pixels_outside_mask":0,"editable_pixels":int((mask>0).sum())}
 a.report.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=="__main__":main()
