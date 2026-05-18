#!/usr/bin/env python3
"""Optimize hero/LCP image in pilot pages.

For each pilot, find the first non-logo <img> in absolute/cover position and:
1. Add srcset using existing -480w / -768w / -1280w variants if present.
2. Remove loading="lazy" -> set loading="eager" + fetchpriority="high".
3. Ensure width/height attrs.
4. Inject <link rel="preload" as="image"> in <head> for LCP.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

PILOTS = [
    "public/precios-orientativos.html",
    "public/zonas/rural/lampa.html",
    "public/zonas/rural/talagante.html",
    "public/zonas/rural/isla-de-maipo.html",
    "public/zonas/rural/colina.html",
    "public/zonas/rural/calera-de-tango.html",
    "public/zonas/rural/pirque.html",
]


def find_variants(src: str) -> dict:
    """Given /images/foo.webp or /images/foo.jpeg, find -480w / -768w / -1280w variants."""
    base = src.rsplit(".", 1)[0]
    # If src already has -###w suffix, strip it
    base = re.sub(r"-\d+w$", "", base)
    variants = {}
    for w in (480, 768, 1280):
        for ext in ("webp", "avif", "jpg", "jpeg", "png"):
            candidate = PUBLIC / f"{base[1:]}-{w}w.{ext}"
            if candidate.exists():
                variants[w] = f"{base}-{w}w.{ext}"
                break
    # Find a "main" srcset image too — prefer webp main
    main_webp = PUBLIC / f"{base[1:]}.webp"
    if main_webp.exists():
        variants["main"] = f"{base}.webp"
    return variants


def find_hero_img(content: str) -> "Optional[re.Match]":
    """Return Match for first non-logo, non-icon hero image."""
    pat = re.compile(
        r'<img\s+(?:[^>]*?\bsrc="(?P<src>[^"]+\.(?:webp|jpg|jpeg|png|avif))"[^>]*?)>',
        re.DOTALL,
    )
    for m in pat.finditer(content):
        src = m.group("src").lower()
        if any(skip in src for skip in ("logo", "icon", "favicon", "avatar", "/og.")):
            continue
        # Skip very early in head (preload links)
        # Hero img usually inside body (after <body>)
        body_start = content.find("<body")
        if body_start == -1 or m.start() < body_start:
            continue
        return m
    return None


def transform(html: str, rel: str) -> tuple[str, bool, str]:
    m = find_hero_img(html)
    if not m:
        return html, False, "no hero img"
    tag = m.group(0)
    src = m.group("src")
    variants = find_variants(src)
    if not variants:
        return html, False, f"no variants for {src}"

    new_tag = tag

    # 1. Add or replace srcset
    if variants:
        srcset_parts = []
        for w in (480, 768, 1280):
            if w in variants:
                srcset_parts.append(f"{variants[w]} {w}w")
        if srcset_parts:
            srcset_val = ", ".join(srcset_parts)
            if 'srcset=' in new_tag:
                new_tag = re.sub(r'\ssrcset="[^"]*"', f' srcset="{srcset_val}"', new_tag)
            else:
                # Insert after src=
                new_tag = re.sub(
                    r'(\ssrc="[^"]+")',
                    rf'\1 srcset="{srcset_val}"',
                    new_tag,
                    count=1,
                )
            # Also add sizes if not present
            if 'sizes=' not in new_tag:
                new_tag = new_tag.replace(' srcset="', ' sizes="100vw" srcset="', 1)

    # 2. Replace loading="lazy" with loading="eager"; ensure fetchpriority
    if 'loading="lazy"' in new_tag:
        new_tag = new_tag.replace('loading="lazy"', 'loading="eager"')
    elif 'loading=' not in new_tag:
        # Insert loading="eager"
        new_tag = re.sub(r'(<img\b)', r'\1 loading="eager"', new_tag, count=1)
    if 'fetchpriority=' not in new_tag:
        new_tag = re.sub(r'(<img\b)', r'\1 fetchpriority="high"', new_tag, count=1)

    # 3. Ensure decoding="async"
    if 'decoding=' not in new_tag:
        new_tag = re.sub(r'(<img\b)', r'\1 decoding="async"', new_tag, count=1)

    # 4. width/height: if not present, add 1920x1080 defaults (hero is cover, will scale)
    if 'width=' not in new_tag:
        new_tag = re.sub(r'(<img\b)', r'\1 width="1920"', new_tag, count=1)
    if 'height=' not in new_tag:
        new_tag = re.sub(r'(<img\b)', r'\1 height="1080"', new_tag, count=1)

    # Apply
    html = html[: m.start()] + new_tag + html[m.end():]

    # 5. Inject <link rel="preload" as="image" imagesrcset=...> in <head> if not present
    if 'rel="preload"' in html and src in html[: html.find('</head>')] and 'as="image"' in html[: html.find('</head>')]:
        # Already has some image preload, skip
        pass
    else:
        srcset_parts_pre = []
        for w in (480, 768, 1280):
            if w in variants:
                srcset_parts_pre.append(f"{variants[w]} {w}w")
        if srcset_parts_pre:
            preload_tag = (
                f'    <link rel="preload" as="image" '
                f'imagesrcset="{", ".join(srcset_parts_pre)}" imagesizes="100vw" fetchpriority="high">\n'
            )
            # Insert just before </head>
            html = html.replace('</head>', preload_tag + '</head>', 1)

    return html, True, f"src={src}, variants={list(variants.keys())}"


def main() -> int:
    for rel in PILOTS:
        f = ROOT / rel
        if not f.exists():
            print(f"  ??  {rel}: not found")
            continue
        text = f.read_text(encoding="utf-8")
        new_text, changed, note = transform(text, rel)
        if changed:
            f.write_text(new_text, encoding="utf-8")
            print(f"  ok  {rel}: {note}")
        else:
            print(f"  --  {rel}: {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
