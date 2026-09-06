#!/bin/bash
# Local inference and deterministic export; this command makes no paid API call.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"
PYTHON="$PROJECT_DIR/.venv-mask/bin/python"
if [ ! -x "$PYTHON" ]; then
  echo "Ambiente .venv-mask ausente. Consulte 17-estudio-v2.md."
  exit 1
fi
"$PYTHON" -u scripts/matting_studio.py
"$PYTHON" -u scripts/montar_studio_v2.py
"$PYTHON" -u scripts/verificar_studio_v2.py
echo "Concluido: trabalhos/panamera/studio-v2/serie-comparativa.jpg"
