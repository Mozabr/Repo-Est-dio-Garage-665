#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

# Superseded after the failed generative pilot. The familiar command now runs
# the local, fidelity-preserving pipeline; archive API flow is opt-in only.
if [[ "${GARAGE665_EXECUTAR_FLUXO_LEGADO:-0}" != "1" ]]; then
  exec bash "$PROJECT_DIR/scripts/executar_studio_v2.sh"
fi

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "A chave OPENAI_API_KEY nao esta disponivel neste Terminal."
  echo "Exporte a chave e rode este arquivo novamente."
  exit 1
fi

API_OUTPUT="trabalhos/panamera/frontal/reflexos-gpt-image-2-v01.png"
if [[ -e "$API_OUTPUT" ]]; then
  echo "A saida da API ja existe: $API_OUTPUT"
  echo "O processo foi interrompido para impedir uma cobranca duplicada."
  exit 2
fi

echo "Enviando a edicao ao GPT Image 2. A resposta pode levar alguns minutos..."
.venv/bin/python scripts/editar_com_gpt_image_2.py \
  --imagem trabalhos/panamera/frontal/composicao-estudio-SAM2-v02.png \
  --mascara trabalhos/panamera/frontal/M03-M04-reflexos-localizados-FINAL.png \
  --prompt prompts/02-reflexos-localizados.txt \
  --saida "$API_OUTPUT" \
  --saida-bruta trabalhos/panamera/frontal/reflexos-gpt-image-2-v01-BRUTO.png
echo "Resposta recebida. Aplicando trava de pixels, marca e formatos..."

.venv/bin/python scripts/aplicar_tampa_placa.py \
  --imagem "$API_OUTPUT" \
  --saida trabalhos/panamera/frontal/panamera-frontal-aprovacao-v01.png \
  --ponto 1435,1650 --ponto 1872,1650 --ponto 1872,1820 --ponto 1435,1820

.venv/bin/python scripts/criar_master_4k.py \
  --imagem trabalhos/panamera/frontal/panamera-frontal-aprovacao-v01.png \
  --saida trabalhos/panamera/frontal/panamera-frontal-master-4096x3072-sem-logo-v01.png

.venv/bin/python scripts/aplicar_logo_parede.py \
  --imagem trabalhos/panamera/frontal/panamera-frontal-master-4096x3072-sem-logo-v01.png \
  --saida entregas/panamera-frontal-SAM2/panamera-frontal-master-4096x3072-v01.png

.venv/bin/python scripts/exportar_formatos.py \
  entregas/panamera-frontal-SAM2/panamera-frontal-master-4096x3072-v01.png \
  --saida entregas/panamera-frontal-SAM2

echo "Piloto finalizado em entregas/panamera-frontal-SAM2"
