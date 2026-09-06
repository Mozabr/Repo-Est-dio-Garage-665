#!/usr/bin/env python3
"""Build reviewable, surface-separated masks at the v6 working resolution."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def polygon_mask(shape: tuple[int, int], points: list[list[int]]) -> np.ndarray:
    result = np.zeros(shape, np.uint8)
    cv2.fillPoly(result, [np.asarray(points, np.int32)], 255)
    return result


def scaled_points(points: list[list[int]], sx: float, sy: float) -> list[list[int]]:
    return [[round(x * sx), round(y * sy)] for x, y in points]


def add_protections(mask: np.ndarray, cfg: dict, sx: float, sy: float) -> None:
    h, w = mask.shape
    for item in cfg.get("protect_polygons", []):
        np.maximum(mask, polygon_mask((h, w), scaled_points(item["points"], sx, sy)), out=mask)
    for item in cfg.get("protect_ellipses", []):
        x0, y0, x1, y1 = item["box"]
        box = [round(x0 * sx), round(y0 * sy), round(x1 * sx), round(y1 * sy)]
        cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
        ax, ay = max(1, (box[2] - box[0]) // 2), max(1, (box[3] - box[1]) // 2)
        cv2.ellipse(mask, (cx, cy), (ax, ay), 0, 0, 360, 255, -1)
    for item in cfg.get("protect_lines", []):
        width = max(1, round(item["width"] * (sx + sy) / 2))
        cv2.polylines(mask, [np.asarray(scaled_points(item["points"], sx, sy), np.int32)], False, 255, width)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/refinamento-dianteira-v6.json")
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text())
    out = ROOT / cfg["out"]
    out.mkdir(parents=True, exist_ok=True)
    source_path, alpha_path = ROOT / cfg["source"], ROOT / cfg["vehicle_alpha"]
    rgb = np.asarray(Image.open(source_path).convert("RGB"))
    alpha = np.asarray(Image.open(alpha_path).convert("L"))
    h, w = rgb.shape[:2]
    cw, ch = cfg["coordinate_size"]
    sx, sy = w / cw, h / ch
    if [w, h] != cfg["work_size"]:
        raise ValueError(f"Unexpected work size {(w, h)}")

    inherited = json.loads((ROOT / cfg["inherit_protection_from"]).read_text())
    protection = np.zeros((h, w), np.uint8)
    add_protections(protection, inherited, sx, sy)
    add_protections(protection, cfg, sx, sy)
    protection = cv2.dilate(protection, np.ones((5, 5), np.uint8))
    Image.fromarray(protection).save(out / "M19-detalhes-protegidos.png")

    edge_inset = cfg["edge_inset_px_at_coordinate_size"] * (sx + sy) / 2
    feather = cfg["feather_inside_px_at_coordinate_size"] * (sx + sy) / 2
    union = np.zeros((h, w), np.uint8)
    overlap_count = np.zeros((h, w), np.uint8)
    tiles: list[Image.Image] = []
    reports = []

    for region in cfg["regions"]:
        allowed = polygon_mask((h, w), scaled_points(region["polygon"], sx, sy))
        allowed[(alpha < 250) | (protection > 0)] = 0
        distance = cv2.distanceTransform(allowed, cv2.DIST_L2, 5)
        strength = np.clip((distance - edge_inset) / feather, 0, 1)
        edit = np.round(strength * 255).astype(np.uint8)
        if not np.any(edit):
            raise ValueError(f"Empty mask: {region['id']}")
        overlap_count += (edit > 0).astype(np.uint8)
        union = np.maximum(union, edit)
        Image.fromarray(edit).save(out / f"{region['id']}-editar.png")
        api = np.full((h, w, 4), 255, np.uint8)
        api[:, :, 3] = 255 - edit
        Image.fromarray(api, "RGBA").save(out / f"{region['id']}-api-alpha.png")

        strength3 = strength[:, :, None]
        overlay = np.round(rgb * (1 - strength3 * .5) + np.array([244, 94, 46]) * strength3 * .5).astype(np.uint8)
        tile = Image.new("RGB", (640, 512), (24, 27, 31))
        tile.paste(Image.fromarray(overlay).resize((640, 480)), (0, 32))
        ImageDraw.Draw(tile).text((12, 8), f"{region['id']} | laranja = editavel", fill="white", font=ImageFont.load_default(size=15))
        tiles.append(tile)
        reports.append({
            "id": region["id"],
            "stage": region["stage"],
            "editable_pixels": int((edit > 0).sum()),
            "fully_editable_pixels": int((edit == 255).sum()),
            "protected_overlap_pixels": int(((edit > 0) & (protection > 0)).sum()),
            "outside_vehicle_pixels": int(((edit > 0) & (alpha < 250)).sum())
        })

    Image.fromarray(union).save(out / "M20-uniao-editavel.png")
    overlap = np.where(overlap_count > 1, 255, 0).astype(np.uint8)
    Image.fromarray(overlap).save(out / "M21-sobreposicoes.png")
    rows = math.ceil(len(tiles) / 2)
    sheet = Image.new("RGB", (1280, rows * 512), (24, 27, 31))
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % 2) * 640, (index // 2) * 512))
    sheet.save(out / "mapa-mascaras-v6.jpg", quality=94)

    report = {
        "status": "containment_tests_passed_visual_review_required",
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "work_size": [w, h],
        "regions": reports,
        "overlap_pixels": int((overlap_count > 1).sum()),
        "outside_vehicle_pixels_total": int(((union > 0) & (alpha < 250)).sum()),
        "protected_overlap_pixels_total": int(((union > 0) & (protection > 0)).sum()),
        "source_pixels_modified": False,
        "api_mask_convention": "transparent alpha is editable"
    }
    if report["outside_vehicle_pixels_total"] or report["protected_overlap_pixels_total"]:
        raise AssertionError(report)
    (out / "qa-mascaras-v6.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
