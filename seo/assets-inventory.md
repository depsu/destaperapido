# Inventario de assets para registros — diagnóstico

Última revisión: 2026-05-18

---

## Resumen ejecutivo

**Listo para usar:** fotos de trabajos (5 imágenes WebP de buena calidad y variedad de orientación).

**Gaps a resolver antes de empezar la campaña de directorios:**

1. ⚠️ **No hay un logo cuadrado en alta resolución**. El `logo.png` actual es 1323×420 (horizontal). Google Business, Facebook, Instagram, LinkedIn, Trustpilot y la mayoría de directorios piden **logo cuadrado ≥1000×1000 px**. Hoy no lo tienes.
2. ⚠️ **OG image declarada como 1200×630 no es exactamente eso**. El archivo real es 1032×576 — Facebook y LinkedIn pueden recortar mal. Idealmente regenerarlo a 1200×630 exacto.
3. ⚠️ **Algunos directorios no aceptan WebP**. Páginas Amarillas, Mercantil y varios clasificados solo aceptan JPG/PNG. Hay que tener variantes JPG de las imágenes clave.

---

## 1. Inventario detallado

| Archivo | Dimensiones | Peso | Uso correcto | Uso problemático |
|---|---|---|---|---|
| `public/logo.png` | 1323×420 | 793 KB | Header de sitio, footer | ❌ NO como foto de perfil cuadrada |
| `public/logo-nav.png` | 139×144 | 46 KB | Header móvil | ❌ NO como logo de perfil (muy chico) |
| `public/logo-nav.webp` | 139×144 | 11 KB | Header móvil | ❌ NO como logo de perfil |
| `public/favicon.png` | 397×411 | 343 KB | Favicon | ⚠️ Solo si no hay otra opción y se acepta WebP |
| `public/images/camio-haciendo-servicio-en-la-calle.webp` | 1032×576 | 186 KB | OG image, foto portada | ⚠️ No es 1200×630 exacto |
| `public/images/Destape-alcantarillado-con-camion-en-subterraneo-de-edificio-1280w.webp` | 1280×543 | 53 KB | Galería | ✅ |
| `public/images/camio-junto-a-trabajador-al-frente-de-una-empresa-haciendo-servicio.webp` | 1056×576 | 200 KB | Galería | ✅ |
| `public/images/camion-haciendo-servicio-en-condominio.webp` | 756×792 | 195 KB | Galería (orientación casi cuadrada) | ✅ |
| `public/images/limpieza-con-camara.jpg` | 791×667 | 254 KB | Galería | ✅ JPG nativo |
| `public/images/camion-haciendo-destape-en-zona-rural.webp` | 810×1013 | 218 KB | Galería (vertical, sirve para Instagram) | ✅ |

---

## 2. Lo que necesitas generar antes de empezar

### A. Logo cuadrado en alta resolución (CRÍTICO)

**Especificaciones requeridas:**
- Tamaño: 1000×1000 px mínimo (recomendado 2000×2000 para futuro-proof)
- Fondo: blanco o transparente (PNG con alpha)
- Formato: PNG (primario) + JPG (fallback)
- Padding interno: ~10% del borde para que no quede pegado a los márgenes
- El logo cuadrado debe verse legible al achicarlo a 128×128 (es así como aparece en Bing Places y algunos clasificados)

**Cómo generarlo (opciones):**
1. **Si tienes Figma/Canva**: parte del logo horizontal y centra sobre fondo blanco 2000×2000.
2. **Quick fix en Preview (macOS)**: abre `logo.png`, Tools → Adjust Size, hazlo 2000×2000 con fondo blanco. Resultado no será óptimo (el isotipo quedará apretado o estirado) — solo úsalo como solución temporal.
3. **Recomendado**: pídele a un diseñador (o a Claude con DALL-E/edición) que cree una versión cuadrada del logo, idealmente con solo el isotipo (sin "DESTAPE RÁPIDO" tipográfico — porque a 128×128 el texto no se lee).

**Guardar como:**
- `public/assets/logo-square-2000.png` (PNG 2000×2000)
- `public/assets/logo-square-2000.jpg` (JPG fondo blanco)
- `public/assets/logo-square-512.png` (versión menor pre-comprimida, útil para uploads con límite de peso)

### B. OG image 1200×630 exacta (RECOMENDADO)

**Especificaciones:**
- Tamaño: 1200×630 exacto (estándar Facebook/LinkedIn)
- Formato: JPG (Facebook recomienda JPG sobre WebP por compatibilidad)
- Peso: <300 KB

**Cómo generarlo:**
1. Toma `camio-haciendo-servicio-en-la-calle.webp` (1032×576)
2. Convierte a JPG y redimensiona a 1200×630. Si el aspect ratio cambia, recorta los bordes (no estires).

**Guardar como:**
- `public/assets/og-image-1200x630.jpg`

**Comando rápido (necesita `cwebp` y `convert` de ImageMagick instalados):**
```bash
# Si tienes ImageMagick:
convert public/images/camio-haciendo-servicio-en-la-calle.webp \
  -resize 1200x630^ -gravity center -extent 1200x630 \
  -quality 85 public/assets/og-image-1200x630.jpg

# Si no, hazlo manual en Preview.
```

### C. Versiones JPG de las fotos de galería (para sitios que no aceptan WebP)

Convierte las 5 fotos de galería de WebP a JPG con calidad 85. Guarda en `public/assets/jpg/`.

```bash
mkdir -p public/assets/jpg
for img in public/images/Destape-alcantarillado-con-camion-en-subterraneo-de-edificio-1280w.webp \
           public/images/camio-junto-a-trabajador-al-frente-de-una-empresa-haciendo-servicio.webp \
           public/images/camion-haciendo-servicio-en-condominio.webp \
           public/images/camion-haciendo-destape-en-zona-rural.webp; do
  out=$(basename "$img" .webp).jpg
  convert "$img" -quality 85 "public/assets/jpg/$out"
done
```

---

## 3. Mapeo asset → uso por tipo de sitio

| Tipo de sitio | Foto perfil/avatar | Foto portada | Galería | Formato |
|---|---|---|---|---|
| Google Business | logo cuadrado 1000×1000 | og-image 1200×630 | 5 fotos galería | JPG/PNG |
| Bing Places | logo cuadrado | og-image | 5 fotos galería | JPG/PNG |
| Facebook Business | logo cuadrado (mín 170×170) | og-image (820×312 ideal) | múltiples | JPG/PNG |
| Instagram Business | logo cuadrado (320×320 mostrado) | N/A | feed posts | JPG/PNG |
| LinkedIn Company | logo cuadrado (300×300 mínimo) | banner 1128×191 | N/A | PNG |
| Páginas Amarillas | logo (sirve horizontal) | foto principal | 1-3 fotos | JPG |
| Infoisinfo | logo cuadrado | foto principal | 3-5 fotos | JPG/PNG |
| Cronoshare | logo cuadrado | banner | hasta 10 fotos trabajos | JPG/PNG |
| Habitissimo | logo cuadrado | portada | hasta 20 fotos trabajos | JPG/PNG |
| Clasificados | N/A | 1 foto destacada | 2-4 fotos | JPG (mayoría no acepta WebP) |
| YouTube | logo cuadrado | banner 2560×1440 | thumbnails 1280×720 | JPG/PNG |

---

## 4. Plan de acción de assets (orden recomendado)

1. **Hoy mismo** (5 min): copia los 5 archivos de fotos actuales a `public/assets/jpg/` en formato JPG con ImageMagick (script arriba).
2. **Esta semana** (1-2 horas): genera logo cuadrado 2000×2000 PNG. Sin esto, el 60% de los directorios te van a quedar feos.
3. **Esta semana** (15 min): genera `og-image-1200x630.jpg` exacto.
4. **Próximas 2 semanas** (opcional): sesión de fotos profesional de la flota y técnicos. 10-15 fotos en alta resolución, orientación variada, para alimentar perfiles que aceptan galería.

---

## 5. Notas sobre redes sociales (sección 9 hoja NAP)

Hoy el sitio **no enlaza** a Facebook, Instagram, LinkedIn, YouTube ni TikTok. Antes de empezar con los registros en directorios, crea al menos:

- Facebook Business Page (5 min)
- Instagram Business (5 min, vincula a Facebook)
- LinkedIn Company Page (10 min)
- YouTube canal (5 min)

Cuando los tengas, actualiza la sección 9 de `nap-destaperapido.md` con las URLs. Muchos directorios chilenos piden esos campos opcionales y los usan como prueba adicional de que la empresa existe (boost SEO indirecto).
