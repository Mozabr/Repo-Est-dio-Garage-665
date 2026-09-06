#!/bin/bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

if ! command -v python3.11 >/dev/null 2>&1; then
  echo "Python 3.11 não foi encontrado. Instale-o e execute este script novamente."
  exit 1
fi

python3.11 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-core.txt

python3.11 -m venv .venv-mask
.venv-mask/bin/python -m pip install --upgrade pip
.venv-mask/bin/python -m pip install -r requirements-mask.txt
.venv-mask/bin/python -m pip install -r requirements-studio.txt

.venv-mask/bin/python scripts/baixar_modelos_studio.py --weights
.venv-mask/bin/python scripts/baixar_depth_anything_v2.py
.venv-mask/bin/python scripts/baixar_sam2.py

echo "Ambiente reconstruído. Leia HANDOFF.md antes de executar qualquer geração paga."

