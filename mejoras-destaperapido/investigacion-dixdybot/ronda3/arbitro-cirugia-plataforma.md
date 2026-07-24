# Arbitraje: "cirugía de plataforma" (ChatGPT) vs reescritura multi-tenant (Gemini) vs evolución incremental E0-E6 (plan propio)

**Fecha:** 2026-07-23. **Rol:** árbitro verificador con fuente primaria.
**Insumos leídos:** `mejoras-destaperapido/investigacion-dixdybot/ronda2/plan-revisado.md` (23-jul) y
`mejoras-destaperapido/investigacion-dixdybot/auditoria-arquitectura-bot.md` (23-jul, commit `cf457ec`).
**Fuentes externas:** solo docs oficiales de Shopify, WordPress, Slack y OpenAI (2 páginas por plataforma, todas consultadas el 2026-07-23).

---

## 1. (a) ¿El patrón "manifest + schema-driven UI" es el estándar real? SÍ — verificado en las 4 plataformas

| Plataforma | Qué verifica la doc primaria | Fuente (consultada 2026-07-23) |
|---|---|---|
| **Shopify theme app extensions** | Los app blocks declaran `"settings": [...]` en un bloque `{% schema %}` JSON y **el theme editor renderiza la UI del comerciante desde esa declaración** ("These settings appear in the theme editor when the block is selected"). Manifest: `shopify.extension.toml` (nombre y tipo de extensión). | shopify.dev/docs/apps/build/online-store/theme-app-extensions + …/theme-app-extensions/configuration |
| **WordPress Settings API** | "Allows admin pages containing settings forms to be managed **semi-automatically**": se registran settings/secciones/campos y WP maneja render, guardado de `$_POST` y "extra security measures such as nonces, etc. **for free**". `register_setting()` acepta `type`, `sanitize_callback`, `default` y `show_in_rest` con clave `'schema'` (JSON Schema real). | developer.wordpress.org/plugins/settings/settings-api/ + …/reference/functions/register_setting/ |
| **Slack app manifest** | "Manifests are YAML or JSON-formatted configuration bundles for Slack apps"; hay **schema de validación** y referencia completa: `display_information`, `features`, `oauth_config` (scopes = permisos), `settings` (eventos), `functions` con inputs/outputs, `workflows`, `datastores`, incluso `mcp_servers`. | docs.slack.dev/app-manifests/configuring-apps-with-app-manifests + docs.slack.dev/reference/app-manifest |
| **OpenAI Apps SDK** | Construido sobre MCP: "your server advertises the tools it supports, **including their JSON Schema input and output contracts**", y cada tool "can optionally point to an embedded resource that represents the interface to render in the ChatGPT client" — el host renderiza el componente desde la declaración. | developers.openai.com/apps-sdk + …/apps-sdk/concepts/mcp-server |

**Veredicto (a): CONFIRMADO.** ChatGPT no inventó el patrón: declaración (manifest/schema) → el host renderiza la UI y aplica permisos es exactamente cómo Shopify, WordPress, Slack y OpenAI resuelven la extensibilidad. Cuatro fuentes primarias independientes, doble página cada una.

**PERO — el contexto que ChatGPT omite:** en las 4 plataformas el patrón existe porque **los módulos los escriben TERCEROS** y el host debe renderizar/validar/limitar código que no controla ni confía. Shopify no conoce a los devs de apps; WordPress no conoce a los autores de plugins; Slack necesita scopes porque la app es ajena al workspace; OpenAI renderiza componentes de servidores MCP ajenos. **dixdybot no tiene autores de módulos terceros**: tarifario, entregas, caminos y cotizador son first-party, del mismo repo y el mismo equipo (la IA + Alejandro). El costo del patrón completo (registro de módulos, manifest por módulo, sistema de permisos, sandboxing) compra un problema que dixdybot no tiene hoy ni tendrá en E6 (E6 = clones config-driven, no marketplace de plugins).

---

## 2. (b) Qué dicen de verdad el plan y la auditoría

Lo que ambos externos tratan como "hueco" ya está en el plan, repartido donde paga:

- **`channel_conversation_id` YA está planificado**: E4 = "mensaje.js/convId, turno.js, canales/whatsapp/, identidad.json" (plan §E4), y la auditoría lo lista como NO-rescatable: "el acoplamiento jid/sock como identidad global (D2): multi-canal exige contacto-con-identidades (`wa:…`, `ig:…`) desde el día 1".
- **El "manifest con schema + validación" YA existe a la escala correcta**: los caminos E3 son `.md + frontmatter` (un mini-manifest por unidad de conocimiento) con **validación al guardar** (lint de frontmatter completo, ámbito válido, cero cifras — patrón Decagon, plan §E3). Eso ES schema-driven a escala first-party.
- **La config sale del código en E2**: `tarifario.json + persona.md + ajustes.json` + vistas Conocimiento/Ajustes v1. El terreno para "el panel renderiza desde schema" ya está sembrado.
- **El multi-cliente E6 NO es multi-tenant**: la doctrina DIXDY es **clon por cliente** ("datos del cliente solo en el clon", "cliente nuevo = clonar + formulario", plan §E6; CLAUDE.md maestro: cada cliente en su carpeta, mismo código, distinto `.env.local`). El aislamiento de tenant es **por instancia/proceso**, no por columna `tenant_id`. Lo que sí exige E6 es **clonabilidad**: cero rutas hardcodeadas (deuda D9) y todo config-driven.
- **La auditoría refuta la reescritura con evidencia de código**: "casi cada rareza es una cicatriz documentada de un incidente real… El rediseño debería ser una **reorganización con trasplantes** (enviar/outbox/dudas/gating/precios-patrón/aprendizaje casi intactos…), **no una reescritura desde cero**". enviar.js (Bad MAC/watchdog ✓✓), outbox.js (reconciliación anti-duplicado), dudas.js (embrión de caminos) son conocimiento anti-ban/anti-incidente pagado en producción que una reescritura tira a la basura. Además el calendario manda: la salida de Baileys debe estar lista el **30-sep-2026** (plan §2); una reescritura de 2-3 meses con el bot vivo congelado pierde esa fecha y deja el número expuesto al enforcement.

---

## 3. (c) Veredicto de ingeniería

### 3.1 Gemini (reescritura multi-tenant desde cero): REFUTADO — se ratifica el descarte del juez

Tres razones verificables: (1) la auditoría demuestra que la lógica está sana y endurecida — lo agotado es la topología, y eso se corrige con interfaces, no con páginas en blanco; (2) el modelo de negocio DIXDY es clon-por-cliente: el multi-tenant in-process resuelve un problema de plataformas SaaS con miles de tenants, no de un operador con 1-5 clientes premium; (3) la fecha dura del canal (30-sep) es incompatible con congelar el bot vivo. Riesgo clásico de segunda versión: se pierden las cicatrices (Bad MAC, ecos append, crash-loops) que ninguna spec captura.

### 3.2 ChatGPT (cirugía de plataforma de 2-3 semanas ANTES de expandir): MATIZADO — se adopta un 40%, comprimido a ~2-3 días, dentro de E2

Lo que ChatGPT acierta y el plan debe incorporar **explícitamente** (hoy está implícito o llega tarde):

**SÍ se extrae, y se extrae en E2 (no como etapa nueva, no antes de E3 como bloque de semanas):**

1. **IDs canónicos ANTES de crear datos nuevos** (~1 día). E4 ya define `convId`/identidad, pero llega DESPUÉS de E2-E3, y E2-E3 crean stores nuevos (embudo, métricas de caminos, uso/cierres por camino). Si esos nacen con clave `jid` desnuda, la deuda D2 CRECE justo antes de pagarla. Regla nueva, formal: **"desde E2, ningún archivo nuevo en `data/` usa jid como clave: usa `convId` (`wa:+569…`) vía un módulo `identidad.js` mínimo"** (20 líneas: normaliza jid↔tel↔convId; mata de paso la triplicación del cruce teléfono↔jid de D2). Los 17 stores viejos NO se migran aquí — eso sigue siendo E4, como está.
2. **Schema para la config que sale del código** (~1 día). `tarifario.json` y `ajustes.json` nacen con JSON Schema al lado, y la vista Ajustes v1 del panel **renderiza el formulario desde el schema** (patrón WordPress Settings API, verificado: registrar campo → el host renderiza y valida). Beneficio inmediato: validación al guardar gratis (coherente con el lint de E3) y cero formularios a mano cuando E6 clone el panel para otro cliente.
3. **Ledger de eventos, no bus de eventos** (~0,5-1 día). El embudo E2 ya exige eventos (chat→cotización→entrega→cobro desde envios.jsonl). Formalizarlo: `eventos.jsonl` append-only (`{ts, tipo, convId, ref}`) como fuente del embudo y de futuras integraciones. Es el "sistema de eventos" de ChatGPT reducido a la forma DIXDY (JSONL, un escritor, patrón envios.jsonl ya probado). **Nada de pub/sub, brokers ni emitters.**

**NO se construye (el 60% restante de la cirugía):**

- **`tenant_id`**: contradice el modelo clon-por-cliente. El equivalente correcto ya está en el plan: clonabilidad (matar rutas hardcodeadas D9 — añadirlo a E0/E2 como ítem barato) + config-driven total.
- **Registro de módulos con manifest + permisos**: patrón de ecosistemas de terceros (verificado §1). El frontmatter de caminos + su lint E3 es el manifest a la escala de dixdybot. Si algún día hay módulos de terceros (no está en E0-E7), se revisa.
- **Panel genérico total renderizado desde schemas**: solo Ajustes/tarifario (config plana). El Kanban, el gimnasio y los caminos tienen UX propia ya decidida (§3.2 del plan: tarjetas+diff+Aprobar); genericidad ahí sería sobre-ingeniería.

### 3.3 Dónde queda cada cosa (respuesta directa a "¿dentro de E4? ¿antes de E3?")

- **La mini-cirugía (IDs + schema-config + eventos.jsonl) entra DENTRO de E2**, sumando ~2-3 días a sus 4-5. No es etapa nueva ni va "antes de E3" como bloque: E2 ya está antes de E3 y ya toca exactamente esos archivos. Así E3 nace con claves canónicas y validación, sin mover ninguna fecha del calendario (30-sep intacto).
- **E4 sigue siendo la cirugía real del canal** (adaptador, retrofit de los 17 stores, sock fuera de integracion/seguimiento/outbox) — sin cambios; llega con menos deuda porque E2-E3 no la engordaron.
- **E6 sigue siendo clon-por-cliente** — se le añade explícitamente el rechazo documentado a tenant_id/registro de módulos, con esta evidencia como respaldo.
- **Regla de contingencia del plan (E4+E5 saltan sobre E3 si hay atraso): se refuerza** — con convId definido desde E2, ese salto cuesta menos.

### 3.4 Síntesis en una línea

ChatGPT diagnostica bien (los IDs canónicos tarde son deuda que crece) pero receta a escala equivocada (plataforma de terceros para un sistema first-party); Gemini receta la amputación; el plan propio tenía razón en la columna vertebral y solo debe **adelantar 3 convenciones baratas de E4/E6 a E2** para que nada nuevo nazca con la clave vieja.

---

## Fuentes primarias (todas consultadas el 2026-07-23)

1. Shopify — Theme app extensions: https://shopify.dev/docs/apps/build/online-store/theme-app-extensions
2. Shopify — Theme app extensions / Configuration (schema de settings, shopify.extension.toml): https://shopify.dev/docs/apps/build/online-store/theme-app-extensions/configuration
3. WordPress — Settings API: https://developer.wordpress.org/plugins/settings/settings-api/
4. WordPress — register_setting() (args con `show_in_rest.schema`): https://developer.wordpress.org/reference/functions/register_setting/
5. Slack — Configuring apps with app manifests: https://docs.slack.dev/app-manifests/configuring-apps-with-app-manifests
6. Slack — App manifest reference (propiedades completas): https://docs.slack.dev/reference/app-manifest
7. OpenAI — Apps SDK: https://developers.openai.com/apps-sdk
8. OpenAI — Apps SDK / MCP server (JSON Schema contracts + embedded resources): https://developers.openai.com/apps-sdk/concepts/mcp-server
9. Internas: `ronda2/plan-revisado.md` (23-jul-2026) y `auditoria-arquitectura-bot.md` (23-jul-2026, commit cf457ec).
