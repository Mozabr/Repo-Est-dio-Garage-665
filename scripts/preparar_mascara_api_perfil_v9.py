#!/usr/bin/env python3
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'trabalhos/panamera/previews-serie-v8/externas/perfil/preview.png'
alpha_path=ROOT/'trabalhos/panamera/previews-serie-v8/externas/perfil/alpha-veiculo-preview.png'
out=ROOT/'trabalhos/panamera/serie-v9/perfil/preparo-api'
out.mkdir(parents=True,exist_ok=True)
image=Image.open(source).convert('RGB')
alpha=np.asarray(Image.open(alpha_path).convert('L'),np.uint8)
# API: alfa 0 permite edição e alfa 255 bloqueia. A borda mais externa fica
# protegida para impedir halos; a resposta será usada somente como doadora.
editable=(alpha>=245).astype(np.uint8)*255
api_alpha=255-editable
rgba=np.zeros((image.height,image.width,4),np.uint8)
rgba[:,:,3]=api_alpha
Image.fromarray(rgba,'RGBA').save(out/'mascara-api-alpha.png')
image.save(out/'alvo-perfil-1600x1200.png')
print(out/'mascara-api-alpha.png')
