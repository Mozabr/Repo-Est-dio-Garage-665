#!/usr/bin/env python3
"""Prepara uma vista externa v11 usando o Studio G já composto e máscara conservadora."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "serie-v11-vistas.json"
PREVIEWS = ROOT / "trabalhos" / "panamera" / "previews-serie-v10-studio-canonico" / "externas"
OUT_ROOT = ROOT / "trabalhos" / "panamera" / "serie-v11"
PROFILE = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("vista")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    if args.vista not in data["views"]:
        raise SystemExit(f"Vista inválida: {args.vista}. Use: {', '.join(data['order'])}")

    view_dir = PREVIEWS / args.vista
    target_path = view_dir / "preview.png"
    alpha_path = view_dir / "alpha-veiculo-preview.png"
    if not target_path.exists() or not alpha_path.exists():
        raise FileNotFoundError(f"Preview/máscara v10 ausente para {args.vista}")

    target = Image.open(target_path).convert("RGB")
    if target.size != (1600, 1200):
        target = target.resize((1600, 1200), Image.Resampling.LANCZOS)
    vehicle = Image.open(alpha_path).convert("L")
    if vehicle.size != target.size:
        vehicle = vehicle.resize(target.size, Image.Resampling.LANCZOS)

    # A API edita onde alpha=0. O limiar alto cria uma faixa protegida na borda
    # do recorte e impede que o gerador redesenhe silhueta, pneus ou espelhos.
    editable = (np.asarray(vehicle, np.uint8) >= 245).astype(np.uint8) * 255
    rgba = np.zeros((*editable.shape, 4), np.uint8)
    rgba[:, :, 3] = 255 - editable

    out = OUT_ROOT / args.vista / "preparo"
    out.mkdir(parents=True, exist_ok=True)
    target.save(out / "alvo-1600x1200.png", icc_profile=PROFILE)
    Image.fromarray(rgba, "RGBA").save(out / "mascara-api-alpha.png", icc_profile=PROFILE)
    rgb = np.asarray(target, np.uint8).astype(np.float32)
    tint = np.zeros_like(rgb)
    tint[:] = (215, 35, 178)
    review = rgb.copy()
    active = editable > 0
    review[active] = review[active] * 0.38 + tint[active] * 0.62
    Image.fromarray(np.clip(review, 0, 255).astype(np.uint8)).save(
        out / "revisao-mascara.jpg", quality=94, icc_profile=PROFILE
    )
    manifest = {
        "vista": args.vista,
        "target": str(target_path.relative_to(ROOT)),
        "vehicle_alpha": str(alpha_path.relative_to(ROOT)),
        "source": data["views"][args.vista]["source"],
        "editable_percent": float((editable > 0).mean() * 100),
        "edge_policy": "vehicle alpha >=245 editable; silhouette transition locked",
        "mask_review": str((out / "revisao-mascara.jpg").relative_to(ROOT)),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(out.resolve())


if __name__ == "__main__":
    main()
