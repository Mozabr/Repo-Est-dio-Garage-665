#!/usr/bin/env python3
"""Technical gate for the Studio H empty photo-bay candidate."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def region_stats(rgb: np.ndarray, box: tuple[float, float, float, float]) -> dict:
    h, w = rgb.shape[:2]
    x0, y0, x1, y1 = box
    crop = rgb[round(y0*h):round(y1*h), round(x0*w):round(x1*w)]
    lightness = cv2.cvtColor(crop, cv2.COLOR_RGB2LAB)[:, :, 0]
    return {
        "mean_rgb": [round(float(v), 3) for v in crop.mean(axis=(0, 1))],
        "mean_L": round(float(lightness.mean()), 3),
        "std_L": round(float(lightness.std()), 3),
        "clipped_white_percent": round(float(np.all(crop >= 250, axis=2).mean() * 100), 5)
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--studio", type=Path, default=ROOT / "estudio-mestre/STUDIO_H-photo-bay-v06-oficial.png")
    parser.add_argument("--metadata", type=Path, default=ROOT / "estudio-mestre/STUDIO_H-photo-bay-v06-oficial.json")
    parser.add_argument("--output", type=Path, default=ROOT / "estudio-mestre/STUDIO_H-photo-bay-v06-qa.json")
    args = parser.parse_args()
    rgb = np.asarray(Image.open(args.studio).convert("RGB"))
    metadata = json.loads(args.metadata.read_text())
    stats = {
        "ceiling": region_stats(rgb, (0, 0, 1, .17)),
        "wall": region_stats(rgb, (.08, .20, .92, .62)),
        "floor": region_stats(rgb, (0, .68, 1, 1)),
        "left_wall": region_stats(rgb, (.05, .20, .35, .62)),
        "right_wall": region_stats(rgb, (.65, .20, .95, .62))
    }
    left_right_delta = stats["left_wall"]["mean_L"] - stats["right_wall"]["mean_L"]
    wall_floor_delta = stats["wall"]["mean_L"] - stats["floor"]["mean_L"]
    checks = {
        "master_is_4096x3072": [rgb.shape[1], rgb.shape[0]] == [4096, 3072],
        "no_clipped_white_in_ceiling_sample": stats["ceiling"]["clipped_white_percent"] < .1,
        "floor_is_darker_than_wall": wall_floor_delta >= 8,
        "floor_is_not_crushed_or_mirror_bright": 155 <= stats["floor"]["mean_L"] <= 195,
        "left_key_is_visible_in_wall_gradient": 6 <= left_right_delta <= 28,
        "logo_artwork_not_regenerated": metadata["logo_regenerated"] is False,
        "logo_is_matte_physical": metadata["logo_finish"] == "matte_physical",
        "logo_has_wall_standoff_mounting": "standoffs" in metadata["mounting"]
    }
    report = {
        "status": "technical_pass_visual_approval_required" if all(checks.values()) else "rejected",
        "studio_sha256": hashlib.sha256(args.studio.read_bytes()).hexdigest(),
        "rig": "GARAGE665-RIG-V6-B",
        "stats": stats,
        "derived": {"left_minus_right_L": round(left_right_delta, 3), "wall_minus_floor_L": round(wall_floor_delta, 3)},
        "checks": checks,
        "limitations": [
            "The 4096x3072 master is a deterministic upscale from a 1448x1086 generated base.",
            "This audit validates the empty studio, not the vehicle reflections.",
            "The room remains a candidate until human visual approval."
        ]
    }
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if report["status"] == "rejected":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
