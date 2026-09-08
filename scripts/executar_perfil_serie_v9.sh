#!/bin/zsh
set -euo pipefail
ROOT="${0:A:h:h}"
cd "$ROOT"
PYTHON="$ROOT/.venv-mask/bin/python"
[[ -x "$PYTHON" ]] || { echo "Ambiente .venv-mask ausente."; exit 1; }

[[ -f trabalhos/panamera/previews-serie-v8/externas/perfil/alpha-veiculo-preview.png ]] || ./scripts/gerar_previews_panamera_v8.sh >/dev/null
"$PYTHON" scripts/transferir_assinatura_estudio_v9.py --config config/serie-v9-perfil.json
"$PYTHON" scripts/transferir_assinatura_estudio_v9.py --config config/serie-v9-perfil-v02.json
echo "$ROOT/trabalhos/panamera/serie-v9/perfil/candidato-v01/candidato-perfil-v01.png"
echo "$ROOT/trabalhos/panamera/serie-v9/perfil/candidato-v02-material/candidato-perfil-v01.png"
