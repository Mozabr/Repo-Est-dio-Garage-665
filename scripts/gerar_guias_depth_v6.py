#!/usr/bin/env python3
"""Infer relative depth locally and derive a conservative normal-like geometry guide."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForDepthEstimation

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("HF_HUB_OFFLINE", "1")
MODEL = ROOT / "modelos/depth-anything-v2-small"
SOURCE = ROOT / "trabalhos/panamera/refinamento-dianteira-v6/entrada/source-2048x1536.png"
ALPHA = ROOT / "trabalhos/panamera/refinamento-dianteira-v6/entrada/alpha-2048x1536.png"
OUT = ROOT / "trabalhos/panamera/refinamento-dianteira-v6/guias"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--alpha", type=Path, default=ALPHA)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    if not (MODEL / "model.safetensors").exists():
        raise FileNotFoundError("Depth Anything V2 Small is not installed. Run baixar_depth_anything_v2.py")
    args.out.mkdir(parents=True, exist_ok=True)
    image = Image.open(args.source).convert("RGB")
    processor = AutoImageProcessor.from_pretrained(MODEL, local_files_only=True, use_fast=False)
    model = AutoModelForDepthEstimation.from_pretrained(MODEL, local_files_only=True)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model.to(device).eval()
    inputs = {key: value.to(device) for key, value in processor(images=image, return_tensors="pt").items()}
    with torch.inference_mode():
        predicted = model(**inputs).predicted_depth
    resized = torch.nn.functional.interpolate(
        predicted.unsqueeze(1), size=(image.height, image.width), mode="bicubic", align_corners=False
    ).squeeze().float().cpu().numpy()
    lo, hi = np.percentile(resized, [1, 99])
    depth = np.clip((resized - lo) / max(hi - lo, 1e-6), 0, 1)
    depth_u16 = np.round(depth * 65535).astype(np.uint16)
    Image.fromarray(depth_u16).save(args.out / "depth-anything-v2-small-16bit.png")
    depth_u8 = np.round(depth * 255).astype(np.uint8)
    Image.fromarray(depth_u8).save(args.out / "depth-anything-v2-small.png")
    color = cv2.cvtColor(cv2.applyColorMap(depth_u8, cv2.COLORMAP_INFERNO), cv2.COLOR_BGR2RGB)
    Image.fromarray(color).save(args.out / "depth-anything-v2-small-preview.png")

    smooth = cv2.GaussianBlur(depth.astype(np.float32), (0, 0), 5.0)
    dx = cv2.Sobel(smooth, cv2.CV_32F, 1, 0, ksize=5) * 10.0
    dy = cv2.Sobel(smooth, cv2.CV_32F, 0, 1, ksize=5) * 10.0
    normals = np.dstack((-dx, -dy, np.ones_like(dx)))
    normals /= np.maximum(np.linalg.norm(normals, axis=2, keepdims=True), 1e-6)
    normals_rgb = np.round((normals * .5 + .5) * 255).astype(np.uint8)
    alpha = np.asarray(Image.open(args.alpha).convert("L")) / 255.0
    neutral = np.full_like(normals_rgb, [128, 128, 255])
    normals_rgb = np.round(normals_rgb * alpha[:, :, None] + neutral * (1 - alpha[:, :, None])).astype(np.uint8)
    Image.fromarray(normals_rgb).save(args.out / "normal-aproximada.png")

    report = {
        "status": "geometry_guides_generated",
        "model": "Depth Anything V2 Small",
        "device": device,
        "source_sha256": hashlib.sha256(args.source.read_bytes()).hexdigest(),
        "depth_percentile_1": float(lo),
        "depth_percentile_99": float(hi),
        "depth_is_metric": False,
        "normal_is_approximation_from_relative_depth": True,
        "allowed_use": "geometry guidance and QA only; never appearance or paint color"
    }
    (args.out / "qa-guias.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
