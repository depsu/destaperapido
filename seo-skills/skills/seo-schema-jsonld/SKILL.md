---
name: seo-schema-jsonld
description: Genera, audita y corrige bloques JSON-LD (Schema.org) para páginas del rubro fosas/baños químicos. Cubre LocalBusiness, Plumber, Service, FAQPage, BreadcrumbList, Review/AggregateRating, Offer, Event (para eventos con baños químicos).
---

# Skill — JSON-LD / Schema.org

## Cuándo usar

- Crear / mejorar JSON-LD en páginas existentes.
- "Valida que el JSON-LD de Colina esté bien."
- Antes de publicar una página nueva.
- Cuando Google Search Console reporta errores de "datos estructurados".

## Tipos relevantes para este rubro

| Tipo | Cuándo usar |
|---|---|
| `LocalBusiness` o `Plumber` | Toda página principal (home, zonas, servicios, contacto) |
| `Service` | Cada página de servicio individual |
| `FAQPage` | Cualquier página con FAQ visible |
| `BreadcrumbList` | Páginas con migas (zonas, servicios) |
| `AggregateRating` + `Review` | Página de reseñas / nosotros — solo con datos REALES |
| `Offer` | Páginas con precios públicos |
| `Event` | Si haces landing para un evento concreto con baños químicos (Fiestas Patrias, conciertos) |
| `Article` / `BlogPosting` | Cada artículo del blog |
| `Organization` | Página "nosotros" / about |

## Reglas duras

1. **Solo afirmar lo verificable.** Reseñas, ratings y casos deben corresponder a datos reales (Google Business Profile como fuente). Inventar `aggregateRating` es violación de las políticas de Google y puede traer manual action.
2. **Coherencia con la UI.** Si el JSON-LD declara una FAQ, esas preguntas y respuestas deben aparecer también en el HTML visible.
3. **No mezclar tipos sin sentido.** Una página de zona NO es una `Article`.
4. **Usar URLs absolutas con `https://www.` consistente.**
5. **`@id` único** por entidad. Si Full Fosas se repite en muchas páginas, usar el MISMO `@id` (ej: `https://www.limpiafosasydestape.cl/#organization`).
6. **`telephone`** en formato E.164: `+56997946463`.
7. **`address` y `areaServed`** completos y precisos. Para empresa que no tiene dirección física pública, usar `addressRegion` y `addressCountry` sin `streetAddress`.

## Snippets base

### LocalBusiness / Plumber (entidad raíz, repetida en todas las páginas)

```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "Plumber"],
  "@id": "https://www.limpiafosasydestape.cl/#business",
  "name": "Full Fosas",
  "url": "https://www.limpiafosasydestape.cl",
  "telephone": "+56997946463",
  "email": "contacto@destaperapido.cl",
  "image": "https://www.limpiafosasydestape.cl/logo.png",
  "logo": "https://www.limpiafosasydestape.cl/logo.png",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "addressRegion": "Región Metropolitana",
    "addressCountry": "CL"
  },
  "areaServed": [
    { "@type": "AdministrativeArea", "name": "Región Metropolitana, Chile" }
  ],
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  }],
  "sameAs": [
    "https://www.facebook.com/...",
    "https://www.instagram.com/..."
  ]
}
```

> **Importante:** las `sameAs` deben ser cuentas reales y activas. No inventar URLs.

### Service (página de servicio)

Ver `seo-skills/skills/seo-servicio-nuevo/SKILL.md` para el ejemplo completo.

Claves: `serviceType`, `provider` (referencia al `LocalBusiness`), `areaServed`, `hasOfferCatalog`.

### FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Cada cuánto debo limpiar mi fosa séptica?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Para una vivienda con 4 personas, se recomienda cada 2-3 años. Si hay más residentes o lavandería intensiva, anualmente."
      }
    }
  ]
}
```

> **Crítico:** la pregunta y respuesta del JSON-LD debe coincidir EXACTAMENTE con la versión visible en HTML. Si la cambias en uno, sincroniza el otro.

### BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.limpiafosasydestape.cl/" },
    { "@type": "ListItem", "position": 2, "name": "Zonas Rurales", "item": "https://www.limpiafosasydestape.cl/zonas/rural/" },
    { "@type": "ListItem", "position": 3, "name": "Colina", "item": "https://www.limpiafosasydestape.cl/zonas/rural/colina.html" }
  ]
}
```

### AggregateRating (SOLO si hay datos reales)

```json
{
  "@type": "LocalBusiness",
  "name": "Full Fosas",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "183",
    "bestRating": "5"
  }
}
```

> Cifras de la memoria del usuario: 4.9★ con 183 reseñas. Mantenerlas sincronizadas con Google Business Profile.

### Event (landing para evento con baños químicos)

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Arriendo de baños químicos para Fiestas Patrias 2026",
  "startDate": "2026-09-17",
  "endDate": "2026-09-21",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": { "@type": "Place", "name": "Región Metropolitana, Chile" },
  "organizer": { "@id": "https://www.limpiafosasydestape.cl/#business" }
}
```

### Article (post de blog)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "datePublished": "2026-05-02",
  "dateModified": "2026-05-02",
  "author": { "@type": "Person", "name": "Alejandro Rivera" },
  "publisher": { "@id": "https://www.limpiafosasydestape.cl/#business" },
  "mainEntityOfPage": "https://www.limpiafosasydestape.cl/blog/<slug>.html",
  "image": "https://www.limpiafosasydestape.cl/images/blog/<slug>.webp"
}
```

## Proceso de auditoría

1. **Extraer** todos los bloques `<script type="application/ld+json">` de la página.
2. **Parsear** el JSON. Si falla, corregir sintaxis (comillas, comas finales).
3. **Validar** contra reglas:
   - `@context` y `@type` presentes
   - URLs absolutas con `https://www.`
   - `telephone` en E.164
   - Coherencia entre JSON-LD y UI (FAQ, Breadcrumb)
   - Sin propiedades inventadas
4. **Sugerir** validación final externa: copiar el JSON al [Rich Results Test](https://search.google.com/test/rich-results) o al [Schema Markup Validator](https://validator.schema.org/).
5. **Reportar** errores y warnings.

## Anti-patrones

- Pegar JSON-LD de un competidor sin entenderlo.
- Tipos exóticos (`MedicalOrganization`, `Restaurant`) en sitios que no lo son.
- Repetir `@id` de una entidad para entidades distintas.
- Mezclar `LocalBusiness` con `Person` como provider.
- JSON-LD con `name` en inglés cuando la UI está en español.
