#!/usr/bin/env python3
"""
seo_replace_unsplash.py
-----------------------
Reemplaza TODAS las imágenes Unsplash genéricas en HTMLs de /public por
imágenes reales del directorio /images/.

Por qué: las imágenes Unsplash son genéricas, no aportan E-E-A-T (no son
fotos del negocio), y bajan el SEO temático para una empresa local.

Estrategia:
- Mapea cada photo-ID conocido a una imagen local relevante.
- Para photo-IDs no mapeados, hace round-robin entre imágenes "genéricas
  pero del negocio" (camiones, servicios, etc.).
- Si la <img> tiene srcset, también lo neutraliza al mismo src.
- Conserva alt y demás atributos.

Idempotente.
"""
from __future__ import annotations

import re
import sys
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
DRY = "--dry" in sys.argv or "--dry-run" in sys.argv

# Imágenes locales válidas (rutas absolutas desde /public)
DEFAULT_POOL = [
    "/images/camio-haciendo-servicio-en-la-calle.webp",
    "/images/camion-haciendo-destape-en-zona-rural.webp",
    "/images/camion-haciendo-servicio-en-condominio.webp",
    "/images/camion-haciendo-destape-en-subterraneo.webp",
    "/images/Destape-alcantarillado-con-camion-en-subterraneo-de-edificio.webp",
    "/images/Destape-alcantarillado-en-parcela.webp",
    "/images/camion-limpia-fosas-y-mas-servicios.webp",
    "/images/camiones-y-camionetas-estacionados.webp",
    "/images/camio-junto-a-trabajador-al-frente-de-una-empresa-haciendo-servicio.webp",
    "/images/alcantarillado.webp",
    "/images/alcantarillado-2.webp",
    "/images/destape-de-alcantarilla.webp",
    "/images/limpieza-con-camara.jpg",
    "/images/video-inspeccion.jpeg",
    "/images/ridgid.jpeg",
]

# Mapping específico de photo-IDs comunes a imágenes contextuales
PHOTO_ID_MAP = {
    # baños / WC
    "1584622050111-993a426fbf0a": "/images/Destape-alcantarillado-con-camion-en-subterraneo-de-edificio.webp",
    "1585314235232-68245d29e929": "/images/camion-haciendo-destape-en-subterraneo.webp",
    # parcelas / rural
    "1500382017468-9049fed747ef": "/images/camion-haciendo-destape-en-zona-rural.webp",
    "1605980776566-0486c3ac7617": "/images/Destape-alcantarillado-en-parcela.webp",
    # edificios
    "1486406146926-c627a92ad1ab": "/images/camion-haciendo-servicio-en-condominio.webp",
    "1518780664697-55e3ad937233": "/images/camion-haciendo-servicio-en-condominio.webp",
    "1564013799919-ab600027ffc6": "/images/Destape-alcantarillado-con-camion-en-subterraneo-de-edificio.webp",
    # cocina / restaurante / desagüe
    "1414235077428-338989a2e8c0": "/images/camio-junto-a-trabajador-al-frente-de-una-empresa-haciendo-servicio.webp",
    "1450101499163-c8848c66ca85": "/images/camio-haciendo-servicio-en-la-calle.webp",
    # contratos / servicio
    "1521791136064-7984c1bc71f0": "/images/camio-haciendo-servicio-en-la-calle.webp",
    "1504198458649-3128b932f49e": "/images/camio-haciendo-servicio-en-la-calle.webp",
    "1516541196182-6bdb0516ed27": "/images/camion-limpia-fosas-y-mas-servicios.webp",
    # zonas / urbano
    "1621905251918-48416bd8575a": "/images/camio-haciendo-servicio-en-la-calle.webp",
    "1600607686527-6fb886090705": "/images/camion-haciendo-servicio-en-condominio.webp",
    # texturas / fondos genéricos
    "1593010952786-78ef92e0eb23": "/images/camiones-y-camionetas-estacionados.webp",
}


PHOTO_ID_RE = re.compile(r"photo-([a-f0-9]+-[a-f0-9]+)", re.IGNORECASE)
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE | re.DOTALL)
SRC_ATTR_RE = re.compile(r'\bsrc="(https://images\.unsplash\.com/[^"]+)"', re.IGNORECASE)
SRCSET_ATTR_RE = re.compile(r'\bsrcset="[^"]*images\.unsplash\.com[^"]*"', re.IGNORECASE)


def pick_replacement(unsplash_url: str) -> str:
    m = PHOTO_ID_RE.search(unsplash_url)
    if m:
        pid = m.group(1)
        if pid in PHOTO_ID_MAP:
            return PHOTO_ID_MAP[pid]
        # Hash determinístico para escoger del pool por defecto
        h = int(hashlib.md5(pid.encode()).hexdigest(), 16)
        return DEFAULT_POOL[h % len(DEFAULT_POOL)]
    # Fallback
    return DEFAULT_POOL[0]


def transform_img_tag(tag: str) -> tuple[str, bool]:
    src_match = SRC_ATTR_RE.search(tag)
    if not src_match:
        return tag, False
    new_src = pick_replacement(src_match.group(1))
    new_tag = SRC_ATTR_RE.sub(f'src="{new_src}"', tag, count=1)
    new_tag = SRCSET_ATTR_RE.sub("", new_tag)
    # Si quedan dobles espacios, normalizar
    new_tag = re.sub(r"  +", " ", new_tag)
    return new_tag, True


def process_file(path: Path) -> int:
    raw = path.read_text(encoding="utf-8")
    out = raw
    changes = 0

    def repl(m: re.Match) -> str:
        nonlocal changes
        new_tag, changed = transform_img_tag(m.group(0))
        if changed:
            changes += 1
        return new_tag

    out = IMG_TAG_RE.sub(repl, out)

    if out != raw and not DRY:
        path.write_text(out, encoding="utf-8")
    return changes


def main() -> int:
    files = sorted(PUBLIC.rglob("*.html"))
    total = 0
    files_changed = 0
    for f in files:
        n = process_file(f)
        if n:
            files_changed += 1
            total += n
            print(f"  {'[dry] ' if DRY else ''}{f.relative_to(PUBLIC)}: {n} imagen(es) reemplazada(s)")
    print()
    print(f"Total <img> Unsplash reemplazadas: {total}")
    print(f"HTMLs modificados: {files_changed}")
    if DRY:
        print("(dry-run, no se escribió nada)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
