#!/usr/bin/env python3
"""Repoe apenas o emblema colorido original, sem copiar o fundo ao redor."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


def parse_box(value: str) -> tuple[int, int, int, int]:
    try:
        return tuple(int(item) for item in value.split(","))  # type: ignore[return-value]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use x1,y1,x2,y2") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagem", type=Path, required=True)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--regiao", type=parse_box, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base = cv2.imread(str(args.imagem), cv2.IMREAD_COLOR)
    original = cv2.imread(str(args.original), cv2.IMREAD_COLOR)
    if base is None or original is None or base.shape != original.shape:
        raise ValueError("Imagem e original devem existir e ter as mesmas dimensoes")

    x1, y1, x2, y2 = args.regiao
    if not (0 <= x1 < x2 <= base.shape[1] and 0 <= y1 < y2 <= base.shape[0]):
        raise ValueError("A regiao ultrapassa a imagem")
    roi = original[y1:y2, x1:x2]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    warm_hue = (hsv[:, :, 0] <= 45) | (hsv[:, :, 0] >= 165)
    saturated = np.where(
        warm_hue & (hsv[:, :, 1] >= 70) & (hsv[:, :, 2] >= 55), 255, 0
    ).astype(np.uint8)
    saturated = cv2.morphologyEx(saturated, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    contours, _ = cv2.findContours(saturated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("Nao foi possivel localizar o emblema colorido")
    significant = [contour for contour in contours if cv2.contourArea(contour) >= 3]
    points = np.vstack(significant or contours)
    hull = cv2.convexHull(points)
    alpha_roi = np.zeros(saturated.shape, dtype=np.uint8)
    cv2.fillConvexPoly(alpha_roi, hull, 255)
    alpha_roi = cv2.dilate(alpha_roi, np.ones((3, 3), np.uint8), iterations=1)
    alpha_roi = cv2.GaussianBlur(alpha_roi, (0, 0), sigmaX=0.7)

    alpha = alpha_roi.astype(np.float32)[:, :, None] / 255.0
    base_roi = base[y1:y2, x1:x2].astype(np.float32)
    original_roi = roi.astype(np.float32)
    base[y1:y2, x1:x2] = np.clip(original_roi * alpha + base_roi * (1.0 - alpha), 0, 255).astype(np.uint8)

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(args.saida), base):
        raise RuntimeError(f"Nao foi possivel salvar {args.saida}")
    print(args.saida.resolve())


if __name__ == "__main__":
    main()
