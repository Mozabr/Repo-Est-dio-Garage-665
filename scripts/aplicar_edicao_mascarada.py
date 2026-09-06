#!/usr/bin/env python3
"""Aplica uma resposta gerada somente na area transparente de uma mascara."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--gerada", type=Path, required=True)
    parser.add_argument("--mascara", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with Image.open(args.original) as original_source, Image.open(args.gerada) as generated_source, Image.open(
        args.mascara
    ) as mask_source:
        original = ImageOps.exif_transpose(original_source).convert("RGB")
        generated = ImageOps.exif_transpose(generated_source).convert("RGB")
        mask = ImageOps.exif_transpose(mask_source).convert("RGBA")
        if not (original.size == generated.size == mask.size):
            raise ValueError("Original, gerada e mascara devem ter o mesmo tamanho")
        edit_alpha = mask.getchannel("A").point(lambda value: 255 - value)
        output = Image.composite(generated, original, edit_alpha)
        profile = original_source.info.get("icc_profile")
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.saida, format="PNG", icc_profile=profile)
    print(args.saida.resolve())


if __name__ == "__main__":
    main()
