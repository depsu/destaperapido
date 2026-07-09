#!/usr/bin/env python3
"""
Aplicador SEO masivo para Destape Rápido.

Ejecuta de forma idempotente sobre todo public/*.html:
- Unifica dominio canónico (siempre con www).
- Estandariza teléfono (+56 9 6588 9226 / +56965889226).
- Inserta canonical, OG, Twitter Card y JSON-LD donde falten.
- Genera JSON-LD apropiado por tipo de página (home, servicio, zona,
  blog, landing, etc.).

Uso:
    python3 scripts/seo_apply.py [--dry-run]

Reglas:
- No toca contenido visible (solo <head> y normalizaciones de phone/dominio).
- No sobreescribe bloques JSON-LD existentes (los respeta).
- Si OG/Twitter ya están, no los duplica.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

BRAND = "Destape Rápido"
BASE_URL = "https://www.destaperapido.cl"
SITE_ID = f"{BASE_URL}/#business"
PHONE_DISPLAY = "+56 9 6588 9226"
PHONE_E164 = "+56965889226"
EMAIL = "contacto@destaperapido.cl"
LOGO = f"{BASE_URL}/logo-nav.webp"
DEFAULT_OG_IMAGE = f"{BASE_URL}/images/camio-haciendo-servicio-en-la-calle.webp"
TODAY = date.today().isoformat()

DRY_RUN = "--dry-run" in sys.argv


# ---------- helpers ----------

def canonical_for(path: Path) -> str:
    rel = path.relative_to(PUBLIC).as_posix()
    if rel == "index.html":
        return f"{BASE_URL}/"
    if rel.endswith("/index.html"):
        return f"{BASE_URL}/{rel[:-len('index.html')]}"
    if rel.endswith(".html"):
        return f"{BASE_URL}/{rel[:-5]}"
    return f"{BASE_URL}/{rel}"


def breadcrumb_levels(path: Path) -> list[tuple[str, str]]:
    rel = path.relative_to(PUBLIC).as_posix()
    pairs: list[tuple[str, str]] = [("Inicio", f"{BASE_URL}/")]

    parts = rel.split("/")
    is_index = parts[-1] == "index.html"
    folder = parts[:-1] if not is_index else parts[:-1]
    name_map = {
        "servicios": "Servicios",
        "zonas": "Zonas",
        "rural": "Zonas Rurales",
        "urbano": "Zonas Urbanas",
        "blog": "Blog",
        "landing": "Landings",
        "casos-reales": "Casos Reales",
    }

    cur = ""
    for p in folder:
        cur += f"{p}/"
        pairs.append((name_map.get(p, p.replace("-", " ").title()),
                      f"{BASE_URL}/{cur}"))

    if not is_index:
        slug = parts[-1].replace(".html", "")
        # Use title from html later; for now generate from slug
        pairs.append((slug.replace("-", " ").title(), canonical_for(path)))
    return pairs


def extract(content: str, pattern: str, group: int = 1) -> Optional[str]:
    m = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    return m.group(group).strip() if m else None


def html_unescape(s: str) -> str:
    return (s.replace("&amp;", "&").replace("&quot;", '"')
             .replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">"))


def insert_before_close_head(content: str, snippet: str) -> str:
    return content.replace("</head>", f"{snippet}\n</head>", 1)


def already_has(content: str, marker: str) -> bool:
    return marker in content


# ---------- JSON-LD builders ----------

def base_business() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "Plumber"],
        "@id": SITE_ID,
        "name": BRAND,
        "url": BASE_URL,
        "telephone": PHONE_E164,
        "email": EMAIL,
        "image": LOGO,
        "logo": LOGO,
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Santiago",
            "addressRegion": "Región Metropolitana",
            "addressCountry": "CL",
        },
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "Región Metropolitana, Chile"}
        ],
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                    "Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday",
                ],
                "opens": "00:00",
                "closes": "23:59",
            }
        ],
    }


def breadcrumb_jsonld(path: Path) -> dict:
    levels = breadcrumb_levels(path)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(levels)
        ],
    }


def service_jsonld(name: str, description: str, area: str = "Región Metropolitana, Chile") -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": name,
        "name": f"{name} en {area}",
        "description": description,
        "provider": {"@id": SITE_ID},
        "areaServed": {"@type": "AdministrativeArea", "name": area},
    }


def article_jsonld(path: Path, title: str, description: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "datePublished": TODAY,
        "dateModified": TODAY,
        "author": {
            "@type": "Person",
            "name": "Alejandro Rivera",
            "url": f"{BASE_URL}/nosotros",
        },
        "publisher": {"@id": SITE_ID},
        "mainEntityOfPage": canonical_for(path),
        "image": DEFAULT_OG_IMAGE,
    }


# ---------- page categorization ----------

def classify(path: Path) -> str:
    rel = path.relative_to(PUBLIC).as_posix()
    if rel == "index.html":
        return "home"
    if rel == "404.html":
        return "404"
    if rel.startswith("servicios/"):
        if rel.endswith("/index.html"):
            return "servicios_index"
        return "servicio"
    if rel.startswith("zonas/"):
        if rel.endswith("/index.html"):
            return "zonas_index"
        return "zona"
    if rel.startswith("blog/"):
        if rel.endswith("/index.html"):
            return "blog_index"
        return "blog_post"
    if rel.startswith("landing/"):
        return "landing"
    if rel.startswith("casos-reales/"):
        return "casos"
    return "static"


# ---------- transformations ----------

DOMAIN_REPLACEMENTS = [
    # Always upgrade non-www to www in absolute references inside HTML
    ("https://destaperapido.cl", "https://www.destaperapido.cl"),
    ("http://destaperapido.cl", "https://www.destaperapido.cl"),
    ("http://www.destaperapido.cl", "https://www.destaperapido.cl"),
]


def normalize_domain_and_phone(content: str) -> str:
    for a, b in DOMAIN_REPLACEMENTS:
        content = content.replace(a, b)
    # Standardize phone
    content = re.sub(r"\+56[\s\xa0]*9[\s\xa0]*3647[\s\xa0]*0112", PHONE_DISPLAY, content)
    content = content.replace("+56936470112", PHONE_E164)
    content = content.replace("tel:+56 9 6588 9226", f"tel:{PHONE_E164}")
    return content


def ensure_canonical(content: str, path: Path) -> str:
    if 'rel="canonical"' in content:
        return content
    can = f'<link rel="canonical" href="{canonical_for(path)}">'
    # Try to insert after viewport meta if present, else before </head>
    if re.search(r'<meta\s+name="viewport"[^>]*>', content):
        return re.sub(
            r'(<meta\s+name="viewport"[^>]*>)',
            r"\1\n    " + can,
            content,
            count=1,
        )
    return insert_before_close_head(content, f"    {can}")


def ensure_og_twitter(content: str, path: Path) -> str:
    title = extract(content, r"<title>(.*?)</title>") or BRAND
    desc = extract(
        content,
        r'<meta\s+name="description"[^>]*content="([^"]+)"',
    ) or f"{BRAND}: destape de alcantarillado y limpieza de fosas sépticas en RM. Atención 24/7."
    title = html_unescape(title)
    desc = html_unescape(desc)
    canon = canonical_for(path)

    snippets: list[str] = []

    if 'property="og:title"' not in content:
        snippets.append(f'    <meta property="og:title" content="{title}">')
    if 'property="og:description"' not in content:
        snippets.append(f'    <meta property="og:description" content="{desc}">')
    if 'property="og:type"' not in content:
        snippets.append('    <meta property="og:type" content="website">')
    if 'property="og:url"' not in content:
        snippets.append(f'    <meta property="og:url" content="{canon}">')
    if 'property="og:image"' not in content:
        snippets.append(f'    <meta property="og:image" content="{DEFAULT_OG_IMAGE}">')
    if 'property="og:locale"' not in content:
        snippets.append('    <meta property="og:locale" content="es_CL">')
    if 'property="og:site_name"' not in content:
        snippets.append(f'    <meta property="og:site_name" content="{BRAND}">')

    if 'name="twitter:card"' not in content:
        snippets.append('    <meta name="twitter:card" content="summary_large_image">')
    if 'name="twitter:title"' not in content:
        snippets.append(f'    <meta name="twitter:title" content="{title}">')
    if 'name="twitter:description"' not in content:
        snippets.append(f'    <meta name="twitter:description" content="{desc}">')
    if 'name="twitter:image"' not in content:
        snippets.append(f'    <meta name="twitter:image" content="{DEFAULT_OG_IMAGE}">')

    if not snippets:
        return content
    return insert_before_close_head(content, "\n".join(snippets))


def existing_jsonld_types(content: str) -> set[str]:
    """Recolecta los @type ya presentes en bloques JSON-LD."""
    types: set[str] = set()
    for block in re.findall(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        content,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        try:
            data = json.loads(block.strip())
        except Exception:
            # JSON-LD no parseable; usar regex como fallback
            for t in re.findall(r'"@type"\s*:\s*"([^"]+)"', block):
                types.add(t)
            for t in re.findall(r'"@type"\s*:\s*\[([^\]]+)\]', block):
                for raw in t.split(","):
                    types.add(raw.strip().strip('"'))
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            t = item.get("@type")
            if isinstance(t, list):
                for x in t:
                    types.add(str(x))
            elif t:
                types.add(str(t))
    return types


def build_jsonld_for(path: Path, content: str) -> Optional[list[dict]]:
    existing = existing_jsonld_types(content)
    has_business = bool(existing & {"LocalBusiness", "Plumber", "Organization"})
    has_breadcrumb = "BreadcrumbList" in existing
    has_service = "Service" in existing
    has_blogposting = bool(existing & {"BlogPosting", "Article"})

    kind = classify(path)
    title = html_unescape(extract(content, r"<title>(.*?)</title>") or BRAND)
    desc = html_unescape(
        extract(content, r'<meta\s+name="description"[^>]*content="([^"]+)"') or ""
    )
    bc = breadcrumb_jsonld(path)

    blocks: list[dict] = []

    def add_business():
        if not has_business:
            blocks.append(base_business())

    def add_breadcrumb():
        if not has_breadcrumb:
            blocks.append(bc)

    if kind in ("static", "404", "casos", "servicios_index", "zonas_index"):
        add_business()
        add_breadcrumb()
        return blocks or None

    if kind == "servicio":
        slug = path.stem
        service_name = title.split("|")[0].strip().replace(" en Santiago", "").replace(" en RM", "")
        add_business()
        if not has_service:
            blocks.append(service_jsonld(
                service_name or slug.replace("-", " ").title(), desc))
        add_breadcrumb()
        return blocks or None

    if kind == "zona":
        slug = path.stem
        comuna = slug.replace("-", " ").title()
        if not has_business:
            blocks.append({
                **base_business(),
                "areaServed": [
                    {"@type": "AdministrativeArea",
                     "name": f"{comuna}, Región Metropolitana, Chile"}
                ],
            })
        if not has_service:
            blocks.append(service_jsonld(
                "Limpieza de fosas sépticas y destape de alcantarillado",
                desc or f"Servicio en {comuna}: limpieza de fosas, destape y mantención.",
                area=f"{comuna}, Región Metropolitana, Chile",
            ))
        add_breadcrumb()
        return blocks or None

    if kind == "blog_index":
        add_business()
        if "Blog" not in existing and "CollectionPage" not in existing:
            blocks.append({
                "@context": "https://schema.org",
                "@type": "Blog",
                "name": f"Blog de {BRAND}",
                "description": desc or "Consejos y guías sobre saneamiento, fosas y destapes.",
                "url": canonical_for(path),
                "publisher": {"@id": SITE_ID},
            })
        add_breadcrumb()
        return blocks or None

    if kind == "blog_post":
        add_business()
        if not has_blogposting:
            blocks.append(article_jsonld(path, title, desc))
        add_breadcrumb()
        return blocks or None

    if kind == "landing":
        slug = path.stem
        service_name = slug.replace("-", " ").title()
        add_business()
        if not has_service:
            blocks.append(service_jsonld(service_name, desc))
        add_breadcrumb()
        return blocks or None

    if kind == "home":
        add_breadcrumb()
        return blocks or None

    return None


def ensure_jsonld(content: str, path: Path) -> str:
    blocks = build_jsonld_for(path, content)
    if not blocks:
        return content
    payload = json.dumps(blocks, ensure_ascii=False, indent=2)
    snippet = (
        '    <script type="application/ld+json">\n'
        f'{payload}\n'
        '    </script>'
    )
    # Insert just before </head>
    return content.replace("</head>", f"{snippet}\n</head>", 1)


# ---------- main loop ----------

CHANGED: list[str] = []


def process(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    new = raw
    new = normalize_domain_and_phone(new)
    new = ensure_canonical(new, path)
    new = ensure_og_twitter(new, path)
    new = ensure_jsonld(new, path)
    if new != raw:
        if not DRY_RUN:
            path.write_text(new, encoding="utf-8")
        CHANGED.append(str(path.relative_to(ROOT)))
        return True
    return False


def main() -> None:
    if not PUBLIC.is_dir():
        sys.exit(f"public/ not found at {PUBLIC}")
    files = sorted(PUBLIC.rglob("*.html"))
    for f in files:
        if f.name == "test.html":
            continue
        process(f)
    print(f"{'[dry-run] ' if DRY_RUN else ''}archivos modificados: {len(CHANGED)}")
    for c in CHANGED:
        print(f"  - {c}")


if __name__ == "__main__":
    main()
