#!/bin/zsh
set -euo pipefail

ROOT="${0:A:h:h}"
cd "$ROOT"
OUT="trabalhos/panamera/refinamento-dianteira-v7/previa-lateral-conjunta-v01"
PYTHON="$ROOT/.venv-mask/bin/python"
CONFIG="config/rig-material-lateral-v7.json"
mkdir -p "$OUT"

"$PYTHON" scripts/construir_mascara_portas_continua_v6f.py
"$PYTHON" scripts/aplicar_rig_lateral_v6f.py \
  --config "$CONFIG" \
  --surface M13M14M15-lateral-continua \
  --output "$OUT/candidato-crop.png" \
  --light-map "$OUT/mapa-luz.png" \
  --effective-mask "$OUT/mascara-efetiva.png" \
  --report "$OUT/qa-material.json" \
  --fail-on-qa
"$PYTHON" scripts/reintegrar_crop_lateral_v6f.py \
  --config "$CONFIG" \
  --crop-result "$OUT/candidato-crop.png" \
  --crop-mask "$OUT/mascara-efetiva.png" \
  --surface M13M14M15-lateral-continua \
  --output "$OUT/candidato-quadro-completo.png" \
  --report "$OUT/qa-reintegracao.json"

echo "$OUT/candidato-quadro-completo.png"
