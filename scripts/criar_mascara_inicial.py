#!/usr/bin/env python3
"""Cria um rascunho de mascara de preservacao usando GrabCut."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageCms


def parse_rectangle(value: str) -> tuple[int, int, int, int]:
    try:
        x, y, width, height = (int(item) for item in value.split(","))
        return x, y, width, height
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use x,y,largura,altura") from exc


def parse_point(value: str) -> tuple[int, int]:
    try:
        x, y = (int(item) for item in value.split(","))
        return x, y
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use x,y") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagem", type=Path, required=True)
    parser.add_argument("--retangulo", type=parse_rectangle, required=True)
    parser.add_argument("--mascara", type=Path, required=True)
    parser.add_argument("--preview", type=Path, required=True)
    parser.add_argument("--dilatacao", type=int, default=4)
    parser.add_argument(
        "--editar-abaixo",
        type=int,
        help="Torna editavel tudo abaixo desta coordenada Y para remover a sombra externa antiga",
    )
    parser.add_argument(
        "--editar-retangulo",
        type=parse_rectangle,
        action="append",
        default=[],
        help="Regiao x,y,largura,altura que deve ser removida da mascara de preservacao",
    )
    parser.add_argument(
        "--forcar-ponto",
        type=parse_point,
        action="append",
        default=[],
        help="Pontos de um poligono interno que deve ser tratado como veiculo",
    )
    return parser.parse_args()


def largest_component(binary: np.ndarray) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    if count <= 1:
        return binary
    index = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    return np.where(labels == index, 255, 0).astype(np.uint8)


def main() -> None:
    args = parse_args()
    full_image = cv2.imread(str(args.imagem), cv2.IMREAD_COLOR)
    if full_image is None:
        raise ValueError(f"Nao foi possivel abrir {args.imagem}")

    x, y, width, height = args.retangulo
    if x < 0 or y < 0 or x + width > full_image.shape[1] or y + height > full_image.shape[0]:
        raise ValueError("O retangulo ultrapassa os limites da imagem")

    scale = min(1.0, 1280.0 / max(full_image.shape[:2]))
    image = cv2.resize(full_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    rectangle = tuple(int(round(value * scale)) for value in (x, y, width, height))

    labels = np.full(image.shape[:2], cv2.GC_BGD, dtype=np.uint8)
    rx, ry, rw, rh = rectangle
    labels[ry : ry + rh, rx : rx + rw] = cv2.GC_PR_BGD
    if args.forcar_ponto:
        if len(args.forcar_ponto) < 3:
            raise ValueError("O poligono forcado precisa de pelo menos tres pontos")
        polygon = np.array(
            [[int(round(px * scale)), int(round(py * scale))] for px, py in args.forcar_ponto],
            dtype=np.int32,
        )
        cv2.fillPoly(labels, [polygon], cv2.GC_FGD)
    background_model = np.zeros((1, 65), dtype=np.float64)
    foreground_model = np.zeros((1, 65), dtype=np.float64)
    cv2.grabCut(
        image,
        labels,
        None,
        background_model,
        foreground_model,
        5,
        cv2.GC_INIT_WITH_MASK,
    )

    foreground = np.where((labels == cv2.GC_FGD) | (labels == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    foreground = largest_component(foreground)
    foreground = cv2.morphologyEx(foreground, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    if args.dilatacao:
        radius = max(1, int(round(args.dilatacao * scale)))
        size = radius * 2 + 1
        foreground = cv2.dilate(foreground, np.ones((size, size), np.uint8), iterations=1)
    alpha = cv2.resize(foreground, (full_image.shape[1], full_image.shape[0]), interpolation=cv2.INTER_LANCZOS4)
    alpha = cv2.GaussianBlur(alpha, (0, 0), sigmaX=1.2)
    if args.editar_abaixo is not None:
        alpha[args.editar_abaixo :, :] = 0
    for clear_x, clear_y, clear_width, clear_height in args.editar_retangulo:
        alpha[clear_y : clear_y + clear_height, clear_x : clear_x + clear_width] = 0

    rgba = np.zeros((full_image.shape[0], full_image.shape[1], 4), dtype=np.uint8)
    rgba[:, :, :3] = 255
    rgba[:, :, 3] = alpha

    overlay = full_image.copy()
    editable = alpha < 128
    magenta = np.full_like(full_image, (180, 40, 210))
    overlay[editable] = cv2.addWeighted(full_image[editable], 0.35, magenta[editable], 0.65, 0)

    args.mascara.parent.mkdir(parents=True, exist_ok=True)
    args.preview.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.mascara), rgba)
    preview_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.fromarray(preview_rgb).save(args.preview, format="JPEG", quality=92, icc_profile=profile)
    print(args.mascara.resolve())
    print(args.preview.resolve())


if __name__ == "__main__":
    main()
