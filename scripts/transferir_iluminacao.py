#!/usr/bin/env python3
"""Transfere luz ampla da geracao preservando o detalhe fotografico original."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageCms, ImageOps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--referencia-luz", type=Path, required=True)
    parser.add_argument("--mascara", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    parser.add_argument("--raio", type=float, default=28.0)
    parser.add_argument("--suavizacao-mascara", type=float, default=38.0)
    parser.add_argument("--ganho-detalhe", type=float, default=0.92)
    parser.add_argument("--forca", type=float, default=0.86)
    return parser.parse_args()


def load_rgb(path: Path) -> tuple[Image.Image, np.ndarray]:
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
    return image, np.asarray(image, dtype=np.float32)


def main() -> None:
    args = parse_args()
    original_image, original = load_rgb(args.original)
    reference_image, reference = load_rgb(args.referencia_luz)
    if reference_image.size != original_image.size:
        raise ValueError("Original e referencia de luz devem ter o mesmo tamanho")

    with Image.open(args.mascara) as mask_source:
        mask = ImageOps.exif_transpose(mask_source).convert("RGBA")
        if mask.size != original_image.size:
            raise ValueError("A mascara deve ter o mesmo tamanho das imagens")
        edit = 1.0 - np.asarray(mask.getchannel("A"), dtype=np.float32) / 255.0

    sigma = max(0.1, args.raio)
    original_low = cv2.GaussianBlur(original, (0, 0), sigmaX=sigma, sigmaY=sigma)
    reference_low = cv2.GaussianBlur(reference, (0, 0), sigmaX=sigma, sigmaY=sigma)
    original_detail = original - original_low

    # A referencia fornece apenas gradientes amplos; textura, linhas e microcontraste
    # continuam vindo da fotografia original.
    candidate = reference_low + original_detail * args.ganho_detalhe
    candidate = np.clip(candidate, 0, 255)

    edit = cv2.GaussianBlur(
        edit,
        (0, 0),
        sigmaX=max(0.1, args.suavizacao_mascara),
        sigmaY=max(0.1, args.suavizacao_mascara),
    )
    edit = np.clip(edit * args.forca, 0.0, 1.0)[:, :, None]
    output = original * (1.0 - edit) + candidate * edit

    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(output, 0, 255).astype(np.uint8)).save(
        args.saida,
        format="PNG",
        icc_profile=profile,
    )
    print(args.saida.resolve())


if __name__ == "__main__":
    main()
