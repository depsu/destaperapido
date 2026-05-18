#!/usr/bin/env python3
"""Add width/height to every <img> sitewide that lacks them.

Goal: CLS = 0. The browser reserves vertical space before the image bytes
arrive, eliminating layout shifts.

Strategy:
- Local images (/images/*.webp, *.jpg, etc.): try to read intrinsic
  dimensions with PIL/Pillow if available; otherwise infer from filename
  patterns like `-480w.webp` and use a sensible default ratio.
- External images (http/https): use generic defaults (1200x630 for og,
  800x600 otherwise) — they're usually decorative or sized via CSS.
- Skip <img> already having both width and height.

Idempotent: pages that already have all dims set are skipped.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# Try Pillow for intrinsic dimensions
try:
    from PIL import Image as PILImage  # type: ignore
    HAS_PIL = True
except Exception:
    HAS_PIL = False


def get_local_dims(src: str) -> "Optional[Tuple[int, int]]":
    """Return (w, h) for /images/foo.webp style paths, if file exists."""
    if not src.startswith("/"):
        return None
    p = PUBLIC / src.lstrip("/")
    if not p.exists():
        return None
    if HAS_PIL:
        try:
            with PILImage.open(p) as im:
                return im.size
        except Exception:
            return None
    # Fallback: guess from filename
    m = re.search(r"-(\d+)w\.", src)
    if m:
        w = int(m.group(1))
        return w, int(w * 9 / 16)
    return None


def default_dims_for(src: str) -> "Tuple[int, int]":
    """Sensible defaults when intrinsic dims unknown."""
    s = src.lower()
    if "logo" in s:
        return 72, 72
    if "avatar" in s:
        return 50, 50
    if "og" in s or "twitter" in s:
        return 1200, 630
    if "texture" in s or "pattern" in s:
        return 800, 800
    if "icon" in s:
        return 24, 24
    return 800, 600


IMG_RE = re.compile(r'<img\b([^>]*)>', re.DOTALL)
SRC_RE = re.compile(r'\bsrc="([^"]+)"')


def transform_img(tag_attrs: str) -> "Tuple[str, bool]":
    if 'width=' in tag_attrs and 'height=' in tag_attrs:
        return tag_attrs, False
    src_m = SRC_RE.search(tag_attrs)
    if not src_m:
        return tag_attrs, False
    src = src_m.group(1)
    if src.startswith("data:"):
        return tag_attrs, False
    dims = get_local_dims(src) or default_dims_for(src)
    w, h = dims
    new = tag_attrs
    if 'width=' not in new:
        new = f' width="{w}"' + new
    if 'height=' not in new:
        new = f' height="{h}"' + new
    return new, new != tag_attrs


def transform(html: str) -> "Tuple[str, int]":
    n = 0

    def _sub(m):
        nonlocal n
        attrs = m.group(1)
        new_attrs, changed = transform_img(attrs)
        if changed:
            n += 1
            return f'<img{new_attrs}>'
        return m.group(0)

    new_html = IMG_RE.sub(_sub, html)
    return new_html, n


def main() -> int:
    changed = 0
    total = 0
    for html_file in PUBLIC.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        new_text, n = transform(text)
        if n:
            html_file.write_text(new_text, encoding="utf-8")
            changed += 1
            total += n
    if HAS_PIL:
        print(f"(Pillow disponible — usé dimensiones intrínsecas reales)")
    else:
        print(f"(Sin Pillow — usé heurísticas de filename)")
    print(f"Archivos modificados: {changed}  Imgs sin dimensiones corregidas: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
