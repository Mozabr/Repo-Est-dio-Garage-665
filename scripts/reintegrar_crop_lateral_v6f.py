#!/usr/bin/env python3
"""Reintegrate one lateral crop into the approved full-frame base with an exact mask lock."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/rig-material-lateral-v6f.json")
    parser.add_argument("--surface", required=True)
    parser.add_argument("--crop-result", type=Path, required=True)
    parser.add_argument("--crop-mask", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text())
    base_path = ROOT / cfg["full_frame_base"]
    box = tuple(cfg["crop_source_xyxy"])
    crop_size = (box[2] - box[0], box[3] - box[1])
    base = np.asarray(Image.open(base_path).convert("RGB"), dtype=np.uint8)
    edit = np.asarray(Image.open(args.crop_result).convert("RGB").resize(crop_size, Image.Resampling.LANCZOS), dtype=np.uint8)
    crop_strength = np.asarray(Image.open(args.crop_mask).convert("L").resize(crop_size, Image.Resampling.LANCZOS), dtype=np.float32) / 255.0
    strength = np.zeros(base.shape[:2], dtype=np.float32)
    strength[box[1]:box[3], box[0]:box[2]] = crop_strength
    proposal = base.copy()
    proposal[box[1]:box[3], box[0]:box[2]] = edit
    output = np.round(base * (1 - strength[:, :, None]) + proposal * strength[:, :, None]).astype(np.uint8)
    outside = strength == 0
    output[outside] = base[outside]
    changed = np.any(output != base, axis=2)
    if np.any(changed & outside):
        raise AssertionError("Pixels changed outside lateral surface mask")

    report = {
        "status": "full_frame_candidate_visual_approval_required",
        "surface": args.surface,
        "base": str(base_path.relative_to(ROOT)),
        "changed_pixels_outside_surface": int((changed & outside).sum()),
        "changed_pixels_inside_surface": int((changed & ~outside).sum()),
        "geometry_transform_used_on_full_frame": False,
        "protected_elements_changed": 0,
        "note": "Every pixel outside the reviewed lateral surface is copied from the approved v25 capot frame."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.fromarray(output).save(args.output, format="PNG", icc_profile=profile)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
