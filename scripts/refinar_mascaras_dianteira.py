"""Deterministic localized edit masks. Does not alter source photography."""
from pathlib import Path
import json,hashlib,argparse
import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from studio_common import load_srgb,save_rgb
ROOT=Path(__file__).resolve().parents[1]
def poly(shape,points):
 m=np.zeros(shape,np.uint8);cv2.fillPoly(m,[np.asarray(points,np.int32)],255);return m
def main():
 p=argparse.ArgumentParser();p.add_argument("--config",type=Path,default=ROOT/"config/refinamento-dianteira-v1.json");args=p.parse_args()
 cfg=json.loads(args.config.read_text())
 out=ROOT/cfg["out"];out.mkdir(parents=True,exist_ok=True)
 source=load_srgb(ROOT/cfg["source"]);rgb=np.asarray(source);h,w=rgb.shape[:2]
 alpha=np.asarray(Image.open(ROOT/cfg["vehicle_alpha"]))
 protection=np.zeros((h,w),np.uint8)
 for p in cfg["protect_polygons"]:protection=np.maximum(protection,poly((h,w),p["points"]))
 for p in cfg["protect_ellipses"]:
  x,y,x1,y1=p["box"];cv2.ellipse(protection,((x+x1)//2,(y+y1)//2),((x1-x)//2,(y1-y)//2),0,0,360,255,-1)
 for p in cfg["protect_lines"]:cv2.polylines(protection,[np.asarray(p["points"],np.int32)],False,255,p["width"])
 protection=cv2.dilate(protection,np.ones((3,3),np.uint8))
 Image.fromarray(protection).save(out/"exclusoes-detalhes.png")
 reports=[];tiles=[];union=np.zeros((h,w),np.uint8);region_masks={}
 for r in cfg["regions"]:
  allowed=poly((h,w),r["polygon"])
  allowed[(alpha<254)|(protection>0)]=0
  dist=cv2.distanceTransform(allowed,cv2.DIST_L2,5)
  strength=np.clip((dist-cfg["edge_inset_px"])/cfg["feather_inside_px"],0,1)
  mask=np.round(strength*255).astype(np.uint8);union=np.maximum(union,mask);region_masks[r["id"]]=mask
  assert not mask[protection>0].any()
  assert not mask[alpha<254].any()
  assert not mask[allowed==0].any()
  Image.fromarray(mask).save(out/(r["id"]+"-editar.png"))
  rgba=np.full((h,w,4),255,np.uint8);rgba[:,:,3]=255-mask
  Image.fromarray(rgba).save(out/(r["id"]+"-api-alpha.png"))
  overlay=rgb.astype(float)*(1-strength[:,:,None]*.45)+np.array([244,94,46])*strength[:,:,None]*.45
  overlay=Image.fromarray(overlay.astype(np.uint8))
  save_rgb(out/(r["id"]+"-preview.jpg"),overlay)
  tile=Image.new("RGB",(640,512),(24,27,31));tile.paste(overlay.resize((640,480)),(0,32))
  ImageDraw.Draw(tile).text((12,8),r["id"]+" | laranja = editavel",fill="white",font=ImageFont.load_default(size=16))
  tiles.append(tile)
  reports.append({"id":r["id"],"nonzero_pixels":int((mask>0).sum()),"fully_editable_pixels":int((mask==255).sum()),"protected_overlap_pixels":0,"outside_vehicle_pixels":0,"stage":r["stage"]})
 Image.fromarray(255-union).save(out/"protecao-completa.png")
 lateral=(region_masks["lateral"] if "lateral" in region_masks else
          np.maximum(region_masks["porta-dianteira"],region_masks["porta-traseira"]))
 Image.fromarray(lateral).save(out/"lateral-editar.png")
 lateral_rgba=np.full((h,w,4),255,np.uint8);lateral_rgba[:,:,3]=255-lateral
 Image.fromarray(lateral_rgba).save(out/"lateral-api-alpha.png")
 lateral_strength=lateral.astype(float)/255
 lateral_overlay=rgb.astype(float)*(1-lateral_strength[:,:,None]*.45)+np.array([244,94,46])*lateral_strength[:,:,None]*.45
 save_rgb(out/"lateral-preview.jpg",Image.fromarray(lateral_overlay.astype(np.uint8)))
 sheet=Image.new("RGB",(1280,1024))
 for i,t in enumerate(tiles):sheet.paste(t,((i%2)*640,(i//2)*512))
 save_rgb(out/"mapa-mascaras.jpg",sheet)
 report={"status":"containment_tests_passed_visual_review_required","source_sha256":hashlib.sha256((ROOT/cfg["source"]).read_bytes()).hexdigest(),"regions":reports,"source_pixels_modified":False,"notes":["Native resolution only; API alpha convention differs from editing-strength mask.","Masks are conservative first-pass local zones, not exhaustive removal of every reflection."]}
 (out/"qa-mascaras.json").write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=="__main__":main()
