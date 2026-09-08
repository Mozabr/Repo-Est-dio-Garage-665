#!/bin/zsh
set -euo pipefail

ROOT="${0:A:h:h}"
cd "$ROOT"
PYTHON="$ROOT/.venv-mask/bin/python"
SOURCE="trabalhos/panamera/refinamento-dianteira-v8/harmonizacao-integral-v07-clearcoat-final/candidato-quadro-completo.png"
OUT="entregas/panamera-v8-aprovada/dianteira-3-4"

if [[ ! -x "$PYTHON" ]]; then
  print -u2 "Ambiente .venv-mask ausente. Execute scripts/configurar_novo_computador.sh."
  exit 1
fi
if [[ ! -f "$SOURCE" ]]; then
  print -u2 "Fonte v07 aprovada ausente: $SOURCE"
  exit 1
fi

mkdir -p "$OUT/formatos"
"$PYTHON" scripts/criar_master_4k.py \
  --imagem "$SOURCE" \
  --saida "$OUT/master-4096x3072.png"
"$PYTHON" scripts/exportar_formatos.py \
  "$OUT/master-4096x3072.png" \
  --saida "$OUT/formatos"

"$PYTHON" - "$SOURCE" "$OUT" <<'PY'
from pathlib import Path
from PIL import Image
import hashlib
import json
import sys

source = Path(sys.argv[1])
out = Path(sys.argv[2])
files = {
    "master": out / "master-4096x3072.png",
    "feed": out / "formatos/feed-4096x3072.jpg",
    "story_horizontal": out / "formatos/story-horizontal-3840x2160.jpg",
    "webmotors": out / "formatos/webmotors-1920x1440.jpg",
}
expected = {
    "master": (4096, 3072),
    "feed": (4096, 3072),
    "story_horizontal": (3840, 2160),
    "webmotors": (1920, 1440),
}
records = {}
for key, path in files.items():
    with Image.open(path) as image:
        size = image.size
        icc = bool(image.info.get("icc_profile"))
    if size != expected[key]:
        raise SystemExit(f"Dimensão inválida em {path}: {size}")
    records[key] = {
        "path": str(path),
        "size": list(size),
        "icc_profile_present": icc,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }
report = {
    "status": "approved_view_exported",
    "view": "dianteira-3-4",
    "source": str(source),
    "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "source_size": list(Image.open(source).size),
    "master_upscaled": True,
    "native_4k_claim": False,
    "generative_upscale": False,
    "resampling": "Lanczos",
    "outputs": records,
}
(out / "qa-exportacao.json").write_text(json.dumps(report, indent=2) + "\n")
print(out / "qa-exportacao.json")
PY

print "$OUT/master-4096x3072.png"
