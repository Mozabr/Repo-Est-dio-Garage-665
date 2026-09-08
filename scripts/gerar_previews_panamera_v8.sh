#!/bin/zsh
set -euo pipefail

ROOT="${0:A:h:h}"
PYTHON="$ROOT/.venv-mask/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  echo "Ambiente do projeto nao encontrado em .venv-mask."
  echo "Consulte COMECE-AQUI.md antes de continuar."
  exit 1
fi

cd "$ROOT"
"$PYTHON" scripts/gerar_previews_serie_panamera_v8.py \
  --config config/previews-serie-panamera-v8.json

echo "Previews prontos em:"
echo "$ROOT/trabalhos/panamera/previews-serie-v8"
