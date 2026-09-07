#!/usr/bin/env python3
"""Merge independent crop-space side-panel corrections onto the approved v25 frame."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]


def parse_item(value: str) -> tuple[str, Path, Path]:
    parts = value.split("=", 2)
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Use ID=CANDIDATE_PATH=MASK_PATH")
    return parts[0], Path(parts[1]), Path(parts[2])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/rig-material-lateral-v6f.json")
    parser.add_argument("--surface", action="append", type=parse_item, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text())
    base = np.asarray(Image.open(ROOT / cfg["full_frame_base"]).convert("RGB"), dtype=np.float32)
    authority_crop = np.asarray(Image.open(ROOT / cfg["source_crop"]).convert("RGB"), dtype=np.float32)
    box = tuple(cfg["crop_source_xyxy"])
    crop_size = (authority_crop.shape[1], authority_crop.shape[0])
    delta_sum = np.zeros_like(authority_crop)
    weight_sum = np.zeros(authority_crop.shape[:2], dtype=np.float32)
    items = []
    for surface_id, candidate_path, mask_path in args.surface:
        candidate = np.asarray(Image.open(candidate_path).convert("RGB").resize(crop_size, Image.Resampling.LANCZOS), dtype=np.float32)
        mask = np.asarray(Image.open(mask_path).convert("L").resize(crop_size, Image.Resampling.LANCZOS), dtype=np.float32) / 255.0
        delta_sum += (candidate - authority_crop) * mask[:, :, None]
        weight_sum += mask
        items.append({"id": surface_id, "editable_pixels": int((mask > 0).sum())})
    normalized_delta = delta_sum / np.maximum(weight_sum[:, :, None], 1.0)
    crop_delta = normalized_delta * np.clip(weight_sum, 0, 1)[:, :, None]
    output = base.copy()
    region = output[box[1]:box[3], box[0]:box[2]]
    full_size = (box[2] - box[0], box[3] - box[1])
    resized_delta = cv2.resize(crop_delta, full_size, interpolation=cv2.INTER_LANCZOS4)
    full_weight = cv2.resize(np.clip(weight_sum, 0, 1), full_size, interpolation=cv2.INTER_LANCZOS4)
    full_weight = np.clip(full_weight, 0, 1)
    region += resized_delta * full_weight[:, :, None]
    output[box[1]:box[3], box[0]:box[2]] = region
    output = np.round(output).clip(0, 255).astype(np.uint8)
    changed = np.any(output != base.astype(np.uint8), axis=2)
    full_union = np.zeros(base.shape[:2], dtype=bool)
    full_union[box[1]:box[3], box[0]:box[2]] = full_weight > 0
    output[~full_union] = base.astype(np.uint8)[~full_union]
    if np.any(changed & ~full_union):
        raise AssertionError("Pixels changed outside lateral union")
    report = {
        "status": "combined_lateral_candidate_visual_approval_required",
        "base": cfg["full_frame_base"],
        "surfaces": items,
        "preserved_source_surface": "M13-paralama-proximo",
        "changed_pixels_outside_lateral_union": 0,
        "geometry_transform_used": False,
        "overlap_pixels_normalized": int((weight_sum > 1.0).sum())
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.fromarray(output).save(args.output, format="PNG", icc_profile=profile)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
