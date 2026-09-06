"""Compare localized windshield trials against the original. Read-only metrics + review sheet."""
from pathlib import Path
import json
import cv2
import numpy as np
from PIL import Image
from studio_common import load_srgb
from montar_studio_v2 import panel
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"trabalhos/panamera"
SOURCE=BASE/"studio-v2/dianteira-3-4/source-srgb.png"
MASK=BASE/"refinamento-dianteira-v2/para-brisa-editar.png"
TRIALS={
 "teste02-escuro":BASE/"refinamento-dianteira-v2-teste02/para-brisa-teste-mascarado.png",
 "teste03-translucido":BASE/"refinamento-dianteira-v3-teste-vidro/para-brisa-teste-mascarado.png",
}
def lab(a): return cv2.cvtColor(a,cv2.COLOR_RGB2LAB).astype(np.float32)
def stats(a,sel):
 la=lab(a);L=la[:,:,0][sel]
 return {"L_mean":float(L.mean()),"L_p10_p50_p90":[float(x) for x in np.percentile(L,[10,50,90])],
  "a_mean":float(la[:,:,1][sel].mean()),"b_mean":float(la[:,:,2][sel].mean())}
def main():
 original=np.asarray(load_srgb(SOURCE))
 mask=np.asarray(Image.open(MASK))
 sel=mask>127
 base=stats(original,sel)
 images=[Image.fromarray(original)];labels=["Original"]
 reports={}
 for name,path in TRIALS.items():
  current=np.asarray(load_srgb(path))
  assert np.array_equal(current[mask==0],original[mask==0])
  s=stats(current,sel)
  s.update({"delta_L_mean":s["L_mean"]-base["L_mean"],
   "delta_a_mean":s["a_mean"]-base["a_mean"],"delta_b_mean":s["b_mean"]-base["b_mean"],
   "changed_pixels_outside_mask":0})
  reports[name]=s;images.append(Image.fromarray(current));labels.append(name)
 output=BASE/"comparacao-testes-vidro.jpg"
 panel(images,labels,output,tile=(640,480),columns=3)
 result={"status":"teste03_preferred_pending_human_approval",
  "measurement_space":"OpenCV 8-bit CIELAB representation after ICC-aware sRGB conversion",
  "scope":"mask values >127; metrics describe pixel appearance, not physical glass transmission",
  "original":base,"trials":reports,
  "interpretation":["Teste02 is materially too dark.","Teste03 preserves average lightness substantially better and reduces the bright reflection tail.","Small chroma shift in Teste03; appearance still requires human inspection.","No trial changes pixels outside the reviewed mask."],
  "approval":{"technical_containment":True,"visual":False,"publication":False}}
 (BASE/"avaliacao-testes-vidro.json").write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
if __name__=="__main__":main()

