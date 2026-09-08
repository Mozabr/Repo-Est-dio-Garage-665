#!/bin/zsh
set -euo pipefail

ROOT="${0:A:h:h}"
cd "$ROOT"

VISTA="${1:-}"
case "$VISTA" in
  perfil) SOURCE="referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.05 (2).jpeg" ;;
  frontal) SOURCE="referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.05 (1).jpg" ;;
  dianteira-3-4-oposta) SOURCE="referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.05.jpg" ;;
  traseira-3-4) SOURCE="referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.06 (2).jpg" ;;
  traseira-3-4-oposta) SOURCE="referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.06.jpg" ;;
  perfil-oposto) SOURCE="referencias/originais-panamera/WhatsApp Image 2025-11-24 at 09.57.07.jpg" ;;
  *)
    print -u2 "Uso: ./scripts/executar_externa_serie_v11_api.sh perfil|frontal|dianteira-3-4-oposta|traseira-3-4|traseira-3-4-oposta|perfil-oposto"
    exit 2
    ;;
esac

[[ -n "${OPENAI_API_KEY:-}" ]] || { print -u2 "OPENAI_API_KEY não está disponível neste Terminal."; exit 3; }
PY_MASK="$ROOT/.venv-mask/bin/python"
PY_API="$ROOT/.venv/bin/python"
[[ -x "$PY_MASK" && -x "$PY_API" ]] || { print -u2 "Ambientes .venv e .venv-mask ausentes."; exit 2; }

OUT="trabalhos/panamera/serie-v11/$VISTA/api-v01"
RAW="$OUT/geracao-bruta-api.png"
if [[ -f "$RAW" ]]; then
  print -u2 "Execução bloqueada para impedir segunda cobrança: $RAW"
  exit 4
fi

"$PY_MASK" scripts/preparar_externa_serie_v11_api.py "$VISTA" >/dev/null
mkdir -p "$OUT"
"$PY_API" scripts/editar_com_gpt_image_2.py \
  --config config/pipeline-serie-v11.json \
  --imagem "trabalhos/panamera/serie-v11/$VISTA/preparo/alvo-1600x1200.png" \
  --mascara "trabalhos/panamera/serie-v11/$VISTA/preparo/mascara-api-alpha.png" \
  --prompt prompts/v11/externa-master-teste-05-lock-v01.txt \
  --referencia referencias/autoridades/panamera-master-estudio-canonico-v01.png \
  --referencia "$SOURCE" \
  --saida "$OUT/candidato-contido.png" \
  --saida-bruta "$RAW" \
  --relatorio "$OUT/qa-api.json"

"$PY_MASK" scripts/validar_externa_serie_v11.py "$VISTA" >/dev/null
print "$ROOT/$OUT/comparacao-master-alvo-candidata.jpg"
