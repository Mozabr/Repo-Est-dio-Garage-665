#!/bin/zsh
set -euo pipefail

ROOT="${0:A:h:h}"
cd "$ROOT"
PYTHON="$ROOT/.venv-mask/bin/python"
OUT="trabalhos/panamera/refinamento-dianteira-v8/harmonizacao-integral-v03"
mkdir -p "$OUT"

"$PYTHON" scripts/transferir_iluminacao_integral_v8.py \
  --output "$OUT/candidato-quadro-completo.png" \
  --aligned-donor "$OUT/doador-alinhado-diagnostico.png" \
  --effective-mask "$OUT/mascara-efetiva.png" \
  --report "$OUT/qa-harmonizacao.json" \
  --fail-on-qa

echo "$OUT/candidato-quadro-completo.png"
