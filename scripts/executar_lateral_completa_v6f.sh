#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h:h}"
cd "$PROJECT_DIR"
ROOT_OUT="trabalhos/panamera/refinamento-dianteira-v6f/lateral-material"

for SURFACE in M14-portas-superiores M15-portas-inferiores; do
  OUT="$ROOT_OUT/${SURFACE}-v01"
  mkdir -p "$OUT"
  .venv-mask/bin/python scripts/aplicar_rig_lateral_v6f.py \
    --config config/rig-material-lateral-v6f.json \
    --surface "$SURFACE" \
    --output "$OUT/candidato-crop.png" \
    --light-map "$OUT/mapa-luz.png" \
    --effective-mask "$OUT/mascara-efetiva.png" \
    --report "$OUT/qa-material.json" \
    --fail-on-qa
done

FINAL="$ROOT_OUT/lateral-completa-v01"
mkdir -p "$FINAL"
.venv-mask/bin/python scripts/mesclar_lateral_v6f.py \
  --config config/rig-material-lateral-v6f.json \
  --surface "M14-portas-superiores=$ROOT_OUT/M14-portas-superiores-v01/candidato-crop.png=$ROOT_OUT/M14-portas-superiores-v01/mascara-efetiva.png" \
  --surface "M15-portas-inferiores=$ROOT_OUT/M15-portas-inferiores-v01/candidato-crop.png=$ROOT_OUT/M15-portas-inferiores-v01/mascara-efetiva.png" \
  --output "$FINAL/candidato-quadro-completo.png" \
  --report "$FINAL/qa-mesclagem.json"

print "$PROJECT_DIR/$FINAL/candidato-quadro-completo.png"
