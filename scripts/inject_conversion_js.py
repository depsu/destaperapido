#!/usr/bin/env python3
"""
Inyecta <script src="/js/conversion.js" defer></script> antes de </body> en
todas las páginas HTML del sitio que aún no lo incluyen. Idempotente.
"""
import os
import sys
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
SNIPPETS = [
    ('<script src="/js/conversion.js" defer></script>', '/js/conversion.js'),
    ('<script src="/js/mobile-sticky-cta.js" defer></script>', '/js/mobile-sticky-cta.js'),
    ('<script src="/js/register-sw.js" defer></script>', '/js/register-sw.js'),
]
SKIP = {"output.css", "logo-nav.png", "logo-nav.webp"}

def find_html_files():
    for p in PUBLIC.rglob("*.html"):
        if "node_modules" in p.parts:
            continue
        yield p

def main():
    counts = {snippet: 0 for snippet, _ in SNIPPETS}
    added_files = set()
    for f in find_html_files():
        text = f.read_text(encoding="utf-8")
        original = text
        for snippet, marker in SNIPPETS:
            if marker in text:
                continue
            idx = text.rfind("</body>")
            if idx < 0:
                print(f"!! Sin </body>: {f}")
                break
            text = text[:idx] + "    " + snippet + "\n" + text[idx:]
            counts[snippet] += 1
            added_files.add(str(f.relative_to(PUBLIC)))
        if text != original:
            f.write_text(text, encoding="utf-8")

    for snippet, count in counts.items():
        print(f"+ {count}: {snippet}")
    print(f"Total archivos modificados: {len(added_files)}")

if __name__ == "__main__":
    main()
