#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h:h}"
cd "$PROJECT_DIR"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  print -u2 "OPENAI_API_KEY nao esta disponivel neste Terminal."
  exit 3
fi

OUT="trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador"
PREP="trabalhos/panamera/refinamento-dianteira-v6e/preparo"
RAW="$OUT/doador-especular-bruto-api.png"
mkdir -p "$OUT"

if [[ -f "$RAW" ]]; then
  print -u2 "Execucao bloqueada: o doador bruto ja existe e uma repeticao causaria nova cobranca."
  print -u2 "$PROJECT_DIR/$RAW"
  exit 4
fi

.venv-mask/bin/python scripts/validar_pacote_v6.py \
  --pipeline config/pipeline-v6f.json \
  --output "$OUT/qa-preflight.json"

.venv/bin/python scripts/editar_com_gpt_image_2.py \
  --config config/pipeline-v6f.json \
  --imagem "$PREP/alvo-crop-2048x1024.png" \
  --mascara "$PREP/mascara-api-alpha-2048x1024.png" \
  --prompt prompts/v6f/M11U-capo-doador-especular.txt \
  --referencia estudio-mestre/STUDIO_H-photo-bay-v06-oficial.png \
  --saida "$OUT/doador-contido-diagnostico.png" \
  --saida-bruta "$RAW" \
  --relatorio "$OUT/qa-api.json"

.venv-mask/bin/python scripts/transferir_material_v6f.py \
  --config config/perfil-material-v6f.json \
  --donor "$RAW" \
  --output "$OUT/capo-material-v6f-crop.png" \
  --light-map "$OUT/mapa-luz-especular-v6f.png" \
  --aligned-donor "$OUT/doador-alinhado-diagnostico.png" \
  --effective-mask "$OUT/mascara-efetiva-v6f.png" \
  --report "$OUT/qa-material-v6f.json" \
  --fail-on-qa

.venv-mask/bin/python scripts/reintegrar_crop_capo_v6e.py \
  --config config/pipeline-v6f.json \
  --crop-result "$OUT/capo-material-v6f-crop.png" \
  --crop-mask "$OUT/mascara-efetiva-v6f.png" \
  --output "$OUT/capo-material-v6f-quadro-completo.png" \
  --report "$OUT/qa-reintegracao-v6f.json"

print "$PROJECT_DIR/$OUT/capo-material-v6f-quadro-completo.png"
