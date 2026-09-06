"""Deterministic studio + exact artwork + contact-aware composition and QA."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from scipy.ndimage import distance_transform_edt
from studio_common import load_srgb, linear, srgb, save_rgb, warp_rgba, SRGB

ROOT = Path(__file__).resolve().parents[1]

def artwork_on_sign(base_path, output_path, finish="standard"):
    image = load_srgb(base_path)
    generation_size = list(image.size)
    image = image.resize((4096,3072), Image.Resampling.LANCZOS)
    bg = np.asarray(image, np.float32)/255
    gray = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    mask = (gray < 80).astype(np.uint8)
    mask[int(image.height*.46):] = 0
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask)
    if n < 2:
        raise ValueError("No dark physical sign found in background")
    i = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    x, y, w, h, _ = stats[i]
    if w < 80 or h < 80:
        raise ValueError("Sign too small for exact official artwork")
    with Image.open(ROOT / "assets/logo-garage-665-transparente.png") as raw:
        logo = raw.convert("RGBA")
        logo = logo.crop(logo.getchannel("A").getbbox())
    s = min(w*.80/logo.width, h*.80/logo.height)
    dw, dh = logo.width*s, logo.height*s
    dx, dy = x+(w-dw)/2, y+(h-dh)/2
    M = np.float32([[s, 0, dx], [0, s, dy], [0, 0, 1]])
    rgb = np.asarray(logo, np.float32)[..., :3]/255
    alpha = np.asarray(logo, np.float32)[..., 3]/255
    if finish == "matte_physical":
        # Keep the official artwork pixel-for-pixel in shape, but compress the
        # baked specular highlights so it reads as a real satin emblem instead
        # of a glowing/glossy AI logo.
        lum = .2126*rgb[...,0] + .7152*rgb[...,1] + .0722*rgb[...,2]
        compressed = np.where(lum > .68, .68 + (lum-.68)*.30, lum)
        rgb = np.clip(rgb * (compressed/np.maximum(lum,.02))[...,None], 0, 1)
    pm, a = warp_rgba(rgb, alpha, M, image.size)
    # Modulate print by the photographed sign's smooth neutral illumination.
    sign_light = cv2.GaussianBlur(gray.astype(np.float32)/255, (0, 0), 6)
    median = float(np.median(sign_light[y+10:y+h-10, x+10:x+w-10]))
    light = np.clip(sign_light / max(median, .01), .9, 1.05)*.88
    bg_linear = linear(bg)
    if finish == "matte_physical":
        # A short, soft offset shadow makes the official emblem visibly raised
        # from the matte carrier panel without adding a fake reflective halo.
        shadow_M = M.copy()
        shadow_M[0,2] += 5
        shadow_M[1,2] += 7
        _, shadow_a = warp_rgba(np.zeros_like(rgb), alpha, shadow_M, image.size)
        shadow_a = cv2.GaussianBlur(shadow_a, (0,0), 4)
        bg_linear *= (1-.20*shadow_a[...,None])
        light = np.clip(light, .82, .94)
    result = pm*light[..., None] + bg_linear*(1-a[..., None])
    save_rgb(output_path, srgb(result))
    return {"plate_bbox_source": [int(v) for v in (x,y,w,h)],
            "logo_transform": M.tolist(), "logo_regenerated": False,
            "base_native_size": list(image.size), "generation_native_size": generation_size,
            "logo_finish": finish,
            "construction": "generated physical plate; exact original artwork composited at master resolution",
            "mounting": "matte carrier panel with physical wall standoffs; raised emblem with short contact shadow" if finish == "matte_physical" else "standard"}

def apply_plate(rgb, quad):
    if quad is None:
        return rgb.copy(), np.zeros(rgb.shape[:2], np.float32)
    q = np.asarray(quad, np.float32)
    if not cv2.isContourConvex(q) or abs(cv2.contourArea(q)) < 10:
        raise ValueError("Plate quadrilateral must be convex and nonzero")
    if (q < 0).any() or (q[:,0] >= rgb.shape[1]).any() or (q[:,1] >= rgb.shape[0]).any():
        raise ValueError("Plate outside photograph")
    with Image.open(ROOT / "assets/tampa-placa/tampa-placa-garage-665-horizontal-v03.png") as im:
        plate = im.convert("RGBA")
    px = np.asarray(plate, np.float32)/255
    corners = np.float32([[0,0],[plate.width-1,0],[plate.width-1,plate.height-1],[0,plate.height-1]])
    M = cv2.getPerspectiveTransform(corners, q)
    pm, a = warp_rgba(px[...,:3], px[...,3], M, (rgb.shape[1],rgb.shape[0]))
    # Clip all drawing to the measured original black patch, even at the border.
    region = np.zeros(rgb.shape[:2], np.uint8)
    cv2.fillConvexPoly(region, q.round().astype(np.int32), 1)
    a *= region
    pm *= region[...,None]
    result = srgb(pm*.92 + linear(rgb)*(1-a[...,None]))
    result[a == 0] = rgb[a == 0]
    return result, a

def defringe(rgb, alpha):
    # Reconstruct only mixed edge colours, never broaden the silhouette.
    opaque = alpha >= .995
    if not opaque.any():
        raise ValueError("No opaque pixels in vehicle mask")
    distances, indices = distance_transform_edt(~opaque, return_indices=True)
    near = rgb[indices[0], indices[1]]
    weight = np.where((alpha > .01) & (alpha < .995) & (distances <= 5), (1-alpha)*.7, 0)
    return rgb*(1-weight[...,None]) + near*weight[...,None]

def contact_shadow(alpha, M, contacts, size, footprint=None, broad_strength=.79):
    """Soft ground shadow follows bottom silhouette; tyre contacts stay tight."""
    w,h = size
    unit=w/1600
    ys,xs = np.nonzero(alpha > .5)
    x0,x1,y1 = int(xs.min()),int(xs.max()),int(ys.max())
    car_width = x1-x0
    broad = np.zeros((h,w),np.float32)
    if footprint:
        points=cv2.perspectiveTransform(np.asarray([footprint],np.float32),M)[0]
        cv2.fillConvexPoly(broad,cv2.convexHull(points.round().astype(np.int32)),broad_strength)
    else:
        cv2.ellipse(broad, ((x0+x1)//2,y1+5), (int(car_width*.47), max(6,int(car_width*.035))),0,0,360,.55,-1)
    broad = cv2.GaussianBlur(broad,(0,0),sigmaX=car_width*.023,sigmaY=car_width*.012)
    tight = np.zeros_like(broad)
    floor_y = np.full(w,y1,dtype=int)
    for x in range(x0,x1+1):
        rows = np.flatnonzero(alpha[:,x] > .5)
        if rows.size:
            floor_y[x] = rows[-1]
    # Underbody shadow runs along the actual lower edge, not a fixed canvas ellipse.
    for x in range(x0,x1+1):
        if floor_y[x] > y1-car_width*.08:
            yy = min(h-1,floor_y[x]+3)
            tight[max(0,yy-2):min(h,yy+7),x] = .62
    tight = cv2.GaussianBlur(tight,(0,0),sigmaX=6*unit,sigmaY=5*unit)
    transformed = cv2.perspectiveTransform(np.asarray([contacts],np.float32),M)[0]
    tyre = np.zeros_like(broad)
    for x,y in transformed:
        cv2.ellipse(tyre,(round(float(x)),round(float(y))+round(3*unit)),(max(9,int(car_width*.04)),round(4*unit)),0,0,360,.72,-1)
    tyre = cv2.GaussianBlur(tyre,(0,0),sigmaX=5*unit,sigmaY=3*unit)
    return 1-(1-broad)*(1-tight)*(1-tyre)

def delta_report(original, edited, alpha, plate_alpha, patches):
    import colour
    protected = (alpha >= .995) & (plate_alpha <= .001)
    changed = np.max(np.abs(original-edited),axis=2)
    # Native source coordinates avoid interpolation differences in colour checks.
    patch_reports=[]
    for box in patches:
        x0,y0,x1,y1=box
        a = original[y0:y1,x0:x1].mean(axis=(0,1))
        b = edited[y0:y1,x0:x1].mean(axis=(0,1))
        d = colour.delta_E(colour.XYZ_to_Lab(colour.sRGB_to_XYZ(a)),colour.XYZ_to_Lab(colour.sRGB_to_XYZ(b)),method="CIE 2000")
        patch_reports.append({"box":box,"delta_e_2000":float(d)})
    return {"protected_pixels":int(protected.sum()),
        "max_protected_rgb_change_8bit":float(changed[protected].max()*255),
        "paint_patches":patch_reports,
        "meaning":"Measures fidelity to this source JPEG, not physical paint calibration without a chart."}

def panel(images, labels, output, tile=(640,480), columns=None):
    columns=columns or len(images)
    rows=(len(images)+columns-1)//columns
    canvas=Image.new("RGB",(tile[0]*columns,(tile[1]+48)*rows),(24,27,31))
    draw=ImageDraw.Draw(canvas)
    for i,(im,label) in enumerate(zip(images,labels)):
        x,y=(i%columns)*tile[0],(i//columns)*(tile[1]+48)
        canvas.paste(ImageOps.contain(im,tile,Image.Resampling.LANCZOS),(x,y+48))
        draw.text((x+16,y+16),label,fill="white",font=ImageFont.load_default(size=17))
    save_rgb(output,canvas)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--config",type=Path,default=ROOT/"config/piloto-v2.json")
    p.add_argument("--somente-estudio",action="store_true")
    args=p.parse_args()
    cfg=json.loads(args.config.read_text())
    studio_path=ROOT/cfg["studio"]
    sign=artwork_on_sign(ROOT/cfg["studio_base"],studio_path,cfg.get("wall_logo_finish","standard"))
    (studio_path.with_suffix(".json")).write_text(json.dumps(sign,indent=2))
    studio=load_srgb(studio_path)
    save_rgb(studio_path.with_name(studio_path.stem+"-4096x3072.png"),studio.resize((4096,3072),Image.Resampling.LANCZOS))
    if args.somente_estudio:
        return
    size=tuple(cfg["stage_size"])
    background=np.asarray(studio.resize(size,Image.Resampling.LANCZOS),np.float32)/255
    previews=[]
    reports=[]
    for job in cfg["photos"]:
        out=ROOT/cfg["workdir"]/job["id"]
        src=load_srgb(job["source"])
        source_rgb=np.asarray(src,np.float32)/255
        alpha=np.asarray(Image.open(out/"alpha-final.png"),np.float32)/255
        render_rgb=defringe(source_rgb,alpha)
        rgb,plate_a=apply_plate(render_rgb,job["plate_quad"])
        colour_report=delta_report(source_rgb,rgb,alpha,plate_a,job.get("paint_patches",[]))
        if colour_report["max_protected_rgb_change_8bit"] > .01:
            raise RuntimeError("Unexpected modification inside protected vehicle")
        ys,xs=np.nonzero(alpha>.5)
        x0,x1,y1=int(xs.min()),int(xs.max()),int(ys.max())
        scale=size[0]*job["vehicle_width_fraction"]/(x1-x0+1)
        tx=size[0]/2-scale*(x0+x1)/2
        ty=size[1]*job["baseline_fraction"]-scale*y1
        M=np.float32([[scale,0,tx],[0,scale,ty],[0,0,1]])
        pm,a=warp_rgba(render_rgb,alpha,M,size)
        shadow=contact_shadow(a,M,job["contact_points"],size,job.get("shadow_footprint"),job.get("shadow_strength",.79))
        final=srgb(pm+linear(background)*(1-shadow[...,None])*(1-a[...,None]))
        # Render official plate artwork at final resolution, avoiding loss of its
        # small lettering from an unnecessary source-resolution intermediate.
        plate_stage=cv2.perspectiveTransform(np.asarray([job["plate_quad"]],np.float32),M)[0] if job["plate_quad"] else None
        final,_=apply_plate(final,plate_stage)
        preview=Image.fromarray(np.round(np.clip(final,0,1)*255).astype(np.uint8))
        save_rgb(out/"preview.png",preview.resize((1600,1200),Image.Resampling.LANCZOS))
        save_rgb(out/"source-srgb.png",src)
        master=preview.resize(tuple(cfg["output_size"]),Image.Resampling.LANCZOS)
        save_rgb(out/"master-4096x3072.png",master)
        if cfg.get("export_deliveries", True):
            subprocess.run([sys.executable,str(ROOT/"scripts/exportar_formatos.py"),str(out/"master-4096x3072.png"),"--saida",str(out/"formatos")],check=True)
        # Reproject baseline original for a side-by-side contour and identity check.
        checker=np.indices(alpha.shape).sum(axis=0)//16%2
        checker_rgb=np.repeat((.3+.2*checker)[...,None],3,axis=2)
        cut=source_rgb*alpha[...,None]+checker_rgb*(1-alpha[...,None])
        cut=Image.fromarray(np.round(cut*255).astype(np.uint8))
        panel([src,cut,preview],["Fotografia original","Alpha refinado (RGB original)","Composicao fiel | reflexos originais"],out/"comparativo.jpg")
        report={"id":job["id"],"status":"technical_pilot_not_approved_for_publication",
            "source_sha256":hashlib.sha256(Path(job["source"]).read_bytes()).hexdigest(),
            "studio_sha256":hashlib.sha256(studio_path.read_bytes()).hexdigest(),
            "source_native_size":list(src.size),"stage_size":list(size),
            "master_size":list(master.size),"upscaled":True,"super_resolution_generative":False,
            "transform":M.tolist(),"plate_quad_source":job["plate_quad"],
            "plate_quad_stage":cv2.perspectiveTransform(np.asarray([job["plate_quad"]],np.float32),M)[0].tolist() if job["plate_quad"] else None,
            "colour":colour_report,"limitations":[job["reflections_status"],"No ColorChecker supplied; physical paint colour cannot be certified.","Camera/light mismatch with indoor studio remains in archive photographs."],
            "wall_sign":sign,
            "vehicle_bbox_stage":[int(np.nonzero(a>.5)[1].min()),int(np.nonzero(a>.5)[0].min()),int(np.nonzero(a>.5)[1].max()),int(np.nonzero(a>.5)[0].max())]}
        (out/"qa.json").write_text(json.dumps(report,indent=2))
        reports.append(report)
        previews.append(preview)
    parent=ROOT/cfg["workdir"]
    panel(previews,[j["id"] for j in cfg["photos"]],parent/"serie-comparativa.jpg",tile=(640,480),columns=3)
    (parent/"qa-serie.json").write_text(json.dumps(reports,indent=2))
    print(parent/"serie-comparativa.jpg",flush=True)

if __name__=="__main__":
    main()
