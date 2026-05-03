---
name: seo-enlazado-interno
description: Audita y refuerza el enlazado interno (internal linking) entre páginas de zona, servicios, blog y casos reales. Detecta páginas huérfanas, anchor texts genéricos, y oportunidades de enlace contextual.
---

# Skill — Enlazado interno

## Cuándo usar

- Después de agregar páginas nuevas (siempre).
- Trimestral, como mantenimiento.
- Cuando una página tiene buen contenido pero no rankea (puede ser falta de equity interno).
- "Audita el linking interno del sitio."

## Por qué importa

El enlazado interno hace tres cosas:
1. **Distribuye PageRank** entre páginas — las más enlazadas reciben más equity.
2. **Indica relevancia temática** a Google con el anchor text.
3. **Mejora UX** y tiempo en sitio.

En sitios estáticos chicos (50-100 páginas), un buen interlinking puede subir posiciones sin tocar contenido.

## Proceso

### 1. Construir el grafo del sitio

Listar todas las páginas:

```bash
find public -name "*.html" -not -path "*node_modules*" | sort
```

Para cada página, contar **enlaces internos entrantes** y **salientes**:

```bash
# Outbound de una página
grep -oE 'href="[^"]+"' public/zonas/rural/colina.html | sort -u

# Inbound a una página
grep -rl 'colina.html' public/ | wc -l
```

O escribir un script Node con cheerio que produzca:

```
PAGE                                  | INBOUND | OUTBOUND_INTERNAL
public/zonas/rural/colina.html        |     8   |    14
public/zonas/rural/lampa.html         |     1   |     6   ← huérfana / casi-huérfana
public/servicios/destape-wc.html      |    32   |    11
```

### 2. Detectar problemas

**Páginas huérfanas:** 0 o 1 enlaces entrantes desde dentro del sitio. Google no las descubrirá fácilmente.

**Páginas con outbound vacío:** las "hojas" sin enlaces salen del flujo y matan el equity.

**Anchor genéricos:** "haz clic aquí", "más info", "ver más". Anchor sin keyword desperdicia la oportunidad SEO.

**Self-links:** una página linkea a sí misma. Generalmente inútil (excepto canonical).

**Linking-loops sin valor:** A → B → A en el mismo párrafo, sin contexto.

**Enlaces rotos:** href que apunta a un archivo que no existe.

### 3. Estrategia de hubs y spokes

```
SERVICIOS (hub)
  ├── /servicios/limpieza-fosas-septicas.html
  ├── /servicios/destape-alcantarillado.html
  └── /servicios/destape-wc-y-banos.html
        ↑↓
ZONAS (spokes)
  ├── /zonas/rural/colina.html  → linkea servicios + comunas vecinas
  ├── /zonas/urbano/las-condes.html
  ...
        ↑↓
BLOG (apoyo informativo)
  └── /blog/cada-cuanto-limpiar-fosa.html → linkea servicios + zonas
```

**Reglas:**
- Cada **zona** linkea a 3+ comunas vecinas + 2+ servicios principales + 1 blog si aplica.
- Cada **servicio** linkea a 5-10 zonas representativas + servicios relacionados.
- Cada **post de blog** linkea a 1-3 servicios + 1 zona relevante.
- Home (`index.html`) linkea a los servicios top y categorías de zona.
- `casos-reales/` linkea a la zona y servicio del caso.

### 4. Anchor texts recomendados

| Mal | Bien |
|---|---|
| "haz clic aquí" | "limpieza de fosas sépticas en Pirque" |
| "ver más" | "destape de alcantarillado en Las Condes" |
| "info" | "tarifas de limpia fosas 2026" |
| "esta página" | "guía de mantención de fosa séptica" |

Variar levemente el anchor entre páginas (no todos exactos) para evitar parecer manipulación.

### 5. Plantilla de bloque "zonas relacionadas"

Para insertar al final de páginas de servicio o zonas:

```html
<section class="related-zones">
  <h2>También cubrimos zonas cercanas</h2>
  <ul>
    <li><a href="/zonas/rural/colina.html">Limpieza de fosas en Colina</a></li>
    <li><a href="/zonas/rural/chicureo.html">Servicio en Chicureo</a></li>
    <li><a href="/zonas/rural/lampa.html">Cobertura en Lampa</a></li>
    <li><a href="/zonas/rural/calera-de-tango.html">Calera de Tango y alrededores</a></li>
  </ul>
</section>
```

### 6. Contextual vs navigational

- **Contextual:** dentro del contenido en párrafos, entre `<p>`. Es el más valioso para SEO.
- **Navigational:** en menús, footers, breadcrumbs. Útil para UX, menos peso SEO porque está en todas las páginas.

Esta skill prioriza generar **contextual links** dentro del cuerpo, no más entradas en menús.

### 7. Implementación

Cuando detectes oportunidades, propón cambios concretos:

```
Página: public/servicios/limpieza-fosas-septicas.html

PROPUESTA: en el párrafo de "zonas con mayor demanda", reemplazar:

  ANTES: "...especialmente en sectores rurales como Colina, Lampa o Pirque."

  DESPUÉS: "...especialmente en sectores rurales como
    <a href="/zonas/rural/colina.html">Colina</a>,
    <a href="/zonas/rural/lampa.html">Lampa</a> o
    <a href="/zonas/rural/pirque.html">Pirque</a>."
```

NO insertes 50 enlaces de golpe. Mejor 5-10 cambios revisables a la vez.

### 8. Script automático (referencia)

Si el proyecto ya tiene `scripts/inject_internal_links.py`, revisar qué reglas usa antes de duplicar trabajo. Para este proyecto:

```bash
python3 scripts/inject_internal_links.py
```

(Verificar primero qué hace exactamente con `head -50` antes de correrlo.)

## Reportar

```
## Estado del enlazado interno

### Huérfanas (0-1 inbound)
- public/zonas/rural/calera-de-tango.html (0 inbound)
- public/blog/que-pasa-si-no-limpio-fosa.html (1 inbound)

### Top equity (más enlazadas)
- public/servicios/limpieza-fosas-septicas.html (45)
- public/zonas/urbano/las-condes.html (38)

### Anchors genéricos detectados
- 14 ocurrencias de "haz clic aquí" en X archivos
- 8 "ver más" en footer de zonas

### Oportunidades concretas
1. servicios/destape-alcantarillado.html → linkear a zonas/urbano/providencia.html
2. blog/cada-cuanto-limpiar.html → linkear a servicios/limpieza-fosas-septicas.html
...
```

Termina preguntando: "¿Aplico los cambios sugeridos?".
