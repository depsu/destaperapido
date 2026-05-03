---
name: seo-keywords-locales
description: Investigación y mapeo de keywords locales (long-tail por comuna, intenciones, modificadores) para limpieza de fosas, destape y baños químicos en Chile. Construye una matriz keyword → página objetivo y detecta gaps de cobertura.
---

# Skill — Investigación de keywords locales (Chile)

## Cuándo usar

- Iniciar un sitio o expansión geográfica.
- Decidir qué páginas crear primero.
- Detectar oportunidades long-tail no cubiertas.
- "¿Qué keywords debería atacar para [comuna/servicio]?"

## Pirámide de keywords del rubro

```
HEAD (poco volumen relativo en regiones, mucha competencia)
  ├── "limpia fosas"
  ├── "destape de alcantarillado"
  ├── "baños químicos"

BODY (modificador de servicio)
  ├── "limpieza fosa séptica precio"
  ├── "destape WC urgente"
  ├── "arriendo baño químico"

LONG-TAIL (geográfica + intención)  ← oro para sitios chicos
  ├── "limpieza fosa séptica Pirque"
  ├── "destape alcantarillado urgente Las Condes"
  ├── "baños químicos para fiestas patrias Santiago"
  ├── "camión limpia fosas Colina"
  ├── "cuánto cuesta limpiar fosa séptica en Chile 2026"
```

**Para sitios locales de servicios → la pirámide invertida:** atacar long-tail primero, ganar tráfico cualificado, después subir a body.

## Modificadores que importan en Chile

### De urgencia
- "urgente", "24 horas", "ahora", "domingo", "feriado", "fin de semana"

### De geografía
- Nombre de comuna ("Pirque", "Las Condes")
- "Santiago", "RM", "Región Metropolitana"
- "norte de Santiago", "zona oriente", "cordillera"
- "rural", "urbano"
- "cerca de mí" (importante en mobile)

### De precio
- "precio", "barato", "económico", "valor", "tarifa", "presupuesto"

### De informacional
- "cómo", "por qué", "cada cuánto", "qué hacer si", "señales", "diferencia entre"

### De empresa
- "empresa", "profesionales", "certificados", "con boleta", "con factura"

### De equipo
- "camión limpia fosas", "hidrojet", "alta presión", "cámara de inspección"

### Específicos de baños químicos
- "para evento", "para faena", "para construcción", "premium", "discapacitados", "WC portátil", "fiestas patrias", "matrimonio"

## Matriz keyword → página

Construir una hoja `keywords.csv` (o `keywords.md` markdown) con:

```
keyword                                        | volumen | dificultad | intención  | url_objetivo                              | estado
limpieza fosa séptica pirque                   | 30/mes  | baja       | trans.     | /zonas/rural/pirque.html                  | ✅ rankea
destape alcantarillado las condes              | 70/mes  | media      | trans.     | /zonas/urbano/las-condes.html             | ⚠️ pos 12
cada cuánto limpiar fosa séptica               | 200/mes | media      | inform.    | /blog/cada-cuanto-limpiar-fosa.html       | 📝 falta crear
baños químicos santiago precio                 | 50/mes  | baja       | trans.     | /servicios/banos-quimicos.html            | ✅ rankea
camión limpia fosas chicureo                   | 10/mes  | muy baja   | trans.     | /zonas/rural/chicureo.html                | ❌ huérfana
```

> Volúmenes son **estimaciones** — sin acceso a herramienta paga, usa sensación + Google Trends + autocompletado para priorizar.

## Cómo investigar sin herramientas pagas

### 1. Autocompletado de Google
- Tipea inicio de keyword → ver sugerencias.
- Probar variantes: "limpieza fosa séptica ", "limpiafosas ", "limpia fosas " (con/sin espacio).
- Recopilar todas las sugerencias con prefijos y sufijos.

Ejemplo:
```
"limpieza fosa séptica" + ?
  → "precio", "santiago", "valor", "cerca de mí", "cuanto cuesta", "metalica", "domiciliaria"
```

### 2. People Also Ask (PAA)
- Hacer la búsqueda de la keyword head.
- Anotar las preguntas que aparecen en el bloque "Otras preguntas".
- Cada pregunta es candidato para un h2 o un artículo.

### 3. Búsquedas relacionadas (footer del SERP)
- Al final de la página de resultados, Google muestra "Búsquedas relacionadas".
- Recopilar todas.

### 4. Google Trends
- Comparar dos keywords ("limpia fosas" vs "destape alcantarillado") en Chile.
- Ver estacionalidad (importante: la limpieza de fosas SUBE en otoño-invierno tras lluvias; los baños químicos suben en verano y septiembre).

### 5. Análisis de competencia (manual y ético)
- Buscar la keyword head.
- Listar los 10 primeros resultados.
- Para cada uno: qué keywords usa en title, h1, h2, meta. (Lectura manual del HTML.)
- Detectar **gaps** — qué cubren y qué no.

### 6. SERP de la competencia con MCP fetch
Si tienes el MCP de fetch instalado:
> "Trae el HTML de [URL competidor en posición 1] y extrae title, h1, h2, meta description, JSON-LD."

### 7. Search Console (cuando haya datos propios)
- Cuando el sitio acumule 3-6 meses de datos, GSC → Performance → Queries muestra QUÉ palabras te traen impresiones.
- Las que tienen impresiones pero baja CTR → revisar title/meta para ganar clic.
- Las que están en posición 11-20 → optimizar contenido para subirlas al top 10.

## Estrategia recomendada para Full Fosas

### Fase 1 — cobertura básica (ya hecha, según el repo)
- 1 página por comuna principal (24 zonas)
- 10 páginas de servicio
- Home + nosotros + faq + contacto

### Fase 2 — long-tail informacional (blog)
- 8-12 artículos del blog cubriendo PAA y "cómo / cuándo / por qué".
- Skill: `seo-blog-articulo`.

### Fase 3 — modificadores comerciales
- Páginas específicas tipo:
  - `/landing/limpia-fosas-urgente-rm.html`
  - `/landing/banos-quimicos-fiestas-patrias.html`
  - `/landing/contratos-condominios.html`
- Skill: `seo-servicio-nuevo` (con ángulo de landing).

### Fase 4 — micro-zonas y cluster geográfico
- Subdividir comunas grandes (ej: "Las Condes — Apoquindo", "Las Condes — Estoril") solo si hay volumen.
- O cubrir comunas más periféricas con menor competencia (Talagante, Padre Hurtado, Peñaflor, Melipilla).

### Fase 5 — multimedia
- Video corto en YouTube por servicio principal.
- Embed en la página + Schema VideoObject.

## Reportar

```
## Análisis de keywords — Limpieza de fosas Pirque

### Keywords principales (intent comercial)
1. "limpieza fosa séptica pirque" — long-tail bajo volumen, baja competencia, MUY GANABLE
2. "limpia fosas pirque" — variante
3. "camión limpia fosas pirque" — específico

### Keywords secundarias
- "limpieza fosa séptica zona rural santiago"
- "limpia fosas parcelas pirque"

### Long-tail informacional
- "fosa séptica pirque cada cuánto limpiar" — apunta a blog
- "tarifa limpia fosas zona oriente santiago"

### Gaps detectados
- No tenemos página específica para parcelas / condominios en Pirque (consolidamos genérica).
- Falta artículo blog "Mantención de fosas en parcelas de la precordillera".

### Acción recomendada
- Reescribir h1 de pirque.html a "Limpieza de Fosas Sépticas en Pirque y Precordillera"
- Agregar sección "Para parcelas grandes" en pirque.html
- Crear blog: "Frecuencia de mantención de fosa séptica según tamaño del terreno"
```
