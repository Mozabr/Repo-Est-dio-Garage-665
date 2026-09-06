#!/usr/bin/env python3
"""Project source-space masks and normals into the fixed Studio H edit target."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qa", type=Path, default=ROOT / "trabalhos/panamera/refinamento-dianteira-v6c/alvo-estudio-h/dianteira-3-4/qa.json")
    parser.add_argument("--source", type=Path, default=ROOT / "trabalhos/panamera/refinamento-dianteira-v6/entrada/source-2048x1536.png")
    parser.add_argument("--mask-dir", type=Path, default=ROOT / "trabalhos/panamera/refinamento-dianteira-v6/mascaras")
    parser.add_argument("--normal", type=Path, default=ROOT / "trabalhos/panamera/refinamento-dianteira-v6/guias/normal-aproximada.png")
    parser.add_argument("--target", type=Path, default=ROOT / "trabalhos/panamera/refinamento-dianteira-v6c/alvo-estudio-h/dianteira-3-4/master-4096x3072.png")
    parser.add_argument("--out", type=Path, default=ROOT / "trabalhos/panamera/refinamento-dianteira-v6c/guias-palco")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    qa = json.loads(args.qa.read_text())
    transform_native = np.asarray(qa["transform"], dtype=np.float32)
    source_work = Image.open(args.source).convert("RGB")
    native_w, native_h = qa["source_native_size"]
    with Image.open(args.target) as target_image:
        target_size = target_image.size
        target_rgb = np.asarray(target_image.convert("RGB"))
    work_to_native = np.float32([[native_w/source_work.width, 0, 0], [0, native_h/source_work.height, 0], [0, 0, 1]])
    transform = transform_native @ work_to_native

    mask_reports = []
    for mask_path in sorted(args.mask_dir.glob("M*-editar.png")):
        edit = np.asarray(Image.open(mask_path).convert("L"))
        projected = cv2.warpPerspective(edit, transform, target_size, flags=cv2.INTER_LINEAR, borderValue=0)
        projected[projected < 2] = 0
        Image.fromarray(projected).save(args.out / mask_path.name)
        api = np.full((target_size[1], target_size[0], 4), 255, np.uint8)
        api[:, :, 3] = 255 - projected
        Image.fromarray(api, "RGBA").save(args.out / mask_path.name.replace("-editar.png", "-api-alpha.png"))
        mask_reports.append({"id": mask_path.stem.replace("-editar", ""), "editable_pixels": int((projected > 0).sum())})

    normal = np.asarray(Image.open(args.normal).convert("RGB"))
    warped_normal = cv2.warpPerspective(normal, transform, target_size, flags=cv2.INTER_LINEAR, borderValue=(128, 128, 255))
    native_alpha = np.asarray(Image.open(args.qa.parent / "alpha-final.png").convert("L"))
    stage_alpha = cv2.warpPerspective(native_alpha, transform_native, target_size, flags=cv2.INTER_LINEAR, borderValue=0)
    neutral = np.full_like(warped_normal, [128, 128, 255])
    a = stage_alpha.astype(np.float32)[:, :, None] / 255
    warped_normal = np.round(warped_normal*a + neutral*(1-a)).astype(np.uint8)
    Image.fromarray(warped_normal).save(args.out / "normal-aproximada-palco.png")

    hood = np.asarray(Image.open(args.out / "M11U-capo-integral-editar.png").convert("L"), np.float32) / 255
    overlay = np.round(target_rgb*(1-hood[:, :, None]*.45) + np.array([244, 94, 46])*hood[:, :, None]*.45).astype(np.uint8)
    Image.fromarray(overlay).save(args.out / "M11U-capo-integral-preview.jpg", quality=94)
    report = {
        "status": "projected_guides_ready_for_visual_review",
        "target_size": list(target_size),
        "target_sha256": hashlib.sha256(args.target.read_bytes()).hexdigest(),
        "source_to_stage_transform": transform.tolist(),
        "masks": mask_reports,
        "normal_role": "geometry guide only",
        "target_pixels_modified": False
    }
    (args.out / "qa-projecao.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
