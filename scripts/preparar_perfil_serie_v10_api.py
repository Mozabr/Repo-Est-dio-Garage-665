#!/usr/bin/env python3
from pathlib import Path
import numpy as np
from PIL import Image, ImageCms

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'trabalhos/panamera/previews-serie-v10-studio-canonico/externas/perfil/preview.png'
ALPHA=ROOT/'trabalhos/panamera/previews-serie-v10-studio-canonico/externas/perfil/alpha-veiculo-preview.png'
OUT=ROOT/'trabalhos/panamera/serie-v10/perfil-api/preparo'
PROFILE=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    image=Image.open(SOURCE).convert('RGB')
    vehicle=np.asarray(Image.open(ALPHA).convert('L'),np.uint8)
    # A borda externa permanece travada; a resposta será apenas uma doadora.
    editable=(vehicle>=245).astype(np.uint8)*255
    rgba=np.zeros((*editable.shape,4),np.uint8)
    rgba[:,:,3]=255-editable
    image.save(OUT/'alvo-perfil-1600x1200.png',icc_profile=PROFILE)
    Image.fromarray(rgba,'RGBA').save(OUT/'mascara-api-alpha.png',icc_profile=PROFILE)
    print(OUT/'mascara-api-alpha.png')

if __name__=='__main__': main()
