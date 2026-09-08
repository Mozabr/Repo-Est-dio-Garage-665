#!/bin/zsh
set -euo pipefail
ROOT="${0:A:h:h}"
cd "$ROOT"

[[ -n "${OPENAI_API_KEY:-}" ]] || { print -u2 "OPENAI_API_KEY nao esta disponivel neste Terminal."; exit 3; }
PY_MASK="$ROOT/.venv-mask/bin/python"
PY_API="$ROOT/.venv/bin/python"
[[ -x "$PY_MASK" && -x "$PY_API" ]] || { print -u2 "Ambientes .venv e .venv-mask ausentes."; exit 2; }

"$PY_MASK" scripts/preparar_interiores_serie_v10_api.py >/dev/null
PROMPT="prompts/v10/interiores-studio-canonico-v01.txt"
REFERENCE="referencias/autoridades/panamera-master-estudio-canonico-v01.png"

run_one() {
  local id="$1"
  local prep="trabalhos/panamera/serie-v10/interiores-api/preparo/$id"
  local out="trabalhos/panamera/serie-v10/interiores-api/$id/v01"
  local raw="$out/geracao-bruta-api.png"
  if [[ -f "$raw" ]]; then
    print "Ignorado para impedir segunda cobranca: $id"
    return
  fi
  mkdir -p "$out"
  "$PY_API" scripts/editar_com_gpt_image_2.py \
    --config config/pipeline-serie-v10-interiores.json \
    --imagem "$prep/alvo-1600x1200.png" \
    --mascara "$prep/mascara-api-alpha.png" \
    --prompt "$PROMPT" \
    --referencia "$REFERENCE" \
    --saida "$out/resultado-contido.png" \
    --saida-bruta "$raw" \
    --relatorio "$out/qa-api.json"
}

# Cada item ausente corresponde a uma chamada paga. Resultados existentes são
# sempre ignorados, permitindo retomar o lote sem cobrança duplicada.
run_one interior-amplo
run_one painel-instrumentos
run_one interior-motorista
print "$ROOT/trabalhos/panamera/serie-v10/interiores-api"
