# Snippets JSON-LD listos para copiar

> Reemplaza los `{{PLACEHOLDERS}}` antes de pegar.

---

## 1. Entidad raíz `LocalBusiness` + `Plumber`

Usar en TODA página, con el mismo `@id` para que Google entienda que es la misma entidad.

```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "Plumber"],
  "@id": "https://www.limpiafosasydestape.cl/#business",
  "name": "Full Fosas",
  "url": "https://www.limpiafosasydestape.cl",
  "telephone": "+56965889226",
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
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "183"
  }
}
```

---

## 2. `Service` (página de servicio)

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "{{SERVICIO}}",
  "name": "{{NOMBRE_SERVICIO}} en Región Metropolitana",
  "description": "{{DESCRIPCION_50_PALABRAS}}",
  "provider": { "@id": "https://www.limpiafosasydestape.cl/#business" },
  "areaServed": { "@type": "AdministrativeArea", "name": "Región Metropolitana, Chile" },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Tarifas referenciales 2026",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": { "@type": "Service", "name": "{{TIPO_1}}" },
        "priceCurrency": "CLP",
        "price": "100000"
      },
      {
        "@type": "Offer",
        "itemOffered": { "@type": "Service", "name": "{{TIPO_2}}" },
        "priceCurrency": "CLP",
        "price": "120000"
      }
    ]
  }
}
```

---

## 3. `FAQPage`

> ⚠️ Las preguntas y respuestas DEBEN aparecer también en el HTML visible. Si no, Google puede penalizar.

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
        "text": "Para una vivienda con 4 personas, cada 2 a 3 años. Si hay más residentes o uso intensivo, anualmente."
      }
    },
    {
      "@type": "Question",
      "name": "¿Atienden en {{COMUNA}}?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, cubrimos {{COMUNA}} y sectores aledaños con disponibilidad 24/7. Cotización inmediata por WhatsApp al +56 9 6588 9226."
      }
    }
  ]
}
```

---

## 4. `BreadcrumbList`

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.limpiafosasydestape.cl/" },
    { "@type": "ListItem", "position": 2, "name": "{{NIVEL_2}}", "item": "{{URL_NIVEL_2}}" },
    { "@type": "ListItem", "position": 3, "name": "{{NIVEL_3}}", "item": "{{URL_NIVEL_3}}" }
  ]
}
```

---

## 5. `Article` / `BlogPosting` (post de blog)

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{{TITULO_ARTICULO}}",
  "description": "{{META_DESCRIPTION}}",
  "datePublished": "2026-05-02",
  "dateModified": "2026-05-02",
  "author": {
    "@type": "Person",
    "name": "Alejandro Rivera",
    "url": "https://www.limpiafosasydestape.cl/nosotros.html"
  },
  "publisher": { "@id": "https://www.limpiafosasydestape.cl/#business" },
  "mainEntityOfPage": "https://www.limpiafosasydestape.cl/blog/{{SLUG}}.html",
  "image": "https://www.limpiafosasydestape.cl/images/blog/{{SLUG}}.webp",
  "wordCount": 1650,
  "keywords": "{{KEYWORDS_SEPARADAS_POR_COMA}}"
}
```

---

## 6. `Event` (landing para evento con baños químicos)

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Arriendo de baños químicos para {{EVENTO}}",
  "startDate": "2026-09-17",
  "endDate": "2026-09-21",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": { "@type": "Place", "name": "Región Metropolitana, Chile" },
  "organizer": { "@id": "https://www.limpiafosasydestape.cl/#business" },
  "description": "{{DESCRIPCION_DEL_EVENTO_O_TEMPORADA}}"
}
```

---

## 7. `Review` individual (testimonio destacado)

```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": { "@id": "https://www.limpiafosasydestape.cl/#business" },
  "author": { "@type": "Person", "name": "{{NOMBRE_REAL}}" },
  "datePublished": "2026-04-15",
  "reviewBody": "{{TEXTO_RESEÑA_REAL}}",
  "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" }
}
```

> ⚠️ Solo usar reseñas reales (de Google Business o similar). Inventarlas viola las políticas de Google.

---

## 8. `VideoObject` (si embebes video propio)

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "{{TITULO_VIDEO}}",
  "description": "{{DESCRIPCION}}",
  "thumbnailUrl": "https://www.limpiafosasydestape.cl/images/video-thumb.webp",
  "uploadDate": "2026-04-01",
  "duration": "PT2M30S",
  "contentUrl": "https://www.youtube.com/watch?v={{ID}}",
  "embedUrl": "https://www.youtube.com/embed/{{ID}}"
}
```

---

## Cómo combinarlos en una sola página

Mete múltiples bloques en un único `<script type="application/ld+json">` como **array**:

```html
<script type="application/ld+json">
[
  { ... LocalBusiness ... },
  { ... Service ... },
  { ... BreadcrumbList ... },
  { ... FAQPage ... }
]
</script>
```

Es válido y más limpio que tener 4 `<script>` separados.

---

## Validación

1. [Rich Results Test](https://search.google.com/test/rich-results) — qué muestra Google.
2. [Schema Markup Validator](https://validator.schema.org/) — validación pura del spec.
3. Cuando esté en producción, GSC → Mejoras → ahí se ven los errores agregados de tu sitio.
