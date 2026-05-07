#!/usr/bin/env python3
"""
apply_srcset.py
---------------
Inyecta atributos srcset+sizes en los <img> que apuntan a las imágenes
para las que ya generamos variantes responsive.

Idempotente: si el <img> ya tiene srcset, lo deja como está.

Uso:
    python3 scripts/apply_srcset.py [--dry]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

DRY = "--dry" in sys.argv

# Mapping: nombre fuente → (variantes disponibles, sizes default)
# variantes incluyen el ancho original al final (asumimos ≥ 1024px en
# pantalla wide). Para el hero LCP a full-bleed usamos sizes 100vw.
SOURCES = {
    "camio-haciendo-servicio-en-la-calle.webp": {
        "widths": [480, 768],
        "fallback_w": 1032,
        "sizes": "100vw",
    },
    "mobile-Destape-alcantarillado-con-camion-en-subterraneo-de-edificio.webp": {
        "widths": [480],
        "fallback_w": 734,
        "sizes": "(max-width: 768px) 100vw, 50vw",
    },
    "limpieza-con-camara.jpg": {
        "widths": [480, 768],
        "fallback_w": 791,
        "sizes": "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw",
    },
    "ridgid.jpeg": {
        "widths": [480, 768],
        "fallback_w": 1245,
        "sizes": "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw",
    },
    "camion-haciendo-servicio-en-condominio.webp": {
        "widths": [480],
        "fallback_w": 756,
        "sizes": "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw",
    },
    "camion-haciendo-destape-en-zona-rural.webp": {
        "widths": [480, 768],
        "fallback_w": 810,
        "sizes": "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw",
    },
    "Destape-alcantarillado-con-camion-en-subterraneo-de-edificio.webp": {
        "widths": [480, 768, 1280],
        "fallback_w": 1782,
        "sizes": "(max-width: 768px) 100vw, 50vw",
    },
    "video-inspeccion.jpeg": {
        "widths": [480, 768],
        "fallback_w": 1200,
        "sizes": "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw",
    },
}


def build_srcset(name: str, conf: dict) -> str:
    stem = name.rsplit(".", 1)[0]
    parts = [f"/images/{stem}-{w}w.webp {w}w" for w in conf["widths"]]
    parts.append(f"/images/{name} {conf['fallback_w']}w")
    return ", ".join(parts)


# Regex que matchea el <img ...> entero cuyo src apunta a /images/<name>
def img_pattern(name: str) -> re.Pattern:
    safe = re.escape(name)
    return re.compile(
        r'(<img\b)([^>]*?\bsrc\s*=\s*"/images/' + safe + r'"[^>]*?)(/?>)',
        re.IGNORECASE | re.DOTALL,
    )


def has_srcset(tag: str) -> bool:
    return re.search(r'\bsrcset\s*=', tag, re.IGNORECASE) is not None


def transform_tag(open_tag: str, attrs: str, close: str, srcset_value: str, sizes_value: str) -> str:
    """Inserta srcset y sizes después del src= dentro del tag."""
    # Si ya tiene srcset, no tocar
    full = open_tag + attrs + close
    if has_srcset(full):
        return full
    new_attrs = re.sub(
        r'(\bsrc\s*=\s*"[^"]+")',
        r'\1 srcset="' + srcset_value + '" sizes="' + sizes_value + '"',
        attrs,
        count=1,
        flags=re.IGNORECASE,
    )
    return open_tag + new_attrs + close


def update_preload(html: str, name: str, conf: dict) -> tuple[str, bool]:
    """Para la LCP, mejora el <link rel='preload'> con imagesrcset."""
    safe = re.escape(name)
    pat = re.compile(
        r'<link\s+rel="preload"\s+as="image"\s+href="/images/' + safe + r'"\s+fetchpriority="high"\s*/?>',
        re.IGNORECASE,
    )
    if not pat.search(html):
        return html, False
    if "imagesrcset" in html:
        return html, False  # ya actualizado
    srcset = build_srcset(name, conf)
    replacement = (
        f'<link rel="preload" as="image" href="/images/{name}" fetchpriority="high" '
        f'imagesrcset="{srcset}" imagesizes="{conf["sizes"]}">'
    )
    new_html = pat.sub(replacement, html, count=1)
    return new_html, new_html != html


def process(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    orig = text
    stats = {"file": str(path.relative_to(ROOT)), "imgs": 0, "preload": False}

    for name, conf in SOURCES.items():
        srcset = build_srcset(name, conf)
        sizes = conf["sizes"]
        pat = img_pattern(name)

        def repl(m: re.Match) -> str:
            new_tag = transform_tag(m.group(1), m.group(2), m.group(3), srcset, sizes)
            if new_tag != m.group(0):
                stats["imgs"] += 1
            return new_tag

        text = pat.sub(repl, text)

        # Update preload solo para el LCP del home/zonas
        text, changed = update_preload(text, name, conf)
        if changed:
            stats["preload"] = True

    if text != orig and not DRY:
        path.write_text(text, encoding="utf-8")
    stats["changed"] = text != orig
    return stats


def main():
    files = sorted(PUBLIC.rglob("*.html"))
    total_files = 0
    total_imgs = 0
    total_preloads = 0
    for f in files:
        s = process(f)
        if s["changed"]:
            total_files += 1
        total_imgs += s["imgs"]
        if s["preload"]:
            total_preloads += 1
        if s["imgs"] or s["preload"]:
            flags = []
            if s["imgs"]:
                flags.append(f"imgs={s['imgs']}")
            if s["preload"]:
                flags.append("preload")
            print(f"  ✓ {s['file']:55s} {' '.join(flags)}")
    print(f"\n{'[DRY] ' if DRY else ''}Archivos: {total_files} · imgs con srcset: {total_imgs} · preloads optimizados: {total_preloads}")


if __name__ == "__main__":
    main()
