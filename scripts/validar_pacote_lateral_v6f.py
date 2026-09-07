#!/usr/bin/env python3
"""Fail-fast audit before one paid GPT Image 2 lateral-surface edit."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    pipeline_path = args.pipeline.resolve()
    cfg = json.loads(pipeline_path.read_text(encoding="utf-8"))
    target = ROOT / cfg["edit_target"]
    edit_mask = ROOT / cfg["edit_mask"]
    api_mask = ROOT / cfg["api_mask"]
    studio = ROOT / cfg["references"]["studio"]
    rig_path = ROOT / cfg["references"]["lighting_rig"]
    manifest_path = ROOT / cfg["references"]["prompt_manifest"]
    prompt_path = ROOT / cfg["references"]["prompt"]
    required = [target, edit_mask, api_mask, studio, rig_path, manifest_path, prompt_path]
    missing = [str(path) for path in required if not path.exists()]
    checks: dict[str, bool] = {
        "openai_api_key_present": bool(os.environ.get("OPENAI_API_KEY")),
        "required_files_present": not missing,
        "one_surface_per_call": cfg["openai_image_edit"]["surfaces_per_call"] == 1,
        "one_candidate_per_surface": cfg["openai_image_edit"]["candidates_per_surface"] == 1,
        "full_vehicle_generation_blocked": cfg["hard_rules"]["full_vehicle_generation"] is False,
        "generated_rgb_blocked": cfg["hard_rules"]["donor_rgb_may_be_used"] is False,
        "generated_fine_texture_blocked": cfg["hard_rules"]["donor_fine_texture_may_be_used"] is False,
        "model_snapshot_locked": cfg["openai_image_edit"]["model"] == "gpt-image-2-2026-04-21",
        "quality_high": cfg["openai_image_edit"]["quality"] == "high",
        "input_fidelity_parameter_omitted": cfg["openai_image_edit"]["input_fidelity_parameter"] == "omit",
    }

    if not missing:
        expected_size = (cfg["working"]["width"], cfg["working"]["height"])
        with Image.open(target) as image, Image.open(edit_mask) as edit, Image.open(api_mask) as api:
            checks["target_and_masks_match_configured_size"] = (
                image.size == edit.size == api.size == expected_size
            )
            checks["api_mask_has_alpha"] = api.mode in {"RGBA", "LA"}
            edit_pixels = np.asarray(edit.convert("L"), dtype=np.int16)
            api_alpha = np.asarray(api.convert("RGBA").getchannel("A"), dtype=np.int16)
            checks["api_alpha_is_inverse_of_edit_strength"] = bool(
                np.max(np.abs((255 - edit_pixels) - api_alpha)) <= 2
            )
            checks["reviewed_surface_is_nonempty"] = bool(np.any(edit_pixels > 0))
            checks["reviewed_surface_is_not_full_frame"] = bool(np.any(edit_pixels == 0))

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        prompt_entry = manifest["prompts"].get("M13-paralama-doador-especular-v02")
        checks["prompt_registered_in_manifest"] = bool(prompt_entry)
        checks["prompt_hash_matches_manifest"] = bool(
            prompt_entry and prompt_entry["path"] == cfg["references"]["prompt"]
            and prompt_entry["sha256"] == sha(prompt_path)
        )
        checks["rig_hash_matches_manifest"] = manifest["rig_sha256"] == sha(rig_path)

    status = "ready_for_one_paid_m13_call" if all(checks.values()) else "blocked"
    report = {
        "status": status,
        "pipeline": str(pipeline_path.relative_to(ROOT)),
        "surface": cfg["surface"],
        "checks": checks,
        "missing": missing,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if status == "blocked":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
