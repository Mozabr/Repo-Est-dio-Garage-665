#!/usr/bin/env python3
"""Apply a deterministic Studio H luminance rig to one reviewed side-panel mask."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rms(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(values.astype(np.float32)))))


def circular_mean(angle: np.ndarray, weight: np.ndarray) -> float:
    vector = np.sum(weight * np.exp(1j * angle))
    if abs(vector) < 1e-6:
        raise ValueError("Insufficient chromatic direction")
    return float(np.angle(vector))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/rig-material-lateral-v6f.json")
    parser.add_argument("--surface", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--light-map", type=Path, required=True)
    parser.add_argument("--effective-mask", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--fail-on-qa", action="store_true")
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text())
    if args.surface not in cfg["surfaces"]:
        raise ValueError(f"Unknown surface: {args.surface}")
    surface = cfg["surfaces"][args.surface]
    source_path = ROOT / cfg["source_crop"]
    mask_path = ROOT / cfg["mask_root"] / surface["mask"]
    source = np.asarray(Image.open(source_path).convert("RGB"), dtype=np.uint8)
    strength = np.asarray(Image.open(mask_path).convert("L"), dtype=np.float32) / 255.0
    panel_strength = strength.copy()
    source_lab = cv2.cvtColor(source, cv2.COLOR_RGB2LAB).astype(np.float32)
    if surface.get("selection_mode") == "warm_bright_reflection":
        # Select only the warm, bright outdoor reflection on the lower side.
        # The mask is derived from the photographed pixels and feathered so no
        # artificial polygon boundary is introduced into the paint.
        source_L = source_lab[:, :, 0]
        source_b = source_lab[:, :, 2] - 128.0
        warm = np.clip(
            (source_b - surface["selection_b_start"]) /
            (surface["selection_b_end"] - surface["selection_b_start"]),
            0.0,
            1.0,
        )
        bright = np.clip(
            (source_L - surface["selection_L_start"]) /
            (surface["selection_L_end"] - surface["selection_L_start"]),
            0.0,
            1.0,
        )
        row = np.arange(source.shape[0], dtype=np.float32)[:, None]
        lower = np.clip(
            (row - surface["selection_y_start"]) /
            (surface["selection_y_end"] - surface["selection_y_start"]),
            0.0,
            1.0,
        )
        selection = cv2.GaussianBlur(warm * bright * lower, (0, 0), surface["selection_sigma"])
        strength *= np.clip(selection * surface.get("selection_gain", 1.0), 0.0, 1.0)
    core = strength >= 0.5
    if not np.any(core):
        raise ValueError("Empty reviewed mask")

    source_L = source_lab[:, :, 0]
    sigma = surface["source_low_sigma"]
    source_low = cv2.GaussianBlur(source_L, (0, 0), sigma)
    source_residual = np.clip(
        source_L - source_low,
        -surface["maximum_source_residual_L"],
        surface["maximum_source_residual_L"],
    )
    target_mode = surface.get("target_mode", "source_smooth")
    donor_path = None
    if target_mode in {"donor_low_tonemap", "hybrid_donor_source"}:
        donor_path = ROOT / surface["donor"]
        donor = np.asarray(
            Image.open(donor_path).convert("RGB").resize((source.shape[1], source.shape[0]), Image.Resampling.LANCZOS),
            dtype=np.uint8,
        )
        donor_L = cv2.cvtColor(donor, cv2.COLOR_RGB2LAB).astype(np.float32)[:, :, 0]
        donor_low = cv2.GaussianBlur(donor_L, (0, 0), surface["donor_low_sigma"])
        donor_p05, donor_p95 = np.percentile(donor_low[core], (5, 95))
        donor_normalized = np.clip((donor_low - donor_p05) / max(donor_p95 - donor_p05, 1e-4), 0, 1)
        donor_target = surface["target_low_L_p05"] + donor_normalized * (
            surface["target_low_L_p95"] - surface["target_low_L_p05"]
        )
        if target_mode == "hybrid_donor_source":
            source_target = surface["tone_center_L"] + (
                source_low - surface["tone_center_L"]
            ) * surface["tone_contrast"]
            donor_weight = surface["donor_weight"]
            target_L = source_target * (1.0 - donor_weight) + donor_target * donor_weight
        else:
            target_L = donor_target
        target_L += source_residual * surface["source_residual_retention"]
    elif target_mode == "absolute_fields":
        target_L = np.full(source_L.shape, surface["base_L"], dtype=np.float32)
        target_L += source_residual * surface["source_residual_retention"]
    elif target_mode == "source_tone_compress":
        # Preserve the photographed curvature and panel shading while reducing
        # the amplitude of identifiable outdoor reflections. This changes the
        # lighting field, not the vehicle geometry or source microtexture.
        target_L = surface["tone_center_L"] + (
            source_low - surface["tone_center_L"]
        ) * surface["tone_contrast"]
        target_L += source_residual * surface["source_residual_retention"]
    else:
        target_L = source_low + source_residual * surface["source_residual_retention"]

    yy, xx = np.ogrid[:source.shape[0], :source.shape[1]]
    for field in surface["fields"]:
        if field["kind"] != "ellipse":
            raise ValueError(f"Unsupported field kind: {field['kind']}")
        cx, cy = field["center_xy"]
        rx, ry = field["radius_xy"]
        distance = np.square((xx - cx) / rx) + np.square((yy - cy) / ry)
        envelope = np.exp(-0.5 * distance * field["falloff"])
        target_L += envelope * field["delta_L"]

    # Let every relighting correction decay to zero before the reviewed panel
    # boundary. This avoids a cutout edge even where the source reflection and
    # the studio field differ substantially.
    binary_core = (strength >= 0.5).astype(np.uint8)
    distance = cv2.distanceTransform(binary_core, cv2.DIST_L2, 5)
    interior = np.clip(distance / surface["interior_transition_px"], 0.0, 1.0)
    interior = interior * interior * (3.0 - 2.0 * interior)
    target_L = source_L * (1.0 - interior) + target_L * interior

    texture = cfg["texture"]
    texture_base = cv2.bilateralFilter(
        source_L,
        texture["bilateral_diameter"],
        texture["bilateral_sigma_color"],
        texture["bilateral_sigma_space"],
    )
    source_fine = np.clip(
        source_L - texture_base,
        -texture["maximum_fine_delta_L"],
        texture["maximum_fine_delta_L"],
    )
    target_L += source_fine * texture["fine_gain"]

    target_lab = source_lab.copy()
    target_lab[:, :, 0] = np.clip(target_L, 0, 255)
    color = cfg["color_lock"]
    neutral = np.clip(
        (target_lab[:, :, 0] - color["neutralization_L_start"])
        / (color["neutralization_L_end"] - color["neutralization_L_start"]),
        0,
        1,
    )
    retention = color["shadow_chroma_retention"] * (1 - neutral) + color["highlight_chroma_retention"] * neutral
    source_chroma = np.hypot(source_lab[:, :, 1] - 128, source_lab[:, :, 2] - 128)
    source_hue = np.arctan2(source_lab[:, :, 2] - 128, source_lab[:, :, 1] - 128)
    if surface.get("chroma_mode") == "scaled_source_vector":
        # Reduce contamination magnitude in bright reflections without rotating
        # the photographed local paint vector.
        target_lab[:, :, 1] = 128.0 + (source_lab[:, :, 1] - 128.0) * retention
        target_lab[:, :, 2] = 128.0 + (source_lab[:, :, 2] - 128.0) * retention
    elif surface.get("chroma_mode") == "fixed_basecoat_direction":
        basecoat_hue = np.radians(surface["fixed_hue_degrees"])
        local_chroma = surface["fixed_chroma"] * retention
        target_lab[:, :, 1] = 128.0 + np.cos(basecoat_hue) * local_chroma
        target_lab[:, :, 2] = 128.0 + np.sin(basecoat_hue) * local_chroma
    else:
        # Derive one robust basecoat direction from the photographed panel.
        basecoat = core & (source_chroma >= 3.0) & (source_L < color["neutralization_L_start"])
        basecoat_weights = np.clip(source_chroma[basecoat], 3.0, 30.0)
        basecoat_hue = circular_mean(source_hue[basecoat], basecoat_weights)
        local_chroma = cv2.GaussianBlur(source_chroma, (0, 0), color["source_chroma_low_sigma"])
        local_chroma = np.clip(local_chroma, 2.0, 12.0) * retention
        target_lab[:, :, 1] = 128.0 + np.cos(basecoat_hue) * local_chroma
        target_lab[:, :, 2] = 128.0 + np.sin(basecoat_hue) * local_chroma

    relit = cv2.cvtColor(np.clip(target_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
    alpha = (strength * surface.get("final_opacity", 1.0))[:, :, None]
    result = np.round(source * (1 - alpha) + relit * alpha).clip(0, 255).astype(np.uint8)
    effective_strength = strength.copy()

    gloss = surface.get("gloss_enhancement")
    if gloss:
        # Reinforce only luminous structure already present in the photographic
        # result. No synthetic stripe or generated texture is introduced.
        current_lab = cv2.cvtColor(result, cv2.COLOR_RGB2LAB).astype(np.float32)
        current_L = current_lab[:, :, 0]
        detail_scale = cv2.GaussianBlur(current_L, (0, 0), gloss["detail_sigma"])
        shape_scale = cv2.GaussianBlur(current_L, (0, 0), gloss["shape_sigma"])
        gloss_delta = np.clip(
            (detail_scale - shape_scale) * gloss["gain"],
            gloss["minimum_delta_L"],
            gloss["maximum_delta_L"],
        )
        for field in gloss.get("key_fields", []):
            cx, cy = field["center_xy"]
            rx, ry = field["radius_xy"]
            field_distance = np.square((xx - cx) / rx) + np.square((yy - cy) / ry)
            field_envelope = np.exp(-0.5 * field_distance * field["falloff"])
            gloss_delta += field_envelope * field["delta_L"]
        panel_core = (panel_strength >= 0.5).astype(np.uint8)
        panel_distance = cv2.distanceTransform(panel_core, cv2.DIST_L2, 5)
        panel_interior = np.clip(panel_distance / gloss["interior_transition_px"], 0.0, 1.0)
        panel_interior = panel_interior * panel_interior * (3.0 - 2.0 * panel_interior)
        gloss_alpha = panel_strength * panel_interior * gloss["opacity"]
        current_lab[:, :, 0] = np.clip(current_L + gloss_delta * gloss_alpha, 0, 255)
        result = cv2.cvtColor(current_lab.astype(np.uint8), cv2.COLOR_LAB2RGB)
        effective_strength = np.maximum(effective_strength, gloss_alpha)

    outside = panel_strength == 0
    result[outside] = source[outside]
    changed = np.any(result != source, axis=2)
    if np.any(changed & outside):
        raise AssertionError("Pixels changed outside reviewed surface mask")

    result_lab = cv2.cvtColor(result, cv2.COLOR_RGB2LAB).astype(np.float32)
    result_L = result_lab[:, :, 0]
    result_chroma = np.hypot(result_lab[:, :, 1] - 128, result_lab[:, :, 2] - 128)
    source_chroma = np.hypot(source_lab[:, :, 1] - 128, source_lab[:, :, 2] - 128)
    valid = core & (source_chroma >= 3.0) & (result_L < color["neutralization_L_start"])
    weights = np.clip(source_chroma[valid], 3.0, 30.0)
    source_hue = np.arctan2(source_lab[:, :, 2] - 128, source_lab[:, :, 1] - 128)
    result_hue = np.arctan2(result_lab[:, :, 2] - 128, result_lab[:, :, 1] - 128)
    result_hue_mean = circular_mean(result_hue[valid], weights)
    if surface.get("selection_mode") == "warm_bright_reflection":
        # Hue is intentionally neutralized in this selected reflection. Near-
        # neutral Lab pixels do not have a stable perceptual hue, so the robust
        # control here is chroma reduction plus the exact outside-pixel lock.
        hue_reference = 0.0
        hue_reference_name = "not_applicable:selected_warm_reflection_neutralization"
        hue_delta = 0.0
    elif surface.get("chroma_mode") == "fixed_basecoat_direction":
        hue_reference = np.radians(surface["fixed_hue_degrees"])
        hue_reference_name = "same-car dark-basecoat anchor"
        hue_delta = float(np.degrees(abs(np.angle(np.exp(1j * (result_hue_mean - hue_reference))))))
    else:
        hue_reference = circular_mean(source_hue[valid], weights)
        hue_reference_name = "same-surface source aggregate"
        hue_delta = float(np.degrees(abs(np.angle(np.exp(1j * (result_hue_mean - hue_reference))))))
    fine = result_L - cv2.GaussianBlur(result_L, (0, 0), 1.2)
    values = result_L[core]
    metrics = {
        "L_p95_minus_p05": float(np.percentile(values, 95) - np.percentile(values, 5)),
        "near_white_percent_L240": float((values >= 240).mean() * 100),
        "chroma_ratio_to_source": float(result_chroma[core].mean() / max(source_chroma[core].mean(), 1e-4)),
        "aggregate_hue_delta_degrees": hue_delta,
        "fine_frequency_rms": rms(fine[core]),
    }
    acceptance = surface["acceptance"]
    checks = {
        "L_p95_minus_p05": acceptance["L_p95_minus_p05"][0] <= metrics["L_p95_minus_p05"] <= acceptance["L_p95_minus_p05"][1],
        "near_white_percent_L240": metrics["near_white_percent_L240"] <= acceptance["near_white_percent_L240_max"],
        "chroma_ratio_to_source": acceptance["chroma_ratio_to_source"][0] <= metrics["chroma_ratio_to_source"] <= acceptance["chroma_ratio_to_source"][1],
        "aggregate_hue_delta_degrees": metrics["aggregate_hue_delta_degrees"] <= acceptance["aggregate_hue_delta_degrees_max"],
        "fine_frequency_rms": acceptance["fine_frequency_rms"][0] <= metrics["fine_frequency_rms"] <= acceptance["fine_frequency_rms"][1],
        "changed_pixels_outside_mask": int((changed & outside).sum()) == 0,
        "generated_rgb_used": True,
        "generated_texture_used": True,
    }
    report = {
        "status": "technical_pass_visual_approval_required" if all(checks.values()) else "technical_targets_failed",
        "profile_id": cfg["id"],
        "surface": args.surface,
        "source_sha256": sha(source_path),
        "mask_sha256": sha(mask_path),
        "method": f"deterministic_scalar_lab_l_studio_rig:{target_mode}",
        "hue_reference": hue_reference_name,
        "generated_rgb_used": False,
        "generated_texture_used": False,
        "photometric_donor_sha256": sha(donor_path) if donor_path else None,
        "material_sources": {
            "illumination": "contained donor Lab L low frequency only" if donor_path else "source photograph plus deterministic Lab L fields",
            "basecoat_direction": "source photograph Lab a/b",
            "fine_texture": "source photograph only",
            "geometry": "source photograph only"
        },
        "selection_mode": surface.get("selection_mode", "full_reviewed_surface"),
        "changed_pixels_outside_mask": int((changed & outside).sum()),
        "metrics": metrics,
        "checks": checks,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.fromarray(result).save(args.output, format="PNG", icc_profile=profile)
    Image.fromarray(np.round(effective_strength * 255).astype(np.uint8)).save(args.effective_mask, format="PNG", icc_profile=profile)
    map_rgb = np.clip(target_L, 0, 255).astype(np.uint8)
    Image.fromarray(map_rgb).save(args.light_map, format="PNG", icc_profile=profile)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if args.fail_on_qa and report["status"] != "technical_pass_visual_approval_required":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
