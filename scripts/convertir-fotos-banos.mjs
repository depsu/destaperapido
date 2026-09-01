// Convierte las fotos de marketing (PNG 1024x1536) a WebP 4:5 para la web + OG 1200x630.
import sharp from "sharp";
import { existsSync } from "node:fs";
const SRC = "marketing/fotos-banos";
const OUT = "public/images/banos-quimicos";
const fotos = [
  ["fiestas-patrias/bano-patio-quincho-18.png", "bano-quimico-18-septiembre-patio-quincho", true],
  ["fiestas-patrias/bano-patio-dieciochero.png", "bano-quimico-fiestas-patrias-patio-dieciochero", true],
  ["interior/interior-puerta-abierta.png", "bano-quimico-interior-limpio-con-papel", false],
  ["galpon/bano-lavamanos-combo.png", "bano-quimico-con-lavamanos-portatil", false],
  ["parcela/bano-parcela-atardecer.png", "bano-quimico-asado-en-parcela", false],
  ["galpon/camion-entrega-bano.png", "camion-entrega-bano-quimico-santiago", false],
  ["galpon/fila-banos-galpon-cielo.png", "flota-banos-quimicos-santiago", true],
  ["galpon/bano-solo-frontal.png", "bano-quimico-modelo-estandar-frontal", false],
  ["evento/bano-cumpleanos-jardin.png", "bano-quimico-kermesse-fiesta-jardin", true],
  ["evento/bano-jardin-evento.png", "bano-quimico-evento-jardin", false],
  ["colegio/bano-patio-colegio-pena.png", "bano-quimico-patio-colegio-pena", true],
  ["fonda/bano-fonda-ramada.png", "bano-quimico-fonda-ramada", true],
  ["galpon/lavamanos-detalle.png", "lavamanos-portatil-detalle", false],
  ["galpon/fila-banos-galpon-vertical.png", "fila-banos-quimicos-galpon", false],
];
for (const [rel, name, og] of fotos) {
  const inp = `${SRC}/${rel}`;
  if (!existsSync(inp)) { console.log("falta", inp); continue; }
  const img = sharp(inp);
  const meta = await img.metadata();
  // recorte 4:5 centrado
  const w = meta.width, h = meta.height;
  const targetH = Math.round(w * 5 / 4);
  const top = Math.max(0, Math.round((h - targetH) / 2));
  await sharp(inp).extract({ left: 0, top, width: w, height: Math.min(targetH, h) })
    .resize(800, 1000).webp({ quality: 78 }).toFile(`${OUT}/${name}.webp`);
  await sharp(inp).extract({ left: 0, top, width: w, height: Math.min(targetH, h) })
    .resize(400, 500).webp({ quality: 74 }).toFile(`${OUT}/${name}-400.webp`);
  if (og) {
    // OG 1200x630: banda central horizontal (el baño queda al centro)
    const bandH = Math.round(w * 630 / 1200);
    const topOg = Math.max(0, Math.round(h * 0.42 - bandH / 2));
    await sharp(inp).extract({ left: 0, top: topOg, width: w, height: bandH })
      .resize(1200, 630).jpeg({ quality: 82, mozjpeg: true }).toFile(`${OUT}/og-${name}.jpg`);
  }
  console.log("ok", name);
}
