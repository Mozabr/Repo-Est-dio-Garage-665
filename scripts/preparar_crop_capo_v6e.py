#!/usr/bin/env python3
"""Prepare a tight hood crop so the image model cannot reinterpret the whole car."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    image.save(path, format="PNG", icc_profile=profile)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/pipeline-v6e.json")
    parser.add_argument("--out", type=Path, default=ROOT / "trabalhos/panamera/refinamento-dianteira-v6e/preparo")
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text())
    source_path = ROOT / cfg["authority_source"]
    source_mask_path = ROOT / "trabalhos/panamera/refinamento-dianteira-v6c/guias-palco/M11U-capo-integral-editar.png"
    crop_box = tuple(cfg["crop_source_xyxy"])
    target_size = (cfg["working"]["width"], cfg["working"]["height"])

    source = Image.open(source_path).convert("RGB")
    source_mask = Image.open(source_mask_path).convert("L")
    crop = source.crop(crop_box).resize(target_size, Image.Resampling.LANCZOS)
    edit_mask = source_mask.crop(crop_box).resize(target_size, Image.Resampling.LANCZOS)
    edit_array = np.asarray(edit_mask, dtype=np.uint8)
    api_rgba = np.zeros((target_size[1], target_size[0], 4), dtype=np.uint8)
    api_rgba[:, :, :3] = 255
    api_rgba[:, :, 3] = 255 - edit_array

    target_path = args.out / "alvo-crop-2048x1024.png"
    edit_path = args.out / "mascara-editar-2048x1024.png"
    api_path = args.out / "mascara-api-alpha-2048x1024.png"
    save_png(crop, target_path)
    save_png(edit_mask, edit_path)
    save_png(Image.fromarray(api_rgba, "RGBA"), api_path)
    report = {
        "status": "crop_ready",
        "source": str(source_path.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "source_size": list(source.size),
        "crop_source_xyxy": list(crop_box),
        "crop_source_size": [crop_box[2] - crop_box[0], crop_box[3] - crop_box[1]],
        "api_size": list(target_size),
        "scale": [target_size[0] / (crop_box[2] - crop_box[0]), target_size[1] / (crop_box[3] - crop_box[1])],
        "editable_pixels_api": int((edit_array > 0).sum()),
        "note": "The wheel, plate, glass and studio may appear as locked context, but their mask alpha is opaque and they are copied from the source after the call."
    }
    (args.out / "qa-preparo.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
