#!/usr/bin/env python3
"""Mantém o carro API aprovado e substitui somente o Studio H pelo teto canônico."""
from pathlib import Path
import hashlib, json
import cv2
import numpy as np
from PIL import Image, ImageCms

ROOT=Path(__file__).resolve().parents[1]
CAR=ROOT/'trabalhos/panamera/serie-v9/perfil/doador-api-v01/doador-contido-diagnostico.png'
BASE=ROOT/'trabalhos/panamera/previews-serie-v10-studio-canonico/externas/perfil/preview.png'
ALPHA=ROOT/'trabalhos/panamera/previews-serie-v10-studio-canonico/externas/perfil/alpha-veiculo-preview.png'
OUT=ROOT/'trabalhos/panamera/serie-v10/perfil-studio-canonico-v01'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 car=np.asarray(Image.open(CAR).convert('RGB'),np.float32)/255
 base=np.asarray(Image.open(BASE).convert('RGB'),np.float32)/255
 alpha=np.asarray(Image.open(ALPHA).convert('L'),np.float32)/255
 if car.shape!=base.shape or alpha.shape!=base.shape[:2]:raise SystemExit('Dimensoes incompatíveis')
 # A resposta API já foi contida na silhueta original. Aqui só trocamos os
 # pixels externos pela sala canônica de teto contínuo.
 # Use somente o núcleo opaco. A silhueta, os pneus, a sombra e a faixa de
 # transição vêm integralmente da composição canônica, eliminando contaminação
 # do fundo anterior e qualquer halo de recorte.
 core=(alpha>=.97).astype(np.uint8)*255
 core=cv2.erode(core,np.ones((9,9),np.uint8),iterations=1)
 core=cv2.GaussianBlur(core,(0,0),2.0).astype(np.float32)/255
 a=core[...,None]
 result=np.round(np.clip(car*a+base*(1-a),0,1)*255).astype(np.uint8)
 result[core==0]=(base[core==0]*255).round().astype(np.uint8)
 profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
 path=OUT/'perfil-studio-canonico-candidato-v01.png';Image.fromarray(result).save(path,icc_profile=profile)
 changed_outside=int(np.any(result!=(base*255).round().astype(np.uint8),axis=2)[alpha==0].sum())
 report={'status':'visual_approval_required','car_source':str(CAR.relative_to(ROOT)),'canonical_background':str(BASE.relative_to(ROOT)),'car_source_sha256':sha(CAR),'background_sha256':sha(BASE),'changed_pixels_outside_vehicle_alpha':changed_outside,'ceiling_policy':'continuous plain ceiling; no visible rectangular luminous panel','car_regenerated_in_this_step':False,'logo_regenerated_in_this_step':False}
 (OUT/'qa-rebase.json').write_text(json.dumps(report,indent=2)+'\n');print(path)
 if changed_outside!=0:raise SystemExit(2)

if __name__=='__main__':main()
