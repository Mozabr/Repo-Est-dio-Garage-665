#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h:h}"
cd "$PROJECT_DIR"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  print -u2 "OPENAI_API_KEY nao esta disponivel neste Terminal. Execute primeiro: export OPENAI_API_KEY=..."
  exit 3
fi

OUT="trabalhos/panamera/refinamento-dianteira-v6b/teste-M11-capo-centro-studio-h"
mkdir -p "$OUT"

.venv-mask/bin/python scripts/validar_pacote_v6.py \
  --pipeline config/pipeline-v6b.json \
  --output "$OUT/qa-preflight.json"

.venv/bin/python scripts/editar_com_gpt_image_2.py \
  --config config/pipeline-v6b.json \
  --imagem trabalhos/panamera/refinamento-dianteira-v6/entrada/source-2048x1536.png \
  --mascara trabalhos/panamera/refinamento-dianteira-v6/mascaras/M11-capo-centro-api-alpha.png \
  --prompt prompts/v6b/M11-capo-centro.txt \
  --referencia estudio-mestre/STUDIO_H-photo-bay-v06-oficial.png \
  --referencia referencias/panamera-cor-estudio/a02d9525b5574f798ca809e501c1594c_1712087709889.jpg \
  --referencia trabalhos/panamera/refinamento-dianteira-v6/guias/normal-aproximada.png \
  --saida "$OUT/candidato-contido-api.png" \
  --saida-bruta "$OUT/geracao-bruta-api.png" \
  --relatorio "$OUT/qa-api.json"

.venv-mask/bin/python scripts/recompor_superficie_v6.py \
  --original trabalhos/panamera/refinamento-dianteira-v6/entrada/source-2048x1536.png \
  --candidate "$OUT/candidato-contido-api.png" \
  --mask trabalhos/panamera/refinamento-dianteira-v6/mascaras/M11-capo-centro-editar.png \
  --output "$OUT/candidato-recomposto-v6b.png" \
  --report "$OUT/qa-recomposicao.json"

print "$PROJECT_DIR/$OUT/candidato-recomposto-v6b.png"
