#!/usr/bin/env python3
"""
Para todas las páginas cuyo <footer>...</footer> no contiene un link a /blog,
inyecta un enlace discreto inline después del copyright. Idempotente.

Decisión de diseño: agregar el enlace al Blog SOLO en el footer (no en el
nav superior) para no distraer conversiones, según indicación del proyecto.
"""
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
LINK = ' · <a href="/blog" class="hover:text-brand-400">Blog</a>'

# Captura el bloque <footer ... > ... </footer>
FOOTER_RE = re.compile(r'<footer[\s\S]*?</footer>', re.IGNORECASE)
COPY_LINE_RE = re.compile(
    r'(&copy;\s*<span id="year"></span>[^<]*?(?:Todos los derechos reservados\.?|Destape Rápido\.?))',
    re.IGNORECASE
)
SIMPLE_COPY_RE = re.compile(r'(©\s*Destape Rápido[^<\n]*)', re.IGNORECASE)

def find_html_files():
    for p in PUBLIC.rglob("*.html"):
        if "node_modules" in p.parts:
            continue
        yield p

def patch_footer(text):
    fm = FOOTER_RE.search(text)
    if not fm:
        return text, False, "no-footer"
    footer = fm.group(0)
    if 'href="/blog' in footer or "href='/blog" in footer:
        return text, False, "ya-tiene"

    # Caso 1: copyright con span id="year"
    cm = COPY_LINE_RE.search(footer)
    if cm:
        new_footer = footer.replace(cm.group(0), cm.group(0) + LINK, 1)
        return text.replace(footer, new_footer, 1), True, "ok"

    # Caso 2: copyright simple
    cm2 = SIMPLE_COPY_RE.search(footer)
    if cm2:
        new_footer = footer.replace(cm2.group(0), cm2.group(0) + LINK, 1)
        return text.replace(footer, new_footer, 1), True, "ok-simple"

    return text, False, "no-copy-pattern"

def main():
    counts = {"ok": 0, "ok-simple": 0, "ya-tiene": 0, "no-footer": 0, "no-copy-pattern": 0}
    failed = []
    for f in find_html_files():
        text = f.read_text(encoding="utf-8")
        new_text, changed, reason = patch_footer(text)
        counts[reason] = counts.get(reason, 0) + 1
        if changed:
            f.write_text(new_text, encoding="utf-8")
        elif reason == "no-copy-pattern":
            failed.append(str(f.relative_to(PUBLIC)))

    for k, v in counts.items():
        print(f"  {k}: {v}")
    if failed:
        print("Sin patrón de copyright:")
        for p in failed: print("  -", p)

if __name__ == "__main__":
    main()
