#!/bin/zsh
set -euo pipefail

ROOT="${0:A:h:h}"
cd "$ROOT"

VISTA="${1:-}"
case "$VISTA" in
  interior-amplo|painel-instrumentos|interior-motorista) ;;
  *)
    print -u2 "Uso: ./scripts/executar_interior_serie_v11_api.sh painel-instrumentos|interior-amplo|interior-motorista"
    exit 2
    ;;
esac

[[ -n "${OPENAI_API_KEY:-}" ]] || { print -u2 "OPENAI_API_KEY não está disponível neste Terminal."; exit 3; }
PY_MASK="$ROOT/.venv-mask/bin/python"
PY_API="$ROOT/.venv/bin/python"
[[ -x "$PY_MASK" && -x "$PY_API" ]] || { print -u2 "Ambientes .venv e .venv-mask ausentes."; exit 2; }

"$PY_MASK" scripts/preparar_interiores_serie_v10_api.py >/dev/null
PREP="trabalhos/panamera/serie-v10/interiores-api/preparo/$VISTA"
OUT="trabalhos/panamera/serie-v11/interiores/$VISTA/api-v01"
RAW="$OUT/geracao-bruta-api.png"
if [[ -f "$RAW" ]]; then
  print -u2 "Execução bloqueada para impedir segunda cobrança: $RAW"
  exit 4
fi

mkdir -p "$OUT"
"$PY_API" scripts/editar_com_gpt_image_2.py \
  --config config/pipeline-serie-v11.json \
  --imagem "$PREP/alvo-1600x1200.png" \
  --mascara "$PREP/mascara-api-alpha.png" \
  --prompt prompts/v11/interior-master-teste-05-lock-v01.txt \
  --referencia referencias/autoridades/panamera-master-estudio-canonico-v01.png \
  --saida "$OUT/candidato-contido.png" \
  --saida-bruta "$RAW" \
  --relatorio "$OUT/qa-api.json"

print "$ROOT/$OUT/candidato-contido.png"
