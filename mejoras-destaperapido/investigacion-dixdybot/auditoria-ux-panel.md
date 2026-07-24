# Auditoría de UX del panel actual del whatsapp-bot (destaperapido)

Fecha: 2026-07-23 · Código auditado:
- `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/src/dashboard.mjs` (1.897 líneas, servidor node:http en :8789)
- `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/web/dashboard.html` (2.673 líneas, ~187 KB, todo inline: CSS+HTML+JS)
- `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/web/entrenar.html` (475 líneas, gimnasio)
- `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/web/aviso.mp3` (sonido de aviso)
- Apoyo: `src/config.js`, `src/precios.js`, `.env`, `data/` (para el mapa de configuración)

Acceso: solo localhost + Tailscale (filtro de IP/Host/Origin en dashboard.mjs:1003-1027). El chat, el Kanban y el gimnasio se refrescan por polling (4s chats/Kanban, 9s estado+dudas; dashboard.html:2662-2670).

---

## (a) Inventario completo de vistas, secciones y acciones

### A. Página principal `/` (dashboard.html) — SPA con 3 vistas + 2 modales

#### A.1 Barra superior (appbar, dashboard.html:486-515) — visible siempre
| Elemento | Qué hace | Dónde vive |
|---|---|---|
| Logo + nombre negocio | Muestra `config.businessName` ("Panel de la IA" hasta cargar) | html:487-491 |
| Semáforo de estado | Bot activo / reconectando / caído / panel sin conexión; sub "Responde solo ✅ / detenido" + contador de reenvíos de auto-sanación. Consulta `/api/estado` cada 9s. Si el bot cae, banner rojo con instrucción de abrir Claude en Terminal | html:492-496, 880-900; backend `botEstado()` mjs:714-747 |
| 🔔 Avisos / 🔊 / 🎵 | Activar sonido+notificación de escritorio al escribir un cliente; probar sonido; subir un .mp3 propio (se guarda en localStorage por dispositivo; el 🎵 se oculta en móvil) | html:497-501, 632-684 |
| ❓ Dudas del bot (+badge rojo) | Abre el modal-buzón de dudas | html:502-505, 2359-2555 |
| Pestañas: 💬 Chats · 🗂️ Kanban · ✨ Aprendió | Cambian de vista (SPA) | html:506-509, showTab() 837 |
| 🏋️ Entrenar | **Link** (no tab) a `/entrenar` — página aparte | html:512 |
| 🚚 Repartidor ↗ | Link externo al panel del repartidor (GitHub Pages `depsu.github.io/cotizaciones-destape-rapido/...`) | html:513 |

#### A.2 Vista 💬 Chats (html:519-548)
**Lista lateral:**
- Buscador de chats (`#q`).
- Toggles: **📅 Solo hoy** (filtra actividad de hoy; persiste en localStorage `chatsSoloHoy2`, apagado por defecto), **⏰ Para seguir** (reordena por días esperando), **📥 Archivados** (bandeja exclusiva estilo WhatsApp). html:522-527, 847-878.
- Barra KPI: "N esperan tu respuesta · N te contestaron · $X en juego" (suma de cotizaciones abiertas). html:938-941.
- Ítem de chat: avatar DiceBear con anillo de estado + emoji de "emoción" (heurística del último texto del cliente, html:744-776), nombre, chips de etapa, chip logístico (💰 Cobrado / 🚚 Entregar hoy / 🔴 Atrasada, cruzado con Supabase), badges "🔔 te esperan / 💬 te contestó / ⏰ Nd", contador 💡 de correcciones pendientes, palpito celeste "✨ nuevo" (1ª vez por dispositivo, localStorage). html:950-967.

**Panel de chat (mismo `#chatpane` se reubica al modal del Kanban, html:970-984):**
- Topbar: chip de estado del ciclo venta→entrega (`estadoNegocio()`, html:1974-1993), botón **📥 Archivar / 📤 Devolver**, y control del bot: **🙋 Yo lo llevo** (pausa el bot en ese chat) o, si está en manual, **⚡ Devolver: responde ya** (`/api/bot-responder`: reactiva Y genera respuesta con el cerebro real) y **🤖 Devolver: espera al cliente** (`/api/control`). html:1014-1019, 1878-1895.
- **🧾 Ficha del cliente** (html:1290-1404) — la tarjeta más cargada del panel:
  - Tag "automática" (regex) o "✨ IA" (+aviso "hay mensajes nuevos" si el análisis quedó viejo) + botón **🔍 Analizar con IA / 🔄 Reanalizar** (`/api/analizar`, corre claude -p; además reconcilia chat↔entrega).
  - Banner de **enlace chat↔entrega**: verde si enlazado (✕ quitar), ámbar si hay sugerencia (✓ Sí es este / no es). html:1306-1315, 1823-1853.
  - Banner **"confirmó por correo, falta subirlo"** con botones de 1 clic: **🚀 Confirmar para mañana / pasado mañana / otro día (date-picker)** o **📱 Pedir lo que falta por WhatsApp** / **📞 El teléfono lo agrego yo**. html:1580-1626.
  - Grid de campos **editables in situ** (clic → input → Enter): comuna, dirección, nº baños, fecha, duración, email, teléfono (whitelist `CAMPOS_MANUALES`, mjs:395-405; endpoint `/api/ficha-campo` mjs:1437). Lo fijado a mano se marca ✏️ y manda sobre regex e IA.
  - Fila **IVA** con botones "Con IVA / Neto / ↺ Auto" (`/api/ficha-iva`; le llega al bot como orden). html:1271-1289.
  - Acciones: **📱 WhatsApp** (wa.me), **🗺️ Ver en Maps**, **📋 Copiar datos**, **💡 Sugerir seguimiento** (rellena el composer, no envía), **📋 Solicitar datos pendientes** (rellena el composer con checklist ✅/❌). html:1333-1339, 1464-1505.
  - Fila **Etapa**: ✅ Cerrado · ❌ Perdido (despliega 7 motivos como botones, html:1861-1867) · ⏳ Pendiente · ↺ Auto (`/api/etapa`).
  - Sección **📄 Cotización formal**: precio neto/baño, nº baños, email, extras dinámicos (➕ agregar extra), flete + motivo, hint de total con IVA; botones **📄 Generar y previsualizar** (PDF vía `generar_cotizacion.py`) y **📧 Enviar por correo + WhatsApp** (Resend + outbox del bot; confirm() con total). html:1346-1365, 1717-1764; backend `/api/cotizar` mjs:1192-1243.
  - Sección **🚚 Confirmar entrega / 🔄 Actualizar entrega**: dirección exacta, neto/baño, fecha (default deducido de "el lunes", "18 de julio"… html:1641-1653), teléfono obligatorio (💾 Guardar en la ficha), hora/franja, contacto de respaldo (nombre+teléfono); **Preparar aviso** (preview dry-run) → dos textareas editables (mensaje al repartidor + confirmación al cliente) → **✅ Enviar aviso + subir al sistema** (Supabase + WhatsApp al repartidor desde el número del bot; dedup con confirm de reenvío; modo actualización = mensaje corto). html:1366-1397, 1660-1715; backend `/api/entregar` mjs:1309-1391.
  - Pies de estado: 📧 cotización enviada / ✅ confirmó por correo / 🚚 entrega avisada. html:1399-1401.
  - **✉️ Correos con esta persona**: lista compacta (worker agente-correos) + los mismos correos **intercalados como tarjetas en el hilo** con expandir cuerpo, abrir adjunto PDF y botón **"✅ Es la confirmación del cliente"** (`/api/confirmacion`: re-análisis IA chat+correos, checklist de faltantes, burbuja en el chat). html:1164-1228, 1766-1809.
- **💤 Seguimiento programado** (tarjeta): fecha+hora+texto, checkbox "🤖 que el bot lo redacte", **💤 Programar mensaje** / **✖️ Cancelar**; muestra el último enviado/cancelado. Envío real lo hace el bot (9:00-21:00, se cancela si el cliente escribe). html:1044-1091; `/api/recordatorio` mjs:1110-1124.
- **📝 Nota general del chat** (textarea → `/api/feedback` target `__chat__`, aprende al instante). html:1029-1034.
- **⭐ ¿Qué tan bien atendió el bot?** (nota-card): estrellas 1-5, botón 💬 Comentario (prompt(); se guarda como nota Y como corrección), chips "⭐ tuya / ⚖️ IA / 👍N·👎N". html:2576-2640.
- **Hilo de mensajes**: burbujas cliente/IA/Tú con ✓/✓✓/✓✓azul reales, aviso "⏳ sin abrir / ⚠️ no entregado", "última conexión" en el subtítulo; bajo cada mensaje del bot: **👍 👎** (calidad) y **💡 enseñar** (textarea → `/api/feedback`, regla al instante). html:1127-1162, 2596-2609.
- **Respuestas rápidas**: 4 botones fijos (qué incluye / formas de pago / tiempos / factura) que rellenan el composer. html:537-542.
- **Composer**: envía por WhatsApp vía outbox del bot y pone el chat en manual. html:543-546, 1900-1911; `/api/responder` mjs:1248-1261.

#### A.3 Vista 🗂️ Kanban (html:550-563, 1913-2357)
- Cabecera: stats (N cotizando · N por confirmar · N por entregar hoy/próximas/atrasadas · $X por cerrar · antiguos ocultos), filtros: **📅 desde** (date, persiste `kanbanDesde`) + **ver todos**, buscador, **✉️ con contacto**, **⏳ esperando al cliente**, **📭 sin cotizar**.
- 4 columnas `LIFE` (html:1927-1932): **Cotizando** y **Cotizado · por confirmar** (chats, con drag&drop que fija etapa vía `/api/etapa`; separadores "✅ CONFIRMADOS · SUBIR AL SISTEMA" / "🕓 ESPERANDO SU SÍ" / "💤 DORMIDOS"), **🚚 Por entregar** y **Cobrado ✓** (entregas desde Supabase, solo lectura, con separadores 🔴 ATRASADAS / 🚚 HOY / 📅 fecha / ✅ ENTREGADO · FALTA COBRAR).
- Tarjeta de chat: avatar, calor 🔥/🟡/🧊, chips (🚽N, contacto ✓, ❌ motivo perdido, 🚚 al repartidor, 📧 confirmó por correo, 📧 cotizado, "falta cotizar", "✅ confirmó · falta subirlo", 💤 despierta), métricas **🤖 IA %** (participación del bot) y **⭐ Gestión %** (nota 1-5 convertida) + ❓ dudas, barra de cuenta regresiva a 24h sin confirmar. Clic = abre el chat en modal. html:2307-2340.
- Tarjeta de entrega: estado (Pendiente/En camino/Entregado/Pagado/Atrasada), reagenda "de X → a Y", plazo del arriendo, y aviso **🔁 cliente recurrente** ("Volvió a escribir — ¿es un pedido nuevo?" → **➕ Es un pedido nuevo** crea tarjeta `jid#2` / **No, es lo mismo**). html:2089-2127; pedidos mjs:78-119.

#### A.4 Vista ✨ Aprendió (html:565-566, 2642-2659)
- Lista de reglas aprendidas (de `data/aprendizajes.jsonl`), cada una con fecha/origen y botón **Deshacer esta regla / Reactivar** (`/api/aprendizajes/estado`). No permite crear ni editar el texto de una regla.

#### A.5 Modal ❓ Dudas del bot (html:578-590, 2359-2554)
- Tarjetas de dudas (tipo 💲precio/📧cotización/🚚entrega/💬retomar/📝dato) con opciones-botón (la recomendada en verde; "otro precio" abre input numérico inline). Si la opción trae acción (`d.accion.endpoint`, ej. cotizar), **primero ejecuta la acción y solo después marca la duda resuelta**; error queda dentro de la tarjeta. Botones: **💬 Ver el chat** (abre modal) y **🗑️ Descartar**. Al responder con avance, el chat vuelve al bot (mjs:1619-1632).

### B. Página `/entrenar` (entrenar.html) — gimnasio
- Header: **← Panel**, **📈 Calidad** (drawer: tabla semanal nota tuya vs nota IA con efectividad %), **✏️ Nota general** (prompt → regla), **🧠 Reglas** (drawer con Apagar/Prender — mismos datos que la pestaña Aprendió), **📋 Copiar resumen** (genera `data/entrenamiento-resumen.md` y lo copia). html:96-105, 421-468.
- Lateral: **7 escenarios hardcoded** (obra, evento, parcela, caro, factura, urgente, libre; html:150-158) + tabs **Prácticas / Chats reales 🤖** (la lista sale de `/api/calidad/resumen`, no de `/api/gym/lista`).
- Barra del chat: chips ⭐ tuya / ⚖️ IA, **⭐ Calificar** (prompt 1-5 + comentario), **⚖️ Evaluar con IA** (juez opus, 30-90s), **🎬 ¿Cómo lo haría el bot solo?** (replay de un chat real: actor-IA imita al cliente; polling cada 5s hasta terminar; solo visible en chats reales). html:117-124, 361-418.
- Chat: tú escribes de cliente → responde el **cerebro real** (`/api/gym/cliente`, mismo tarifario y reglas); mensajes del bot con **👍 👎 ✏️** (corrección → regla al instante, toast "🧠 Regla nueva"); tarjetas de sistema **[ENSAYO]** cuando la ficha llega al 100%: PDF real de cotización, correo que saldría, imagen de la ficha del baño; misma puerta de coherencia de precios que producción (mjs:1734-1783).

### C. Endpoints del backend (dashboard.mjs) — 43 rutas
`GET /` `/aviso.mp3` `/api/chats`(1048) `/api/entregas`(1053) `/api/avatar`(1061) `/api/estado`(1090) `/api/ficha-img`(1395) `/api/coti-pdf`(1401) `/api/correos-lead`(1455) `/api/correo-adjunto`(1467) `/api/correo-lead`(1535) `/api/chat`(1546) `/api/aprendizajes`(1573) `/api/control`(1587) `/api/dudas`(1605) `/api/dudas/chat`(1610) `/api/calidad/chat`(1652) `/api/calidad/resumen`(1659) `/api/gym/replay-estado`(1695) `/entrenar`(1700) `/api/gym/lista`(1708) `/api/gym/resumen`(1839) · `POST /api/etapa`(1096) `/api/recordatorio`(1110) `/api/archivar`(1128) `/api/enlazar`(1138) `/api/pedido`(1150) `/api/analizar`(1166) `/api/cotizar`(1192) `/api/responder`(1248) `/api/bot-responder`(1267) `/api/entregar`(1309) `/api/ficha-telefono`(1413) `/api/ficha-iva`(1425) `/api/ficha-campo`(1437) `/api/confirmacion`(1484) `/api/feedback`(1552) `/api/aprendizajes/estado`(1577) `/api/control`(1593) `/api/dudas/responder`(1619) `/api/dudas/anular`(1634) `/api/calidad/nota`(1644) `/api/calidad/evaluar`(1664) `/api/gym/replay`(1676) `/api/gym/cliente`(1785).
- **Sin consumidor en el front** (verificado con grep): `GET /api/gym/lista`, `GET /api/dudas/chat`, `GET /api/control` (el front solo usa el POST; el estado manual llega dentro de `/api/chats`).

---

## (b) Mapa "dónde se configura qué" hoy

| Cosa | Dónde vive | ¿Visible en el panel? | ¿Editable desde el panel? |
|---|---|---|---|
| **Persona del bot** (prompt completo) | `.env` → `BOT_PERSONA` (línea 9 del `.env`; leído en `src/config.js:59`) | ❌ No se ve en ninguna vista | ❌ Solo editando `.env` + reiniciar el bot |
| Género del bot / uso del nombre del cliente | `.env` → `BOT_GENERO`, `USAR_NOMBRE` (config.js:69-70) | ❌ | ❌ |
| **Tarifario / precios oficiales** | **Código**: `src/precios.js` (tablas `CENTRICAS`/`LEJANAS`, escaleras multi-baño, política IVA comentada en cabecera) | ❌ No hay vista de precios; solo se asoman indirectamente (dudas de precio, cotización retenida en el gimnasio) | ❌ Cambiar un precio = editar código + kickstart del bot + correr `_test-precios.mjs` |
| Política de IVA por chat | `datos-lead.json` campo `modo_iva_manual` | ✅ fila IVA de la ficha | ✅ botones Con IVA/Neto/↺Auto |
| **Reglas aprendidas** | `data/aprendizajes.jsonl` (+ espejo `.md`) | ✅ en DOS lugares: pestaña ✨ Aprendió y drawer 🧠 Reglas del gimnasio | ⚠️ Solo activar/retirar. **No** se puede crear una regla directa ni editar su texto: solo nacen de correcciones (feedback) destiladas por `claude -p` |
| **Pausa del bot por chat** ("yo lo llevo") | `data/control.json` | ✅ pero solo chat a chat (botón en el chat abierto; chip "🙋 tú" en tarjetas) — **no hay vista global de pausas ni interruptor global del bot** | ✅ por chat |
| Parámetros de auto-pausa (TTL al escribir el dueño, umbral sticky) | `.env` → `OWNER_MANUAL_TTL_MS`, `OWNER_MANUAL_STICK_AFTER` (config.js:96-101) | ❌ | ❌ |
| **Gating anti-ban** (delays de respuesta, topes 40/hora y 200/día, horario de atención, ignorar grupos) | `.env` → `REPLY_DELAY_MS`, `FOLLOWUP_DELAY_MS`, `MAX_ENVIOS_HORA/DIA`, `BUSINESS_HOURS_*`, `IGNORE_GROUPS` (config.js:81-103) | ❌ | ❌ |
| **Recordatorios 💤** | `data/recordatorios.json` | ✅ por chat (tarjeta 💤 + chip en Kanban) — no hay lista global "todos los programados" | ✅ agendar/cancelar por chat. La **ventana 9:00-21:00 está fija en código** (`src/recordatorios.js`), no configurable |
| Dudas (umbrales de cuándo preguntar) | Código: `src/dudas.js`, `src/integracion.js` (`precioCoherente`) | ✅ las dudas sí (buzón) | ❌ los umbrales no |
| Número del repartidor | `.env` → `REPARTIDOR_NUMERO` (validado en `/api/entregar` mjs:1332) | ❌ (solo el error "no hay número configurado") | ❌ |
| Imagen de la ficha del baño | `.env` → `FICHA_IMG` (config.js:108) | ✅ se sirve en `/api/ficha-img` | ❌ cambiar la foto = editar `.env` |
| Cerebro (modo cli/stub, límite de historia) | `.env` → `BRAIN_MODE`, `HISTORY_LIMIT` | ⚠️ el backend lo expone (`/api/estado` → `bot.brain`) pero **el front nunca lo muestra**; ídem `loop.lastRunMin` del loop de aprendizaje | ❌ |
| Credenciales Supabase / correo / cotizaciones / python | `.env` + `config/agente.local.json` del repo de cotizaciones (mjs:816-821) | ❌ | ❌ |
| Escenarios de práctica del gimnasio | **Hardcoded** en entrenar.html:150-158 | ✅ como chips | ❌ agregar un escenario = editar HTML |
| Respuestas rápidas del composer | **Hardcoded** en dashboard.html:538-541 | ✅ | ❌ |
| Plantillas de mensajes (confirmación al cliente, solicitar datos, sugerir seguimiento, aviso al repartidor) | Código: mjs:884-918 y html:1464-1505, 1615-1622 | ✅ se ven al usarlas (editables ANTES de enviar, bien) | ❌ la plantilla base no se puede cambiar |
| Sonido y filtros de vista | localStorage por dispositivo (`crm_avisos_on`, `crm_sonido_src`, `chatsSoloHoy2`, `kanbanDesde`, `crm_clientes_vistos`) | ✅ | ✅ (pero invisible que es "por dispositivo") |
| Horario del loop de aprendizaje | launchd (fuera del repo del panel) | ❌ | ❌ |

**Resumen duro:** lo que define el COMPORTAMIENTO del bot (persona, tarifario, gating, horarios, umbrales de dudas, repartidor) vive en `.env` y en código; el panel solo administra lo OPERATIVO (chats, etapas, cotizaciones, entregas, reglas on/off, recordatorios, pausas por chat).

---

## (c) Puntos de confusión detectados

1. **El entrenamiento está repartido en 5 entradas distintas que van al mismo lugar** (`/api/feedback`): 💡 "enseñar" bajo cada mensaje (dashboard, textarea inline), ✏️ del gimnasio (caja ámbar), 📝 "Nota general del chat" (tarjeta del dashboard), ✏️ "Nota general" del gimnasio (un `prompt()` nativo), y 💬 "Comentario" de la nota-card (otro `prompt()` que además guarda en calidad). Cinco UIs, tres estilos visuales, mismo efecto. Nadie podría deducir cuál usar cuándo.
2. **Las reglas aprendidas tienen dos administradores con vocabulario distinto**: pestaña ✨ Aprendió ("Deshacer esta regla / Reactivar", html:2651) y drawer 🧠 Reglas del gimnasio ("Apagar / Prender", entrenar.html:444). Mismos datos, dos lugares, dos verbos.
3. **La calidad también está duplicada con patrones distintos**: en el dashboard la nota 1-5 son botones-estrella bonitos (html:2576); en el gimnasio es `prompt("Nota para este chat…")` (entrenar.html:364) — incómodo en iPhone. Los 👍👎 sí son consistentes.
4. **Dos taxonomías de embudo conviven y no calzan**: `STAGES` del backend (nuevo/cotizo/pendiente/concreto/perdido, mjs:206-212) vs columnas `LIFE` del Kanban (cotizando/cotizados/por_entregar/cobrado, html:1927-1932). Arrastrar a "Cotizando" fija la etapa `cotizo`, a "Por confirmar" fija `pendiente`; "concreto" y "perdido" no tienen columna (los perdidos desaparecen del tablero; los cerrados se "gradúan" a entrega solo si hay match por teléfono/enlace). Hay incluso un guard que avisa "arrastrar aquí no sirve" (html:2353). La etapa además se cambia en la ficha (4 botones) y automáticamente por regex → 3 mecanismos para el mismo dato.
5. **El precio se toca en 3 lugares dentro de la MISMA ficha**: la fila 💵 del grid (no editable, solo muestra), el input de 📄 Cotización formal (`coti-precio`) y el input de 🚚 Entrega (`ent-precio`). Extras y teléfono también se repiten entre secciones. La tarjeta de ficha completa supera las 100 líneas de HTML generado con ~25 acciones posibles.
6. **"Confirmar para mañana" existe en 2 lugares**: banner de la ficha (html:1587) y dentro de la tarjeta del correo en el hilo (html:1181) — con lógicas de scroll cruzadas entre ambas ("usa los botones de la ficha 👆").
7. **Botones que rellenan el composer sin enviarlo** (💡 Sugerir seguimiento, 📋 Solicitar datos, respuestas rápidas): patrón bueno para control, pero invisible — el resultado aparece abajo, lejos del botón, y solo un toast lo explica.
8. **Dos apps visuales distintas**: el gimnasio es una página aparte con su propio CSS (colores y componentes diferentes: `--acento` vs `--accent`, drawers vs modales, tabs propias). Se llega por una "pestaña" que en realidad es un link; volver es "← Panel". La lista "Chats reales 🤖" del gimnasio duplica la lista de chats del dashboard pero sin ficha ni acciones.
9. **Filtros de fecha independientes y persistidos distinto**: "📅 Solo hoy" (lista de chats, `chatsSoloHoy2`) y "📅 desde" (Kanban, `kanbanDesde`). Mismo concepto, dos controles, dos claves; la clave `chatsSoloHoy2` es v2 porque hubo que invalidar la preferencia vieja — deuda de diseño.
10. **El semáforo desaprovecha datos que el backend ya expone**: `/api/estado` devuelve `loop.lastRunMin` (último repaso del aprendizaje) y `bot.brain`, pero `loadEstado()` (html:881-900) nunca los muestra. No hay forma de saber desde el panel si el loop de aprendizaje está vivo.
11. **Endpoints muertos**: `GET /api/gym/lista`, `GET /api/dudas/chat` y `GET /api/control` no tienen consumidor en ningún HTML (verificado por grep) — señal de flujos que se movieron y dejaron rastro.
12. **Monolito frágil**: dashboard.html concentra 2.673 líneas con CSS+markup+lógica; todo se repinta con `innerHTML` + firmas anti-parpadeo (LIST_SIG/KANBAN_SIG/CURRENT_SIG/DUDAS_SIG, 4 sistemas de firma distintos) y los handlers van como strings `onclick` con doble escape (`esc`/`jsq`, html:686-691). Cada feature nueva agranda la ficha o agrega otra firma.
13. **No existe ninguna vista de "configuración"**: el dueño no puede ver desde el panel qué persona tiene el bot, qué precios oficiales usa, sus límites anti-ban ni su horario. Cuando algo de eso cambia, no hay huella visible (contrasta con las "novedades ✨" del panel-cliente del maestro).

---

## (d) Qué debería tener un "panel de configuración del bot" limpio (necesidades reales, derivadas de lo que YA existe)

Cada punto de abajo corresponde a algo que hoy existe pero está en `.env`, en código o duplicado — no es wishlist:

1. **🧠 Persona y trato** — ver/editar `BOT_PERSONA`, género, uso del nombre del cliente, con "aplicar" que reinicie/recargue el bot. Hoy: `.env` a mano (el bot ni siquiera muestra qué persona corre).
2. **💵 Tarifario** — la tabla de zonas/precios de `src/precios.js` renderizada y editable con validación (y el equivalente del `_test-precios.mjs` corriendo antes de aplicar), incluida la política de IVA y las escaleras multi-baño. Es EL dato de negocio que más cambia y hoy exige editar código.
3. **📚 Conocimiento/reglas (los futuros "caminos")** — UN solo administrador de reglas aprendidas: crear regla directa, editar texto, apagar/prender, ver origen (chat real / gimnasio / duda) y cuándo se aplicó. Hoy: dos UIs de solo on/off y las reglas solo nacen por destilación de correcciones.
4. **⏸️ Control del bot** — interruptor global (pausar el bot entero), vista de TODOS los chats en pausa manual (hoy hay que abrirlos uno a uno), y los parámetros de gating en simple: velocidad de respuesta, topes por hora/día, horario de atención. Todo eso ya existe en `.env`/`control.json`.
5. **📇 Canales y conexión** — estado de la sesión WhatsApp (ya está el semáforo), número vinculado, re-vincular; y sitio preparado para el segundo canal (Instagram). Mostrar también `bot.brain` y `loop.lastRunMin` que el backend ya entrega.
6. **🔌 Integraciones** — número del repartidor, correo (worker), Supabase, sistema de cotizaciones, foto de la ficha del baño (subirla en vez de rutear un archivo). Todos son valores de `.env`/JSON que hoy solo fallan en silencio ("no hay número de repartidor configurado").
7. **💬 Textos del negocio** — respuestas rápidas del composer (hoy 4 hardcoded), plantillas de: confirmación al cliente, aviso al repartidor, solicitar datos, seguimiento sugerido y los escenarios del gimnasio (hoy hardcoded en entrenar.html).
8. **💤 Recordatorios** — lista global de mensajes programados (hoy solo por chat) y la ventana horaria de envío configurable (hoy 9:00-21:00 fija en `recordatorios.js`).
9. **🏋️ Entrenamiento unificado** — una sola entrada "enseñar" con la misma UI en chat real, gimnasio y dudas; la nota 1-5 con el mismo widget en ambas páginas; el gimnasio integrado a la misma app (no página con CSS aparte). El flujo "el bot pregunta → tú respondes → nace la regla → queda el camino" ya está completo en dudas+feedback+aprendizajes: solo falta unificarlo y hacerlo visible.
10. **🔔 Preferencias del dispositivo** — un lugar que agrupe lo que hoy está regado en la appbar y localStorage (sonido, notificaciones, filtros por defecto) y que DIGA que es por dispositivo.

**Lo que ya está bien y conviene conservar tal cual**: el patrón preview-antes-de-enviar (cotización, aviso al repartidor, recordatorio IA), el buzón de dudas con acciones ejecutadas antes de resolver, la edición in situ de la ficha con ✏️ manual-gana-a-IA, los checks ✓/✓✓ reales, el enlace chat↔entrega con sugerencia confirmable, y el guardado optimista con firmas que evita parpadeo.
