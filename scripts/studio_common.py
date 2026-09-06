"""Shared colour-managed, premultiplied-alpha composition primitives."""
from io import BytesIO
import cv2
import numpy as np
from PIL import Image, ImageCms, ImageOps

SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))

def load_srgb(path):
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im)
        profile = im.info.get("icc_profile")
        rgb = im.convert("RGB")
        if profile:
            rgb = ImageCms.profileToProfile(rgb, ImageCms.ImageCmsProfile(BytesIO(profile)), SRGB, outputMode="RGB")
        return rgb

def linear(rgb):
    a = np.asarray(rgb, np.float32)
    return np.where(a <= .04045, a / 12.92, ((a + .055) / 1.055) ** 2.4)

def srgb(rgb):
    a = np.clip(rgb, 0, 1)
    return np.where(a <= .0031308, a * 12.92, 1.055 * np.power(a, 1 / 2.4) - .055)

def save_rgb(path, rgb):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(rgb, Image.Image):
        rgb = Image.fromarray(np.round(np.clip(rgb, 0, 1)*255).astype(np.uint8))
    rgb.save(path, icc_profile=SRGB.tobytes())

def warp_rgba(rgb, alpha, transform, size):
    """Warp premultiplied linear RGB to prevent black/white fringes."""
    premult = linear(rgb) * alpha[..., None]
    warped_a = np.clip(cv2.warpPerspective(alpha, transform, size, flags=cv2.INTER_LINEAR), 0, 1)
    warped_rgb = cv2.warpPerspective(premult, transform, size, flags=cv2.INTER_LINEAR)
    return warped_rgb, warped_a
