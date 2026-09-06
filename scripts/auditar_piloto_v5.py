"""Audit that the final treated source changes only the approved local masks."""
from pathlib import Path
import hashlib
import json
import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "trabalhos/panamera/studio-v2/dianteira-3-4/source-srgb.png"
TREATED = ROOT / "trabalhos/panamera/refinamento-dianteira-v8-final-source/carro-fonte-tratado.png"
MASKS = {
    "para_brisa": ROOT / "trabalhos/panamera/refinamento-dianteira-v4/para-brisa-editar.png",
    "capo": ROOT / "trabalhos/panamera/refinamento-dianteira-v4/capo-editar.png",
    "lateral": ROOT / "trabalhos/panamera/refinamento-dianteira-v4/lateral-editar.png",
}
REPORT = ROOT / "trabalhos/panamera/refinamento-dianteira-v8-final-source/qa-fidelidade-fonte.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    original = np.asarray(Image.open(ORIGINAL).convert("RGB"))
    treated = np.asarray(Image.open(TREATED).convert("RGB"))
    if original.shape != treated.shape:
        raise RuntimeError(f"Dimension mismatch: {original.shape} != {treated.shape}")
    edit_union = np.zeros(original.shape[:2], dtype=bool)
    mask_pixels = {}
    for name, path in MASKS.items():
        mask = np.asarray(Image.open(path).convert("L")) > 0
        edit_union |= mask
        mask_pixels[name] = int(mask.sum())
    delta = np.max(np.abs(original.astype(np.int16)-treated.astype(np.int16)), axis=2)
    outside = ~edit_union
    changed_outside = int(np.count_nonzero(delta[outside]))
    if changed_outside:
        raise RuntimeError(f"Found {changed_outside} changed pixels outside approved masks")
    report = {
        "status": "technical_containment_passed_visual_approval_pending",
        "source_size": [int(original.shape[1]), int(original.shape[0])],
        "source_sha256": sha(ORIGINAL),
        "treated_sha256": sha(TREATED),
        "editable_pixels_by_mask": mask_pixels,
        "editable_union_pixels": int(edit_union.sum()),
        "protected_pixels": int(outside.sum()),
        "changed_pixels_outside_approved_masks": changed_outside,
        "max_rgb_change_outside_approved_masks_8bit": int(delta[outside].max()),
        "interpretation": "Geometry/details outside windshield, hood and continuous side masks are byte-identical to the source. Plate artwork is applied later inside the measured source quadrilateral."
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
