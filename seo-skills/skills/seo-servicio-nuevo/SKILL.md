---
name: seo-servicio-nuevo
description: Crea o reescribe una página de servicio (limpieza fosas, destape, baños químicos, hidrojet, inspección con cámara, etc.) optimizada para SEO comercial. Estructura: hero con CTA, problema, solución, proceso, equipamiento, precios, FAQ y JSON-LD Service.
---

# Skill — Crear / mejorar página de servicio

## Cuándo usar

- "Crea la página del servicio [X]" o "mejora `servicios/destape-wc-y-banos.html`".
- Lanzar un nuevo servicio (ej: arriendo de baños químicos premium, retiro de RILes industriales).
- Reescribir una página antigua que está perdiendo posiciones.

## Estructura recomendada

### HEAD

- Title 50-62 chars: `"<Servicio> en Santiago y RM | Camiones <equipo> — Full Fosas"`
- Meta description 140-160 chars con diferenciador real + CTA.
- Canonical: `https://www.limpiafosasydestape.cl/servicios/<slug>.html`.
- OG/Twitter completos con imagen del servicio (no genérica).
- JSON-LD: `Service` + `LocalBusiness` (provider) + `BreadcrumbList` + `FAQPage` si hay FAQ visible. Para servicios con precio público: `Offer`.

### BODY

```
<main>
  1. HERO
     - h1 con keyword principal
     - subtítulo con propuesta de valor (15-30 palabras)
     - 2 CTAs: WhatsApp + "ver precios"
     - badge: 24/7, +15 años, etc.

  2. PROBLEMA / DOLOR
     - "¿Cuándo necesitas este servicio?" — 4-6 escenarios
     - señales que indican que el problema existe (ej: malos olores, lentitud en desagüe, fosa que rebalsa)

  3. SOLUCIÓN — qué incluye el servicio
     - bullets concretos (NO genéricos)
     - equipos: camión limpia fosas X litros, hidrojet, inspección con cámara, etc.
     - cobertura: comunas atendidas

  4. PROCESO PASO A PASO
     - 4-6 pasos numerados, breves
     - tiempo estimado por paso si aplica

  5. PRECIOS REFERENCIALES
     - tabla simple con tarifas (consultar memoria del usuario para 2026)
     - aclarar que dependen de tamaño de fosa, distancia, accesibilidad
     - CTA "cotiza tu caso"

  6. PROYECTOS / CASOS REALES
     - 2-3 mini-cards con imagen + breve historia
     - Anchor desde aquí a casos-reales/

  7. PREGUNTAS FRECUENTES
     - 6-10 preguntas reales (no inventadas)
     - respuestas 50-100 palabras

  8. ZONAS DONDE OPERAMOS
     - Listado con enlace a las páginas de zona
     - Mejora el interlinking interno

  9. CTA FINAL
     - WhatsApp grande
     - "Atención 24/7, respuesta inmediata"
</main>
```

## Reglas de contenido

### Long-form, pero útil
- Mínimo 1000 palabras para servicios principales (limpieza fosas, destape alcantarillado).
- 700+ para servicios secundarios (hidrojet específico, inspección cámara).
- Pero **no relleno** — cada párrafo debe sumar.

### Vocabulario y semántica
Mezcla los términos que la gente busca con los técnicos:
- "fosa séptica" + "pozo séptico" + "tanque séptico"
- "destape" + "desatascar" + "desobstruir"
- "WC tapado" + "inodoro tapado" + "baño tapado"
- "alcantarillado" + "red de servidumbre" + "cañería pluvial"
- "baño químico" + "WC portátil" + "sanitario móvil"

### EEAT (autoridad y confianza)
Incluir SIEMPRE:
- **Experiencia:** "+15 años atendiendo en RM" (memoria) o cifra real verificable.
- **Equipamiento:** "camiones de 8.000 litros + hidrojet 4000 PSI" (cifras concretas).
- **Cumplimiento:** "trabajamos según DS 236/1926" para fosas, "OS-10" cuando aplique.
- **Sociales:** rating real, reseñas Google, testimonios con nombre y comuna.
- **Garantía:** política clara (ej: "si vuelve a taparse en 7 días, regresamos sin costo" — solo si es real).

### Datos sensibles a no inventar
- No prometer tiempos de llegada en minutos (memoria).
- No usar precios "exactos" si dependen de variables — siempre "desde $X".
- No copiar testimonios de otros sitios.

## JSON-LD Service (esqueleto)

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Limpieza de fosas sépticas",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Full Fosas",
    "telephone": "+56997946463",
    "url": "https://www.limpiafosasydestape.cl",
    "address": {
      "@type": "PostalAddress",
      "addressRegion": "Región Metropolitana",
      "addressCountry": "CL"
    }
  },
  "areaServed": {
    "@type": "AdministrativeArea",
    "name": "Región Metropolitana, Chile"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Servicios de saneamiento",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": { "@type": "Service", "name": "Limpieza fosa séptica residencial" },
        "priceCurrency": "CLP",
        "price": "100000"
      }
    ]
  }
}
```

## Servicios típicos del rubro y ángulo recomendado

| Servicio | Ángulo SEO recomendado |
|---|---|
| Limpieza de fosas sépticas | "tamaño + frecuencia + zonas rurales" |
| Destape de alcantarillado | "urgencia 24/7 + camión hidrojet" |
| Destape WC y baños | "residencial + bajo costo + sin romper" |
| Destape desagües cocina/grasa | "trampa de grasa + restaurantes" |
| Destape edificios y condominios | "B2B + contratos mensuales" |
| Hidrojet alta presión | "limpieza profunda + cañerías obstruidas con grasa o raíces" |
| Inspección con cámara | "diagnóstico antes de obra + comunidades" |
| Mantención preventiva | "contratos anuales + ahorro vs emergencias" |
| Arriendo baños químicos | "eventos + faenas + cantidad por persona/día" |
| Contratos empresas/condominios | "B2B + facturación + convenios" |

## Después de crear / reescribir

1. Correr `seo-audit-onpage` sobre la página.
2. Asegurar que aparece linkeada desde:
   - `public/servicios/index.html`
   - `public/index.html` (si es servicio principal)
   - Páginas de zona donde aplica
3. Actualizar `public/sitemap.xml` (`<lastmod>`).
4. Validar JSON-LD en `https://search.google.com/test/rich-results`.
