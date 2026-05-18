#!/usr/bin/env python3
"""
Para cada blog post sin FAQPage schema, genera uno mínimo (1 pregunta) usando
el H1 como pregunta y el primer párrafo significativo del artículo como
respuesta. Idempotente.
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

PUBLIC = Path(__file__).resolve().parent.parent / "public"
BLOG = PUBLIC / "blog"

SKIP = {"index.html"}  # el índice no es un artículo

def first_meaningful_paragraph(soup):
    main = soup.find("main") or soup.find("article") or soup
    for p in main.find_all("p"):
        text = p.get_text(" ", strip=True)
        if len(text) >= 80 and len(text) <= 600:
            return text
    return None

def title_as_question(h1_text):
    t = (h1_text or "").strip().rstrip(":.,;")
    if not t:
        return None
    if t.endswith("?"):
        return t
    if t.startswith("¿"):
        return t + "?"
    # Heurística simple: si empieza con verbo / "cómo" / "por qué"
    lower = t.lower()
    if lower.startswith(("cómo", "como", "por qué", "porque", "cuándo", "cuando", "qué", "que", "cuánto", "cuanto")):
        return "¿" + t + "?"
    return t  # Statement: lo dejamos sin "?" (no calza FAQ, mejor saltar)

def faq_schema(question, answer):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": answer}
        }]
    }

def main():
    added = 0
    skipped_no_h1 = 0
    skipped_no_p = 0
    skipped_not_question = 0
    for f in sorted(BLOG.glob("*.html")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        if "FAQPage" in text:
            continue

        soup = BeautifulSoup(text, "html.parser")
        h1 = soup.find("h1")
        if not h1:
            skipped_no_h1 += 1
            print(f"!! sin h1: {f.name}")
            continue

        question = title_as_question(h1.get_text(" ", strip=True))
        if not question or "?" not in question:
            skipped_not_question += 1
            print(f"~  H1 no-pregunta, salto schema FAQ: {f.name}")
            continue

        answer = first_meaningful_paragraph(soup)
        if not answer:
            skipped_no_p += 1
            print(f"!! sin párrafo apto: {f.name}")
            continue

        schema = faq_schema(question, answer)
        snippet = (
            '\n    <script type="application/ld+json">\n'
            + json.dumps(schema, ensure_ascii=False, indent=2)
            + '\n    </script>\n'
        )
        idx = text.rfind("</head>")
        if idx < 0:
            continue
        new_text = text[:idx] + snippet + text[idx:]
        f.write_text(new_text, encoding="utf-8")
        added += 1
        print(f"+ FAQ blog: {f.name}")

    print(f"\n+ {added} agregados | sin h1: {skipped_no_h1} | sin párrafo: {skipped_no_p} | h1 no pregunta: {skipped_not_question}")

if __name__ == "__main__":
    main()
