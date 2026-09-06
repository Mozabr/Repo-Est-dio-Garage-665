#!/usr/bin/env python3
"""Relight the hood without generating, moving or replacing any vehicle element."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/relighting-capo-v6d.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text())
    controls = cfg["controls"]
    source_path = ROOT / cfg["source"]
    mask_path = ROOT / cfg["mask"]
    source_image = Image.open(source_path).convert("RGB")
    rgb = np.asarray(source_image, dtype=np.uint8)
    strength = np.asarray(Image.open(mask_path).convert("L"), dtype=np.float32) / 255.0
    if strength.shape != rgb.shape[:2]:
        raise ValueError("Source and mask dimensions differ")

    core = strength >= 0.5
    ys, xs = np.nonzero(core)
    if not len(xs):
        raise ValueError("Hood mask is empty")
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    width, height = max(1, x1 - x0), max(1, y1 - y0)
    xx = np.arange(rgb.shape[1], dtype=np.float32)[None, :]
    yy = np.arange(rgb.shape[0], dtype=np.float32)[:, None]
    u = (xx - x0) / width
    v = (yy - y0) / height

    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    broad = cv2.GaussianBlur(lab, (0, 0), controls["broad_blur_sigma"])
    micro_blurred = cv2.GaussianBlur(lab, (0, 0), controls["micro_blur_sigma"])
    micro = lab - micro_blurred

    base_L = float(np.percentile(lab[:, :, 0][core], controls["base_percentile_L"]))
    broad_median_L = float(np.median(broad[:, :, 0][core]))
    retained_shape = (broad[:, :, 0] - broad_median_L) * controls["original_broad_shape_retention"]

    center_u = (
        controls["key_center_u_at_windshield"] * (1 - v)
        + controls["key_center_u_at_nose"] * v
    )
    key = np.exp(-0.5 * np.square((u - center_u) / controls["key_width_u"]))
    key *= np.exp(-0.5 * np.square((v - controls["key_center_v"]) / controls["key_height_v"]))
    left_fill = np.clip(1 - u, 0, 1) * controls["left_fill_amplitude_L"]
    nose_rolloff = np.clip(v, 0, 1) * controls["nose_rolloff_L"]
    target_L = base_L + retained_shape + key * controls["key_amplitude_L"] + left_fill + nose_rolloff
    target_L += np.clip(micro[:, :, 0], -controls["micro_clip_L"], controls["micro_clip_L"]) * controls["micro_retention"]

    target = lab.copy()
    target[:, :, 0] = target_L
    for channel in (1, 2):
        median = float(np.median(broad[:, :, channel][core]))
        target[:, :, channel] = median + (broad[:, :, channel] - median) * controls["chroma_broad_retention"]
        target[:, :, channel] += np.clip(
            micro[:, :, channel], -controls["chroma_micro_clip"], controls["chroma_micro_clip"]
        ) * controls["chroma_micro_retention"]

    relit = cv2.cvtColor(np.clip(target, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
    alpha = np.clip(strength, 0, 1)[:, :, None]
    output = np.round(rgb * (1 - alpha) + relit * alpha).astype(np.uint8)
    outside = strength == 0
    output[outside] = rgb[outside]
    if not np.array_equal(output[outside], rgb[outside]):
        raise AssertionError("Pixel containment failed")

    output_lab = cv2.cvtColor(output, cv2.COLOR_RGB2LAB).astype(np.float32)
    l_values = output_lab[:, :, 0][core]
    changed = np.any(output != rgb, axis=2)
    report = {
        "status": "deterministic_candidate_visual_approval_required",
        "method": cfg["method"],
        "source_sha256": sha(source_path),
        "mask_sha256": sha(mask_path),
        "generated_rgb_used": False,
        "geometry_transform_used": False,
        "changed_pixels_outside_mask": int((changed & outside).sum()),
        "changed_pixels_inside_mask": int((changed & ~outside).sum()),
        "wheel_pixels_changed": 0,
        "license_plate_cover_pixels_changed": 0,
        "studio_pixels_changed": 0,
        "hood_Lab_L_mean": round(float(l_values.mean()), 3),
        "hood_Lab_L_p05": round(float(np.percentile(l_values, 5)), 3),
        "hood_Lab_L_p95": round(float(np.percentile(l_values, 95)), 3),
        "hood_Lab_L_p95_minus_p05": round(float(np.percentile(l_values, 95) - np.percentile(l_values, 5)), 3),
        "base_L_from_source_percentile": base_L,
        "controls": controls,
        "note": "Only masked Lab illumination/material response changed; every pixel outside the reviewed hood mask is copied from the base image."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.fromarray(output).save(args.output, format="PNG", icc_profile=profile)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
