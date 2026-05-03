# Workflow — Crear una página nueva (zona, servicio o blog)

Checklist de extremo a extremo. Sigue los pasos en orden.

---

## 0. Antes de empezar — clarificar

- [ ] ¿Qué tipo de página? (zona / servicio / blog / landing)
- [ ] ¿Cuál es la **keyword principal**?
- [ ] ¿Cuál es el **ángulo único** que la justifica?
- [ ] ¿Qué páginas existentes son **vecinas semánticas** (deberán enlazar a esta y viceversa)?
- [ ] Slug definitivo (kebab-case, sin tildes).

Si falta cualquiera de estos, **pregunta antes de escribir HTML**.

---

## 1. Investigación (skill `seo-keywords-locales`)

- [ ] Listar 5-10 long-tail relacionadas.
- [ ] Buscar el SERP de la keyword principal — ver qué muestran los 3 primeros.
- [ ] Identificar gaps temáticos.
- [ ] Recopilar PAA y "búsquedas relacionadas".

**Output:** mini-documento con keyword principal + 5-10 secundarias + ángulo único.

---

## 2. Redactar (según tipo)

### Zona
- [ ] Skill: `seo-zona-nueva`.
- [ ] Template: `templates/zona-template.html`.
- [ ] Mínimo 800 palabras de contenido único.

### Servicio
- [ ] Skill: `seo-servicio-nuevo`.
- [ ] Template: `templates/servicio-template.html`.
- [ ] Mínimo 1000 palabras (700+ si es servicio secundario).

### Blog
- [ ] Skill: `seo-blog-articulo`.
- [ ] Mínimo 1200 palabras.

---

## 3. Meta y JSON-LD

- [ ] Skill `seo-meta-unicos` para validar title/description únicos (50-62 / 140-160 chars).
- [ ] Skill `seo-schema-jsonld` para construir bloques.
- [ ] OG/Twitter sincronizados con title/description.
- [ ] Imagen OG existe físicamente, < 300 KB, .webp.

---

## 4. Auditar on-page

- [ ] Skill `seo-audit-onpage` sobre el archivo recién creado.
- [ ] Resolver todos los puntos críticos.
- [ ] Resolver al menos 50% de los "mejorables".

---

## 5. Enlazado interno

- [ ] Skill `seo-enlazado-interno`.
- [ ] Insertar 3-6 enlaces salientes contextuales hacia páginas vecinas.
- [ ] Insertar **inbound links** desde 3-5 páginas existentes hacia la nueva.

Ejemplo concreto al crear `zonas/rural/penaflor.html`:
- Linkear desde `zonas/rural/talagante.html`, `zonas/rural/isla-de-maipo.html`, `zonas/rural/calera-de-tango.html` (vecinas).
- Linkear desde `zonas/rural/index.html` (listado).
- Linkear desde 1-2 servicios (`servicios/limpieza-fosas-septicas.html`).

---

## 6. Sitemap y navegación

- [ ] Skill `seo-sitemap-robots`.
- [ ] Agregar `<url>` con `<loc>` y `<lastmod>` a `public/sitemap.xml`.
- [ ] Si hay listado/menu de zonas, agregar la nueva entrada ahí.

---

## 7. Performance

- [ ] Skill `seo-core-web-vitals`.
- [ ] Imagen hero en `.webp`, con `width`, `height`, `fetchpriority="high"` y `<link rel="preload">`.
- [ ] Resto de imágenes con `loading="lazy"` y `decoding="async"`.

---

## 8. Build y commit

```bash
pnpm run build       # compila Tailwind
git add public/ seo-skills/
git commit -m "feat(seo): página nueva [zona/servicio/blog] — [slug]"
```

Mensaje de commit recomendado:
```
feat(seo): nueva página de zona Peñaflor (rural)

- 950 palabras, ángulo "parcelas y zona agrícola"
- JSON-LD: LocalBusiness + Service + Breadcrumb + FAQPage
- 5 inbound links agregados desde zonas vecinas
- Entrada en sitemap.xml con lastmod=2026-05-02
```

---

## 9. Deploy y validación post-deploy

- [ ] `vercel --prod`.
- [ ] Esperar ~1 min y verificar la URL en producción.
- [ ] **Rich Results Test:** copiar URL en `https://search.google.com/test/rich-results`. Cero errores de schema.
- [ ] **GSC → Inspeccionar URL:** "Solicitar indexación".
- [ ] **PageSpeed Insights:** verificar que CWV sea verde o ámbar.

---

## 10. Seguimiento (a 30, 60, 90 días)

- [ ] **30 días:** verificar en GSC que la página tiene impresiones (si no, hay problema de descubrimiento o relevancia).
- [ ] **60 días:** revisar posiciones promedio para la keyword principal.
- [ ] **90 días:** decidir si se necesita iteración: más contenido, más enlaces internos, o agregar una sección que falte.

---

## Atajos típicos a evitar

- Saltarse la auditoría on-page "porque la página se ve bien".
- Copiar el JSON-LD de otra zona y olvidar cambiar `areaServed` y `name`.
- Publicar sin enlaces internos contextuales (solo nav y footer).
- No actualizar el sitemap.
- Olvidar comprimir la imagen hero.
