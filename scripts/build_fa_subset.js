#!/usr/bin/env node
/**
 * Genera webfonts woff2 con solo los iconos Font Awesome usados.
 *
 * Lee scripts/fa-icons.json (producido por extract_fa_icons.py) y escribe
 * los archivos a public/fonts/webfonts/, sobrescribiendo el set completo.
 */
const path = require("path");
const fs = require("fs");
const { fontawesomeSubset } = require("fontawesome-subset");

const ROOT = path.resolve(__dirname, "..");
const ICONS_FILE = path.join(ROOT, "scripts", "fa-icons.json");
const OUT_DIR = path.join(ROOT, "public", "fonts", "webfonts");

async function main() {
  const icons = JSON.parse(fs.readFileSync(ICONS_FILE, "utf8"));

  // fontawesome-subset solo soporta woff2 a partir de v4
  const subset = {
    solid: icons.solid || [],
    brands: icons.brands || [],
    regular: icons.regular || [],
  };

  // Tamaños antes
  const before = ["fa-solid-900.woff2", "fa-brands-400.woff2", "fa-regular-400.woff2"]
    .map(name => ({ name, size: safeSize(path.join(OUT_DIR, name)) }));

  console.log("Antes:");
  before.forEach(b => console.log(`  ${b.name}: ${(b.size/1024).toFixed(1)} KB`));

  await fontawesomeSubset(subset, OUT_DIR, { targetFormats: ["woff2"] });

  console.log("\nDespués:");
  ["fa-solid-900.woff2", "fa-brands-400.woff2", "fa-regular-400.woff2"]
    .forEach(name => {
      const size = safeSize(path.join(OUT_DIR, name));
      console.log(`  ${name}: ${(size/1024).toFixed(1)} KB`);
    });

  console.log("\nIconos incluidos:");
  console.log(`  solid: ${subset.solid.length}`);
  console.log(`  brands: ${subset.brands.length}`);
  console.log(`  regular: ${subset.regular.length}`);
}

function safeSize(p) {
  try { return fs.statSync(p).size; } catch { return 0; }
}

main().catch(err => {
  console.error("Error:", err);
  process.exit(1);
});
