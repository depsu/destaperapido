---
name: seo-sitemap-robots
description: Mantiene sitemap.xml y robots.txt consistentes con el estado real del sitio. Detecta páginas faltantes en el sitemap, URLs muertas, lastmod desactualizados y reglas robots problemáticas.
---

# Skill — Sitemap.xml y robots.txt

## Cuándo usar

- Después de agregar/borrar/renombrar páginas.
- Antes de cada deploy importante.
- Mensual, como mantenimiento.
- "Verifica que el sitemap esté al día."

## Sitemap.xml

### Reglas

1. **Solo URLs canónicas** — con `https://www.` consistente con el canonical de cada página.
2. **Solo URLs indexables** — no páginas con `noindex` ni redirecciones.
3. **`<lastmod>` real** (ISO 8601) — no fechas inventadas. Si no sabes la fecha del último cambio significativo, usa la del último commit del archivo.
4. **`<priority>` y `<changefreq>` opcionales** — Google los ignora prácticamente. No vale la pena pelear con ellos.
5. **Máx 50.000 URLs** y **50 MB** descomprimido por sitemap. Para sitios chicos no es problema.
6. **Codificar caracteres especiales** en URLs (espacios → `%20`, etc.).
7. **Validar XML** — un solo `&` sin escapar rompe el sitemap completo.

### Proceso de auditoría

#### a) Listar URLs reales del sitio

```bash
find public -name "*.html" -not -path "*/node_modules/*" \
  | sed 's|^public|https://www.limpiafosasydestape.cl|' \
  | sed 's|/index\.html$|/|' \
  | sort > /tmp/urls-reales.txt
```

#### b) Listar URLs en sitemap.xml

```bash
grep -oE '<loc>[^<]+</loc>' public/sitemap.xml \
  | sed 's|<loc>||;s|</loc>||' \
  | sort > /tmp/urls-sitemap.txt
```

#### c) Comparar

```bash
# URLs en disco pero NO en sitemap (faltantes)
comm -23 /tmp/urls-reales.txt /tmp/urls-sitemap.txt

# URLs en sitemap pero NO en disco (zombies)
comm -13 /tmp/urls-reales.txt /tmp/urls-sitemap.txt
```

#### d) Validar XML

```bash
xmllint --noout public/sitemap.xml && echo "OK"
# o
pnpm dlx sitemap-validator public/sitemap.xml
```

### Estructura mínima

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.limpiafosasydestape.cl/</loc>
    <lastmod>2026-05-02</lastmod>
  </url>
  <url>
    <loc>https://www.limpiafosasydestape.cl/zonas/rural/colina.html</loc>
    <lastmod>2026-04-29</lastmod>
  </url>
  ...
</urlset>
```

### Subcasos

**Páginas que NO deben estar en sitemap:**
- 404.html
- Páginas con `noindex`
- Páginas duplicadas que apuntan a otra como canonical
- Landings privadas / de prueba

**Lastmod inteligente:**
- No actualices `<lastmod>` por cambios cosméticos (estilo, typo).
- Sí actualízalo si cambias title, meta, h1, JSON-LD, o el cuerpo de manera relevante.
- Tip: usa `git log -1 --format=%ai -- public/zonas/rural/colina.html` para obtener fecha exacta del último commit que tocó esa página.

### Sitemap index (cuando hay > 50k URLs o > 50MB)

Para este proyecto NO aplica todavía (es un sitio chico). Si en el futuro crece:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.limpiafosasydestape.cl/sitemap-zonas.xml</loc>
    <lastmod>2026-05-02</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.limpiafosasydestape.cl/sitemap-servicios.xml</loc>
    <lastmod>2026-05-02</lastmod>
  </sitemap>
  ...
</sitemapindex>
```

---

## robots.txt

### Estructura recomendada

```txt
User-agent: *
Allow: /

# Endpoints serverless
Disallow: /api/

# Archivos internos sin valor SEO
Disallow: /404.html

Sitemap: https://www.limpiafosasydestape.cl/sitemap.xml
```

### Reglas

1. **Allow: /** explícito por claridad.
2. **Bloquear** `/api/` (serverless functions de Vercel).
3. **Bloquear** assets de build si por error quedan accesibles (`/node_modules/`, `/.git/`, etc. — generalmente no se sirven, pero por las dudas).
4. **NO bloquear** `output.css` ni `*.js` críticos — Google necesita renderizar.
5. **NO bloquear** `images/` — perdería rich snippets visuales y Google Images.
6. **Sitemap** declarado al final, URL absoluta.
7. **Una sola directiva `User-agent`** general suele ser suficiente.

### Anti-patrones frecuentes

- `Disallow: /` por accidente (deindexea todo el sitio). Cuidado al editar.
- Bloquear CSS o JS — Google Mobile-Friendly Test falla y la página puede caer en posiciones.
- `Crawl-delay: 10` — Google ignora la directiva, otros bots la respetan a costa de menor cobertura. Evitar.
- Agregar bots específicos sin razón clara (permitir GoogleBot pero negar BingBot por ejemplo).

---

## Después de cambios

1. **Subir a producción** (deploy).
2. **GSC → Sitemaps** → enviar `https://www.limpiafosasydestape.cl/sitemap.xml`.
3. **Verificar fetch del robots:**
   ```
   curl -s https://www.limpiafosasydestape.cl/robots.txt
   ```
4. **Inspeccionar URL** de páginas críticas en GSC para confirmar que están "Indexable" sin warnings.

## Reportar

```
## Estado del sitemap

### URLs reales: 87
### URLs en sitemap.xml: 84
### Faltantes (3):
  - https://www.limpiafosasydestape.cl/zonas/rural/calera-de-tango.html
  - https://www.limpiafosasydestape.cl/blog/destape-grasa-cocina.html
  - https://www.limpiafosasydestape.cl/casos-reales/colina-condominio-2025.html

### Zombies en sitemap (1):
  - https://www.limpiafosasydestape.cl/landing/oferta-marzo-2024.html  (archivo no existe)

### Lastmod desactualizados (>180 días sin tocar): 12 URLs
```

Termina con: "¿Sincronizo el sitemap.xml con el estado real del disco?".
