#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h:h}"
cd "$PROJECT_DIR"
OUT="trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M14M15-portas-continuas-v01"
mkdir -p "$OUT"

.venv-mask/bin/python scripts/construir_mascara_portas_continua_v6f.py
.venv-mask/bin/python scripts/aplicar_rig_lateral_v6f.py \
  --config config/rig-material-lateral-v6f.json \
  --surface M14M15-portas-continuas \
  --output "$OUT/candidato-crop.png" \
  --light-map "$OUT/mapa-luz.png" \
  --effective-mask "$OUT/mascara-efetiva.png" \
  --report "$OUT/qa-material.json" \
  --fail-on-qa

.venv-mask/bin/python scripts/reintegrar_crop_lateral_v6f.py \
  --config config/rig-material-lateral-v6f.json \
  --surface M14M15-portas-continuas \
  --crop-result "$OUT/candidato-crop.png" \
  --crop-mask "$OUT/mascara-efetiva.png" \
  --output "$OUT/candidato-quadro-completo.png" \
  --report "$OUT/qa-reintegracao.json"

print "$PROJECT_DIR/$OUT/candidato-quadro-completo.png"
