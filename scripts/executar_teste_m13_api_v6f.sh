#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h:h}"
cd "$PROJECT_DIR"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  print -u2 "OPENAI_API_KEY nao esta disponivel neste Terminal."
  exit 3
fi

OUT="trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M13-paralama-proximo-api-v02"
PREP="trabalhos/panamera/refinamento-dianteira-v6f/preparo-lateral"
RAW="$OUT/doador-bruto-api-rejeitado-como-imagem.png"
CONTAINED="$OUT/doador-contido-diagnostico.png"
mkdir -p "$OUT"

if [[ -f "$RAW" ]]; then
  print -u2 "Execucao bloqueada: o doador bruto M13 ja existe e uma repeticao causaria nova cobranca."
  print -u2 "$PROJECT_DIR/$RAW"
  exit 4
fi

.venv-mask/bin/python scripts/validar_pacote_lateral_v6f.py \
  --pipeline config/pipeline-v6f-lateral-m13.json \
  --output "$OUT/qa-preflight.json"

.venv/bin/python scripts/editar_com_gpt_image_2.py \
  --config config/pipeline-v6f-lateral-m13.json \
  --imagem "$PREP/alvo-lateral-1536x1024.png" \
  --mascara "$PREP/M13-paralama-proximo-api-alpha.png" \
  --prompt prompts/v6f/M13-paralama-doador-especular-v02.txt \
  --referencia estudio-mestre/STUDIO_H-photo-bay-v06-oficial.png \
  --saida "$CONTAINED" \
  --saida-bruta "$RAW" \
  --relatorio "$OUT/qa-api.json"

.venv-mask/bin/python scripts/aplicar_rig_lateral_v6f.py \
  --config config/rig-material-lateral-v6f-api-m13.json \
  --surface M13-paralama-proximo \
  --output "$OUT/candidato-crop.png" \
  --light-map "$OUT/mapa-luz.png" \
  --effective-mask "$OUT/mascara-efetiva.png" \
  --report "$OUT/qa-material.json" \
  --fail-on-qa

.venv-mask/bin/python scripts/reintegrar_crop_lateral_v6f.py \
  --config config/rig-material-lateral-v6f-api-m13.json \
  --surface M13-paralama-proximo \
  --crop-result "$OUT/candidato-crop.png" \
  --crop-mask "$OUT/mascara-efetiva.png" \
  --output "$OUT/candidato-quadro-completo.png" \
  --report "$OUT/qa-reintegracao.json"

print "$PROJECT_DIR/$OUT/candidato-quadro-completo.png"
