"""Download pinned official model snapshots; never execute downloaded code here."""
from pathlib import Path
import argparse
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("HF_HOME", str(ROOT / "modelos" / "hf-cache"))
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
from huggingface_hub import HfApi, snapshot_download

MODELS = {
    "birefnet": "ZhengPeng7/BiRefNet",
    "vitmatte": "hustvl/vitmatte-small-composition-1k",
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", action="store_true")
    args = parser.parse_args()
    path = ROOT / "integracoes" / "modelos-lock.json"
    lock = json.loads(path.read_text()) if path.exists() else {}
    for name, repo in MODELS.items():
        if name not in lock:
            info = HfApi().model_info(repo)
            lock[name] = {"repo": repo, "revision": info.sha,
                          "license_model_card": getattr(info.card_data, "license", None)}
            path.write_text(json.dumps(lock, indent=2) + "\n")
        entry = lock[name]
        folder = ROOT / "modelos" / name
        patterns = ["*.json", "*.py", "README.md", "LICENSE*"]
        if args.weights:
            patterns += ["*.safetensors"]
        print(f"Downloading {repo}@{entry['revision']} (weights={args.weights})", flush=True)
        snapshot_download(repo, revision=entry["revision"], local_dir=folder,
                          allow_patterns=patterns, max_workers=2)
        entry["files_sha256"] = {
            str(p.relative_to(folder)): hashlib.file_digest(p.open("rb"), "sha256").hexdigest()
            for p in folder.rglob("*") if p.is_file() and ".cache" not in p.parts
        }
        entry["weights_downloaded"] = bool(list(folder.glob("*.safetensors")))
        path.write_text(json.dumps(lock, indent=2) + "\n")
    print(path, flush=True)

if __name__ == "__main__":
    main()
