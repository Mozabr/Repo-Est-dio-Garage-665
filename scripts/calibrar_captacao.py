"""Detect a real ColorChecker and estimate an optional, explicit linear colour matrix.

Default detection uses segmentation (BSD), not the YOLO/AGPL inference path.
Fit mode requires known corresponding reference swatches under chosen illuminant.
Never infer a physical paint reference from a JPEG's mean colour.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import colour
from colour_checker_detection import detect_colour_checkers_segmentation
from studio_common import load_srgb, linear

def main():
    p=argparse.ArgumentParser()
    p.add_argument("imagem",type=Path)
    p.add_argument("--saida",type=Path,required=True)
    p.add_argument("--referencia-srgb",type=Path,help="JSON with 24 corresponding reference sRGB patches in [0,1]")
    args=p.parse_args()
    rgb=np.asarray(load_srgb(args.imagem),np.float32)/255
    detections=detect_colour_checkers_segmentation(rgb)
    report={"source":str(args.imagem),"method":"segmentation","charts_detected":len(detections),"calibration_applied":False}
    if len(detections)==1:
        patches=np.asarray(detections[0],float)
        report["sampled_srgb"]=patches.tolist()
        if args.referencia_srgb:
            reference=np.asarray(json.loads(args.referencia_srgb.read_text()),float)
            if reference.shape!=(24,3) or not np.isfinite(reference).all() or (reference<0).any() or (reference>1).any():
                raise ValueError("Reference must be 24x3 sRGB swatches in [0,1]")
            matrix=colour.matrix_colour_correction(linear(patches),linear(reference),method="Cheung 2004",terms=3)
            predicted=colour.algebra.vector_dot(matrix,linear(patches))
            errors=colour.delta_E(colour.XYZ_to_Lab(colour.sRGB_to_XYZ(colour.cctf_encoding(predicted))),colour.XYZ_to_Lab(colour.sRGB_to_XYZ(reference)),method="CIE 2000")
            report.update({"matrix_linear_rgb":matrix.tolist(),"delta_e_fit_median":float(np.median(errors)),"status":"fit_only_requires_holdout_chart_validation"})
    elif len(detections)>1:
        report["status"]="multiple_charts_select_one_before_calibration"
    else:
        report["status"]="no_chart_no_colour_calibration"
    args.saida.parent.mkdir(parents=True,exist_ok=True)
    args.saida.write_text(json.dumps(report,indent=2))
    print(args.saida)

if __name__=="__main__":
    main()
