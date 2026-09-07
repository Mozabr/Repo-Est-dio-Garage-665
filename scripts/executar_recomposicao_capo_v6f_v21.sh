#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h:h}"
cd "$PROJECT_DIR"
OUT="trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador"
DONOR="$OUT/doador-especular-bruto-api.png"

if [[ ! -f "$DONOR" ]]; then
  print -u2 "Doador bruto ausente. A v21 não autoriza uma nova chamada de API."
  exit 3
fi

.venv-mask/bin/python scripts/transferir_material_v6f.py \
  --config config/perfil-material-v6f-v21.json \
  --donor "$DONOR" \
  --output "$OUT/capo-material-v6f-v21-crop.png" \
  --light-map "$OUT/mapa-luz-especular-v6f-v21.png" \
  --aligned-donor "$OUT/doador-alinhado-v21-diagnostico.png" \
  --effective-mask "$OUT/mascara-efetiva-v6f-v21.png" \
  --report "$OUT/qa-material-v6f-v21.json" \
  --fail-on-qa

.venv-mask/bin/python scripts/reintegrar_crop_capo_v6e.py \
  --config config/pipeline-v6f.json \
  --crop-result "$OUT/capo-material-v6f-v21-crop.png" \
  --crop-mask "$OUT/mascara-efetiva-v6f-v21.png" \
  --output "$OUT/capo-material-v6f-v21-quadro-completo.png" \
  --report "$OUT/qa-reintegracao-v6f-v21.json"

print "$PROJECT_DIR/$OUT/capo-material-v6f-v21-quadro-completo.png"

