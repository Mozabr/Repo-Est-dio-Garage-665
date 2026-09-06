#!/usr/bin/env python3
"""Cria o master 4096x3072 sem inventar detalhes ou alterar o enquadramento."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageCms, ImageOps


MASTER_SIZE = (4096, 3072)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagem", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with Image.open(args.imagem) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        if image.width * 3 != image.height * 4:
            raise ValueError(f"A entrada precisa ser 4:3; recebido {image.size}")
        master = image.resize(MASTER_SIZE, Image.Resampling.LANCZOS)
        profile = source.info.get("icc_profile") or ImageCms.ImageCmsProfile(
            ImageCms.createProfile("sRGB")
        ).tobytes()
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    master.save(args.saida, format="PNG", icc_profile=profile)
    print(args.saida.resolve())


if __name__ == "__main__":
    main()
