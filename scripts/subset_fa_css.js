#!/usr/bin/env node
/**
 * Genera un Font Awesome CSS subset usando PurgeCSS contra los HTML del sitio.
 * Conserva las reglas que efectivamente se usan (selectores .fa-...).
 *
 * Salida: public/fonts/fontawesome/all.min.css (sobrescribe el actual)
 */
const path = require("path");
const fs = require("fs");
const { PurgeCSS } = require("purgecss");

const ROOT = path.resolve(__dirname, "..");
const SOURCE_CSS = path.join(ROOT, "node_modules/@fortawesome/fontawesome-free/css/all.min.css");
const OUT_CSS = path.join(ROOT, "public/fonts/fontawesome/all.min.css");

async function main() {
  const beforeSize = fs.statSync(OUT_CSS).size;
  console.log(`Antes: ${(beforeSize/1024).toFixed(1)} KB`);

  const result = await new PurgeCSS().purge({
    content: [path.join(ROOT, "public/**/*.html")],
    css: [SOURCE_CSS],
    safelist: {
      // Conservar utilidades base que pueden activarse por JS o reglas
      // sin matching directo en HTML
      standard: [
        /^fa$/, /^fas$/, /^far$/, /^fab$/,
        /^fa-solid$/, /^fa-regular$/, /^fa-brands$/,
        /^sr-only$/, /^fa-sr-only$/, /^fa-fw$/,
        /^fa-spin/, /^fa-pulse/, /^fa-flip/, /^fa-rotate/,
        /^fa-stack/, /^fa-stack-1x$/, /^fa-stack-2x$/, /^fa-inverse$/,
        /^fa-xs$/, /^fa-sm$/, /^fa-lg$/, /^fa-2x$/, /^fa-3x$/, /^fa-4x$/, /^fa-5x$/,
        /^fa-li$/, /^fa-ul$/, /^fa-pull-/, /^fa-border$/,
        /^fa-beat/, /^fa-fade/, /^fa-shake/, /^fa-bounce/,
      ],
      // greedy: preserva selectores que CONTENGAN estos tokens
      greedy: [
        /:before/, /::before/, /^@font-face/, /^@keyframes/
      ],
      // Conservar variables CSS de FA
      variables: [
        /^--fa/
      ]
    },
    fontFace: true,
    keyframes: true,
    variables: true,
  });

  const purged = result[0].css;
  fs.writeFileSync(OUT_CSS, purged, "utf8");
  const afterSize = fs.statSync(OUT_CSS).size;
  console.log(`Después: ${(afterSize/1024).toFixed(1)} KB`);
  console.log(`Reducción: ${((1 - afterSize/beforeSize) * 100).toFixed(1)}%`);
}

main().catch(err => {
  console.error("Error:", err);
  process.exit(1);
});
