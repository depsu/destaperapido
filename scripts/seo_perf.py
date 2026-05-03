#!/usr/bin/env python3
"""
Optimizaciones de Core Web Vitals seguras y idempotentes:
- FontAwesome CDN: cargar async (media=print + onload=swap) + noscript fallback.
- Scripts JS no críticos: añadir `defer`.
- index.html: añadir <link rel="preload"> del hero (LCP).

NO toca:
- Tailwind CDN (puede romper layouts).
- output.css (build).
- Imágenes inline.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DRY = "--dry-run" in sys.argv

# Marcadores idempotentes para no aplicar dos veces
FA_MARK = 'media="print" onload'

# 1) FontAwesome CDN sync → async
FA_PATTERN = re.compile(
    r'<link\s+rel="stylesheet"\s+href="(https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+)"\s*/?>',
    re.IGNORECASE,
)


def transform_fontawesome(content: str) -> str:
    if FA_MARK in content and "cdnjs.cloudflare.com/ajax/libs/font-awesome" in content:
        # Already converted on at least one tag — but verify each occurrence:
        return FA_PATTERN.sub(
            lambda m: (
                f'<link rel="preload" as="style" href="{m.group(1)}">\n'
                f'    <link rel="stylesheet" href="{m.group(1)}" media="print" onload="this.media=\'all\'">\n'
                f'    <noscript><link rel="stylesheet" href="{m.group(1)}"></noscript>'
            ),
            content,
        ) if False else content  # dejarlo como está si ya hay 1 con marcador

    def repl(m: re.Match) -> str:
        href = m.group(1)
        return (
            f'<link rel="preload" as="style" href="{href}">\n'
            f'    <link rel="stylesheet" href="{href}" media="print" onload="this.media=\'all\'">\n'
            f'    <noscript><link rel="stylesheet" href="{href}"></noscript>'
        )

    return FA_PATTERN.sub(repl, content)


# 2) <script src="/js/...js"> sin defer → con defer
JS_PATTERN = re.compile(
    r'<script\s+src="(/js/[^"]+\.js)"\s*></script>'
)


def transform_local_scripts(content: str) -> str:
    def repl(m: re.Match) -> str:
        return f'<script src="{m.group(1)}" defer></script>'

    return JS_PATTERN.sub(repl, content)


# 3) Hero preload sólo para index.html
HERO_PRELOAD = (
    '    <link rel="preload" as="image" '
    'href="/images/camio-haciendo-servicio-en-la-calle.webp" '
    'fetchpriority="high">'
)


def add_hero_preload(content: str, path: Path) -> str:
    rel = path.relative_to(PUBLIC).as_posix()
    if rel != "index.html":
        return content
    if "rel=\"preload\" as=\"image\"" in content:
        return content
    # Insert just before </head>
    return content.replace("</head>", f"{HERO_PRELOAD}\n</head>", 1)


def process(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    new = raw
    new = transform_fontawesome(new)
    new = transform_local_scripts(new)
    new = add_hero_preload(new, path)
    if new != raw:
        if not DRY:
            path.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed: list[str] = []
    for f in sorted(PUBLIC.rglob("*.html")):
        if f.name == "test.html":
            continue
        if process(f):
            changed.append(str(f.relative_to(ROOT)))
    print(f"{'[dry-run] ' if DRY else ''}archivos optimizados: {len(changed)}")
    for c in changed:
        print(f"  - {c}")


if __name__ == "__main__":
    main()
