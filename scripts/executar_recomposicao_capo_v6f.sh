#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h:h}"
cd "$PROJECT_DIR"
OUT="trabalhos/panamera/refinamento-dianteira-v6f/capo-material"
mkdir -p "$OUT"

.venv-mask/bin/python scripts/transferir_material_v6f.py \
  --config config/perfil-material-v6f.json \
  --output "$OUT/capo-material-v6f-v02-crop.png" \
  --light-map "$OUT/mapa-luz-especular-v6f-v02.png" \
  --aligned-donor "$OUT/doador-alinhado-diagnostico-v02.png" \
  --effective-mask "$OUT/mascara-efetiva-v6f-v02.png" \
  --report "$OUT/qa-material-v6f-v02.json"

.venv-mask/bin/python scripts/reintegrar_crop_capo_v6e.py \
  --config config/pipeline-v6e.json \
  --crop-result "$OUT/capo-material-v6f-v02-crop.png" \
  --crop-mask "$OUT/mascara-efetiva-v6f-v02.png" \
  --output "$OUT/capo-material-v6f-v02-quadro-completo.png" \
  --report "$OUT/qa-reintegracao-v6f-v02.json"

print "$PROJECT_DIR/$OUT/capo-material-v6f-v02-quadro-completo.png"
