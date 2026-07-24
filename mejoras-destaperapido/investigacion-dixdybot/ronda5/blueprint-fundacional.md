# BLUEPRINT FUNDACIONAL — núcleo dixdybot

**Fecha: 23-jul-2026 · Arquitecto fundacional · Estado: diseño cerrado, listo para construir.**

Este documento ATERRIZA el plan vigente (`ronda2/plan-revisado.md`, etapas E0-E7) con la
biblioteca de planos (`ronda4/planos-sintesis.md`), los requisitos no negociables
(`DIXDYBOT-ESTADO.md`) y los 4 informes de esta ronda (stack-2026, media-ingesta-canales,
procesar-media-ia, media-ingesta). **No reemplaza el plan: le pone carpetas, contratos,
versiones y semanas.** Criterio de diseño #1 en cada decisión: SENCILLEZ — lo opera una
sola persona con IA.

---

## 0. La reconciliación: "crear de 0" Y "el bot vivo vende hoy"

Las dos frases no chocan si se separa **dónde nace el código** de **dónde corre la venta**:

- **El núcleo `dixdybot/` nace LIMPIO en el repo maestro DIXDY**, como un módulo genérico
  más, hermano de `correo-worker/`, `panel-cliente/`, `whatsapp-bot/`: plantilla
  config-driven, **cero datos de cliente**, construida con los planos de la ronda 4 y el
  stack verificado de esta ronda. No hereda deuda: hereda órganos.
- **destaperapido es el primer cliente y se estrangula POR DENTRO** (patrón strangler fig):
  la instancia viva (`~/SaSS/destaperapido/whatsapp-bot/`) sigue vendiendo sin
  interrupción mientras el núcleo la va reemplazando en 3 movimientos reversibles:
  1. **El cerebro** — `brain.js` del vivo se convierte en un shim de ~20 líneas que llama a
     `llm.ts` del núcleo. El vivo sigue mandando; el núcleo es su motor LLM. (Semana 1)
  2. **El canal** — los **órganos sanos se TRASPLANTAN, no se reescriben**: `enviar.js`,
     `gating.js`, `outbox.js`, `extraer.js`, `integracion.js` se copian tal cual a
     `src/canales/wa-baileys/legado/` y `src/organos/` del núcleo — el type stripping de
     Node 24 deja convivir `.js` y `.ts` en el mismo proceso, y se tipan archivo por
     archivo cuando toque. El proceso del núcleo reemplaza al vivo vía launchd; el vivo
     queda congelado como fallback 30 días (rollback = re-apuntar el .plist). (Semana 5)
  3. **Los datos** — un migrador one-shot lleva `conversaciones.jsonl` + `envios.jsonl` a
     las 5 tablas SQLite; los JSONL viejos quedan como archivo histórico de solo lectura.
     (Semana 5, mismo cutover)
- **Gate de corte** (nada se corta sin esto): gimnasio verde (6 personas guionadas
  deterministas) + juez LLM ≥ 4,0 + `tsc --noEmit` y vitest en verde + 48 h de sombra con
  el canal `sim` re-jugando conversaciones reales del log.

Doctrina DIXDY intacta: template en el maestro, instancia por cliente en su clon
(`data/`, `.env.local`, `auth/` — gitignored), aprendizajes se PROMUEVEN al maestro.

---

## 1. Las 10 decisiones fundacionales

| # | Decisión | Fuente |
|---|---|---|
| 1 | **Núcleo nuevo en el maestro + estrangulamiento por órganos** de destaperapido (shim cerebro → canal → datos), nunca big-bang; rollback siempre por launchd | plan E0-E7 + este blueprint |
| 2 | **Stack "Node puro 2026"**: Node 24 LTS, TS estricto ejecutado NATIVO (type stripping, sin build, launchd apunta al `.ts`), **~6 deps runtime**, pnpm 11.17, vitest 4.1.10 pineado | stack-2026 [confirmado] |
| 3 | **SQLite (better-sqlite3, WAL, un escritor, aislado en `db.ts`)** para el estado vivo (5 tablas estilo Chatwoot); **JSONL solo ledgers append-only**; `node:sqlite` anotado como sucesor = cambiar 1 archivo | stack-2026 [confirmado, invierte JSONL de r4 solo para núcleo-de-0] |
| 4 | **Zod 4 fuente única de verdad**: el mismo schema valida config de módulo, dibuja la vista Ajustes (`z.toJSONSchema()` nativo), tipa el StructuredOutput del cerebro y filtra webhooks Meta — cero interfaces paralelas | stack-2026 [confirmado] |
| 5 | **`llm.ts` puerta única con failover tipado `sdk→cli→api→plantilla`** (cola por conversación, sesión persistida en el evento `init`, costo por `modelUsage`, ledger por turno) — el seguro contra el vaivén de Anthropic; prioridad #1 | plano de oro #2 |
| 6 | **Interfaz Canal con `ventana()` y `enviarPlantilla()` de primera clase** + `MediaEntrante` con ref opaca por canal y `obtenerBinario()` lazy; el binario JAMÁS viaja por el bus; canal `sim` como ciudadano pleno | planos de oro #3 y #4 + media-ingesta-canales |
| 7 | **Caminos = azúcar sobre reglas** (proyección Parlant): UN evaluador de UNA llamada LLM por turno + resolver determinista explicable (Kahn + Resolution); campo `dominio` en el esquema desde el día 1 → la IA madre enruta EN SILENCIO al especialista, que carga SOLO su dominio | plano de oro #1 + requisito 3 de Alejandro |
| 8 | **Pausa-y-pregunta en 3 capas** — snapshot suspendido persistido (mastra) + tarjeta/relay con código de 5 letras por WhatsApp (nanoclaw/Channels) + draft-solo-comete-aprobado con `canUseTool→'ask'` (boop) — EL diferenciador de producto | plano de oro #5 |
| 9 | **Ingesta multimodal: guardar SIEMPRE al recibir, anotar a texto AL INGRESO** (cache idempotente); Claude ve imagen/PDF (por RUTA = $0 en suscripción), **Groq transcribe voz (ÚNICO proveedor nuevo, US$0,04/h)**; video v1 = solo ficha; fallo = nota explícita, jamás silencio; < US$0,50/mes | informes media ×3 |
| 10 | **Todo módulo nace administrable**: `manifest` + `configSchema` Zod + `fragmentoPersona` + `herramientas`; on/off y ajustes desde el panel PWA (soft-disable, git = historial y rollback); mejoras reutilizables se promueven al maestro | requisito 1 de Alejandro + E2 |

---

## 2. Estructura de carpetas COMPLETA del módulo `dixdybot/`

Repo **PLANO** (un solo `package.json`, patrón NanoClaw 30k★ — el análogo más cercano;
los monorepos de Mastra/builderbot existen porque publican paquetes npm y dixdybot no
publica nada: el clon-por-cliente copia el repo entero). Carpetas como fronteras. Tests
colocalizados (`x.test.ts` junto a `x.ts`). Vive en
`/Users/alejandroriveracarrasco/SaSS/DIXDY/dixdybot/`.

```
dixdybot/                          # MÓDULO GENÉRICO en el repo maestro (cero datos de cliente)
├── package.json                   # único; pnpm 11.17 pineado (packageManager), deps con pin exacto
├── tsconfig.json                  # strict, module nodenext, erasableSyntaxOnly, noEmit
├── config.example.env             # plantilla → el clon la copia a .env.local (gitignored)
├── SETUP.md                       # instanciar por cliente (patrón correo-worker/SETUP.md)
├── MANUAL.md                      # operación diaria + runbook Coexistence (patrón whatsapp-bot/MANUAL.md)
├── launchd/                       # plantillas .plist: bot (apunta a src/index.ts), respaldo db+auth
│
├── src/
│   ├── index.ts                   # arranque: valida config (Zod) → abre db → monta módulos activos
│   │                              #   → factory de canales → panel Hono → timbre. UN solo proceso.
│   │
│   ├── core/                      # el corazón; nada aquí conoce un canal ni un rubro
│   │   ├── db.ts                  # ÚNICO archivo que toca better-sqlite3 (WAL, prepared statements,
│   │   │                          #   transacciones). Migrar a node:sqlite = editar SOLO esto.
│   │   ├── esquema.sql            # las 5 tablas (§4.4) + índices; migraciones con schema_version
│   │   ├── escritor.ts            # un-solo-escritor: TODA escritura a las 5 tablas pasa por aquí;
│   │   │                          #   dedup INSERT OR IGNORE por (conversacion, source_id_externo)
│   │   ├── llm.ts                 # puerta única al cerebro (§4.2): cola, failover, sesiones, ledger
│   │   ├── cola.ts                # promise-chain por conversación (FIFO por chat, paralelo entre
│   │   │                          #   chats, limpieza del Map al asentarse — fix del leak del bridge)
│   │   ├── bus.ts                 # eventos internos tipados (EventoCanal → gating → cerebro → envío)
│   │   ├── config.ts              # carga data/ajustes/*.json del clon, valida contra schema del
│   │   │                          #   módulo, cache TTL 30s + alias + SNAPSHOT por turno (boop/nanoclaw)
│   │   ├── ledger.ts              # append-only JSONL: uso-llm.jsonl, eventos.jsonl, envios.jsonl
│   │   └── schemas/               # ZOD FUENTE ÚNICA — un archivo por contrato; z.infer = los tipos
│   │       ├── mensaje.ts         #   MensajeEntrante, MediaEntrante, MediaSaliente, ResultadoEnvio
│   │       ├── llm.ts             #   ConsultaLLM, RespuestaLLM, UsoLLM, EventoLLM, errores tipados
│   │       ├── camino.ts          #   Camino (YAML), Regla, Relacion, EvaluacionTurno (JSON del cerebro)
│   │       ├── manifest.ts        #   ManifestModulo + contrato Modulo (§6)
│   │       └── pausa.ts           #   SnapshotSuspendido, PreguntaDueno, RespuestaDueno
│   │
│   ├── organos/                   # TRASPLANTES del bot vivo (JS tal cual; se tipan cuando toque)
│   │   ├── gating.js              # debounce + timbre + anti-flood (probado en producción)
│   │   ├── extraer.js             # extractor de datos de cotización + fechaISO (el único juez de fechas)
│   │   └── integracion.js         # cotizar/PDF/Supabase/repartidor (se modulariza en E2, no antes)
│   │
│   ├── canales/                   # E4: la factory; el core JAMÁS ve un vendor
│   │   ├── canal.ts               # LA interfaz Canal (§4.1) + eventos canónicos
│   │   ├── factory.ts             # arranca canales según data/ajustes/canales.json; sin credenciales
│   │   │                          #   → null = canal apagado sin romper el boot (nanoclaw)
│   │   ├── wa-baileys/            # adaptador Baileys 7.0.0-rc.9 pineado, endurecido:
│   │   │   ├── adaptador.ts       #   backoff 1s→30s cap + circuit breaker (N reconexiones/M min →
│   │   │   │                      #   detenerse + avisar), LID translateJid, loggedOut vs shutdown,
│   │   │   │                      #   getMessage desde sentMessageCache; ventana() = {abierta:true}
│   │   │   ├── media.ts           #   descarga E2E: downloadMediaMessage + reuploadRequest (nanoclaw)
│   │   │   └── legado/            #   enviar.js + outbox.js trasplantados (candado anti-jid-de-prueba
│   │   │                          #   DENTRO del emisor — doble candado vocero)
│   │   ├── wa-cloud/              # E5: adaptador Cloud API contra Worker meta-buzon (polling timbre v2)
│   │   │   ├── adaptador.ts       #   ventana() real calculada (chatwoot ~70 líneas), enviarPlantilla,
│   │   │   │                      #   árbol: template_params → plantilla; can_reply → sesión; → failed
│   │   │   ├── media.ts           #   GET /{media-id} → URL 5 min → GET Bearer; 401 = canal a reautorizar
│   │   │   └── webhook.ts         #   verificación GET + HMAC timingSafeEqual sobre rawBody +
│   │   │                          #   extractStatus (robado de builderbot provider-meta, MIT)
│   │   ├── ig/                    # E5: Instagram DM (payload.url directa → descargar YA; topes propios)
│   │   └── sim/                   # canal simulado: gimnasio, tests, replay y las 48 h de sombra
│   │
│   ├── ingesta/                   # §5 — multimodal; corre ANTES del cerebro, administrable por panel
│   │   ├── index.ts               # orquestador: placeholder al hilo YA → guardar → procesar async
│   │   ├── guardar.ts             # ÚNICO que toca binarios entrantes; nombre SIEMPRE generado
│   │   ├── anotar.ts              # cache <archivo>.anotacion.json + reemplaza placeholder en el hilo
│   │   └── procesadores/
│   │       ├── imagen.ts          # visión vía llm.ts (ruta en modo cli; base64 en api)
│   │       ├── audio.ts           # OGG/Opus directo a Groq whisper-large-v3-turbo (fetch nativo)
│   │       ├── documento.ts       # PDF → bloque document de Claude (nativo, sin beta)
│   │       └── video.ts           # v1: solo ficha {duración, tamaño}; v2 opcional: frames+audio
│   │
│   ├── motor/                     # E3: caminos — el corazón del producto
│   │   ├── proyector.ts           # camino→reglas transitorias id `journey_node:<n>:<a>` + follow_ups
│   │   │                          #   (LA joya de parlant: un solo motor para reglas Y caminos)
│   │   ├── evaluador.ts           # UNA llamada por turno vía llm.ts: reglas del dominio + camino vivo
│   │   │                          #   → EvaluacionTurno (JSON tipado, rationale ANTES del booleano)
│   │   ├── resolver.ts            # determinista post-LLM: Kahn (~20 líneas) → prioridad → entailment;
│   │   │                          #   cada decisión = Resolution con porqué humano (para el panel)
│   │   ├── pausa.ts               # 3 capas: snapshot suspendido persistido + relay código 5 letras
│   │   │                          #   ("si abcde" por WhatsApp del dueño, primera respuesta gana,
│   │   │                          #   campos del cliente NO confiables) + drafts que solo cometen aprobados
│   │   └── lint.ts                # validación al guardar (Decagon): frontmatter completo, CERO cifras
│   │                              #   en el cuerpo, máx una transición sin condición, sin solape retirado
│   │
│   ├── agentes/                   # IA madre → especialistas (§6.2)
│   │   ├── madre.ts               # dispatcher: PROHIBIDO responder hechos del mundo; ack <2s
│   │   │                          #   (typing + frase corta); deriva EN SILENCIO por dominio
│   │   ├── especialista.ts        # compone persona base + fragmentos de módulos del dominio +
│   │   │                          #   SOLO caminos del dominio (proyectados); tools SOLO del paso
│   │   └── componer.ts            # claude-md-compose de nanoclaw: prompt por fragmentos en cada turno
│   │
│   ├── modulos/                   # capacidades enchufables; cada una cumple el contrato Modulo (§6.1)
│   │   ├── indice.ts              # barrel: UNA línea de import por módulo (instalador = documento)
│   │   ├── precios/               # tarifario-en-datos + validador precioCoherente POST-generación
│   │   │                          #   (la doble muralla; genérico multi-rubro: la tabla es del cliente)
│   │   ├── seguimiento/           # recordatorios 💤 + cotización abandonada (plantilla utility en E5)
│   │   └── (cotizador/, agenda/…) # los del rubro nacen en el CLON y se promueven si son genéricos
│   │
│   ├── panel/                     # PWA del dueño (iPhone primero) — decidido: PWA, sin app nativa
│   │   ├── servidor.ts            # Hono: /api/* + estáticos + webhooks; @hono/zod-validator en el borde
│   │   ├── api/                   # conversaciones, conocimiento (tarjetas+diff+Aprobar), ajustes
│   │   │                          #   (render desde JSON Schema), embudo, gimnasio, pausas pendientes
│   │   └── pwa/                   # vanilla HTML/CSS/JS + manifest.json + sw.js; DaisyUI opcional;
│   │                              #   push por avisos-worker (VAPID ya operativo); SIN canvas de nodos
│   │
│   ├── gimnasio/                  # calidad; el juez es un SCRIPT, no un test
│   │   ├── personas.ts            # 6 guiones fijos SIN LLM (vocero) = regresión determinista en vitest
│   │   ├── juez.ts                # script aparte: veredicto tipado {verde|amarillo|rojo, hallazgos con
│   │   │                          #   evidencia citada, sugerencia aplicable}; gate de despliegue ≥4,0
│   │   └── replay.ts              # forkSession (sin contaminar) + backtesting patrón Fin al editar
│   │
│   └── cli/                       # herramientas de operación (una persona + IA)
│       ├── doctor.ts              # healthcheck: db, auth, canal, cerebro, ledgers, espacio en disco
│       ├── migrar.ts              # migraciones esquema + one-shot JSONL viejo → 5 tablas
│       ├── vincular.ts            # pairing por código (sin QR), como hoy
│       └── juez.ts                # correr juez/backtesting a mano
│
└── plantillas/                    # persona base genérica + respuestas enlatadas + fragmentos ejemplo
```

**En el CLON del cliente** (fuera del maestro; para destaperapido:
`~/SaSS/destaperapido/dixdybot/` junto al bot vivo):

```
dixdybot/            # copia del template
├── .env.local       # credenciales (gitignored): Baileys/Meta, GROQ_API_KEY, ANTHROPIC_API_KEY (failover)
├── auth/            # sesión del canal (gitignored, respaldada por launchd)
└── data/            # TODO el estado del cliente
    ├── bot.db       # SQLite (5 tablas) — respaldo diario con VACUUM INTO
    ├── media/<convId>/<msgId>.<ext> (+ .anotacion.json)   # binarios + anotaciones cacheadas
    ├── caminos/*.yml            # el conocimiento del negocio, versionado en el git DEL CLON
    ├── ajustes/<modulo>.json    # config por módulo (lo que edita el panel)
    ├── persona/base.md + fragmentos/   # la voz del negocio
    └── ledgers/uso-llm.jsonl · eventos.jsonl · envios.jsonl   # bitácoras inmutables
```

---

## 3. El stack final (versiones verificadas 23-jul-2026)

| Pieza | Elección | Por qué (una línea) |
|---|---|---|
| Runtime | **Node.js 24 LTS** (subir el Mac desde 22.18; → 26 LTS en oct-2026) | `child_process` sagrado para `claude -p`; los 8 repos estudiados corren Node; Bun 1.3.14 aún parchea compat Node cada release |
| Lenguaje | **TypeScript 6.0 estricto ejecutado NATIVO** (type stripping ESTABLE desde Node 24.12) — `noEmit`, sin build, sin dist/, launchd apunta al `.ts` | `tsc --noEmit` = el verificador más barato para una IA (5 s); `.js` del vivo convive en el mismo proceso |
| Persistencia | **better-sqlite3 13.0.1** (21-jul-2026), WAL, un escritor, TODO el acceso en `db.ts` + **JSONL para ledgers** | UNIQUE/dedup/estados de los planos salen gratis; síncrono = sin carreras; NanoClaw lo valida; `node:sqlite` (ya RC) = sucesor a costo de 1 archivo |
| HTTP | **hono 4.12.31 + @hono/node-server 2.0.11 + @hono/zod-validator 0.9.0** | cero deps, Web Standards, mismo handler Mac ↔ Cloudflare Worker (meta-buzon); Mastra usa hono ^4.12.8 para lo mismo |
| Schemas | **zod 4.4.3** fuente única (config + StructuredOutput + webhooks; `z.toJSONSchema()` para Ajustes) | un schema, tres contratos; tools del Agent SDK ya hablan Zod |
| Canal WA | **baileys 7.0.0-rc.9 pineado** (+ mitigaciones nanoclaw) hoy; Cloud API en E5 | rampa de clientes nuevos; la salida del número vivo tiene fecha (30-sep) |
| Estructura | **Repo plano**, un package.json, **pnpm 11.17.0** con `packageManager` + pins exactos | patrón NanoClaw; workspaces se agregan en una tarde SI E6 lo exige |
| Testing | **vitest 4.1.10 pineado** (5.0 beta: no) para lo determinista; el juez LLM fuera, como script con gate ≥4,0 | unanimidad de la clase (NanoClaw/Mastra/boop) |
| Transcripción | **Groq whisper-large-v3-turbo** por `fetch` nativo (sin SDK) — US$0,04/hora | único proveedor nuevo de todo el sistema; acepta el OGG/Opus de WhatsApp sin ffmpeg |
| **Deps runtime totales** | **6**: baileys, better-sqlite3, hono, @hono/node-server, @hono/zod-validator, zod | la sencillez como número auditable |

Node 24 nativo ya trae: `fetch`, `--env-file` (adiós dotenv), `--watch` (adiós nodemon),
type stripping (adiós tsx/build) y `node:sqlite` en camino.

**Convenciones de la casa** (obligatorias, por el type stripping y la doctrina):
- **PROHIBIDO**: `enum` (usar uniones de literales), decoradores, parameter properties,
  namespaces con runtime. Imports con extensión `.ts` explícita; `import type` para tipos.
- `tsconfig`: `"strict": true, "module": "nodenext", "erasableSyntaxOnly": true, "noEmit": true`.
- Los contratos de dominio hablan **español** (`consultar`, `MensajeEntrante`, `ventana`) —
  es la lengua del método completo (planos, plan, panel) y de quien lo opera; la
  infraestructura estándar queda en inglés. Archivos kebab-case.
- Cero interfaces TS paralelas a los schemas: `z.infer<>` es el único origen de tipos de datos.

---

## 4. Los contratos núcleo (TypeScript)

### 4.1 La interfaz Canal (`src/canales/canal.ts`)

Esqueleto builderbot (probado en 15+ canales) + refinamientos nanoclaw (factory-null,
isMention del adaptador) + lo que ningún repo tiene y dixdybot exige: `ventana()`,
`enviarPlantilla()`, `ResultadoEnvio` honesto, `estado_envio`.

```ts
// src/canales/canal.ts
import type { MensajeEntrante, MediaSaliente, ResultadoEnvio } from '../core/schemas/mensaje.ts';

/** Eventos canónicos que todo adaptador emite al bus. El core JAMÁS ve el vendor. */
export type EventoCanal =
  | { tipo: 'mensaje'; msg: MensajeEntrante }
  | { tipo: 'listo' }                                   // socket abierto (Baileys) o webhook verificado (Meta)
  | { tipo: 'accion_requerida'; datos: { codigoPairing?: string } }  // solo canales con vinculación
  | { tipo: 'auth_fallida'; motivo: string }            // 401 Meta / loggedOut Baileys → avisar, no loopear
  | { tipo: 'estado_envio'; msgIdNativo: string;        // los ✓✓ REALES del panel
      estado: 'enviado' | 'entregado' | 'leido' | 'fallido'; motivo?: string }
  | { tipo: 'aviso'; texto: string };

export interface Canal {
  /** 'wa-baileys' | 'wa-cloud' | 'ig' | 'sim' — prefijo del convId compuesto `canal:idNativo` */
  readonly id: string;

  iniciar(alBus: (ev: EventoCanal) => void): Promise<void>;
  detener(): Promise<void>;

  enviarTexto(convId: string, texto: string): Promise<ResultadoEnvio>;
  enviarMedia(convId: string, media: MediaSaliente): Promise<ResultadoEnvio>;

  /** De PRIMERA clase: fuera de ventana la Cloud API EXIGE plantilla. No-op honesto en Baileys. */
  enviarPlantilla(convId: string, nombre: string, idioma: string,
                  vars: Record<string, string>): Promise<ResultadoEnvio>;

  /** Calculada al estilo chatwoot (del último mensaje ENTRANTE), JAMÁS persistida.
   *  Baileys: siempre { abierta: true, expiraTs: null }. El core la consulta ANTES de enviar;
   *  si igual falla → motivo 'fuera_de_ventana' → degradar a plantilla + evento. */
  ventana(convId: string): { abierta: boolean; expiraTs: number | null };

  /** Asimetría real: Baileys teclea por jid; Meta exige el wamid del mensaje ENTRANTE. */
  escribiendo(convId: string, msgIdNativoEntrante?: string): Promise<void>;

  /** Semántica de plataforma resuelta POR el adaptador; el router no adivina. */
  esMencion?(msg: MensajeEntrante): boolean;
}

/** Factory: devuelve null si faltan credenciales → canal apagado SIN romper el boot. */
export type FabricaCanal = (config: unknown) => Canal | null;
```

```ts
// src/core/schemas/mensaje.ts  (extracto — Zod fuente única)
import { z } from 'zod';

export const MediaEntrante = z.object({
  // 'voz' ≠ 'audio': WA lo marca (voice/ptt); en IG los audio DM se asumen 'voz'
  tipo: z.enum(['imagen', 'voz', 'audio', 'video', 'documento', 'sticker', 'otro']),
  mime: z.string(),                       // p.ej. 'audio/ogg; codecs=opus'
  tamanoBytes: z.number().nullable(),     // Cloud lo da (file_size); IG no siempre
  nombreArchivo: z.string().nullable(),   // solo documentos; JAMÁS se usa como nombre en disco
  caption: z.string().nullable(),
  sha256: z.string().nullable(),          // dedup de binarios (Cloud y Baileys lo traen)
  caducaEn: z.number().nullable(),        // WA Cloud: ahora+7d (media ID webhook); Baileys/IG: null = bajar YA
});
export type MediaEntrante = z.infer<typeof MediaEntrante>;

/** Runtime: el adaptador envuelve la media con su resolución lazy del binario.
 *  Baileys = bajar ciphertext + descifrar E2E con mediaKey (+ reuploadRequest si el CDN expiró);
 *  Cloud   = GET /{media-id} → URL de 5 min → GET con Bearer (re-pedir si venció);
 *  IG      = GET directo al payload.url (sin auth, vigencia no documentada);
 *  correo  = parsed.attachments ya en memoria.
 *  Errores tipados: MediaCaducado (re-pedible o no) y MediaMuyGrande. */
export interface MediaConBinario extends MediaEntrante {
  obtenerBinario(): Promise<Buffer>;
}

export const MensajeEntrante = z.object({
  convId: z.string(),        // COMPUESTO `${canal}:${idNativo}` — nunca teléfono pelado
  canal: z.string(),
  idNativo: z.string(),      // jid / fono sin '+' / ig user id — normalizado POR el canal
  tipo: z.enum(['texto', 'media', 'boton', 'ubicacion', 'contacto', 'sistema']),
  texto: z.string(),         // botón/lista COLAPSAN al título (el cerebro es agnóstico de botones);
                             // media = placeholder hasta que ingesta lo reemplace por la anotación
  media: MediaEntrante.nullable(),
  msgIdNativo: z.string(),   // wamid / key.id → dedup de webhooks + correlación de acks
  ts: z.number(),
  crudo: z.unknown(),        // payload nativo; SOLO el adaptador lo mira
});
export type MensajeEntrante = z.infer<typeof MensajeEntrante>;

export const ResultadoEnvio = z.object({
  ok: z.boolean(),
  msgIdNativo: z.string().optional(),
  // HONESTO: jamás catch(e){ return e } (anti-patrón builderbot)
  motivo: z.enum(['fuera_de_ventana', 'auth', 'rate', 'media_muy_grande', 'red', 'otro']).optional(),
});
export type ResultadoEnvio = z.infer<typeof ResultadoEnvio>;

export const MediaSaliente = z.object({
  tipo: z.enum(['imagen', 'audio', 'video', 'documento', 'sticker']),
  mime: z.string(),
  nombreArchivo: z.string().nullable(),
  caption: z.string().nullable(),        // topes por canal: WA 1024 chars; IG texto 1000
  origen: z.union([z.instanceof(Buffer), z.string()]),  // Buffer (Baileys/local) o URL pública
});
export type MediaSaliente = z.infer<typeof MediaSaliente>;
```

Topes de envío (tabla viva en cada adaptador, del informe media-ingesta-canales): WA Cloud
5/16/16/100 MB (imagen/audio/video/doc), sticker 100/500 KB; IG 8/25/25/25 MB; correo
adjunto D1 ≤ ~1,4 MB o R2. WA saliente: upload-primero con `id` reutilizable 30 días (la
ficha/PDF frecuentes se suben UNA vez y se cachea el id por cliente).

### 4.2 El contrato llm (`src/core/schemas/llm.ts` + `src/core/llm.ts`)

El plano de oro #2, cerrado. Lo genuinamente nuestro: la cadena de failover tipada.

```ts
// src/core/schemas/llm.ts (extracto)
import { z } from 'zod';

export type ModoLLM = 'vendedor' | 'especialista' | 'fondo';
export type MotorLLM = 'sdk' | 'cli' | 'api' | 'plantilla';   // la cadena, en orden

export const UsoLLM = z.object({
  motor: z.enum(['sdk', 'cli', 'api', 'plantilla']),
  modelo: z.string(),
  inTok: z.number(), outTok: z.number(),
  cacheR: z.number(), cacheW: z.number(),
  costoUsd: z.number(),          // preferir modelUsage (agrega TODA la query) sobre usage (gotcha boop)
  duracionMs: z.number(),
});

export interface ConsultaLLM {
  conversacionId: string;
  prompt: string;
  sistema: string;                              // compuesto por fragmentos (componer.ts)
  herramientas?: HerramientaMCP[];              // tools propias como MCP en-proceso (boop):
                                                //   contratos MCP-compatibles = seguro anti-lock-in
  permitidas?: string[]; prohibidas?: string[]; // SIEMPRE ambas listas (cinturón y tirantes, boop)
  modo: ModoLLM;                                // timeouts y presupuesto por rol
  salidaEsquema?: z.ZodType;                    // StructuredOutput: JSON que no parsea = fallo tipado → failover
  preguntarDueno?: (p: PreguntaDueno) => Promise<RespuestaDueno>;  // gancho canUseTool→'ask' (E3)
  onTexto?: (t: string) => void;
  onUso?: (u: z.infer<typeof UsoLLM>) => void;
}

export interface RespuestaLLM {
  texto: string;
  json?: unknown;                               // validado contra salidaEsquema
  uso: z.infer<typeof UsoLLM>;
  eventos: Array<{ tipo: 'fallback'; de: MotorLLM; a: MotorLLM;
                   causa: 'timeout' | 'rate_limit' | 'placeholder' | 'sesion_invalida' | 'error' }>;
}

export declare function consultar(c: ConsultaLLM): Promise<RespuestaLLM>;
```

Comportamiento interno de `llm.ts` (todo del plano #2, nada inventado):
- **Cola promise-chain por `conversacionId`** (bridge) — FIFO por chat, paralelismo entre
  chats, limpieza del Map. La cola ES la semilla del un-solo-escritor.
- **Snapshot de config al inicio del turno** (boop): un cambio a mitad de turno no parte
  el turno en dos cerebros.
- **Cadena `sdk→cli→api→plantilla`** con clasificación de error tipado: `rate_limit`
  espera y reintenta; `auth` NO degrada (avisa); placeholder/`(no output)` degrada;
  regex de sesión inválida → retry con sesión fresca (nanoclaw). Cada salto = evento en el ledger.
- **Sesión por conversación persistida APENAS llega el evento `init`** (no al final del
  turno: un crash no huerfanea la conversación), keyed por motor, en
  `conversaciones.sesion_llm` (SQLite: es estado vivo). Rotación de transcript >12 MB o
  >14 días. Peldaños `cli`/`api` sin `resume`: historial por presupuesto de tokens (mastra), no por N mensajes.
- **Ledger por turno** a `data/ledgers/uso-llm.jsonl` (con `modelUsage`, `total_cost_usd`)
  — operativo antes del **19-ago** (fecha dura del plan).
- Topes duros por turno: `maxTurns`, `maxBudgetUsd` (SDK).

### 4.3 El esquema de camino con dominio/agente (`src/core/schemas/camino.ts`)

YAML en `data/caminos/*.yml` del clon, validado por Zod. El `dominio` entra desde el día 1
(requisito de Alejandro). El motor NO ejecuta caminos: los **proyecta a reglas** (Parlant).

```ts
// src/core/schemas/camino.ts (extracto)
import { z } from 'zod';

export const Paso = z.object({
  id: z.string(),
  tipo: z.enum(['mensaje', 'tool', 'pausa-dueno', 'decision']).default('mensaje'),
  accion: z.string(),                            // NL o plantilla_id (cifras SIEMPRE desde tools)
  herramientas: z.array(z.string()).default([]), // habilitadas SOLO en este paso (parlant)
  espera_del_cliente: z.boolean().default(true),
  continua: z.boolean().default(false),
  respuestas: z.array(z.object({                 // plantillas con campos origen tool:
    plantilla: z.string(),                       //   "en desviación cuantitativa la plantilla tiene razón"
    campos_generativos: z.array(z.string()).default([]),
  })).default([]),
  timeout_horas: z.number().optional(),          // solo pausa-dueno (escalada; enlatada inmediata)
  respuesta_espera: z.string().optional(),       // lo que el cliente ve mientras el dueño decide
});

export const Camino = z.object({
  id: z.string(),
  version: z.number().int().default(1),
  dominio: z.string(),                           // agente especialista dueño: 'ventas' | 'agenda' | …
  titulo: z.string(),
  estado: z.enum(['borrador', 'activo', 'retirado']).default('borrador'),  // retirar = soft-disable, JAMÁS borrar
  origen: z.enum(['manual', 'aprendido']).default('manual'),               // badge "nuevo" en el panel
  disparadores: z.array(z.string()).min(1),      // condiciones NL (reglas trigger)
  pasos: z.array(Paso).min(1),
  transiciones: z.array(z.object({
    de: z.string(), a: z.string(),
    condicion: z.string().nullable(),            // máx UNA sin condición por paso (lint.ts)
  })),
  relaciones: z.array(z.object({                 // vocabulario parlant, subconjunto útil
    tipo: z.enum(['prioridad_sobre', 'depende_de', 'implica', 'desambiguar', 'reevaluar']),
    con: z.string(),
  })).default([]),
  schema_version: z.number().int().default(1),   // upgrades encadenados baratos
});
export type Camino = z.infer<typeof Camino>;

/** Lo que el cerebro devuelve por turno — UNA llamada, rationale ANTES del booleano. */
export const EvaluacionTurno = z.object({
  reglas_aplican: z.array(z.object({ id: z.string(), razon: z.string(), aplica: z.boolean() })),
  camino: z.object({
    sigue: z.boolean(),
    paso_completado: z.boolean(),
    transicion_elegida: z.string().nullable(),
  }).nullable(),
  dominio_detectado: z.string().nullable(),      // la madre enruta con esto si no hay camino vivo
  respuesta: z.string().nullable(),
  plantilla_id: z.string().nullable(),
});
```

Estado por conversación (persistido en `conversaciones`): `camino_activo`, `camino_paso`,
`reglas_aplicadas` — sobrevive reinicios. El resolver corre DESPUÉS, determinista y gratis,
y guarda cada decisión como `Resolution {tipo, descripcion_humana, contrapartes}` para que
el panel pueda mostrar "esta regla no disparó porque X tuvo prioridad".

### 4.4 El esquema de datos: 5 tablas (`src/core/esquema.sql`)

Campos de Chatwoot + disciplina nanoclaw. **Un solo proceso escribe `bot.db`** (el núcleo,
vía `escritor.ts`); panel y Kanban leen del mismo proceso; scripts externos leen respaldo
o pasan por la API.

```sql
-- contactos: la PERSONA, agnóstica de canal (resource de mastra)
CREATE TABLE contactos (
  id            INTEGER PRIMARY KEY,
  nombre        TEXT,
  telefono      TEXT UNIQUE,          -- cascada de unificación: identifier → email → teléfono
  email         TEXT UNIQUE,
  identificador TEXT UNIQUE,
  creado_ts     INTEGER NOT NULL,
  schema_version INTEGER NOT NULL DEFAULT 1
);

-- identidades: LA pieza que no teníamos (ContactInbox de chatwoot)
CREATE TABLE identidades (
  id          INTEGER PRIMARY KEY,
  contacto_id INTEGER NOT NULL REFERENCES contactos(id),
  canal_id    TEXT    NOT NULL,
  source_id   TEXT    NOT NULL,       -- jid / fono sin '+' / ig id — normaliza EL CANAL
  UNIQUE (canal_id, source_id)        -- la llave de enrutamiento de TODO lo entrante;
);                                    -- la migración Coexistence conserva historial al cambiar source_id

-- canales: config y estado por canal (provider_config de chatwoot)
CREATE TABLE canales (
  id          TEXT PRIMARY KEY,       -- 'wa-baileys' | 'wa-cloud' | 'ig' | 'sim'
  tipo        TEXT NOT NULL,
  config      TEXT NOT NULL DEFAULT '{}',   -- JSON: credenciales/provider (validado por Zod del adaptador)
  plantillas  TEXT NOT NULL DEFAULT '{}',   -- catálogo cacheado (sync periódico en wa-cloud)
  bot_activo  INTEGER NOT NULL DEFAULT 1,
  horario     TEXT
);

-- conversaciones: thread por canal; handoff bot↔humano COMO DATOS
CREATE TABLE conversaciones (
  id            INTEGER PRIMARY KEY,
  conv_id       TEXT UNIQUE NOT NULL,       -- `${canal}:${source_id}`
  contacto_id   INTEGER REFERENCES contactos(id),
  canal_id      TEXT NOT NULL,
  estado        TEXT NOT NULL DEFAULT 'pendiente_bot',  -- pendiente_bot|abierta|resuelta|dormida
  asignado      TEXT NOT NULL DEFAULT 'bot',            -- bot|humano (pending=bot, bot_handoff)
  snoozed_until INTEGER,                    -- recordatorios 💤 gratis
  waiting_since INTEGER, first_reply_ts INTEGER,        -- métricas de espera del Kanban gratis
  camino_activo TEXT, camino_paso TEXT, reglas_aplicadas TEXT,  -- estado E3 persistido
  sesion_llm    TEXT                        -- JSON {sdk: id, cli: id} — escrito en el evento init
);

-- mensajes: resuelve EN el dato el dedup, los ✓✓ y el "¿quién cotizó?"
CREATE TABLE mensajes (
  id                INTEGER PRIMARY KEY,
  conversacion_id   INTEGER NOT NULL REFERENCES conversaciones(id),
  tipo              TEXT NOT NULL,          -- entrante|saliente|actividad|plantilla
  remitente         TEXT NOT NULL,          -- contacto|bot|humano
  texto             TEXT NOT NULL,          -- media: la ANOTACIÓN reemplaza el placeholder aquí
  media_ruta        TEXT, media_tipo TEXT,  -- ruta en disco; el binario JAMÁS en la tabla
  source_id_externo TEXT,                   -- wamid/key.id → dedup webhooks + correlación acks
  estado            TEXT,                   -- enviado|entregado|leido|fallido (evento estado_envio)
  privado           INTEGER NOT NULL DEFAULT 0,
  ts                INTEGER NOT NULL,
  UNIQUE (conversacion_id, source_id_externo)   -- dedup de reentregas: INSERT OR IGNORE
);
```

**Regla de reparto**: estado vivo y claves únicas → SQLite; bitácora inmutable → JSONL
(`uso-llm.jsonl`, `eventos.jsonl`, `envios.jsonl` como ledger `delivered` con
`{message_out_id, platform_message_id, status, delivered_at}`). Backup diario:
`VACUUM INTO` + el respaldo de `auth/` que launchd ya hace.

### 4.5 El manifest de módulo (`src/core/schemas/manifest.ts`)

```ts
// src/core/schemas/manifest.ts
import { z } from 'zod';
import type { Hono } from 'hono';
import type { MensajeEntrante } from './mensaje.ts';

export const ManifestModulo = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/),   // kebab-case: 'ingesta', 'precios', 'seguimiento'
  nombre: z.string(),                     // lo que el dueño ve en el panel
  descripcion: z.string(),                // una frase en simple
  version: z.string(),
  dominio: z.string().nullable(),         // si aporta conocimiento/tools a UN especialista
  requiere: z.array(z.string()).default([]),
});
export type ManifestModulo = z.infer<typeof ManifestModulo>;

/** El contrato que TODO módulo cumple. Registrarse = una línea en modulos/indice.ts. */
export interface Modulo<C = unknown> {
  manifest: ManifestModulo;

  /** LA pieza genérico-modular: el MISMO schema (1) valida data/ajustes/<id>.json al
   *  arrancar, (2) se exporta z.toJSONSchema() y el panel DIBUJA la vista Ajustes solo,
   *  (3) tipa el snapshot que el módulo recibe por turno. Un módulo nuevo = schema nuevo
   *  = pantalla nueva, cero código de panel. */
  configSchema: z.ZodType<C>;
  configDefault: C;

  /** Fragmento de persona/prompt que aporta al componer el sistema (claude-md-compose). */
  fragmentoPersona?(config: C): string;

  /** Tools que aporta al cerebro — MCP-compatibles en-proceso (patrón boop). */
  herramientas?(config: C): HerramientaMCP[];

  /** Hook pre-cerebro sobre el mensaje entrante (ej: ingesta anota media). */
  alMensaje?(msg: MensajeEntrante, ctx: ContextoModulo): Promise<void>;

  /** Sub-rutas propias que el panel monta bajo /api/mod/<id>/. */
  rutasPanel?(): Hono;

  iniciar?(config: C, ctx: ContextoModulo): Promise<void>;
  detener?(): Promise<void>;
}
```

Estado on/off + config del cliente viven en `data/ajustes/<id>.json` del clon
(**el panel edita datos, nunca código**; git del clon = historial y rollback). Apagar =
`{"activo": false}` (soft-disable, nunca borrar). El snapshot de config se materializa por
turno (nanoclaw) con cache TTL 30 s (boop).

---

## 5. El módulo `ingesta/` multimodal

Capacidad **genuinamente nuestra** (ninguno de los 8 repos OSS procesa media con IA; el
bot vivo hoy reduce todo a "📷 Foto" y ya costó plata: el compromiso a ciegas del 20-jul
con la válvula, la confirmación de 30 baños en nota de voz del 21-jul que nadie pudo leer).

**Principio**: guardar es barato y corre SIEMPRE (sensor); describir/transcribir es el
juicio caro y corre según config (escalones DIXDY). Normalizar **al ingreso, no bajo
demanda**: todo se vuelve texto anotado en el hilo, cacheado e idempotente.

### Flujo

```
canal (adaptador) ──MensajeEntrante{tipo:'media'}──► hilo: placeholder "[FOTO: procesando…]" YA
      │
      └─► ingesta.index: guardar.ts INMEDIATO (disco) ──► procesadores/<tipo> (async, vía llm.ts / Groq)
                                                                   │
        mensajes.texto ◄── anotar.ts: reemplaza placeholder ◄── anotación (cacheada en .anotacion.json)
                                                                   │
        timbre (gating) re-dispara al cerebro → responde VIENDO la evidencia
        → panel muestra thumbnail por media_ruta → calidad/juez/replay evalúan con lo mismo
```

Reglas duras (lecciones de nanoclaw/chatwoot, verificadas en código):
- **Guardar SIEMPRE al recibir** — el modelo perezoso de builderbot pierde el binario si el
  proceso reinicia; con Baileys el CDN expira: `downloadMediaMessage` **con
  `reuploadRequest`** (recuperable en vez de perdido). En Cloud API, bajar dentro de los
  7 días del media ID (en la práctica: al webhook); URL de 5 min re-emitible. En IG,
  `payload.url` sin vigencia documentada → bajar al tiro.
- **Nombre en disco SIEMPRE generado** (`<msgId>.<ext>` en `data/media/<convId>/`):
  `fileName` del cliente viaja E2E y es attacker-controlled (path traversal). Escritura con
  flag `wx`, sin symlinks.
- **Fallo = nota explícita al hilo, jamás silencio**: `[FOTO recibida pero no se pudo
  descargar — pídele que la reenvíe]` → el cerebro pide reenvío con naturalidad.
- **El cerebro solo ve texto anotado + la ruta** (patrón nanoclaw `[image: … — saved to
  <ruta>]`); nunca base64 en el hilo, ni en la tabla, ni en ledgers. `sha256` para no bajar
  dos veces.
- **Anotación cacheada** en `<archivo>.anotacion.json` (patrón `transcribed_text` de
  Chatwoot enterprise): se paga UNA vez; reanalizar/replay/juez la reusan gratis.

### Por tipo de media: qué corre dónde y qué cuesta

| Tipo | Pipeline | Local vs API | Costo unitario |
|---|---|---|---|
| 🖼️ Foto | guardar → re-escalar ≤1568 px → visión vía `llm.ts` → `[FOTO: dos estanques ~1.000L con válvula de bola en la salida]` | modo `cli`: Claude lee la **RUTA** (tool Read) = **$0 suscripción**; modo `api`: bloque image base64 | US$0,005-0,012 (Sonnet 5) |
| 🎤 Nota de voz | OGG/Opus **directo a Groq** whisper-large-v3-turbo (`language: 'es'`, fetch nativo, sin ffmpeg) → `[AUDIO transcrito: "sí, confirmo los 30 estándar y el de discapacitados"]` | API Groq (216× tiempo real; 1-2 s, invisible en la mediana de 22,6 s del bot) | US$0,04/**hora** (mín. 10 s) |
| 📄 PDF/boleta | bloque `document` nativo de Claude (sin beta, 32 MB/600 págs) → resumen anotado | modo `cli`: ruta = $0; api: base64 | US$0,01-0,03/doc |
| 🎬 Video 10-30 s | **v1: SOLO ficha** `[VIDEO recibido: 0:42, guardado — avisa al dueño si es clave]`; v2 opcional: ffmpeg 6-8 frames → visión + pista de audio → Groq | v1: local gratis; v2: API | v2 ≈ US$0,03/clip |
| 🙂 Sticker / 👤 contacto / 📍 ubicación | NO pasan por ingesta: colapsan a texto en el adaptador (ubicación → link Maps, como hoy) | local | $0 |

- **Fallback de audio SIN segundo proveedor** (sencillez): si Groq falla, el bot responde
  "no pude escuchar tu audio, ¿me lo escribes? 🙏" (pausa-y-pregunta). whisper.cpp local en
  el Mac queda documentado como opción futura (Apple Silicon first-class, $0) solo por
  privacidad Ley 21.719 o si Groq molesta seguido. **Gemini descartado** (tercer proveedor
  por un caso marginal).
- **Costo total al volumen medido** (~120 conv/mes, ~20% con media; 16 medias entrantes
  reales en 17 días): **< US$0,50/mes** (Groq ≈ $0,01; visión/PDF ≈ $0,25-0,35 — y $0
  mientras el cerebro corra por suscripción). Con tráfico ×10 sigue < US$5/mes. La decisión
  es por sencillez, no por precio.
- **Administrable** (contrato Modulo): `configSchema` con switches por tipo (imagen+audio
  ON, video OFF en v1), tope MB, y **prompt de visión por rubro** ("en destapes describe
  válvulas/estanques/diámetros") — el panel lo dibuja solo desde el schema.
- **Contratar Groq = plata** → OK de Alejandro vía Guardián antes de activar `audio.ts`.

---

## 6. Módulos administrables y la IA madre

### 6.1 Del manifest al panel (cómo nace administrable CUALQUIER cosa)

1. El módulo declara `manifest` + `configSchema` (Zod) + `configDefault` y se registra con
   UNA línea en `modulos/indice.ts` (el instalador es un documento ejecutable — patrón
   skills de nanoclaw; desinstalar = quitar la línea, los datos quedan).
2. Al arrancar (y por turno, snapshot): `config.ts` lee `data/ajustes/<id>.json`, lo valida
   contra el schema; inválido o ausente → `configDefault` + aviso.
3. El panel pide `GET /api/modulos` → recibe `[{manifest, jsonSchema: z.toJSONSchema(configSchema),
   config, activo}]` → **la vista Ajustes se RENDERIZA desde el JSON Schema** (boolean →
   switch, enum → selector, number con min/max → slider, string largo → textarea). Cero
   pantallas hechas a mano por módulo; `description` de cada campo = el texto de ayuda en simple.
4. Guardar = `PUT /api/modulos/<id>/config` → valida con el MISMO schema → escribe el JSON
   → commit en el git del clon (historial + rollback) → snapshot nuevo en el próximo turno.
5. El módulo aporta al sistema por sus hooks: `fragmentoPersona` (se compone al prompt),
   `herramientas` (tools MCP-compatibles al cerebro), `alMensaje` (pre-cerebro),
   `rutasPanel` (UI propia si la necesita).

Así se cumple el requisito #1 de Alejandro al pie de la letra: **toda capacidad nueva nace
como módulo con schema, y por lo tanto nace con pantalla de Ajustes, sin trabajo extra.**

### 6.2 IA madre → agentes especialistas (routing por dominio)

Barato primero, LLM después — y en silencio (requisito #3):

1. **Determinista gratis**: si la conversación tiene `camino_activo`, manda el `dominio` de
   ese camino → mismo especialista. Sin clasificar nada.
2. **En la misma llamada del turno**: si no hay camino vivo, el JSON del evaluador trae
   `dominio_detectado` — la clasificación viaja DENTRO de la única llamada, no como llamada extra.
3. **`madre.ts` (dispatcher, patrón boop)**: PROHIBIDO responder hechos del mundo; ack
   obligatorio < 2 s (typing + frase corta del rubro) antes de trabajo lento; deriva con
   tarea crisp (no el mensaje crudo) al especialista.
4. **`especialista.ts`**: compone su sistema con `componer.ts` = persona base + fragmentos
   de los módulos de SU dominio + SOLO los caminos de su dominio proyectados a reglas +
   tools SOLO del paso activo. Un especialista nuevo = un `dominio` nuevo en los datos
   (caminos + fragmentos), **no una clase nueva**.
5. **Pausa-y-pregunta** (transversal, 3 capas): snapshot suspendido persistido con la
   pregunta como payload validado por schema (mastra `WorkflowRunState`); tarjeta al dueño
   por push + código de 5 letras respondible desde el panel O por WhatsApp ("si abcde"),
   primera respuesta gana, campos del cliente NO confiables (nanoclaw/Channels); acciones
   externas como draft que SOLO comete aprobado + `canUseTool → 'ask'` en modo sdk (boop).
   El cliente recibe la respuesta enlatada inmediata; escalada a los 30 min; la
   conversación se REANUDA con lo aprendido sin repetir pasos.

---

## 7. Orden de construcción semana a semana

Aterriza E0-E7 — no lo reemplaza. Regla de contingencia del plan intacta: **la fecha del
canal manda** (si E3 se atrasa al 30-ago, E4+E5 pasan por encima). Fechas duras: 19-ago
(métricas LLM midiendo), 31-ago (Sonnet 5 probado con juez), 30-sep (decisión
Coexistence), 1-oct (Meta cobra), 1-dic (Ley 21.719).

| Semana | Etapa | Qué se construye | destaperapido lo usa |
|---|---|---|---|
| **S0 · 24-27 jul** | **E0 + fundación** | (a) E0 sobre el bot VIVO: cinturón completo del plan (commit fixes, circuit breaker, backup, pins, healthcheck 401) **+ `guardar.js` de media en el vivo (~40 líneas con reuploadRequest)**. (b) Pre-etapa Meta arranca (expediente + Worker `meta-buzon`). (c) En el maestro NACE `dixdybot/`: esqueleto compilable — package.json, tsconfig, `db.ts` + `esquema.sql`, `schemas/` núcleo, canal `sim`, `doctor.ts`, vitest verde desde el primer commit | **Desde el día 1 no se pierde ni un binario** (hoy cada media es irrecuperable); bot vivo blindado |
| **S1 · 28 jul-3 ago** | **E1 (prioridad #1)** | `llm.ts` completo: cola, snapshot, cadena `sdk→cli→api→plantilla`, clasificación tipada, sesión en `init`, rotación, ledger `uso-llm.jsonl`; tools internas como MCP en-proceso; evaluación Agent SDK como backend del modo cli. Clon del núcleo a `~/SaSS/destaperapido/dixdybot/` + **shim: `brain.js` del vivo llama a `llm.ts`** (commit reversible) | El cerebro del bot vivo ya corre tras la puerta única con failover — el seguro contra Anthropic, activo. Métricas midiendo (holgura al 19-ago) |
| **S2 · 4-10 ago** | **E2** | Contrato `Modulo` + `config.ts` + vista Ajustes renderizada desde `z.toJSONSchema`; tarifario/persona/ajustes como datos en `data/` del clon; **ingesta completa: `imagen.ts` + `audio.ts`** (OK de plata a Alejandro por Groq) + `documento.ts`; panel PWA v1 (Hono + vanilla): Conversaciones, Ajustes, Conocimiento v1 (tarjetas), **embudo por etapa** | El bot VE fotos y ESCUCHA notas de voz (los dos casos perdidos de julio, resueltos); el dueño administra módulos desde el iPhone |
| **S3-S4 · 11-24 ago** | **E3 (el corazón)** | `motor/`: proyector camino→reglas, evaluador de UNA llamada, resolver Kahn con Resolution explicable, `lint.ts` al guardar, backtesting patrón Fin; migración 68 reglas → 20-30 caminos CON `dominio`; `pausa.ts` 3 capas + relay código 5 letras; `madre.ts`/`especialista.ts`; gimnasio completo (6 personas + juez gate ≥4,0 + replay `forkSession`) | Caminos vivos tras flag `CAMINOS_ON` con gate del juez; el dueño aprueba dudas desde WhatsApp; aprendizaje en caliente con reanudación |
| **S5 · 25-31 ago** | **E4 (cutover)** | `CanalWaBaileys` envuelve los órganos trasplantados; un-solo-escritor a 5 tablas; `migrar.ts` one-shot JSONL→SQLite; 48 h de sombra con canal `sim`; **launchd pasa a `dixdybot/src/index.ts`; el vivo queda de fallback congelado 30 días**. Gate: gimnasio verde + juez ≥4,0 + **Sonnet 5 probado antes del 31-ago** | El núcleo ES el bot de producción; panel lee las 5 tablas (✓✓ reales, quién-cotizó en el dato, dormidos gratis) |
| **Sep (2ª quincena)** | **E5** | `wa-cloud/` contra `meta-buzon` (webhook builderbot: verify + HMAC rawBody + extractStatus); piloto en número secundario; `ventana()` real + `enviarPlantilla` + seguimiento de cotización abandonada; `ig/` en una tarde; **decisión Coexistence 30-sep** (Baileys fallback caliente 30-60 días; queda como rampa de clientes nuevos) | El número vivo migra a la vía oficial ANTES del cobro del 1-oct y del enforcement; atribución CTWA en el ledger |
| **Oct →** | **E6 (continuo)** | SETUP.md de clonado formalizado; API key por cliente con expiración; Cloudflare Access; pricing 4-6 / 8-12 UF + setup 5-10 UF; verificación Tech Provider DIXDY arranca; contrato encargo de tratamiento + ARCO+P en panel (antes del 1-dic, Ley 21.719) | dixdybot = producto; cliente nuevo = clonar + formulario + Baileys día 1 → Coexistence esa semana |
| **Después** | E7 | Solo carpeta `voz/` con evidencia (Avoca, Retell ~US$0,09-0,15/min). NO se construye | — |

**Toda semana termina con**: `tsc --noEmit` verde + vitest verde + registro en
`actividad.py` + lo reutilizable promovido al maestro.

---

## 8. Principios de sencillez (lo que este sistema NO tiene)

La lista es parte del diseño: cada NO es una decisión con dueño y fecha, no una omisión.

| NO tiene | Por qué |
|---|---|
| **Bun** | 1.3.x aún parchea compat Node cada release; el cerebro vive de `child_process`; cero pares en la clase. Re-evaluar solo si existe Bun 2.0 + un bot 24/7 probado meses |
| **Docker** | Mac mini + launchd: una VM extra es otra capa que muere. El sandbox de agentes lo dan los permisos de `claude -p` |
| **Redis / BullMQ / colas externas** | La cola promise-chain por conversación + SQLite cubren el caso; un Redis caído es un modo de fallo REGALADO |
| **ORM (Prisma/Drizzle)** | 5 tablas, un escritor: SQL a mano con prepared statements es MÁS legible para la IA que una DSL |
| **Postgres/MySQL** | Servidor aparte que administrar; SQLite es cero-ops y suficiente por años |
| **Monorepo (turbo/nx/lerna/workspaces)** | No publicamos paquetes; el clon copia el repo. Workspaces se agregan en una tarde SI E6 lo exigiera |
| **dotenv, nodemon, tsx, paso de build** | Node 24 nativo: `--env-file`, `--watch`, type stripping. launchd apunta al `.ts` |
| **`enum`, decoradores, namespaces** | Rompen el type stripping; uniones de literales en su lugar |
| **NestJS/Express/Fastify** | Hono con cero deps hace todo; Fastify valida con ajv (chocaría con Zod fuente única) |
| **React/Next en el panel v1** | PWA vanilla + DaisyUI opcional (decidido en el plan); Next recién si E6 justificara reescritura |
| **Canvas de nodos** | Tarjetas + diff + Aprobar + stepper vertical (decidido; el mercado serio abandonó el canvas) |
| **App nativa iOS** | PWA instalable + push por avisos-worker (decidido) |
| **Segundo transcriptor / Gemini / whisper local obligatorio** | Groq + pausa-y-pregunta como fallback; local solo por privacidad o si Groq molesta |
| **n8n/Dify/plataformas low-code** | Licencias hostiles a revender; el gateway propio delgado está ratificado |
| **Segundo proceso / workers paralelos / crons nuevos** | UN proceso Node + launchd + los motores DIXDY que ya existen (doctrina: lo nuevo se SUMA) |
| **tenant_id / multi-tenancy en DB** | Clon-por-cliente (aislamiento por filesystem, doctrina DIXDY); de los multi-tenant solo patrones puntuales |

**Números auditables de sencillez**: 6 deps runtime · 1 proceso · 1 archivo que toca la DB
· 1 puerta al cerebro · 1 llamada LLM por turno · 1 proveedor nuevo (Groq) · 0 pasos de build.

---

## 9. Riesgos y reversibilidad

| Riesgo | Mitigación en este diseño |
|---|---|
| Anthropic reactiva metering de `claude -p` | `llm.ts` primero (S1); cadena con `api` probada con juez antes del 31-ago; ledger midiendo desde S1 |
| Ban de Baileys antes de migrar | Circuit breaker (S0) + expediente Meta precargado (pre-etapa) = emergencia en horas; `wa-cloud/` es "otra factory" |
| El cutover S5 sale mal | El vivo queda congelado 30 días; rollback = re-apuntar launchd; datos: JSONL histórico intacto + `bot.db` regenerable con `migrar.ts` |
| SQLite se queda chico | Imposible a esta escala; y `db.ts` es el único archivo que lo sabe (node:sqlite o lo que sea = 1 archivo) |
| Groq se cae / sube precio | Fallback pausa-y-pregunta sin segundo proveedor; whisper.cpp local documentado |
| Un módulo nuevo rompe el turno | Config inválida → default + aviso; soft-disable desde el panel; snapshot por turno = nunca a mitad de turno |
| Ley 21.719 (1-dic) | Datos del cliente SOLO en su clon (ya cumple minimización); ARCO+P y contrato de encargo en E6 con fecha |

## Fuentes de este blueprint

- `mejoras-destaperapido/investigacion-dixdybot/ronda4/planos-sintesis.md` (5 planos de oro, decisiones de conflicto, lo genuinamente nuestro)
- `mejoras-destaperapido/investigacion-dixdybot/ronda2/plan-revisado.md` (E0-E7, fechas duras, regla de contingencia)
- `mejoras-destaperapido/DIXDYBOT-ESTADO.md` (requisitos no negociables, ajustes ronda 3)
- `scratchpad/informes5/stack-2026.md` · `media-ingesta-canales.md` · `procesar-media-ia.md` · `media-ingesta.md` (verificados 23-jul-2026)
- Patrón de módulos del maestro: `DIXDY/correo-worker/`, `DIXDY/panel-cliente/`, `DIXDY/whatsapp-bot/`
