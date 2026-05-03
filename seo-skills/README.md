# SEO Skills · Limpia Fosas + Baños Químicos (Chile)

Pack de **skills, MCPs y herramientas npm** pensado para sitios estáticos del rubro de:

- Limpieza de fosas sépticas
- Destape de alcantarillado
- Arriendo de baños químicos

Optimizado para mercado chileno (RM, regiones), búsquedas locales y long-tail por zona.

---

## Contenido

```
seo-skills/
├── README.md              ← Este archivo (índice general)
├── INSTALACION.md         ← Cómo importar las skills a otro proyecto
├── MCP.md                 ← Servidores MCP recomendados + comandos
├── npm-tools.txt          ← Lista curada de paquetes npm para auditar SEO
│
├── skills/                ← Skills invocables desde Claude Code (/<nombre>)
│   ├── seo-audit-onpage/      → Auditoría on-page de una página
│   ├── seo-zona-nueva/        → Crear página nueva de zona (urbano/rural)
│   ├── seo-servicio-nuevo/    → Crear página de servicio
│   ├── seo-meta-unicos/       → Generar/revisar titles + meta descriptions únicos
│   ├── seo-schema-jsonld/     → JSON-LD (LocalBusiness, Service, FAQ, Breadcrumb)
│   ├── seo-enlazado-interno/  → Auditar y reforzar interlinking
│   ├── seo-sitemap-robots/    → Mantener sitemap.xml y robots.txt
│   ├── seo-blog-articulo/     → Redactar artículo de blog largo (EEAT)
│   ├── seo-keywords-locales/  → Investigación de keywords long-tail por comuna
│   └── seo-core-web-vitals/   → Auditar CWV con Lighthouse y corregir
│
├── templates/             ← Plantillas reutilizables
│   ├── zona-template.html
│   ├── servicio-template.html
│   └── jsonld-snippets.md
│
└── workflows/             ← Procesos completos paso a paso
    ├── flujo-pagina-nueva.md   → Checklist al agregar página
    └── flujo-mensual.md        → Mantenimiento SEO mensual
```

---

## Cómo usar este pack

1. **Instalar las skills:** ver `INSTALACION.md`. Resumen: copiar la carpeta `skills/` a `.claude/skills/` del proyecto destino.
2. **Instalar MCPs útiles:** ver `MCP.md` para Lighthouse, Playwright, Fetch, etc.
3. **Instalar herramientas npm de auditoría:** ver `npm-tools.txt`.
4. **Ejecutar workflows:** desde Claude Code escribes `/seo-audit-onpage`, `/seo-zona-nueva`, etc.

---

## Filosofía

- **Local first:** todas las skills asumen mercado chileno y palabras clave en español de Chile (uso de "comuna", "RUT", "fosa séptica", "WPI", etc.).
- **Contenido único por página:** cero duplicate content entre comunas similares.
- **EEAT:** experiencia, expertise, autoridad y confianza son el norte (años de operación, número de servicios, reseñas reales, casos reales).
- **Sitio estático rápido:** Core Web Vitals primero, JS al mínimo, imágenes `webp` con `loading="lazy"`.
- **Reglamentos vigentes:** referencias al **DS 236/1926** (sanitario), normas de retiro de RILes y OS-10 cuando aplique.

---

## Mantenedor

Pack creado por/para Alejandro Rivera Carrasco (`rivera.ale982@gmail.com`).
Marca de referencia: **Full Fosas** — `limpiafosasydestape.cl`.
