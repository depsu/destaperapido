#!/usr/bin/env python3
"""
seo_a11y_fix.py
---------------
Mejoras masivas de accesibilidad y SEO aplicadas a TODOS los HTML de /public.

Idempotente y conservador: si una mejora ya existe, no la duplica.

Cambios aplicados:
  1. <body> class: reemplaza pb-30 (no existe en Tailwind) por pb-32; deduplica.
  2. Skip-to-content link visible al hacer focus (accesibilidad WCAG 2.4.1).
  3. <main id="main-content"> envolviendo el contenido principal (entre </nav>/menú móvil y <footer>).
  4. Hamburguesa móvil: aria-expanded="false" + aria-controls="mobile-menu-overlay".
  5. JS openMenu/closeMenu: actualiza aria-expanded al abrir/cerrar.
  6. <i> de FontAwesome decorativos: aria-hidden="true" (sólo si no lo tienen).
  7. <img>: añade decoding="async" donde falte (loading=lazy ya lo hace seo_perf_mobile.py).
  8. Imágenes rotas: corrige rutas inexistentes:
        /images/video-inspección.jpeg → /images/video-inspeccion.jpeg
        /images/destape-de-wc.webp     → /images/camion-haciendo-destape-en-subterraneo.webp
        /images/destape-de-cocina.webp → /images/camio-junto-a-trabajador-al-frente-de-una-empresa-haciendo-servicio-con-un-trabajador-3-.webp
  9. /chat-avatar.png en widget WA → /logo-nav.webp + alt accesible.
 10. Imágenes Unsplash genéricas en servicios/index.html → imágenes reales del sitio.

Uso:
    python3 scripts/seo_a11y_fix.py [--dry]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
DRY = "--dry" in sys.argv or "--dry-run" in sys.argv


# ---------------------------------------------------------------------------
# 1) Body class: pb-30 → pb-32, deduplicar
# ---------------------------------------------------------------------------
BODY_RE = re.compile(r'(<body\b[^>]*\bclass=")([^"]*)(")', re.IGNORECASE)


def fix_body_classes(html: str) -> tuple[str, bool]:
    m = BODY_RE.search(html)
    if not m:
        return html, False
    classes = m.group(2)
    original = classes
    # Reemplaza pb-30 por pb-32
    classes = re.sub(r"\bpb-30\b", "pb-32", classes)
    # Deduplica tokens manteniendo el orden
    seen = set()
    deduped = []
    for tok in classes.split():
        if tok in seen:
            continue
        seen.add(tok)
        deduped.append(tok)
    classes = " ".join(deduped)
    if classes == original:
        return html, False
    return html[: m.start(2)] + classes + html[m.end(2):], True


# ---------------------------------------------------------------------------
# 2) Skip-to-content link
# ---------------------------------------------------------------------------
SKIP_LINK_MARK = "skip-to-content-link"
SKIP_LINK_HTML = (
    '\n    <a href="#main-content" id="skip-to-content-link" '
    'class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 '
    'focus:z-[100] focus:bg-brand-600 focus:text-white focus:px-4 focus:py-2 '
    'focus:rounded-lg focus:shadow-lg focus:font-bold">'
    "Saltar al contenido</a>\n"
)
BODY_OPEN_RE = re.compile(r"(<body\b[^>]*>)", re.IGNORECASE)


def add_skip_link(html: str) -> tuple[str, bool]:
    if SKIP_LINK_MARK in html:
        return html, False
    m = BODY_OPEN_RE.search(html)
    if not m:
        return html, False
    insert_at = m.end()
    return html[:insert_at] + SKIP_LINK_HTML + html[insert_at:], True


# ---------------------------------------------------------------------------
# 3) <main id="main-content">
# ---------------------------------------------------------------------------
MAIN_OPEN_RE = re.compile(r"<main\b[^>]*>", re.IGNORECASE)
NAV_CLOSE_RE = re.compile(r"</nav>", re.IGNORECASE)
FOOTER_OPEN_RE = re.compile(r"<footer\b", re.IGNORECASE)
# Primer bloque de contenido principal después del nav
CONTENT_START_RE = re.compile(
    r"(?:<header\b[^>]*\bclass=\"[^\"]*(?:hero|mb-10|relative)[^\"]*\""
    r"|<section\b[^>]*\bclass=\""
    r"|<section\b[^>]*\bid=\""
    r"|<article\b[^>]*\bclass=\"[^\"]*(?:max-w|prose)[^\"]*\")",
    re.IGNORECASE,
)


def add_main_landmark(html: str) -> tuple[str, bool]:
    if MAIN_OPEN_RE.search(html):
        return html, False
    fm = FOOTER_OPEN_RE.search(html)
    if not fm:
        return html, False
    navs = list(NAV_CLOSE_RE.finditer(html))
    if not navs:
        return html, False
    after_nav = navs[-1].end()
    cm = CONTENT_START_RE.search(html, after_nav)
    if not cm:
        return html, False
    insert_at = cm.start()
    if insert_at >= fm.start():
        return html, False

    new = (
        html[:insert_at]
        + '<main id="main-content">\n    '
        + html[insert_at:fm.start()]
        + "</main>\n\n    "
        + html[fm.start():]
    )
    return new, True


# ---------------------------------------------------------------------------
# 4) Hamburguesa móvil accesible
# ---------------------------------------------------------------------------
HAMBURGER_RE = re.compile(
    r'(<button\b[^>]*\bonclick="openMenu\(\)"[^>]*?)(/?>)',
    re.IGNORECASE,
)


def fix_hamburger_aria(html: str) -> tuple[str, bool]:
    changed = False

    def repl(m: re.Match) -> str:
        nonlocal changed
        attrs, end = m.group(1), m.group(2)
        added = ""
        if "aria-expanded" not in attrs:
            added += ' aria-expanded="false"'
        if "aria-controls" not in attrs:
            added += ' aria-controls="mobile-menu-overlay"'
        if not added:
            return m.group(0)
        changed = True
        return attrs + added + end

    new_html = HAMBURGER_RE.sub(repl, html)
    return new_html, changed


# ---------------------------------------------------------------------------
# 5) JS openMenu/closeMenu actualiza aria-expanded
# ---------------------------------------------------------------------------
JS_OPEN_RE = re.compile(
    r"(function\s+openMenu\s*\(\s*\)\s*\{)(\s*overlay\.classList\.remove\([^)]+\);)",
    re.IGNORECASE,
)
JS_CLOSE_RE = re.compile(
    r"(function\s+closeMenu\s*\(\s*\)\s*\{)(\s*panel\.classList\.add\([^)]+\);)",
    re.IGNORECASE,
)
JS_ARIA_OPEN_MARK = "ariaExpandedTrueDestaperapido"
JS_ARIA_BLOCK = (
    "\n            // a11y: actualizar aria-expanded del botón hamburguesa\n"
    "            try {\n"
    "                document.querySelectorAll('[onclick=\"openMenu()\"]').forEach(function (b) {\n"
    "                    b.setAttribute('aria-expanded', '__VAL__'); /* " + JS_ARIA_OPEN_MARK + " */\n"
    "                });\n"
    "            } catch (e) {}\n"
)


def fix_menu_js(html: str) -> tuple[str, bool]:
    if JS_ARIA_OPEN_MARK in html:
        return html, False
    changed = False
    new_html = html

    m = JS_OPEN_RE.search(new_html)
    if m:
        new_html = (
            new_html[:m.end(2)]
            + JS_ARIA_BLOCK.replace("__VAL__", "true")
            + new_html[m.end(2):]
        )
        changed = True

    m = JS_CLOSE_RE.search(new_html)
    if m:
        new_html = (
            new_html[:m.end(2)]
            + JS_ARIA_BLOCK.replace("__VAL__", "false")
            + new_html[m.end(2):]
        )
        changed = True

    return new_html, changed


# ---------------------------------------------------------------------------
# 6) <i> FontAwesome decorativos: aria-hidden="true"
# ---------------------------------------------------------------------------
ICON_RE = re.compile(r"<i\b([^>]*)>", re.IGNORECASE)


def fix_decorative_icons(html: str) -> tuple[str, bool]:
    changed = False

    def repl(m: re.Match) -> str:
        nonlocal changed
        attrs = m.group(1)
        if "aria-hidden" in attrs:
            return m.group(0)
        if "fa-" not in attrs:
            return m.group(0)
        changed = True
        return f"<i{attrs} aria-hidden=\"true\">"

    new_html = ICON_RE.sub(repl, html)
    return new_html, changed


# ---------------------------------------------------------------------------
# 7) <img> decoding="async"
# ---------------------------------------------------------------------------
IMG_RE = re.compile(r"<img\b([^>]*)>", re.IGNORECASE | re.DOTALL)


def fix_img_decoding(html: str) -> tuple[str, bool]:
    changed = False

    def repl(m: re.Match) -> str:
        nonlocal changed
        attrs = m.group(1)
        if "decoding=" in attrs.lower():
            return m.group(0)
        changed = True
        return f"<img{attrs} decoding=\"async\">"

    new_html = IMG_RE.sub(repl, html)
    return new_html, changed


# ---------------------------------------------------------------------------
# 8 + 9) Reemplazo de rutas de imágenes rotas
# ---------------------------------------------------------------------------
IMAGE_REPLACEMENTS = {
    "/images/video-inspecci%C3%B3n.jpeg": "/images/video-inspeccion.jpeg",
    "/images/video-inspección.jpeg": "/images/video-inspeccion.jpeg",
    "/images/destape-de-wc.webp": "/images/camion-haciendo-destape-en-subterraneo.webp",
    "/images/destape-de-cocina.webp": "/images/camio-junto-a-trabajador-al-frente-de-una-empresa-haciendo-servicio-con-un-trabajador-3-.webp",
}


def fix_broken_image_paths(html: str) -> tuple[str, bool]:
    changed = False
    for old, new in IMAGE_REPLACEMENTS.items():
        if old in html:
            html = html.replace(old, new)
            changed = True
    return html, changed


# Chat-avatar PNG → logo webp + alt accesible
CHAT_AVATAR_RE = re.compile(
    r'<img\s+src="/(?:logo-nav\.png|chat-avatar\.png)"\s+alt="[^"]*"\s+class="wa-profile-pic"([^>]*)>',
    re.IGNORECASE,
)


def fix_chat_avatar(html: str) -> tuple[str, bool]:
    if not CHAT_AVATAR_RE.search(html):
        return html, False
    new_html = CHAT_AVATAR_RE.sub(
        '<img src="/logo-nav.webp" alt="Avatar de Destape Rápido en WhatsApp" '
        'class="wa-profile-pic" width="50" height="50" loading="lazy" decoding="async">',
        html,
    )
    return new_html, new_html != html


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
TRANSFORMS = [
    ("body-classes", fix_body_classes),
    ("skip-link", add_skip_link),
    ("main-landmark", add_main_landmark),
    ("hamburger-aria", fix_hamburger_aria),
    ("menu-js-aria", fix_menu_js),
    ("decorative-icons", fix_decorative_icons),
    ("img-decoding", fix_img_decoding),
    ("broken-images", fix_broken_image_paths),
    ("chat-avatar", fix_chat_avatar),
]


def process_file(path: Path) -> dict[str, bool]:
    raw = path.read_text(encoding="utf-8")
    out = raw
    report = {}
    for name, fn in TRANSFORMS:
        out, changed = fn(out)
        report[name] = changed
    if out != raw and not DRY:
        path.write_text(out, encoding="utf-8")
    return report


def main() -> int:
    files = sorted(PUBLIC.rglob("*.html"))
    total_changes = 0
    by_kind: dict[str, int] = {}
    for f in files:
        report = process_file(f)
        if any(report.values()):
            rel = f.relative_to(PUBLIC)
            kinds = [k for k, v in report.items() if v]
            print(f"  {'[dry] ' if DRY else ''}{rel}: {', '.join(kinds)}")
            total_changes += 1
            for k in kinds:
                by_kind[k] = by_kind.get(k, 0) + 1
    print()
    print(f"Total HTMLs procesados: {len(files)}")
    print(f"Total HTMLs modificados: {total_changes}")
    print("Cambios por categoría:")
    for k, v in sorted(by_kind.items(), key=lambda x: -x[1]):
        print(f"  - {k:20s} {v}")
    if DRY:
        print("(modo dry-run, ningún archivo fue escrito)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
