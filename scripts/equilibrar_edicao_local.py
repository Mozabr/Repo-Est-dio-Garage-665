"""Balance a contained local edit with the original source in linear sRGB."""
from pathlib import Path
import argparse,json
import cv2,numpy as np
from PIL import Image
from studio_common import load_srgb,linear,srgb,save_rgb
ROOT=Path(__file__).resolve().parents[1]
def stats(rgb,sel):
 lab=cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB).astype(np.float32)
 return [float(lab[:,:,i][sel].mean()) for i in range(3)]
def main():
 p=argparse.ArgumentParser();p.add_argument("--original",type=Path,required=True);p.add_argument("--treated",type=Path,required=True);p.add_argument("--mask",type=Path,required=True);p.add_argument("--share",type=float,required=True);p.add_argument("--output",type=Path,required=True);p.add_argument("--report",type=Path,required=True);a=p.parse_args()
 if not 0<=a.share<=1:raise ValueError("share must be 0..1")
 original=np.asarray(load_srgb(a.original));treated=np.asarray(load_srgb(a.treated));mask=np.asarray(Image.open(a.mask).convert("L"),np.float32)/255
 strength=mask*a.share
 mixed=srgb(linear(original/255)*(1-strength[:,:,None])+linear(treated/255)*strength[:,:,None])
 result=np.round(np.clip(mixed,0,1)*255).astype(np.uint8);result[mask==0]=original[mask==0]
 assert np.array_equal(result[mask==0],original[mask==0])
 sel=mask>.5;s0=stats(original,sel);s1=stats(result,sel)
 report={"status":"balanced_not_visually_approved","treatment_share":a.share,"original_share":1-a.share,"blend_space":"linear sRGB","delta_Lab_mean":[s1[i]-s0[i] for i in range(3)],"changed_pixels_outside_mask":0}
 a.output.parent.mkdir(parents=True,exist_ok=True);save_rgb(a.output,Image.fromarray(result));a.report.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=="__main__":main()

