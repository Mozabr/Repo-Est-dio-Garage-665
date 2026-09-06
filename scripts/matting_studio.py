"""BiRefNet selection + ViTMatte trimap refinement, at source resolution.

Uses only pinned, downloaded snapshots. Original RGB stays unchanged in the
opaque vehicle interior. All intermediate masks remain available for review.
"""
from pathlib import Path
import argparse
import gc
import hashlib
import json
import os
import time

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("HF_HOME", str(ROOT / "modelos" / "hf-cache"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import cv2
import numpy as np
import torch
from PIL import Image, ImageOps
from torchvision import transforms
from transformers import AutoModelForImageSegmentation, VitMatteForImageMatting, VitMatteImageProcessor

def read_rgb(path):
    from studio_common import load_srgb
    return load_srgb(path)

def fingerprint(job, stage, out):
    lock = json.loads((ROOT / "integracoes/modelos-lock.json").read_text())
    entry = lock["birefnet" if stage == "birefnet" else "vitmatte"]
    value = {"source_sha": hashlib.sha256(Path(job["source"]).read_bytes()).hexdigest(),
             "roi": job["roi"], "revision": entry["revision"], "implementation": 1}
    if stage == "vitmatte":
        value.update({"base_alpha_sha": hashlib.sha256((out/"alpha-birefnet.png").read_bytes()).hexdigest(),
                      "fg": job.get("force_foreground", []), "bg": job.get("force_background", [])})
        if job.get("trimap_override"):
            value["trimap_override_sha"] = hashlib.sha256((ROOT/job["trimap_override"]).read_bytes()).hexdigest()
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def cached(out, stage, key, filename):
    record=out/f"cache-{stage}.json"
    return (out/filename).exists() and record.exists() and json.loads(record.read_text()).get("key")==key

def save_cache(out, stage, key):
    (out/f"cache-{stage}.json").write_text(json.dumps({"key":key}))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, default=ROOT / "config" / "piloto-v2.json")
    p.add_argument("--vista", action="append")
    p.add_argument("--etapa", choices=["birefnet", "vitmatte", "ambas"], default="ambas")
    args = p.parse_args()
    cfg = json.loads(args.config.read_text())
    jobs = [j for j in cfg["photos"] if not args.vista or j["id"] in args.vista]
    torch.set_num_threads(4)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Matting device: {device}", flush=True)
    if args.etapa in ("birefnet", "ambas"):
        model = AutoModelForImageSegmentation.from_pretrained(
            ROOT / "modelos/birefnet", trust_remote_code=True,
            local_files_only=True, use_safetensors=True).eval().to(device)
        transform = transforms.Compose([transforms.Resize((1024, 1024)), transforms.ToTensor(),
            transforms.Normalize([.485, .456, .406], [.229, .224, .225])])
        for job in jobs:
            out = ROOT / cfg["workdir"] / job["id"]
            out.mkdir(parents=True, exist_ok=True)
            key = fingerprint(job, "birefnet", out)
            if cached(out, "birefnet", key, "alpha-birefnet.png"):
                print(f"Reuse {job['id']} BiRefNet", flush=True)
                continue
            start = time.time()
            src = read_rgb(job["source"])
            box = tuple(job["roi"])
            crop = src.crop(box)
            print(f"BiRefNet: {job['id']} {crop.size}", flush=True)
            with torch.inference_mode():
                pred = model(transform(crop).unsqueeze(0).to(device))[-1].sigmoid()[0, 0].cpu().numpy()
            pred = cv2.resize(pred, crop.size, interpolation=cv2.INTER_LINEAR)
            # Keep the largest connected object inside the user-scoped car ROI.
            n, labels, stats, _ = cv2.connectedComponentsWithStats((pred > .5).astype(np.uint8))
            if n < 2:
                raise RuntimeError(f"No foreground found: {job['id']}")
            component = (labels == (1 + np.argmax(stats[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
            support = cv2.dilate(component, np.ones((11, 11), np.uint8))
            pred *= support
            alpha = np.zeros((src.height, src.width), dtype=np.float32)
            alpha[box[1]:box[3], box[0]:box[2]] = pred
            Image.fromarray(np.round(alpha * 255).astype(np.uint8)).save(out / "alpha-birefnet.png")
            save_cache(out, "birefnet", key)
            print(f"BiRefNet done: {time.time()-start:.1f}s", flush=True)
        del model
        gc.collect()
    if args.etapa in ("vitmatte", "ambas"):
        model = VitMatteForImageMatting.from_pretrained(ROOT / "modelos/vitmatte", local_files_only=True,
                   use_safetensors=True).eval().to(device)
        processor = VitMatteImageProcessor.from_pretrained(ROOT / "modelos/vitmatte", local_files_only=True)
        for job in jobs:
            out = ROOT / cfg["workdir"] / job["id"]
            key = fingerprint(job, "vitmatte", out)
            if cached(out, "vitmatte", key, "alpha-final.png"):
                print(f"Reuse {job['id']} ViTMatte", flush=True)
                continue
            start = time.time()
            src = read_rgb(job["source"])
            base = np.asarray(Image.open(out / "alpha-birefnet.png"))
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            fg = cv2.erode((base >= 245).astype(np.uint8), kernel) > 0
            bg = cv2.dilate((base > 10).astype(np.uint8), kernel) == 0
            trimap = np.full(base.shape, 128, dtype=np.uint8)
            trimap[fg] = 255
            trimap[bg] = 0
            # Explicit, reviewable patches only; no automatic fill of glass or wheel holes.
            for polygon in job.get("force_foreground", []):
                cv2.fillPoly(trimap, [np.asarray(polygon, np.int32)], 255)
            for polygon in job.get("force_background", []):
                cv2.fillPoly(trimap, [np.asarray(polygon, np.int32)], 0)
            if job.get("trimap_override"):
                with Image.open(ROOT/job["trimap_override"]) as override:
                    replacement=np.asarray(override.convert("L"))
                if replacement.shape!=trimap.shape or not np.isin(replacement,[0,128,255]).all():
                    raise ValueError("Manual trimap must match the source and contain only 0,128,255")
                trimap=replacement.copy()
            box = tuple(job["roi"])
            crop = src.crop(box)
            tri_crop = Image.fromarray(trimap).crop(box)
            inputs = processor(images=crop, trimaps=tri_crop, return_tensors="pt")
            print(f"ViTMatte: {job['id']} {crop.size}", flush=True)
            with torch.inference_mode():
                pred = model(**inputs.to(device)).alphas[0, 0].cpu().numpy()
            pred = pred[:crop.height, :crop.width]
            alpha = np.zeros_like(base, dtype=np.float32)
            alpha[box[1]:box[3], box[0]:box[2]] = pred
            alpha[trimap == 255] = 1
            alpha[trimap == 0] = 0
            alpha = np.clip(alpha, 0, 1)
            rgba = src.convert("RGBA")
            rgba.putalpha(Image.fromarray(np.round(alpha * 255).astype(np.uint8)))
            rgba.save(out / "carro-rgba.png")
            Image.fromarray(trimap).save(out / "trimap.png")
            Image.fromarray(np.round(alpha * 255).astype(np.uint8)).save(out / "alpha-final.png")
            report = {"source": job["source"], "source_size": list(src.size),
                "device": device, "matting_seconds": round(time.time()-start, 2),
                "foreground_fraction": float((alpha > .5).mean()),
                "fractional_edge_pixels": int(((alpha > .01) & (alpha < .99)).sum()),
                "interior_rgb_rebuilt": False, "status": "needs_visual_review"}
            (out / "matting.json").write_text(json.dumps(report, indent=2))
            save_cache(out, "vitmatte", key)
            print(f"ViTMatte done: {time.time()-start:.1f}s", flush=True)

if __name__ == "__main__":
    main()
