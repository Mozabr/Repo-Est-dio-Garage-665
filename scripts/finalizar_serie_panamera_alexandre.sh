#!/bin/zsh
set -euo pipefail

ROOT="${0:A:h:h}"
cd "$ROOT"

PYTHON="$ROOT/.venv-mask/bin/python"
OUT="$ROOT/entregas/panamera-serie-final-alexandre"

if [[ ! -x "$PYTHON" ]]; then
  print -u2 "Ambiente .venv-mask ausente. Execute scripts/configurar_novo_computador.sh."
  exit 1
fi

typeset -A SOURCES
SOURCES=(
  dianteira-3-4 "trabalhos/panamera/previews-validacao-v12/externas/dianteira-3-4-master-aprovada.png"
  frontal "trabalhos/panamera/previews-validacao-v12/externas/frontal-aprovada-anexo.png"
  perfil "trabalhos/panamera/previews-validacao-v12/externas/perfil-candidata-v01.png"
  dianteira-3-4-oposta "trabalhos/panamera/previews-validacao-v12/externas/dianteira-3-4-oposta-candidata-v01.png"
  perfil-oposto "trabalhos/panamera/previews-validacao-v12/externas/perfil-oposto-candidata-v01.png"
  traseira-3-4 "trabalhos/panamera/previews-validacao-v12/externas/traseira-3-4-candidata-v01.png"
  traseira-3-4-oposta "trabalhos/panamera/previews-validacao-v12/externas/traseira-3-4-oposta-candidata-v01.png"
  interior-amplo "trabalhos/panamera/previews-validacao-v12/interiores/interior-amplo-candidata-v01.png"
  painel-instrumentos "trabalhos/panamera/previews-validacao-v12/interiores/painel-instrumentos-candidata-v01.png"
  interior-motorista "trabalhos/panamera/previews-validacao-v12/interiores/interior-motorista-candidata-v02-studio-soft.png"
)

ORDER=(
  dianteira-3-4
  frontal
  perfil
  dianteira-3-4-oposta
  perfil-oposto
  traseira-3-4
  traseira-3-4-oposta
  interior-amplo
  painel-instrumentos
  interior-motorista
)

mkdir -p "$OUT"

for view in $ORDER; do
  source_file="${SOURCES[$view]}"
  view_out="$OUT/$view"
  if [[ ! -f "$source_file" ]]; then
    print -u2 "Fonte ausente para $view: $source_file"
    exit 1
  fi
  mkdir -p "$view_out/formatos"
  cp "$source_file" "$view_out/preview-aprovada.png"
  "$PYTHON" scripts/criar_master_4k.py \
    --imagem "$source_file" \
    --saida "$view_out/master-4096x3072.png"
  "$PYTHON" scripts/exportar_formatos.py \
    "$view_out/master-4096x3072.png" \
    --saida "$view_out/formatos"
done

(
  cd "$OUT"
  find . -type f \( -name '*.png' -o -name '*.jpg' \) -print0 \
    | sort -z \
    | xargs -0 shasum -a 256 > MANIFESTO-SHA256.txt
)

print "$OUT"

