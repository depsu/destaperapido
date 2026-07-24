# Diagnóstico — Capa de conexión WhatsApp (Baileys) del bot de destaperapido.cl

Fecha del diagnóstico: 23-07-2026 (madrugada). Código vivo analizado:
`/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot`.

## 1. Stack y versiones (verificado)

| Componente | Valor | Fuente |
|---|---|---|
| Baileys | **@whiskeysockets/baileys 6.7.23** (spec `^6.7.0`) | `package.json` + `package-lock.json` + `node_modules/@whiskeysockets/baileys/package.json` |
| libsignal | 6.0.0 (fork whiskeysockets, git commit `bcea72d`) | `package-lock.json` |
| Node | v22.18.0 (vía nvm) | plist instalado en `~/Library/LaunchAgents/com.dixdy.whatsapp-bot.plist` |
| Supervisión | launchd `com.dixdy.whatsapp-bot`, `KeepAlive=true`, `caffeinate -is`, stdout→`bot.log`, stderr→`bot.error.log` | `launchd/com.dixdy.whatsapp-bot.plist` |
| Estado actual | Proceso PID 49112 corriendo, uptime ~3h11m al momento del análisis; último exit status `-15` (SIGTERM = reinicio manual/launchd, no crash) | `launchctl list` + `ps` |

Nota: no pude verificar sin internet si existe una versión más nueva de Baileys que 6.7.23
(instalada el 06-jul-2026). Dado que la mayoría de los problemas giran en torno a chats
`@lid` (leads de anuncios) y sesiones Signal, vale la pena revisar el changelog upstream:
el manejo de LID ha sido un frente activo de esa librería.

## 2. Evidencia cuantificada en logs

Los logs fueron rotados el 11-jul (archivo viejo en `backups/`). Timestamps en las líneas
existen SOLO desde ~21-jul 15:56 (los agregó `src/quiet.js` tras el incidente del 21-jul);
todo lo anterior está sin fecha.

### 2.1 Era de la "tormenta" (06-jul → 11-jul, `backups/bot.log.hasta-20260711`, 3.6 MB)

| Patrón | Conteo |
|---|---|
| `Conexión cerrada (408)` | **81.917** |
| `Conexión cerrada (500)` | 75 |
| `Conexión cerrada (428)` | 12 |
| `Conexión cerrada (503)` | 4 |
| `Conexión cerrada (405)` | 3 |
| `Conexión cerrada (515)` | 1 |
| Reinicios de proceso ("Contexto recuperado") | 15 |

En `backups/bot.error.log.hasta-20260711` (**53 MB en ~5 días**):
**65.469 líneas "Bad MAC"**, 2.540 "Failed to decrypt", 6 "timed out".
Es decir: ~16.000 desconexiones/día por 408 (timeout de keep-alive) = el bucle de
reconexión instantánea sin backoff que los comentarios del código describen como
"tormenta de reconexión" (quemaba CPU, filtraba memoria y dejaba al bot ciego a ratos).

### 2.2 Era actual (11-jul → 23-jul, `bot.log` 708 líneas / `bot.error.log` 5.7 MB, 42.433 líneas)

| Patrón | Conteo |
|---|---|
| `Conexión cerrada (408)` | 29 |
| `Conexión cerrada (428)` | 23 |
| `Conexión cerrada (500)` | 20 |
| `Conexión cerrada (503)` | 6 |
| Desconexiones con fecha: 21-jul | 6 |
| Desconexiones con fecha: 22-jul | 7 |
| Reinicios de proceso ("Contexto recuperado") | 42 en ~11 días (solo 3 con fecha: 1 el 21-jul, 2 el 22-jul — dos seguidos a las 21:07 y 21:17) |
| "Bad MAC" total | **6.909** (268 el 21-jul, **2.631 el 22-jul**, 4.010 sin fecha = 11→21 jul) |
| "Failed to decrypt" | 272 |
| Reenvíos del watchdog (`[sanar] reenviado`) | **25** (casi todos a jids `@lid`; repetidos al mismo jid: `209401231233149@lid` ×5, `99991150436465@lid` ×2, `76948684427310@lid` ×2, `100699937476840@lid` ×2) |
| Sanadas del candado de entrada (`[candado]`) | 9 con fecha (21-jul), p.ej. ráfaga de las 15:57:00-15:57:07 contra `40068404228316:17@lid` = **el propio teléfono del bot** |
| `cerrada (440)` / "conflict" / "stream error" / 401 real | **0** en los logs conservados (las "tormentas de 440" que citan los comentarios y MEMORY ocurrieron en sesiones de terminal del 14-15 jul, no quedaron en estos archivos) |

La ráfaga del 22-jul 14:14:24 (cientos de "Bad MAC" en el mismo segundo) es del **candado
con el propio teléfono** (`40068404228316:17@lid` = un device de la misma cuenta): los ecos
de sincronización multi-dispositivo no se pueden descifrar. Junto a eso, decenas de
"Closing open session in favor of incoming prekey bundle" (renegociación de sesión).

### 2.3 Sesiones corruptas (relink completo)

Carpetas preservadas: `auth.dañada-20260706-164334`, `auth.dañada-20260711-1552`,
`auth.dañada-20260714-161759`, `auth.enredada-20260715-003623` (+2 `auth.prev-20260715-*`).
= **4 corrupciones de sesión que exigieron re-vincular en 9 días** (06→15 jul).
**Ninguna desde el 15-jul**: 7+ días con la misma sesión (356 archivos en `auth/`:
155 session, 138 pre-key, 54 sender-key).

## 3. Diagnóstico por síntoma

### Síntoma 1 — "El bot queda ciego" → causa MIXTA, hoy mayormente mitigada

Cuatro mecanismos distintos, todos con evidencia:

1. **Tormenta de reconexión (código propio, ya corregido).** El close handler viejo
   reconectaba al instante en cada 408 → 81.917 cierres en 5 días; durante cada ciclo el
   bot no veía nada. Agravante descubierto y documentado en `src/quiet.js:1-6`: el volcado
   de libsignal a stdout (archivo síncrono bajo launchd) bloqueaba el event loop, se
   perdían los keep-alive y WhatsApp cortaba el stream (los 408 se auto-alimentaban).
   Mitigación actual: guard + backoff exponencial 2s→30s (`src/index.js:156-173` y
   `287-317`), `keepAliveIntervalMs: 20000` (`src/index.js:227`), filtro de ruido +
   timestamps (`src/quiet.js`), cierre del socket viejo con `removeAllListeners()` +
   `sock.end()` (`src/index.js:293-298`, evita el OOM por listeners acumulados). Resultado
   medible: de ~16.000 cierres/día a **6-7/día con recuperación en 2s**.

2. **Bad MAC entrante (protocolo/Baileys+libsignal).** Cuando el candado Signal con un
   contacto se corrompe, el mensaje llega como stub CIPHERTEXT **sin contenido**: el
   teléfono del cliente sí lo muestra, el bot no — ceguera selectiva e invisible.
   6.909 casos desde el 11-jul. Mitigación (agregada 21/22-jul, **aún sin commit**):
   manejo del stub (`src/index.js:457-460` + `92-143`): sana el candado del remitente
   (`sanarSesion`, throttle 1 vez/10min por sesión), registra en el panel la huella
   "🔒 (llegó un mensaje que no se pudo leer)" y, si en 90s WhatsApp no reintenta con
   éxito, le pide al cliente que reenvíe (throttle 30 min). La CAUSA de fondo (por qué se
   corrompen las sesiones, sobre todo `@lid` y el propio multi-device) es de la
   librería/protocolo; el código solo puede remediar.

3. **Mensajes durante una caída (código propio, corregido 21-jul, sin commit).** Baileys
   re-entrega como `messages.upsert type:"append"` lo que llegó con el stream caído; el
   código viejo solo procesaba `notify` → un cliente que escribía durante una caída quedaba
   sin registro ni respuesta (incidente 21-jul). Fix: `src/index.js:380-390` procesa
   `append` (con ventana de frescura ampliada a 600s, `src/index.js:473-478`) + backfill
   de historial `messaging-history.set` acotado a HISTORY_DAYS con piso anti-duplicado
   (`src/index.js:395-418`).

4. **Ceguera residual sin alarma (falta).** Si llega un 401 loggedOut, el proceso queda
   VIVO pero sin socket y "no se reintenta" (`src/index.js:303-306`) — con
   `KeepAlive=true` launchd no lo reinicia porque no murió. Y en ningún punto se avisa a
   Alejandro (no hay integración con `avisos-worker`/`avisar.py` en `src/`: grep sin
   resultados). Hoy la ceguera larga solo se nota cuando un cliente reclama.

### Síntoma 2 — Mensajes duplicados → causa MIXTA (Baileys pone la trampa, el código cayó dos veces)

Dos fenómenos distintos que el dueño percibe igual:

1. **Duplicado REAL al cliente = watchdog de sanación reenviando algo que sí llegó.**
   Cadena causal: en chats `@lid` (la mayoría de los leads de anuncios) el acuse ✓✓
   muchas veces NO llega por `messages.update` sino por `message-receipt.update`, y tras
   una reconexión los acuses llegan atrasados en lote. El watchdog (`revisarPendientes`,
   `src/enviar.js:138-167`) interpretaba "sin ✓✓ en 30s" como candado corrupto y reenviaba
   → duplicado (caso Germán, 16-jul, citado en `src/index.js:350-353` y `src/enviar.js:17-20`).
   Mitigaciones ya puestas: HEAL_MS 30s→**180s** (`src/enviar.js:21`), `MAX_HEAL=1`
   (`:22`), escuchar `message-receipt.update` (`src/index.js:354-370`), reset del reloj de
   pendientes al recuperar la conexión (`src/enviar.js:57-61`), y el criterio
   `vistoActivoDesde` por presencia: sin señales de vida no reenvía hasta un tope de 30 min
   (`src/enviar.js:27-43,147`). **Riesgo residual por diseño**: "un duplicado raro es
   mejor que un mensaje perdido". Los 25 reenvíos desde el 11-jul —con hasta 5 al mismo
   `@lid` (cada globo del turno es un pendiente aparte)— son cada uno un duplicado
   potencial si el original sí había llegado. Para `@lid` la presencia suele no estar
   disponible → el criterio degrada al reenvío de respaldo a los 30 min.

2. **Duplicado SOLO en el panel (un solo envío real) = eco "append" (incidente 22-jul).**
   Baileys emite el eco de cada envío PROPIO como `messages.upsert type:"append"` con
   `fromMe`. Al abrir el procesamiento de `append` (fix del síntoma 1.3), esos ecos
   entraron como mensajes nuevos: burbuja doble en el panel. Fix (sin commit):
   `src/index.js:383` — `if (type === "append" && msg?.key?.fromMe) continue`.
   Refuerzos anti-duplicado que ya existían: dedup por id `seenMsgIds` con evicción 8000→2000
   (`src/index.js:440-449`), y en `src/outbox.js`: guard de re-entrada `drenando` (:42,58-59),
   reconciliación por id que evita el item doble (:46-55), sacada del item apenas enviado
   (no al final del lote, :94-97) y `item.pdf=null` persistido apenas sale el PDF para que
   un fallo del texto no re-mande la cotización (:82-87). Todos esos comentarios describen
   duplicados que YA ocurrieron y se taparon uno a uno.

3. **Hueco vigente (menor):** `seenMsgIds` vive solo en RAM. Tras un reinicio del proceso,
   un mensaje de cliente re-entregado dentro de la ventana de 600s puede ser respondido de
   nuevo (el hidratado del historial le da contexto al cerebro, pero no impide el segundo
   turno). No encontré evidencia en logs de que haya ocurrido, pero la ventana existe.

### Síntoma 3 — "El bot se pausa solo" → causa PRINCIPAL en código propio (gatillada por un comportamiento de Baileys), más pausas por diseño que parecen fallo

1. **El bug de verdad (incidente 22-jul, fix sin commit):** los ecos `append fromMe` del
   punto anterior entraban a `onOwnerMessage` (`src/gating.js:81-104`) → cada respuesta del
   bot contaba como "el dueño contestó" (`ownerReplied=true`) y, con
   `OWNER_MANUAL_STICK_AFTER=3` (default, `src/config.js:98`), al tercer mensaje el chat
   pasaba a **owner-takeover = pausa INDEFINIDA** que solo se suelta desde el panel. O sea:
   el bot se pausaba solo, chat tras chat, sin que nadie lo tocara. El mismo fix del eco
   (`src/index.js:383`) mata este síntoma.
2. **Pausas por diseño que el dueño percibe como "se pausó solo":**
   - Toque del dueño desde su teléfono → pausa 30 min (`OWNER_MANUAL_TTL_MS=1800000`, .env).
   - Portero detecta "soporte de cliente antiguo" por regex → pausa manual del chat
     (`src/portero.js:33` + `src/index.js:519-523`).
   - Tope de 12 respuestas por chat (`MAX_BOT_REPLIES_PER_CHAT=12`) y topes globales
     anti-baneo (40/hora, 200/día, `src/config.js:89-90`, `src/gating.js:45-58`) → el bot
     calla y parece pausado.
   - Fuera de `withinBusinessHours()` → silencio.
   Ninguna de estas se muestra con su MOTIVO de forma prominente al dueño → opacidad, no bug.
3. **Pausa fantasma histórica:** antes del catch en `src/gating.js:179-183`, un
   `sendMessage` con el socket caído era un unhandledRejection que **mataba el proceso
   entero** (comentario en el propio código) — el bot "se pausaba" hasta que launchd lo
   levantaba. Ya corregido.

## 4. Mitigaciones existentes (resumen) vs. lo que falta

Ya existe (con archivo:línea):
- Backoff exponencial + guard de reconexión única (`src/index.js:156-173, 307-316`).
- Silenciador/timestamps de logs para no bloquear el event loop (`src/quiet.js`).
- Cierre limpio del socket viejo anti-OOM (`src/index.js:293-298`).
- Auto-sanación de candado saliente + reenvío único con watchdog conservador
  (`src/enviar.js:111-167`), reloj reseteado al reconectar (`:57-61`), criterio de
  presencia (`:32-43`).
- Auto-sanación de candado ENTRANTE + pedir reenvío al cliente (`src/index.js:92-143,457-460`).
- Doble canal de acuses ✓✓ (`messages.update` + `message-receipt.update`, `src/index.js:336-370`).
- Dedup por id de mensaje + backfill con piso (`src/index.js:440-449, 395-418`).
- Outbox con re-entrada bloqueada, reconciliación por id, lote de 3, PDF no repetible
  (`src/outbox.js`).
- Sync de historial pesado SOLO en vinculación fresca (`syncFullHistory: freshLink`,
  `src/index.js:213,232`) — la causa declarada de las tormentas de 440 post-relink.
- Vinculador limpio aparte (`src/link-code.mjs`) que no arrastra la reconexión agresiva.
- Captura del unhandledRejection que mataba el proceso (`src/gating.js:179-183`).

Lo que FALTA (brechas concretas):
1. **Sin alarma de ceguera:** nada avisa a Alejandro si la conexión queda caída >N minutos
   o si llega un 401 (el proceso queda vivo y mudo). El `avisos-worker` de DIXDY existe y
   no está conectado aquí. Es la brecha nº1: todos los incidentes se descubrieron tarde.
2. **Fixes críticos sin commit:** el manejo de `append`/eco/stub-CIPHERTEXT y los
   timestamps de quiet.js están solo en el working tree (`git status`: `M src/index.js`,
   `M src/quiet.js`; último commit del repo 20-jul). Un checkout o un clon desde el
   maestro los perdería. Tampoco están promovidos al template del maestro
   (`DIXDY/whatsapp-bot/`), que la doctrina exige.
3. **Dedup no persistente:** `seenMsgIds` y la vigilancia `pendientes` viven en RAM;
   reinicio = ventana de re-respuesta (600s) y mensajes en vuelo huérfanos.
4. **Sin rotación de logs:** `bot.error.log` creció a 53 MB en 5 días en la era mala y ya
   va en 5,7 MB; las trazas "Bad MAC" (stack de 6 líneas cada una, 2.631 el 22-jul) salen
   por stderr SÍNCRONO sin filtro (quiet.js no toca console.error) — el mismo mecanismo
   que alimentó los 408.
5. **Bad MAC sigue alto y creciendo** (268 → 2.631 entre 21 y 22-jul): la sanación actual
   remedia por contacto con throttle, pero no hay métrica/alerta de tendencia ni evaluación
   de upgrade de Baileys (6.7.23) / del fork libsignal, que es donde vive la causa raíz.
6. **@lid sin presencia:** el criterio anti-duplicado del watchdog depende de señales de
   presencia que los `@lid` rara vez dan → en el peor caso sigue habiendo un reenvío ciego
   a los 30 min. Una mejora barata: consultar el estado del mensaje vía la propia app
   (receipt histórico) antes del reenvío de respaldo, o marcar esos reenvíos con texto
   idéntico para que WhatsApp los colapse.

## 5. Veredicto

| Síntoma | Causa raíz | Estado |
|---|---|---|
| Queda ciego | MIXTA: bucle de reconexión propio (corregido) + Bad MAC de protocolo/Baileys (remediado, no curado) + `append` ignorado (corregido, sin commit) | Mitigado en ~95%; falta alarma de ceguera |
| Duplicados | MIXTA: acuses `@lid` por doble canal y atrasados (Baileys/protocolo) × watchdog impaciente propio (ya conservador) + eco `append` en el panel (corregido, sin commit) | Mitigado; riesgo residual asumido por diseño |
| Se pausa solo | CÓDIGO PROPIO (eco `append` → falso "dueño contestó" → takeover indefinido; corregido, sin commit) + pausas por diseño sin explicar al dueño | Corregido; falta transparencia de motivos |

La capa de conexión HOY está órdenes de magnitud más estable que hace dos semanas
(de ~16.000 cierres/día a 6-7/día; 0 relinks desde el 15-jul), pero se sostiene sobre
parches sin commitear, sin alertas y sobre una librería no oficial cuya fragilidad de
sesiones Signal (`@lid`, multi-device) es la fuente común de los tres síntomas. Para el
rediseño "dixdybot", la capa de conexión merece: (a) commitear y promover estos fixes,
(b) un vigía de salud con timbre (conexión caída, racha de Bad MAC, 401), (c) dedup y
vigilancia persistentes en disco, (d) evaluación de upgrade de Baileys, y (e) exponer al
dueño el MOTIVO de cada silencio/pausa en el panel.
