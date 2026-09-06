#!/usr/bin/env python3
"""Cria uma mascara precisa do veiculo com o SAM 2 oficial da Meta."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageCms, ImageFilter, ImageOps
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor


def parse_point(value: str) -> tuple[int, int]:
    try:
        x, y = (int(item) for item in value.split(","))
        return x, y
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use x,y") from exc


def parse_box(value: str) -> tuple[int, int, int, int]:
    try:
        x1, y1, x2, y2 = (int(item) for item in value.split(","))
        return x1, y1, x2, y2
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use x1,y1,x2,y2") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagem", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument(
        "--config",
        default="configs/sam2.1/sam2.1_hiera_s.yaml",
        help="Configuracao Hydra instalada com o pacote SAM 2",
    )
    parser.add_argument("--caixa", type=parse_box, required=True)
    parser.add_argument("--incluir", type=parse_point, action="append", default=[])
    parser.add_argument("--excluir", type=parse_point, action="append", default=[])
    parser.add_argument("--mascara", type=Path, required=True)
    parser.add_argument("--preview", type=Path, required=True)
    parser.add_argument("--dilatacao", type=int, default=3)
    parser.add_argument("--suavizacao", type=float, default=1.0)
    parser.add_argument("--dispositivo", choices=("auto", "mps", "cpu"), default="auto")
    parser.add_argument(
        "--inverter",
        action="store_true",
        help="Deixa a regiao segmentada transparente para uso como mascara de edicao",
    )
    return parser.parse_args()


def choose_device(requested: str) -> torch.device:
    if requested == "mps":
        if not torch.backends.mps.is_available():
            raise RuntimeError("MPS nao esta disponivel neste computador")
        return torch.device("mps")
    if requested == "cpu":
        return torch.device("cpu")
    return torch.device("mps" if torch.backends.mps.is_available() else "cpu")


def main() -> None:
    args = parse_args()
    if not args.checkpoint.exists():
        raise FileNotFoundError(args.checkpoint)

    with Image.open(args.imagem) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
    image_np = np.asarray(image)
    width, height = image.size

    x1, y1, x2, y2 = args.caixa
    if not (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height):
        raise ValueError("A caixa ultrapassa os limites da imagem")

    points = args.incluir + args.excluir
    point_coords = np.asarray(points, dtype=np.float32) if points else None
    point_labels = (
        np.asarray([1] * len(args.incluir) + [0] * len(args.excluir), dtype=np.int32)
        if points
        else None
    )

    device = choose_device(args.dispositivo)
    print(f"Dispositivo: {device}")
    model = build_sam2(args.config, str(args.checkpoint), device=device)
    predictor = SAM2ImagePredictor(model)
    predictor.set_image(image_np)
    masks, scores, _ = predictor.predict(
        point_coords=point_coords,
        point_labels=point_labels,
        box=np.asarray([x1, y1, x2, y2], dtype=np.float32),
        multimask_output=True,
    )

    best = int(np.argmax(scores))
    foreground = masks[best].astype(bool)
    alpha_image = Image.fromarray((foreground.astype(np.uint8) * 255), "L")
    if args.dilatacao > 0:
        kernel = args.dilatacao * 2 + 1
        alpha_image = alpha_image.filter(ImageFilter.MaxFilter(kernel))
    if args.suavizacao > 0:
        alpha_image = alpha_image.filter(ImageFilter.GaussianBlur(args.suavizacao))

    alpha = np.asarray(alpha_image, dtype=np.uint8)
    if args.inverter:
        alpha = 255 - alpha
    rgba = np.full((height, width, 4), 255, dtype=np.uint8)
    rgba[:, :, 3] = alpha

    editable = alpha < 128
    preview = image_np.astype(np.float32)
    magenta = np.zeros_like(preview)
    magenta[:, :, :] = (210, 40, 180)
    preview[editable] = preview[editable] * 0.35 + magenta[editable] * 0.65

    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    args.mascara.parent.mkdir(parents=True, exist_ok=True)
    args.preview.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(args.mascara, format="PNG", icc_profile=profile)
    Image.fromarray(np.clip(preview, 0, 255).astype(np.uint8), "RGB").save(
        args.preview,
        format="JPEG",
        quality=94,
        icc_profile=profile,
    )
    coverage = float(np.count_nonzero(alpha >= 128)) / alpha.size
    print(f"Mascara escolhida: {best}; score={float(scores[best]):.5f}; cobertura={coverage:.2%}")
    print(args.mascara.resolve())
    print(args.preview.resolve())


if __name__ == "__main__":
    main()
