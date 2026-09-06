"""Read-only image diagnosis. Regions are analyst annotations, NOT editing masks."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ExifTags
import cv2
from studio_common import load_srgb
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"trabalhos/panamera/diagnostico-dianteira-3-4"
SOURCE=ROOT/"referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.06 (1).jpg"
REGIONS=[
 {"id":"R1","name":"Para-brisa","polygon":[[444,355],[556,242],[906,232],[959,338],[773,379]],"observation":"Ceu e nuvens muito reconheciveis; cabine parcialmente ocultada","risk":"alto","action":"Trocar apenas reflexao optica em teste separado; nao inventar bancos, volante ou transparencias"},
 {"id":"R2","name":"Capo","polygon":[[189,408],[440,362],[765,392],[517,505],[359,558],[123,535]],"observation":"Nuvens, fios e construcoes sobrepostos a volumes e brilho metalico","risk":"alto","action":"Retoque por trechos, protegendo emblema, vincos e textura; substituir ambiente reconhecivel por reflexos amplos, nunca por superficie fosca"},
 {"id":"R3","name":"Portas e lateral","polygon":[[940,367],[1101,355],[1151,449],[1094,591],[934,683],[925,504]],"observation":"Fachada escura e piso claro refletidos; nao sao duas cores de tinta","risk":"alto","action":"Separar paineis e frisos; nao aplicar dessaturacao global ou preencher toda lateral"},
 {"id":"R4","name":"Faixa pintada do para-choque","polygon":[[90,548],[360,583],[734,558],[764,612],[422,639],[84,605]],"observation":"Reflexos horizontais do ambiente sobre curva frontal","risk":"medio-alto","action":"Ajustar apenas areas pintadas; preservar sensores e toda grade"},
 {"id":"R5","name":"Farol proximo","polygon":[[520,537],[591,472],[725,418],[774,444],[772,489],[716,535],[618,561]],"observation":"Conjunto optico, lentes e reflexos misturados","risk":"critico","action":"Bloqueado para geracao; nao mudar modulos, LEDs ou contorno"},
 {"id":"R6","name":"Roda dianteira visivel","polygon":[[797,545],[855,505],[905,516],[932,590],[919,707],[877,781],[824,787],[794,727]],"observation":"Raios finos, pneu, freio e pinca verde caracteristicos","risk":"critico","action":"Preservar pixel e geometria; nao reconstruir"},
 {"id":"R7","name":"Tampa-placa","polygon":[[202,609],[321,618],[318,667],[198,658]],"observation":"Tarja preta medida no arquivo original","risk":"controlado","action":"Arte oficial por perspectiva, sem extrapolar quadrilatero"}
]
PATCHES=[("P1-faixa-metalica", [557,541,587,554]),("P2-capo", [400,514,430,530]),("P3-lateral-escura", [1000,402,1013,415])]
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 im=Image.open(SOURCE)
 rgb=np.asarray(load_srgb(SOURCE))
 alpha=np.asarray(Image.open(ROOT/"trabalhos/panamera/studio-v2/dianteira-3-4/alpha-final.png"))
 opaque=alpha>=254
 lab=cv2.cvtColor(rgb.astype(np.float32)/255,cv2.COLOR_RGB2LAB)
 samples=[]
 for name,box in PATCHES:
  x,y,x1,y1=box
  pixels=rgb[y:y1,x:x1].reshape(-1,3)
  samples.append({"id":name,"box_xyxy":box,"rgb_median":np.median(pixels,axis=0).tolist(),
   "lab_d65_median":np.median(lab[y:y1,x:x1].reshape(-1,3),axis=0).tolist(),
   "rgb_percentile_10":np.percentile(pixels,10,axis=0).tolist(),
   "rgb_percentile_90":np.percentile(pixels,90,axis=0).tolist(),
   "meaning":"Appearance sample only: mixture of paint, light and reflection; not factory colour or a neutral reference."})
 exif={ExifTags.TAGS.get(k,str(k)):str(v) for k,v in im.getexif().items() if ExifTags.TAGS.get(k,str(k)) in ["Make","Model","FocalLength","ExposureTime","FNumber","PhotographicSensitivity","WhiteBalance","ColorSpace","LensModel"]}
 ys,xs=np.nonzero(alpha>127)
 data={"source":str(SOURCE),"sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 "size":list(im.size),"mode":im.mode,"format":im.format,"icc_present":bool(im.info.get("icc_profile")),"capture_metadata":exif,
 "vehicle_bbox_xyxy":[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],
 "opaque_pixels":int(opaque.sum()),"mixed_alpha_pixels":int(((alpha>0)&(alpha<254)).sum()),
 "any_channel_ge250_pct_opaque":float((rgb[opaque].max(1)>=250).mean()*100),
 "all_channels_le5_pct_opaque":float((rgb[opaque].max(1)<=5).mean()*100),
 "stats_caveat":"Threshold statistics are not a RAW clipping diagnosis; black redaction and black parts are included.",
 "regions":REGIONS,"region_coordinates":"Original 1280x960, origin top-left. Approximate analysis polygons; overlapping; NOT approved editing masks.",
 "samples":samples,"factory_paint_code":None,"physical_colour_calibrated":False,
 "protected_details":["silhueta e vincos","emblema Porsche","e-hybrid","ambos farois","rodas e pneus","pincas verdes","frisos cromados","retrovisores","macanetas","grades, sensores e LEDs","tampa-placa"],
 "policy":"No image pixels modified by this diagnosis."}
 (OUT/"mapa-dados.json").write_text(json.dumps(data,ensure_ascii=False,indent=2))
 print(json.dumps(data,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
