#!/usr/bin/env python3
"""Download a pinned Depth Anything V2 Small snapshot and record its provenance."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("HF_HOME", str(ROOT / "modelos/hf-cache"))
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

from huggingface_hub import HfApi, snapshot_download

REPO = "depth-anything/Depth-Anything-V2-Small-hf"
OUT = ROOT / "modelos/depth-anything-v2-small"
LOCK = ROOT / "integracoes/modelos-lock-v6.json"


def main() -> None:
    lock = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    pinned = lock.get("depth_anything_v2_small", {}).get("revision")
    info = HfApi().model_info(REPO, revision=pinned) if pinned else HfApi().model_info(REPO)
    revision = pinned or info.sha
    snapshot_download(
        REPO,
        revision=revision,
        local_dir=OUT,
        allow_patterns=["*.json", "*.safetensors", "README.md", "LICENSE*"],
        max_workers=2,
    )
    files = {
        str(path.relative_to(OUT)): hashlib.file_digest(path.open("rb"), "sha256").hexdigest()
        for path in OUT.rglob("*") if path.is_file() and ".cache" not in path.parts
    }
    lock["depth_anything_v2_small"] = {
        "upstream_repository": "https://github.com/DepthAnything/Depth-Anything-V2",
        "weights_repository": REPO,
        "revision": revision,
        "license_model_card": getattr(info.card_data, "license", None),
        "files_sha256": files
    }
    LOCK.write_text(json.dumps(lock, indent=2) + "\n")
    print(json.dumps(lock["depth_anything_v2_small"], indent=2))


if __name__ == "__main__":
    main()
