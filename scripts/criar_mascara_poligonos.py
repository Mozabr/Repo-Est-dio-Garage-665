#!/usr/bin/env python3
"""Cria mascara alfa auditavel a partir de regioes poligonais editaveis."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms, ImageDraw, ImageFilter, ImageOps


def parse_polygon(value: str) -> list[tuple[int, int]]:
    try:
        points = []
        for pair in value.split():
            x, y = (int(item) for item in pair.split(","))
            points.append((x, y))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use 'x1,y1 x2,y2 x3,y3 ...'") from exc
    if len(points) < 3:
        raise argparse.ArgumentTypeError("Cada poligono precisa de pelo menos tres pontos")
    return points


def parse_box(value: str) -> tuple[int, int, int, int]:
    try:
        x1, y1, x2, y2 = (int(item) for item in value.split(","))
        return x1, y1, x2, y2
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use x1,y1,x2,y2") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagem", type=Path, required=True)
    parser.add_argument(
        "--limitar-a",
        type=Path,
        help="Mascara RGBA cuja area opaca limita a edicao (por exemplo, o recorte do carro)",
    )
    parser.add_argument("--editar-poligono", type=parse_polygon, action="append", default=[])
    parser.add_argument("--proteger-poligono", type=parse_polygon, action="append", default=[])
    parser.add_argument("--proteger-retangulo", type=parse_box, action="append", default=[])
    parser.add_argument("--proteger-elipse", type=parse_box, action="append", default=[])
    parser.add_argument("--suavizacao", type=float, default=3.0)
    parser.add_argument("--mascara", type=Path, required=True)
    parser.add_argument("--preview", type=Path, required=True)
    return parser.parse_args()


def validate_box(box: tuple[int, int, int, int], width: int, height: int) -> None:
    x1, y1, x2, y2 = box
    if not (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height):
        raise ValueError(f"Regiao fora da imagem: {box}")


def main() -> None:
    args = parse_args()
    if not args.editar_poligono:
        raise ValueError("Informe ao menos um --editar-poligono")

    with Image.open(args.imagem) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
    width, height = image.size
    alpha = Image.new("L", image.size, 255)
    draw = ImageDraw.Draw(alpha)

    for polygon in args.editar_poligono:
        for x, y in polygon:
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(f"Ponto fora da imagem: {(x, y)}")
        draw.polygon(polygon, fill=0)
    for polygon in args.proteger_poligono:
        draw.polygon(polygon, fill=255)
    for box in args.proteger_retangulo:
        validate_box(box, width, height)
        draw.rectangle(box, fill=255)
    for box in args.proteger_elipse:
        validate_box(box, width, height)
        draw.ellipse(box, fill=255)

    if args.suavizacao > 0:
        alpha = alpha.filter(ImageFilter.GaussianBlur(args.suavizacao))

    alpha_np = np.asarray(alpha, dtype=np.uint8)
    if args.limitar_a:
        with Image.open(args.limitar_a) as limiter_source:
            limiter = ImageOps.exif_transpose(limiter_source).convert("RGBA")
            if limiter.size != image.size:
                raise ValueError("A mascara limitadora deve ter o mesmo tamanho da imagem")
            limiter_alpha = np.asarray(limiter.getchannel("A"), dtype=np.uint8)
        alpha_np = np.maximum(alpha_np, 255 - limiter_alpha)
    rgba = np.full((height, width, 4), 255, dtype=np.uint8)
    rgba[:, :, 3] = alpha_np

    image_np = np.asarray(image, dtype=np.float32)
    editable_strength = (255.0 - alpha_np.astype(np.float32)) / 255.0
    red = np.zeros_like(image_np)
    red[:, :, :] = (230, 45, 55)
    mix = editable_strength[:, :, None] * 0.62
    preview = image_np * (1.0 - mix) + red * mix

    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    args.mascara.parent.mkdir(parents=True, exist_ok=True)
    args.preview.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba).save(args.mascara, format="PNG", icc_profile=profile)
    Image.fromarray(np.clip(preview, 0, 255).astype(np.uint8)).save(
        args.preview,
        format="JPEG",
        quality=94,
        icc_profile=profile,
    )
    coverage = float(np.count_nonzero(alpha_np < 128)) / alpha_np.size
    print(f"Area editavel: {coverage:.2%}")
    print(args.mascara.resolve())
    print(args.preview.resolve())


if __name__ == "__main__":
    main()
