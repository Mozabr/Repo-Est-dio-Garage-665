#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h:h}"
cd "$PROJECT_DIR"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  print -u2 "OPENAI_API_KEY nao esta disponivel neste Terminal. Execute primeiro: export OPENAI_API_KEY=..."
  exit 3
fi

OUT="trabalhos/panamera/refinamento-dianteira-v6c/teste-capo-integral-studio-h"
TARGET="trabalhos/panamera/refinamento-dianteira-v6c/alvo-estudio-h/dianteira-3-4/alvo-edicao-2048x1536.png"
MASK="trabalhos/panamera/refinamento-dianteira-v6c/guias-palco/M11U-capo-integral-editar.png"
API_MASK="trabalhos/panamera/refinamento-dianteira-v6c/guias-palco/M11U-capo-integral-api-alpha.png"
mkdir -p "$OUT"

.venv-mask/bin/python scripts/validar_pacote_v6.py \
  --pipeline config/pipeline-v6c.json \
  --output "$OUT/qa-preflight.json"

.venv/bin/python scripts/editar_com_gpt_image_2.py \
  --config config/pipeline-v6c.json \
  --imagem "$TARGET" \
  --mascara "$API_MASK" \
  --prompt prompts/v6c/M11U-capo-integral.txt \
  --referencia estudio-mestre/STUDIO_H-photo-bay-v06-oficial.png \
  --referencia referencias/panamera-cor-estudio/a02d9525b5574f798ca809e501c1594c_1712087709889.jpg \
  --referencia trabalhos/panamera/refinamento-dianteira-v6c/guias-palco/normal-aproximada-palco.png \
  --saida "$OUT/candidato-contido-direto.png" \
  --saida-bruta "$OUT/geracao-bruta-api.png" \
  --relatorio "$OUT/qa-api.json"

# The raw response must remain registered to the already composed Studio H target.
# A good-looking but displaced or redrawn car is rejected before any blending.
.venv-mask/bin/python scripts/conter_edicao_local.py \
  --original "$TARGET" \
  --generated "$OUT/geracao-bruta-api.png" \
  --mask "$MASK" \
  --output "$OUT/candidato-alinhado-contido.png" \
  --report "$OUT/qa-registro.json"

.venv-mask/bin/python scripts/recompor_superficie_v6.py \
  --original "$TARGET" \
  --candidate "$OUT/candidato-alinhado-contido.png" \
  --mask "$MASK" \
  --light-strength 0.62 \
  --micro-strength 0.90 \
  --max-light-delta 14 \
  --output "$OUT/capo-integral-recomposto-v6c.png" \
  --report "$OUT/qa-recomposicao.json"

print "$PROJECT_DIR/$OUT/capo-integral-recomposto-v6c.png"
