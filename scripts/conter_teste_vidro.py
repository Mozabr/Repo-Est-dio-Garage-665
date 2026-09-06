"""Constrain the generated glass trial to the reviewed source-space edit mask."""
from pathlib import Path
import argparse,json,hashlib
import cv2,numpy as np
from PIL import Image
from studio_common import load_srgb,save_rgb
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument("candidate",type=Path);p.add_argument("--folder",type=Path,default=ROOT/"trabalhos/panamera/refinamento-dianteira-v1");a=p.parse_args()
 folder=a.folder
 src=load_srgb(ROOT/"trabalhos/panamera/studio-v2/dianteira-3-4/source-srgb.png")
 generated=load_srgb(a.candidate)
 if abs(generated.width/generated.height-src.width/src.height)>.005:raise ValueError("Aspect ratio changed")
 native_size=list(generated.size)
 generated=generated.resize(src.size,Image.Resampling.LANCZOS)
 original=np.asarray(src);candidate=np.asarray(generated)
 mask=np.asarray(Image.open(folder/"para-brisa-editar.png"))
 # Registration diagnostic on areas that were explicitly NOT requested to change.
 orb=cv2.ORB_create(nfeatures=3000)
 safe=np.where(mask==0,255,0).astype(np.uint8)
 k1,d1=orb.detectAndCompute(cv2.cvtColor(original,cv2.COLOR_RGB2GRAY),safe)
 k2,d2=orb.detectAndCompute(cv2.cvtColor(candidate,cv2.COLOR_RGB2GRAY),safe)
 if d1 is None or d2 is None:raise ValueError("No registration features")
 pairs=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(d1,d2,k=2)
 matches=[m for pair in pairs if len(pair)==2 for m,n in [pair] if m.distance<.7*n.distance]
 if len(matches)<30:raise ValueError("Insufficient registration evidence")
 points=np.float32([k1[m.queryIdx].pt for m in matches])
 targets=np.float32([k2[m.trainIdx].pt for m in matches])
 H,inliers=cv2.findHomography(targets,points,cv2.RANSAC,2)
 if H is None:raise ValueError("No stable registration")
 fraction=float(inliers.mean())
 # Align only a generated candidate; never resample the original.
 aligned=cv2.warpPerspective(candidate,H,src.size,flags=cv2.INTER_LANCZOS4)
 bounds=np.float32([[[450,240],[910,240],[880,365],[450,355]]])
 movement=np.linalg.norm(cv2.perspectiveTransform(bounds,H)-bounds,axis=2)
 if fraction<.6 or float(movement.max())>12:raise ValueError("Registration exceeds conservative gate")
 strength=mask.astype(float)/255
 final=np.round(original*(1-strength[:,:,None])+aligned*strength[:,:,None]).astype(np.uint8)
 assert np.array_equal(final[mask==0],original[mask==0])
 save_rgb(folder/"para-brisa-teste-mascarado.png",Image.fromarray(final))
 save_rgb(folder/"gerada-alinhada.png",Image.fromarray(aligned))
 from montar_studio_v2 import panel
 panel([src,Image.fromarray(final)],["Original","Teste local | nao aprovado"],folder/"comparacao-para-brisa.jpg")
 report={"status":"contained_trial_not_visually_approved","generated_native_size":native_size,
 "source_size":list(src.size),"matches":len(matches),"inlier_fraction":fraction,
 "registration_H":H.tolist(),"maximum_registration_displacement_px":float(movement.max()),
 "changed_pixels_outside_mask":0,"source_pixels_outside_mask":int((mask==0).sum()),
 "source_sha256":hashlib.sha256((ROOT/"trabalhos/panamera/studio-v2/dianteira-3-4/source-srgb.png").read_bytes()).hexdigest(),
 "visual_review_required":["cloud remnants","glass gradient seam","cabin hallucination","windshield tint"]}
 (folder/"qa-teste-vidro.json").write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=="__main__":main()
