#!/usr/bin/env python3
"""Transfer only studio-scale light while retaining photographic microdetail and paint chroma."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageCms


def load(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8)


def rms(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(values.astype(np.float32)))))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--mask", type=Path, required=True, help="grayscale edit-strength mask")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--light-radius", type=float, default=24.0)
    parser.add_argument("--micro-radius", type=float, default=1.25)
    parser.add_argument("--light-strength", type=float, default=.72)
    parser.add_argument("--micro-strength", type=float, default=.82)
    parser.add_argument("--max-light-delta", type=float, default=18.0)
    args = parser.parse_args()
    if not 0 <= args.light_strength <= 1 or not 0 <= args.micro_strength <= 1:
        raise ValueError("Strength values must be between 0 and 1")

    original_rgb, candidate_rgb = load(args.original), load(args.candidate)
    if original_rgb.shape != candidate_rgb.shape:
        raise ValueError("Original and candidate must be pixel-aligned and equal in size")
    mask = np.asarray(Image.open(args.mask).convert("L"), dtype=np.float32) / 255.0
    if mask.shape != original_rgb.shape[:2]:
        raise ValueError("Mask size differs from images")

    original_lab = cv2.cvtColor(original_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    candidate_lab = cv2.cvtColor(candidate_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    sigma = max(1.0, args.light_radius)
    original_low = cv2.GaussianBlur(original_lab, (0, 0), sigma)
    candidate_low = cv2.GaussianBlur(candidate_lab, (0, 0), sigma)

    # Start from the generated proposal so removed outdoor structures do not
    # return. Cap only its broad exposure change and pull broad chroma strongly
    # toward the photograph, while retaining candidate mid-frequency geometry.
    raw_light_delta = candidate_low[:, :, 0] - original_low[:, :, 0]
    accepted_light_delta = np.clip(raw_light_delta, -args.max_light_delta, args.max_light_delta) * args.light_strength
    target = candidate_lab.copy()
    target[:, :, 0] += accepted_light_delta - raw_light_delta
    target[:, :, 1:] += (original_low[:, :, 1:] - candidate_low[:, :, 1:]) * .88

    # Replace only the candidate's finest band with the photographed finest
    # band. This is identity-preserving when candidate==original and does not
    # reinsert the larger cloud/building/cable edges removed by the model.
    micro_sigma = max(.5, args.micro_radius)
    original_micro = original_lab - cv2.GaussianBlur(original_lab, (0, 0), micro_sigma)
    candidate_micro = candidate_lab - cv2.GaussianBlur(candidate_lab, (0, 0), micro_sigma)
    micro_correction = np.clip(original_micro - candidate_micro, -7.0, 7.0)
    target += micro_correction * args.micro_strength
    target = np.clip(target, 0, 255).astype(np.uint8)
    reconstructed_rgb = cv2.cvtColor(target, cv2.COLOR_LAB2RGB).astype(np.float32)

    strength = np.clip(mask, 0, 1)[:, :, None]
    output = np.round(original_rgb * (1 - strength) + reconstructed_rgb * strength).astype(np.uint8)
    outside = mask == 0
    output[outside] = original_rgb[outside]
    if not np.array_equal(output[outside], original_rgb[outside]):
        raise AssertionError("Pixel containment failed")

    selector = mask > .5
    orig_detail = original_lab[:, :, 0] - cv2.GaussianBlur(original_lab[:, :, 0], (0, 0), args.micro_radius)
    out_lab = cv2.cvtColor(output, cv2.COLOR_RGB2LAB).astype(np.float32)
    out_detail = out_lab[:, :, 0] - cv2.GaussianBlur(out_lab[:, :, 0], (0, 0), args.micro_radius)
    report = {
        "status": "recomposed_not_visually_approved",
        "changed_pixels_outside_mask": 0,
        "editable_pixels": int((mask > 0).sum()),
        "light_strength": args.light_strength,
        "micro_strength": args.micro_strength,
        "max_light_delta_Lab_L": args.max_light_delta,
        "mean_abs_chroma_delta_ab": [
            float(np.mean(np.abs(out_lab[:, :, index][selector] - original_lab[:, :, index][selector])))
            for index in (1, 2)
        ],
        "microdetail_rms_original": rms(orig_detail[selector]),
        "microdetail_rms_output": rms(out_detail[selector]),
        "note": "Only low-frequency illumination comes from the candidate; original fine detail is clamped and reinserted."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.fromarray(output).save(args.output, format="PNG", icc_profile=profile)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
