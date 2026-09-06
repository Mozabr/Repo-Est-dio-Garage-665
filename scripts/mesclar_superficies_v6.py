#!/usr/bin/env python3
"""Merge independently approved surface edits without cumulative regeneration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms


def parse_item(value: str) -> tuple[str, Path, Path]:
    parts = value.split("=", 2)
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Use ID=CANDIDATE_PATH=MASK_PATH")
    return parts[0], Path(parts[1]), Path(parts[2])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--surface", action="append", type=parse_item, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    original = np.asarray(Image.open(args.original).convert("RGB"), dtype=np.float32)
    delta_sum = np.zeros_like(original)
    weight_sum = np.zeros(original.shape[:2], dtype=np.float32)
    items = []
    for surface_id, candidate_path, mask_path in args.surface:
        candidate = np.asarray(Image.open(candidate_path).convert("RGB"), dtype=np.float32)
        mask = np.asarray(Image.open(mask_path).convert("L"), dtype=np.float32) / 255.0
        if candidate.shape != original.shape or mask.shape != original.shape[:2]:
            raise ValueError(f"Size mismatch for {surface_id}")
        delta_sum += (candidate - original) * mask[:, :, None]
        weight_sum += mask
        items.append({"id": surface_id, "candidate": str(candidate_path), "mask": str(mask_path), "editable_pixels": int((mask > 0).sum())})
    normalized_delta = delta_sum / np.maximum(weight_sum[:, :, None], 1.0)
    union_strength = np.clip(weight_sum, 0, 1)[:, :, None]
    output = np.round(original + normalized_delta * union_strength).clip(0, 255).astype(np.uint8)
    outside = weight_sum == 0
    output[outside] = original.astype(np.uint8)[outside]
    if not np.array_equal(output[outside], original.astype(np.uint8)[outside]):
        raise AssertionError("Pixel containment failed")
    report = {
        "status": "merged_not_visually_approved",
        "method": "normalized_non_accumulative_delta_merge",
        "surface_count": len(items),
        "surfaces": items,
        "union_pixels": int((weight_sum > 0).sum()),
        "transition_overlap_pixels": int((weight_sum > 1).sum()),
        "changed_pixels_outside_union": 0
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.fromarray(output).save(args.output, format="PNG", icc_profile=profile)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
