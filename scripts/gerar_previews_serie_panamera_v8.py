"""Gera previews rastreaveis das vistas restantes da Panamera, nunca masters."""
from pathlib import Path
import argparse
import hashlib
import json

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

from montar_studio_v2 import artwork_on_sign, apply_plate, contact_shadow, defringe
from studio_common import load_srgb, linear, save_rgb, srgb, warp_rgba

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def contact_sheet(items, output, columns=3, tile=(640, 480)):
    rows = (len(items) + columns - 1) // columns
    label_h = 54
    canvas = Image.new("RGB", (tile[0] * columns, (tile[1] + label_h) * rows), (24, 27, 31))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=17)
    for index, (label, image) in enumerate(items):
        x = (index % columns) * tile[0]
        y = (index // columns) * (tile[1] + label_h)
        contained = ImageOps.contain(image, tile, Image.Resampling.LANCZOS)
        px = x + (tile[0] - contained.width) // 2
        py = y + label_h + (tile[1] - contained.height) // 2
        canvas.paste(contained, (px, py))
        draw.text((x + 14, y + 16), label, fill="white", font=font)
    save_rgb(output, canvas)


def render_external(job, studio, stage_size, preview_size, alpha_root, out_root):
    source_path = ROOT / job["source"]
    alpha_path = ROOT / alpha_root / job["id"] / "alpha-final.png"
    output_dir = out_root / "externas" / job["id"]
    output_dir.mkdir(parents=True, exist_ok=True)

    source = load_srgb(source_path)
    source_rgb = np.asarray(source, np.float32) / 255
    alpha = np.asarray(Image.open(alpha_path).convert("L"), np.float32) / 255
    if alpha.shape != source_rgb.shape[:2]:
        raise ValueError(f"Mascara incompativel: {job['id']}")

    render_rgb = defringe(source_rgb, alpha)
    render_rgb, _ = apply_plate(render_rgb, job.get("plate_quad"))
    ys, xs = np.nonzero(alpha > .5)
    x0, x1, y1 = int(xs.min()), int(xs.max()), int(ys.max())
    scale = stage_size[0] * job["vehicle_width_fraction"] / (x1 - x0 + 1)
    tx = stage_size[0] / 2 - scale * (x0 + x1) / 2
    ty = stage_size[1] * job["baseline_fraction"] - scale * y1
    matrix = np.float32([[scale, 0, tx], [0, scale, ty], [0, 0, 1]])

    premultiplied, stage_alpha = warp_rgba(render_rgb, alpha, matrix, stage_size)
    background = np.asarray(studio.resize(stage_size, Image.Resampling.LANCZOS), np.float32) / 255
    shadow = contact_shadow(
        stage_alpha,
        matrix,
        job["contact_points"],
        stage_size,
        job.get("shadow_footprint"),
        job.get("shadow_strength", .79),
    )
    result = srgb(premultiplied + linear(background) * (1 - shadow[..., None]) * (1 - stage_alpha[..., None]))
    plate_quad = job.get("plate_quad")
    if plate_quad:
        plate_stage = cv2.perspectiveTransform(np.asarray([plate_quad], np.float32), matrix)[0]
        result, _ = apply_plate(result, plate_stage)

    preview = Image.fromarray(np.round(np.clip(result, 0, 1) * 255).astype(np.uint8))
    preview = preview.resize(preview_size, Image.Resampling.LANCZOS)
    preview_path = output_dir / "preview.png"
    save_rgb(preview_path, preview)
    report = {
        "id": job["id"],
        "type": "external_preview",
        "status": "PREVIEW_ONLY_NOT_APPROVED_AS_MASTER",
        "source": job["source"],
        "source_sha256": sha256(source_path),
        "alpha": str(alpha_path.relative_to(ROOT)),
        "alpha_sha256": sha256(alpha_path),
        "preview_size": list(preview.size),
        "transform": matrix.tolist(),
        "plate_quad_source": plate_quad,
        "limitations": [
            "Reflexos urbanos ainda presentes; o tratamento v07 sera adaptado somente apos aprovacao desta vista.",
            "Preview para validar selecao, enquadramento, escala, contato e tampa-placa; nao e master.",
        ],
    }
    (output_dir / "qa-preview.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    return preview, report


def render_interior(item, preview_size, out_root):
    source_path = ROOT / item["source"]
    output_dir = out_root / "interiores" / item["id"]
    output_dir.mkdir(parents=True, exist_ok=True)
    source = load_srgb(source_path)
    preview = source.resize(preview_size, Image.Resampling.LANCZOS)
    preview_path = output_dir / "preview.png"
    save_rgb(preview_path, preview)
    report = {
        "id": item["id"],
        "type": "interior_preview",
        "status": "PREVIEW_ONLY_NOT_APPROVED_AS_MASTER",
        "source": item["source"],
        "source_sha256": sha256(source_path),
        "source_native_size": list(source.size),
        "preview_size": list(preview.size),
        "processing": "Conversao sRGB e redimensionamento Lanczos; nenhum elemento ou cor alterado.",
    }
    (output_dir / "qa-preview.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    return preview, report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/previews-serie-panamera-v8.json")
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text())
    out_root = ROOT / cfg["workdir"]
    out_root.mkdir(parents=True, exist_ok=True)

    studio_path = ROOT / cfg["studio_preview"]
    sign_report = artwork_on_sign(
        ROOT / cfg["studio_base"], studio_path, cfg.get("wall_logo_finish", "matte_physical")
    )
    (studio_path.with_suffix(".json")).write_text(json.dumps(sign_report, indent=2, ensure_ascii=False))
    studio = load_srgb(studio_path)

    source_cfg = json.loads((ROOT / cfg["external_config_source"]).read_text())
    excluded = set(cfg.get("excluded_external_views", []))
    external_jobs = [job for job in source_cfg["photos"] if job["id"] not in excluded]
    stage_size = tuple(cfg["stage_size"])
    preview_size = tuple(cfg["preview_size"])

    external_items, interior_items, reports = [], [], []
    for job in external_jobs:
        preview, report = render_external(
            job, studio, stage_size, preview_size, cfg["external_alpha_root"], out_root
        )
        external_items.append((f"EXTERNA | {job['id']} | PREVIEW", preview))
        reports.append(report)
    for item in cfg["interiors"]:
        preview, report = render_interior(item, preview_size, out_root)
        interior_items.append((f"INTERIOR | {item['id']} | PREVIEW", preview))
        reports.append(report)

    contact_sheet(external_items, out_root / "01-previews-externas.jpg", columns=3)
    contact_sheet(interior_items, out_root / "02-previews-interiores.jpg", columns=3)
    contact_sheet(external_items + interior_items, out_root / "03-serie-completa-previews.jpg", columns=3)
    manifest = {
        "version": cfg["version"],
        "status": cfg["status"],
        "approved_view_excluded": list(excluded),
        "counts": {"external": len(external_items), "interior": len(interior_items), "total": len(reports)},
        "studio": cfg["studio_preview"],
        "studio_sha256": sha256(studio_path),
        "policy": cfg["preview_policy"],
        "items": reports,
    }
    (out_root / "manifesto-previews.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(out_root / "03-serie-completa-previews.jpg")


if __name__ == "__main__":
    main()
