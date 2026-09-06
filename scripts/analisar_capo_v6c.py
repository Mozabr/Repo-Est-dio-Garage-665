#!/usr/bin/env python3
"""Measure the photographed hood before a paid relighting call."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--mask", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rgb = np.asarray(Image.open(args.image).convert("RGB"), dtype=np.uint8)
    strength = np.asarray(Image.open(args.mask).convert("L"), dtype=np.float32) / 255.0
    if strength.shape != rgb.shape[:2]:
        raise ValueError("Mask and image dimensions differ")
    selected = strength >= 0.5
    ys, xs = np.nonzero(selected)
    if not len(xs):
        raise ValueError("Mask has no editable pixels")

    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    luminance = lab[:, :, 0]
    chroma = np.sqrt(np.square(lab[:, :, 1] - 128) + np.square(lab[:, :, 2] - 128))
    broad_luminance = cv2.GaussianBlur(luminance, (0, 0), 8.0)
    gx = cv2.Sobel(broad_luminance, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(broad_luminance, cv2.CV_32F, 0, 1, ksize=3)
    gradient = np.sqrt(gx * gx + gy * gy)

    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    width, height = max(1, x1 - x0 + 1), max(1, y1 - y0 + 1)
    nx = (np.arange(rgb.shape[1])[None, :] - x0) / width
    ny = (np.arange(rgb.shape[0])[:, None] - y0) / height
    zones = {
        "windshield_side": selected & (ny < 1 / 3),
        "middle": selected & (ny >= 1 / 3) & (ny < 2 / 3),
        "nose_side": selected & (ny >= 2 / 3),
        "camera_left": selected & (nx < 1 / 3),
        "center": selected & (nx >= 1 / 3) & (nx < 2 / 3),
        "camera_right": selected & (nx >= 2 / 3),
    }

    def stats(selector: np.ndarray) -> dict[str, float | int]:
        l = luminance[selector]
        c = chroma[selector]
        g = gradient[selector]
        return {
            "pixels": int(selector.sum()),
            "Lab_L_mean": round(float(l.mean()), 3),
            "Lab_L_p05": round(float(np.percentile(l, 5)), 3),
            "Lab_L_p95": round(float(np.percentile(l, 95)), 3),
            "Lab_L_dynamic_range_p95_p05": round(float(np.percentile(l, 95) - np.percentile(l, 5)), 3),
            "Lab_chroma_mean": round(float(c.mean()), 3),
            "broad_gradient_p95": round(float(np.percentile(g, 95)), 3),
        }

    high_threshold = float(np.percentile(broad_luminance[selected], 90))
    high = ((broad_luminance >= high_threshold) & selected).astype(np.uint8)
    components, labels, component_stats, _ = cv2.connectedComponentsWithStats(high, connectivity=8)
    areas = sorted(
        (int(component_stats[index, cv2.CC_STAT_AREA]) for index in range(1, components)),
        reverse=True,
    )
    report = {
        "status": "measured_before_relighting_not_visual_approval",
        "image": str(args.image),
        "mask": str(args.mask),
        "bounds_xyxy": [x0, y0, x1, y1],
        "editable_pixels_at_50_percent": int(selected.sum()),
        "whole_hood": stats(selected),
        "zones": {name: stats(zone) for name, zone in zones.items() if zone.any()},
        "brightest_decile": {
            "broad_Lab_L_threshold": round(high_threshold, 3),
            "connected_regions": len(areas),
            "largest_region_pixels": areas[0] if areas else 0,
        },
        "interpretation_limits": [
            "These measurements describe the pixels; semantic outdoor reflections require visual review.",
            "They do not identify the physical Porsche paint color without a calibrated color target.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
