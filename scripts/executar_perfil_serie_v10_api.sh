#!/bin/zsh
set -euo pipefail
ROOT="${0:A:h:h}"
cd "$ROOT"

[[ -n "${OPENAI_API_KEY:-}" ]] || { print -u2 "OPENAI_API_KEY nao esta disponivel neste Terminal."; exit 3; }
PY_MASK="$ROOT/.venv-mask/bin/python"
PY_API="$ROOT/.venv/bin/python"
[[ -x "$PY_MASK" && -x "$PY_API" ]] || { print -u2 "Ambientes .venv e .venv-mask ausentes."; exit 2; }

OUT="trabalhos/panamera/serie-v10/perfil-api/doador-v01"
RAW="$OUT/geracao-bruta-api.png"
if [[ -f "$RAW" ]]; then
  print -u2 "Execucao bloqueada para impedir segunda cobranca: $RAW"
  exit 4
fi

"$PY_MASK" scripts/preparar_perfil_serie_v10_api.py >/dev/null
mkdir -p "$OUT"
"$PY_API" scripts/editar_com_gpt_image_2.py \
  --config config/pipeline-serie-v10-perfil.json \
  --imagem trabalhos/panamera/serie-v10/perfil-api/preparo/alvo-perfil-1600x1200.png \
  --mascara trabalhos/panamera/serie-v10/perfil-api/preparo/mascara-api-alpha.png \
  --prompt prompts/v10/perfil-doador-studio-canonico-v01.txt \
  --referencia referencias/autoridades/panamera-master-estudio-canonico-v01.png \
  --referencia trabalhos/panamera/serie-v9/perfil/doador-api-v01/geracao-bruta-api.png \
  --referencia "referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.05 (2).jpeg" \
  --saida "$OUT/doador-contido.png" \
  --saida-bruta "$RAW" \
  --relatorio "$OUT/qa-api.json"

print "$ROOT/$OUT/doador-contido.png"
