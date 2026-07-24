# Validación de la apuesta "todo por Claude Code, no por APIs" (dixdybot)

Fecha de investigación: 2026-07-23. Contexto: destaperapido.cl tiene un auto-respondedor de WhatsApp
en producción cuyo cerebro es `claude -p` (Claude Code CLI, sin API key), y Alejandro quiere
rediseñarlo como "dixdybot" multi-canal. Esta investigación valida (o matiza) esa apuesta con
fuentes oficiales de Anthropic y experiencia de la comunidad.

---

## (a) ¿Es viable y está permitido usar Claude Code con suscripción (Pro/Max) como cerebro de un bot de producción 24/7?

### Lo técnico: SÍ es viable y está documentado oficialmente

- `claude -p` (modo headless/print) es una superficie oficial y de primera clase: la doc
  "Run Claude Code programmatically" (https://code.claude.com/docs/en/headless) documenta
  `-p`, `--output-format json|stream-json`, `--json-schema`, `--continue`/`--resume`,
  `--allowedTools`, `--append-system-prompt`, y hasta el campo `total_cost_usd` en la salida JSON
  para rastrear gasto por invocación.
- Para entornos sin navegador existe `claude setup-token`: genera un token OAuth de **1 año**
  que se exporta como `CLAUDE_CODE_OAUTH_TOKEN`. Requiere plan Pro, Max, Team o Enterprise y
  "solo puede hacer peticiones de modelo" (https://code.claude.com/docs/en/authentication,
  sección "Generate a long-lived token").
- El login normal por `/login` **caduca** (Claude Code avisa 3 días antes: "Your login expires
  in 3 days · run /login to renew"). La propia doc advierte que las sesiones desatendidas
  "dejan de progresar cuando la credencial caduca" — para un bot 24/7 el token de `setup-token`
  es la vía, no el login interactivo.

### Lo legal: ZONA GRIS con letra oficial en contra para "productos"

La página oficial **Legal and compliance** (https://code.claude.com/docs/en/legal-and-compliance)
dice textualmente (traducido):

1. "Los límites de uso anunciados para los planes Pro y Max **asumen un uso ordinario e
   individual** de Claude Code y del Agent SDK."
2. "La autenticación OAuth está pensada **exclusivamente** para compradores de los planes...
   y está diseñada para soportar el **uso ordinario de Claude Code y otras aplicaciones nativas
   de Anthropic**."
3. "Los **desarrolladores que construyen productos o servicios** que interactúan con las
   capacidades de Claude, **incluidos los que usan el Agent SDK, deben usar autenticación por
   API key**... Anthropic **no permite** a desarrolladores terceros ofrecer login de Claude.ai
   ni **enrutar peticiones a través de credenciales de planes Free/Pro/Max en nombre de sus
   usuarios**."
4. "Anthropic se reserva el derecho de tomar medidas para hacer cumplir estas restricciones
   **y puede hacerlo sin previo aviso**."

Interpretación honesta para el caso dixdybot:

- Un bot de WhatsApp que **atiende clientes del negocio 24/7** es, según la letra de esa página,
  un "producto o servicio" → el camino explícitamente bendecido es **API key** (Commercial Terms),
  no OAuth de suscripción.
- El matiz a favor: la prohibición dura apunta a "desarrolladores terceros" que enrutan tráfico
  de **sus usuarios** por credenciales de suscripción (revender acceso, SaaS multi-tenant).
  Alejandro usando SU propia Max para SU propio negocio no es reventa — la comunidad lo clasifica
  como "gris": la guía de claudefa.st (https://claudefa.st/blog/guide/development/claude-code-subscription)
  resume la regla práctica como "una persona, una suscripción, un beneficiario" y pone
  "bots de Slack multi-usuario / herramientas que benefician a otros" en la franja gris, y
  "productos donde usuarios finales golpean tu token OAuth" en la franja de baneo.
- **Precedente real de endurecimiento**: en 2025-2026 Anthropic bloqueó tokens OAuth de
  suscripción en harneses de terceros (OpenClaw, OpenCode) y actualizó docs con "OAuth tokens
  obtained through Claude Free, Pro, or Max accounts cannot be used in any product, tool, or
  service" (caso documentado: https://daveswift.com/claude-trouble/). Ojo: eso aplica a
  **herramientas de terceros**; usar el CLI oficial `claude -p` NO es un harness de terceros.
- **Límites semanales (agosto 2025)**: Anthropic introdujo topes semanales el 28-08-2025
  **explícitamente para frenar a quienes corrían Claude Code 24/7 en background** y el
  account-sharing (TechCrunch: https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/).
  Cifras publicadas entonces: Max 5x ($100/mes) ≈ **140–280 h/semana de Sonnet + 15–35 h/semana
  de Opus**; Max 20x ($200/mes) ≈ **240–480 h Sonnet + 24–40 h Opus**. Además hay ventanas de
  5 horas (buckets de sesión). La página oficial del plan Max
  (https://support.claude.com/en/articles/11049741-what-is-the-max-plan) confirma "dos límites
  semanales" y que Anthropic "puede limitar el uso de otras formas... a su discreción".
  Los límites se **comparten** entre Claude.ai, Claude Code y el Agent SDK
  (https://support.claude.com/en/articles/11145838): el bot compite con el uso interactivo de
  Alejandro y con los loops nocturnos de DIXDY.

**Respuesta corta (a):** técnicamente sí y con soporte oficial de headless; legalmente es zona
gris tolerada para automatización personal del dueño, pero para un bot comercial de producción
la letra oficial apunta a API key, y Anthropic puede endurecer sin aviso (ya lo hizo dos veces).
Riesgo real: throttling semanal antes que baneo, y baneo si algún día huele a multi-tenant.

### Gotcha técnico crítico descubierto (futuro cercano)

La doc de headless dice que `--bare` "es el modo recomendado para llamadas de script y SDK, y
**será el default de `-p` en un release futuro**" — y **bare mode NO lee OAuth ni keychain ni
`CLAUDE_CODE_OAUTH_TOKEN`**: exige `ANTHROPIC_API_KEY` o `apiKeyHelper`
(https://code.claude.com/docs/en/headless#start-faster-with-bare-mode). Es decir: **Anthropic ya
está empujando el uso scriptado de `claude -p` hacia API key**. Un bot que hoy vive de la
suscripción vía `-p` puede romperse en un update automático del CLI (los installs nativos se
auto-actualizan). Mitigación: fijar canal `stable`/`minimumVersion`, no pasar `--bare`, y tener
failover listo.

---

## (b) ¿Claude Code corre igual de bien en un VPS Linux headless? ¿Qué se pierde vs Mac local?

### Soporte oficial: Linux es plataforma de primera clase

- Requisitos (https://code.claude.com/docs/en/setup): Ubuntu 20.04+, Debian 10+, Alpine 3.19+,
  4 GB RAM, x64/ARM64. Instalador nativo (`curl -fsSL https://claude.ai/install.sh | bash`) o
  **repos firmados apt/dnf/apk** oficiales. El binario es nativo (no necesita Node en runtime;
  el paquete npm pide Node 22+ solo para instalar).
- Login sin navegador: el flujo "paste code" está documentado para SSH/WSL/containers, y para
  producción se usa `claude setup-token` (generado una vez en una máquina con navegador) +
  `CLAUDE_CODE_OAUTH_TOKEN` en el servidor.
- La inferencia ocurre en la nube: **la calidad del modelo es idéntica** en Mac o VPS. Lo que
  cambia es el entorno de herramientas (bash, archivos) — en Linux funciona igual o mejor.

### Qué se pierde vs el Mac de Alejandro

1. **Keychain cifrado**: en macOS las credenciales van al Keychain; en Linux quedan en
   `~/.claude/.credentials.json` con permisos 0600 (texto plano) — hay que cuidar el acceso al VPS.
2. **launchd**: los motores DIXDY usan launchd; en VPS sería systemd/cron (equivalente, pero es
   migración).
3. **El ecosistema local ya montado**: la instancia viva del whatsapp-bot, dashboard :8789,
   Tailscale al iPhone, sesión Baileys, `envios.jsonl`, Chrome con perfil para GSC — todo eso vive
   en el Mac. El CLI corre igual en VPS, pero mover el sistema completo no es trivial.
4. **Auto-updates**: en VPS conviene canal `stable` y `minimumVersion` para que un update no
   rompa el bot de madrugada (el instalador nativo se actualiza solo).

### Experiencia de la comunidad

Es un camino muy transitado: guía de VPS de claudefa.st
(https://claudefa.st/blog/guide/development/infraops-vps-guide), gist de setup headless en VPS
(https://gist.github.com/coenjacobs/d37adc34149d8c30034cd1f20a89cce9), artículo de cómo correr
el CLI headless con suscripción sin API key
(https://medium.com/@nimeshka/how-to-run-the-claude-code-cli-completely-headless-without-paying-for-api-keys-e04a72559f0f).
Advertencias recurrentes de la comunidad: (1) `claude -p` sin streaming bufferiza toda la salida
hasta terminar (usar `--output-format stream-json` si se necesita progreso), (2) el loop agéntico
consume muchos más tokens de lo esperado y "pega directo al pool de la suscripción", (3) en
servidores lo práctico es API key.

**Respuesta corta (b):** sí, corre igual de bien (Linux es plataforma soportada con repos
firmados); lo que se pierde es Keychain, launchd y el ecosistema local ya integrado en el Mac.
Para dixdybot en un Mac local no hay impedimento; el VPS es una opción real si algún día hace
falta, con `setup-token` o (mejor, para cumplir términos) API key.

---

## (c) Plan de resiliencia: failover AUTOMÁTICO a API de pago / Bedrock / Vertex

### Claude Code soporta nativamente los tres backends

Documentado en https://code.claude.com/docs/en/third-party-integrations y
https://code.claude.com/docs/en/authentication (precedencia de credenciales):

1. Proveedores cloud si `CLAUDE_CODE_USE_BEDROCK=1` / `CLAUDE_CODE_USE_VERTEX=1` /
   `CLAUDE_CODE_USE_FOUNDRY=1` (con `AWS_REGION`, `ANTHROPIC_VERTEX_PROJECT_ID` +
   `CLOUD_ML_REGION`, etc.)
2. `ANTHROPIC_AUTH_TOKEN` (bearer, para gateways)
3. `ANTHROPIC_API_KEY` — **en modo `-p` "the key is always used when present"** (sin prompt de
   aprobación). Esto es oro para failover: basta exportar la variable en el reintento.
4. `apiKeyHelper` (script que devuelve una key; refresco configurable con
   `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`)
5. `CLAUDE_CODE_OAUTH_TOKEN` (token de setup-token)
6. OAuth de suscripción (login normal)

Consecuencia práctica: **la misma prompt, el mismo harness, el mismo `claude -p`** funcionan con
suscripción, API directa, Bedrock o Vertex — solo cambian variables de entorno. No hay que
reescribir nada del cerebro.

### Cómo detectar el fallo para conmutar

- `--output-format stream-json` emite eventos `system/api_retry` con categoría de error
  tipada: `rate_limit`, `overloaded`, `billing_error`, `authentication_failed`,
  `oauth_org_not_allowed`, `server_error`, etc. (tabla en
  https://code.claude.com/docs/en/headless). Eso permite distinguir "límite semanal agotado"
  de "caída transitoria".
- Exit code ≠ 0 + mensaje de límite en stderr es la señal burda pero suficiente para un wrapper.

### Diseño de failover recomendado (wrapper de ~30 líneas en el bot)

```
intento 1: claude -p ... (suscripción Max, sin ANTHROPIC_API_KEY en el env)
  └─ si error ∈ {rate_limit persistente, oauth_org_not_allowed, authentication_failed, login expirado}:
intento 2: ANTHROPIC_API_KEY=sk-... claude -p ...   (misma prompt, factura API)
  └─ si también falla (caída de Anthropic):
intento 3: CLAUDE_CODE_USE_BEDROCK=1 AWS_REGION=us-east-1 claude -p ...  (opcional, requiere cuenta AWS con Bedrock habilitado)
```

Cuidados:
- **No dejar `ANTHROPIC_API_KEY` exportada globalmente**: en `-p` siempre gana y facturaría API
  en silencio aunque la suscripción esté disponible (gotcha confirmado por comunidad y por la
  precedencia oficial).
- La salida `--output-format json` trae `total_cost_usd`: registrar cuánto costó cada mensaje
  que cayó en failover (con suscripción reporta el costo teórico; con API es gasto real).
- Alternativa oficial semi-automática: al agotar límites, la cuenta puede habilitar
  "usage credits / pay-as-you-go a tarifas API estándar" con consentimiento explícito
  (https://support.claude.com/en/articles/11145838) — pero es un toggle de cuenta, no
  automatizable por bot; el wrapper con env var es el failover real.
- El **Agent SDK** (Python/TS) usa el mismo harness y las mismas variables (`apiKeyHelper`,
  `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` "aplican al CLI y a las superficies que lo
  envuelven, incluido el Agent SDK" — doc de authentication), así que migrar de `claude -p` a
  SDK no cambia el plan de failover. Eso sí: la letra legal dice que productos con Agent SDK
  deben usar API key.

**Respuesta corta (c):** el failover automático es no solo posible sino barato: mismo binario,
misma prompt, un wrapper que reintenta con `ANTHROPIC_API_KEY` (y opcionalmente
`CLAUDE_CODE_USE_BEDROCK/VERTEX`). Los tres backends están soportados oficialmente por Claude Code.

---

## (d) Comparación de costos realista: ~100–300 invocaciones/día de cerebro conversacional

Precios API vigentes (skill oficial claude-api, cache 2026-06-24): Sonnet 5 **$3/$15** por MTok
(intro $2/$10 hasta 2026-08-31), Haiku 4.5 **$1/$5**, Opus 4.8 **$5/$25**. Cache read ≈ 0.1× el
input; cache write 1.25×. Suscripciones: Pro $20/mes, Max 5x $100/mes, Max 20x $200/mes
(https://claude.com/pricing).

### Escenario A — cerebro "delgado" por API directa (prompt propia: persona + tarifario + 60 msgs)

Supuestos (ESTIMACIÓN, no medición): ~6k tokens input/invocación (≈4k cacheables), ~400 tokens
output. 9.000 invocaciones/mes (300/día).

| Modelo | 100/día | 300/día |
|---|---|---|
| Haiku 4.5 | ≈ $9–13/mes | ≈ $27–40/mes |
| Sonnet 5 (intro $2/$10) | ≈ $18–27/mes | ≈ $55–80/mes |
| Sonnet 5 (pleno $3/$15) | ≈ $27–40/mes | ≈ $80–120/mes |
| Opus 4.8 | ≈ $65–90/mes | ≈ $190–270/mes |

### Escenario B — cerebro vía `claude -p` (harness completo) facturado a API

El harness de Claude Code carga su system prompt (~15–25k tokens) + CLAUDE.md + tools + loop
agéntico por invocación. Estimación: 20–50k tokens input-equivalentes por mensaje. A tarifa
Sonnet plena eso es ~$0.08–0.30/invocación → **$250–900/mes a 300/día** (el caching de prefijo
ayuda solo si las invocaciones caen dentro del TTL de 5 min y el prefijo es byte-idéntico).
Conclusión: pagar `claude -p` por API es la peor combinación; el harness solo sale a cuenta
con tarifa plana de suscripción.

### Escenario C — cerebro vía `claude -p` con Max (lo actual)

300 invocaciones/día de 30–60 s ≈ 2,5–5 h/día ≈ **17–35 "horas Claude Code"/semana**, dentro
del rango Sonnet de Max 5x (140–280 h/sem) incluso sumando el uso interactivo de Alejandro,
pero justo o corto si el cerebro usa Opus (15–35 h/sem en Max 5x). Costo marginal: $0 sobre los
$100–200/mes que ya se pagan. Riesgos: buckets de 5 h en ráfagas, límites compartidos con todo
el uso de la cuenta, y que las cifras son "aproximadas" y modificables a discreción de Anthropic.

### Lectura

- Mientras el volumen sea 100–300/día y ya exista Max: la suscripción es imbatible en precio
  ($0 marginal) — por eso la apuesta actual "funciona".
- Pero el failover a API del mismo `claude -p` es caro (Escenario B). El failover barato exige
  un **camino API delgado** (Escenario A): con Haiku/Sonnet + caching, TODO el tráfico del bot
  por API costaría $30–120/mes — menos que una Max 5x. O sea: la API directa no es solo el plan
  B legal, es competitiva en precio si la prompt es delgada.

---

## (e) Veredicto: ¿es sensata la arquitectura "cerebro = Claude Code local + fallback API"?

**Sensata a corto plazo, con dos correcciones obligatorias y una evolución recomendada.**

Lo que está bien de la apuesta:
- `claude -p`/Agent SDK headless es superficie oficial, estable y con JSON estructurado,
  costo por invocación reportado y streaming.
- Con Max ya pagada, el costo marginal del cerebro es $0 y el volumen actual cabe en los
  límites semanales.
- El failover a API/Bedrock/Vertex es trivial (mismas prompts, variables de entorno) — la
  parte (c) de la apuesta es sólida y hay que implementarla YA, no "si falla".

Lo que está mal o frágil:
1. **Cumplimiento**: la página legal oficial dice que productos/servicios (incl. Agent SDK)
   deben usar API key y que los límites Pro/Max asumen "uso ordinario e individual". Un bot
   comercial 24/7 es exactamente el patrón que motivó los límites semanales de ago-2025.
   Para UN bot del propio dueño es gris tolerado; para **dixdybot multi-cliente** (varios
   negocios DIXDY colgando de una Max) cruza a la franja prohibida ("enrutar peticiones de
   credenciales Pro/Max en nombre de tus usuarios") → ahí es API sí o sí.
2. **Fragilidad técnica**: `--bare` será default de `-p` y no lee OAuth → fijar versión/canal
   stable, no usar `--bare` con suscripción, monitorear release notes. El login de `/login`
   caduca; usar `claude setup-token` (1 año). No dejar `ANTHROPIC_API_KEY` exportada.
3. **Eficiencia**: el harness completo por mensaje conversacional es una excavadora para
   clavar un clavo. El día que el tráfico caiga a API, la factura del harness (Escenario B)
   dolerá.

**Arquitectura recomendada (evolución, no revolución):**
- **Hoy**: mantener `claude -p` con Max como cerebro en el Mac + wrapper de failover automático
  a `ANTHROPIC_API_KEY` (misma prompt). Detectar `rate_limit`/`oauth_org_not_allowed` en
  stream-json. Fijar canal stable del CLI.
- **Siguiente paso (dixdybot)**: separar dos vías. (1) Mensajes conversacionales (90% del
  tráfico: cotizar, responder, agendar) → llamada API Messages directa con prompt delgada +
  prompt caching (Haiku/Sonnet, $30–120/mes todo incluido) — cumple términos y es más rápida.
  (2) Tareas agénticas donde el harness aporta de verdad (aprender.mjs, crear "caminos",
  reanálisis, entrenamiento, tocar archivos) → Claude Code/Agent SDK local con la Max, que es
  el uso "ordinario e individual" del dueño que los términos sí contemplan.
- **Si dixdybot se vende a varios clientes**: API key por cliente (o Bedrock/Vertex), nunca la
  Max de Alejandro enrutando tráfico de terceros.

No encontré (lo digo explícitamente): cifras oficiales actuales de horas semanales en
support.claude.com (las cifras 140–280/240–480 h provienen del anuncio de ago-2025 recogido por
prensa y guías; la página oficial del Max confirma la existencia de los dos límites semanales
pero ya no publica las horas), ni casos documentados de baneo por usar el CLI oficial `claude -p`
con suscripción propia en bajo volumen (los lockouts documentados fueron por harneses de
terceros usando tokens OAuth).

---

## Fuentes

Oficiales (Anthropic):
- https://code.claude.com/docs/en/legal-and-compliance — términos, OAuth vs API key, "ordinary individual usage"
- https://code.claude.com/docs/en/authentication — precedencia de credenciales, setup-token, expiración de login
- https://code.claude.com/docs/en/headless — claude -p, stream-json, api_retry, --bare y su futuro default
- https://code.claude.com/docs/en/third-party-integrations — CLAUDE_CODE_USE_BEDROCK/VERTEX/FOUNDRY, gateways
- https://code.claude.com/docs/en/setup — requisitos Linux, repos apt/dnf/apk firmados, auto-update
- https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan — límites compartidos, pay-as-you-go
- https://support.claude.com/en/articles/11049741-what-is-the-max-plan — precios Max, dos límites semanales
- https://claude.com/pricing — precios de planes
- Skill claude-api (Anthropic, cache 2026-06-24) — precios por token de Opus 4.8/Sonnet 5/Haiku 4.5 y economía del caching

Prensa y comunidad:
- https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/ — límites semanales y su motivación (uso 24/7)
- https://daveswift.com/claude-trouble/ — lockout de tokens OAuth Max en herramientas de terceros
- https://claudefa.st/blog/guide/development/claude-code-subscription — franjas seguro/gris/baneable
- https://claudefa.st/blog/guide/development/infraops-vps-guide — setup en VPS
- https://gist.github.com/coenjacobs/d37adc34149d8c30034cd1f20a89cce9 — automatización headless en VPS
- https://medium.com/@nimeshka/how-to-run-the-claude-code-cli-completely-headless-without-paying-for-api-keys-e04a72559f0f — headless con suscripción
- https://autonomee.ai/blog/claude-code-terms-of-service-explained/ — análisis de términos
