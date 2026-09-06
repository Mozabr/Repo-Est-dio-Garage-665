"""Blend the contained generated glass with the original in linear light."""
from pathlib import Path
import json
import cv2,numpy as np
from PIL import Image
from studio_common import load_srgb,linear,srgb,save_rgb
from montar_studio_v2 import panel
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"trabalhos/panamera"
SOURCE=BASE/"studio-v2/dianteira-3-4/source-srgb.png"
CANDIDATE=BASE/"refinamento-dianteira-v3-teste-vidro/para-brisa-teste-mascarado.png"
MASK=BASE/"refinamento-dianteira-v2/para-brisa-editar.png"
OUT=BASE/"refinamento-dianteira-v4-vidro-equilibrado"
GENERATED_SHARE=.70
def lab_stats(rgb,sel):
 lab=cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB).astype(np.float32);L=lab[:,:,0][sel]
 return {"L_mean":float(L.mean()),"L_p10_p50_p90":[float(x) for x in np.percentile(L,[10,50,90])],
 "a_mean":float(lab[:,:,1][sel].mean()),"b_mean":float(lab[:,:,2][sel].mean())}
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 original=np.asarray(load_srgb(SOURCE))
 candidate=np.asarray(load_srgb(CANDIDATE))
 mask=np.asarray(Image.open(MASK),np.float32)/255
 strength=mask*GENERATED_SHARE
 mixed=srgb(linear(original/255)*(1-strength[:,:,None])+linear(candidate/255)*strength[:,:,None])
 result=np.round(np.clip(mixed,0,1)*255).astype(np.uint8)
 result[mask==0]=original[mask==0]
 assert np.array_equal(result[mask==0],original[mask==0])
 save_rgb(OUT/"para-brisa-candidato-equilibrado.png",Image.fromarray(result))
 panel([Image.fromarray(original),Image.fromarray(candidate),Image.fromarray(result)],
 ["Original","Teste03","Teste04 | 70% tratamento"],OUT/"comparacao.jpg",tile=(640,480),columns=3)
 sel=mask>.5;base=lab_stats(original,sel);current=lab_stats(result,sel)
 report={"status":"preferred_candidate_pending_human_approval","generated_treatment_share":GENERATED_SHARE,
 "original_reflection_share":1-GENERATED_SHARE,"blend_space":"linear sRGB",
 "source":base,"candidate":current,"delta_L_mean":current["L_mean"]-base["L_mean"],
 "delta_a_mean":current["a_mean"]-base["a_mean"],"delta_b_mean":current["b_mean"]-base["b_mean"],
 "changed_pixels_outside_mask":0,
 "meaning":"Original share preserves some authentic reflection and transmission. This is an aesthetic candidate, not a physical measurement of glass reflectance.",
 "approval":{"technical_containment":True,"visual":False,"publication":False}}
 (OUT/"qa.json").write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=="__main__":main()

