#!/usr/bin/env python3
"""Normaliza a foto 4:3 para o tamanho de trabalho da edicao mascarada."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageCms, ImageOps


WORK_SIZE = (3264, 2448)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("origem", type=Path)
    parser.add_argument("saida", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(args.origem) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        ratio = image.width / image.height
        if abs(ratio - (4 / 3)) > 0.005:
            raise ValueError("A entrada nao e 4:3. Faca o enquadramento manual sem cortar o veiculo")
        image = image.resize(WORK_SIZE, Image.Resampling.LANCZOS)
        icc = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
        image.save(args.saida, format="PNG", icc_profile=icc)
    print(args.saida.resolve())


if __name__ == "__main__":
    main()
