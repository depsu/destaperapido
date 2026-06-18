#!/usr/bin/env python3
"""
Agrega el contenedor GTM-PG2RQNCD a las páginas de public/ que no lo tienen.
Inserta el snippet <head> (justo tras <head>) y el <noscript> (justo tras <body>),
idénticos a los del resto del sitio. Idempotente: salta las que ya tienen GTM.

Uso:
    python3 scripts/fix_add_gtm.py --dry-run
    python3 scripts/fix_add_gtm.py
"""
import argparse
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')
CONTAINER = 'GTM-PG2RQNCD'

HEAD_SNIPPET = """
    <!-- Google Tag Manager -->
    <script>(function(w, d, s, l, i){
    function _loadGTM(){
      w[l] = w[l] || []; w[l].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
      var f = d.getElementsByTagName(s)[0], j = d.createElement(s),
          dl = l != 'dataLayer' ? '&l=' + l : '';
      j.async = true;
      j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
      f.parentNode.insertBefore(j, f);
    }
    function _schedule(){
      if ('requestIdleCallback' in w) {
        requestIdleCallback(_loadGTM, { timeout: 3000 });
      } else {
        setTimeout(_loadGTM, 1500);
      }
    }
    if (d.readyState === 'complete') { _schedule(); }
    else { w.addEventListener('load', _schedule, { once: true }); }
})(window, document, 'script', 'dataLayer', 'GTM-PG2RQNCD');</script>
    <!-- End Google Tag Manager -->"""

NOSCRIPT_SNIPPET = """
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PG2RQNCD" height="0" width="0"
            style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->"""

head_re = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
body_re = re.compile(r'(<body[^>]*>)', re.IGNORECASE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    fixed, skipped, failed = 0, 0, 0
    for dirpath, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, encoding='utf-8') as f:
                html = f.read()
            rel = os.path.relpath(path, ROOT)
            if CONTAINER in html:
                skipped += 1
                continue
            if not head_re.search(html) or not body_re.search(html):
                print(f'   ⚠ {rel}: no encontré <head> o <body>, lo dejo igual')
                failed += 1
                continue
            new = head_re.sub(r'\1' + HEAD_SNIPPET, html, count=1)
            new = body_re.sub(r'\1' + NOSCRIPT_SNIPPET, new, count=1)
            if args.dry_run:
                print(f'   [DRY-RUN] Agregaría GTM a {rel}')
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new)
                print(f'   ✓ GTM agregado a {rel}')
            fixed += 1

    print(f'\n{"[dry-run] " if args.dry_run else ""}fixed: {fixed} · ya tenían: {skipped} · sin <head>/<body>: {failed}')


if __name__ == '__main__':
    main()
