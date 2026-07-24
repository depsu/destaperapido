# El stack más simple y moderno 2026 para el núcleo dixdybot

**Fecha del informe: 23-jul-2026.** Encargo: recomendar la mejor base técnica para un núcleo
dixdybot creado de 0 — última tecnología, máxima sencillez, operado por una persona + IA
desarrolladora (Claude Code), corriendo 24/7 en un Mac mini con launchd.

## Método y calidad de la evidencia

Dos fuentes, ambas fechadas:

1. **Evidencia primaria de código:** los 8 clones de la ronda 4 siguen en
   `scratchpad/clones/` (nanoclaw actualizado al 21-jul-2026, mastra al 23-jul-2026,
   boop-agent 13-jul, builderbot 12-jul, bridge 11-jul, vocero 10-jul). Leí sus
   `package.json`, `tsconfig.json` y `pnpm-workspace.yaml` reales — no notas de blog.
2. **Fuentes oficiales vía web** (leídas 23-jul-2026): endoflife.date/nodejs,
   nodejs.org/api/sqlite.html, nodejs.org/api/typescript.html, bun.com/blog,
   zod.dev/v4, hono.dev/docs, releases de vitest y TypeScript en GitHub, y el registro
   npm directo (versiones + fecha de publicación exactas).

**Nota de contexto:** el WebSearch de la sesión estaba agotado; todo lo de web salió por
WebFetch a fuentes primarias, que es incluso mejor (cero intermediarios).

## Qué usan HOY los proyectos similares serios (leído de su código, jul-2026)

| Proyecto | Rol | Runtime | Lenguaje | DB | HTTP | Test | Repo |
|---|---|---|---|---|---|---|---|
| **NanoClaw** (30k★, espejo de E1+E4) | Bot WhatsApp + Agent SDK | Node ≥20, pnpm 10.33 | TS 5.7 `strict:true`, tsx dev / tsc build | **better-sqlite3 11.10.0** (pin exacto) | **node:http pelado** (1 webhook) | vitest 4.0, tests colocalizados | **PLANO** (un package.json, carpetas src/channels, src/db, src/cli) |
| **Mastra** (framework agentes TS) | Plataforma | Node, pnpm 11.13 | **TS 6.0.3** (catalog) | **@libsql/client 0.17.4** (uno de 20+ stores) | **Hono 4.12.8** (packages/server y deployer) | vitest 4.1.10 | Monorepo turbo (publican 30+ paquetes npm) |
| **boop-agent** | Madre→especialistas Agent SDK | Node ≥20 | TS 5.6 | Convex (app Electron) | Express 5 | vitest 4.1.10 | Plano |
| **whatsapp-agent-bridge** | Puente WA↔Agent SDK | Node | TS 5.6 | RAM (anti-ejemplo) | Express 5 | — | Plano |
| **vocero-crm** | CRM+gimnasio WhatsApp | Node ≥20, pnpm 11.5 | TS 5.7 | Postgres+Drizzle | Next.js 15 | vitest 2 | Plano |
| **builderbot** | Framework 15+ canales | Node ≥18, pnpm 9 | TS | — | polka | jest/uvu | Monorepo lerna+nx (anti-ejemplo: pesado) |
| **Bot vivo dixdy** (a reemplazar/evolucionar) | Producción | Node 22.18 en el Mac | JS ESM sin tipos | JSONL | node:http (dashboard) | tests propios | Plano |

Lectura transversal: **todos los proyectos de esta clase son TypeScript estricto sobre
Node + pnpm + vitest**; el que más se nos parece en escala y filosofía (NanoClaw) es
además **repo plano, SQLite síncrono y cero framework HTTP**. Nadie serio de esta clase
corre Bun en producción, nadie usa ORM en el núcleo del bot, nadie usa NestJS.

---

## (a) Runtime: **Node.js 24 LTS** (no Bun). Actualizar a 26 LTS en octubre.

**Estado verificado (endoflife.date, 23-jul-2026):**
- **Node 24 = Active LTS** (LTS desde oct-2025; activo hasta oct-2026, seguridad hasta
  abr-2028).
- **Node 26 = Current** (salió 5-may-2026; será LTS el 27-oct-2026).
- El Mac corre hoy Node 22.18 (Maintenance LTS) → subir a 24 es parte del arranque.

**Estado de Bun (bun.com/blog, 23-jul-2026):** última versión **1.3.14 (13-may-2026)**;
**Bun 2.0 no existe**. Cada release de la serie 1.3.x sigue anunciando "Node.js
compatibility improvements" y decenas de fixes (la 1.3.14 sola cierra 92 issues) — la
superficie de compatibilidad Node **aún no está terminada**, por admisión implícita del
propio changelog.

**Por qué Node y no Bun para ESTE sistema:**
1. **El cerebro entero vive de `child_process`**: cada turno spawnea `claude -p` / el
   Agent SDK spawnea el CLI. `child_process` de Node es la pieza más batalla-probada del
   ecosistema; en Bun es exactamente el tipo de API que sigue recibiendo parches de
   compatibilidad. Un bug sutil de spawn/stdio en un proceso 24/7 = bot mudo a las 3 AM.
2. **Baileys, el Agent SDK de Anthropic y los SDK de Meta se testean contra Node**, no
   contra Bun. Ser el caso raro = ser quien descubre los bugs.
3. **Las ventajas de Bun no aplican aquí**: arranque rápido y bundler importan en
   serverless/CLI; un daemon launchd arranca una vez por semana. `bun:sqlite` y
   `Bun.serve` son lock-in a cambio de nada que Node 24 no dé ya.
4. **Node 24 se comió las razones para salir de Node** (todo nativo, cero deps):
   type stripping de TS **estable** (ver e), `node:sqlite` (ver b), fetch/WebSocket,
   `--env-file` (adiós dotenv), `node --watch` (adiós nodemon). El "Node aburrido" de
   2026 es moderno.
5. NanoClaw, Mastra, boop, builderbot: **todos `engines: node`**. Cero de los 8 repos
   estudiados corre Bun.

**Cuándo re-evaluar Bun:** si algún día sale Bun 2.0 con la capa Node declarada completa
Y algún proyecto de esta clase (bot 24/7 + child_process + SQLite) lo corra en producción
meses. Hoy no existe ese ejemplo.

## (b) Persistencia: **SQLite con better-sqlite3** (un escritor, WAL) + JSONL solo para ledgers append-only. libsql descartado.

**Veredicto:** para un núcleo creado de 0, la decisión de la ronda 4 ("JSONL disciplinado,
SQLite como cantera") se invierte: esa decisión era correcta para la **evolución
incremental** del bot vivo; partiendo de 0, la disciplina que los planos exigen
(un-solo-escritor, ledger `delivered`, dedup por wamid, **UNIQUE(canal_id, source_id)** en
`identidades`, estados de conversación) es **exactamente lo que SQLite regala** y lo que en
JSONL hay que construir y vigilar a mano. Con 5 tablas estilo Chatwoot, SQLite ES la
opción simple, no la compleja.

- **better-sqlite3 13.0.1 (publicada 21-jul-2026, npm)** — vivísima; es la elección de
  NanoClaw (pin exacto 11.10.0), API 100% síncrona (calza con el modelo un-solo-escritor:
  sin await no hay carreras), WAL de un pragma, transacciones triviales.
- **`node:sqlite` (nativo, cero deps): el sucesor designado.** Verificado en
  nodejs.org/api/sqlite.html (23-jul-2026): ya **no es experimental** desde v22.13/v23.4 y
  es **Release Candidate (Stability 1.2)** en Node 26; API síncrona casi idéntica
  (DatabaseSync/StatementSync, prepared statements, transacciones, backup). Decisión
  práctica: **aislar todo acceso en un solo módulo `src/core/db.ts`** — migrar de
  better-sqlite3 a node:sqlite cuando madure en Node 26 LTS será cambiar UN archivo y
  borrar la única dependencia nativa del proyecto.
- **libsql (@libsql/client 0.17.4, 15-jun-2026): descartado.** Su valor es réplica/sync
  con Turso (nube) y API async — dixdybot es un proceso local single-writer; pagar un
  cliente async + un actor de nube para no usar ninguna de sus features es complejidad
  gratis. Mastra lo trae porque vende 20+ stores intercambiables; nosotros vendemos UNO.
- **JSONL no muere: queda para lo que es append-only por naturaleza** — `uso-llm.jsonl`
  (ledger de costos E1), `eventos.jsonl` (E2), transcripts. Regla simple: **estado vivo y
  claves únicas → SQLite; bitácora inmutable → JSONL.** Backup = copiar 1 archivo .db
  (launchd ya respalda auth/; se suma el .db con `VACUUM INTO`).
- Las 5 tablas del plano de oro #4 (contactos / identidades / canales / conversaciones /
  mensajes) se escriben en SQL a mano con prepared statements: **sin ORM** (ver h).

## (c) HTTP: **Hono sobre @hono/node-server** (webhooks Meta + API del panel + PWA estática).

Versiones verificadas en npm (23-jul-2026): **hono 4.12.31 (18-jul-2026)**,
**@hono/node-server 2.0.11 (21-jul-2026)**, @hono/zod-validator 0.9.0 (15-jul-2026).
Fastify 5.10.0 (5-jul-2026) también está sano — pero pierde.

**Por qué Hono:**
1. **Cero dependencias, Web Standards puros**, `hono/tiny` <14kB (hono.dev). Es el
   framework mínimo que todavía da router tipado + middleware.
2. **El mismo código corre en Node y en Cloudflare Workers.** DIXDY ya opera Workers
   (meta-buzon, avisos, correo): el handler del webhook Meta escrito en Hono se puede
   mover del Mac al Worker (o compartir validación) sin reescribir. Ningún otro candidato
   da esa portabilidad.
3. **Mastra lo eligió para su server** (hono ^4.12.8 en packages/server y deployer,
   leído del clon) — el proyecto TS de agentes más grande del momento validó exactamente
   esta pieza para exactamente este rol.
4. **@hono/zod-validator** conecta la fuente única de schemas (d) a cada endpoint en una
   línea: request inválido nunca toca la lógica.
5. Contra **Fastify**: excelente, pero su valor (throughput extremo, ecosistema de
   plugins, encapsulación) apunta a APIs grandes multi-equipo. Para ~10-15 endpoints a
   volumen de pyme es maquinaria sin uso, y su validación nativa es JSON Schema por
   ajv — chocaría con Zod como fuente única o exigiría puente.
6. Contra **node:http pelado** (lo que hace NanoClaw con SU único webhook): viable, pero
   dixdybot sirve webhooks Meta (GET verify + POST firmado) + API del panel PWA + API
   del gimnasio + estáticos. Router, parseo, firma HMAC sobre rawBody y 404s a mano son
   ~200 líneas propias que Hono da gratis y tipadas. La línea NanoClaw se cruza al tercer
   endpoint.
7. Contra **Express 5** (boop y bridge lo usan): API de 2010, middleware con mutación de
   `req`, tipos añadidos aparte. En 2026 es la opción por inercia, no por diseño.

## (d) Validación/Schemas: **Zod 4 como fuente única de verdad.** Confirmado sin matices.

**Zod 4.4.3 = latest en npm (publicada 4-may-2026); v4 estable desde 2025** (zod.dev).
Mastra la fija en su catálogo pnpm (`zod: ^4.4.3`, leído del clon 23-jul). Números de la
casa: parseo 7-14x más rápido que v3, 100x menos instanciaciones de tipos en `tsc` (esto
importa: el chequeo de tipos lo corre la IA decenas de veces al día).

La jugada que lo vuelve LA pieza central del diseño genérico-modular: **un schema Zod por
módulo alimenta los TRES contratos a la vez:**
1. **Config de módulos + panel:** `z.toJSONSchema()` es **nativo en v4** → la vista
   Ajustes renderizada-desde-schema que E2 exige sale del MISMO schema que valida el
   archivo de config al arrancar. Un módulo nuevo declara su schema y el panel lo dibuja
   solo. (El plan pedía "JSON Schema + vista Ajustes": Zod 4 lo da sin segunda fuente.)
2. **StructuredOutput del cerebro:** el JSON del turno (`{reglas_aplican, camino,
   respuesta}`, plano E3) se valida con Zod antes de tocar el mundo; y las tools del
   Agent SDK ya reciben zodShape directo (patrón boop `tool(name, desc, zodShape,
   handler)`, leído del clon). Respuesta del LLM que no parsea = fallo tipado → failover.
3. **Webhooks Meta:** payload validado en el borde con @hono/zod-validator; campos del
   cliente como no-confiables (regla del permission relay) formalizados en el schema.

Convención: schemas en `src/core/schemas/`, un archivo por módulo, `z.infer<>` como único
origen de tipos de datos. Nada de mantener interfaces TS paralelas a los schemas.

## (e) Lenguaje: **TypeScript estricto ejecutado NATIVO por Node (type stripping), sin paso de build.** No JS+JSDoc.

**El hallazgo que cambia el juego** (nodejs.org/api/typescript.html, leído 23-jul-2026):
el type stripping es **ESTABLE (Stability 2) desde Node 24.12** (y v26 le quitó hasta el
flag de transform). Es decir: `node src/index.ts` corre TypeScript directo, sin tsc, sin
tsx, sin bundler, sin dist/. El launchd apunta al .ts. Lo mejor de los dos mundos que el
dilema "TS vs JS" asumía imposible en 2024.

**Por qué TS estricto conviene DE VERDAD a un código mantenido por IA:**
1. **`tsc --noEmit` es el test más barato que existe para una IA desarrolladora**: 5
   segundos, cero mantenimiento, y caza la clase de error que la IA más comete — campos
   renombrados a medias, contratos que derivan entre módulos, null-paths olvidados. Sin
   revisor humano, cada verificador mecánico vale doble. Claude Code lo corre solo en
   cada cambio; con JSDoc el chequeo existe pero los tipos complejos (uniones
   discriminadas de `MensajeEntrante`, genéricos de `z.infer`) se vuelven ilegibles o
   imposibles de expresar.
2. **Los 6 repos TS estudiados usan strict** (nanoclaw `strict:true` explícito); ninguno
   de los proyectos serios de esta clase eligió JSDoc. La preferencia del dueño (TS
   estricto, ya en su CLAUDE.md) coincide con la práctica de la industria: cero fricción.
3. **La migración desde el bot vivo JS sigue abierta**: con type stripping, `.js` y `.ts`
   conviven en el mismo proceso sin build — `enviar.js`/`gating.js` (que el plan
   conserva) se importan tal cual y se tipan cuando toque, archivo por archivo.

**Reglas del type stripping que se vuelven convención de la casa** (limitaciones
verificadas): **prohibido `enum`** (usar uniones de literales: `type Modo = 'vendedor' |
'especialista'` — más idiomático y Zod-friendly igual), prohibido parameter properties y
namespaces con runtime, **imports con extensión `.ts` explícita** e `import type` para
tipos. tsconfig con `"strict": true, "module": "nodenext", "erasableSyntaxOnly": true,
"noEmit": true` (el compilador solo chequea, jamás emite). ESLint 9 + typescript-eslint
(setup NanoClaw) como segunda malla.

## (f) Estructura: **repo PLANO** (un package.json), carpetas como fronteras. pnpm igual. Workspaces solo si E6 lo exige algún día.

- **La evidencia manda:** NanoClaw — el análogo más cercano en tamaño y misión — es un
  repo plano con carpetas (`src/channels/`, `src/db/`, `src/cli/`) y le sobra. Los que
  usan monorepo (Mastra: turbo; builderbot: lerna+nx) lo hacen porque **publican decenas
  de paquetes npm** — dixdybot no publica nada: el clon-por-cliente copia el repo entero
  (doctrina DIXDY), y un monorepo interno no le aporta ni un feature a eso.
- **Estructura propuesta:** `src/core/` (llm, db, schemas, motor de caminos),
  `src/canales/` (baileys/, wa-cloud/, sim/ — la factory de E4), `src/panel/` (Hono
  routes + PWA estática vanilla), `src/cli/` (herramientas de operación), tests
  colocalizados (`x.test.ts` junto a `x.ts`, patrón NanoClaw/Mastra).
- **Costo de cambiar de opinión: casi cero.** Si E6 algún día justifica compartir un
  paquete entre clones vía npm privado, `pnpm workspaces` se agrega en una tarde
  (pnpm-workspace.yaml + mover carpetas). No se paga hoy la burocracia de `workspace:*`,
  versionados internos y pipelines de build para una sola persona.
- **pnpm 11.17.0 (publicada HOY 23-jul-2026)**; fijar con el campo `packageManager` +
  corepack, como NanoClaw (`pnpm@10.33.0`) y Mastra (`pnpm@11.13.1`). Pins exactos de
  deps (disciplina NanoClaw, y el plan E0 ya pedía pins).

## (g) Testing: **Vitest 4 (pineado) + los escenarios dorados como suite; el juez LLM aparte.**

- **Vitest 4.1.10 = última estable (6-jul-2026, GitHub releases)**; la 5.0 está en beta →
  **pinear 4.1.x** y no tocar la beta. Es el test runner de NanoClaw (^4.0.18), Mastra
  (4.1.10 en catalog) y boop (4.1.10): unanimidad total en la clase.
- Con Node nativo corriendo TS, vitest queda SOLO para tests (no para dev-loop), que es
  su mejor rol: watch, mocks (`vi.fn`), snapshots.
- **Dos niveles, ya diseñados por la ronda 4:** (1) unit/integración determinista en
  vitest — el motor de caminos con YAML fixtures, la ventana-24h, el resolver Kahn, dedup
  del ledger, y las **personas guionadas SIN LLM de vocero** (6 guiones = regresión
  determinista, corren en CI/pre-commit en segundos); (2) el **juez LLM** (gimnasio,
  replay, backtesting patrón Fin) queda FUERA de vitest como script propio — es caro, no
  determinista, y su veredicto ya tiene formato tipado propio. vitest da el semáforo
  barato; el juez da el gate ≥4,0 de despliegue.

## (h) Qué NO usar (y por qué, en una línea cada uno)

| NO | Por qué |
|---|---|
| **Bun** (hoy) | 1.3.x aún parchea compat Node cada release; el cerebro vive de child_process; cero ejemplos en la clase (a). |
| **Express** | API legacy; Hono lo reemplaza con cero deps y portabilidad a Workers. |
| **NestJS / AdonisJS** | Framework de equipo grande: DI, decoradores (¡rompen type stripping!), ceremonia — anti-sencillez. |
| **ORMs (Drizzle/Prisma)** | 5 tablas, un escritor, SQL a mano con prepared statements es MÁS legible para la IA que una DSL; Prisma además arrastra engine binario. |
| **Postgres / MySQL** | Servidor aparte que administrar en el Mac mini; SQLite es cero-ops y suficiente por años (ratificado ronda 4). |
| **Redis / BullMQ / colas externas** | La cola promise-chain por conversación (plano E1) + SQLite cubren el caso; un Redis caído es un modo de fallo nuevo regalado. |
| **Docker** | En un Mac mini con launchd solo agrega una VM, consumo y otra capa que muere; NanoClaw usa contenedores como SANDBOX de agentes (otro problema, que claude -p ya resuelve con permisos). |
| **turbo / nx / lerna** | Orquestación de monorepo sin monorepo (f). |
| **dotenv, nodemon, tsx en producción** | Node 24 nativo: `--env-file`, `--watch`, type stripping (tsx queda opcional solo si algún día se quisiera sintaxis no-borrable). |
| **enums de TS, decoradores, namespaces** | Rompen el type stripping nativo (e); uniones de literales en su lugar. |
| **Vitest 5 beta, TS 7/tsgo** | Beta y no-lanzado respectivamente; se adopta estable o nada. |
| **n8n / Dify / plataformas low-code** | Licencias hostiles a revender/embeber (ya descartadas en ronda 2); el gateway propio delgado está ratificado. |
| **React/Next para el panel v1** | El plan ya lo decidió: PWA vanilla + DaisyUI opcional; Next.js recién si E6 justificara reescritura. |

## EL STACK FINAL

| Pieza | Elección (versión verificada 23-jul-2026) | Por qué (corto) | Alternativa descartada |
|---|---|---|---|
| Runtime | **Node.js 24 LTS** → 26 LTS en oct-2026 | child_process sagrado para `claude -p`; LTS aburrido = 24/7; todo lo moderno ya es nativo | Bun 1.3.14 (compat Node inconclusa, cero pares en la clase) |
| Lenguaje | **TypeScript 6.0 estricto, ejecutado nativo** (type stripping estable Node 24.12+), `noEmit` | `tsc --noEmit` = el verificador más barato para una IA; sin build, launchd apunta al .ts; .js vivo convive | JS+JSDoc (tipos complejos ilegibles); build tsc/dist (paso extra sin pago) |
| Persistencia | **SQLite vía better-sqlite3 13.0.1**, WAL, un escritor, acceso aislado en `db.ts` + **JSONL para ledgers append-only** | Las UNIQUE/dedup/estados de los planos salen gratis; síncrono = sin carreras; NanoClaw lo valida | libsql (features de nube sin uso), JSONL-para-todo (disciplina a mano), Postgres (ops) |
| Sucesión DB | **node:sqlite** cuando sea stable en 26 LTS | Cero deps nativas; API casi idéntica; migración = 1 archivo | — |
| HTTP | **Hono 4.12 + @hono/node-server 2.0** | Cero deps, tipado, mismo código Mac↔Cloudflare Worker; Mastra lo eligió para lo mismo | Fastify 5 (maquinaria sin uso, valida con ajv), node:http (200 líneas propias), Express (legacy) |
| Schemas | **Zod 4.4.3 fuente única**: config módulos + StructuredOutput cerebro + webhooks; `z.toJSONSchema()` para la vista Ajustes | Un schema, tres contratos; tools del Agent SDK ya hablan Zod; Mastra lo fija en catalog | ajv/JSON Schema a mano (dos fuentes de verdad), valibot (ecosistema menor) |
| Estructura | **Repo plano**, un package.json, `src/{core,canales,panel,cli}`, tests colocalizados | NanoClaw (el análogo) le sobra así; el clon-por-cliente copia el repo, no publica paquetes | pnpm workspaces (se agrega en una tarde SI E6 lo exige), turbo/nx/lerna |
| Package manager | **pnpm 11.17** fijado con `packageManager` + pins exactos | Preferencia del dueño + práctica unánime de la clase + doctrina de pins de E0 | npm, yarn, bun install |
| Testing | **Vitest 4.1.10 pineado** para lo determinista (incl. personas guionadas); juez LLM como script aparte | Unanimidad NanoClaw/Mastra/boop; el juez es caro y no determinista → fuera del runner | Vitest 5 beta, jest (config pesada), node:test (sin watch/mocks maduros) |
| Deps runtime totales del núcleo | **~6**: baileys, better-sqlite3, hono, @hono/node-server, @hono/zod-validator, zod | La sencillez como número auditable | — |

**La frase para Alejandro:** el núcleo nuevo es "Node puro y duro versión 2026": el propio
Node ya trae casi todo (correr TypeScript, base de datos en camino, .env, watch), se le
suman solo 6 piezas pequeñas y probadas por los proyectos que admiramos, y cada una tiene
su reemplazo anotado por si el mundo se mueve. Nada que instalar aparte, nada que
administrar, y la IA puede verificar su propio trabajo en segundos.

## Encaje con el plan vigente (no contradice, precisa)

- El plan E0-E7 dice "evolución incremental, sin sistema paralelo": este stack **no exige
  big-bang** — type stripping deja convivir el JS vivo con módulos TS nuevos en el mismo
  proceso; `enviar.js`/`gating.js`/`outbox.js` se conservan tal cual el plan manda.
- La única decisión de ronda 4 que este informe **revisa** es JSONL-como-almacén-principal
  → SQLite para el estado vivo (las 5 tablas), manteniendo JSONL para bitácoras. Motivo:
  el encargo pide el núcleo "creado de 0", y ahí la balanza de sencillez se invierte.
  Si se mantuviera la evolución pura sin núcleo nuevo, la decisión JSONL de ronda 4 sigue
  siendo válida hasta que haya contención.
- Todo lo demás (Hono, Zod 4, TS estricto, vitest, repo plano, pnpm) es compatible con
  E1-E6 tal como están escritas y con la doctrina DIXDY (nativo sobre dependencias, sin
  librerías grandes sin preguntar: las 6 deps del núcleo son chicas y justificadas).

## Fuentes

**Evidencia primaria local (clones ronda 4, fechas de último commit):**
- `scratchpad/clones/nanoclaw` (21-jul-2026): package.json, tsconfig.json, src/
- `scratchpad/clones/mastra` (23-jul-2026): pnpm-workspace.yaml (catalog), packages/server/package.json, stores/libsql/package.json
- `scratchpad/clones/boop-agent` (13-jul-2026), `whatsapp-agent-bridge` (11-jul-2026), `vocero-crm` (10-jul-2026), `builderbot` (12-jul-2026): package.json
- Bot vivo: `~/SaSS/destaperapido/whatsapp-bot/package.json` + `node --version` del Mac (22.18.0)

**Web (leídas 23-jul-2026):**
- https://endoflife.date/nodejs — calendario LTS (Node 24 activo, 26 → LTS 27-oct-2026)
- https://nodejs.org/api/sqlite.html — node:sqlite Release Candidate, no-experimental desde 22.13/23.4
- https://nodejs.org/api/typescript.html — type stripping estable desde 24.12/25.2; sintaxis prohibida
- https://bun.com/blog — Bun 1.3.14 (13-may-2026), sin 2.0, compat Node en curso
- https://zod.dev/v4 — Zod 4 estable, z.toJSONSchema nativo, cifras de performance
- https://hono.dev/docs/ — cero dependencias, Web Standards, multi-runtime
- https://github.com/vitest-dev/vitest/releases — 4.1.10 estable (6-jul-2026), 5.0 en beta
- https://github.com/microsoft/TypeScript/releases — TS 6.0.3 última estable
- Registro npm directo (registry.npmjs.org, consultado 23-jul-2026): better-sqlite3 13.0.1 (21-jul), hono 4.12.31 (18-jul), zod 4.4.3 (4-may), pnpm 11.17.0 (23-jul), @libsql/client 0.17.4 (15-jun), @hono/node-server 2.0.11 (21-jul), @hono/zod-validator 0.9.0 (15-jul), fastify 5.10.0 (5-jul)

**Documentos del proyecto:**
- `mejoras-destaperapido/investigacion-dixdybot/ronda2/plan-revisado.md`
- `mejoras-destaperapido/investigacion-dixdybot/ronda4/planos-sintesis.md`
- `mejoras-destaperapido/DIXDYBOT-ESTADO.md`
