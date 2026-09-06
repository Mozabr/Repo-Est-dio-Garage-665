"""Regression checks for identity, alpha edges, plate geometry and output contracts."""
from pathlib import Path
import json
import numpy as np
import cv2
from PIL import Image
from montar_studio_v2 import apply_plate, defringe
from studio_common import warp_rgba, srgb

ROOT=Path(__file__).resolve().parents[1]

def main():
    # An arbitrary photograph must not change anywhere outside the plate polygon.
    rng=np.random.default_rng(665)
    source=rng.random((100,160,3),dtype=np.float32)
    quad=[[40,30],[115,35],[110,64],[43,58]]
    result,mask=apply_plate(source,quad)
    assert np.array_equal(result[mask==0],source[mask==0]),"Plate changed outside pixels"
    try:
        apply_plate(source,[[0,0],[30,30],[0,30],[30,0]])
        raise AssertionError("Crossed plate corners accepted")
    except ValueError:
        pass
    # Straight-alpha black outside a white subject must not create dark fringes.
    rgba=np.zeros((16,16,3),np.float32)
    alpha=np.zeros((16,16),np.float32)
    rgba[4:12,4:12]=1
    alpha[4:12,4:12]=1
    M=np.float32([[1,0,.5],[0,1,.5],[0,0,1]])
    pm,a=warp_rgba(rgba,alpha,M,(16,16))
    on_white=srgb(pm+(1-a[...,None]))
    assert np.max(np.abs(on_white-1))<1e-5,"Fringe in premultiplied composition"
    cleaned=defringe(rgba,alpha)
    assert np.array_equal(cleaned[alpha==1],rgba[alpha==1])
    cfg=json.loads((ROOT/"config/piloto-v2.json").read_text())
    hashes=set()
    plate_reviews=[]
    for job in cfg["photos"]:
        folder=ROOT/cfg["workdir"]/job["id"]
        qa=json.loads((folder/"qa.json").read_text())
        assert qa["colour"]["max_protected_rgb_change_8bit"]==0
        assert all(p["delta_e_2000"]<1e-5 for p in qa["colour"]["paint_patches"])
        hashes.add(qa["studio_sha256"])
        native=Image.open(job["source"])
        if job["plate_quad"]:
            q=np.asarray(job["plate_quad"],np.int32)
            x0,y0=q.min(0)-4
            x1,y1=q.max(0)+5
            region=np.asarray(native.convert("RGB"))[y0:y1,x0:x1]
            black=region.max(axis=2)<8
            footprint=np.zeros(black.shape,np.uint8)
            cv2.fillConvexPoly(footprint,q-[x0,y0],1)
            overlap=np.logical_and(black,footprint).sum()/np.logical_or(black,footprint).sum()
            if overlap<=.95:
                assert job.get("plate_review_required",False), f"Unexpected plate mismatch: {job['id']} {overlap}"
                plate_reviews.append({"view":job["id"],"black_patch_iou":float(overlap),
                    "status":"manual_review_required",
                    "reason":"Dark plate support and redaction cannot be separated reliably by threshold; exact match is not certified."})
        matte=np.asarray(Image.open(folder/"alpha-final.png"))
        assert matte.shape==(native.height,native.width)
        assert ((matte>0)&(matte<255)).any(),"Missing fractional edge alpha"
        for name,size in {"feed-4096x3072.jpg":(4096,3072),"story-horizontal-3840x2160.jpg":(3840,2160),"webmotors-1920x1440.jpg":(1920,1440)}.items():
            with Image.open(folder/"formatos"/name) as im:
                assert im.size==size and im.info.get("icc_profile")
        # The vehicle must stay inside the 16:9 center crop's vertical safe area.
        x0,y0,x1,y1=qa["vehicle_bbox_stage"]
        assert y0>=cfg["stage_size"][1]*.125 and y1<cfg["stage_size"][1]*.875
        # Physical wall plate and vehicle may not intersect in image space.
        sx,sy,sw,sh=qa["wall_sign"]["plate_bbox_source"]
        native_h=qa["wall_sign"]["base_native_size"][1]
        assert (sy+sh)/native_h*cfg["stage_size"][1]+12<y0,"Car obscures studio sign"
    assert len(hashes)==1,"Studio background differs across views"
    report={"status":"passed_with_review_pending" if plate_reviews else "passed","views":len(cfg["photos"]),"plate_reviews":plate_reviews,"checks":["plate containment","invalid quad rejection","premultiplied alpha fringe","opaque RGB unchanged","source-resolution matte","source paint deltaE","export dimensions and ICC","story safe area","wall sign clearance","same studio hash"],"visual_approval":False}
    (ROOT/cfg["workdir"]/"verificacao.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
