---
name: seo-blog-articulo
description: Redacta un artículo de blog largo (1200-2000 palabras) optimizado para SEO informacional del rubro fosas/baños químicos, con estructura EEAT, JSON-LD Article, FAQ embebida y enlazado interno a servicios y zonas.
---

# Skill — Artículo de blog SEO

## Cuándo usar

- "Escribe un artículo sobre [tema]."
- Cuando hay que cubrir una intención informacional (people also ask, "cómo / cuándo / por qué").
- Para construir autoridad temática (topical authority) en saneamiento.

## Filosofía

El blog NO existe para vender directo — existe para **rankear keywords informacionales** que después se convierten vía enlaces a servicios. Las páginas de servicio cazan transaccionales ("contratar destape Las Condes"), el blog caza informacionales ("cada cuánto limpiar fosa séptica").

## Investigación previa

### 1. Validar la intención

Antes de escribir, responder:
- ¿Qué busca exactamente la persona que tipea el query?
- ¿Es informacional, transaccional o navegacional?
- ¿Qué muestra Google hoy en la primera página? (chequear manualmente el SERP)
- ¿Hay featured snippet, PAA, video, imágenes?

### 2. Keyword principal + variantes

```
Keyword principal: "cada cuánto limpiar fosa séptica"
Variantes:
  - "frecuencia limpieza fosa séptica"
  - "cuándo limpiar fosa séptica"
  - "señales fosa llena"
  - "cuántos años dura una fosa séptica"
```

### 3. Esqueleto de tópicos (people also ask)

Mira el bloque "Otras preguntas" de Google y úsalo como base para los `<h2>` y la sección FAQ.

## Estructura recomendada

```
HEAD
  - title 50-62 chars con keyword principal
  - meta description con keyword + valor (ej: "Aprende a detectar las señales y la frecuencia recomendada según el tamaño de tu fosa.")
  - canonical
  - OG/Twitter
  - JSON-LD: Article + FAQPage + BreadcrumbList

BODY
  <article>
    <h1>            ← keyword principal natural, no exacta-match a la fuerza
    <p> intro       ← 80-120 palabras, anuncia qué va a aprender el lector

    <h2> tópico 1   ← responder la duda principal en los primeros 200 palabras (TL;DR)
    <h2> tópico 2
    <h2> tópico 3
    ... (5-8 secciones)

    <h2> Tabla / lista práctica  (frecuencia por nº de personas, costos, etc.)

    <h2> Cuándo llamar a un profesional  ← gancho a tu servicio
       <p> + CTA contextual a /servicios/limpieza-fosas-septicas.html

    <h2> Preguntas frecuentes  ← 5-8 Q&A, replicadas en JSON-LD FAQPage

    <p> conclusión + CTA WhatsApp
  </article>

  <aside> "Artículos relacionados" — 3 enlaces a otros posts del blog
```

## Reglas de redacción

### Largo
- Mínimo **1200 palabras**, ideal **1500-2000**.
- Más NO siempre es mejor — Google premia profundidad útil, no relleno.

### Tono
- Español de Chile, segunda persona ("tu fosa", "te recomendamos").
- Profesional pero cercano. Sin jerga innecesaria.
- Cuando uses tecnicismos, explícalos brevemente.

### Densidad de keyword
- Keyword principal en: title, h1, primer párrafo, 1 h2, 1 imagen alt, slug, meta description.
- **No keyword stuffing.** Densidad < 1.5%. Mejor variar con sinónimos.

### EEAT en el cuerpo
- Citar fuentes autoritativas: SISS, Ministerio de Salud, DS 236/1926, Reglamento Sanitario.
- Datos numéricos concretos (litros, años, costos) — verificables.
- Mencionar experiencia propia: "en nuestros 15+ años hemos visto..." (con cuidado de no sobrevender).
- Foto con autor real al final si aplica.

### Snippets capturables
Estructura el inicio para ganar el featured snippet:
- **Pregunta como `<h2>`** y **respuesta concisa de 40-60 palabras** justo abajo.
- Listas y tablas — Google las extrae directo a snippets.
- Definiciones cortas en `<dl><dt><dd>`.

### Enlazado interno desde el blog
Cada artículo debe linkear:
- 1-2 páginas de servicio (con anchor descriptivo, no "haz clic aquí").
- 1 página de zona si el tema es geográficamente relevante.
- 1-2 otros posts del blog (cluster temático).

### Imágenes
- 3-6 imágenes a lo largo del artículo.
- Formato `.webp`.
- Alt descriptivo con keyword cuando sea natural.
- `loading="lazy"` (excepto la primera).
- Caption opcional para imágenes complejas.

## JSON-LD Article + FAQPage

```json
[
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Cada cuánto limpiar una fosa séptica: guía 2026",
    "datePublished": "2026-05-02",
    "dateModified": "2026-05-02",
    "author": {
      "@type": "Person",
      "name": "Alejandro Rivera",
      "url": "https://www.limpiafosasydestape.cl/nosotros.html"
    },
    "publisher": { "@id": "https://www.limpiafosasydestape.cl/#business" },
    "mainEntityOfPage": "https://www.limpiafosasydestape.cl/blog/cada-cuanto-limpiar-fosa.html",
    "image": "https://www.limpiafosasydestape.cl/images/blog/limpiar-fosa.webp",
    "wordCount": 1650
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [ ... ]
  }
]
```

## Temas con potencial para este rubro

### Fosas sépticas (informacional)
- "Cada cuánto limpiar una fosa séptica"
- "Cuánto cuesta limpiar una fosa séptica en Chile 2026"
- "Cuánto dura una fosa séptica"
- "Cómo saber si la fosa séptica está llena"
- "Diferencia entre fosa séptica y pozo negro"
- "Qué hacer si la fosa séptica rebalsa"
- "Mantención preventiva de fosa séptica: pasos"
- "Cómo dimensionar una fosa séptica para 4-6-8 personas"

### Destape (informacional)
- "Cómo destapar un WC sin romper"
- "Por qué se tapa el alcantarillado: causas reales"
- "Hidrojet vs destape mecánico: cuál elegir"
- "Qué NO tirar al WC para evitar tapaduras"

### Baños químicos (informacional + comercial)
- "Cuántos baños químicos necesito para X personas"
- "Cuánto cuesta arrendar un baño químico en Chile"
- "Normativa de baños químicos en eventos masivos en Chile"
- "Tipos de baños químicos: estándar, premium, accesible"

### B2B
- "Mantención de redes de alcantarillado en condominios"
- "Inspección con cámara: cuándo es necesaria"
- "Cómo elegir empresa de limpia fosas (checklist)"

## Después de publicar

1. **GSC → Inspeccionar URL** → solicitar indexación.
2. **Compartir** en redes y/o Google Business como post.
3. **Linkear desde** páginas de servicio relevantes ("artículo relacionado").
4. **Programar revisión** a los 3-6 meses para actualizar precios/datos y refrescar `dateModified`.

## Anti-patrones

- Artículo "10 cosas que no sabías de las fosas" — clickbait sin sustancia.
- Reescribir un post viejo sin agregar valor real (Google lo nota).
- Keyword exacta repetida 30 veces.
- Sin enlace a servicios (el blog se vuelve isla y no convierte).
- Sin imágenes (parece llenar nomás).
- Inventar estadísticas para sonar autoritativo.
