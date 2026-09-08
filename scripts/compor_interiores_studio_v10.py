#!/usr/bin/env python3
"""Substitui somente o exterior visível pelos vidros por uma vista neutra do estúdio canônico."""
from pathlib import Path
import hashlib, json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from studio_common import load_srgb, linear, save_rgb, srgb

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'trabalhos/panamera/previews-serie-v10-studio-canonico/interiores-studio'
STUDIO=ROOT/'trabalhos/panamera/previews-serie-v10-studio-canonico/studio-canonico-oficial.png'
SOURCES={
 'interior-amplo':ROOT/'referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.06 (3).jpeg',
 'painel-instrumentos':ROOT/'referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.07 (1).jpeg',
 'interior-motorista':ROOT/'referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.07 (2).jpeg'}
VISUAL_DONORS={
 'interior-motorista':ROOT/'trabalhos/panamera/serie-v10/interiores-candidatos/integrado/interior-motorista-candidato-v01.png'}

def poly(shape,pts):
 m=np.zeros(shape,np.uint8);cv2.fillPoly(m,[np.asarray(pts,np.int32)],255);return m

def backdrop(name,size):
 studio=load_srgb(STUDIO)
 # Recorte exclusivamente da parede canônica, sem placa, teto, cantos ou piso.
 # No enquadramento fechado do painel a sala inteira não seria legível: ela
 # aparece como um plano neutro fora de foco, tal como numa captura real.
 if name=='painel-instrumentos':
  # Parede direita, longe da placa. O logo não deve surgir através do para-brisa
  # neste ângulo fechado, pois isso denuncia uma montagem artificial.
  box=(int(studio.width*.68),int(studio.height*.24),int(studio.width*.88),int(studio.height*.58))
  sigma=22
 else:
  box=(int(studio.width*.18),int(studio.height*.27),int(studio.width*.44),int(studio.height*.64))
  sigma=14
 crop=studio.crop(box).resize(size,Image.Resampling.LANCZOS)
 arr=np.asarray(crop,np.uint8)
 return cv2.GaussianBlur(arr,(0,0),sigma)

def mask_for(name,rgb):
 h,w=rgb.shape[:2];m=np.zeros((h,w),np.uint8)
 if name=='interior-amplo':
  m=poly((h,w),[(82,210),(1195,210),(1032,404),(178,404)])
  cv2.rectangle(m,(555,190),(760,335),0,-1) # retrovisor e console do teto
 elif name=='painel-instrumentos':
  # Limite geométrico da borda SUPERIOR do aro. Tudo abaixo dele permanece
  # fotografia original, eliminando o risco de a IA recriar volante/comandos.
  cx,cy,rx,ry=w*.50,h*.72,w*.57,h*.60
  xs=np.arange(w,dtype=np.float32)
  root=np.sqrt(np.clip(1-((xs-cx)/rx)**2,0,1))
  boundary=np.clip(cy-ry*root,0,h).astype(np.int32)
  for x,y in enumerate(boundary):
   m[:max(y-5,0),x]=255
  # Pequena janela visível dentro do aro: edita somente pixels claros do
  # exterior, protegendo integralmente couro, costura, painel e instrumentos.
  opening=poly((h,w),[(245,205),(1035,205),(1000,350),(280,350)])
  gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
  light=(gray>72).astype(np.uint8)*255
  light=cv2.morphologyEx(light,cv2.MORPH_CLOSE,np.ones((11,11),np.uint8))
  m=cv2.max(m,cv2.bitwise_and(opening,light))
 elif name=='interior-motorista':
  # O doador visual é usado somente para LOCALIZAR a parede clara, jamais para
  # fornecer RGB. A erosão e o corte superior mantêm folga de segurança nas
  # molduras, coluna A, retrovisor e painel da fotografia original.
  donor=np.asarray(load_srgb(VISUAL_DONORS[name]).resize((w,h),Image.Resampling.LANCZOS),np.uint8)
  hsv=cv2.cvtColor(donor,cv2.COLOR_RGB2HSV)
  yy=np.indices((h,w))[0]
  m=((hsv[:,:,1]<58)&(hsv[:,:,2]>145)&(yy<232)).astype(np.uint8)*255
  m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((7,7),np.uint8))
  m=cv2.erode(m,np.ones((11,11),np.uint8))
 m=cv2.GaussianBlur(m,(0,0),2.2 if name=='painel-instrumentos' else 4)
 return m.astype(np.float32)/255

def main():
 OUT.mkdir(parents=True,exist_ok=True);items=[];reports=[]
 for name,path in SOURCES.items():
  src=load_srgb(path);rgb=np.asarray(src,np.uint8);m=mask_for(name,rgb);bg=backdrop(name,src.size)
  # Mantém somente luminância de baixa frequência do exterior original. Isso
  # preserva a sensação óptica do vidro sem reintroduzir céu, árvores ou placas.
  original_gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
  original_gray=cv2.GaussianBlur(original_gray,(0,0),18)
  neutral=np.repeat(original_gray[...,None],3,axis=2)
  studio_view=srgb(linear(bg/255.0)*.95+linear(neutral/255.0)*.05)
  a=m[...,None];result=np.round(np.clip(studio_view*a+(rgb/255.0)*(1-a),0,1)*255).astype(np.uint8)
  result[m==0]=rgb[m==0]
  d=OUT/name;d.mkdir(parents=True,exist_ok=True);save_rgb(d/'preview.png',Image.fromarray(result));Image.fromarray(np.round(m*255).astype(np.uint8)).save(d/'mascara-exterior-vidros.png')
  changed=np.any(result!=rgb,axis=2);report={'id':name,'status':'preview_visual_approval_required','source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'studio_sha256':hashlib.sha256(STUDIO.read_bytes()).hexdigest(),'changed_pixels_outside_mask':int((changed&(m==0)).sum()),'interior_geometry_regenerated':False,'logo_inserted':False,'method':'blurred canonical off-white wall composited only through reviewed glass/exterior mask; 5% neutral low-frequency luminance retained'}
  (d/'qa-preview.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report);items.append((name,Image.fromarray(result)))
 # Grade de revisão
 canvas=Image.new('RGB',(1920,534),(24,27,31));draw=ImageDraw.Draw(canvas);font=ImageFont.load_default(size=17)
 for i,(name,im) in enumerate(items):
  tile=ImageOps.fit(im,(640,480),Image.Resampling.LANCZOS);canvas.paste(tile,(i*640,54));draw.text((i*640+14,17),f'INTERIOR | {name} | STUDIO CANONICO',fill='white',font=font)
 sheet=OUT/'serie-interiores-studio-canonico.jpg'
 save_rgb(sheet,canvas)
 save_rgb(OUT.parent/'02-previews-interiores.jpg',canvas)
 external_sheet=OUT.parent/'01-previews-externas.jpg'
 if external_sheet.exists():
  external=load_srgb(external_sheet)
  combined=Image.new('RGB',(1920,external.height+canvas.height),(24,27,31))
  combined.paste(external,(0,0));combined.paste(canvas,(0,external.height))
  save_rgb(OUT.parent/'03-serie-completa-previews.jpg',combined)
 (OUT/'qa-serie.json').write_text(json.dumps(reports,indent=2)+'\n');print(sheet)

if __name__=='__main__':main()
