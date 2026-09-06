#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h:h}"
cd "$PROJECT_DIR"

OUT="trabalhos/panamera/refinamento-dianteira-v6d/capo-deterministico"
mkdir -p "$OUT"

PYTHONPYCACHEPREFIX=/private/tmp/garage665-pycache .venv-mask/bin/python \
  scripts/relight_capo_deterministico_v6d.py \
  --config config/relighting-capo-v6d.json \
  --output "$OUT/capo-relight-v6d.png" \
  --report "$OUT/qa-relight-v6d.json"

print "$PROJECT_DIR/$OUT/capo-relight-v6d.png"
