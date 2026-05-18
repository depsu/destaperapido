#!/usr/bin/env python3
"""
Inyecta BreadcrumbList schema en blog posts que aún no lo tienen,
construyendo la breadcrumb desde el canonical y el h1.
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

PUBLIC = Path(__file__).resolve().parent.parent / "public"
BLOG = PUBLIC / "blog"

def main():
    added = 0
    for f in sorted(BLOG.glob("*.html")):
        if f.name == "index.html":
            continue
        text = f.read_text(encoding="utf-8")
        if "BreadcrumbList" in text:
            continue

        soup = BeautifulSoup(text, "html.parser")
        canonical = (soup.find("link", rel="canonical") or {}).get("href") if soup.find("link", rel="canonical") else None
        h1 = soup.find("h1")
        title = h1.get_text(" ", strip=True) if h1 else None
        if not canonical or not title:
            print(f"!! salto (sin canonical/h1): {f.name}")
            continue

        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.destaperapido.cl/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.destaperapido.cl/blog"},
                {"@type": "ListItem", "position": 3, "name": title, "item": canonical}
            ]
        }
        snippet = (
            '\n    <script type="application/ld+json">\n'
            + json.dumps(breadcrumb, ensure_ascii=False, indent=2)
            + '\n    </script>\n'
        )
        idx = text.rfind("</head>")
        if idx < 0:
            continue
        new_text = text[:idx] + snippet + text[idx:]
        f.write_text(new_text, encoding="utf-8")
        added += 1
        print(f"+ Breadcrumb: {f.name}")

    print(f"\nTotal agregados: {added}")

if __name__ == "__main__":
    main()
