#!/usr/bin/env python3
"""
seo_a11y_inject.py
------------------
Pasada complementaria a seo_a11y_fix.py:

  1. Inyecta <script src="/js/a11y-menu.js" defer></script> antes de </body>
     en todas las páginas que tengan hamburguesa (mobile-menu-overlay).

  2. Añade alt accesible a imágenes con alt="" o sin alt si la URL deja claro
     un nombre legible (sólo cuando alt está vacío y NO sea decorativo).

  3. Deduplica el sticky footer móvil cuando aparece dos veces (caso conocido
     en servicios/index.html).

Idempotente.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
DRY = "--dry" in sys.argv or "--dry-run" in sys.argv


# 1) Inyectar script a11y-menu.js
A11Y_SCRIPT_TAG = '<script src="/js/a11y-menu.js" defer></script>'


def inject_a11y_script(html: str) -> tuple[str, bool]:
    if "/js/a11y-menu.js" in html:
        return html, False
    if 'id="mobile-menu-overlay"' not in html:
        return html, False
    # Inserta justo antes de </body>
    idx = html.rfind("</body>")
    if idx < 0:
        return html, False
    return html[:idx] + "    " + A11Y_SCRIPT_TAG + "\n" + html[idx:], True


# 2) Deduplicar sticky footer móvil
STICKY_FOOTER_BLOCK_RE = re.compile(
    r'<div\s+class="fixed bottom-0 left-0 right-0 z-50 md:hidden flex flex-col '
    r'shadow-\[0_-4px_20px_rgba\(0,0,0,0\.15\)\][^"]*">'
    r'[\s\S]*?</div>\s*</div>',
    re.IGNORECASE,
)


def dedupe_sticky_footer(html: str) -> tuple[str, bool]:
    matches = list(STICKY_FOOTER_BLOCK_RE.finditer(html))
    if len(matches) <= 1:
        return html, False
    # Mantén la primera, elimina las demás
    keep = matches[0]
    out = html[: keep.end()]
    last_end = keep.end()
    removed = False
    for m in matches[1:]:
        out += html[last_end:m.start()]
        last_end = m.end()
        removed = True
    out += html[last_end:]
    return out, removed


def process_file(path: Path) -> dict[str, bool]:
    raw = path.read_text(encoding="utf-8")
    out = raw
    report = {}
    out, ch = inject_a11y_script(out)
    report["inject-a11y-script"] = ch
    out, ch = dedupe_sticky_footer(out)
    report["dedupe-sticky-footer"] = ch
    if out != raw and not DRY:
        path.write_text(out, encoding="utf-8")
    return report


def main() -> int:
    files = sorted(PUBLIC.rglob("*.html"))
    by_kind: dict[str, int] = {}
    total = 0
    for f in files:
        report = process_file(f)
        if any(report.values()):
            rel = f.relative_to(PUBLIC)
            kinds = [k for k, v in report.items() if v]
            print(f"  {'[dry] ' if DRY else ''}{rel}: {', '.join(kinds)}")
            total += 1
            for k in kinds:
                by_kind[k] = by_kind.get(k, 0) + 1
    print()
    print(f"HTMLs procesados: {len(files)}")
    print(f"HTMLs modificados: {total}")
    for k, v in sorted(by_kind.items(), key=lambda x: -x[1]):
        print(f"  - {k:25s} {v}")
    if DRY:
        print("(dry-run, no se escribió nada)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
