#!/usr/bin/env python3
"""Aplica o logo oficial como placa de parede, sem qualquer regeneracao."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOGO = ROOT / "assets" / "logo-garage-665-transparente.png"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagem", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    parser.add_argument("--logo", type=Path, default=DEFAULT_LOGO)
    parser.add_argument("--largura", type=int, default=700, help="Largura visivel no master 4K")
    parser.add_argument("--centro-x", type=int, default=2048)
    parser.add_argument("--topo", type=int, default=300)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with Image.open(args.imagem) as background_source, Image.open(args.logo) as logo_source:
        background = ImageOps.exif_transpose(background_source).convert("RGBA")
        logo = ImageOps.exif_transpose(logo_source).convert("RGBA")
        bbox = logo.getchannel("A").getbbox()
        if not bbox:
            raise ValueError("O logo nao possui pixels visiveis")
        logo = logo.crop(bbox)
        height = round(logo.height * args.largura / logo.width)
        logo = logo.resize((args.largura, height), Image.Resampling.LANCZOS)
        x = args.centro_x - logo.width // 2
        y = args.topo
        if x < 0 or y < 0 or x + logo.width > background.width or y + logo.height > background.height:
            raise ValueError("O logo ultrapassa os limites da imagem")

        shadow_alpha = logo.getchannel("A").filter(ImageFilter.GaussianBlur(13))
        shadow_alpha = shadow_alpha.point(lambda value: round(value * 0.30))
        shadow = Image.new("RGBA", logo.size, (18, 16, 14, 0))
        shadow.putalpha(shadow_alpha)
        background.alpha_composite(shadow, (x + 13, y + 16))
        background.alpha_composite(logo, (x, y))
        output = background.convert("RGB")
        profile = background_source.info.get("icc_profile")

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.saida, format="PNG", icc_profile=profile)
    print(args.saida.resolve())


if __name__ == "__main__":
    main()
