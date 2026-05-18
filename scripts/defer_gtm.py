#!/usr/bin/env python3
"""Defer Google Tag Manager initialization until after window 'load' event.

Replaces the inline GTM snippet with a wrapped version that runs ~1.5s after the
load event (via requestIdleCallback fallback). This frees the main thread during
LCP/FCP without losing analytics.

Idempotent: only transforms if the original snippet pattern is present.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

ORIGINAL_RE = re.compile(
    r"<script>\s*\(function\s*\(\s*w\s*,\s*d\s*,\s*s\s*,\s*l\s*,\s*i\s*\)\s*\{[^<]*?GTM-[A-Z0-9]+'\)\s*;?\s*</script>",
    re.DOTALL,
)

# We replace with a self-contained deferred loader.
def deferred_snippet() -> str:
    return (
        "<script>(function(w, d, s, l, i){\n"
        "    function _loadGTM(){\n"
        "      w[l] = w[l] || []; w[l].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});\n"
        "      var f = d.getElementsByTagName(s)[0], j = d.createElement(s),\n"
        "          dl = l != 'dataLayer' ? '&l=' + l : '';\n"
        "      j.async = true;\n"
        "      j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;\n"
        "      f.parentNode.insertBefore(j, f);\n"
        "    }\n"
        "    function _schedule(){\n"
        "      if ('requestIdleCallback' in w) {\n"
        "        requestIdleCallback(_loadGTM, { timeout: 3000 });\n"
        "      } else {\n"
        "        setTimeout(_loadGTM, 1500);\n"
        "      }\n"
        "    }\n"
        "    if (d.readyState === 'complete') { _schedule(); }\n"
        "    else { w.addEventListener('load', _schedule, { once: true }); }\n"
        "})(window, document, 'script', 'dataLayer', 'GTM-PG2RQNCD');</script>"
    )


def transform(html: str) -> tuple[str, bool]:
    if "_loadGTM" in html:
        return html, False  # already deferred
    new_html, n = ORIGINAL_RE.subn(deferred_snippet(), html, count=1)
    return new_html, n > 0


def main() -> int:
    changed = 0
    skipped = 0
    for html_file in PUBLIC.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        new_text, ok = transform(text)
        if ok:
            html_file.write_text(new_text, encoding="utf-8")
            changed += 1
        else:
            skipped += 1
    print(f"Changed: {changed}  Skipped (already deferred or no GTM): {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
