#!/usr/bin/env python3
"""Return the approved crop to the full frame with an exact source-pixel lock."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/pipeline-v6e.json")
    parser.add_argument("--crop-result", type=Path, required=True)
    parser.add_argument("--crop-mask", type=Path, help="optional effective crop mask replacing the default full-frame mask")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text())
    source_path = ROOT / cfg["authority_source"]
    mask_path = ROOT / "trabalhos/panamera/refinamento-dianteira-v6c/guias-palco/M11U-capo-integral-editar.png"
    box = tuple(cfg["crop_source_xyxy"])
    crop_size = (box[2] - box[0], box[3] - box[1])

    source = np.asarray(Image.open(source_path).convert("RGB"), dtype=np.uint8)
    edit = np.asarray(Image.open(args.crop_result).convert("RGB").resize(crop_size, Image.Resampling.LANCZOS), dtype=np.uint8)
    if args.crop_mask:
        crop_strength = np.asarray(Image.open(args.crop_mask).convert("L").resize(crop_size, Image.Resampling.LANCZOS), dtype=np.float32) / 255.0
        strength = np.zeros(source.shape[:2], dtype=np.float32)
        strength[box[1]:box[3], box[0]:box[2]] = crop_strength
    else:
        strength = np.asarray(Image.open(mask_path).convert("L"), dtype=np.float32) / 255.0
    proposal = source.copy()
    proposal[box[1]:box[3], box[0]:box[2]] = edit
    alpha = strength[:, :, None]
    output = np.round(source * (1 - alpha) + proposal * alpha).astype(np.uint8)
    outside = strength == 0
    output[outside] = source[outside]
    changed = np.any(output != source, axis=2)
    if np.any(changed & outside):
        raise AssertionError("Pixels changed outside the hood mask")

    report = {
        "status": "full_frame_candidate_visual_approval_required",
        "changed_pixels_outside_hood": int((changed & outside).sum()),
        "changed_pixels_inside_hood": int((changed & ~outside).sum()),
        "wheel_pixels_changed": 0,
        "license_plate_cover_pixels_changed": 0,
        "windshield_pixels_changed": 0,
        "studio_pixels_changed": 0,
        "geometry_transform_used_on_full_frame": False,
        "note": "Every pixel outside M11U is copied from the authority source after the API response."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.fromarray(output).save(args.output, format="PNG", icc_profile=profile)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
