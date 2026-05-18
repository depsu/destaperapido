# Bitácora de Mejoras — 18 mayo 2026

Registro cronológico de las mejoras de SEO, performance, accesibilidad y UX
aplicadas sobre destaperapido.cl en esta tanda. Documenta el problema
detectado, la solución, los archivos tocados y cómo verificarlo en
producción.

---

## 1. Restaurar @font-face de Font Awesome (FIX CRÍTICO)

**Síntoma:** iconos invisibles en todo el sitio. Se veían cuadrados vacíos en
el header (phone, hamburger), CTAs ("Llamar", "WhatsApp"), badges, cards de
zona urbana/rural, chevrons, etc.

**Causa raíz:** el script de subset previo (`subset_fa_css.js`) generó las
fuentes `.woff2` correctamente pero eliminó los bloques `@font-face` del
CSS. El navegador veía `font-family: "Font Awesome 7 Free"` sin saber dónde
cargarla → glyphs vacíos.

**Fix:** `scripts/restore_fa_fontface.mjs` reinyecta los 10 `@font-face`
del paquete original `@fortawesome/fontawesome-free` apuntando a
`/fonts/webfonts/fa-*.woff2`. CSS pasa de 12.7KB → 14.8KB.

**Verificación:**
```
curl https://www.destaperapido.cl/fonts/fontawesome/all.min.css | grep '@font-face'
```
Debe devolver 10 bloques.

---

## 2. Eliminar FOUC (Flash of Unstyled Content) globalmente

**Síntoma:** al cargar cualquier página "bailaba todo" durante unos
milisegundos: el contenido aparecía con estilos parciales y luego saltaba
cuando llegaba el CSS completo.

**Causa raíz:** estrategia de critical CSS inline + carga async de
`output.css` con `media="print" onload="this.media='all'"`. El critical CSS
extraído por la herramienta `critical` no cubría TODAS las utilidades
Tailwind del above-the-fold (esto es esperable para sitios con muchas
variantes responsive). Resultado: render parcial con critical → segundo
render con output.css completo → CLS visible.

**Fix:** `scripts/revert_async_css.py` revierte 107 archivos a carga
bloqueante normal:
```html
<!-- Antes (FOUC) -->
<link rel="preload" as="style" href="/output.css">
<link rel="stylesheet" href="/output.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="/output.css"></noscript>

<!-- Después (sin FOUC) -->
<link rel="stylesheet" href="/output.css">
```

También se eliminó el `<style>` con ~22KB de critical CSS inline en
`index.html`, redundante con la carga bloqueante.

**Tradeoff:** +50ms en first paint, pero render limpio sin saltos. Mejor UX
percibida. El LCP real se ve favorecido porque ya no hay reflow.

---

## 3. Eliminar hover:grayscale en todo el sitio (mobile-first)

**Síntoma:** secciones con iconos/logos aparecían en escala de grises con
opacidad reducida hasta que el usuario pasaba el mouse encima. En mobile
(donde no hay hover) la imagen quedaba para siempre apagada.

**Casos afectados:**
- Bloque "Garantía Total / Servicio 24/7 / Flota Propia / Precios Claros"
  en home.
- Sección "Empresas que confían en nosotros" en 22 páginas piloto
  (zonas/urbano + zonas/rural + empresas + servicios).
- Imágenes de equipo/flota en zonas rurales (Pirque, Lampa, Buin-Paine, etc.).

**Fix:** `scripts/remove_hover_grayscale.py` elimina los tokens
`grayscale opacity-70 hover:grayscale-0 hover:opacity-100 transition-all
duration-500` y variantes en 22 archivos / 60 atributos `class`.

**Resultado:** todas las imágenes y logos se muestran en color desde el
primer paint, llamativos y útiles para conversión en mobile.

---

## 4. Validación en producción

Antes de empujar, los cambios pasaron por:
1. Build prod (`pnpm run build`).
2. `npx serve ./public` + Playwright headless con capturas mobile (412×915) y
   desktop (1440×900) en 9 páginas piloto + 4 control.
3. Inspección visual de iconos via `scripts/check_icons_prod.mjs`
   (`document.fonts` API + screenshots).
4. `curl -sI` contra producción para validar headers de seguridad, status,
   sitemaps segmentados y deploy efectivo.

**Carpeta de capturas (ignorada en git):**
`mejoras-destaperapido/capturas-icons-prod/`

---

## 5. Próximos pasos (sesión siguiente, una vez validado en GSC)

Sin orden estricto:
- **Performance — alternativa al critical CSS**: investigar lazy-load de
  fuentes Plus Jakarta Sans con `font-display: optional` y subset.
- **SEO técnico**:
  - `BlogPosting` schema en los 35 posts del blog.
  - `Service` schema en `/servicios/*.html`.
  - `HowTo` schema en posts tutoriales (cómo destapar, qué hacer si...).
  - Related posts al final de cada post.
  - Anchor links contextuales hacia páginas de zona y servicio.
  - Geo meta tags en zonas urbanas y rurales que aún no las tienen.
- **UX / Conversión**:
  - Revisar nav desktop: actualmente apretado (8 enlaces sin gap suficiente).
  - Generar variantes `og-<comuna>.jpg` reales (hoy se usa `og.jpg`
    genérico como fallback).
  - `width`/`height` en todas las imágenes del sitio para CLS = 0.
- **Mantenimiento**:
  - Lighthouse mobile sobre las 9 piloto y comparar con baseline mayo 2026.
  - Rich Results Test en home, precios y una zona — validar FAQPage,
    LocalBusiness, BreadcrumbList.
  - Search Console: re-enviar sitemap-index y solicitar indexación manual
    de las 12 URLs nuevas (4 páginas + 8 posts).
