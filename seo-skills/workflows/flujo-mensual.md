# Workflow — Mantenimiento SEO mensual

Rutina ~2-3 horas, 1 vez al mes. Mantiene el sitio sano y captura oportunidades.

---

## Día 1 — Datos en GSC y diagnóstico

### 1. Google Search Console — Performance
- [ ] Top 10 queries por impresiones (últimos 28 días).
- [ ] Top 10 queries por clics.
- [ ] Queries con **alta impresión + bajo CTR** (< 2%) → revisar title/meta de la URL objetivo.
- [ ] Queries en **posición 11-20** → oportunidad de mejorar contenido para subir al top 10.
- [ ] Queries que aparecen en **posiciones 1-3 con muchas impresiones** → consolidar.

### 2. GSC — Indexación
- [ ] Páginas en "Indexadas": cuántas y cuáles.
- [ ] Páginas en "No indexadas, motivo": revisar cada motivo.
- [ ] URLs con error 404 o redirect en cadena: corregir.

### 3. GSC — Experiencia en la página (CWV)
- [ ] Cuántas URLs son "Buenas / A mejorar / Pobres" en móvil y escritorio.
- [ ] Si hay URLs "Pobres": skill `seo-core-web-vitals` para diagnosticar.

### 4. GSC — Enlaces
- [ ] Páginas más enlazadas externamente: ¿son las que esperabas?
- [ ] Anchor texts entrantes: ¿son relevantes? ¿hay spam?

---

## Día 2 — Salud técnica del sitio

### 5. Skill `seo-sitemap-robots`
- [ ] Sincronizar `public/sitemap.xml` con el estado real del disco.
- [ ] Validar XML.
- [ ] Verificar `robots.txt`.

### 6. Enlaces rotos
```bash
pnpm dlx linkinator http://localhost:3000 --recurse --skip "wa.me|tel:|mailto:"
```
- [ ] Reparar 4xx y 5xx internos.
- [ ] Para externos rotos, decidir: actualizar o quitar.

### 7. Validación HTML
```bash
pnpm dlx html-validate "public/**/*.html"
```
- [ ] Resolver errores estructurales.

### 8. Core Web Vitals (sitio entero)
```bash
pnpm dlx unlighthouse --site http://localhost:3000
```
- [ ] Listar las 5 páginas con peor performance.
- [ ] Aplicar correcciones (skill `seo-core-web-vitals`).

---

## Día 3 — Contenido

### 9. Detectar duplicate content interno
- [ ] Skill `seo-meta-unicos`.
- [ ] Reescribir titles/metas duplicados.

### 10. Páginas que decaen
- [ ] Identificar páginas que perdieron > 30% de impresiones vs mes anterior (datos GSC).
- [ ] Para cada una: revisar contenido, refrescar fecha de último update, agregar 1-2 enlaces internos entrantes.

### 11. Páginas huérfanas
- [ ] Skill `seo-enlazado-interno`.
- [ ] Asegurar que toda página tiene mínimo 3 inbound links internos.

### 12. Refrescar contenido top
- [ ] Top 10 páginas por tráfico: ¿están actualizadas (precios 2026, fecha mod)?
- [ ] Aprovechar para sumar 1 párrafo nuevo y bumpear `<lastmod>`.

---

## Día 4 — Crecimiento

### 13. Investigación de keywords (skill `seo-keywords-locales`)
- [ ] Identificar 1-2 keywords con potencial sin cubrir.
- [ ] Decidir: ¿nueva página o sumar sección a una existente?

### 14. Plan editorial
- [ ] Si toca, redactar 1-2 artículos de blog (skill `seo-blog-articulo`).

### 15. Reseñas de Google Business Profile
- [ ] Solicitar 3-5 reseñas a clientes recientes.
- [ ] Responder a TODAS las reseñas (positivas y negativas) en GBP.
- [ ] Si la cuenta de reseñas cambia, actualizar `aggregateRating` en JSON-LD.

### 16. Posts en GBP
- [ ] Crear 1-2 posts en GBP con foto de un servicio reciente.

---

## Día 5 — Reporte interno

Generar un mini-reporte en `docs/seo-reportes/YYYY-MM.md`:

```markdown
# Reporte SEO — Mayo 2026

## KPIs
- Clics: 1.240 (+12% vs abril)
- Impresiones: 18.500 (+8%)
- CTR promedio: 6.7% (+0.4 pp)
- Posición promedio: 14.2 (vs 15.1)

## Top movimientos
- "limpia fosas pirque": pos 8 → pos 4 (mejorada con enlace interno desde servicios/limpieza-fosas-septicas)
- "destape WC las condes": pos 12 → pos 7

## Cambios aplicados
- Reescritos 6 titles de zonas rurales para evitar duplicate.
- Sitemap regenerado (88 URLs).
- 5 enlaces rotos corregidos.
- Hero del index optimizado (LCP 3.2s → 1.7s).

## Pendientes para junio
- Crear página zona Peñaflor.
- Artículo blog "cuánto cuesta un baño químico premium".
- Optimizar imágenes en 4 páginas con CWV "A mejorar".
```

---

## Frecuencia recomendada por tarea

| Tarea | Frecuencia |
|---|---|
| Revisar GSC Performance | Mensual |
| Sincronizar sitemap | Mensual o tras cambios masivos |
| Auditoría CWV completa | Mensual |
| Audit on-page de páginas top | Trimestral |
| Refrescar contenido | Trimestral |
| Reportar a stakeholders | Mensual |
| Reseñas y GBP | Semanal o quincenal |
| Crear página nueva | Bajo demanda (idealmente 1-2/mes) |

---

## Indicadores de alerta

🚨 Acciones urgentes si ves:
- **Caída > 30% en clics** mes a mes sin causa clara → revisar GSC manual actions, server errors, cambios recientes.
- **Cobertura indexación bajando** → problema técnico (robots, canonical, server).
- **CWV "Pobre" en > 30% de URLs** → priorizar performance.
- **Página crítica fuera del sitemap** o con `noindex` por error.
