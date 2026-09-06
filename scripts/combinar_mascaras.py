#!/usr/bin/env python3
"""Combina mascaras RGBA mantendo a convencao: transparente = editavel."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms, ImageOps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagem", type=Path, required=True)
    parser.add_argument("--uniao-editavel", type=Path, action="append", required=True)
    parser.add_argument(
        "--limitar-editavel-a",
        type=Path,
        action="append",
        default=[],
        help="A edicao final fica restrita tambem as areas transparentes destas mascaras",
    )
    parser.add_argument("--mascara", type=Path, required=True)
    parser.add_argument("--preview", type=Path, required=True)
    return parser.parse_args()


def alpha_from(path: Path, size: tuple[int, int]) -> np.ndarray:
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("RGBA")
        if image.size != size:
            raise ValueError(f"Mascara {path} tem tamanho {image.size}; esperado {size}")
        return np.asarray(image.getchannel("A"), dtype=np.uint8)


def main() -> None:
    args = parse_args()
    with Image.open(args.imagem) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
    image_np = np.asarray(image, dtype=np.float32)

    alpha = np.full((image.height, image.width), 255, dtype=np.uint8)
    for path in args.uniao_editavel:
        alpha = np.minimum(alpha, alpha_from(path, image.size))
    for path in args.limitar_editavel_a:
        alpha = np.maximum(alpha, alpha_from(path, image.size))

    rgba = np.full((image.height, image.width, 4), 255, dtype=np.uint8)
    rgba[:, :, 3] = alpha
    strength = (255.0 - alpha.astype(np.float32)) / 255.0
    magenta = np.zeros_like(image_np)
    magenta[:, :, :] = (210, 40, 180)
    mix = strength[:, :, None] * 0.65
    preview = image_np * (1.0 - mix) + magenta * mix

    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    args.mascara.parent.mkdir(parents=True, exist_ok=True)
    args.preview.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba).save(args.mascara, format="PNG", icc_profile=profile)
    Image.fromarray(np.clip(preview, 0, 255).astype(np.uint8)).save(
        args.preview, format="JPEG", quality=94, icc_profile=profile
    )
    print(args.mascara.resolve())
    print(args.preview.resolve())


if __name__ == "__main__":
    main()
