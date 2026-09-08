#!/bin/zsh
set -euo pipefail
ROOT="${0:A:h:h}"
cd "$ROOT"
PYTHON="$ROOT/.venv-mask/bin/python"
[[ -x "$PYTHON" ]] || { echo "Ambiente .venv-mask ausente."; exit 1; }
"$PYTHON" scripts/gerar_previews_serie_panamera_v8.py --config config/previews-serie-panamera-v10.json
"$PYTHON" scripts/compor_interiores_studio_v10.py
echo "$ROOT/trabalhos/panamera/previews-serie-v10-studio-canonico"
