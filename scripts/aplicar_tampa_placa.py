#!/usr/bin/env python3
"""Aplica o tampa-placa oficial em um quadrilatero medido na fotografia."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLATE = ROOT / "assets" / "tampa-placa" / "tampa-placa-garage-665-horizontal-v03.png"


def parse_point(value: str) -> tuple[float, float]:
    try:
        x, y = value.split(",", maxsplit=1)
        return float(x), float(y)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use o formato x,y") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagem", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    parser.add_argument("--tampa-placa", type=Path, default=DEFAULT_PLATE)
    parser.add_argument(
        "--ponto",
        type=parse_point,
        action="append",
        required=True,
        help="Repetir quatro vezes: superior-esquerdo, superior-direito, inferior-direito, inferior-esquerdo",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if len(args.ponto) != 4:
        raise ValueError("Forneca exatamente quatro pontos na ordem documentada")

    background = cv2.imread(str(args.imagem), cv2.IMREAD_COLOR)
    plate = cv2.imread(str(args.tampa_placa), cv2.IMREAD_UNCHANGED)
    if background is None:
        raise ValueError(f"Nao foi possivel abrir {args.imagem}")
    if plate is None or plate.shape[2] != 4:
        raise ValueError("O tampa-placa deve ser PNG RGBA")

    height, width = plate.shape[:2]
    source = np.float32([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])
    destination = np.float32(args.ponto)
    transform = cv2.getPerspectiveTransform(source, destination)

    canvas_size = (background.shape[1], background.shape[0])
    warped = cv2.warpPerspective(plate, transform, canvas_size, flags=cv2.INTER_LANCZOS4)
    plate_max = float(np.iinfo(warped.dtype).max)
    plate_rgb = warped[:, :, :3].astype(np.float32) / plate_max
    alpha = warped[:, :, 3:4].astype(np.float32) / plate_max
    background_rgb = background.astype(np.float32) / 255.0
    composed = (plate_rgb * alpha + background_rgb * (1.0 - alpha)) * 255.0

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(args.saida), np.clip(composed, 0, 255).astype(np.uint8)):
        raise RuntimeError(f"Nao foi possivel salvar {args.saida}")
    print(args.saida.resolve())


if __name__ == "__main__":
    main()
