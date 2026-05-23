---
name: seo-meta-unicos
description: Audita y reescribe titles + meta descriptions del proyecto para garantizar unicidad, longitud óptima e inclusión de keyword + CTA. Detecta duplicate content interno, descripciones débiles y titles que no respetan los rangos de pixeles de Google.
---

# Skill — Titles y meta descriptions únicos

## Cuándo usar

- "Revisa que ningún title se repita."
- "Mejora las meta descriptions de las páginas de zonas rurales."
- Después de un copy-paste masivo (riesgo de duplicate content).
- Trimestral, como mantenimiento.

## Proceso

### 1. Inventariar todos los titles y metas

Usa Bash:

```bash
# Inventario rápido de titles
grep -rh '<title>' public/ | sort | uniq -c | sort -rn | head -50

# Inventario de meta descriptions
grep -rh 'name="description"' public/ | sort | uniq -c | sort -rn | head -50

# Páginas que NO tienen meta description
for f in $(find public -name "*.html"); do
  grep -L 'name="description"' "$f"
done
```

O escribe un script Node con `cheerio` que genere CSV: `archivo, title, meta, len_title, len_meta`.

### 2. Detectar problemas

**Duplicates exactos:** dos páginas con el mismo `<title>` o misma meta. **Crítico.**

**Near-duplicates:** difieren solo en el nombre de la comuna ("Limpieza Fosas en Las Condes" vs "Limpieza Fosas en Vitacura"). **Mejorable** — variar ángulo.

**Largo fuera de rango:**
- Title < 30 chars: aprovechar más caracteres.
- Title > 65 chars: probablemente truncado por Google (~580px).
- Meta < 120 chars: demasiado corta, perdiendo CTR.
- Meta > 165 chars: truncada en SERP móvil.

**Sin keyword en title:** el title debe contener la keyword principal. Si la página es "destape WC en Las Condes" y el title dice "Servicios sanitarios | Full Fosas", está mal.

**Sin CTA en meta:** la meta debe invitar a clic. Buenos CTAs: "Cotiza por WhatsApp", "Atención 24/7", "Solicita tu visita".

### 3. Patrones recomendados

**Páginas de zona (24 zonas, evitar repetir patrón):**
- `"Limpieza Fosas Sépticas en Pirque | Servicio Rural — Full Fosas"`
- `"Destape Alcantarillado Las Condes | Camión Hidrojet 24/7"`
- `"Limpieza Fosas Colina | Parcelas y Condominios — Full Fosas"`
- `"Baños Químicos en Buin | Eventos y Faenas Agrícolas"`

Idealmente, **alternar la keyword principal** entre comunas:
- En zonas rurales — priorizar "limpieza fosas sépticas"
- En zonas urbanas — priorizar "destape alcantarillado" o "destape WC"
- En condominios — priorizar "destape edificios"

**Páginas de servicio:**
- `"Limpieza de Fosas Sépticas en Santiago RM | Full Fosas"`
- `"Destape de Alcantarillado 24/7 | Camión Hidrojet — Full Fosas"`
- `"Arriendo Baños Químicos en Chile | Eventos y Faenas"`

**Páginas top:**
- Home: `"Limpia Fosas y Destapes en RM | Servicio 24/7 — Full Fosas"`
- Contacto: `"Contacto Full Fosas | WhatsApp +56 9 9794 6463"`
- FAQ: `"Preguntas Frecuentes — Limpieza de Fosas y Destapes"`
- Nosotros: `"Sobre Full Fosas | +15 Años en Saneamiento RM"`

### 4. Reglas para meta descriptions

Plantilla:
> `[Servicio] en [Zona/Chile]. [Diferenciador real: equipo, años, 24/7]. [CTA: WhatsApp / cotización].`

Ejemplos:
- `"Limpieza de fosas sépticas en Pirque y zona rural. Camiones de 8.000 L, +15 años de experiencia, atención 24/7. Cotiza por WhatsApp."`  → 144 chars ✅
- `"Destape de alcantarillado en Las Condes. Camión hidrojet 4.000 PSI, respuesta inmediata 24/7. Solicita visita por WhatsApp."` → 130 chars ✅

Evitar:
- "Somos los mejores en limpieza de fosas..." (auto-elogio sin valor).
- Meta que termina cortada por longitud.
- Empezar con "En Full Fosas..." (desperdicia primeros caracteres).

### 5. Reescritura

Cuando reescribes una página:
1. Pregunta o infiere el ángulo de la página (¿qué la hace única?).
2. Genera 2-3 candidatos de title con diferente keyword principal.
3. Verifica unicidad con `grep -rh "<title>$CANDIDATO</title>" public/`.
4. Genera meta description que **complemente** el title (no lo repita).
5. Cuenta caracteres (`echo -n "..." | wc -c`).
6. Edita en el HTML preservando la estructura existente.
7. **Sincroniza** `og:title`, `og:description`, `twitter:title`, `twitter:description` con los nuevos valores. Es un error frecuente actualizar solo `<title>` y meta description y olvidar OG/Twitter.

### 6. Reportar

```
## Cambios sugeridos

### public/zonas/rural/colina.html
- Title actual (62 chars): "Limpieza Fosas Sépticas en Colina | Full Fosas - Servicio 24/7"
- Title propuesto (58 chars): "Limpieza Fosas en Colina | Parcelas y Condominios — Full Fosas"
- Razón: el actual se repite con Lampa y Chicureo.

- Meta actual (98 chars): demasiado corta.
- Meta propuesta (152 chars): "..."
```

## Aviso al usuario

Cuando termines, recuérdale:
- Verificar que el sitemap NO necesita actualización (el contenido cambia, las URLs no).
- Pedir reindexación en Google Search Console solo de las páginas con cambios significativos.
- No usar el cambio masivo como excusa para "amar" todos los textos a la vez si es complejo — preferir tandas de 5-10 páginas auditables.
