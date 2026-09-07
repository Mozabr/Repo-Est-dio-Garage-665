#!/usr/bin/env python3
"""Build continuous body-side masks without filling protected cutouts."""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]
MASK_ROOT = ROOT / "trabalhos/panamera/refinamento-dianteira-v6f/preparo-lateral"


def main() -> None:
    fender = np.asarray(Image.open(MASK_ROOT / "M13-paralama-proximo-editar.png").convert("L"), dtype=np.uint8)
    upper = np.asarray(Image.open(MASK_ROOT / "M14-portas-superiores-editar.png").convert("L"), dtype=np.uint8)
    lower = np.asarray(Image.open(MASK_ROOT / "M15-portas-inferiores-editar.png").convert("L"), dtype=np.uint8)
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()

    for name, union, kernel_size in (
        ("M14M15-portas-continuas-editar.png", np.maximum(upper, lower), 25),
        ("M13M14M15-lateral-continua-editar.png", np.maximum.reduce((fender, upper, lower)), 19),
    ):
        # Close only narrow artificial segmentation gaps. Protected handle and
        # badge notches are larger and remain open.
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        core = cv2.morphologyEx((union >= 128).astype(np.uint8) * 255, cv2.MORPH_CLOSE, kernel)
        feather = cv2.GaussianBlur(core.astype(np.float32) / 255.0, (0, 0), 2.0)
        result = np.round(np.clip(feather, 0, 1) * 255).astype(np.uint8)
        out = MASK_ROOT / name
        Image.fromarray(result).save(out, format="PNG", icc_profile=profile)
        print(out)


if __name__ == "__main__":
    main()
