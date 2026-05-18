#!/usr/bin/env python3
"""Remove grayscale + hover:grayscale-0 patterns sitewide.

Mobile-first sites should show full color immediately. Hover-to-reveal-color
effects don't trigger on touch devices and make the site look "dull" by default,
which kills above-the-fold appeal.

Patterns removed:
- `grayscale opacity-70 hover:grayscale-0 hover:opacity-100 transition-all duration-500`
- `grayscale hover:grayscale-0 transition-all duration-500`
- `grayscale hover:grayscale-0 transition duration-700`
- And variants on `<img>` and container `<div>` elements.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# Tokens we always want to strip when found together with `grayscale`
GRAYSCALE_TOKENS = re.compile(
    r"\s+(?:"
    r"grayscale"
    r"|hover:grayscale-0"
    r"|opacity-70"
    r"|hover:opacity-100"
    r"|transition-all\s+duration-500"
    r"|transition\s+duration-700"
    r"|transition-all"
    r"|duration-500"
    r"|duration-700"
    r")\b"
)


def transform_class_value(class_value: str) -> str:
    """Strip grayscale-related tokens from a single class string."""
    if "grayscale" not in class_value:
        return class_value
    # Only strip transition/duration tokens if grayscale is also present
    # (to avoid removing legit transitions elsewhere)
    cleaned = " " + class_value + " "
    # remove the specific tokens
    cleaned = re.sub(
        r"\s+(grayscale|hover:grayscale-0|opacity-70|hover:opacity-100)\b",
        "",
        cleaned,
    )
    # also strip the matching transition+duration tokens that were tied to the effect
    cleaned = re.sub(r"\s+transition-all\s+duration-500\b", "", cleaned)
    cleaned = re.sub(r"\s+transition\s+duration-700\b", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


CLASS_ATTR_RE = re.compile(r'(\sclass=")([^"]*?grayscale[^"]*?)(")', re.DOTALL)


def transform(html: str) -> tuple[str, int]:
    n = 0

    def _sub(m):
        nonlocal n
        prefix, classes, suffix = m.group(1), m.group(2), m.group(3)
        new_classes = transform_class_value(classes)
        if new_classes != classes:
            n += 1
            return prefix + new_classes + suffix
        return m.group(0)

    new_html = CLASS_ATTR_RE.sub(_sub, html)
    return new_html, n


def main() -> int:
    changed = 0
    total_replacements = 0
    for html_file in PUBLIC.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        if "grayscale" not in text:
            continue
        new_text, n = transform(text)
        if n:
            html_file.write_text(new_text, encoding="utf-8")
            changed += 1
            total_replacements += n
            print(f"  ok  {html_file.relative_to(PUBLIC)}: {n} class atributos limpiados")
    print(f"\nArchivos modificados: {changed}  Atributos class limpiados: {total_replacements}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
