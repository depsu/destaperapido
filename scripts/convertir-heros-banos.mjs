// Fondos horizontales del hero (Codex 1536x1024) → WebP 1600 px de ancho para escritorio.
import sharp from "sharp";
import { existsSync } from "node:fs";
const SRC = "marketing/fotos-banos/hero";
const OUT = "public/images/banos-quimicos";
for (const name of ["hero-18-patio-quincho", "hero-fonda-ramada", "hero-colegio-pena"]) {
  const inp = `${SRC}/${name}.png`;
  if (!existsSync(inp)) { console.log("falta", name); continue; }
  await sharp(inp).flop().resize({ width: 1600 }).webp({ quality: 74 }).toFile(`${OUT}/${name}-1600.webp`);
  console.log("ok", name);
}
