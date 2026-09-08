#!/usr/bin/env python3
"""Prepara PNGs e máscaras alfa para edições internas estritamente contidas."""
from pathlib import Path
import json
import sys
import numpy as np
from PIL import Image, ImageCms, ImageOps

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from compor_interiores_studio_v10 import SOURCES, mask_for

OUT=ROOT/'trabalhos/panamera/serie-v10/interiores-api/preparo'
PROFILE=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()

def main():
    manifest=[]
    for name,path in SOURCES.items():
        with Image.open(path) as raw:
            image=ImageOps.exif_transpose(raw).convert('RGB')
        rgb=np.asarray(image,np.uint8)
        edit=np.clip(mask_for(name,rgb),0,1)
        image=image.resize((1600,1200),Image.Resampling.LANCZOS)
        edit=np.asarray(Image.fromarray(np.round(edit*255).astype(np.uint8)).resize((1600,1200),Image.Resampling.BILINEAR),np.float32)/255
        rgb=np.asarray(image,np.uint8)
        # API: alfa zero edita; alfa 255 bloqueia.
        api_alpha=np.round((1-edit)*255).astype(np.uint8)
        rgba=np.zeros((*api_alpha.shape,4),np.uint8)
        rgba[:,:,3]=api_alpha
        d=OUT/name;d.mkdir(parents=True,exist_ok=True)
        image.save(d/'alvo-1600x1200.png',icc_profile=PROFILE)
        Image.fromarray(rgba,'RGBA').save(d/'mascara-api-alpha.png',icc_profile=PROFILE)
        overlay=rgb.astype(np.float32)
        tint=np.zeros_like(overlay);tint[:]=(212,40,180)
        active=edit>.10
        overlay[active]=overlay[active]*.34+tint[active]*.66
        Image.fromarray(np.clip(overlay,0,255).astype(np.uint8)).save(d/'revisao-mascara.jpg',quality=94,icc_profile=PROFILE)
        manifest.append({'id':name,'source':str(path.relative_to(ROOT)),'editable_percent':float((edit>.10).mean()*100),'protected_percent':float((edit<=.10).mean()*100)})
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(OUT)

if __name__=='__main__': main()
