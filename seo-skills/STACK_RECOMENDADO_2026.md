# Stack npm recomendado · SEO orgánico + pagado + mobile

> Curado para **destaperapido.cl** (HTML estático en Vercel, Tailwind, sin SSG).
> No instalar todo: empezá por el bloque "esencial" y sumá lo demás según
> donde duela (lo descubrís corriendo Lighthouse).

---

## Bloque 1 · Esencial (instalar AHORA con `pnpm`)

```bash
pnpm add -D lighthouse @lhci/cli html-validate linkinator unlighthouse
```

| Paquete | Qué hace | Cuándo correrlo |
|---|---|---|
| `lighthouse` | Audita 1 página: perf/SEO/a11y/PWA. | Pre-deploy de cambios grandes. |
| `unlighthouse` | Crawlea TODO el sitio en paralelo (60+ páginas tuyas). | 1× por mes. |
| `@lhci/cli` | Lighthouse en CI con presupuestos (LCP, TBT). | GitHub Actions en cada PR. |
| `html-validate` | Linter HTML estricto. | Pre-commit. |
| `linkinator` | Detecta links rotos. | Pre-deploy. |

```bash
# Audit completo del sitio en local
pnpm dlx unlighthouse --site http://localhost:3000

# Audit producción
pnpm dlx unlighthouse --site https://www.destaperapido.cl
```

---

## Bloque 2 · Optimización de imágenes (mobile LCP)

Tienes imágenes de 200-1300 KB sin variantes responsive. Cada una pesa de más en mobile.

```bash
pnpm add -D sharp svgo
```

| Paquete | Para qué |
|---|---|
| `sharp` | Generar variantes 480w / 768w / 1280w en webp/avif. Reducir 60-80% peso. |
| `svgo` | Optimizar SVG (logos, íconos). |

**Acción concreta**: la imagen LCP `camio-haciendo-servicio-en-la-calle.webp` (182KB) debería tener variante de 768px (~60KB) servida con `srcset`/`sizes` en mobile. Lo mismo para `mobile-Destape-alcantarillado-...webp` (1.3MB ‼).

---

## Bloque 3 · SEO técnico (estructura, schema, sitemap)

```bash
pnpm add -D structured-data-testing-tool sitemap-validator cheerio
```

| Paquete | Para qué |
|---|---|
| `structured-data-testing-tool` | Validar JSON-LD localmente (sin Rich Results Test online). |
| `sitemap-validator` | Confirmar que sitemap.xml cumple schema oficial. |
| `cheerio` | Para tus scripts en `scripts/` que parsean HTML (ya tenés varios). |

---

## Bloque 4 · Accesibilidad (impacta SEO indirectamente)

```bash
pnpm add -D pa11y pa11y-ci @axe-core/cli
```

```bash
# Audita todo el sitemap
pnpm dlx pa11y-ci --sitemap https://www.destaperapido.cl/sitemap.xml
```

Google usa señales de UX (Core Web Vitals + a11y básica) como ranking factor. `pa11y` te dice si el contraste, los `alt`, los aria-labels o el orden de tab están mal.

---

## Bloque 5 · Mobile UX testing

```bash
pnpm add -D playwright
```

Permite simular mobile reales (iPhone 13, Galaxy S22) y testear conversión:
```js
// scripts/mobile-test.js
import { test, devices } from '@playwright/test';
test.use(devices['iPhone 13']);
test('CTA WhatsApp visible sin scroll en home', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('a[href*="wa.me"]').first()).toBeInViewport();
});
```

---

## Bloque 6 · SEO **pagado** (Google Ads)

> No son paquetes npm, son cambios que ya implementé hoy + lo que falta.

### Ya implementado en este commit
- `dataLayer.push({event:'click_whatsapp'})` y `click_tel` en cada click — **úsalo como conversión en Google Ads** vía GTM trigger custom event.
- `dataLayer.push({event:'lead_submit'})` en form contacto.
- WA con `?text=` contextual = mejor calidad de lead.
- Page speed (lazy imgs, parallax fixed quitado) → mejor **Quality Score** en Ads.

### Pendiente para Ads (manual, fuera de código)
1. **GTM**: crear triggers para `click_whatsapp`, `click_tel`, `lead_submit` y enlazarlos a tags de **Conversión Ads** + **GA4**.
2. **Google Ads conversion linker**: agregar tag `Conversion Linker` en GTM (gclid persistence).
3. **Phone call extensions**: en Ads, activar "call asset" con +56 9 2846 1485.
4. **Local Services Ads (LSA)**: revisar elegibilidad para "Plomeros - Santiago" — hace lead generation directo y ranquea sobre Ads tradicional.
5. **Landing pages dedicadas a Ads** (ya existen: `/landing/destape-urgente-sector-oriente`, etc.) — revisar que cada una matchee 1 ad group con keywords específicas.
6. **Bid modifier mobile +20%** si los datos muestran mejor CR mobile (lo más probable en este rubro).

---

## Bloque 7 · Performance avanzado (cuando duela)

```bash
pnpm add -D critical size-limit terser
```

| Paquete | Cuándo |
|---|---|
| `critical` | Inline del CSS crítico above-the-fold por página. Solo si Lighthouse marca "render-blocking CSS". |
| `size-limit` | Falla CI si Tailwind o JS supera presupuesto. |
| `terser` | Si en algún momento agregas bundle JS propio. |

---

## Workflow mensual sugerido

```bash
# 1. Construir CSS
pnpm run build

# 2. Validar HTML
pnpm dlx html-validate "public/**/*.html"

# 3. Detectar links rotos
pnpm dlx linkinator http://localhost:3000 --recurse

# 4. Audit performance/SEO global
pnpm dlx unlighthouse --site http://localhost:3000

# 5. A11y
pnpm dlx pa11y-ci --sitemap http://localhost:3000/sitemap.xml

# 6. JSON-LD
pnpm dlx structured-data-testing-tool --url https://www.destaperapido.cl
```

---

## Resumen de prioridades

1. **Hoy mismo (gratis)**: instalar bloque 1 + correr `unlighthouse` en local.
2. **Esta semana**: bloque 2 (responsive images) — es el cambio que más mejora LCP mobile.
3. **Este mes**: configurar conversiones en GTM (bloque 6) → arranca con datos para Ads.
4. **Trimestral**: pa11y + lighthouse-ci en CI/CD.
