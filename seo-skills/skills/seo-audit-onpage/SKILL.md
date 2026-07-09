---
name: seo-audit-onpage
description: Auditoría on-page SEO completa de una página HTML estática del rubro fosas/baños químicos. Revisa title, meta description, encabezados, alt, canonical, OG/Twitter, JSON-LD, enlaces internos, imágenes y CWV básico.
---

# Skill — Auditoría on-page SEO

## Cuándo usar

- El usuario te pasa una ruta concreta (ej: `public/zonas/rural/colina.html`) y pide "audita SEO".
- Después de crear o modificar una página, antes de hacer commit.
- Como paso previo en el workflow `flujo-pagina-nueva.md`.

## Datos del proyecto (Full Fosas)

- Marca: **Full Fosas**
- Dominio canónico: `https://www.limpiafosasydestape.cl`
- Teléfono: `+56 9 6588 9226` (WhatsApp `https://wa.me/56965889226`)
- Email: `contacto@destaperapido.cl` (NO `@limpiafosasydestape.cl` — decisión del dueño)
- Mercado: Región Metropolitana, Chile

## Proceso

### 1. Leer la página
Lee el HTML completo. Si el archivo es muy grande, foco en `<head>`, primeros `<h1>`/`<h2>`, último bloque (footer / scripts), y bloques `<script type="application/ld+json">`.

### 2. Checklist a verificar

**HEAD — meta básicos**
- [ ] `<title>` único (cruzar con todos los demás `<title>` del proyecto). Largo: 50–62 caracteres.
- [ ] `<meta name="description">` único. Largo: 140–160 caracteres. Incluye keyword principal + CTA.
- [ ] `<link rel="canonical">` apuntando a `https://www.limpiafosasydestape.cl/<ruta>` (con www, sin parámetros, sin slash final inconsistente con el resto).
- [ ] `<html lang="es">`.
- [ ] `<meta charset="UTF-8">`.
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- [ ] Robots: si la página debe indexar, NO debe haber `<meta name="robots" content="noindex">`.

**HEAD — Open Graph / Twitter**
- [ ] `og:title`, `og:description`, `og:type`, `og:url`, `og:image`, `og:locale=es_CL`.
- [ ] `twitter:card=summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image`.
- [ ] La imagen OG debe existir físicamente (verifica el archivo en `public/images/`) y pesar < 300 KB.

**Estructura semántica**
- [ ] Exactamente UN `<h1>` por página, con la keyword principal.
- [ ] Jerarquía coherente: `h1 → h2 → h3` (sin saltar de h2 a h4).
- [ ] Cada `<h2>` cubre una intención de búsqueda secundaria.
- [ ] `<main>` envuelve el contenido principal. `<header>`, `<footer>`, `<nav>` correctamente usados.

**Imágenes**
- [ ] Todas las `<img>` tienen `alt` descriptivo (no genérico tipo "imagen").
- [ ] Imágenes pesadas (no logo) tienen `loading="lazy" decoding="async"`.
- [ ] El primer hero / LCP NO es lazy (debe cargar inmediato).
- [ ] Formato `.webp` preferido. Si hay `.jpg`/`.png`, sugerir conversión.
- [ ] `width` y `height` definidos para evitar CLS.

**Enlaces internos**
- [ ] Mínimo 5 enlaces internos contextuales (no solo nav/footer).
- [ ] Anchor text descriptivo (NO "haz clic aquí", "más info").
- [ ] Apuntan a páginas relevantes: zonas hermanas, servicios relacionados, blog.
- [ ] No hay enlaces rotos (todos los `href` internos resuelven a archivos existentes).

**Enlaces externos**
- [ ] Externos (no propios) llevan `rel="noopener"` mínimo.
- [ ] Patrocinados / afiliados: `rel="sponsored"`. UGC: `rel="ugc"`.

**JSON-LD (Schema.org)**
- [ ] Mínimo: `LocalBusiness` o `Plumber` con dirección, teléfono, areaServed, openingHours.
- [ ] Si hay FAQ visible: `FAQPage` con cada pregunta.
- [ ] Si es página de servicio: `Service`.
- [ ] `BreadcrumbList` si hay migas en la UI.
- [ ] Validar mentalmente contra Schema.org (sin propiedades inventadas).
- [ ] Sugerir validar con `https://search.google.com/test/rich-results` antes de publicar.

**Contenido**
- [ ] Mínimo 600 palabras útiles para páginas de zona/servicio (idealmente 900+).
- [ ] Keyword principal en title, h1, primer párrafo, al menos 1 h2, slug y meta.
- [ ] Densidad razonable (no keyword stuffing — máx 1.5%).
- [ ] Variantes semánticas: "fosa séptica", "pozo séptico", "limpieza de fosas", "destape de cañerías", "baño químico", "WC portátil".
- [ ] Datos de confianza visibles: años de operación, número de servicios, reseñas, fotos reales.

**Performance básica (sin abrir Lighthouse)**
- [ ] CSS crítico inline o `output.css` cacheado.
- [ ] Sin Tailwind CDN en producción.
- [ ] Scripts no críticos con `defer` o `async`.
- [ ] Sin `<style>` enormes inline.

**Marca y datos sensibles**
- [ ] Teléfono en formato consistente: `+56 9 6588 9226`.
- [ ] Enlaces wa.me: `https://wa.me/56965889226` (sin espacios, sin +).
- [ ] Dominio canónico con `www`.
- [ ] Logo split correcto: `<span>FULL<span class="text-brand-600">FOSAS</span></span>`.

### 3. Reportar

Genera un **reporte en formato checklist** con secciones:

```
## ✅ Bien
- ...

## ⚠️ Mejorable
- ...

## ❌ Crítico (corregir antes de publicar)
- ...

## 📊 Métricas estimadas
- Largo title: X caracteres
- Largo meta: X caracteres
- Palabras del cuerpo: X
- Enlaces internos: X
- Imágenes con alt: X / Y
- JSON-LD presentes: ...
```

### 4. Ofrecer correcciones

Termina preguntando: "¿Quieres que corrija los puntos críticos ahora?". No edites sin confirmación.

## Errores frecuentes en este rubro

- Repetir el mismo `<title>` "Limpieza de Fosas Sépticas en [Comuna] - Full Fosas" entre 24 comunas → **duplicate content**. Cada comuna debe tener un title único con un ángulo distinto (rural vs urbano, condominio, etc.).
- Olvidar el JSON-LD `Service` en páginas de servicios.
- `meta description` que repite el `<title>` literal.
- `canonical` apuntando a la versión sin `www` cuando el sitio canónico SÍ tiene www.
- Imágenes `.jpg` de 800 KB sin lazy → arruina LCP.

## Recursos relacionados

- Templates: `seo-skills/templates/zona-template.html`, `servicio-template.html`
- Snippets JSON-LD: `seo-skills/templates/jsonld-snippets.md`
- Skill complementaria: `seo-meta-unicos` para regenerar titles/descriptions.
