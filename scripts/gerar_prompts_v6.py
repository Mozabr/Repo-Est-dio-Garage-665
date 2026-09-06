#!/usr/bin/env python3
"""Generate locked GPT Image 2 prompts from one immutable lighting rig."""
from __future__ import annotations

import hashlib
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RIG_PATH = ROOT / "config/rig-iluminacao-studio-v6.json"
OUT = ROOT / "prompts/v6"

SURFACES = {
    "M11U-capo-integral": "the complete hood as one continuous physical panel; preserve the Porsche crest, full perimeter shut line, both sculpted creases and both headlight boundaries",
    "M10-teto-pintura": "the narrow visible painted roof panel; preserve roof rails, roof seams and glass boundaries",
    "M11-capo-centro": "the central hood surface; preserve the Porsche crest, shut lines, exact creases and metallic flake",
    "M12-capo-lateral-distante": "the far-side hood shoulder; preserve the far headlight boundary and hood crease",
    "M12-capo-lateral-proxima": "the near-side hood shoulder; preserve the near headlight boundary and hood crease",
    "M13-paralama-proximo": "the near front fender paint; preserve the wheel arch, tire, headlight, sensor and panel gaps",
    "M14-portas-superiores": "the upper visible door paint; preserve handles, chrome trim, mirror and shut lines",
    "M15-portas-inferiores": "the lower visible door paint; preserve rocker trim, shut lines and panel curvature",
    "M16-para-brisa": "the windshield glass only; retain natural transparency and visible cabin, reducing outdoor reflections without darkening the glass",
    "M17-vidros-laterais": "the side glass only; retain the original tint and cabin visibility, removing identifiable outdoor reflections without making it black"
}

SURFACE_GOALS = {
    "M11U-capo-integral": "Treat the hood as one convex continuous metal panel, never as three graphic zones. The overhead diffuser must read only as a restrained low-contrast illumination envelope: it begins broadly near the windshield-side of the hood, follows both original sculpted creases, widens smoothly through the central curvature and fades gradually before the front shut line. Keep the center ridge visible through natural curvature, but create no straight center seam, diagonal division, bilateral split, hard boundary or pasted gray patch. Do not mirror the literal rectangular ceiling, its black perimeter frame or the wall logo. Keep the base paint dark gray; the highlight may lift luminance moderately but must retain metallic flake and clear-coat depth. The transition at the full hood perimeter must be invisible at 200 percent zoom."
}

BASE = """ROLE OF EACH INPUT
Image 1 is the authority source and the only authority for the exact vehicle, camera, perspective, paint color, body geometry, equipment and fine details.
Image 2 is the exact target studio and the authority for illumination direction, neutral color temperature and reflected environment.
Image 3 is identity and material reference only for this same vehicle and paint. Do not copy its camera, background, exposure or outdoor reflections.
Image 4 is a relative-depth or normal-like geometry guide only. Never reproduce its false colors or use it as appearance.
{target_note}

EDIT SCOPE
Change only the transparent area of the supplied mask: {surface}.
Do not alter, regenerate, move, rescale or redraw any other area. Keep the camera and framing pixel-aligned with Image 1.

TARGET
Remove recognizable outdoor reflections only inside this surface. Reconstruct the same photographed dark-gray metallic Porsche paint or glass under the exact studio lighting of Image 2. Preserve original curvature, panel boundaries, clear-coat depth, metallic flake, microtexture, local exposure, paint hue and real photographic detail.
{surface_goal}

LOCKED LIGHTING — {rig_id}
{lighting}

FORBIDDEN
No sky, clouds, trees, buildings, cables, poles, people, other cars, storefronts, street or yellow pavement lines. No clipped white, mirror finish, matte or flat paint, plastic CGI surface, excessive denoise, artificial sharpening, invented detail, invented body line or invented accessory.

INVARIANTS
Do not change the Porsche model, silhouette, proportions, panel boundaries, headlights, wheels, tires, brakes, badges, lettering, sensors, grille, mirror, glass shape, camera angle, framing, license-plate cover or background. Do not recolor the vehicle. The light direction, softness and energy must match the other surfaces from the same locked rig.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rig", type=Path, default=RIG_PATH)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--target-in-studio", action="store_true")
    args = parser.parse_args()
    rig_path = args.rig.resolve()
    out_path = args.out.resolve()
    rig = json.loads(rig_path.read_text())
    out_path.mkdir(parents=True, exist_ok=True)
    manifest = {"rig_id": rig["id"], "rig_path": str(rig_path.relative_to(ROOT)), "rig_sha256": hashlib.sha256(rig_path.read_bytes()).hexdigest(), "prompts": {}}
    for name, description in SURFACES.items():
        target_note = "Image 1 already contains the exact final Studio H background, vehicle scale, position and shadow. Do not recreate, replace or reinterpret the room; edit only the supplied transparent mask on that existing composition." if args.target_in_studio else ""
        prompt = BASE.format(surface=description, rig_id=rig["id"], lighting=rig["prompt_block"], target_note=target_note, surface_goal=SURFACE_GOALS.get(name, "")).strip() + "\n"
        path = out_path / f"{name}.txt"
        path.write_text(prompt)
        manifest["prompts"][name] = {"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(prompt.encode()).hexdigest()}
    (out_path / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
