#!/usr/bin/env python3
"""
Validador SEO/GEO local para destaperapido.cl.

Hace 5 chequeos en todos los archivos HTML de public/:
  1. JSON-LD: cada bloque <script type="application/ld+json"> es JSON válido y tiene @context/@type.
  2. Consistencia: AggregateRating, streetAddress, foundingDate, telephone deben ser iguales en TODOS los archivos donde aparecen.
  3. Meta tags: title, meta description, canonical, og:title, og:description, og:image presentes.
  4. Links internos rotos: cada href="/..." apunta a un archivo que existe en public/.
  5. Imágenes referenciadas: cada src="/images/..." apunta a un archivo que existe.

Salida: resumen al final con conteo de errores/warnings por categoría.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

# --- Patrones ---
JSONLD_RE = re.compile(
    r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
    flags=re.DOTALL | re.IGNORECASE,
)
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.DOTALL | re.IGNORECASE)
META_DESC_RE = re.compile(r'<meta\s+name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', re.IGNORECASE)
CANONICAL_RE = re.compile(r'<link\s+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', re.IGNORECASE)
OG_TITLE_RE = re.compile(r'<meta\s+property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', re.IGNORECASE)
OG_DESC_RE = re.compile(r'<meta\s+property=["\']og:description["\'][^>]*content=["\']([^"\']+)["\']', re.IGNORECASE)
OG_IMG_RE = re.compile(r'<meta\s+property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', re.IGNORECASE)

# href/src internos: /algo, /algo/, /algo.html, /algo#anchor
HREF_INTERNAL_RE = re.compile(r'href=["\'](/[^"\'#\?]*[^"\'/])["\']', re.IGNORECASE)
SRC_IMG_RE = re.compile(r'src=["\'](/images/[^"\']+)["\']', re.IGNORECASE)


# --- Estructuras de resultado ---
errors: list[str] = []
warnings: list[str] = []

consistency: dict[str, dict[str, set[str]]] = {
    "ratingValue": defaultdict(set),
    "reviewCount": defaultdict(set),
    "streetAddress": defaultdict(set),
    "addressLocality": defaultdict(set),
    "postalCode": defaultdict(set),
    "foundingDate": defaultdict(set),
    "telephone": defaultdict(set),
}

stats = {
    "files_checked": 0,
    "jsonld_blocks": 0,
    "jsonld_invalid": 0,
    "meta_missing": 0,
    "broken_links": 0,
    "broken_images": 0,
}


def collect_consistency_values(item: dict, file_rel: str) -> None:
    """Recoge valores que deben ser consistentes entre archivos."""
    if not isinstance(item, dict):
        return
    types = item.get("@type", [])
    if isinstance(types, str):
        types = [types]
    is_business = any(t in ("LocalBusiness", "Plumber", "Organization") for t in types)

    if is_business:
        if "telephone" in item:
            consistency["telephone"][str(item["telephone"])].add(file_rel)
        if "foundingDate" in item:
            consistency["foundingDate"][str(item["foundingDate"])].add(file_rel)
        addr = item.get("address")
        if isinstance(addr, dict):
            for key in ("streetAddress", "addressLocality", "postalCode"):
                if key in addr:
                    consistency[key][str(addr[key])].add(file_rel)
        rating = item.get("aggregateRating")
        if isinstance(rating, dict):
            if "ratingValue" in rating:
                consistency["ratingValue"][str(rating["ratingValue"])].add(file_rel)
            if "reviewCount" in rating:
                consistency["reviewCount"][str(rating["reviewCount"])].add(file_rel)


def validate_jsonld(content: str, file_rel: str) -> None:
    """Valida cada bloque JSON-LD del archivo."""
    blocks = JSONLD_RE.findall(content)
    for i, body in enumerate(blocks, 1):
        body = body.strip()
        if not body:
            continue
        stats["jsonld_blocks"] += 1
        try:
            data = json.loads(body)
        except json.JSONDecodeError as e:
            errors.append(f"  ❌ {file_rel} · bloque JSON-LD #{i}: JSON inválido — {e.msg} (línea {e.lineno}, col {e.colno})")
            stats["jsonld_invalid"] += 1
            continue

        items = data if isinstance(data, list) else [data]
        for j, item in enumerate(items, 1):
            if not isinstance(item, dict):
                continue
            if "@context" not in item:
                warnings.append(f"  ⚠️  {file_rel} · bloque #{i}, item #{j}: falta @context")
            if "@type" not in item:
                warnings.append(f"  ⚠️  {file_rel} · bloque #{i}, item #{j}: falta @type")
            collect_consistency_values(item, file_rel)


def validate_meta(content: str, file_rel: str) -> None:
    """Verifica que los meta tags básicos estén presentes."""
    # Skip 404 y otras páginas que no necesitan canonical
    if file_rel.endswith("404.html"):
        return

    checks = {
        "title": TITLE_RE.search(content),
        "meta description": META_DESC_RE.search(content),
        "canonical": CANONICAL_RE.search(content),
        "og:title": OG_TITLE_RE.search(content),
        "og:description": OG_DESC_RE.search(content),
        "og:image": OG_IMG_RE.search(content),
    }
    missing = [name for name, m in checks.items() if not m]
    if missing:
        warnings.append(f"  ⚠️  {file_rel} · meta tags faltantes: {', '.join(missing)}")
        stats["meta_missing"] += 1


def validate_internal_links(content: str, file_rel: str) -> None:
    """Verifica que cada href interno apunte a un archivo existente."""
    found = HREF_INTERNAL_RE.findall(content)
    for href in set(found):  # dedup
        # ignorar anchors, query strings, telefono, mailto
        if href.startswith(("/#", "tel:", "mailto:")):
            continue
        # Posibles destinos: /foo → /foo.html o /foo/index.html
        candidates = [
            PUBLIC / href.lstrip("/"),
            PUBLIC / (href.lstrip("/") + ".html"),
            PUBLIC / href.lstrip("/") / "index.html",
        ]
        if not any(c.exists() and c.is_file() for c in candidates):
            errors.append(f"  ❌ {file_rel} · link roto: {href}")
            stats["broken_links"] += 1


def validate_images(content: str, file_rel: str) -> None:
    """Verifica que cada src de imagen apunte a un archivo existente."""
    found = SRC_IMG_RE.findall(content)
    for src in set(found):
        path = PUBLIC / src.lstrip("/")
        if not path.exists():
            warnings.append(f"  ⚠️  {file_rel} · imagen no encontrada: {src}")
            stats["broken_images"] += 1


def main() -> None:
    html_files = sorted(
        p for p in PUBLIC.rglob("*.html")
        if "node_modules" not in p.parts
    )

    for path in html_files:
        rel = str(path.relative_to(PUBLIC))
        stats["files_checked"] += 1
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            errors.append(f"  ❌ {rel}: no se puede leer como UTF-8 ({e})")
            continue

        # Para link/img validation, eliminar comentarios HTML para evitar falsos positivos.
        content_no_comments = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

        validate_jsonld(content, rel)
        validate_meta(content, rel)
        validate_internal_links(content_no_comments, rel)
        validate_images(content_no_comments, rel)

    # --- Reporte ---
    print("=" * 72)
    print("VALIDACIÓN SEO/GEO — destaperapido.cl")
    print("=" * 72)
    print(f"\nArchivos HTML escaneados: {stats['files_checked']}")
    print(f"Bloques JSON-LD encontrados: {stats['jsonld_blocks']}")

    print("\n" + "─" * 72)
    print("CONSISTENCIA DE DATOS (deben tener un solo valor común)")
    print("─" * 72)
    inconsistencies = 0
    for key, values_to_files in consistency.items():
        if not values_to_files:
            continue
        if len(values_to_files) == 1:
            value = next(iter(values_to_files))
            files_count = len(values_to_files[value])
            print(f"  ✅ {key}: '{value}' en {files_count} archivo(s)")
        else:
            inconsistencies += 1
            print(f"  ⚠️  {key}: {len(values_to_files)} valores distintos detectados")
            for value, files in values_to_files.items():
                files_list = sorted(files)
                preview = ", ".join(files_list[:3])
                more = f" (+{len(files_list)-3} más)" if len(files_list) > 3 else ""
                print(f"     - '{value}' en: {preview}{more}")

    if inconsistencies == 0:
        print("\n  ✅ Todos los valores críticos son consistentes.")

    print("\n" + "─" * 72)
    print(f"ERRORES: {len(errors)}")
    print("─" * 72)
    if errors:
        for e in errors[:30]:
            print(e)
        if len(errors) > 30:
            print(f"  ... y {len(errors) - 30} errores más (truncado)")
    else:
        print("  ✅ Sin errores.")

    print("\n" + "─" * 72)
    print(f"WARNINGS: {len(warnings)}")
    print("─" * 72)
    if warnings:
        for w in warnings[:30]:
            print(w)
        if len(warnings) > 30:
            print(f"  ... y {len(warnings) - 30} warnings más (truncado)")
    else:
        print("  ✅ Sin warnings.")

    print("\n" + "=" * 72)
    print("RESUMEN")
    print("=" * 72)
    print(f"  JSON-LD inválidos:   {stats['jsonld_invalid']}")
    print(f"  Meta tags faltantes: {stats['meta_missing']}")
    print(f"  Links rotos:         {stats['broken_links']}")
    print(f"  Imágenes rotas:      {stats['broken_images']}")
    print(f"  Inconsistencias:     {inconsistencies}")

    has_errors = bool(errors)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
