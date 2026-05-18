#!/usr/bin/env python3
"""
Extrae los testimonios visibles de testimonios.html y agrega Review schema
al LocalBusiness/Plumber existente, junto al aggregateRating ya presente.
Idempotente.
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

PUBLIC = Path(__file__).resolve().parent.parent / "public"
PAGE = PUBLIC / "testimonios.html"

def extract_testimonials():
    soup = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")
    seen = set()
    out = []
    for h4 in soup.find_all("h4"):
        card = h4
        for _ in range(8):
            card = card.find_parent()
            if not card:
                break
            stars = card.select(".fa-star")
            p = card.find("p", class_=lambda c: c and "italic" in c)
            if len(stars) >= 5 and p:
                quote = p.get_text(" ", strip=True).strip('"').strip()
                author = h4.get_text(" ", strip=True)
                role_p = h4.find_next("p")
                role = role_p.get_text(" ", strip=True) if role_p else ""
                if quote in seen:
                    break
                seen.add(quote)
                out.append({"author": author, "location": role, "quote": quote})
                break
    return out

def main():
    text = PAGE.read_text(encoding="utf-8")
    if '"@type": "Review"' in text or '"@type":"Review"' in text:
        print("ya tiene Review schema, salto")
        return

    testimonials = extract_testimonials()
    if not testimonials:
        print("!! sin testimonios extraídos")
        return

    # Encontrar el primer bloque application/ld+json y parsearlo
    m = re.search(r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)', text)
    if not m:
        print("!! sin script ld+json")
        return
    head, body, tail = m.groups()
    data = json.loads(body)
    if not isinstance(data, list):
        data = [data]

    # Buscar el LocalBusiness/Plumber para inyectarle review[]
    target = None
    for item in data:
        types = item.get("@type")
        if not types:
            continue
        types_list = types if isinstance(types, list) else [types]
        if any(t in ("LocalBusiness", "Plumber") for t in types_list):
            target = item
            break
    if target is None:
        print("!! sin LocalBusiness/Plumber")
        return

    reviews = []
    for t in testimonials:
        reviews.append({
            "@type": "Review",
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": "5",
                "bestRating": "5",
                "worstRating": "1"
            },
            "author": {"@type": "Person", "name": t["author"]},
            "reviewBody": t["quote"],
            **({"locationCreated": t["location"]} if t["location"] else {})
        })
    target["review"] = reviews

    new_body = json.dumps(data, ensure_ascii=False, indent=2)
    new_block = head + "\n" + new_body + "\n" + tail
    new_text = text.replace(m.group(0), new_block, 1)
    PAGE.write_text(new_text, encoding="utf-8")
    print(f"+ {len(reviews)} reviews inyectados en testimonios.html")

if __name__ == "__main__":
    main()
