#!/bin/zsh
set -euo pipefail
ROOT="${0:A:h:h}"
cd "$ROOT"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  print -u2 "OPENAI_API_KEY nao esta disponivel neste Terminal."
  exit 3
fi

PY_MASK="$ROOT/.venv-mask/bin/python"
PY_API="$ROOT/.venv/bin/python"
[[ -x "$PY_MASK" && -x "$PY_API" ]] || { print -u2 "Ambientes .venv e .venv-mask ausentes."; exit 2; }

OUT="trabalhos/panamera/serie-v9/perfil/doador-api-v01"
RAW="$OUT/geracao-bruta-api.png"
if [[ -f "$RAW" ]]; then
  print -u2 "Execucao bloqueada para impedir segunda cobranca: $RAW"
  exit 4
fi

[[ -f trabalhos/panamera/previews-serie-v8/externas/perfil/alpha-veiculo-preview.png ]] || ./scripts/gerar_previews_panamera_v8.sh >/dev/null
"$PY_MASK" scripts/preparar_mascara_api_perfil_v9.py >/dev/null
mkdir -p "$OUT"
"$PY_API" scripts/editar_com_gpt_image_2.py \
  --config config/pipeline-serie-v9-perfil.json \
  --imagem trabalhos/panamera/serie-v9/perfil/preparo-api/alvo-perfil-1600x1200.png \
  --mascara trabalhos/panamera/serie-v9/perfil/preparo-api/mascara-api-alpha.png \
  --prompt prompts/v9/perfil-doador-studio-h-v01.txt \
  --referencia entregas/panamera-v8-aprovada/dianteira-3-4/master-4096x3072.png \
  --referencia "referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.05 (2).jpeg" \
  --saida "$OUT/doador-contido-diagnostico.png" \
  --saida-bruta "$RAW" \
  --relatorio "$OUT/qa-api.json"

"$PY_MASK" scripts/transferir_assinatura_estudio_v9.py --config config/serie-v9-perfil-api.json
print "$ROOT/trabalhos/panamera/serie-v9/perfil/candidato-api-v01/candidato-perfil-v01.png"
