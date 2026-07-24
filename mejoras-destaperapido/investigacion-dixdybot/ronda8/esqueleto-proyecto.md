# EL ESQUELETO DEL PROYECTO dixdybot — scaffold definitivo desde 0

**Fecha: 24-jul-2026 · Arquitecto del esqueleto · Reconcilia:** blueprint r5
(`ronda5/blueprint-fundacional.md`) + prototipo v4 de 18 iteraciones
(`scratchpad/dixdybot-prototipo.html`, bloque DATA + funciones JS) + gapcheck r7
(auditoría de modularidad, flujos motor/embudo, matriz visión→prototipo) + las 5 memorias
de decisiones post-blueprint (pausa junior→senior, flujo chats y config, IA madre,
genérico-modular, design system).

**Principio del dueño, cumplido al pie de la letra:** el proyecto nace DE CERO, limpio y
bonito. Nunca se clona el bot viejo; los órganos sanos se trasplantan como archivos
escogidos (§3). Clon-por-cliente = clonar el molde nuevo. El primer día de código es
copiar este esqueleto.

---

## 0. Qué cambió después del blueprint r5 y dónde aterriza en el scaffold

El blueprint r5 sigue siendo el documento rector de stack y arquitectura profunda. Estas
son las decisiones que el prototipo y las memorias agregaron DESPUÉS, ya reconciliadas:

| # | Decisión post-blueprint (fuente) | Dónde aterriza |
|---|---|---|
| 1 | **Pausa junior→senior con 2 checks**: resumen del caso, evaluación bidireccional (el agente discute con argumentos), check 1 = responder al cliente YA, check 2 = afinar el camino con calma (memoria pausa-junior-senior; `pausaHTML()` del prototipo) | `schemas/duda.ts` (Duda multi-turno con fases, §2.3) + `motor/duda.ts` + tabla `dudas` en `esquema.sql`. **Reemplaza** al `pausa.ts` de una vuelta del r5 |
| 2 | **Módulos declaran APORTES de UI** — métricas de Hoy, etapas de tablero, campos de ficha, tipos de decisión — para que apagar un módulo limpie el panel solo (auditoría r7; `verFichaConfig()` "cada campo lo aporta un módulo") | `schemas/manifest.ts` v2 con `Aportes` (§2.1); el panel compone Hoy/tablero/ficha SOLO desde módulos activos |
| 3 | **Tablero/etapas = DATOS del módulo Embudo** + tabla `pedidos` (6ª entidad) + `escritor.moverPedido()` única vía + efectos de paso (flujos-motor-embudo r7; `pop-etapas` del prototipo: origen camino/tú/externo) | `modulos/embudo/` + `schemas/pedido.ts` (§2.5) + eventos canónicos `pedido.*` en `eventos.jsonl` |
| 4 | **Conexiones = módulos que aportan HERRAMIENTAS con permiso por herramienta** (Bot solo / Con mi OK / Solo yo), 3 vías (catálogo, MCP, API propia por chat de conexión → Claude Code fabrica), log de actividad, credenciales editables (memoria flujo-chats-config §4; `nuevaConexion()`/`conexionChat()`/`verActividadCx()`) | `src/conexiones/` + `schemas/conexion.ts` (§2.4); permiso `con-ok` reusa la máquina Duda |
| 5 | **Chats a escala**: bautizo automático (nombre+comuna+pedido renombra la fila), orden por ATENCIÓN (Esperan algo de ti → Activos → Dormidos auto-archivados), buscador global, etiquetas automáticas grande/nuevo/urgente (memoria flujo-chats-config §1; `renderLista()`/`DORMIDOS`) | columnas `titulo` y `etiquetas` en `conversaciones` (delta al esquema r5) + `modulos/ficha/` (bautizo desde el extractor) + queries de `panel/api/chats.ts` |
| 6 | **Guía conversacional** en Caminos/Módulos/Conexiones/Onboarding: preguntar en contexto, pedir cambios → **Borrador tipado con diff + pruebas + Publicar/Descartar** (funciones `guia()`, `modIA()`, `verBorrador()` del prototipo) | `motor/guia.ts` + `schemas/borrador.ts`; un solo patrón para las 4 superficies |
| 7 | **Onboarding de negocio nuevo**: describe el negocio (texto/audio/URL) → propuesta COMPLETA como diff aprobable (agente, módulos, etapas, ficha, caminos borrador, encargos a Claude Code); cada negocio = su propio dixdybot (`nuevoNegocio()` del prototipo; memoria §5) | `panel/api/onboarding.ts` + `plantillas/onboarding.md` + Borrador tipo `negocio` |
| 8 | **Seguimientos programados VISIBLES** en el hilo (tarjeta "se enviará el vie 10:00" + Editar/Cancelar) (chat `jorge` del prototipo) | tabla `seguimientos` (migración de `modulos/seguimiento/`) + prog-card en el panel |
| 9 | **Correo multi-modo por negocio**: reenvío (recomendado), Gmail OAuth, IMAP hosting, crear con dominio o `@dixdybot.cl` (memoria §2; `verCorreoConfig()`) | `canales/correo/` con `modos.ts`; destaperapido = puente al correo-worker que ya opera |
| 10 | **Gate de activación de agente**: nota juez ≥ 4,0 para pasar de "practicando" a "activa" (AGENTES.destapes del prototipo) | `agentes/gate.ts` |
| 11 | **Cobros separado de Entregas** (huérfano #1 de la auditoría r7: un rubro sin repartidor igual cobra) | `modulos/cobros/` (quién marca, medios de pago, `cobrado_cuando`) |
| 12 | **Encargos a Claude Code**: la IA solo activa/configura lo que EXISTE; lo inexistente se encarga, se fabrica aparte con manifest+pruebas, aparece en el catálogo y el dueño lo activa (límite duro de Alejandro) | `data/encargos/` en el clon + registro en la **cola única** del maestro (doctrina DIXDY: nada de workers nuevos) |
| 13 | **Design system único** (tokens del prototipo: n1-n12, acento, ámbar, rojo, azul; vista Diseño como guardián) | `panel/pwa/tokens.css` nace el DÍA 1 copiado del `<style>` del prototipo; regla: ningún componente fuera de la vista Diseño |
| 14 | **Handoff con vuelta**: Tomar / Devolver a Sofía, bot se calla 30 min si el dueño escribe (flujos r7 §2.2; `enviarTu()`) | `conversaciones.asignado` + `panel/api/chats.ts`; config del silencio en `modulos/` base |

Todo lo demás del r5 queda VIGENTE sin cambios: stack (§4 de este doc), 10 decisiones
fundacionales, ingesta multimodal, llm.ts, interfaz Canal, los 16 NOes de sencillez, el
calendario S0-S5 y las fechas duras (19-ago métricas, 30-sep Coexistence, 1-oct cobro
Meta, 1-dic Ley 21.719).

---

## 1. Estructura de carpetas COMPLETA y comentada

Repo **PLANO** (un `package.json`, patrón NanoClaw), tests colocalizados
(`x.test.ts` junto a `x.ts`). Vive en `/Users/alejandroriveracarrasco/SaSS/DIXDY/dixdybot/`
como módulo genérico del maestro (cero datos de cliente), hermano de `correo-worker/`,
`panel-cliente/`, `whatsapp-bot/`.

**Marcas de nacimiento:** `[D1]` = nace el día 1 (S0, esqueleto compilable con vitest
verde) · `[S1]` `[S2]` `[S3-4]` `[S5]` = semana del plan · `[E5]` `[E6]` = etapa posterior.

```
dixdybot/
├── package.json                   [D1] pnpm 11.17 pineado (packageManager); 6 deps runtime
│                                  #    exactas: baileys, better-sqlite3, hono,
│                                  #    @hono/node-server, @hono/zod-validator, zod
├── tsconfig.json                  [D1] strict, module nodenext, erasableSyntaxOnly, noEmit
├── config.example.env             [D1] plantilla → el clon la copia a .env.local (gitignored)
├── .gitignore                     [D1] .env.local, auth/, data/, *.log
├── SETUP.md                       [D1] instanciar por cliente (patrón correo-worker); crece hasta E6
├── MANUAL.md                      [S5] operación diaria + runbook Coexistence
├── launchd/
│   ├── com.dixdy.dixdybot.plist       [D1] apunta DIRECTO a src/index.ts (type stripping, sin build)
│   └── com.dixdy.respaldo.plist       [D1] VACUUM INTO diario de bot.db + respaldo auth/
├── plantillas/                    # textos genéricos SIN datos de cliente
│   ├── persona-base.md            [D1] la voz genérica; el clon la especializa en data/persona/
│   ├── onboarding.md              [S2] guion de la entrevista de negocio nuevo (→ Borrador 'negocio')
│   └── enlatadas.md               [S3-4] respuestas de espera de duda, fallos de media, fuera de horario
│
├── src/
│   ├── index.ts                   [D1] arranque: valida config (Zod) → abre db → migraciones core y
│   │                              #    de módulos → monta módulos activos → factory de canales →
│   │                              #    panel Hono → timbre. UN solo proceso.
│   │
│   ├── core/                      # el corazón; nada aquí conoce un canal ni un rubro
│   │   ├── db.ts                  [D1] ÚNICO archivo que toca better-sqlite3 (WAL, prepared, txn)
│   │   ├── esquema.sql            [D1] las 6 tablas núcleo (§2.7) + índices + schema_version
│   │   ├── escritor.ts            [D1] un-solo-escritor de TODA tabla; dedup INSERT OR IGNORE;
│   │   │                          #    [S2] gana moverPedido(pedidoId, a, origen, porque) —
│   │   │                          #    la única puerta que cambia pedidos.etapa (§2.5)
│   │   ├── llm.ts                 [S1] puerta única al cerebro: cola, snapshot de config, cadena
│   │   │                          #    sdk→cli→api→plantilla, sesión en `init`, ledger uso-llm
│   │   ├── cola.ts                [S1] promise-chain por conversación (FIFO por chat, limpieza del Map)
│   │   ├── bus.ts                 [D1] eventos internos tipados (EventoCanal → gating → cerebro → envío)
│   │   ├── config.ts              [D1] lee data/ajustes/*.json del clon, valida contra el schema del
│   │   │                          #    módulo, cache TTL 30 s + SNAPSHOT por turno
│   │   ├── ledger.ts              [D1] append-only JSONL: uso-llm, eventos (incl. pedido.* y
│   │   │                          #    conexion.uso), envios (ledger delivered)
│   │   └── schemas/               [D1 TODOS — los contratos nacen ANTES que el código que los usa]
│   │       ├── mensaje.ts         #    MensajeEntrante, MediaEntrante/ConBinario, MediaSaliente,
│   │       │                      #    ResultadoEnvio (sin cambios r5)
│   │       ├── llm.ts             #    ConsultaLLM, RespuestaLLM, UsoLLM, errores tipados (sin cambios r5)
│   │       ├── camino.ts          #    Camino v2: dominio + pasos con EFECTOS + pruebas doradas (§2.2)
│   │       ├── manifest.ts        #    ManifestModulo + contrato Modulo v2 con APORTES (§2.1)
│   │       ├── duda.ts            #    Duda multi-turno con fases junior→senior (§2.3) — antes pausa.ts
│   │       ├── conexion.ts        #    Conexion + HerramientaConexion + permisos (§2.4)
│   │       ├── pedido.ts          #    Pedido, Etapa, ConfigEmbudo, EventoPedido (§2.5)
│   │       └── borrador.ts        #    Borrador tipado de la guía: diff + pruebas + publicar (§2.6)
│   │
│   ├── organos/                   # TRASPLANTES del bot vivo (§3) — .js tal cual, conviven por type
│   │   ├── gating.js              [S5] debounce + timbre + anti-flood (probado en producción)
│   │   ├── extraer.js             [S2] extractor de ficha + fechaISO (ÚNICO juez de fechas);
│   │   │                          #    alimenta el bautizo de modulos/ficha
│   │   └── integracion.js         [S2] cotizar/PDF/Supabase/repartidor; se DESARMA en E2 hacia
│   │                              #    modulos/cotizador (clon) + conexiones fabricadas
│   │
│   ├── canales/                   # la factory; el core JAMÁS ve un vendor
│   │   ├── canal.ts               [D1] LA interfaz Canal + eventos canónicos (sin cambios r5)
│   │   ├── factory.ts             [D1] arranca canales según config; sin credenciales → null =
│   │   │                          #    canal apagado sin romper el boot
│   │   ├── sim/                   [D1] canal simulado: gimnasio, tests, replay, 48 h de sombra —
│   │   │                          #    ciudadano pleno desde el primer commit
│   │   ├── wa-baileys/            [S5] adaptador Baileys 7.0.0-rc.9 pineado
│   │   │   ├── adaptador.ts       #    backoff+circuit breaker, LID translateJid, ventana()={abierta}
│   │   │   ├── media.ts           #    downloadMediaMessage + reuploadRequest
│   │   │   └── legado/            #    enviar.js + outbox.js TRASPLANTADOS (candado anti-jid,
│   │   │                          #    auto-sanación Bad MAC — §3)
│   │   ├── wa-cloud/              [E5] Cloud API contra Worker meta-buzon
│   │   │   ├── adaptador.ts       #    ventana() real, enviarPlantilla, árbol plantilla/sesión/failed
│   │   │   ├── media.ts           #    GET /{media-id} → URL 5 min → Bearer
│   │   │   └── webhook.ts         #    verify GET + HMAC timingSafeEqual + extractStatus
│   │   ├── ig/                    [E5] Instagram DM (una tarde, mismo cerebro)
│   │   └── correo/                [E5] canal correo MULTI-MODO (decisión post-blueprint):
│   │       ├── adaptador.ts       #    hilo de correo = conversación más; adjuntos → ingesta
│   │       └── modos.ts           #    reenvio (recomendado, cero config) | gmail-oauth |
│   │                              #    imap-hosting | dominio-propio | dixdybot-cl
│   │                              #    destaperapido: puente al correo-worker que YA opera
│   │
│   ├── ingesta/                   [S2] multimodal; corre ANTES del cerebro; administrable (sin cambios r5)
│   │   ├── index.ts               #    placeholder al hilo YA → guardar → procesar async
│   │   ├── guardar.ts             #    ÚNICO que toca binarios; nombre SIEMPRE generado
│   │   ├── anotar.ts              #    cache .anotacion.json + reemplaza placeholder
│   │   └── procesadores/          #    imagen.ts (visión) · audio.ts (Groq) · documento.ts (PDF) ·
│   │                              #    video.ts (v1: solo ficha)
│   │
│   ├── motor/                     [S3-4] caminos — el corazón del producto
│   │   ├── proyector.ts           #    camino→reglas transitorias (LA joya de Parlant: un solo motor)
│   │   ├── evaluador.ts           #    UNA llamada LLM por turno → EvaluacionTurno (rationale antes
│   │   │                          #    del booleano)
│   │   ├── resolver.ts            #    determinista post-LLM: Kahn → prioridad → entailment;
│   │   │                          #    cada decisión = Resolution con porqué humano (la traza del panel)
│   │   ├── efectos.ts             #    NUEVO r7: ejecuta los efectos del paso completado
│   │   │                          #    (crear_pedido, mover_pedido → escritor.moverPedido,
│   │   │                          #    registrar_cobro, programar_seguimiento, avisar_dueno,
│   │   │                          #    usar_herramienta → conexiones/permisos). El LLM solo declara
│   │   │                          #    que el paso terminó; el movimiento es determinista.
│   │   ├── duda.ts                #    máquina de fases junior→senior (§2.3): resumen → respuesta →
│   │   │                          #    evaluación bidireccional (contra-argumenta) → check1 responde
│   │   │                          #    al cliente YA → check2 afina el camino con calma → camino
│   │   │                          #    nuevo con badge. Reanudación sin repetir pasos. Relay código
│   │   │                          #    5 letras por WhatsApp; primera respuesta gana.
│   │   ├── guia.ts                #    NUEVO: edición conversacional (Caminos/Módulos/Embudo/
│   │   │                          #    Conexiones/Onboarding). Contexto = catálogo + caminos +
│   │   │                          #    métricas; salida = Borrador tipado (§2.6). Lo que no existe
│   │   │                          #    → encargo a Claude Code, JAMÁS activar solo.
│   │   └── lint.ts                #    al guardar camino: frontmatter, CERO cifras en el cuerpo, máx
│   │                              #    una transición sin condición, efectos → etapas existentes con
│   │                              #    origen 'camino' permitido; lint INVERSO al editar embudo.json
│   │
│   ├── agentes/                   [S3-4] IA madre → especialistas
│   │   ├── madre.ts               #    dispatcher: obvio→directo gratis · "hola" pelado→saludo neutro ·
│   │   │                          #    ambiguo→UNA aclaración (los 3 casos del pop-madre del
│   │   │                          #    prototipo); PROHIBIDO responder hechos; ack < 2 s; deriva EN
│   │   │                          #    SILENCIO; con 1 solo agente se auto-omite
│   │   ├── especialista.ts        #    persona base + fragmentos de módulos del dominio + SOLO
│   │   │                          #    caminos del dominio proyectados + tools SOLO del paso
│   │   ├── componer.ts            #    prompt por fragmentos en cada turno (claude-md-compose)
│   │   └── gate.ts                #    NUEVO: activación de agente por nota juez ≥ 4,0 (mismo listón
│   │                              #    que pasó Sofía); "practicando" → "activa" queda en eventos.jsonl
│   │
│   ├── conexiones/                [S2] NUEVO (decisión post-blueprint): APIs/MCP como herramientas
│   │   ├── registro.ts            #    carga data/ajustes/conexiones.json + data/conexiones/*.ts del
│   │   │                          #    clon; expone herramientas activas como tools MCP-compatibles
│   │   ├── permisos.ts            #    aplica bot|con-ok|solo-dueno por herramienta y por agente;
│   │   │                          #    'con-ok' crea una Duda de aprobación (misma bandeja de Hoy);
│   │   │                          #    cada uso → eventos.jsonl ('conexion.uso') + traza del chat
│   │   ├── mcp.ts                 #    cliente MCP genérico: pegar URL → descubrir herramientas solas
│   │   └── catalogo/              #    conectores conocidos config-driven (supabase.ts primero;
│   │                              #    google-calendar, webpay… se agregan cuando un cliente los pida)
│   │                              #    Los FABRICADOS (API propia vía chat de conexión) viven en el
│   │                              #    CLON (data/conexiones/) — Claude Code los fabrica con pruebas
│   │
│   ├── modulos/                   # capacidades enchufables; cada una cumple Modulo v2 (§2.1)
│   │   ├── indice.ts              [D1] barrel: UNA línea de import por módulo (instalador = documento)
│   │   ├── embudo/                [S2] EL TABLERO COMO DATOS (r7):
│   │   │   ├── modulo.ts          #    manifest + configSchema (Etapa/ConfigEmbudo §2.5) + aportes
│   │   │   ├── migracion.sql      #    tabla pedidos (la 6ª entidad de negocio)
│   │   │   └── consultas.ts       #    tablero por etapa, plata por columna, embudo con tasas
│   │   ├── ficha/                 [S2] extractor administrable: aporta camposFicha; BAUTIZO del chat
│   │   │                          #    (nombre+comuna+pedido → conversaciones.titulo) + ETIQUETAS
│   │   │                          #    automáticas (grande >umbral, nuevo, urgente — nunca manuales)
│   │   ├── precios/               [S2] tarifario-en-datos (data/ajustes/precios.json) + validador
│   │   │                          #    precioCoherente POST-generación (la doble muralla)
│   │   ├── cotizador/             [S2] genérico: arma cotización desde ficha+precios, PDF, "último
│   │   │                          #    click" (Siempre yo | Solo si no calza | Automático); aporta
│   │   │                          #    etapas cotizando/por-confirmar + hero de plata + decisión
│   │   │                          #    aprobar-cotizacion. Lo específico del rubro vive en el clon.
│   │   ├── cobros/                [S2] SEPARADO de entregas (auditoría r7): quién marca (repartidor/
│   │   │                          #    dueno/bot), medios de pago, cobrado_cuando total|primer_abono
│   │   ├── seguimiento/           [S2-S3] recordatorios + cotización abandonada; migracion.sql →
│   │   │                          #    tabla seguimientos; los programados son VISIBLES en el hilo
│   │   │                          #    (prog-card Editar/Cancelar) — nunca un envío sorpresa
│   │   ├── calidad/               [S3-4] el gimnasio administrable: práctica nocturna on/off,
│   │   │                          #    frecuencia, gate del juez, presupuesto LLM del juez
│   │   └── (entregas/, agenda/…)  #    del rubro: nacen en el CLON y se promueven si son genéricos
│   │
│   ├── panel/                     # PWA del dueño (iPhone primero); Hono
│   │   ├── servidor.ts            [S2] /api/* + estáticos + webhooks; @hono/zod-validator en el borde
│   │   ├── api/
│   │   │   ├── hoy.ts             [S2] compone: dudas pendientes + decisiones (tiposDecision de
│   │   │   │                      #    módulos) + borradores + métricas desde APORTES activos;
│   │   │   │                      #    resueltas colapsan
│   │   │   ├── chats.ts           [S2] orden por ATENCIÓN (Esperan algo de ti → Activos → Dormidos),
│   │   │   │                      #    buscador global (nombre/comuna/pedido/contenido), Tomar/
│   │   │   │                      #    Devolver, ficha compuesta desde aportes
│   │   │   ├── caminos.ts         [S3-4] cascada por grupos con uso/cierre/plata, peek, historial,
│   │   │   │                      #    pruebas doradas, borrador→publicar (candado del lint)
│   │   │   ├── guia.ts            [S3-4] endpoint de motor/guia.ts (las 4 superficies conversacionales)
│   │   │   ├── modulos.ts         [S2] GET catálogo {manifest, jsonSchema, config, activo, aportes};
│   │   │   │                      #    la vista Ajustes se RENDERIZA desde z.toJSONSchema — cero
│   │   │   │                      #    pantallas a mano; PUT valida y commitea en el git del clon
│   │   │   ├── conexiones.ts      [S2] alta (catálogo/MCP/chat de conexión), permisos por
│   │   │   │                      #    herramienta, credencial editable, log de actividad
│   │   │   ├── agentes.ts         [S3-4] madre navegable, especialistas, gate 4,0, presets de persona
│   │   │   ├── embudo.ts          [S2] tablero desde pedidos + "¿por qué está aquí?" (último
│   │   │   │                      #    pedido.movido), mover a mano con transiciones acotadas +
│   │   │   │                      #    Perdido con motivo, editar etapas (diff aprobable)
│   │   │   ├── dudas.ts           [S3-4] la mini-conversación junior→senior (píldora del hilo y
│   │   │   │                      #    tarjeta de Hoy = el MISMO objeto)
│   │   │   ├── gimnasio.ts        [S3-4] Probar (impersonar cliente), replays, veredicto del juez
│   │   │   └── onboarding.ts      [S2] entrevista → Borrador 'negocio' → crear clon configurado
│   │   └── pwa/
│   │       ├── tokens.css         [D1] EL design system del prototipo (n1-n12, ac/amb/rojo/azul,
│   │       │                      #    dark mode, .fila/.chip/.pto/.btn/.traza/.diff/.sw) — se copia
│   │       │                      #    del <style> del prototipo el día 1; cero variaciones
│   │       ├── index.html         [S2] shell L invertida 240px + vistas
│   │       ├── app.js             [S2] vanilla; las funciones del prototipo son la spec de interacción
│   │       ├── vistas/            [S2→] hoy · chats · caminos · modulos · agentes · diseno
│   │       ├── manifest.json      [S2] PWA instalable
│   │       └── sw.js              [S2] offline básico + push por avisos-worker (VAPID ya operativo)
│   │
│   ├── gimnasio/                  # calidad; el juez es un SCRIPT, no un test
│   │   ├── personas.ts            [D1 esqueleto · S3-4 completo] 6 guiones fijos SIN LLM = regresión
│   │   │                          #    determinista en vitest (corre contra canal sim desde el día 1)
│   │   ├── juez.ts                [S3-4] veredicto tipado {verde|amarillo|rojo, hallazgos con
│   │   │                          #    evidencia, sugerencia aplicable}; alimenta gate ≥ 4,0
│   │   └── replay.ts              [S3-4] forkSession sin contaminar + backtesting patrón Fin al editar
│   │
│   └── cli/                       # operación (una persona + IA)
│       ├── doctor.ts              [D1] healthcheck: db, auth, canal, cerebro, ledgers, disco
│       ├── migrar.ts              [S5] migraciones esquema + one-shot JSONL del vivo → tablas
│       ├── vincular.ts            [S5] pairing por código sin QR (adaptado de link-code.mjs)
│       └── juez.ts                [S3-4] correr juez/backtesting a mano
```

**En el CLON del cliente** (para destaperapido: `~/SaSS/destaperapido/dixdybot/`, junto al
bot vivo mientras dura el estrangulamiento):

```
dixdybot/                          # copia del template del maestro
├── .env.local                     # credenciales (gitignored): canal, GROQ_API_KEY, ANTHROPIC_API_KEY
├── auth/                          # sesión del canal (gitignored, respaldada por launchd)
└── data/                          # TODO el estado del cliente
    ├── bot.db                     # SQLite (6 tablas núcleo + las de módulos) — VACUUM INTO diario
    ├── media/<convId>/<msgId>.<ext> (+ .anotacion.json)
    ├── caminos/*.yml              # el conocimiento del negocio, versionado en el git DEL CLON
    ├── pruebas/*.yml              # pruebas doradas compartidas (los caminos las referencian)
    ├── ajustes/<modulo>.json      # config por módulo (embudo.json = LAS ETAPAS del rubro;
    │                              #   conexiones.json; precios.json = el tarifario)
    ├── conexiones/*.ts            # conectores FABRICADOS por Claude Code (API propia, con pruebas)
    ├── credenciales.json          # secretos de conexiones, editables desde el panel (gitignored)
    ├── encargos/*.md              # encargos a Claude Code pendientes/fabricados (v. cola única DIXDY)
    ├── persona/base.md + fragmentos/
    └── ledgers/uso-llm.jsonl · eventos.jsonl · envios.jsonl
```

---

## 2. Los contratos núcleo ACTUALIZADOS (TypeScript real)

Convenciones r5 vigentes: PROHIBIDO `enum` TS (uniones de literales; `z.enum` sí, es
runtime), imports con extensión `.ts`, `z.infer` único origen de tipos, dominio en
español. Todo esto vive en `src/core/schemas/` desde el DÍA 1.

### 2.1 `manifest.ts` — Modulo v2 con APORTES (cierra la brecha #1 de la auditoría r7)

```ts
// src/core/schemas/manifest.ts
import { z } from 'zod';
import type { Hono } from 'hono';
import { Etapa } from './pedido.ts';
import type { MensajeEntrante } from './mensaje.ts';
import type { HerramientaMCP, ContextoModulo } from './llm.ts';

export const ManifestModulo = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/),      // 'embudo', 'ficha', 'precios', 'cotizador'
  nombre: z.string(),                         // verbo de dueño: 'Cotiza', 'Te pide ayuda cuando no sabe'
  descripcion: z.string(),                    // una frase en simple
  consecuenciaApagar: z.string(),             // visible en la fila: "se van el hero de plata y la
                                              //   etapa Cotizando" (decisión del prototipo)
  categoria: z.enum(['venta', 'operacion', 'canales', 'base']),  // secciones de la vista Módulos;
                                              //   'base' = núcleo no-apagable, solo-lectura
  version: z.string(),
  dominio: z.string().nullable(),             // si aporta conocimiento/tools a UN especialista
  requiere: z.array(z.string()).default([]),
});
export type ManifestModulo = z.infer<typeof ManifestModulo>;

/** LO NUEVO r7: todo lo VISIBLE pertenece a un módulo. El panel compone Hoy, el tablero
 *  y la ficha SOLO desde los aportes de módulos activos → apagar un módulo limpia sus
 *  columnas, métricas, campos y decisiones sin tocar código de panel. */
export const AporteMetricaHoy = z.object({
  id: z.string(),
  etiqueta: z.string(),                       // 'cotizaciones', 'en juego hoy'
  tipo: z.enum(['hero', 'contador']),         // hero = la cifra grande; si hay varios gana prioridad
  prioridad: z.number().int().default(0),
  consulta: z.string(),                       // id de consulta con nombre registrada por el módulo
});

export const AporteCampoFicha = z.object({
  id: z.string(),                             // 'comuna', 'fechas', 'correo'
  etiqueta: z.string(),
  seccion: z.string().default('Ficha'),       // 'Ficha' | 'Cotización' | 'Entrega' | propia
  tipo: z.enum(['texto', 'numero', 'fecha', 'monto', 'correo', 'telefono', 'url']).default('texto'),
  requerido: z.boolean().default(false),      // el extractor lo persigue; gatilla "Datos completos ✓"
});

export const AporteTipoDecision = z.object({
  id: z.string(),                             // 'aprobar-cotizacion', 'ok-despacho'
  descripcion: z.string(),
  acciones: z.array(z.string()).min(1),       // botones de la tarjeta en Hoy: ['Aprobar', 'Ver']
});

export const Aportes = z.object({
  metricasHoy: z.array(AporteMetricaHoy).default([]),
  etapasTablero: z.array(Etapa).default([]),  // DEFAULTS que embudo.json adopta al activar el módulo
                                              //   (cotizador → cotizando, por-confirmar; cobros →
                                              //   cobrado; entregas → por-entregar). El dueño después
                                              //   las edita como datos suyos.
  camposFicha: z.array(AporteCampoFicha).default([]),
  tiposDecision: z.array(AporteTipoDecision).default([]),
});
export type Aportes = z.infer<typeof Aportes>;

/** El contrato que TODO módulo cumple. Registrarse = una línea en modulos/indice.ts. */
export interface Modulo<C = unknown> {
  manifest: ManifestModulo;

  /** El MISMO schema (1) valida data/ajustes/<id>.json, (2) z.toJSONSchema() dibuja la
   *  vista Ajustes solo, (3) tipa el snapshot por turno. Módulo nuevo = pantalla nueva,
   *  cero código de panel. */
  configSchema: z.ZodType<C>;
  configDefault: C;

  /** v2: aportes de UI en función de la config (p.ej. el umbral de la etiqueta 'grande'). */
  aportes?(config: C): Aportes;

  /** v2: migraciones SQL propias (embudo → pedidos; seguimiento → seguimientos),
   *  aplicadas por cli/migrar.ts con schema_version — el core no las conoce. */
  migraciones?: string[];

  fragmentoPersona?(config: C): string;
  herramientas?(config: C): HerramientaMCP[];
  alMensaje?(msg: MensajeEntrante, ctx: ContextoModulo): Promise<void>;
  rutasPanel?(): Hono;
  iniciar?(config: C, ctx: ContextoModulo): Promise<void>;
  detener?(): Promise<void>;
}
```

### 2.2 `camino.ts` — Camino v2: dominio + pasos con EFECTOS + pruebas doradas

```ts
// src/core/schemas/camino.ts
import { z } from 'zod';

/** r7: cómo un camino mueve el mundo. El LLM SOLO declara paso_completado; los efectos
 *  son deterministas, validados contra la config del embudo/conexiones. Doctrina idéntica
 *  a "cifras del tarifario, nunca del modelo". */
export const Efecto = z.object({
  tipo: z.enum(['crear_pedido', 'mover_pedido', 'registrar_cobro',
                'programar_seguimiento', 'avisar_dueno', 'usar_herramienta']),
  a: z.string().optional(),                    // etapa destino (mover_pedido)
  herramienta: z.string().optional(),          // 'repartidor:crear_entrega' (usar_herramienta;
                                               //   pasa por conexiones/permisos.ts)
  plazoHoras: z.number().optional(),           // programar_seguimiento
});

export const Paso = z.object({
  id: z.string(),
  tipo: z.enum(['mensaje', 'tool', 'pausa-dueno', 'decision']).default('mensaje'),
  accion: z.string(),                          // NL o plantilla_id (cifras SIEMPRE desde tools)
  herramientas: z.array(z.string()).default([]),  // habilitadas SOLO durante este paso (Parlant)
  efectos: z.array(Efecto).default([]),        // r7: corren AL COMPLETARSE el paso, deterministas
  espera_del_cliente: z.boolean().default(true),
  continua: z.boolean().default(false),
  respuestas: z.array(z.object({
    plantilla: z.string(),
    campos_generativos: z.array(z.string()).default([]),
  })).default([]),
  timeout_horas: z.number().optional(),        // solo pausa-dueno
  respuesta_espera: z.string().optional(),     // lo que el cliente ve mientras el dueño decide
});

/** Prototipo: "Pruebas 5/5 ✓ · se re-juegan en cada cambio; si un cambio rompe una
 *  prueba, el borrador NO puede publicarse." Viven en data/pruebas/*.yml (pool
 *  compartido); los caminos las referencian por id. */
export const PruebaDorada = z.object({
  id: z.string(),
  titulo: z.string(),                          // 'Regateo duro (Baños King)'
  guion: z.array(z.object({ de: z.enum(['cliente', 'bot']), texto: z.string() })),
  criterio: z.string(),                        // 'cerró en el piso, no bajó de $150.000'
  tipo: z.enum(['determinista', 'juez']).default('determinista'),
});

export const Camino = z.object({
  id: z.string(),
  version: z.number().int().default(1),
  dominio: z.string(),                         // agente especialista dueño — desde el DÍA 1
  titulo: z.string(),
  grupo: z.string().default('general'),        // la cascada del panel agrupa por esto
                                               //   ('Precios céntricos', 'Cierre y objeciones')
  estado: z.enum(['borrador', 'activo', 'retirado']).default('borrador'),
  origen: z.enum(['manual', 'aprendido']).default('manual'),  // 'aprendido' = nació de una Duda
                                               //   → badge "nuevo" + "nació de la pausa de hoy"
  disparadores: z.array(z.string()).min(1),
  pasos: z.array(Paso).min(1),
  transiciones: z.array(z.object({
    de: z.string(), a: z.string(),
    condicion: z.string().nullable(),          // máx UNA sin condición por paso (lint.ts)
  })),
  relaciones: z.array(z.object({
    tipo: z.enum(['prioridad_sobre', 'depende_de', 'implica', 'desambiguar', 'reevaluar']),
    con: z.string(),
  })).default([]),
  pruebas: z.array(z.string()).default([]),    // ids de PruebaDorada — candado de publicación
  schema_version: z.number().int().default(1),
});
export type Camino = z.infer<typeof Camino>;

/** Lo que el cerebro devuelve por turno — UNA llamada, rationale ANTES del booleano. */
export const EvaluacionTurno = z.object({
  reglas_aplican: z.array(z.object({ id: z.string(), razon: z.string(), aplica: z.boolean() })),
  camino: z.object({
    sigue: z.boolean(),
    paso_completado: z.boolean(),              // → motor/efectos.ts ejecuta los efectos del paso
    transicion_elegida: z.string().nullable(),
  }).nullable(),
  dominio_detectado: z.string().nullable(),
  respuesta: z.string().nullable(),
  plantilla_id: z.string().nullable(),
});
```

### 2.3 `duda.ts` — la Duda multi-turno junior→senior (reemplaza `pausa.ts` del r5)

La píldora en el hilo y la tarjeta en Hoy son el MISMO objeto visto desde dos lugares
(memoria pausa-junior-senior). Las 3 capas del r5 (snapshot suspendido + relay código 5
letras + draft-solo-comete-aprobado) siguen: son el transporte; esto es la conversación.

```ts
// src/core/schemas/duda.ts
import { z } from 'zod';

export const FaseDuda = z.enum([
  'pendiente',      // resumen enviado al dueño (Hoy + push + WhatsApp con código 5 letras)
  'evaluando',      // el dueño respondió; el agente EVALÚA antes de obedecer: si parece error,
                    //   contra-argumenta con datos ("Buin va a $200k y el flete es mayor…") y
                    //   propone alternativa — mini-conversación; el dueño siempre puede imponer
  'check1_listo',   // ✓1 cliente respondido AL TIRO con la decisión — nadie quedó esperando
  'check2_afinando',// ⧗2 generalización con calma: ¿todo el tramo o solo esa comuna?,
                    //   pruebas doradas, choques con otros caminos
  'resuelta',       // camino creado/afinado (origen 'aprendido', badge "nuevo") · deshacer posible
  'expirada',       // timeout_horas sin respuesta → escalada (30 min) ya corrida + enlatada al cliente
]);

export const Duda = z.object({
  id: z.string().length(5),                    // el código del relay ("si abcde" por WhatsApp)
  conversacionId: z.string(),
  agente: z.string(),
  dominio: z.string(),

  /** El resumen tipo junior→senior: el dueño NO lee el chat. */
  resumen: z.object({
    quien: z.string(),                         // 'Carolina · Melipilla'
    quiere: z.string(),                        // '5 baños mensuales para una obra'
    potencial: z.string().nullable(),          // 'sobre $1M al mes' (lo calcula el módulo embudo)
    falta: z.string(),                         // 'no tengo camino para 5 baños en zona lejana'
  }),
  pregunta: z.string(),                        // '¿qué precio le doy?'
  mientrasTanto: z.string(),                   // 'ella junta dirección y fechas' — el chat SIGUE
  respuestaEspera: z.string(),                 // enlatada inmediata que ve el cliente

  fase: FaseDuda,
  turnos: z.array(z.object({                   // la mini-conversación completa, auditable
    de: z.enum(['agente', 'dueno']),
    via: z.enum(['panel', 'whatsapp']).default('panel'),  // primera respuesta gana
    texto: z.string(),
    ts: z.number(),
  })).default([]),
  evaluacion: z.object({                       // la contra-argumentación del agente
    conforme: z.boolean(),
    argumento: z.string(),                     // con datos de caminos/tarifario, nunca inventados
    alternativa: z.string().nullable(),        // 'yo diría $190.000 c/u'
  }).nullable(),
  decisionFinal: z.string().nullable(),        // lo que se usó con el cliente (check 1)
  caminoResultante: z.string().nullable(),     // id del camino creado/afinado (check 2)

  snapshotSuspendido: z.unknown(),             // estado del tema pausado (patrón mastra) — el RESTO
                                               //   del chat nunca se pausa
  timeoutHoras: z.number().default(4),
  escaladaMin: z.number().default(30),         // insistir si no responde (config del módulo base)
  creadaTs: z.number(),
  resueltaTs: z.number().nullable(),
});
export type Duda = z.infer<typeof Duda>;
```

Nota de unificación: una herramienta de conexión con permiso `con-ok` y una decisión de
módulo (`AporteTipoDecision`, ej. aprobar cotización) generan Dudas DEGENERADAS (fase
única de aprobación, sin evaluación bidireccional). Así Hoy tiene UNA sola bandeja y un
solo contador.

### 2.4 `conexion.ts` — Conexiones con herramientas y permisos (nuevo)

```ts
// src/core/schemas/conexion.ts
import { z } from 'zod';

export const PermisoHerramienta = z.enum(['bot', 'con-ok', 'solo-dueno']);
// bot        = el agente la usa solo (queda en traza + actividad)
// con-ok     = el agente propone, se crea Duda de aprobación, comete solo aprobada (draft, boop)
// solo-dueno = jamás disponible para el cerebro; solo botón en el panel

export const HerramientaConexion = z.object({
  id: z.string(),                              // 'crear_entrega'
  descripcion: z.string(),                     // en simple: 'mensaje + pin de Maps al confirmar'
  activa: z.boolean().default(false),          // el dueño elige cuáles se activan
  permiso: PermisoHerramienta.default('con-ok'),
  agentes: z.array(z.string()).nullable().default(null),  // null = todos; o SOLO estos dominios
  esquemaEntrada: z.unknown(),                 // JSON Schema de argumentos (MCP-compatible: las
                                               //   herramientas SON tools del cerebro vía llm.ts)
});

export const Conexion = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/),        // 'repartidor', 'supabase'
  nombre: z.string(),
  origen: z.enum(['catalogo', 'mcp', 'fabricada']),
  // catalogo  = conector conocido del maestro (credenciales guiadas)
  // mcp       = URL pegada; herramientas autodescubiertas (mcp.ts)
  // fabricada = API propia: chat de conexión → la IA explora la doc en SOLO-LECTURA, propone
  //             herramientas y su provecho, el dueño fija permisos, Claude Code fabrica el
  //             conector CON pruebas en data/conexiones/ del clon (encargo asíncrono — nada
  //             se activa solo)
  endpoint: z.string().nullable(),
  credencialRef: z.string().nullable(),        // clave en data/credenciales.json (gitignored,
                                               //   editable desde el panel) — el secreto JAMÁS aquí
  herramientas: z.array(HerramientaConexion),
  estado: z.enum(['conectada', 'error', 'apagada']).default('apagada'),
  ultimoUso: z.object({ ts: z.number(), ok: z.boolean() }).nullable().default(null),
});
export type Conexion = z.infer<typeof Conexion>;

/** Cada uso → eventos.jsonl + la traza del chat donde ocurrió — nada invisible. */
export const EventoConexion = z.object({
  tipo: z.literal('conexion.uso'),
  ts: z.number(),
  conexionId: z.string(),
  herramienta: z.string(),
  convId: z.string().nullable(),
  caminoId: z.string().nullable(),             // qué camino la usó como acción
  agente: z.string().nullable(),
  ok: z.boolean(),
  errorSimple: z.string().nullable(),          // 'clave vencida — se reintentó tras cambiarla'
});
```

### 2.5 `pedido.ts` — Pedido/Etapa: el tablero como datos del módulo Embudo (r7 canónico)

```ts
// src/core/schemas/pedido.ts
import { z } from 'zod';

export const Etapa = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/),        // 'cotizando', 'por-confirmar', 'perdido'
  nombre: z.string(),
  tipo: z.enum(['abierta', 'ganada', 'perdida']),  // semántica terminal → métricas y % cierre
  orden: z.number().int(),
  requiere: z.array(z.string()).default([]),   // campos de ficha exigidos al ENTRAR
  limite_horas: z.number().nullable().default(null),  // SLA → punto ámbar
});
export type Etapa = z.infer<typeof Etapa>;

/** data/ajustes/embudo.json del clon — LAS ETAPAS SON DEL NEGOCIO, no del código.
 *  Editarlas = mismo patrón diff+Aprobar de los caminos, con lint inverso. */
export const ConfigEmbudo = z.object({
  activo: z.boolean().default(true),
  etapas: z.array(Etapa).min(2),
  etapa_inicial: z.string(),
  transiciones: z.array(z.object({
    de: z.string(), a: z.string(),
    origenes: z.array(z.enum(['camino', 'dueno', 'externo'])).min(1),
  })),
  cobrado_cuando: z.enum(['total', 'primer_abono']).default('total'),
  perdido_por_silencio_dias: z.number().nullable().default(null),  // PROPONE, nunca auto-mueve
});

export const OrigenMovimiento = z.discriminatedUnion('clase', [
  z.object({ clase: z.literal('camino'), caminoId: z.string(), pasoId: z.string(),
             turnoRef: z.string() }),
  z.object({ clase: z.literal('dueno'), via: z.enum(['panel', 'whatsapp']),
             gesto: z.enum(['arrastre', 'boton', 'codigo']) }),
  z.object({ clase: z.literal('externo'), fuente: z.string(), ref: z.string().nullable() }),
]);                                            // 'repartidor-supabase' | 'webhook-pago' | 'timeout'

export const Pedido = z.object({
  id: z.string(),                              // 'p-218'
  conversacionId: z.string().nullable(),       // null = alta manual sin chat (llamada/persona);
                                               //   un chat sin pedido JAMÁS ensucia el tablero
  contactoId: z.number().nullable(),
  etapa: z.string(),                           // presente materializado; la HISTORIA va al ledger
  montoNeto: z.number().nullable(),
  saldo: z.number().nullable(),                // cobro parcial = N eventos cobro_registrado
  datos: z.record(z.string(), z.unknown()).default({}),   // la ficha (campos de APORTES)
  motivoCierre: z.string().nullable(),         // OBLIGATORIO si la etapa es tipo 'perdida'
  creadoTs: z.number(),
  actualizadoTs: z.number(),
});
export type Pedido = z.infer<typeof Pedido>;
```

Vía única de escritura: `escritor.moverPedido(pedidoId, a, origen, porque)` valida
transición+origen y `requiere`, actualiza `pedidos.etapa`, apendea `pedido.movido` a
`eventos.jsonl` y emite al bus (tablero al día + píldora de actividad EN el hilo). Nadie
más escribe `etapa`: ni el camino, ni el panel, ni el poller de Supabase. Eventos
canónicos: `pedido.creado · movido · actualizado · cobro_registrado · reabierto ·
movimiento_rechazado`.

### 2.6 `borrador.ts` — la salida tipada de la guía conversacional (nuevo)

```ts
// src/core/schemas/borrador.ts
import { z } from 'zod';

/** TODO cambio propuesto por IA (guía de caminos, config por conversación, editar etapas,
 *  onboarding) es un Borrador: diff visible + pruebas + Publicar/Descartar. Nada vive sin
 *  el click del dueño; publicar = commit en el git del clon; deshacer restaura borrador. */
export const Borrador = z.object({
  id: z.string(),
  tipo: z.enum(['caminos', 'modulos', 'embudo', 'conexion', 'negocio']),
  titulo: z.string(),                          // 'Precios céntricos +10%'
  pedidoPor: z.string(),                       // la frase del dueño que lo originó
  cambios: z.array(z.object({
    objeto: z.string(),                        // 'camino:mensual-centrico' | 'ajuste:embudo'
    antes: z.string().nullable(),              // render humano (el diff rojo/verde del panel)
    despues: z.string(),
  })).min(1),
  pruebas: z.object({                          // candado: rompe una dorada → NO puede publicarse
    corridas: z.number(), pasadas: z.number(),
    choques: z.array(z.string()).default([]),
  }).nullable(),
  encargos: z.array(z.object({                 // lo que NO existe → Claude Code lo fabrica aparte
    que: z.string(),                           //   (data/encargos/ + cola única del maestro);
    estado: z.enum(['pendiente', 'fabricando', 'listo']),  //   el dueño lo activa cuando aparece
  })).default([]),
  estado: z.enum(['borrador', 'publicado', 'descartado']).default('borrador'),
  creadoTs: z.number(),
});
export type Borrador = z.infer<typeof Borrador>;
```

### 2.7 `esquema.sql` día 1 — 6 tablas núcleo + migraciones de módulo

Las 5 tablas del r5 quedan igual salvo dos deltas reconciliados, más la tabla `dudas`:

```sql
-- DELTA 1 (chats a escala): conversaciones gana el bautizo y las etiquetas automáticas
--   titulo   TEXT,                        -- 'Carolina · Melipilla · 5 baños' (modulos/ficha lo
--                                         --   escribe apenas el extractor sabe; nunca manual)
--   etiquetas TEXT NOT NULL DEFAULT '[]', -- JSON: ['grande','nuevo','urgente'] (calculadas)
-- (se suman a: conv_id, contacto_id, canal_id, estado pendiente_bot|abierta|resuelta|dormida,
--  asignado bot|humano, snoozed_until, waiting_since, first_reply_ts,
--  camino_activo, camino_paso, reglas_aplicadas, sesion_llm)

-- DELTA 2 (la 6ª tabla núcleo): las dudas junior→senior sobreviven reinicios
CREATE TABLE dudas (
  id              TEXT PRIMARY KEY,        -- el código de 5 letras del relay
  conversacion_id INTEGER NOT NULL REFERENCES conversaciones(id),
  agente          TEXT NOT NULL,
  fase            TEXT NOT NULL DEFAULT 'pendiente',
  payload         TEXT NOT NULL,           -- la Duda completa (JSON validado por schemas/duda.ts)
  creada_ts       INTEGER NOT NULL,
  resuelta_ts     INTEGER
);

-- MIGRACIONES DE MÓDULO (Modulo.migraciones, las aplica cli/migrar.ts):
-- modulos/embudo/migracion.sql      → tabla pedidos (§2.5, SQL del informe flujos r7)
-- modulos/seguimiento/migracion.sql → tabla seguimientos:
CREATE TABLE seguimientos (
  id              INTEGER PRIMARY KEY,
  conversacion_id INTEGER NOT NULL REFERENCES conversaciones(id),
  enviar_ts       INTEGER NOT NULL,        -- 'viernes 26 · 10:00' resuelto por fechaISO
  texto           TEXT NOT NULL,           -- editable desde la prog-card hasta esa hora
  origen          TEXT NOT NULL,           -- 'camino:<id>' | 'dueno' | 'modulo:seguimiento'
  estado          TEXT NOT NULL DEFAULT 'programado',  -- programado|enviado|cancelado
  ts              INTEGER NOT NULL
);
```

Contratos SIN cambios respecto al r5 (referencia, no se repiten aquí): **Canal** con
`ventana()`, `enviarPlantilla()`, `escribiendo()`, eventos canónicos y factory-null
(`canales/canal.ts`); **MensajeEntrante / MediaEntrante / MediaConBinario /
ResultadoEnvio** (`schemas/mensaje.ts`); **ConsultaLLM / RespuestaLLM / UsoLLM** con la
cadena `sdk→cli→api→plantilla` y `salidaEsquema` (`schemas/llm.ts`). El texto exacto está
en blueprint r5 §4.1-4.2 y se copia tal cual el día 1.

---

## 3. Órganos del bot vivo: qué se trasplanta y qué NO

Bot vivo: `~/SaSS/destaperapido/whatsapp-bot/` (archivos en la raíz, verificados hoy).
Regla del dueño: nace DE CERO — se trasplantan ARCHIVOS ESCOGIDOS, jamás se clona el
repo. Los `.js` conviven con `.ts` por type stripping y se tipan archivo por archivo.

### 3.1 SÍ se trasplantan (código, tal cual o adaptación mínima)

| Órgano vivo | Destino en el núcleo | Cuándo | Por qué se salva |
|---|---|---|---|
| `enviar.js` | `src/canales/wa-baileys/legado/enviar.js` | S5 | candado anti-jid-de-prueba DENTRO del emisor + auto-sanación Bad MAC (borra sesión Signal + reenvía) — probado en producción |
| `outbox.js` | `src/canales/wa-baileys/legado/outbox.js` | S5 | cola de salida persistente; el único camino de lo irreversible |
| `gating.js` | `src/organos/gating.js` | S5 | debounce + timbre + anti-flood; re-dispara al cerebro cuando la ingesta anota |
| `extraer.js` | `src/organos/extraer.js` | S2 | extractor de ficha + `fechaISO()` (el ÚNICO juez de fechas — memoria: no escribir otro regex); alimenta el bautizo de `modulos/ficha` |
| `integracion.js` | `src/organos/integracion.js` | S2 | cotizar/PDF/Supabase/repartidor; TRANSITORIO: en E2 se desarma hacia `modulos/cotizador` (clon) + conexiones `repartidor`/`supabase` fabricadas |
| `link-code.mjs` | `src/cli/vincular.ts` | S5 | pairing por código sin QR (adaptación mjs→ts, no copia ciega) |

### 3.2 Se trasplantan como DATOS (nunca como código)

| Del vivo | Al clon del núcleo | Cuándo |
|---|---|---|
| `precios.js` (tabla de tarifas) | `data/ajustes/precios.json` — tarifario-en-datos; el validador `precioCoherente` se REESCRIBE en `modulos/precios/` | S2 |
| persona/`BOT_PERSONA` (en `config.js`) | `data/persona/base.md` + `fragmentos/` | S2 |
| 68 reglas aprendidas | 20-30 caminos YAML `data/caminos/*.yml` CON `dominio` | S3-4 |
| casos de `_test-precios.mjs`, `_test-calidad.mjs` y correcciones del gimnasio vivo | pruebas doradas `data/pruebas/*.yml` | S3-4 |
| `conversaciones.jsonl` + `envios.jsonl` | `cli/migrar.ts` one-shot → `bot.db`; los JSONL quedan de archivo histórico solo-lectura | S5 |
| dudas pendientes de `dudas.js` | filas de la tabla `dudas` (migradas por `migrar.ts`) | S5 |

### 3.3 NO se trasplantan (y quién los reemplaza)

| Órgano vivo | Por qué NO | Reemplazo en el núcleo |
|---|---|---|
| `brain.js` | se vuelve SHIM de ~20 líneas EN EL VIVO llamando a `llm.ts` (S1); el núcleo nunca hereda su lógica | `core/llm.ts` + `agentes/` |
| `index.js` | boot Frankenstein; el arranque nuevo valida config con Zod | `src/index.ts` |
| `store.js` | JSONL como estado vivo era el problema | `core/db.ts` + `escritor.ts` (SQLite) |
| `portero.js` | embrión CONCEPTUAL de la madre; se reescribe con los 3 casos del prototipo | `agentes/madre.ts` |
| `dudas.js` | embrión conceptual; la Duda nueva es multi-turno con evaluación bidireccional | `motor/duda.ts` + `schemas/duda.ts` |
| `calidad.js`, `aprender.mjs`, `aprender-core.mjs` | el ciclo 👍👎→reglas se rediseña como gimnasio con juez tipado y gate | `gimnasio/` + `modulos/calidad/` |
| `dashboard.mjs` | el panel nuevo nace del design system, no del Frankenstein | `panel/` (Hono + PWA) |
| `recordatorios.js`, `seguimiento.js` | renacen VISIBLES y editables (prog-card), sobre tabla | `modulos/seguimiento/` |
| `entregas.js`, `contacto.js`, `faltantes.js`, `quiet.js` | sus comportamientos renacen como datos: entregas → conexión fabricada + embudo; contacto → tabla `contactos`; faltantes → `AporteCampoFicha.requerido`; quiet → `canales.horario` | módulos + esquema |
| `config.js` | mezcla persona+flags+secretos | `core/config.ts` + `data/ajustes/` + `.env.local` |
| `link-qr.js` | solo pairing por código en el núcleo | `cli/vincular.ts` |
| `bridge/`, tests `_selftest.mjs`/`_smoke-brain.mjs` | la cola del bridge ya está absorbida en `core/cola.ts` (con el fix del leak); los smoke se reescriben en vitest | `core/cola.ts`, tests colocalizados |

---

## 4. Stack decidido → archivo donde se materializa

| Decisión de stack | Se materializa en | Detalle |
|---|---|---|
| **Node 24 LTS + TS 6 estricto NATIVO** (type stripping, sin build) | `tsconfig.json` (`strict`, `module: nodenext`, `erasableSyntaxOnly`, `noEmit`) · `launchd/com.dixdy.dixdybot.plist` apunta DIRECTO a `src/index.ts` · `package.json` (`engines.node >=24.12`) | imports con `.ts` explícito; PROHIBIDO `enum`/decoradores/namespaces; `--env-file` reemplaza dotenv; `--watch` reemplaza nodemon; verificador barato: `tsc --noEmit` (5 s) |
| **SQLite (better-sqlite3 13, WAL, un escritor)** | `core/db.ts` (ÚNICO archivo que lo importa — migrar a `node:sqlite` = editar solo esto) · `core/esquema.sql` (6 tablas) · `core/escritor.ts` (toda escritura, incl. `moverPedido`) · migraciones de módulo (`modulos/*/migracion.sql`) vía `cli/migrar.ts` · respaldo `VACUUM INTO` en launchd | JSONL SOLO ledgers append-only (`core/ledger.ts`: uso-llm, eventos, envios) |
| **Hono 4.12 + @hono/node-server + @hono/zod-validator** | `panel/servidor.ts` (API + estáticos + webhooks, un proceso) · `panel/api/*.ts` (zod-validator en el borde) · `canales/wa-cloud/webhook.ts` · `Modulo.rutasPanel()` monta sub-apps Hono bajo `/api/mod/<id>/` | mismo handler Mac ↔ Cloudflare Worker (meta-buzon) |
| **Zod 4 fuente única** | `core/schemas/*.ts` (TODOS los contratos; `z.infer` = los tipos) · `panel/api/modulos.ts` (`z.toJSONSchema()` → la vista Ajustes se dibuja sola) · `core/llm.ts` (`salidaEsquema` tipa el StructuredOutput del cerebro) · `core/config.ts` (valida `data/ajustes/*.json`) · webhooks Meta | cero interfaces TS paralelas a los schemas |
| **pnpm 11.17 + pins exactos** | `package.json` (`packageManager` pineado; 6 deps runtime: baileys, better-sqlite3, hono, @hono/node-server, @hono/zod-validator, zod) | la sencillez como número auditable |
| **vitest 4.1.10** | tests colocalizados `*.test.ts` · `gimnasio/personas.ts` (6 guiones deterministas contra canal `sim`) — verde desde el primer commit | el juez LLM queda FUERA de vitest: `gimnasio/juez.ts` es script con gate ≥ 4,0 |
| **Groq whisper-large-v3-turbo (fetch nativo)** | `ingesta/procesadores/audio.ts` | único proveedor nuevo; contratarlo = plata → OK de Alejandro vía Guardián |
| **Cadena LLM `sdk→cli→api→plantilla`** | `core/llm.ts` + `core/cola.ts` + `schemas/llm.ts` + ledger `uso-llm.jsonl` | prioridad #1 (S1); métricas midiendo antes del 19-ago |
| **Design system único (r6 + prototipo)** | `panel/pwa/tokens.css` (copiado del `<style>` del prototipo el DÍA 1) + vista `diseno` como guardián | regla: ningún componente nace fuera de esa vista; acento en UNA acción por vista; ≤40 palabras de chrome |

---

## 5. El primer día de código (checklist copiable, S0)

1. `mkdir -p ~/SaSS/DIXDY/dixdybot` y crear el árbol `[D1]` del §1 (carpetas vacías
   incluidas, con un `.gitkeep` o el archivo real).
2. `package.json` + `tsconfig.json` + `config.example.env` + `.gitignore` + `launchd/`
   (§4, columnas 1-2 y 5-6).
3. Copiar los contratos: §2 de este informe (manifest, camino, duda, conexion, pedido,
   borrador) + §4.1-4.2 del blueprint r5 (canal, mensaje, llm) → `src/core/schemas/`.
4. `core/db.ts` + `esquema.sql` (5 tablas r5 + deltas titulo/etiquetas + tabla dudas) +
   `escritor.ts` + `ledger.ts` + `bus.ts` + `config.ts`.
5. `canales/canal.ts` + `factory.ts` + `sim/` (el canal simulado responde eco) +
   `modulos/indice.ts` vacío + `cli/doctor.ts`.
6. `panel/pwa/tokens.css` copiado del `<style>` del prototipo (líneas 1-335).
7. `src/index.ts` que arranca todo lo anterior; `gimnasio/personas.ts` esqueleto con 1
   guion; primer test: sim recibe "hola" → el bus lo enruta → doctor verde.
8. `pnpm install && npx tsc --noEmit && npx vitest run` — TODO verde en el primer commit.
9. Registrar en `actividad.py` (doctrina: deja huella).

Con esto, S1 (llm.ts + shim en el vivo) arranca sobre suelo firme y cada decisión de
producto de las 18 iteraciones del prototipo ya tiene su casa con nombre y apellido.

## Fuentes

- `scratchpad/dixdybot-prototipo.html` (v4, 18 iteraciones — DATA CHATS/CAMINOS/AGENTES,
  `pausaHTML`, `verFichaConfig`, `nuevaConexion`, `conexionChat`, `nuevoNegocio`,
  `verCorreoConfig`, `pop-etapas`, NOTAS)
- `mejoras-destaperapido/investigacion-dixdybot/ronda5/blueprint-fundacional.md` (rector)
- `ronda7-gapcheck/auditoria-modularidad.md` (aportes), `flujos-motor-embudo.md`
  (pedidos/etapas/efectos), `matriz-vision-prototipo.md` (brechas)
- Memorias `project_dixdybot-*` (pausa-junior-senior, flujo-chats-config, ia-madre,
  generico-modular, design-system)
- `~/SaSS/destaperapido/whatsapp-bot/` (listado real de órganos, verificado 24-jul)
