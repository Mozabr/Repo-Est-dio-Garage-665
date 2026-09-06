#!/usr/bin/env python3
"""Fail-fast audit before any paid GPT Image 2 edit."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline", type=Path, default=ROOT / "config/pipeline-v6.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    pipeline_path = args.pipeline.resolve()
    pipeline = json.loads(pipeline_path.read_text())
    mask_cfg = json.loads((ROOT / "config/refinamento-dianteira-v6.json").read_text())
    rig_path = ROOT / pipeline.get("references", {}).get("lighting_rig", "config/rig-iluminacao-studio-v6.json")
    prompt_manifest_path = ROOT / pipeline.get("references", {}).get("prompt_manifest", "prompts/v6/manifest.json")
    rig = json.loads(rig_path.read_text())
    prompt_manifest = json.loads(prompt_manifest_path.read_text())
    masks_qa = json.loads((ROOT / mask_cfg["out"] / "qa-mascaras-v6.json").read_text())
    guides_qa_path = ROOT / pipeline.get(
        "guides_qa", "trabalhos/panamera/refinamento-dianteira-v6/guias/qa-guias.json"
    )
    guides_qa = json.loads(guides_qa_path.read_text())
    source = ROOT / pipeline["authority_source"]
    work_source = ROOT / pipeline.get("edit_target", mask_cfg["source"])
    work_alpha = ROOT / mask_cfg["vehicle_alpha"]
    edit_mask = ROOT / pipeline["edit_mask"] if pipeline.get("edit_mask") else None
    api_mask = ROOT / pipeline["api_mask"] if pipeline.get("api_mask") else None
    required = [source, work_source, work_alpha, guides_qa_path]
    required.extend(path for path in (edit_mask, api_mask) if path is not None)
    for key in ("studio", "same_paint", "depth", "normal_guide", "lighting_rig", "prompt_manifest"):
        if key in pipeline.get("references", {}):
            required.append((ROOT / pipeline["references"][key]).resolve())
    missing = [str(path) for path in required if not path.exists()]
    expected_size = (pipeline["working"]["width"], pipeline["working"]["height"])
    target_size_ok = False
    if work_source.exists():
        with Image.open(work_source) as image:
            target_size_ok = image.size == expected_size
    mask_sizes_ok = True
    mask_alpha_inverse_ok = True
    if edit_mask is not None and api_mask is not None and edit_mask.exists() and api_mask.exists():
        with Image.open(edit_mask).convert("L") as editable, Image.open(api_mask).convert("RGBA") as api:
            mask_sizes_ok = editable.size == api.size == expected_size
            editable_pixels = np.asarray(editable, dtype=np.int16)
            api_alpha_pixels = np.asarray(api.getchannel("A"), dtype=np.int16)
            # OpenAI image edit convention: transparent pixels are editable.
            # Feathered masks are intentional, so validate inverse alpha rather
            # than incorrectly requiring a binary edge.
            mask_alpha_inverse_ok = int(np.max(np.abs((255 - editable_pixels) - api_alpha_pixels))) <= 2
    prompt_hashes_ok = all(
        sha(ROOT / item["path"]) == item["sha256"] for item in prompt_manifest["prompts"].values()
    )
    checks = {
        "required_files_present": not missing,
        "edit_target_size_matches_api": target_size_ok,
        "edit_and_api_mask_sizes_match_target": mask_sizes_ok,
        "api_alpha_is_inverse_of_edit_strength": mask_alpha_inverse_ok,
        "rig_hash_matches_prompt_manifest": sha(rig_path) == prompt_manifest["rig_sha256"],
        "prompt_hashes_match": prompt_hashes_ok,
        "mask_containment_passed": masks_qa["outside_vehicle_pixels_total"] == 0 and masks_qa["protected_overlap_pixels_total"] == 0,
        "depth_is_guidance_only": guides_qa["depth_is_metric"] is False,
        "one_surface_per_call": pipeline["openai_image_edit"]["surfaces_per_call"] == 1,
        "full_vehicle_generation_blocked": pipeline["hard_rules"]["full_vehicle_generation"] is False
    }
    status = "ready_for_visual_mask_review" if all(checks.values()) else "blocked"
    report = {"status": status, "pipeline": str(pipeline_path.relative_to(ROOT)), "rig_id": rig["id"], "checks": checks, "missing": missing}
    out = args.output or ROOT / f"trabalhos/panamera/refinamento-dianteira-v6/qa-preflight-{pipeline_path.stem}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if status == "blocked":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
