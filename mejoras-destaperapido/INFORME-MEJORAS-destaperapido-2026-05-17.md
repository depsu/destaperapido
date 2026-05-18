# 📊 INFORME COMPLETO DE MEJORAS - destaperapido.cl

**Fecha:** 17 mayo 2026
**Repositorio:** https://github.com/depsu/destaperapido
**Objetivo:** Conseguir 95-100/100 en Performance, Accesibilidad, Best Practices y SEO en MOBILE
**Fuente de datos:** Lighthouse 13.0.1 (Moto G Power emulado, 4G lenta) + CrUX 28 días + Inspección DOM

---

## 🎯 SCORES ACTUALES vs OBJETIVO (MOBILE)

| Página | Perf actual | Perf objetivo | A11y actual | A11y objetivo |
|---|---|---|---|---|
| / (home) | 76 🟠 | **95** ✅ | 90 | **100** ✅ |
| /zonas/rural/talagante | 60 🟠 | **95** ✅ | 90 | **100** ✅ |
| /zonas/rural/isla-de-maipo | 73 🟠 | **95** ✅ | 90 | **100** ✅ |
| /zonas/rural/colina | 61 🟠 | **95** ✅ | 90 | **100** ✅ |
| /zonas/rural/buin-paine | 66 🟠 | **95** ✅ | 90 | **100** ✅ |
| /zonas/rural/lampa | **52** 🔴 | **90** ✅ | 92 | **100** ✅ |
| /zonas/rural/calera-de-tango | 58 🟠 | **95** ✅ | 92 | **100** ✅ |
| /zonas/rural/pirque | 65 🟠 | **95** ✅ | 92 | **100** ✅ |
| /precios-orientativos | 63 🟠 | **95** ✅ | 88 🔴 | **100** ✅ |

---

## 🔥 PROBLEMAS CRÍTICOS IDENTIFICADOS POR GOOGLE

### Performance

**1. Imágenes mal optimizadas (mayor impacto: -15 a -25 puntos)**
- Lampa: ahorro estimado **311 KiB** | Calera: 307 KiB | Pirque: 307 KiB | Buin-Paine: 221 KiB
- Talagante: 170 KiB | Isla de Maipo: 133 KiB | Colina: 117 KiB | Home: 69 KiB
- **EVIDENCIA EN CÓDIGO:** Imagen 'Paisaje rural Lampa' tiene natW=2070px pero se muestra a 393px en mobile. Se sirven 5x más píxeles.
- **EVIDENCIA EN CÓDIGO:** Logo del header tiene `loading="lazy"` siendo above-the-fold (debe ser eager).

**2. Render-blocking resources (-5 a -10 puntos)**
- Lampa y Talagante: **450 ms** de ahorro detectado
- Calera, Colina, Precios: 300 ms cada uno
- Buin-Paine, Isla-Maipo, Pirque: 150 ms cada uno
- **CAUSA:** Font Awesome CDN (`https://cdnjs.cloudflare.com/.../font-awesome/6.4.0/css/all.min.css`) ~70KB bloqueante.
- **CAUSA:** Google Fonts cargado síncrono.

**3. JavaScript no usado: 148 KiB por página (-5 a -8 puntos)**
- Consistente en TODAS las páginas.
- **CAUSA:** Bundle único sin code-splitting + GTM + Clarity sincrónicos.

**4. CSS no usado: 18-28 KiB por página**
- **CAUSA:** Tailwind output.css probablemente sin purge configurado correctamente.

**5. Tareas largas en hilo principal: TBT 80-360 ms**
- Lampa: **360 ms** (7 tareas largas) ← peor caso
- Buin-Paine: 260 ms | Precios: 270 ms | Home: 220 ms

**6. Demasiados preconnects (6 detectados, recomendado máximo 3)**
- Actual: transparenttextures.com, cdnjs.cloudflare.com, googletagmanager.com, fonts.googleapis.com, fonts.gstatic.com, images.unsplash.com
- **Mantener solo:** fonts.gstatic.com y googletagmanager.com

### Accesibilidad

**A1. CONTRASTE insuficiente** (todas las páginas)
- Texto fondo claro sobre fondo claro sin ratio 4.5:1
- Ubicaciones probables: subtítulos en gris claro, botones flotantes WhatsApp/teléfono

**A2. Enlaces sin nombre reconocible** (todas)
- **EVIDENCIA REAL EN CÓDIGO:**
  ```html
  <a href="tel:+56997946463" class="...">
    <i class="fa-solid fa-phone"></i>
  </a>
  ```
  Falta `aria-label`. Los lectores de pantalla dicen "enlace" sin contexto.

**A3. Orden incorrecto de headings**
- **EVIDENCIA REAL:** En home se detectó H1 → H3 saltando H2
- Páginas afectadas: home, lampa, colina, calera-de-tango

**A4. Falta landmark <main>**
- Detectado en: /zonas/rural/isla-de-maipo

### Best Practices (96/100 en algunas páginas)
- Posibles cookies sin SameSite explícito (Clarity, GTM)
- Posibles errores en console

---

## ✅ PLAN DE IMPLEMENTACIÓN PASO A PASO

### SEMANA 1: Quick Wins (8-12h) → Esperado: 52-76 → 85-95

#### FIX-02: Quitar loading="lazy" del logo (15 min)
**Buscar en todos los HTML:**
```html
<img src="/logo-nav.webp" ... loading="lazy" decoding="async">
```
**Reemplazar por:**
```html
<img src="/logo-nav.webp" ... loading="eager" fetchpriority="high">
```

#### FIX-04: Reducir preconnects (30 min)
**Eliminar de TODOS los HTML:**
```html
<link rel="preconnect" href="https://www.transparenttextures.com/">
<link rel="preconnect" href="https://cdnjs.cloudflare.com/">
<link rel="preconnect" href="https://images.unsplash.com/">
<link rel="preconnect" href="https://fonts.googleapis.com/">
```
**Mantener solo:**
```html
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://www.googletagmanager.com">
```

#### FIX-07: Recompilar Tailwind con purge (1h)
**En tailwind.config.js:**
```js
module.exports = {
  content: ['./public/**/*.html', './public/**/*.js'],
  // ...
}
```
**Compilar:**
```bash
NODE_ENV=production npx tailwindcss -i ./src/input.css -o ./public/output.css --minify
```
Verificar que output.css quede <30 KB.

#### FIX-A11Y-02: aria-label en enlaces con solo icono (2h)
**Patrón a corregir en TODOS los HTML:**
```html
<!-- ANTES -->
<a href="tel:+56997946463" class="...">
  <i class="fa-solid fa-phone"></i>
</a>

<!-- DESPUÉS -->
<a href="tel:+56997946463" aria-label="Llamar al +56 9 9794 6463" class="...">
  <i class="fa-solid fa-phone" aria-hidden="true"></i>
</a>
```
Aplicar lo mismo a iconos de WhatsApp, redes sociales, menú hamburguesa, etc.

#### FIX-SEO-01: Redirect 301 http→https (1h)
**En .htaccess (Apache):**
```
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```
**En Nginx:**
```nginx
server {
  listen 80;
  server_name destaperapido.cl www.destaperapido.cl;
  return 301 https://www.destaperapido.cl$request_uri;
}
```
**Impacto:** Recuperar 6045 impresiones/mes desperdiciadas.

#### FIX-01 (parcial): Optimizar imagen LCP de home y lampa (3h)
1. Generar AVIF + WebP responsive (400w, 800w, 1200w) con Squoosh o sharp.
2. Comprimir a <60KB mobile.
3. Usar `<picture>` con srcset.
4. Preload del LCP en `<head>`.

```html
<!-- En <head> -->
<link rel="preload" as="image"
  imagesrcset="/images/hero-400.avif 400w, /images/hero-800.avif 800w, /images/hero-1200.avif 1200w"
  imagesizes="100vw" type="image/avif">

<!-- En body -->
<picture>
  <source type="image/avif" srcset="/images/hero-400.avif 400w, /images/hero-800.avif 800w, /images/hero-1200.avif 1200w" sizes="100vw">
  <source type="image/webp" srcset="/images/hero-400.webp 400w, /images/hero-800.webp 800w, /images/hero-1200.webp 1200w" sizes="100vw">
  <img src="/images/hero-800.webp" alt="..." width="1200" height="600" fetchpriority="high" decoding="async">
</picture>
```

---

### SEMANA 2: Optimizaciones pesadas (12-16h) → 85-95 → 95-100

#### FIX-03: Eliminar Font Awesome CDN (3h)
1. Auditar iconos usados: `grep -rho 'fa-[a-z-]*' public/ | sort -u`
2. Descargar SVGs equivalentes desde fontawesome.com o usar heroicons.com.
3. Reemplazar `<i class="fa-...">` por SVG inline.
4. Eliminar `<link>` a cdnjs.cloudflare.com.

**Ejemplo:**
```html
<!-- ANTES -->
<i class="fa-solid fa-phone"></i>

<!-- DESPUÉS -->
<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
  <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
</svg>
```

#### FIX-05: Auto-hospedar Google Fonts (2h)
1. Descargar woff2 desde google-webfonts-helper.
2. Hospedar en /fonts/.
3. Eliminar `<link>` a fonts.googleapis.com.

```html
<link rel="preload" href="/fonts/inter-regular.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-regular.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}
</style>
```

#### FIX-06: Inline critical CSS (3h)
```bash
npx critical public/index.html --width=412 --height=915 --inline
```
Pegar CSS resultante inline en `<style>` y cargar el resto async:
```html
<link rel="preload" href="/output.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/output.css"></noscript>
```

#### FIX-08: Diferir GTM y Clarity (1h)
Mover al final del `<body>` y retrasar 2-3 segundos:
```html
<script>
window.addEventListener('load', function(){
  setTimeout(function(){
    // Código de GTM aquí
  }, 2000);
});
</script>
```

---

### SEMANA 3: Accesibilidad y SEO (10-14h) → A11y 88-92 → 100

#### FIX-A11Y-01: Corregir contraste (3h)
- Auditar con webaim.org/resources/contrastchecker
- Cambiar `text-slate-400` → `text-slate-600` en fondos claros.
- En hero con imagen de fondo: agregar overlay `bg-black/50`.

#### FIX-A11Y-03: Corregir orden de headings (2h)
En home, agregar H2 'Servicios principales' antes del bloque que tiene H3 '¿Dónde es el problema?'.

#### FIX-SEO-02: Expandir /precios-orientativos a 800+ palabras (4h)
Agregar H2:
- "Precios destape de alcantarillado en Santiago"
- "Precios limpieza fosas sépticas"
- "Factores que afectan el precio"
- "Tabla comparativa por comuna"
- "Preguntas frecuentes sobre precios" (con FAQ Schema)

#### Indexación manual (1h)
12 URLs en Google Search Console (zonas urbanas y rurales secundarias).

---

## 📋 CHECKLIST DE VALIDACIÓN FINAL

### Performance 100 ✓
- [ ] LCP <2.5s en lab (ideal <1.5s)
- [ ] FCP <1.8s
- [ ] TBT <200ms (ideal <100ms)
- [ ] CLS <0.1 (ideal 0)
- [ ] Sin render-blocking resources
- [ ] Imágenes mobile <100KB cada una
- [ ] JS bundle total <100KB
- [ ] CSS total <30KB

### Accesibilidad 100 ✓
- [ ] Todos los textos con contraste 4.5:1+
- [ ] Todos los enlaces con nombre accesible
- [ ] Todas las imágenes con alt descriptivo
- [ ] Jerarquía de headings correcta
- [ ] Elemento <main> presente
- [ ] Elemento <nav> presente
- [ ] HTML con lang="es"

### Best Practices 100 ✓
- [ ] HTTPS en todos los recursos
- [ ] Sin errores en console
- [ ] Cookies con SameSite y Secure

### SEO 100 ✓
- [ ] Title único 50-60 caracteres
- [ ] Meta description única 150-160 caracteres
- [ ] Canonical correcto
- [ ] Schema.org markup
- [ ] Sitemap.xml válido

---

## 🛠 COMANDOS ÚTILES

```bash
# Auditar tamaño de imágenes
find public/images -name '*.jpg' -o -name '*.png' | xargs ls -lh

# Generar AVIF + WebP
npx @squoosh/cli --avif '{quality:50}' --webp '{quality:75}' public/images/*.jpg

# Generar critical CSS
npx critical public/index.html --width=412 --height=915 --inline > public/index-critical.html

# Validar con Lighthouse
npx lighthouse https://destaperapido.cl --preset=mobile --output=html --output-path=./report.html

# Recompilar Tailwind con purge
NODE_ENV=production npx tailwindcss -i ./src/input.css -o ./public/output.css --minify

# Validar HTML
npx html-validator-cli --file=public/index.html
```

---

## 🎯 KPIs OBJETIVO

| Métrica | Actual | Objetivo |
|---|---|---|
| Clics 28 días | 166 | 300 |
| Impresiones 28 días | 5,180 | 8,000 |
| CTR | 3.2% | 5.5% |
| Posición promedio | 7.5 | 4.5 |

---

## 📂 ARCHIVOS A MODIFICAR (21 HTMLs)

```
public/
├── index.html ⚠
├── precios-orientativos.html ⚠
└── zonas/
    ├── rural/
    │   ├── talagante.html ⚠
    │   ├── isla-de-maipo.html ⚠
    │   ├── colina.html ⚠
    │   ├── buin-paine.html ⚠
    │   ├── lampa.html 🔴 (crítico)
    │   ├── calera-de-tango.html ⚠
    │   ├── pirque.html ⚠
    │   ├── chicureo.html
    │   ├── curacavi.html
    │   ├── melipilla.html
    │   ├── padre-hurtado.html
    │   ├── penaflor.html
    │   └── san-jose-de-maipo.html
    └── urbano/
        ├── las-condes.html
        ├── vitacura.html
        ├── lo-barnechea.html
        ├── providencia.html
        ├── la-reina.html
        └── nunoa.html
```

🔴 = LCP crítico (>7s en lab)
⚠ = Performance bajo 80
