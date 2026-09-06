#!/usr/bin/env python3
"""Remove blocos de luz mantendo microtextura e detalhes finos da pintura."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageCms, ImageOps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagem", type=Path, required=True)
    parser.add_argument("--mascara", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    parser.add_argument("--raio-gradiente", type=float, default=110.0)
    parser.add_argument("--raio-detalhe", type=float, default=4.0)
    parser.add_argument("--suavizacao-mascara", type=float, default=10.0)
    parser.add_argument("--ganho-detalhe", type=float, default=0.92)
    parser.add_argument("--forca", type=float, default=0.88)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with Image.open(args.imagem) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        source_profile = source.info.get("icc_profile")
    with Image.open(args.mascara) as mask_source:
        mask = ImageOps.exif_transpose(mask_source).convert("RGBA")
        if mask.size != image.size:
            raise ValueError("Imagem e mascara devem ter o mesmo tamanho")

    pixels = np.asarray(image, dtype=np.float32)
    broad = cv2.GaussianBlur(
        pixels, (0, 0), sigmaX=args.raio_gradiente, sigmaY=args.raio_gradiente
    )
    detail_base = cv2.GaussianBlur(
        pixels, (0, 0), sigmaX=args.raio_detalhe, sigmaY=args.raio_detalhe
    )
    fine_detail = pixels - detail_base
    candidate = np.clip(broad + fine_detail * args.ganho_detalhe, 0, 255)

    edit = 1.0 - np.asarray(mask.getchannel("A"), dtype=np.float32) / 255.0
    edit = cv2.GaussianBlur(
        edit,
        (0, 0),
        sigmaX=args.suavizacao_mascara,
        sigmaY=args.suavizacao_mascara,
    )
    edit = np.clip(edit * args.forca, 0, 1)[:, :, None]
    output = pixels * (1.0 - edit) + candidate * edit

    profile = source_profile or ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(output, 0, 255).astype(np.uint8)).save(
        args.saida, format="PNG", icc_profile=profile
    )
    print(args.saida.resolve())


if __name__ == "__main__":
    main()
