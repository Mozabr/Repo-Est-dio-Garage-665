#!/usr/bin/env python3
"""Prepare one shared lateral crop and one isolated API mask per painted panel."""
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
    parser.add_argument("--config", type=Path, default=ROOT / "config/superficies-carroceria-v6f.json")
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text())
    source_path = ROOT / cfg["authority_source"]
    mask_root = ROOT / cfg["mask_root"]
    out = ROOT / cfg["output_root"]
    box = tuple(cfg["crop_source_xyxy"])
    api_size = tuple(cfg["api_size"])
    source = Image.open(source_path).convert("RGB")
    target = source.crop(box).resize(api_size, Image.Resampling.LANCZOS)
    target_path = out / "alvo-lateral-1536x1024.png"
    save_png(target, target_path)

    report_surfaces = []
    union = np.zeros((api_size[1], api_size[0]), dtype=np.uint8)
    for surface in cfg["surfaces"]:
        mask = Image.open(mask_root / surface["mask"]).convert("L")
        edit = mask.crop(box).resize(api_size, Image.Resampling.LANCZOS)
        edit_array = np.asarray(edit, dtype=np.uint8)
        api = np.full((api_size[1], api_size[0], 4), 255, dtype=np.uint8)
        api[:, :, 3] = 255 - edit_array
        edit_path = out / f"{surface['id']}-editar.png"
        api_path = out / f"{surface['id']}-api-alpha.png"
        save_png(edit, edit_path)
        save_png(Image.fromarray(api, "RGBA"), api_path)
        overlap = int(((union > 0) & (edit_array > 0)).sum())
        union = np.maximum(union, edit_array)
        report_surfaces.append({
            "id": surface["id"],
            "stage": surface["stage"],
            "editable_pixels": int((edit_array > 0).sum()),
            "overlap_with_previous_pixels": overlap,
            "edit_mask": str(edit_path.relative_to(ROOT)),
            "api_mask": str(api_path.relative_to(ROOT)),
        })

    report = {
        "status": "lateral_crops_ready_not_authorized_before_hood_approval",
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "source_size": list(source.size),
        "crop_source_xyxy": list(box),
        "api_size": list(api_size),
        "surfaces": report_surfaces,
        "invariants": [
            "one surface per API call",
            "wheels, glass, handles, badge and panel gaps remain protected",
            "no lateral API call before hood visual approval"
        ]
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "qa-preparo-lateral.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
