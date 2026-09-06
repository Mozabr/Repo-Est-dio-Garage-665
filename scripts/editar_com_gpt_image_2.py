#!/usr/bin/env python3
"""Executa uma unica edicao mascarada no GPT Image 2."""

from __future__ import annotations

import argparse
import base64
from contextlib import ExitStack
import hashlib
from io import BytesIO
import json
from pathlib import Path

from openai import OpenAI
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "pipeline.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imagem", type=Path, required=True)
    parser.add_argument("--mascara", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument(
        "--referencia",
        type=Path,
        action="append",
        default=[],
        help="Imagem de referencia adicional; repita a opcao para manter a ordem declarada no prompt",
    )
    parser.add_argument("--relatorio", type=Path)
    parser.add_argument(
        "--saida-bruta",
        type=Path,
        help="Opcional: arquiva a resposta integral da API antes da trava de pixels",
    )
    return parser.parse_args()


def validate_files(image_path: Path, mask_path: Path, references: list[Path]) -> tuple[int, int]:
    if image_path.suffix.lower() != ".png" or mask_path.suffix.lower() != ".png":
        raise ValueError("A imagem de trabalho e a mascara devem ser PNG")
    with Image.open(image_path) as image, Image.open(mask_path) as mask:
        if image.size != mask.size:
            raise ValueError(f"Imagem {image.size} e mascara {mask.size} devem ter o mesmo tamanho")
        if mask.mode not in {"RGBA", "LA"}:
            raise ValueError("A mascara precisa ser PNG com canal alfa")
    if image_path.stat().st_size >= 50 * 1024 * 1024 or mask_path.stat().st_size >= 50 * 1024 * 1024:
        raise ValueError("Imagem e mascara devem ter menos de 50 MB")
    for reference in references:
        if not reference.exists():
            raise FileNotFoundError(reference)
        if reference.stat().st_size >= 50 * 1024 * 1024:
            raise ValueError(f"Referencia deve ter menos de 50 MB: {reference}")
        with Image.open(reference) as ref:
            ref.verify()
    with Image.open(image_path) as image:
        return image.size


def main() -> None:
    args = parse_args()
    work_size = validate_files(args.imagem, args.mascara, args.referencia)
    config = json.loads(args.config.read_text(encoding="utf-8"))["openai_image_edit"]
    configured_size = tuple(map(int, config["size"].split("x")))
    if work_size != configured_size:
        raise ValueError(f"Entrada {work_size} difere do tamanho configurado {configured_size}")
    prompt = args.prompt.read_text(encoding="utf-8")

    client = OpenAI()
    with ExitStack() as stack:
        image_files = [stack.enter_context(args.imagem.open("rb"))]
        image_files.extend(stack.enter_context(path.open("rb")) for path in args.referencia)
        mask_file = stack.enter_context(args.mascara.open("rb"))
        result = client.images.edit(
            model=config["model"],
            image=image_files,
            mask=mask_file,
            prompt=prompt,
            quality=config["quality"],
            size=config["size"],
            output_format=config["output_format"],
        )

    generated_bytes = base64.b64decode(result.data[0].b64_json)
    if args.saida_bruta:
        args.saida_bruta.parent.mkdir(parents=True, exist_ok=True)
        args.saida_bruta.write_bytes(generated_bytes)

    with (
        Image.open(args.imagem) as original_source,
        Image.open(args.mascara) as mask_source,
        Image.open(BytesIO(generated_bytes)) as generated_source,
    ):
        original = original_source.convert("RGB")
        generated = generated_source.convert("RGB")
        mask_alpha = mask_source.convert("RGBA").getchannel("A")
        if generated.size != original.size:
            raise ValueError(
                f"A API retornou {generated.size}, mas a entrada mede {original.size}; "
                "a trava de pixels nao permite redimensionamento automatico"
            )
        edit_alpha = mask_alpha.point(lambda value: 255 - value)
        locked = Image.composite(generated, original, edit_alpha)
        icc_profile = original_source.info.get("icc_profile")

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    locked.save(args.saida, format="PNG", icc_profile=icc_profile)
    if args.relatorio:
        report = {
            "status": "generated_and_hard_contained_not_visually_approved",
            "model": config["model"],
            "quality": config["quality"],
            "size": config["size"],
            "source_sha256": hashlib.sha256(args.imagem.read_bytes()).hexdigest(),
            "mask_sha256": hashlib.sha256(args.mascara.read_bytes()).hexdigest(),
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "reference_sha256": [hashlib.sha256(path.read_bytes()).hexdigest() for path in args.referencia],
            "changed_pixels_outside_mask": 0
        }
        args.relatorio.parent.mkdir(parents=True, exist_ok=True)
        args.relatorio.write_text(json.dumps(report, indent=2) + "\n")
    print(args.saida.resolve())


if __name__ == "__main__":
    main()
