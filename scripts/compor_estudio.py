#!/usr/bin/env python3
"""Compoe os pixels preservados do carro sobre uma placa-mestre fixa."""

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
    parser.add_argument("--fundo", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    parser.add_argument("--sombra-opacidade", type=float, default=0.22)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with Image.open(args.imagem) as source, Image.open(args.mascara) as mask_source, Image.open(args.fundo) as background_source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        mask = ImageOps.exif_transpose(mask_source).convert("RGBA")
        if image.size != mask.size:
            raise ValueError("Imagem e mascara devem ter o mesmo tamanho")
        background = ImageOps.fit(
            ImageOps.exif_transpose(background_source).convert("RGB"),
            image.size,
            method=Image.Resampling.LANCZOS,
        )

        foreground_np = np.asarray(image, dtype=np.float32)
        background_np = np.asarray(background, dtype=np.float32)
        alpha = np.asarray(mask.getchannel("A"), dtype=np.float32) / 255.0

        height, width = alpha.shape
        shadow = np.zeros((height, width), dtype=np.uint8)
        cv2.ellipse(
            shadow,
            (width // 2, int(height * 0.855)),
            (int(width * 0.34), int(height * 0.055)),
            0,
            0,
            360,
            255,
            -1,
        )
        shadow = cv2.GaussianBlur(shadow, (0, 0), sigmaX=45, sigmaY=28).astype(np.float32) / 255.0
        shadow_strength = np.clip(shadow * args.sombra_opacidade, 0.0, 0.5)
        background_np *= (1.0 - shadow_strength[:, :, None])

        output = foreground_np * alpha[:, :, None] + background_np * (1.0 - alpha[:, :, None])
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
