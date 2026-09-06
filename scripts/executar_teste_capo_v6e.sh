#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h:h}"
cd "$PROJECT_DIR"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  print -u2 "OPENAI_API_KEY nao esta disponivel neste Terminal."
  exit 3
fi

OUT="trabalhos/panamera/refinamento-dianteira-v6e/teste-capo-crop"
PREP="trabalhos/panamera/refinamento-dianteira-v6e/preparo"
mkdir -p "$OUT"

.venv-mask/bin/python scripts/validar_pacote_v6.py \
  --pipeline config/pipeline-v6e.json \
  --output "$OUT/qa-preflight.json"

.venv/bin/python scripts/editar_com_gpt_image_2.py \
  --config config/pipeline-v6e.json \
  --imagem "$PREP/alvo-crop-2048x1024.png" \
  --mascara "$PREP/mascara-api-alpha-2048x1024.png" \
  --prompt prompts/v6e/M11U-capo-crop-fotometrico.txt \
  --referencia estudio-mestre/STUDIO_H-photo-bay-v06-oficial.png \
  --saida "$OUT/crop-contido-direto.png" \
  --saida-bruta "$OUT/diagnostico-resposta-integral-nao-usar.png" \
  --relatorio "$OUT/qa-api.json"

.venv-mask/bin/python scripts/conter_edicao_local.py \
  --original "$PREP/alvo-crop-2048x1024.png" \
  --generated "$OUT/diagnostico-resposta-integral-nao-usar.png" \
  --mask "$PREP/mascara-editar-2048x1024.png" \
  --output "$OUT/crop-alinhado-contido.png" \
  --report "$OUT/qa-registro.json" \
  --minimum-inlier-fraction 0.70 \
  --maximum-displacement-px 8

.venv-mask/bin/python scripts/recompor_superficie_v6.py \
  --original "$PREP/alvo-crop-2048x1024.png" \
  --candidate "$OUT/crop-alinhado-contido.png" \
  --mask "$PREP/mascara-editar-2048x1024.png" \
  --light-strength 0.50 \
  --micro-strength 0.97 \
  --max-light-delta 10 \
  --output "$OUT/crop-recomposto.png" \
  --report "$OUT/qa-recomposicao.json"

.venv-mask/bin/python scripts/reintegrar_crop_capo_v6e.py \
  --config config/pipeline-v6e.json \
  --crop-result "$OUT/crop-recomposto.png" \
  --output "$OUT/capo-v6e-quadro-completo.png" \
  --report "$OUT/qa-reintegracao.json"

print "$PROJECT_DIR/$OUT/capo-v6e-quadro-completo.png"
