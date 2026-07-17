#!/usr/bin/env python3
"""Arreglador de accesibilidad (a11y) — aplica los fixes MECÁNICOS y seguros que
detecta seo_a11y_audit.py, en toda la carpeta public/. Idempotente.

Qué arregla (todo invisible para el usuario, sin tocar el diseño):
  1. Ícono de búsqueda del header: agrega aria-label (antes solo tenía title=).
  2. <button> sin type: agrega type="button" SOLO a botones seguros (con onclick,
     o de menú por hover, o el de cerrar chat) — nunca a un submit de formulario.
  3. Footer: columnas <h4 ...uppercase tracking-wider...> → <h3> (evita el salto
     de encabezado h2 → h4 del pie de página).
  4. Recuadro superior: el primer <h3> que aparece ANTES del primer <h2> del
     cuerpo → <h2> (evita el salto h1 → h3 de los bloques "hero/emergencia").

NO toca contraste de color ni los campos de formulario sin label (esos 5 se
arreglan a mano, uno por uno, porque cada input es distinto).

Uso:
  python3 scripts/seo_a11y_fix_v2.py --dry-run     # muestra qué haría
  python3 scripts/seo_a11y_fix_v2.py               # aplica
  python3 scripts/seo_a11y_fix_v2.py --page public/x.html
"""
import os
import re
import sys
import glob
import argparse

SEARCH_RE = re.compile(r'(<a\s+href="/buscar"(?![^>]*aria-label)[^>]*)(>)')
BTN_RE = re.compile(r'<button\b(?![^>]*\btype=)([\s\S]*?)>', re.IGNORECASE)
HEADING_RE = re.compile(r'<h([1-6])\b([^>]*)>([\s\S]*?)</h\1>', re.IGNORECASE)


def fix_search(html):
    n = 0
    def repl(m):
        nonlocal n
        n += 1
        return f'{m.group(1)} aria-label="Buscar en el sitio"{m.group(2)}'
    return SEARCH_RE.sub(repl, html), n


def fix_buttons(html):
    n = 0
    has_form = "<form" in html.lower()
    def repl(m):
        nonlocal n
        inner = m.group(1)
        # Seguro (no es un submit de formulario) si: tiene manejador/estado
        # propio, o data-*, o la página no tiene ningún <form>.
        safe = ("onclick=" in inner or "cursor-default" in inner
                or "wa-close-btn" in inner or "data-" in inner or not has_form)
        if not safe:
            return m.group(0)  # posible submit de formulario: no tocar
        n += 1
        return f'<button type="button"{inner}>'
    return BTN_RE.sub(repl, html), n


def normalize_headings(html):
    """Recorre los encabezados en orden y elimina saltos de jerarquía: si uno
    salta más de un nivel respecto al anterior (ej. h2 → h4), lo baja al nivel
    permitido (h3). Nunca crea saltos; conserva las clases (mismo aspecto)."""
    n = 0
    prev = 0  # nivel del encabezado anterior ya normalizado

    def repl(m):
        nonlocal n, prev
        lvl = int(m.group(1))
        new = min(lvl, prev + 1) if prev else lvl  # el primero (h1) no se toca
        prev = new
        if new != lvl:
            n += 1
            return f'<h{new}{m.group(2)}>{m.group(3)}</h{new}>'
        return m.group(0)

    return HEADING_RE.sub(repl, html), n


def process(path, dry):
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    orig = html
    html, n1 = fix_search(html)
    html, n2 = fix_buttons(html)
    html, n3 = normalize_headings(html)
    n4 = 0
    total = n1 + n2 + n3 + n4
    if total and not dry:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
    return (n1, n2, n3, n4, html != orig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="public")
    ap.add_argument("--page")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    files = [args.page] if args.page else sorted(
        glob.glob(os.path.join(args.dir, "**", "*.html"), recursive=True))

    tot = [0, 0, 0, 0]
    changed = 0
    for f in files:
        n1, n2, n3, n4, ch = process(f, args.dry_run)
        for i, v in enumerate((n1, n2, n3, n4)):
            tot[i] += v
        if ch:
            changed += 1
            print(f"  {'(dry) ' if args.dry_run else ''}{f.replace('public','')}: "
                  f"buscar={n1} botones={n2} headings={n3}")
    print(f"\n{'DRY-RUN — ' if args.dry_run else ''}"
          f"{changed}/{len(files)} páginas · "
          f"aria-buscar={tot[0]} · type-boton={tot[1]} · headings-normalizados={tot[2]}")


if __name__ == "__main__":
    main()
