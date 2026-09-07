#!/usr/bin/env python3
"""Build glossy paint from AI illumination plus source color and microtexture."""
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


def masked_blur(channel: np.ndarray, weight: np.ndarray, sigma: float) -> np.ndarray:
    numerator = cv2.GaussianBlur(channel * weight, (0, 0), sigma)
    denominator = cv2.GaussianBlur(weight, (0, 0), sigma)
    return numerator / np.maximum(denominator, 1e-4)


def rms(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(values.astype(np.float32)))))


def weighted_circular_mean(angle: np.ndarray, weight: np.ndarray) -> float:
    """Return a robust mean hue direction in radians."""
    vector = np.sum(weight * np.exp(1j * angle))
    if abs(vector) < 1e-6:
        raise ValueError("Insufficient chromatic direction for aggregate hue metric")
    return float(np.angle(vector))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/perfil-material-v6f.json")
    parser.add_argument(
        "--donor",
        type=Path,
        help="Doador fotometrico alternativo. O RGB nunca e incorporado; somente Lab L alinhado.",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--light-map", type=Path, required=True)
    parser.add_argument("--aligned-donor", type=Path, required=True)
    parser.add_argument("--effective-mask", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument(
        "--fail-on-qa",
        action="store_true",
        help="Encerra com erro depois de salvar o diagnostico quando qualquer gate falhar.",
    )
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text())
    hood = cfg["hood"]
    registration = cfg["registration"]
    bands = cfg["frequency_separation"]
    color = cfg["color_lock"]
    source_path = ROOT / hood["source"]
    donor_path = args.donor.resolve() if args.donor else ROOT / hood["donor"]
    mask_path = ROOT / hood["mask"]
    source = np.asarray(Image.open(source_path).convert("RGB"), dtype=np.uint8)
    donor = np.asarray(Image.open(donor_path).convert("RGB").resize((source.shape[1], source.shape[0]), Image.Resampling.LANCZOS), dtype=np.uint8)
    strength = np.asarray(Image.open(mask_path).convert("L"), dtype=np.float32) / 255.0
    core = strength >= 0.5
    safe = np.where(strength == 0, 255, 0).astype(np.uint8)

    source_gray = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
    donor_gray = cv2.cvtColor(donor, cv2.COLOR_RGB2GRAY)
    # Keep the same stable detector density used by the v6e registration audit.
    # A denser field admitted weak room-texture matches and reduced the inlier
    # fraction even though the residual error stayed low.
    orb = cv2.ORB_create(nfeatures=3500)
    key_source, desc_source = orb.detectAndCompute(source_gray, safe)
    key_donor, desc_donor = orb.detectAndCompute(donor_gray, safe)
    if desc_source is None or desc_donor is None:
        raise ValueError("Insufficient descriptors for donor registration")
    pairs = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(desc_source, desc_donor, k=2)
    matches = [m for pair in pairs if len(pair) == 2 for m, n in [pair] if m.distance < 0.7 * n.distance]
    if len(matches) < registration["minimum_matches"]:
        raise ValueError(f"Only {len(matches)} registration matches")
    target_points = np.float32([key_source[m.queryIdx].pt for m in matches])
    donor_points = np.float32([key_donor[m.trainIdx].pt for m in matches])
    transform, inliers = cv2.findHomography(donor_points, target_points, cv2.RANSAC, 2.0)
    if transform is None:
        raise ValueError("Homography could not be estimated")
    aligned = cv2.warpPerspective(donor, transform, (source.shape[1], source.shape[0]), flags=cv2.INTER_LANCZOS4)
    inlier_selector = inliers.ravel().astype(bool)
    projected = cv2.perspectiveTransform(donor_points.reshape(-1, 1, 2), transform).reshape(-1, 2)
    reprojection = np.linalg.norm(projected - target_points, axis=1)
    inlier_fraction = float(inlier_selector.mean())
    reprojection_p95 = float(np.percentile(reprojection[inlier_selector], 95))
    ys, xs = np.nonzero(core)
    bounds = np.float32([[[xs.min(), ys.min()], [xs.max(), ys.min()], [xs.max(), ys.max()], [xs.min(), ys.max()]]])
    movement = np.linalg.norm(cv2.perspectiveTransform(bounds, transform) - bounds, axis=2)
    maximum_movement = float(movement.max())
    registration_pass = (
        inlier_fraction >= registration["minimum_inlier_fraction"]
        and reprojection_p95 <= registration["maximum_inlier_reprojection_p95_px"]
        and maximum_movement <= registration["maximum_transform_displacement_px"]
    )
    if not registration_pass:
        raise ValueError(
            f"Donor rejected: inliers={inlier_fraction:.3f}, reprojection_p95={reprojection_p95:.3f}, movement={maximum_movement:.3f}"
        )

    source_lab = cv2.cvtColor(source, cv2.COLOR_RGB2LAB).astype(np.float32)
    donor_lab = cv2.cvtColor(aligned, cv2.COLOR_RGB2LAB).astype(np.float32)
    weight = np.clip(strength, 0, 1).astype(np.float32)
    # The API mask protects a deliberately generous area around the crest. For
    # local material transfer, relight that surrounding paint and protect only
    # a tight ellipse containing the physical badge, avoiding a blue halo.
    process_weight = weight.copy()
    emblem = cfg["emblem_lock"]
    cx, cy = emblem["crop_center_xy"]
    rx, ry = emblem["preserve_radius_xy"]
    yy, xx = np.ogrid[:weight.shape[0], :weight.shape[1]]
    # Threshold the fully editable core so the entire feathered crest-exclusion
    # ring is treated as a hole. The outer hood feather remains connected to
    # image background and is therefore not filled by the flood operation.
    binary_weight = (weight >= 0.95).astype(np.uint8)
    inverse = 1 - binary_weight
    flood = inverse.copy()
    cv2.floodFill(flood, None, (0, 0), 2)
    enclosed_holes = (flood == 1).astype(np.float32)
    ellipse_distance = np.sqrt(np.square((xx - cx) / rx) + np.square((yy - cy) / ry))
    # Fill only the oversized hole around the crest, not the outer hood edge.
    # Turning the whole closed mask on would destroy its feather and reveal the
    # polygon as a pasted patch. The badge itself remains copied from source.
    # Fill only enclosed protection holes. Flood-fill distinguishes the crest
    # hole from the outer background, preserving the reviewed hood feather.
    process_weight = np.maximum(process_weight, enclosed_holes)
    if emblem.get("mode") == "warm_chroma_convex_hull":
        warm = (
            (source_lab[:, :, 1] >= emblem["lab_a_min"])
            & (source_lab[:, :, 2] >= emblem["lab_b_min"])
            & (ellipse_distance <= 1.35)
        )
        component_count, labels, stats, _ = cv2.connectedComponentsWithStats(warm.astype(np.uint8), 8)
        if component_count > 1:
            largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
            badge_keep = np.where(labels == largest, 255, 0).astype(np.uint8)
            dilation = emblem["dilate_px"]
            badge_keep = cv2.dilate(
                badge_keep,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilation * 2 + 1, dilation * 2 + 1)),
            )
            badge_keep = cv2.GaussianBlur(badge_keep.astype(np.float32) / 255.0, (0, 0), emblem["feather_px"])
        else:
            badge_keep = (ellipse_distance <= 1.0).astype(np.float32)
    else:
        badge_keep = (ellipse_distance <= 1.0).astype(np.float32)
    process_weight *= 1.0 - badge_keep
    core = process_weight >= 0.5

    # The base illumination is strictly low-frequency. Using the lightly
    # denoised donor as the base accidentally copied contour/noise patterns and
    # made the paint look processed. Mid-frequency specular shape is added in a
    # separate bounded band below.
    donor_clean = cv2.GaussianBlur(
        donor_lab[:, :, 0],
        (0, 0),
        max(bands["donor_denoise_sigma"], bands["specular_outer_sigma"]),
    )
    low_p05, low_p95 = np.percentile(donor_clean[core], (5, 95))
    normalized_low = np.clip((donor_clean - low_p05) / max(1e-4, low_p95 - low_p05), 0, 1)
    target_low = bands["target_low_L_p05"] + normalized_low * (bands["target_low_L_p95"] - bands["target_low_L_p05"])
    donor_specular_inner = cv2.GaussianBlur(donor_lab[:, :, 0], (0, 0), bands["specular_inner_sigma"])
    donor_specular_outer = cv2.GaussianBlur(donor_lab[:, :, 0], (0, 0), bands["specular_outer_sigma"])
    donor_mid = (donor_specular_inner - donor_specular_outer) * bands["specular_contrast_gain"]
    target_mid = np.clip(donor_mid, -bands["maximum_mid_delta_L"], bands["maximum_mid_delta_L"])
    if bands.get("source_texture_mode") == "bilateral_residual":
        texture_base = cv2.bilateralFilter(
            source_lab[:, :, 0],
            bands["source_texture_bilateral_diameter"],
            bands["source_texture_bilateral_sigma_color"],
            bands["source_texture_bilateral_sigma_space"],
        )
        source_fine = source_lab[:, :, 0] - texture_base
    else:
        source_fine = source_lab[:, :, 0] - cv2.GaussianBlur(source_lab[:, :, 0], (0, 0), bands["fine_sigma"])
    gx = cv2.Sobel(source_lab[:, :, 0], cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(source_lab[:, :, 0], cv2.CV_32F, 0, 1, ksize=3)
    tensor_sigma = bands["structure_tensor_sigma"]
    jxx = cv2.GaussianBlur(gx * gx, (0, 0), tensor_sigma)
    jyy = cv2.GaussianBlur(gy * gy, (0, 0), tensor_sigma)
    jxy = cv2.GaussianBlur(gx * gy, (0, 0), tensor_sigma)
    coherence = np.sqrt(np.square(jxx - jyy) + 4 * np.square(jxy)) / np.maximum(jxx + jyy, 1e-4)
    source_mid = cv2.GaussianBlur(source_lab[:, :, 0], (0, 0), bands["specular_inner_sigma"]) - cv2.GaussianBlur(source_lab[:, :, 0], (0, 0), bands["specular_outer_sigma"])
    source_mid *= 1.0 - coherence * bands["directional_edge_suppression"]
    source_mid = np.clip(source_mid, -bands["maximum_source_mid_delta_L"], bands["maximum_source_mid_delta_L"])
    target_mid += source_mid * bands["source_mid_retention"]
    texture_isotropy = np.clip(
        1.0 - coherence * bands["directional_edge_suppression"], 0.0, 1.0
    )
    source_fine *= texture_isotropy
    source_fine = np.clip(source_fine, -bands["maximum_source_fine_delta_L"], bands["maximum_source_fine_delta_L"])

    target_lab = source_lab.copy()
    target_lab[:, :, 0] = target_low + target_mid + source_fine * bands["source_fine_retention"]
    center_key = bands.get("center_key")
    if center_key and center_key.get("enabled", False):
        key_cx, key_cy = center_key["center_xy"]
        key_rx, key_ry = center_key["radius_xy"]
        key_distance = np.square((xx - key_cx) / key_rx) + np.square((yy - key_cy) / key_ry)
        key_field = np.exp(-0.5 * key_distance * center_key.get("falloff", 2.0))
        target_lab[:, :, 0] += key_field * center_key["peak_delta_L"]
    if color.get("mode") == "exact_source_lab_ab":
        # Preserve the measured color-direction channels pixel for pixel. The
        # donor is not allowed to neutralize, recolor or synthesize basecoat.
        target_lab[:, :, 1:3] = source_lab[:, :, 1:3]
    elif color.get("mode") == "neutral_specular_over_source_basecoat":
        # A clear-coat highlight carries the neutral studio-light color, while
        # the darker basecoat keeps the measured source hue. Scale chroma along
        # its original vector (no hue rotation) according to relit luminance.
        t = np.clip(
            (target_lab[:, :, 0] - color["neutralization_L_start"])
            / (color["neutralization_L_end"] - color["neutralization_L_start"]),
            0,
            1,
        )
        retention = color["shadow_chroma_retention"] * (1 - t) + color["highlight_chroma_retention"] * t
        source_a = cv2.GaussianBlur(source_lab[:, :, 1], (0, 0), color["source_chroma_low_sigma"])
        source_b = cv2.GaussianBlur(source_lab[:, :, 2], (0, 0), color["source_chroma_low_sigma"])
        target_lab[:, :, 1] = 128.0 + (source_a - 128.0) * retention
        target_lab[:, :, 2] = 128.0 + (source_b - 128.0) * retention
    else:
        source_ab_low = np.stack(
            [cv2.GaussianBlur(source_lab[:, :, channel], (0, 0), color["source_chroma_low_sigma"]) for channel in (1, 2)],
            axis=2,
        )
        neutral_vector = source_ab_low - 128.0
        proposed_ab = 128.0 + neutral_vector * color["chroma_retention"]
        ab_shift = proposed_ab - source_ab_low
        shift_norm = np.linalg.norm(ab_shift, axis=2, keepdims=True)
        ab_shift *= np.minimum(1.0, color["maximum_ab_shift_from_source"] / np.maximum(shift_norm, 1e-4))
        for offset, channel in enumerate((1, 2)):
            fine_ab = source_lab[:, :, channel] - cv2.GaussianBlur(source_lab[:, :, channel], (0, 0), bands["fine_sigma"])
            fine_ab = np.clip(fine_ab, -color["maximum_fine_ab"], color["maximum_fine_ab"])
            target_lab[:, :, channel] = source_ab_low[:, :, offset] + ab_shift[:, :, offset] + fine_ab * color["source_fine_chroma_retention"]

    relit = cv2.cvtColor(np.clip(target_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
    alpha = process_weight[:, :, None]
    result = np.round(source * (1 - alpha) + relit * alpha).astype(np.uint8)
    outside = process_weight == 0
    result[outside] = source[outside]
    if not np.array_equal(result[outside], source[outside]):
        raise AssertionError("Pixels changed outside the reviewed hood mask")

    result_lab = cv2.cvtColor(result, cv2.COLOR_RGB2LAB).astype(np.float32)
    result_L = result_lab[:, :, 0]
    result_low = cv2.GaussianBlur(result_L, (0, 0), bands["specular_outer_sigma"])
    result_mid = cv2.GaussianBlur(result_L, (0, 0), bands["specular_inner_sigma"]) - result_low
    result_fine = result_L - cv2.GaussianBlur(result_L, (0, 0), bands["fine_sigma"])
    result_chroma = np.sqrt(np.square(result_lab[:, :, 1] - 128) + np.square(result_lab[:, :, 2] - 128))
    source_chroma = np.sqrt(np.square(source_lab[:, :, 1] - 128) + np.square(source_lab[:, :, 2] - 128))
    source_hue = np.arctan2(source_lab[:, :, 2] - 128, source_lab[:, :, 1] - 128)
    result_hue = np.arctan2(result_lab[:, :, 2] - 128, result_lab[:, :, 1] - 128)
    hue_delta = np.angle(np.exp(1j * (result_hue - source_hue)))
    # Hue is undefined in nearly neutral pixels. Measure only pixels with enough
    # source chroma to carry paint-color direction, otherwise tiny Lab rounding
    # errors become large and misleading angle changes.
    hue_valid = core & (source_chroma >= 5.0)
    values = result_L[core]
    basecoat_valid = (
        core
        & (source_chroma >= 5.0)
        & (result_L < color.get("neutralization_L_start", 256.0))
    )
    basecoat_weights = np.clip(source_chroma[basecoat_valid], 5.0, 30.0)
    source_basecoat_hue = weighted_circular_mean(source_hue[basecoat_valid], basecoat_weights)
    result_basecoat_hue = weighted_circular_mean(result_hue[basecoat_valid], basecoat_weights)
    basecoat_hue_delta = float(
        np.degrees(abs(np.angle(np.exp(1j * (result_basecoat_hue - source_basecoat_hue)))))
    )
    source_fine_metric = source_lab[:, :, 0] - cv2.GaussianBlur(
        source_lab[:, :, 0], (0, 0), bands["fine_sigma"]
    )
    metrics = {
        "hood_chroma_mean": float(result_chroma[core].mean()),
        "hood_mid_frequency_rms": rms(result_mid[core]),
        "hood_fine_frequency_rms": rms(result_fine[core]),
        "source_hood_fine_frequency_rms": rms(source_fine_metric[core]),
        "hood_L_p95_minus_p05": float(np.percentile(values, 95) - np.percentile(values, 5)),
        "hood_low_frequency_std": float(np.std(result_low[core])),
        "hood_near_white_percent_L240": float((values >= 240).mean() * 100),
        "hood_chroma_ratio_to_source": float(result_chroma[core].mean() / max(source_chroma[core].mean(), 1e-4)),
        "hood_hue_mean_absolute_delta_degrees": float(np.degrees(np.abs(hue_delta[hue_valid])).mean()),
        "hood_basecoat_aggregate_hue_delta_degrees": basecoat_hue_delta,
    }
    targets = cfg["acceptance_targets"]
    checks = {
        key: targets[key][0] <= value <= targets[key][1]
        for key, value in metrics.items()
        if isinstance(targets.get(key), list)
    }
    checks["hood_near_white_percent_L240"] = metrics["hood_near_white_percent_L240"] <= targets["hood_near_white_percent_L240_max"]
    if "hood_hue_mean_absolute_delta_degrees_max" in targets:
        checks["hood_hue_mean_absolute_delta_degrees"] = (
            metrics["hood_hue_mean_absolute_delta_degrees"] <= targets["hood_hue_mean_absolute_delta_degrees_max"]
        )
    if "hood_basecoat_aggregate_hue_delta_degrees_max" in targets:
        checks["hood_basecoat_aggregate_hue_delta_degrees"] = (
            metrics["hood_basecoat_aggregate_hue_delta_degrees"]
            <= targets["hood_basecoat_aggregate_hue_delta_degrees_max"]
        )
    checks.update({
        "changed_pixels_outside_mask": True,
        "generated_rgb_used": targets["generated_rgb_used"] is False,
        "generated_fine_texture_used": targets["generated_fine_texture_used"] is False,
    })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.fromarray(result).save(args.output, format="PNG", icc_profile=profile)
    Image.fromarray(aligned).save(args.aligned_donor, format="PNG", icc_profile=profile)
    Image.fromarray(np.round(process_weight * 255).astype(np.uint8)).save(args.effective_mask, format="PNG", icc_profile=profile)
    map_normalized = np.clip((target_low + target_mid - 96) / 128 * 255, 0, 255).astype(np.uint8)
    Image.fromarray(map_normalized).save(args.light_map, format="PNG", icc_profile=profile)
    changed = np.any(result != source, axis=2)
    report = {
        "status": "technical_pass_visual_approval_required" if all(checks.values()) else "technical_targets_failed",
        "profile_id": cfg["id"],
        "source_sha256": sha(source_path),
        "donor_sha256": sha(donor_path),
        "mask_sha256": sha(mask_path),
        "registration": {
            "matches": len(matches),
            "inlier_fraction": inlier_fraction,
            "inlier_reprojection_p95_px": reprojection_p95,
            "maximum_transform_displacement_px": maximum_movement,
        },
        "material_sources": {
            "low_and_mid_frequency_illumination": "aligned donor Lab L only",
            "basecoat_direction": "source photograph Lab a/b",
            "fine_texture": "source photograph only",
            "geometry": "source photograph only",
            "center_key": "deterministic scalar Lab L field" if center_key else "disabled",
        },
        "generated_rgb_used": False,
        "generated_fine_texture_used": False,
        "changed_pixels_outside_mask": int((changed & outside).sum()),
        "metrics": metrics,
        "checks": checks,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if args.fail_on_qa and report["status"] != "technical_pass_visual_approval_required":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
