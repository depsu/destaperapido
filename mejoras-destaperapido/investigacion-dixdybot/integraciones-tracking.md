# Auditoría: integraciones y tracking inicio→fin del whatsapp-bot (destaperapido)

Fecha: 2026-07-23. Código auditado: `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot`
(instancia viva) contrastado con el template maestro `/Users/alejandroriveracarrasco/SaSS/DIXDY/whatsapp-bot`
y el método documentado en `/Users/alejandroriveracarrasco/SaSS/DIXDY/docs/24-whatsapp-bot-autoresponder.md`.

Estado operativo verificado en el `.env` vivo: `INTEGRACION_ON=true`, `INTEGRACION_MODE=live`,
`ULTIMO_CLICK=todo`, `BRAIN_MODE=cli`, `CLAUDE_MODEL=opus`, `HISTORY_LIMIT=60`. Es decir: el
pipeline completo está EN PRODUCCIÓN, con supervisión "último click" para cotización y entrega.

---

## (a) Pipeline real de punta a punta

### 1. Chat (entrada)

- `src/index.js:440-497` — llega el mensaje por Baileys: dedup por id de WhatsApp (Set con evicción a
  2000), guardia de frescura (`messageTimestamp` ≤120s, 600s tras reconexión offline; los viejos solo se
  persisten, no se responden), captura de `senderPn` (número real aunque el chat sea `@lid`, línea 451)
  y `pushName`. Todo mensaje se persiste vía `gating.js` → `store.js:persistMessage` en
  `data/conversaciones.jsonl` con contrato `{id, ts ISO, jid, name, from: client|bot|owner, text, phone?}`.
- `src/index.js:499-510` — al disparar la respuesta, **la integración corre DESACOPLADA del reply**:
  `procesarIntegracion(sock, jid, history, nombre, telefono)` se lanza en paralelo (aunque el bot calle,
  esté en manual o fuera de horario). Este desacople es deliberado y es de lo mejor del diseño.
- Contextos inyectados al cerebro antes de responder (`index.js:552-567`): `contextoEntrega`
  (entregas.js — "este cliente ya cerró, no lo re-cotices"), `contextoTarifario` (precios.js),
  `contextoFaltantes` (faltantes.js — qué dato pedir y cuáles NO repreguntar), `contextoDudas`
  (decisiones ya tomadas por Alejandro).

### 2. Extracción de intención + datos

- `src/extraer.js:14-17` — gating barato `valeAnalizar`: solo analiza si en los últimos 4 mensajes del
  cliente hay un email (regex) o palabra de cierre (`agend|confirm|lo tomo|dale|listo|...`). Evita gastar
  una llamada LLM por turno.
- `src/extraer.js:33-83` — `SCHEMA_PROMPT`: extractor JSON estricto vía `claude -p` (mismo cerebro cli,
  timeout duro de 90s con SIGKILL, línea 100-104). Devuelve `{quiere_cotizacion, confirmo, datos{nombre,
  comuna, cantidad_banos, tipo_uso, duracion, precio_clp (neto por unidad), precio_modo, flete_clp,
  extras[], email, telefono_contacto, direccion, requiere_factura, factura{}, fecha, fecha_fin}}` con
  reglas de negocio destiladas (el Dueño manda ante contradicción, anti precio-ancla, IVA÷1,19,
  separar extras del precio del baño, fecha SOLO de entrega y en ISO). Ventana propia
  `EXTRACT_HISTORY_LIMIT=200` (config.js:137), separada de la del bot (60).
- `src/extraer.js:21-23` — anti-inyección: neutraliza "Dueño:" escrito por un cliente en el texto.
- `src/integracion.js:694-741` — `procesarIntegracion`: guard síncrono `enVuelo` (evita doble análisis),
  respeta `isManual`, dedup persistente `yaCotizado(45 días)`/`yaDespachado(∞)` leyendo `envios.jsonl`
  (líneas 33-49), merge de la **ficha manual del panel** sobre lo extraído (líneas 718-723), normaliza
  la fecha con `fechaISO()` (único juez de fechas en español natural, líneas 105-163) y refresca la
  ficha del lead (`saveDatos`) en cada análisis.

### 3. Cotización (PDF + correo + WhatsApp)

- `src/integracion.js:744-845` — si `quiere_cotizacion`:
  - faltan datos (`datosCompletosCotizar` = email + precio + comuna, línea 236) → NO se cuelga: `faltantes.js`
    hace que el bot pida el dato él mismo (rescate determinista por regex de email/comuna en el historial
    para no repreguntar, faltantes.js:26-37).
  - precio no calza (`precioCoherente`, líneas 277-294: tarifario oficial de la comuna ± IVA + precios
    dichos por el DUEÑO en el chat ± IVA) → **duda** con opciones ejecutables (`addDuda` con
    `accion:{endpoint:"/api/cotizar", body}`) + push a Alejandro (`avisar.py`). Si ya respondió antes,
    `respuestaPrevia` aplica su decisión sola (líneas 761-772).
  - todo calza pero `ULTIMO_CLICK=todo` → duda "¿la mando?" esperando el click (líneas 813-835).
  - `doCotizacion` (líneas 570-636): arma config JSON (`construirConfigCotizacion`, líneas 321-403; regla
    grabada en piedra: **la cotización SIEMPRE es mensual, nunca multiplicar por meses**, líneas 310-320;
    IVA por defecto, neto solo explícito) → `generar_cotizacion.py` (reportlab, PDF) →
    `enviar_cotizacion.py` (Resend con fallback SMTP) → **`logEnvio` APENAS sale el correo, antes del
    WhatsApp** (líneas 604-610: si se registrara al final, una caída repetiría el correo) → PDF por
    WhatsApp con sesión "en caliente" (`resolverJid`+`enviarSeguro`). Fallos parciales avisados por push.

### 4. Confirmación → entrega

- `src/integracion.js:846-907` — si `confirmo`:
  - `datosCompletosEntrega` (línea 295) = precio + dirección exacta (>5 chars) + `fechaISO(fecha)`.
  - `ULTIMO_CLICK=off` → despacha solo (`doEntrega`); si no → duda "¿Despacho?" con acción
    `/api/entregar`; si falta un dato → duda "entrega-falta" con opción "pregúntaselo tú al cliente".
- `construirEntrega` (líneas 406-502) — contrato del objeto entrega:
  `{id: "YYYY-MM-DD-kebab(cliente)-suf4tel", cliente, telefono, fecha, hora?, servicio, cantidad,
  direccion (sin el link de Maps pegado), comuna, maps_url?, telefono_respaldo?, contacto_respaldo?,
  pago:{monto (total CON IVA por defecto = precio×baños + extras + flete), desglose, nota}, notas,
  periodo? ("2 días"), retiro?:{fecha,nota}, estado:"pendiente", factura?}`. `entrega_id` fuerza reusar
  el id (actualización sin duplicar en Supabase, línea 481-483). `maps_url` viaja de punta a punta
  (linkMapsDe, líneas 226-234: el ÚLTIMO link del cliente manda).

### 5. Supabase + repartidor

- `prepararEntrega` (integracion.js:641-660) — **construye pero NO envía**: llama a
  `bridge/entrega_bridge.py` (JSON por stdin) y devuelve `{entrega, resumen, repTel, subida, dry}`.
  Reutilizable por el flujo automático Y el panel (la costura correcta para multi-canal).
- `bridge/entrega_bridge.py` — reusa los scripts del ecosistema del repartidor SIN reinventar:
  `resumen_repartidor.construir_resumen()` (texto del aviso) + `sync_entregas_supabase.upsert_entrega()`
  (upsert idempotente por `id`). Si Supabase falla, **el aviso al repartidor sale igual** con
  `subida=false` (líneas 40-48). OJO: la ruta a los scripts está HARDCODEADA
  (`/Users/.../cotizaciones-destape-rapido/resumen-repartidor/scripts`, líneas 16-18).
- Contrato Supabase (sync_entregas_supabase.py): tabla `entrega` = `{id, fecha, informado_at, data (jsonb
  = la entrega completa), card_html (horneado en Python con gl.tarjeta(e) — nunca portado a JS), eliminado}`;
  tabla `entrega_estado` = `{id, estado, fecha (reagenda), eliminado}` — la escribe el panel del repartidor.
- `doEntrega` (integracion.js:662-690) — envía el resumen al repartidor por el PROPIO Baileys del bot
  (`REPARTIDOR_NUMERO` del .env MANDA sobre el de entregas.json, línea 658), `logEnvio` tipo "entrega",
  `setEtapa("concreto")` sin pisar etapa manual, push a Alejandro "el bot despachó solo".

### 6. Vuelta del estado (repartidor → chat)

- `dashboard.mjs:959-1001` — `/api/entregas` lee EN VIVO de Supabase (`entrega` + `entrega_estado`,
  fetch con timeout de 4s, caché 20s, fallback al snapshot local `entregas.json`); `normEntrega` unifica
  la forma venga de donde venga y normaliza estados (pagado/cancelado → "cobrado").
- `data/enlaces.json` — enlace chat↔entrega: `{links:{jid: entregaId}, rechazos:{jid:[ids]}}`
  (dashboard.mjs:60-76). Auto-enlace al despachar desde el panel (línea 1388) y para actualizaciones
  reusa el `entrega_id` enlazado (línea 1343-1344). Las columnas 3/4 del Kanban (Por entregar/Cobrado)
  salen de este cruce.
- `src/entregas.js` — cierra el círculo hacia el CEREBRO: cruza el teléfono del que escribe (últimos 9
  dígitos) contra `entregas.json` y le inyecta al prompt "NO es un lead nuevo, ya tiene entrega
  agendada/entregada/cobrada — coordina, no re-cotices". Solo lectura, nunca rompe la respuesta.

### 7. Cobro

- El cobro NO tiene evento propio en el bot: vive como estado `cobrado` en `entrega_estado` (lo marca el
  repartidor en su panel) y el bot/panel solo lo REFLEJAN (Kanban col. 4, frase de contexto en
  entregas.js:38-39). No hay conciliación de pago real (monto cobrado vs pactado) en ningún archivo.

### 8. Flujos satélite del tracking

- `src/seguimiento.js` — seguimiento ÚNICO de leads tibios: silencio 3-24h, hubo precio, ventana 9-21h,
  máx 2/ronda, respeta "yo le aviso" (RE_ME_AVISA), `[[SILENCIO]]` del cerebro, un solo intento por chat
  para siempre (`seguimientos.json`). **Envía DIRECTO con `enviarSeguro`, no por el outbox** (línea 130)
  — segunda vía de envío paralela.
- `src/recordatorios.js` — "dormidos 💤" agendados desde el panel (`recordatorios.json`, compartido por
  disco entre procesos): auto-cancela si el cliente escribió / archivado / perdido / ya despachado
  (líneas 119-122), ventana 9-21h, goteo 2/ronda, sale por el **outbox** con la burbuja del mismo id.
- `src/outbox.js` — bandeja de salida entre procesos (`outbox.json`): `encolar({to, text?, pdf?, id?})`
  desde panel/recordatorios/cotización; el bot la drena cada 6s con conexión viva, máx 3 por tick,
  reintentos (5), espaciado humano, e idempotencia fina del PDF (`item.pdf=null` persistido apenas sale,
  líneas 83-87, para que un reintento no duplique el adjunto).
- `/api/confirmacion` (dashboard.mjs:1484-1532) — confirmación llegada por CORREO: re-analiza con IA el
  chat + los correos del lead (worker agente-correos), corre `checklistEntrega` (línea 857-871: dirección,
  comuna, precio, fecha, teléfono ≥8 dígitos, RUT si factura), registra `logEnvio` tipo "confirmacion" y
  deja burbuja en el chat para que el bot también lo sepa.
- Pedidos recurrentes (dashboard.mjs:78-119): un chat = una persona con VARIAS ventas; tarjetas `jid#2`,
  `jid#3` con corte temporal `desde` — la ficha del pedido nuevo no hereda dirección/precio del anterior.

### Libro mayor del tracking: `data/envios.jsonl`

Contrato: `{id, ts, jid, tipo: cotizacion|entrega|seguimiento|recordatorio|confirmacion, detalle{...}}`.
Append-only, compartido por disco entre bot y panel. Hoy: 30 registros = 18 cotizacion, 7 entrega,
4 seguimiento, 1 confirmacion. Es a la vez el **anti-duplicados** (`yaCotizado`/`yaDespachado`) y la
traza auditable (el `detalle` de una entrega guarda el resumen completo enviado al repartidor,
`manual:true/auto:true`, `actualizacion`, `clienteAvisado`). Ejemplo real del bug que motivó el diseño:
cotización de $1 del 20-jul (truco del panel) quedó registrada (`"precio":1`).

---

## (b) Integraciones existentes y su acople al canal WhatsApp

| Integración | Cómo | Dónde | Acople a WhatsApp |
|---|---|---|---|
| PDF cotización | spawn `generar_cotizacion.py <cfg.json> <pdf>` (reportlab) | integracion.js:578-583, dashboard.mjs:1218 | **Cero** — JSON puro |
| Correo salida | spawn `enviar_cotizacion.py` (Resend, fallback SMTP) | integracion.js:593-599 | **Cero** |
| Correo entrada | fetch al correo-worker (Cloudflare D1) con `x-panel-pass`; config en `cotizaciones-destape-rapido/config/agente.local.json` | dashboard.mjs:816-853, 1455-1544 | **Cero** (clave de cruce = email del lead) |
| Supabase entregas | `entrega_bridge.py` → `upsert_entrega` (REST + anon key); lectura viva `/api/entregas` | bridge/, dashboard.mjs:959-1001 | **Cero** |
| Repartidor | resumen de texto por el WhatsApp del bot | integracion.js:680-681, /api/entregar vía outbox | **Alto** (es un mensaje WhatsApp, pero el texto lo arma Python) |
| Extractor IA | `claude -p` texto→JSON | extraer.js | **Cero** (recibe `history` genérico) |
| Avisos push | spawn `DIXDY/scripts/avisar.py` | integracion.js:52-62 | Cero |
| Tarifario | `precios.js` (tabla en código) | precios.js | Cero |

### Qué se rompería al agregar Instagram

1. **El `jid` de WhatsApp es LA clave primaria de todo el tracking**: conversaciones.jsonl, envios.jsonl,
   enlaces.json, datos-lead.json, dudas.jsonl, control.json, etapas.json, pedidos.json, seguimientos.json.
   No hay un id de conversación neutro de canal. Un DM de Instagram no tiene jid → o se inventa un id
   compatible o se abstrae la clave (lo segundo es lo correcto en dixdybot).
2. **Supuestos de formato de jid regados**: `jid.endsWith("@s.whatsapp.net")` y `jid.split("@")[0]` usados
   como TELÉFONO en integracion.js:425 y dashboard.mjs:1335; sufijo `@lid`, `@entrenamiento`. Instagram no
   tiene teléfono, y **el teléfono es la clave de cruce chat↔entrega** (entregas.js:16-19, tel9 en
   dashboard.mjs:921): ese cruce quedaría ciego y todo dependería de `enlaces.json` (que por suerte ya
   existe justo para chats sin número visible).
3. **`index.js` (650 líneas) es un monolito Baileys**: conexión, dedup, frescura, presencia, typing,
   leído, Bad MAC/auto-sanación. Nada reusable directo para otro canal.
4. **`enviar.js`/`resolverJid` (sanación de sesión Signal) y el gating anti-ban** son 100% WhatsApp.
5. **`doCotizacion` y `doEntrega` reciben `sock`** (el socket Baileys) y envían directo
   (integracion.js:613-623, 680-681). En cambio `prepararEntrega` NO envía — y el panel demuestra el
   patrón correcto: prepara y **encola en el outbox**. El outbox (`encolar({to,...})`) ya es la
   abstracción de canal embrionaria: solo `drenarOutbox` conoce Baileys. Generalizar "un outbox por
   canal" es el camino natural.
6. **`contacto.js` depende del pushName** de WhatsApp (Instagram tiene username, no nombre real).
7. Lo que NO se rompe (portable tal cual): extractor, faltantes, precios/tarifario, fechaISO,
   construirConfigCotizacion/construirEntrega, bridge+Supabase, dudas, store (salvo la clave), calidad.

---

## (c) Divergencias template maestro vs instancia viva

Medido con `diff` archivo a archivo (2026-07-23):

- **Volumen**: maestro `src/` = 12 archivos, ~1.912 líneas (1.553 .js + 359 .mjs). Vivo = 24 archivos,
  ~7.119 líneas (4.942 .js + 2.177 .mjs). **~73% del código vivo no existe en el maestro.**
- **Módulos completos AUSENTES en el maestro** (todo el sistema de integración/tracking de esta
  auditoría): `integracion.js` (911), `extraer.js` (130), `entregas.js` (65), `recordatorios.js` (151),
  `seguimiento.js` (141), `outbox.js` (115), `enviar.js` (167), `precios.js` (492), `calidad.js` (344),
  `faltantes.js` (134), `quiet.js` (28), `link-code.mjs` (127). Tampoco existe `bridge/`.
- **dashboard.mjs**: maestro 214 líneas vs vivo 1.897 (Kanban 4 columnas, entregas Supabase, dudas,
  pedidos, gimnasio, correos en el chat, recordatorios, avatares, blindaje CSRF/Tailscale).
- **Divergencia en archivos compartidos**: `index.js` 553 líneas de diff, `store.js` 328, `gating.js`
  124, `brain.js` 96, `config.js` 81, `dudas.js` 56. Idénticos: `contacto.js`, `portero.js`, `link-qr.js`.
- **docs/24 (275 líneas) documenta solo hasta la "segunda iteración" (§7)**: conexión, toques humanos,
  método de la persona, gating, dashboard + loop de aprendizaje, portero, CRM heurístico. **NO documenta
  nada** del pipeline auditado aquí: ni extractor, ni cotización/entrega automática, ni Supabase, ni
  dudas/último click, ni outbox, ni seguimientos/recordatorios, ni pedidos, ni calidad/juez, ni gimnasio.
  Peor: §5 dice que el "siguiente paso natural" sería una skill `preparar-cotizacion` — eso ya se
  construyó (mucho más completo) dentro del bot y el doc quedó atrás.
- Config del vivo vs doc: doc §4.4 dice `MAX_BOT_REPLIES_PER_CHAT=12` ✓ pero el `HISTORY_LIMIT` vivo es
  60 (memoria del proyecto) y el `CLAUDE_MODEL` vivo es **opus** (config.js:124 declara default sonnet
  "porque fable es el más caro" — el vivo lo subió a opus por .env).
- Conclusión doctrina DIXDY: la regla "promueve al maestro toda mejora reutilizable" está incumplida a
  escala de sistema completo. El rediseño dixdybot es la oportunidad de saldar esa deuda de una vez en
  vez de retro-portar 5.000 líneas.

---

## (d) La joya a conservar en el rediseño (dixdybot)

En orden de valor:

1. **`envios.jsonl` como libro mayor append-only anti-duplicados** (store.js:394-414 +
   integracion.js:33-49): `yaCotizado(45d)` / `yaDespachado(∞)` leídos DE DISCO entre procesos, y el
   registro se escribe **apenas sale lo irreversible** (correo → log → WhatsApp, integracion.js:604-610).
   Es el contrato que evitó los re-envíos (caso brisa 17-jul) y sobrevive reinicios. En dixdybot debería
   ser el event-log central, con canal como campo.
2. **El sistema de dudas** (dudas.js + integracion.js:773-905 + panel): el bot NO se cuelga ni actúa a
   ciegas — pausa ESA decisión, pregunta con opciones ejecutables (`accion:{endpoint, body}` con el valor
   elegido), dedup en disco con clave estable, y `respuestaPrevia` aplica la decisión aprendida sin
   volver a molestar. **Es exactamente el embrión de los "caminos" que Alejandro quiere**: falta un
   camino → pausa → pregunta al humano → aprende → sigue solo. Conservar y generalizar.
3. **El dial de autonomía `ULTIMO_CLICK`** (config.js:157-174): todo/entrega/off, validado contra typos,
   y con el texto del cerebro ajustado al modo real (faltantes.js:102-116: "NUNCA digas que ya la
   enviaste" cuando espera aprobación). Autonomía graduable sin tocar código.
4. **La costura preparar/enviar** (`prepararEntrega` construye y sube, el llamador envía por SU canal —
   integracion.js:638-660) + **el outbox** (outbox.js: cola por disco, reintentos, idempotencia del PDF,
   goteo anti-ráfaga, tope global). Juntos son la arquitectura multi-canal ya insinuada: motor puro +
   un drenador por canal.
5. **`fechaISO`/`fechaFinISO` como único juez de fechas** (integracion.js:105-201): español natural
   completo (rangos, días de semana, "mañana", año probable, retiro deducido de la duración). Regla de
   memoria del proyecto: no escribir otro regex de fechas jamás.
6. **`precioCoherente` + tarifario en código** (integracion.js:246-294, precios.js): nada sale sin
   calzar con el tarifario oficial o con un precio dicho por el DUEÑO (±IVA), y la duda propone el
   oficial más cercano de un click. Es el guardián de plata del bot.
7. **El círculo cerrado con el repartidor** (bridge idempotente por `entrega_id` + `card_html` horneado
   en Python + `entrega_estado` de vuelta + `entregas.js` inyectando "ya cerró, no re-cotices" al
   cerebro). Pocas integraciones de este tamaño cierran el loop de vuelta al prompt.
8. **Ficha del lead con precedencia manual > IA** (store.js:322-392 `conManual`/`setCampoManual`;
   merge al flujo automático en integracion.js:718-723): lo que Alejandro fija a mano sobrevive a
   cualquier re-análisis y el motor automático lo VE.
9. **Enlaces chat↔entrega + pedidos `jid#2`** (dashboard.mjs:60-119): modela bien que una conversación
   es una persona con N ventas — y es además la salida al problema "Instagram no tiene teléfono".
10. **Desacople integración/respuesta + guardias de carrera** (index.js:505-510, `enVuelo`, `getGen`,
    frescura anti-reconexión): la venta se procesa aunque el bot calle, sin dobles disparos.

### Riesgos/deudas a NO arrastrar al rediseño

- Ruta absoluta hardcodeada en `entrega_bridge.py:16-18` y config del correo leída de
  `cotizacionesDir/config/agente.local.json` (acople por rutas entre repos).
- Dos vías de envío (seguimiento.js manda directo; el resto por outbox) — unificar en el outbox.
- Doble contabilidad de estado (Map `estado` en RAM + envios.jsonl) — dejar solo el disco.
- El cobro no tiene evento propio (solo estado en Supabase): dixdybot debería registrar el cierre
  económico (monto real cobrado) para cerrar el embudo de verdad.
- El extractor re-analiza hasta 200 mensajes con `claude -p` en cada mensaje que pasa el gating: caro y
  lento (90s de timeout); en dixdybot conviene extracción incremental o cacheada por msgCount.
- docs/24 desactualizado y maestro sin ninguno de estos módulos (ver sección c).
