#!/usr/bin/env python3
"""Deriva Feed, Story horizontal e Webmotors do mesmo master aprovado."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageCms, ImageOps


MASTER_SIZE = (4096, 3072)
FORMATS = {
    "feed-4096x3072.jpg": ((4096, 3072), 95),
    "story-horizontal-3840x2160.jpg": ((3840, 2160), 95),
    "webmotors-1920x1440.jpg": ((1920, 1440), 94),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("master", type=Path)
    parser.add_argument("--saida", type=Path, required=True)
    return parser.parse_args()


def srgb_bytes() -> bytes:
    return ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()


def main() -> None:
    args = parse_args()
    args.saida.mkdir(parents=True, exist_ok=True)
    with Image.open(args.master) as source:
        master = ImageOps.exif_transpose(source).convert("RGB")
        if master.size != MASTER_SIZE:
            raise ValueError(f"O master deve medir {MASTER_SIZE[0]}x{MASTER_SIZE[1]}; recebido {master.size}")

        for filename, (size, quality) in FORMATS.items():
            if size == (3840, 2160):
                output = ImageOps.fit(master, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            else:
                output = master.resize(size, Image.Resampling.LANCZOS)
            output.save(
                args.saida / filename,
                format="JPEG",
                quality=quality,
                subsampling=0,
                optimize=True,
                icc_profile=srgb_bytes(),
            )
            print((args.saida / filename).resolve())


if __name__ == "__main__":
    main()
