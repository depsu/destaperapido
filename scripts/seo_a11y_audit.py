#!/usr/bin/env python3
"""Auditor de accesibilidad (a11y) estático para el sitio — SOLO LECTURA.

Recorre todas las páginas HTML de public/ y reporta problemas de accesibilidad
frecuentes según WCAG 2.1, sin dependencias externas (solo stdlib). No renderiza,
así que NO revisa contraste de color ni cosas dinámicas; sí cubre el grueso de
issues de un sitio estático:

  CRÍTICO — bloquean a usuarios de lector de pantalla / teclado:
    • <img> sin atributo alt
    • <html> sin lang
    • enlace/botón sin nombre accesible (ícono solo, sin texto ni aria-label)
    • input/select/textarea sin etiqueta asociada
    • falta <title> o está vacío
  SERIO — degradan mucho la experiencia:
    • salto en la jerarquía de encabezados (ej. h1 → h3)
    • más de un <h1> o ningún <h1>
    • viewport que bloquea el zoom (user-scalable=no / maximum-scale)
    • tabindex positivo (rompe el orden de tabulación)
  MENOR — buenas prácticas:
    • enlace/botón cuyo nombre viene solo de title=
    • <button> sin type
    • ids duplicados (rompen aria/label)

Uso:
  python3 scripts/seo_a11y_audit.py                 # todas las páginas
  python3 scripts/seo_a11y_audit.py --dir public    # otra carpeta
  python3 scripts/seo_a11y_audit.py --page public/servicios/x.html
  python3 scripts/seo_a11y_audit.py --severidad critico   # filtra
"""
import os
import sys
import glob
import argparse
from html.parser import HTMLParser

VOID = {"img", "input", "br", "hr", "meta", "link", "source", "area", "base", "col"}
INTERACTIVE = {"a", "button"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

CRIT, SERIO, MENOR = "CRÍTICO", "SERIO", "MENOR"
ORDER = {CRIT: 0, SERIO: 1, MENOR: 2}


class A11yParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.issues = []          # (severidad, regla, detalle)
        self.stack = []           # elementos abiertos: [{tag, attrs}]
        self.interactive = []     # contextos de <a>/<button> acumulando nombre
        self.aria_hidden_depth = 0
        self.html_lang = None
        self.has_title = False
        self._in_title = False
        self._title_text = ""
        self.h1_count = 0
        self.last_heading = 0     # nivel del último encabezado visto
        self.ids = {}             # id -> veces

    def add(self, sev, rule, detail):
        self.issues.append((sev, rule, detail))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        # ids duplicados
        if "id" in a:
            self.ids[a["id"]] = self.ids.get(a["id"], 0) + 1
        # tabindex positivo
        ti = a.get("tabindex")
        if ti and ti.lstrip("+").isdigit() and int(ti) > 0:
            self.add(SERIO, "tabindex-positivo", f"<{tag} tabindex={ti}>")

        if tag == "html":
            self.html_lang = a.get("lang")
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            c = a.get("content", "").lower().replace(" ", "")
            if "user-scalable=no" in c or "maximum-scale=1" in c or "maximum-scale=0" in c:
                self.add(SERIO, "zoom-bloqueado", f'viewport "{a.get("content","")}"')
        # encabezados: jerarquía
        if tag in HEADINGS:
            lvl = int(tag[1])
            if tag == "h1":
                self.h1_count += 1
            if self.last_heading and lvl > self.last_heading + 1:
                self.add(SERIO, "salto-encabezado",
                         f"h{self.last_heading} → h{lvl} (se salta h{self.last_heading+1})")
            self.last_heading = lvl
        # img sin alt
        if tag == "img":
            if "alt" not in a:
                src = a.get("src", "")[:60]
                self.add(CRIT, "img-sin-alt", f'<img src="{src}">')
        # inputs sin etiqueta
        if tag in {"input", "select", "textarea"}:
            itype = a.get("type", "").lower()
            if itype not in {"hidden", "submit", "button", "reset", "image"}:
                wrapped = any(e["tag"] == "label" for e in self.stack)
                labelled = ("aria-label" in a or "aria-labelledby" in a
                            or "title" in a or a.get("id") in _labels_for or wrapped)
                if not labelled:
                    self.add(CRIT, "campo-sin-label",
                             f'<{tag}{(" type="+itype) if itype else ""} name={a.get("name","?")}>')

        # aria-hidden: entra en subárbol oculto
        entering_hidden = a.get("aria-hidden") == "true"
        if entering_hidden:
            self.aria_hidden_depth += 1

        # abrir contexto interactivo
        if tag in INTERACTIVE:
            ctx = {"tag": tag, "attrs": a, "name_parts": [], "title_only": False}
            # aria-label / labelledby dan nombre directo
            if a.get("aria-label", "").strip() or a.get("aria-labelledby", "").strip():
                ctx["name_parts"].append("[aria]")
            self.interactive.append(ctx)
            # <a> sin href real
            if tag == "a":
                href = a.get("href", "").strip()
                if href in ("", "#") or href.startswith("javascript:"):
                    if "role" not in a and "onclick" not in a:
                        self.add(SERIO, "enlace-sin-destino", f'<a href="{href or "(vacío)"}">')

        # img con alt dentro de un contexto interactivo aporta nombre
        if tag == "img" and self.interactive and self.aria_hidden_depth == 0:
            if a.get("alt", "").strip():
                self.interactive[-1]["name_parts"].append("[img-alt]")
        # cualquier elemento con aria-label dentro aporta nombre
        if self.interactive and self.aria_hidden_depth == 0 and a.get("aria-label", "").strip():
            self.interactive[-1]["name_parts"].append("[aria-desc]")

        if tag not in VOID:
            self.stack.append({"tag": tag, "aria_hidden": entering_hidden})
        elif entering_hidden:
            # void con aria-hidden: cerrar de inmediato
            self.aria_hidden_depth -= 1

    def handle_data(self, data):
        if self._in_title:
            self._title_text += data
        if data.strip() and self.interactive and self.aria_hidden_depth == 0:
            self.interactive[-1]["name_parts"].append(data.strip()[:20])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
            if self._title_text.strip():
                self.has_title = True
        # cerrar contexto interactivo (el más reciente de ese tag)
        if tag in INTERACTIVE:
            for i in range(len(self.interactive) - 1, -1, -1):
                if self.interactive[i]["tag"] == tag:
                    ctx = self.interactive.pop(i)
                    self._check_name(ctx)
                    break
        # pop del stack + ajustar aria-hidden
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                if self.stack[i]["aria_hidden"]:
                    self.aria_hidden_depth = max(0, self.aria_hidden_depth - 1)
                del self.stack[i:]
                break
        # botón sin type
        # (se evalúa al abrir; aquí no hace falta)

    def _check_name(self, ctx):
        a = ctx["attrs"]
        has_real = any(p not in ("[title]",) for p in ctx["name_parts"])
        if not ctx["name_parts"]:
            # sin nombre visible ni aria — ¿title lo salva?
            if a.get("title", "").strip():
                self.add(MENOR, "nombre-solo-title",
                         f'<{ctx["tag"]}> con nombre solo por title="{a.get("title","")[:30]}"')
            else:
                cls = a.get("class", "")[:40]
                self.add(CRIT, "sin-nombre-accesible",
                         f'<{ctx["tag"]} class="{cls}"> sin texto ni aria-label')
        # botón sin type
        if ctx["tag"] == "button" and "type" not in {k.lower() for k in a}:
            self.add(MENOR, "boton-sin-type", f'<button class="{a.get("class","")[:30]}">')


# pre-escaneo simple de <label for=...> por archivo
_labels_for = set()


def scan_labels(html):
    import re
    return set(re.findall(r'<label[^>]*\bfor="([^"]+)"', html))


def audit_file(path):
    global _labels_for
    with open(path, encoding="utf-8", errors="replace") as fh:
        html = fh.read()
    _labels_for = scan_labels(html)
    p = A11yParser()
    try:
        p.feed(html)
    except Exception as e:  # noqa: BLE001 — nunca abortar todo por una página
        return [(SERIO, "parse-error", str(e)[:80])]
    out = list(p.issues)
    if p.html_lang is None:
        out.append((CRIT, "html-sin-lang", "<html> sin atributo lang"))
    if not p.has_title:
        out.append((CRIT, "sin-title", "falta <title> o está vacío"))
    if p.h1_count == 0:
        out.append((SERIO, "sin-h1", "la página no tiene <h1>"))
    elif p.h1_count > 1:
        out.append((SERIO, "multiple-h1", f"{p.h1_count} elementos <h1>"))
    for _id, n in p.ids.items():
        if n > 1:
            out.append((MENOR, "id-duplicado", f'id="{_id}" ×{n}'))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="public")
    ap.add_argument("--page")
    ap.add_argument("--severidad", choices=["critico", "serio", "menor"])
    args = ap.parse_args()

    if args.page:
        files = [args.page]
    else:
        files = sorted(glob.glob(os.path.join(args.dir, "**", "*.html"), recursive=True))

    filt = {"critico": CRIT, "serio": SERIO, "menor": MENOR}.get(args.severidad)
    total = {CRIT: 0, SERIO: 0, MENOR: 0}
    per_page = []

    for f in files:
        issues = audit_file(f)
        if filt:
            issues = [i for i in issues if i[0] == filt]
        for sev, _, _ in issues:
            total[sev] += 1
        if issues:
            per_page.append((f, issues))

    # ranking por gravedad
    per_page.sort(key=lambda x: (
        -sum(1 for i in x[1] if i[0] == CRIT),
        -sum(1 for i in x[1] if i[0] == SERIO),
        -len(x[1])))

    for f, issues in per_page:
        rel = f.replace("public", "")
        nc = sum(1 for i in issues if i[0] == CRIT)
        ns = sum(1 for i in issues if i[0] == SERIO)
        nm = sum(1 for i in issues if i[0] == MENOR)
        print(f"\n📄 {rel}   ({nc} crít · {ns} serio · {nm} menor)")
        issues.sort(key=lambda i: ORDER[i[0]])
        # agrupa reglas repetidas
        seen = {}
        for sev, rule, detail in issues:
            seen.setdefault((sev, rule), []).append(detail)
        for (sev, rule), details in seen.items():
            icon = {"CRÍTICO": "🔴", "SERIO": "🟠", "MENOR": "🟡"}[sev]
            extra = f"  (×{len(details)})" if len(details) > 1 else ""
            print(f"   {icon} {rule}{extra}: {details[0]}")

    print(f"\n{'='*60}")
    print(f"RESUMEN: {len(files)} páginas · {len(per_page)} con issues")
    print(f"  🔴 {total[CRIT]} críticos · 🟠 {total[SERIO]} serios · 🟡 {total[MENOR]} menores")


if __name__ == "__main__":
    main()
