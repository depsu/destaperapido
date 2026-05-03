---
name: seo-core-web-vitals
description: Audita y corrige Core Web Vitals (LCP, INP, CLS) y otros aspectos de performance que impactan SEO. Usa Lighthouse / Unlighthouse y propone correcciones concretas (preload, lazy, dimensiones de imagen, defer scripts).
---

# Skill — Core Web Vitals

## Cuándo usar

- "Optimiza el rendimiento de la home / la página X."
- Después de un cambio grande de UI.
- Mensual, como mantenimiento.
- Cuando GSC reporta URLs con CWV "deficientes" en el reporte de "Experiencia en la página".

## Métricas que importan (2026)

| Métrica | Bueno | A mejorar | Pobre |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5–4s | > 4s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200–500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1–0.25 | > 0.25 |

INP reemplazó a FID en marzo 2024. Mide la respuesta del JS al input del usuario.

Otros indicadores útiles (no son CWV oficiales pero sí los lee Lighthouse):
- **FCP** (First Contentful Paint) ≤ 1.8s
- **TTFB** (Time to First Byte) ≤ 0.6s
- **TBT** (Total Blocking Time) ≤ 200ms

## Proceso

### 1. Medir baseline

```bash
# Página específica
pnpm dlx lighthouse https://www.limpiafosasydestape.cl --view

# Todo el sitio (mejor)
pnpm dlx unlighthouse --site https://www.limpiafosasydestape.cl
```

Si quieres datos reales de usuarios (no laboratorio):
- GSC → "Experiencia en la página" / "Core Web Vitals" muestra datos del campo (CrUX).
- PageSpeed Insights muestra ambos (campo + lab).

### 2. Identificar el cuello de botella

#### LCP alto
**Sospechosos:**
- Imagen hero pesada (`.jpg`/`.png` en lugar de `.webp`, sin compresión).
- Imagen hero sin `fetchpriority="high"` y/o con `loading="lazy"` por error.
- CSS bloqueante grande (Tailwind sin purge → `output.css` de varios cientos de KB).
- Servidor lento (TTFB alto). En Vercel suele estar bien — si es alto puede ser un endpoint serverless mal configurado.
- Web Font remoto sin `font-display: swap`.

**Correcciones:**
- Convertir hero a `.webp` o `.avif`. Tamaño ideal < 80 KB.
- `<img src="hero.webp" fetchpriority="high" decoding="async" width="1200" height="630">`
- Preload del hero: `<link rel="preload" as="image" href="/images/hero.webp">`
- Inline critical CSS si es posible. Diferir lo demás con `media="print" onload="this.media='all'"`.
- Self-hostear fuentes con `font-display: swap`.

#### INP alto
**Sospechosos:**
- Listeners de scroll/resize/click sin throttle/debounce.
- Bibliotecas JS pesadas (jQuery, sliders) corriendo al cargar.
- Long tasks > 50ms en main thread.

**Correcciones:**
- Defer scripts no críticos: `<script src="..." defer></script>`.
- Mover lógica pesada a `requestIdleCallback` o web workers.
- Quitar bibliotecas no usadas.
- Para sitios estáticos, idealmente cero JS bloqueante en el head.

#### CLS alto
**Sospechosos:**
- Imágenes sin `width`/`height` declarados.
- Fonts cargando tarde y empujando contenido.
- Banners que aparecen después del paint y mueven el layout (cookies, popups).
- Anuncios o iframes sin reserva de espacio.

**Correcciones:**
- TODA `<img>` con `width` y `height` explícitos (HTML attribute, no CSS).
- `<link rel="preload" as="font" ...>` para fonts críticas.
- Cookie banner que aparezca con position:fixed sin empujar contenido.
- Si hay placeholder, usar mismo tamaño que el contenido final.

### 3. Checklist específico para este proyecto (Full Fosas)

- [ ] `output.css` minificado y servido con cache headers largos. Verificar que no haya Tailwind CDN (la memoria del repo dice que se quitó).
- [ ] Hero del index con `fetchpriority="high"` y sin lazy.
- [ ] Logo `.webp` con dimensiones declaradas.
- [ ] Imágenes en `public/images/` todas en `.webp`. Si quedan `.jpg`/`.png`, convertir.
- [ ] Sin Tailwind CSS conflict (memoria menciona que se corrigió un conflicto lazy/fetchpriority en heros).
- [ ] Widget de WhatsApp (`whatsapp-widget.js`): cargar con `defer`, no bloquear.
- [ ] `availability-badge.js`: igual, con `defer`.
- [ ] `<head>` sin scripts `<script>` síncronos pesados.
- [ ] CSP configurado pero sin restringir recursos críticos.
- [ ] Vercel sirve los HTML con `Cache-Control` razonable.

### 4. Optimizaciones de imagen masivas

```bash
# Convertir todos los JPG/PNG no críticos a webp (Q=82 por defecto)
pnpm dlx sharp-cli -i "public/images/**/*.{jpg,png}" -f webp -o public/images/

# Optimizar SVGs
pnpm dlx svgo -f public/images/

# Generar versiones AVIF (más nuevo, mejor compresión)
pnpm dlx sharp-cli -i "public/images/hero/*.webp" -f avif -o public/images/hero/
```

### 5. Verificar después

```bash
pnpm dlx lighthouse http://localhost:3000 --view
```

Comparar baseline vs después. Documentar en commit message:

```
perf: optimizar LCP del hero (3.2s → 1.8s)

- Convertir hero.jpg a hero.webp (480 KB → 78 KB)
- Agregar preload del hero
- fetchpriority=high
```

## Reportar

```
## Auditoría CWV — public/index.html (laboratorio)

### Antes
- LCP: 3.4s ❌
- INP: 180ms ✅
- CLS: 0.18 ⚠️
- Score Lighthouse Performance: 72

### Causas detectadas
1. Hero `images/hero.jpg` (520 KB) sin webp ni preload
2. Logo PNG en lugar de webp
3. `<img>` sin width/height en 6 lugares (banner servicios)
4. Tailwind output.css de 280 KB (no purgado)

### Plan de corrección
1. [Crítico] Convertir hero a webp + preload + fetchpriority
2. [Crítico] Agregar width/height a todas las <img>
3. [Importante] Verificar tailwind.config content[] (debería purgar)
4. [Menor] Convertir logo a webp

¿Aplico las correcciones críticas?
```

## Anti-patrones

- Optimizar solo en ambiente local — los datos reales de campo (CrUX) son lo que cuenta.
- Confiar en una sola medición — corre Lighthouse 3-5 veces y usa la mediana.
- Atacar score de Lighthouse a costa de UX (ej: deshabilitar todo el JS).
- Lazy-load del hero (rompe LCP).
- Cambiar `output.css` minificado a mano.
