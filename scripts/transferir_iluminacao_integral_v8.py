#!/usr/bin/env python3
"""Transfer only aligned low-frequency Lab L from a generated lighting donor."""
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


def smooth_interior(mask: np.ndarray, transition: float) -> np.ndarray:
    core = (mask >= 0.5).astype(np.uint8)
    distance = cv2.distanceTransform(core, cv2.DIST_L2, 5)
    interior = np.clip(distance / transition, 0.0, 1.0)
    interior = interior * interior * (3.0 - 2.0 * interior)
    return mask * interior


def register(source: np.ndarray, donor: np.ndarray, editable: np.ndarray, cfg: dict):
    safe = np.where(editable == 0, 255, 0).astype(np.uint8)
    orb = cv2.ORB_create(nfeatures=5000)
    key_source, desc_source = orb.detectAndCompute(cv2.cvtColor(source, cv2.COLOR_RGB2GRAY), safe)
    key_donor, desc_donor = orb.detectAndCompute(cv2.cvtColor(donor, cv2.COLOR_RGB2GRAY), safe)
    if desc_source is None or desc_donor is None:
        raise ValueError("Insufficient registration descriptors")
    pairs = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(desc_source, desc_donor, k=2)
    matches = [m for pair in pairs if len(pair) == 2 for m, n in [pair] if m.distance < 0.7 * n.distance]
    if len(matches) < cfg["minimum_matches"]:
        raise ValueError(f"Only {len(matches)} registration matches")
    target = np.float32([key_source[m.queryIdx].pt for m in matches])
    origin = np.float32([key_donor[m.trainIdx].pt for m in matches])
    transform, inliers = cv2.findHomography(origin, target, cv2.RANSAC, 2.0)
    if transform is None:
        raise ValueError("Registration failed")
    height, width = source.shape[:2]
    aligned = cv2.warpPerspective(donor, transform, (width, height), flags=cv2.INTER_LANCZOS4)
    bounds = np.float32([[[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]]])
    movement = np.linalg.norm(cv2.perspectiveTransform(bounds, transform) - bounds, axis=2)
    report = {
        "matches": len(matches),
        "inlier_fraction": float(inliers.mean()),
        "maximum_registration_displacement_px": float(movement.max()),
        "transform": transform.tolist(),
    }
    report["passed"] = (
        report["inlier_fraction"] >= cfg["minimum_inlier_fraction"]
        and report["maximum_registration_displacement_px"] <= cfg["maximum_displacement_px"]
    )
    return aligned, report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/harmonizacao-integral-v8.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--aligned-donor", type=Path, required=True)
    parser.add_argument("--effective-mask", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--fail-on-qa", action="store_true")
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text())
    source_path = ROOT / cfg["authority"]
    donor_path = ROOT / cfg["lighting_donor"]
    mask_root = ROOT / cfg["mask_root"]
    source_image = Image.open(source_path).convert("RGB")
    source = np.asarray(source_image, dtype=np.uint8)
    donor = np.asarray(Image.open(donor_path).convert("RGB").resize(source_image.size, Image.Resampling.LANCZOS), dtype=np.uint8)
    registration_mask = np.asarray(Image.open(mask_root / cfg["registration_mask"]).convert("L"), dtype=np.uint8)
    donor, registration = register(source, donor, registration_mask, cfg["registration"])
    if not registration["passed"]:
        raise SystemExit("Donor rejected by registration gate")

    source_lab = cv2.cvtColor(source, cv2.COLOR_RGB2LAB).astype(np.float32)
    donor_lab = cv2.cvtColor(donor, cv2.COLOR_RGB2LAB).astype(np.float32)
    source_L = source_lab[:, :, 0]
    donor_L = donor_lab[:, :, 0]
    accumulated_delta = np.zeros_like(source_L)
    accumulated_weight = np.zeros_like(source_L)
    surface_reports = {}

    for surface in cfg["surfaces"]:
        mask = np.asarray(Image.open(mask_root / surface["mask"]).convert("L"), dtype=np.float32) / 255.0
        weight = smooth_interior(mask, surface["transition_px"])
        source_low = cv2.GaussianBlur(source_L, (0, 0), surface["low_sigma"])
        donor_low = cv2.GaussianBlur(donor_L, (0, 0), surface["low_sigma"])
        delta = np.clip(
            (donor_low - source_low) * surface["gain"] + surface.get("lift_L", 0.0),
            -surface["maximum_delta_L"],
            surface["maximum_delta_L"],
        )
        accumulated_delta += delta * weight
        accumulated_weight += weight
        active = weight >= 0.05
        surface_reports[surface["id"]] = {
            "active_pixels": int(active.sum()),
            "mean_delta_L": float(delta[active].mean()) if np.any(active) else 0.0,
            "p95_absolute_delta_L": float(np.percentile(np.abs(delta[active]), 95)) if np.any(active) else 0.0,
        }

    union = accumulated_weight > 0
    # Convert the independently feathered surface corrections into one continuous
    # low-frequency lighting field. Normalized convolution avoids dark bands at
    # internal mask boundaries without importing donor texture or RGB pixels.
    seam_sigma = float(cfg.get("seam_smoothing_sigma", 0.0))
    if seam_sigma > 0:
        blurred_delta = cv2.GaussianBlur(accumulated_delta, (0, 0), seam_sigma)
        blurred_weight = cv2.GaussianBlur(accumulated_weight, (0, 0), seam_sigma)
        stable = blurred_weight > 1e-5
        continuous_delta = np.zeros_like(source_L)
        continuous_delta[stable] = blurred_delta[stable] / blurred_weight[stable]
    else:
        continuous_delta = np.zeros_like(source_L)
        continuous_delta[union] = accumulated_delta[union] / accumulated_weight[union]
    normalized_delta = np.zeros_like(source_L)
    normalized_delta[union] = continuous_delta[union]
    target_lab = source_lab.copy()
    target_lab[:, :, 0] = np.clip(source_L + normalized_delta, 0, 255)
    result = cv2.cvtColor(target_lab.astype(np.uint8), cv2.COLOR_LAB2RGB)

    protected = np.asarray(Image.open(mask_root / cfg["protected_mask"]).convert("L"), dtype=np.uint8) > 0
    result[protected] = source[protected]
    result[~union] = source[~union]
    changed = np.any(result != source, axis=2)
    result_lab = cv2.cvtColor(result, cv2.COLOR_RGB2LAB).astype(np.float32)
    absolute_delta = np.abs(result_lab[:, :, 0] - source_L)
    source_chroma = np.hypot(source_lab[:, :, 1] - 128, source_lab[:, :, 2] - 128)
    result_chroma = np.hypot(result_lab[:, :, 1] - 128, result_lab[:, :, 2] - 128)
    active_values = result_lab[:, :, 0][union]
    metrics = {
        "changed_pixels_outside_union": int((changed & ~union).sum()),
        "changed_pixels_in_protected_mask": int((changed & protected).sum()),
        "mean_absolute_delta_L": float(absolute_delta[union].mean()),
        "p95_absolute_delta_L": float(np.percentile(absolute_delta[union], 95)),
        "near_white_percent_L240": float((active_values >= 240).mean() * 100),
        "chroma_ratio_to_source": float(result_chroma[union].mean() / max(source_chroma[union].mean(), 1e-4)),
    }
    limits = cfg["acceptance"]
    checks = {
        "changed_pixels_outside_union": metrics["changed_pixels_outside_union"] == limits["changed_pixels_outside_union"],
        "changed_pixels_in_protected_mask": metrics["changed_pixels_in_protected_mask"] == limits["changed_pixels_in_protected_mask"],
        "mean_absolute_delta_L": metrics["mean_absolute_delta_L"] <= limits["mean_absolute_delta_L_max"],
        "p95_absolute_delta_L": metrics["p95_absolute_delta_L"] <= limits["p95_absolute_delta_L_max"],
        "near_white_percent_L240": metrics["near_white_percent_L240"] <= limits["near_white_percent_L240_max"],
        "chroma_ratio_to_source": limits["chroma_ratio_to_source"][0] <= metrics["chroma_ratio_to_source"] <= limits["chroma_ratio_to_source"][1],
        "registration": registration["passed"],
    }
    report = {
        "status": "technical_pass_visual_approval_required" if all(checks.values()) else "technical_targets_failed",
        "profile_id": cfg["id"],
        "authority_sha256": sha(source_path),
        "lighting_donor_sha256": sha(donor_path),
        "method": "registered_generated_donor_low_frequency_L_only",
        "seam_smoothing_sigma": seam_sigma,
        "generated_rgb_used": False,
        "generated_texture_used": False,
        "source_geometry_used": True,
        "source_chroma_used": True,
        "source_details_reinserted": True,
        "registration": registration,
        "surfaces": surface_reports,
        "metrics": metrics,
        "checks": checks,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.fromarray(result).save(args.output, format="PNG", icc_profile=profile)
    Image.fromarray(donor).save(args.aligned_donor, format="PNG", icc_profile=profile)
    Image.fromarray(np.round(np.clip(accumulated_weight, 0, 1) * 255).astype(np.uint8)).save(args.effective_mask, format="PNG")
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if args.fail_on_qa and not all(checks.values()):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
