# Instalación del pack `seo-skills`

## 1. Importar las skills a otro proyecto

Las skills de Claude Code viven en `<proyecto>/.claude/skills/<nombre-skill>/SKILL.md` (skills de proyecto) o en `~/.claude/skills/<nombre-skill>/SKILL.md` (skills globales).

### Opción A — copiar al proyecto destino (recomendado)

```bash
# Desde la raíz del proyecto destino
mkdir -p .claude/skills
cp -R /ruta/a/seo-skills/skills/* .claude/skills/
```

### Opción B — instalar globalmente

```bash
mkdir -p ~/.claude/skills
cp -R /ruta/a/seo-skills/skills/* ~/.claude/skills/
```

### Opción C — symlink (para iterar el pack en muchos proyectos)

```bash
ln -s /ruta/a/seo-skills/skills/seo-audit-onpage .claude/skills/seo-audit-onpage
# Repetir por cada skill
```

---

## 2. Verificar que Claude Code las ve

Reinicia la sesión y escribe en el prompt:

```
/
```

Deberías ver `seo-audit-onpage`, `seo-zona-nueva`, etc. en el listado de skills.

---

## 3. Importar templates y workflows

Los archivos en `templates/` y `workflows/` **no son skills** — son recursos que las skills consultan. Cópialos a un lugar accesible del proyecto:

```bash
mkdir -p docs/seo
cp -R seo-skills/templates docs/seo/
cp -R seo-skills/workflows docs/seo/
```

Las skills referencian estas rutas relativas dentro de su contenido — si las pones en otro lugar, ajusta los paths en cada `SKILL.md`.

---

## 4. Instalar MCPs (opcional pero recomendado)

Ver `MCP.md`. Resumen mínimo:

```bash
# Fetch (HTTP requests para verificar metas en producción)
claude mcp add fetch --scope user -- npx -y @modelcontextprotocol/server-fetch

# Playwright (navegar y screenshots para CWV / SEO visual)
claude mcp add playwright --scope user -- npx -y @playwright/mcp@latest
```

---

## 5. Instalar herramientas npm de auditoría

Ver `npm-tools.txt`. Para empezar:

```bash
pnpm add -D lighthouse pa11y broken-link-checker html-validate sitemap-validator
```

---

## 6. Adaptar al proyecto destino

Cada `SKILL.md` tiene una sección **`Datos del proyecto`** con valores hardcoded para Full Fosas (teléfono, dominio, marca). Si exportas a otro proyecto, edita esos bloques o moverlos a un archivo `seo-skills/contexto-proyecto.md` y referenciarlo desde las skills.
