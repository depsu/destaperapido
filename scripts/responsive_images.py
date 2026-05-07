#!/usr/bin/env python3
"""
responsive_images.py
--------------------
Genera variantes responsive (480w / 768w / 1280w) de las imágenes más
pesadas del sitio en formato WebP a calidad 80.

Uso:
    python3 scripts/responsive_images.py            # genera todo
    python3 scripts/responsive_images.py --force    # regenera aunque exista
"""
from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "public" / "images"

FORCE = "--force" in sys.argv

# Solo procesamos las imágenes "above the fold" / hero / cards visibles.
# El resto ya están lazy-loaded y no merecen el costo de mantener variantes.
SOURCES = [
    "camio-haciendo-servicio-en-la-calle.webp",                                    # LCP home + 59 páginas
    "mobile-Destape-alcantarillado-con-camion-en-subterraneo-de-edificio.webp",    # 1.3MB en 5 zonas
    "limpieza-con-camara.jpg",                                                     # card en 7 páginas
    "ridgid.jpeg",                                                                 # card en 7 páginas
    "camion-haciendo-servicio-en-condominio.webp",                                 # card en 7 páginas
    "camion-haciendo-destape-en-zona-rural.webp",                                  # 5 páginas
    "Destape-alcantarillado-con-camion-en-subterraneo-de-edificio.webp",
    "video-inspeccion.jpeg",
]

WIDTHS = [480, 768, 1280]
QUALITY = 80


def process(src_name: str) -> None:
    src = IMG_DIR / src_name
    if not src.exists():
        print(f"  ⚠ {src_name}: no existe")
        return
    stem = src.stem
    try:
        im = Image.open(src)
    except Exception as e:
        print(f"  ✗ {src_name}: {e}")
        return

    # Si la imagen no tiene alpha y es JPEG, convertimos a RGB para webp
    if im.mode in ("RGBA", "LA"):
        target_mode = "RGBA"
    else:
        im = im.convert("RGB")
        target_mode = "RGB"

    orig_w = im.size[0]
    out_lines = []
    for w in WIDTHS:
        if w >= orig_w:
            continue  # no upscale
        out_path = IMG_DIR / f"{stem}-{w}w.webp"
        if out_path.exists() and not FORCE:
            out_lines.append(f"={w}w (exists)")
            continue
        ratio = w / orig_w
        new_h = int(round(im.size[1] * ratio))
        resized = im.resize((w, new_h), Image.LANCZOS)
        if target_mode == "RGBA":
            resized.save(out_path, "WEBP", quality=QUALITY, method=6)
        else:
            resized.save(out_path, "WEBP", quality=QUALITY, method=6)
        out_lines.append(f"+{w}w ({out_path.stat().st_size//1024}KB)")
    print(f"  ✓ {src_name:80s} {orig_w}px → {' '.join(out_lines)}")


def main():
    print(f"Generando variantes responsive en {IMG_DIR}/\n")
    for s in SOURCES:
        process(s)
    print("\nListo.")


if __name__ == "__main__":
    main()
