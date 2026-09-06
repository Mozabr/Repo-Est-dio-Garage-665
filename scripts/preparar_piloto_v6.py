#!/usr/bin/env python3
"""Create the immutable 2048x1536 working copies used by the v6 pilot."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "trabalhos/panamera/studio-v2/dianteira-3-4/source-srgb.png"
DEFAULT_ALPHA = ROOT / "trabalhos/panamera/studio-v2/dianteira-3-4/alpha-final.png"
DEFAULT_OUT = ROOT / "trabalhos/panamera/refinamento-dianteira-v6/entrada"
WORK_SIZE = (2048, 1536)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--alpha", type=Path, default=DEFAULT_ALPHA)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    source_out = args.out / "source-2048x1536.png"
    alpha_out = args.out / "alpha-2048x1536.png"
    icc = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    with Image.open(args.source) as src:
        rgb = src.convert("RGB")
        if abs(rgb.width / rgb.height - 4 / 3) > 0.005:
            raise ValueError("Source must be 4:3; no automatic crop is permitted")
        rgb.resize(WORK_SIZE, Image.Resampling.LANCZOS).save(source_out, icc_profile=icc)
    with Image.open(args.alpha) as src_alpha:
        src_alpha.convert("L").resize(WORK_SIZE, Image.Resampling.LANCZOS).save(alpha_out)
    report = {
        "status": "prepared",
        "source_original": str(args.source),
        "source_original_sha256": digest(args.source),
        "alpha_original_sha256": digest(args.alpha),
        "work_size": list(WORK_SIZE),
        "source_work_sha256": digest(source_out),
        "alpha_work_sha256": digest(alpha_out),
        "crop_performed": False,
        "source_pixels_modified": False,
        "note": "The working copy is resized; the authority source remains untouched."
    }
    (args.out / "preparo.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
