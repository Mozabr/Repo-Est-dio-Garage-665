#!/usr/bin/env python3
"""Audita contenção e cria comparação visual de uma candidata externa v11."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("vista")
    return parser.parse_args()


def lab_l(rgb: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)[:, :, 0].astype(np.float32)


def main() -> None:
    vista = parse_args().vista
    work = ROOT / "trabalhos" / "panamera" / "serie-v11" / vista
    prep = work / "preparo"
    api = work / "api-v01"
    target_path = prep / "alvo-1600x1200.png"
    mask_path = prep / "mascara-api-alpha.png"
    candidate_path = api / "candidato-contido.png"
    master_path = ROOT / "referencias" / "autoridades" / "panamera-master-estudio-canonico-v01.png"

    target = np.asarray(Image.open(target_path).convert("RGB"), np.uint8)
    candidate = np.asarray(Image.open(candidate_path).convert("RGB"), np.uint8)
    protected = np.asarray(Image.open(mask_path).convert("RGBA"), np.uint8)[:, :, 3] == 255
    editable = ~protected
    if target.shape != candidate.shape:
        raise ValueError(f"Dimensões diferentes: {target.shape} e {candidate.shape}")

    changed = np.any(target != candidate, axis=2)
    outside_changed = int(np.count_nonzero(changed & protected))
    before_l = lab_l(target)
    after_l = lab_l(candidate)
    hp_before = before_l - cv2.GaussianBlur(before_l, (0, 0), 3)
    hp_after = after_l - cv2.GaussianBlur(after_l, (0, 0), 3)
    texture_before = float(np.std(hp_before[editable]))
    texture_after = float(np.std(hp_after[editable]))
    near_white = float(np.mean(np.max(candidate[editable], axis=1) >= 250) * 100)

    report = {
        "status": "technical_pass_visual_approval_required" if outside_changed == 0 else "technical_fail",
        "vista": vista,
        "size": [int(target.shape[1]), int(target.shape[0])],
        "changed_pixels_outside_vehicle_mask": outside_changed,
        "mean_abs_luminance_change_inside_mask": float(np.mean(np.abs(after_l[editable] - before_l[editable]))),
        "microtexture_rms_before": texture_before,
        "microtexture_rms_after": texture_after,
        "microtexture_ratio": float(texture_after / max(texture_before, 1e-6)),
        "near_white_percent_inside_mask": near_white,
        "automatic_guarantee": "only containment and dimensions",
        "human_gate": [
            "same vehicle geometry and wheel orientation",
            "same paint identity; glossy metallic, not matte",
            "same Studio G lighting signature as teste 05",
            "no outdoor reflections, halo or cutout appearance"
        ]
    }
    (api / "qa-tecnico.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    font = ImageFont.load_default(size=20)
    panels = [
        (Image.fromarray(target), "ALVO TÉCNICO"),
        (Image.open(master_path).convert("RGB"), "MASTER TESTE 05"),
        (Image.fromarray(candidate), "CANDIDATA GPT IMAGE 2")
    ]
    canvas = Image.new("RGB", (2400, 650), (22, 24, 28))
    draw = ImageDraw.Draw(canvas)
    for i, (image, label) in enumerate(panels):
        tile = ImageOps.fit(image, (800, 600), Image.Resampling.LANCZOS)
        canvas.paste(tile, (i * 800, 50))
        draw.text((i * 800 + 18, 15), label, fill="white", font=font)
    canvas.save(api / "comparacao-master-alvo-candidata.jpg", quality=94)
    print((api / "comparacao-master-alvo-candidata.jpg").resolve())


if __name__ == "__main__":
    main()
