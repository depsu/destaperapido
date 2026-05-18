#!/usr/bin/env python3
"""
Agrega loading="lazy" decoding="async" a imágenes que no lo tienen, evitando
las que probablemente sean LCP (fetchpriority="high" o dentro del primer
<header>/primera <section>). Idempotente.
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup

PUBLIC = Path(__file__).resolve().parent.parent / "public"
TARGETS = [
    "blog", "servicios", "zonas/urbano", "zonas/rural", "casos-reales",
    "landing"
]

def main():
    total_added = 0
    files_changed = 0
    for sub in TARGETS:
        for f in (PUBLIC / sub).rglob("*.html"):
            text = f.read_text(encoding="utf-8")
            soup = BeautifulSoup(text, "html.parser")

            # Identificar imágenes "above the fold" para no marcarlas lazy
            protected_imgs = set()
            # 1. Imágenes con fetchpriority="high" o loading="eager"
            for img in soup.find_all("img"):
                fp = (img.get("fetchpriority") or "").lower()
                ld = (img.get("loading") or "").lower()
                if fp == "high" or ld == "eager":
                    protected_imgs.add(id(img))

            # 2. Primera imagen del primer <header>
            first_header = soup.find("header")
            if first_header:
                first_img = first_header.find("img")
                if first_img:
                    protected_imgs.add(id(first_img))

            # 3. Primera imagen del primer <main> > <section>
            main_el = soup.find("main")
            section = main_el.find("section") if main_el else soup.find("section")
            if section:
                first_img = section.find("img")
                if first_img:
                    protected_imgs.add(id(first_img))

            changed = 0
            for img in soup.find_all("img"):
                if img.has_attr("loading"):
                    continue
                if id(img) in protected_imgs:
                    continue
                img["loading"] = "lazy"
                if not img.has_attr("decoding"):
                    img["decoding"] = "async"
                changed += 1

            if changed:
                f.write_text(str(soup), encoding="utf-8")
                files_changed += 1
                total_added += changed
                print(f"+ {changed:2d} imgs lazy: {f.relative_to(PUBLIC)}")

    print(f"\nTotal: {total_added} imágenes en {files_changed} archivos")

if __name__ == "__main__":
    main()
