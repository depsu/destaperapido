#!/usr/bin/env python3
"""
Para todas las páginas que no incluyen el backlink a paginasfast.cl,
inyecta una línea de crédito en el footer junto al copyright. Idempotente.
"""
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
CREDIT = ('<span class="text-xs text-slate-500 ml-2">· Diseñado por '
          '<a href="https://www.paginasfast.cl/" target="_blank" rel="noopener" '
          'class="hover:underline">PaginasFast.cl</a></span>')

# Match line containing &copy;...derechos reservados or just &copy;...Destape Rápido.
COPYRIGHT_RE = re.compile(
    r'(&copy;\s*<span id="year"></span>[^<]*?(?:Todos los derechos reservados\.?|Destape Rápido\.?))',
    re.IGNORECASE
)

def find_html_files():
    for p in PUBLIC.rglob("*.html"):
        if "node_modules" in p.parts:
            continue
        yield p

def main():
    added = []
    skipped = []
    no_match = []
    for f in find_html_files():
        text = f.read_text(encoding="utf-8")
        if "paginasfast" in text.lower():
            skipped.append(str(f.relative_to(PUBLIC)))
            continue
        m = COPYRIGHT_RE.search(text)
        if not m:
            no_match.append(str(f.relative_to(PUBLIC)))
            continue
        new_text = text.replace(m.group(0), m.group(0) + " " + CREDIT, 1)
        f.write_text(new_text, encoding="utf-8")
        added.append(str(f.relative_to(PUBLIC)))

    print(f"+ {len(added)} agregados")
    for p in added: print("  +", p)
    print(f"= {len(skipped)} ya tenían")
    print(f"!! {len(no_match)} sin patrón &copy; reconocible")
    for p in no_match: print("  !!", p)

if __name__ == "__main__":
    main()
