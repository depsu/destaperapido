---
name: seo-zona-nueva
description: Crea una nueva página de zona (comuna urbana o rural) optimizada para SEO local en Chile. Genera title, meta description, contenido único de 800+ palabras, JSON-LD LocalBusiness con areaServed, enlaces internos y entrada en el sitemap.
---

# Skill — Crear página nueva de zona

## Cuándo usar

- El usuario dice "crea la página de [comuna]" o "agrega zona [X]".
- Se va a abrir cobertura a una comuna nueva (ej: Peñaflor, Padre Hurtado, Melipilla).
- En el workflow de expansión geográfica.

## Proceso

### 1. Pedir / inferir datos clave

Antes de escribir, asegúrate de tener:
- **Nombre de la comuna** (ej: "Peñaflor")
- **Tipo:** urbano / rural / mixto
- **Particularidades reales:** ¿hay muchos condominios? ¿zonas agrícolas? ¿edificios? ¿ascendencia colonial? ¿cercanía a río o napa subterránea (relevante para fosas sépticas)?
- **Slug:** kebab-case sin tildes (`peñaflor` → `penaflor`).
- **Categoría:** `urbano` o `rural` (define la subcarpeta en `public/zonas/`).
- **Comunas vecinas ya cubiertas:** para enlazar.

Si falta info, pregunta antes de inventar. Especialmente cuidado con afirmaciones tipo "zona conocida por X" — solo usar si es verificable.

### 2. Diseñar el ángulo único de la página

NO repitas el mismo template entre comunas. Cada página debe tener un **ángulo distintivo** que justifique su existencia ante Google.

Ejemplos de ángulos:
- **Pirque:** parcelas grandes, fosa séptica como infraestructura principal, terreno con napa subterránea variable.
- **Las Condes:** edificios y condominios verticales, mantención de redes prediales, urgencias de WC tapado en horario laboral.
- **Colina:** condominios cerrados, accesos restringidos, contratos mensuales, fosas dimensionadas para 6+ personas.
- **Buin/Paine:** zona agrícola, retiro de RILes, alta humedad por canales de regadío.

El ángulo debe reflejarse en: title, h1, intro, FAQ, casos.

### 3. Estructura mínima de la página

Usa `seo-skills/templates/zona-template.html` como base. Debe contener:

```
<head>
  - title único (ver §4)
  - meta description única
  - canonical https://www.limpiafosasydestape.cl/zonas/<categoria>/<slug>.html
  - OG / Twitter completos
  - JSON-LD: LocalBusiness + areaServed + Service + BreadcrumbList + FAQPage
</head>

<body>
  <header> ← compartido (importar igual que otras zonas)
  <main>
    <h1> ← keyword principal con comuna
    <section> intro 120-180 palabras (ángulo único)
    <section> servicios disponibles en la zona (3-5 bullets)
    <section> por qué la fosa/baño-químico es relevante AQUÍ (datos locales)
    <section> proceso paso a paso
    <section> precios referenciales (sin mentir — ver memoria de precios)
    <section> casos reales / testimonios (si los hay)
    <section> FAQ (4-6 preguntas LOCALES, no genéricas)
    <section> CTA grande con WhatsApp
    <section> "También cubrimos en zonas cercanas" + 4-6 enlaces internos
  </main>
  <footer> ← compartido
</body>
```

### 4. Title y meta description

**Reglas:**
- Title 50-62 caracteres. Patrón sugerido (variar entre comunas):
  - Rural: `"Limpieza Fosas Sépticas en [Comuna] | Servicio 24/7 — Full Fosas"`
  - Urbano: `"Destape Alcantarillado en [Comuna] | Camión Hidrojet — Full Fosas"`
  - Variar el ángulo: condominios, parcelas, urgencia, etc.
- Meta description 140-160 caracteres. Debe incluir:
  - Servicio + comuna
  - Diferenciador real (24/7, +15 años, +8000 servicios — datos verídicos de memoria)
  - CTA suave ("Cotiza por WhatsApp")

**Verificar unicidad:** antes de guardar, busca el title y meta propuestos en `public/**/*.html` con grep. Si ya existe uno parecido, modifícalo.

### 5. Contenido (mínimo 800 palabras)

**Reglas estrictas:**
- Cero párrafos genéricos copy/paste de otra comuna.
- Mencionar la comuna 4-8 veces en el cuerpo, naturalmente.
- Usar variantes: "vecinos de [comuna]", "en [comuna] y alrededores", "particulares y empresas en [comuna]".
- Incluir 1-2 datos hiperlocales verificables (ej: "el sector rural de Pirque depende mayoritariamente de fosas dado que no hay alcantarillado en gran parte del valle").
- NO inventar regulaciones específicas de la comuna sin verificar.
- Mencionar el reglamento sanitario nacional (DS 236/1926) cuando aplique a fosas.
- Para baños químicos: mencionar normativa OS-10 o eventos específicos (eventos masivos, faenas, fiestas patrias).

### 6. JSON-LD requerido

Mínimo 4 bloques (ver `templates/jsonld-snippets.md`):

```json
[
  { "@type": "LocalBusiness", "areaServed": "<Comuna>, Región Metropolitana, Chile", ... },
  { "@type": "Service", "areaServed": "<Comuna>", "provider": { "@type": "LocalBusiness", "name": "Full Fosas" }, ... },
  { "@type": "FAQPage", "mainEntity": [ ... 4-6 preguntas ... ] },
  { "@type": "BreadcrumbList", ... Home > Zonas > Categoría > Comuna }
]
```

### 7. Enlaces internos obligatorios

Mínimo en la página:
- 3 a comunas vecinas ya cubiertas
- 2 a páginas de servicio relevantes (`servicios/limpieza-fosas-septicas.html`, etc.)
- 1 a `casos-reales/` o blog si hay artículo relacionado
- 1 a `contacto.html`

Y al revés: agregar enlace **DESDE** las comunas vecinas hacia esta nueva página (ver skill `seo-enlazado-interno`).

### 8. Sitemap y navegación

- Agregar entrada en `public/sitemap.xml` con `<lastmod>` actual.
- Si hay un menú/listado de zonas (`public/zonas/<categoria>/index.html`), agregar el enlace ahí.
- Si hay un componente de "navegación de zonas" reutilizado, actualizarlo.

### 9. Validar antes de cerrar

Corre mentalmente la skill `seo-audit-onpage` sobre la página recién creada. Reporta puntuación y arregla lo crítico.

## Después de crear

Sugiere al usuario:
1. Validar JSON-LD en `https://search.google.com/test/rich-results`.
2. Ejecutar el script `scripts/inject_internal_links.py` (si existe en su flujo) para reforzar el linking automático.
3. En GSC: enviar la URL nueva al index manualmente (`Inspeccionar URL` → `Solicitar indexación`).

## Anti-patrones

- Generar 10 páginas de comunas con el mismo template — Google las verá como duplicate content.
- Inventar testimonios o datos de servicios realizados en la comuna.
- Prometer "llegamos en 30 minutos" — la memoria del usuario lo prohíbe (no prometer minutos fijos).
- Copiar el JSON-LD de otra zona sin actualizar `areaServed` y `name`.
