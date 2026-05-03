# MCPs recomendados para SEO

Servidores MCP (Model Context Protocol) que **complementan** las skills de este pack. Todos opcionales — las skills funcionan sin ellos pero rinden más con ellos.

> Comandos para Claude Code (CLI). Para Claude Desktop la config va en `claude_desktop_config.json`.

---

## 1. `fetch` — descargar HTML / JSON

**Para qué:** verificar metas en producción, comparar con páginas de la competencia, leer respuestas de robots.txt o sitemap.xml en vivo.

```bash
claude mcp add fetch --scope user -- npx -y @modelcontextprotocol/server-fetch
```

**Uso típico:**
> "Trae el HTML de `https://www.competidor.cl/zonas/colina/` y compáralo con el nuestro."

---

## 2. `playwright` — navegador headless

**Para qué:** auditar Core Web Vitals reales, capturar screenshots para revisión visual, validar que el JS no rompe nada, scraping ético de SERPs propias (no recomendado para Google directo — usa la API).

```bash
claude mcp add playwright --scope user -- npx -y @playwright/mcp@latest
```

**Uso típico:**
> "Abre `localhost:3000/zonas/rural/colina.html` y dame LCP, CLS y FID estimado."

---

## 3. `filesystem` — ya viene implícito

Claude Code accede al filesystem con sus tools nativas (`Read`, `Write`, `Edit`). No necesitas un MCP aparte salvo que quieras restringir el acceso.

---

## 4. `puppeteer` (alternativa a Playwright)

Si ya usas Puppeteer en tus scripts.

```bash
claude mcp add puppeteer --scope user -- npx -y @modelcontextprotocol/server-puppeteer
```

---

## 5. `git` — historial y diffs

**Para qué:** entender qué páginas SEO se modificaron recientemente, diff de metas entre versiones.

```bash
claude mcp add git --scope user -- npx -y @modelcontextprotocol/server-git
```

> Nota: Claude Code ya tiene Bash, así que `git log` / `git diff` funcionan sin MCP. Este servidor expone una API más estructurada si la necesitas.

---

## 6. `sqlite` — para tracking propio

**Para qué:** mantener una base local de keywords objetivo, posiciones tracked, páginas auditadas, historial de cambios. Útil si quieres construir un "panel SEO" simple.

```bash
claude mcp add sqlite --scope user -- npx -y @modelcontextprotocol/server-sqlite --db-path ~/.seo-tracker.db
```

---

## 7. MCPs de SEO específicos (comunidad, evaluar antes de usar)

> Verifica el repositorio y los permisos antes de instalar — son de terceros.

- **DataForSEO MCP** — datos de keywords, SERP, backlinks (requiere cuenta paga DataForSEO).
- **Ahrefs / Semrush MCPs no oficiales** — algunos en GitHub, calidad variable. No los uses sin auditar.
- **Google Search Console MCP** — algunos forks en GitHub. La forma "oficial" es seguir usando la GUI o la API directamente. Si encuentras uno confiable, conéctalo con OAuth de tu cuenta GSC.

**Recomendación:** para datos de SERP/keywords prefiere **API directa + script Node propio** antes que un MCP comunitario sin firmar. La privacidad y los costos importan.

---

## Cómo gestionarlos

```bash
claude mcp list                    # listar instalados
claude mcp remove fetch            # eliminar uno
claude mcp get fetch               # ver detalle de uno
```

Scope `--scope user` los hace globales (todos tus proyectos). `--scope project` los deja sólo en este repo (`.mcp.json`).

---

## Mínimo viable para empezar

```bash
claude mcp add fetch --scope user -- npx -y @modelcontextprotocol/server-fetch
claude mcp add playwright --scope user -- npx -y @playwright/mcp@latest
```

Con esos dos cubres el 80% del trabajo SEO técnico desde Claude Code.
