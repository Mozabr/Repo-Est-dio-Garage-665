#!/usr/bin/env python3
"""Baixa o checkpoint oficial SAM 2.1 Small e valida seu SHA-256."""
from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "modelos/sam2/sam2.1_hiera_small.pt"
URL = "https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_small.pt"
EXPECTED_SHA256 = "6d1aa6f30de5c92224f8172114de081d104bbd23dd9dc5c58996f0cad5dc4d38"


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists() and sha256(OUT) == EXPECTED_SHA256:
        print(f"Checkpoint já validado: {OUT}")
        return
    temporary = OUT.with_suffix(".pt.part")
    urllib.request.urlretrieve(URL, temporary)
    actual = sha256(temporary)
    if actual != EXPECTED_SHA256:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"SHA-256 inesperado: {actual}")
    temporary.replace(OUT)
    print(f"Checkpoint instalado e validado: {OUT}")


if __name__ == "__main__":
    main()

