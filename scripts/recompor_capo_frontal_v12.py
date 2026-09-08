#!/usr/bin/env python3
"""Recompose the frontal hood with donor lighting and photographed fine detail."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageCms


def load_rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--lighting-donor", type=Path, required=True)
    parser.add_argument("--mask", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--fine-sigma", type=float, default=1.8)
    parser.add_argument("--fine-gain", type=float, default=0.95)
    args = parser.parse_args()

    source = load_rgb(args.source)
    donor = load_rgb(args.lighting_donor)
    if source.shape != donor.shape:
        raise ValueError("Source and lighting donor must be pixel-aligned")

    mask = np.asarray(Image.open(args.mask).convert("L"), dtype=np.float32) / 255.0
    if mask.shape != source.shape[:2]:
        raise ValueError("Mask must match source dimensions")

    source_lab = cv2.cvtColor(source, cv2.COLOR_RGB2LAB).astype(np.float32)
    donor_lab = cv2.cvtColor(donor, cv2.COLOR_RGB2LAB).astype(np.float32)

    sigma = max(0.6, args.fine_sigma)
    source_fine = source_lab - cv2.GaussianBlur(source_lab, (0, 0), sigma)
    donor_fine = donor_lab - cv2.GaussianBlur(donor_lab, (0, 0), sigma)

    # The rejected V01 contains two vertical borders from the synthetic centre
    # panel. They are narrow enough to leak into the fine band, so source detail
    # is attenuated only in those two strips. Coordinates are normalized to keep
    # the rule stable if the preview size changes.
    height, width = mask.shape
    seam_keep = np.ones((height, width), dtype=np.float32)
    for center_x in (0.400 * width, 0.597 * width):
        half_width = max(5, int(round(width * 0.009)))
        x0 = max(0, int(round(center_x)) - half_width)
        x1 = min(width, int(round(center_x)) + half_width)
        seam_keep[int(height * 0.44) : int(height * 0.61), x0:x1] = 0.0
    seam_keep = cv2.GaussianBlur(seam_keep, (0, 0), max(2.0, width * 0.004))

    # Donor supplies the continuous hood illumination. The source supplies the
    # original fine photographic band and all paint chroma. Medium-frequency
    # source structure is intentionally excluded so the rectangular seam cannot
    # return with the texture.
    target_lab = donor_lab.copy()
    correction = (source_fine - donor_fine) * args.fine_gain
    correction *= seam_keep[:, :, None]
    target_lab += correction
    target = cv2.cvtColor(
        np.clip(target_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB
    ).astype(np.float32)

    strength = np.clip(mask, 0, 1)[:, :, None]
    output = np.round(source.astype(np.float32) * (1 - strength) + target * strength).astype(
        np.uint8
    )
    outside = mask == 0
    output[outside] = source[outside]
    if not np.array_equal(output[outside], source[outside]):
        raise AssertionError("Containment failed")

    result_lab = cv2.cvtColor(output, cv2.COLOR_RGB2LAB).astype(np.float32)
    selector = mask > 0.5
    source_rms = float(np.sqrt(np.mean(np.square(source_fine[:, :, 0][selector]))))
    result_fine = result_lab[:, :, 0] - cv2.GaussianBlur(
        result_lab[:, :, 0], (0, 0), sigma
    )
    result_rms = float(np.sqrt(np.mean(np.square(result_fine[selector]))))
    changed = np.any(output != source, axis=2)
    report = {
        "status": "candidate_requires_visual_approval",
        "method": "donor Lab field plus source fine Lab detail with V01 seam suppression",
        "changed_pixels_outside_mask": int(np.sum(changed & outside)),
        "editable_pixels": int(np.sum(mask > 0)),
        "fine_sigma": args.fine_sigma,
        "fine_gain": args.fine_gain,
        "microdetail_rms_source": source_rms,
        "microdetail_rms_output": result_rms,
        "microdetail_ratio": result_rms / source_rms if source_rms else None,
        "note": "All pixels outside the contained hood mask are copied from V01.",
    }

    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(output).save(args.output, format="PNG", icc_profile=profile)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
