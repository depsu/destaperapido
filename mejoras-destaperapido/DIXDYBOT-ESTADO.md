# DIXDYBOT — Estado del proyecto y mapa de documentos

**Última actualización:** 26-jul-2026 (S5: el negocio en el panel + el cerebro
reparado) · **Estado: CONSTRUCCIÓN EN MARCHA.**

---

## 🚦 EMPIEZA POR AQUÍ (26-jul-2026) — 840 tests verdes, tsc limpio

**Lo más importante que hay que saber antes de tocar nada:**

> ### 🚨 EL PEDIDO NUNCA NACE — bloqueante del cutover del 25-ago
>
> `escritor.crearPedido` tiene **un solo llamador en producción**:
> `src/modulos/migrador/espejo.ts:703` (el migrador). Los 23 pedidos de la base viva son
> todos `p-mig-*`. **El sistema nuevo jamás ha creado un pedido.** Cuando la instancia
> tome el número, los clientes conversarán bien y el tablero quedará congelado en esos 23
> para siempre. No se nota el día uno: se nota la semana siguiente.
>
> Medido en la base viva: **75 chats vivos sin pedido**, 73 escribieron esta semana, 62
> con 7+ mensajes. No es basura — es negocio sin ficha. (Otros 88 sin pedido están
> dormidos.)
>
> **La cadena está rota en tres puntos, verificados uno por uno:**
> 1. `Efecto` con `crear_pedido`/`mover_pedido` **existe** (`src/schemas/camino.ts:8-16`),
>    y `Paso.efectos` también (`:23`).
> 2. `motor/efectos.ts`, al que apunta el comentario de `camino.ts:77`, **no existe**.
> 3. Los 30 caminos publicados declaran **cero efectos** (24 pasos, todos `mensaje`).
>
> Y hay un cuarto punto, el más caro: `orquestador.ts:145` **le pide `paso_completado` al
> modelo y nunca lee la respuesta** (`pathSiguiente:218-240` solo usa `sigue` y
> `transicion_elegida`).
>
> **Pieza previa que falta y nadie había visto:** `SalidaTurno` (`src/schemas/turno.ts`)
> NO trae campos extraídos. **Hoy nada saca la dirección, la fecha o la cantidad de lo que
> el cliente escribe** — eso lo hacía `extraer.js` del bot viejo, y el migrador solo copió
> su resultado. Sin extracción, los checks del despacho (abajo) tampoco se llenarían solos.
>
> **Decisión de Alejandro (26-jul):** el pedido nace **al primer dato duro** (aparece una
> dirección, una fecha, una cantidad o un precio → nace la ficha; antes es conversación).
> Genérico: sirve a cualquier rubro y atrapa al cliente aunque no entre en ningún camino.

### Lo que se hizo el 26-jul

- **`fea6c39` · los 4 checks del despacho.** Regla de Alejandro: no sale a terreno sin
  dirección, día, cantidad y valor. Los tres primeros son campos de ficha (`requiere` del
  embudo); el VALOR no se podía exigir porque `montoNeto` es COLUMNA del pedido, no ficha
  → `Etapa.requiere_monto` (default `false`, retrocompatible). El rechazo devuelve el
  porqué guardado en `CAMPO_SIN_MONTO`: es una instrucción, no un no. Verificado contra la
  base viva: los 6 pedidos ya despachados pasan los cuatro.
- **`f2d2a56` · módulo `entregas`.** El commit anterior dejó una TRAMPA: exigía `direccion`
  y `cantidad_banos` y **ningún módulo declaraba esos campos** (los únicos del molde eran
  `comuna`/`pedido`/`correo` del cotizador) → el panel no los dibujaba y el dueño no podía
  completarlos a mano. `entregas` declara dirección y fecha, aporta la etapa `por-entregar`
  y trae **`campos_extra`**: la vía para que un CLON declare campos de su rubro sin que el
  molde sepa del rubro (destaperapido suma `cantidad_banos` en
  `dixdybot-data/ajustes/entregas.json`). **Ojo:** los ids de ficha son snake_case, a
  diferencia de los ids de etapa/módulo, que son kebab estricto.
  Incluye **dedup de etapas en `componerAportes`** — embudo y entregas nombran ambos
  `por-entregar` y el tablero la pintaba dos veces; gana la primera (= la del dueño,
  porque `embudo` va antes en `MODULOS`) y hay test que fija ese orden.
- **`3869b2c` · el cerebro volvió a pensar.** Primera prueba de punta a punta contra la
  instancia viva: el bot contestaba la plantilla de emergencia. La sospecha obvia (el
  envoltorio del CLI 2.1.220 cambió) era **FALSA** — se verificó campo por campo. La causa:
  pidiéndole `camino: { sigue, paso_completado }`, el modelo leyó `sigue` como
  "¿CUÁL sigue?" y devolvió el **id del camino** donde iba un booleano; JSON perfecto, con
  la respuesta al cliente ya escrita, tumbado entero por Zod. Arreglo en dos capas: el
  prompt declara los tipos (plan A) y `booleanoTolerante()` endereza (red). **Los negativos
  incluyen los del castellano** (`ninguno`/`ninguna`/`nada`/`no aplica`): el prompt está en
  español y sin eso un `"sigue": "ninguno"` se leía como SÍ — invertir la respuesta es peor
  que perderla. El aviso al dueño ya adjunta el texto que llegó.

### Cómo probar HOY (sin WhatsApp, sin cuenta Meta, sin gastar)

1. El servicio corre por launchd: `launchctl kickstart -k gui/501/com.dixdy.dixdybot-panel`.
   Panel en **http://127.0.0.1:8793**. Datos en `~/SaSS/destaperapido/dixdybot-data/`.
2. `panel.entrada_de_prueba` quedó **prendido** en `ajustes/panel.json`. Escribirle al bot
   como si fueras cliente:
   `curl -s -X POST http://127.0.0.1:8793/api/simular/entrante -H 'Content-Type: application/json' -d '{"texto":"...","de":"quien-sea"}'`
   El mismo `de` continúa la MISMA conversación. El canal `sim` se monta solo.
3. Leer el hilo: `GET /api/chats/sim%3A<de>`. El cerebro tarda ~12-30 s (motor `cli`, la
   suscripción de Alejandro; **no hay `ANTHROPIC_API_KEY`** — el motor `api` siempre da
   `no_disponible` y eso NO es un bug).
4. Si sale *"Dame un momento, ya te confirmo."* el cerebro NO pensó: mirar la última línea
   de `dixdybot-data/panel.log`, que ahora dice la causa con el texto recibido.

### Estado de los canales (26-jul)

`wa-baileys`: **apagado**, sin número — nunca se ha vinculado un WhatsApp real.
`wa-cloud`: apagado, le faltan los 4 requisitos de Meta. Único canal vivo: `sim`.

### Decisiones de Alejandro del 26-jul (ya tomadas, no volver a preguntar)

| Tema | Decisión |
|---|---|
| Los chats sin pedido | Se llaman **"cotizando"** — van en esa pestaña (⚠️ **sin implementar**) |
| Checks del despacho | **Los cuatro**: dirección, día, cantidad, valor ✅ hecho |
| Comprobante de pago | **Mueve solo a Cobrado** (eligió el automático sobre avisar-y-confirmar) ⚠️ sin implementar |
| Cuándo nace el pedido | **Al primer dato duro** ⚠️ sin implementar |

**Sobre el comprobante automático — advertencias que Alejandro ya escuchó y aceptó:**
(1) la transición `por-entregar→cobrado` **no acepta origen `camino`**, solo `dueno`/`externo`;
(2) quien paga por adelantado está en `por-confirmar` y **no existe transición** desde ahí a
`cobrado`; (3) `cobrado_cuando: 'total'` y una foto no prueba el monto. Las dos primeras son
cambios en SU embudo que aún no ha autorizado explícitamente — **pídeselos antes de tocar**.

### Lo que necesita a Alejandro

- **Llave de API de respaldo** (cuesta plata): sin ella, si su suscripción falla el bot
  queda mudo. Hoy la cadena es `cli → api → plantilla` y el eslabón del medio no existe.
- **Vincular un WhatsApp de pruebas** (2 min, con un número secundario, NUNCA el que vende).
- **Aprobar los 30 caminos** en lote (tarea #9) — y ahí se declara en qué paso nace el pedido.
- Expediente Meta (tope **30-sep**) y la decisión del servicio de sombra (cuesta cuota).

### Reglas de esta obra que no se negocian

- **NO tocar el bot vivo** de `~/SaSS/destaperapido/whatsapp-bot/` — es lo que vende hoy.
  Solo lectura. Nada de `kill`, `restart`, `npm`, `launchctl unload`.
- **NUNCA agregar una columna a `src/db/esquema.sql`**: todo es `CREATE TABLE IF NOT
  EXISTS` y SQLite ignora en silencio una columna nueva si la tabla ya existe. Los tests
  usan `:memory:` (verde), tsc verde, commit verde — y la base viva no la recibe. Salida
  probada: tabla lateral en las `migraciones` del módulo. Un `CREATE INDEX IF NOT EXISTS`
  **sí** se aplica en cada arranque.
- **Reparto por ARCHIVOS, no por tema.** El FRONT edita `dixdybot/panel/pwa/*`; el backend
  no los toca. Ver `REPARTO-SESIONES.md`.
- `pnpm exec tsc --noEmit` **y** `pnpm exec vitest run` en verde, o no hay commit.

---

> **Arranque de S5 (25-jul, tarde) — dos agujeros de fondo tapados, 647 tests verdes:**
> **(1) El mensajero** (`core/mensajero.ts` + `modulos/mensajero`, núcleo): el pipeline
> hacía `await canal.enviarTexto(...)` y TIRABA el resultado — un envío fallido dejaba al
> cliente esperando para siempre y al dueño sin enterarse; y los acuses que los canales ya
> emitían al bus no los escuchaba nadie (las 3.979 filas de la instancia tenían `estado`
> vacío). Ahora: ritmo humano por ajuste, topes anti-bloqueo **leídos de la base** (un
> reinicio ya no regala cupo, a diferencia del bot vivo), reintentos solo de lo
> reintentable (`auth` NO se reintenta), acuses **monótonos en el UPDATE**, y nada en
> silencio. **(2) La ingesta** (`modulos/ingesta`, apagable): fotos y documentos se
> guardan y **el cerebro los MIRA por su ruta en el mismo turno** — 1 llamada, $0 de API
> extra, verificado con `claude -p` antes de construir sobre el supuesto. El audio nace
> SIN transcripción (es plata nueva): el bot pide que se lo escriban en vez de inventar.
> Probado con el cerebro real: foto → describió los colores exactos en 28,1 s; audio →
> "no puedo escucharlo, ¿me lo escribes?" en 16,8 s, sin cifras inventadas.
> **(3) El adaptador `wa-baileys`** (25-jul, tarde — `src/canales/wa-baileys/` +
> `cli/vincular.ts`, 706 tests verdes): el molde ya puede hablar por el número propio.
> Construido leyendo el bot vivo en SOLO-LECTURA y trasplantando sus **28 cicatrices**
> documentadas, no reinventándolas. **Reparto núcleo/adaptador:** lo genérico (ritmo,
> topes desde la base, reintentos, escalera de acuses) se queda en `core/mensajero.ts`;
> lo que solo existe en WhatsApp no oficial (reconexión + circuit breaker 8/5min→10min,
> candado cifrado corrupto y su sanación, jid canónico literal incl. `@lid`, presencia
> real) vive en el adaptador — el core nunca ve un vendor. **Decisión que se apartó del
> plan:** el legado del emisor se REESCRIBIÓ en TS conservando cada número y su razón, en
> vez de copiar los `.js` (aceptar JS mezclado abre una excepción permanente en tsconfig).
> Cerrado con test que MUERDE (verificado por mutación deliberada): eco de envíos propios,
> los DOS canales de acuses, 401 sin reintento, sanación con 3 min + 1 reintento + guarda
> de presencia, acuse del reenvío reportado con el id ORIGINAL, filtro del ruido de
> libsignal. `cli/vincular.ts` es proceso APARTE (vincular desde el bot dejaba la sesión
> en 440); marcador de enlace = `me`, no `registered`. Baileys pineado en 6.7.23 (la
> versión probada en producción); es la dep #6 del molde y con diferencia la más pesada.
> **Falta de S5:** el `MANUAL.md` + launchd del cutover (P6), el gate de corte de 5
> condiciones y **la primera conexión real a WhatsApp** (todo lo de canal está probado
> contra un WhatsApp simulado; nunca se ha vinculado un número de verdad — conviene hacerlo
> con un número secundario, no con el que vende).
>
> **Hecho el 25-jul (además del adaptador):**
> - **P5 · el migrador ya no pierde tus preguntas** (commit `86615eb`). El plan pedía que la
>   corrida final trajera las dudas pendientes de `dudas.js` y `espejo.ts` no abría ese
>   archivo: 8 decisiones tuyas en pausa se habrían perdido en el corte. `dudas.jsonl` es un
>   LOG PLEGABLE (alta + líneas de respuesta con el mismo id), así que se pliega por id antes
>   de mirar nada; ningún campo del schema lleva `.default()` porque un default rellena la
>   clave ausente y al plegar borraría las opciones del alta. Solo cruzan las PENDIENTES.
>   Se avisa dentro de cada una que contestarla **no** dispara el envío que allá disparaba
>   (`/api/cotizar` no existe acá). `migrar-huerfanos.jsonl` ganó `clase`: `no-corresponde`
>   (ruido esperado) vs `falta-dato` (trabajo real) — mezclados, 2 problemas dentro de 8
>   líneas se veían como 8.
> - **P3 · la compuerta** (commit `6de0907`). Debounce con presencia real, handoff al dueño
>   (30 min por un toque, indefinido si insiste 3 veces), **topes contados desde la base**
>   —la deuda D5: en el vivo cada reinicio de launchd regalaba cupo y el tope era una
>   lotería—, horario que cruza la medianoche, interruptor general del bot y aviso al topar
>   (el vivo se quedaba mudo sin avisar). Nace la tabla `pausas` y `conversaciones.asignado`
>   deja de ser una columna que nadie leía.
>   Destapó dos huecos que quedaron cerrados: el adaptador de P1 descartaba **todos** los
>   mensajes propios (el core nunca habría visto al dueño entrar al chat), y un takeover
>   indefinido sin endpoint de devolución dejaba el chat mudo para siempre.
>   **Cambio estructural:** `atenderMensaje` agenda y vuelve; el turno corre dentro del
>   agendador, serializado por chat. Lo que el cerebro aún no vio se acumula, así que la
>   foto que llegó antes de "mira esto" no se pierde con el turno cancelado.
>
> **⚠️ Si vas a trabajar el backend en varias sesiones a la vez: lee primero
> `REPARTO-SESIONES.md`** (mapa de las 16 piezas pendientes P1-P16, qué archivo puente toca
> cada una, qué combinaciones se pisan y el tablero de piezas tomadas). El reparto es por
> ARCHIVOS, no por tema: dos sesiones sobre `escritor.ts` o `index.ts` se borran entre sí.
> Nota de calendario: el plan rector fecha S5 en 25-31 ago y el código ya va en S5 el 25-jul
> — vamos ~4 semanas adelantados respecto al documento.
Investigación completa (8 rondas, ~70 agentes + 2 deep research externos arbitrados) +
DISEÑO CONGELADO (prototipo v5, 18 iteraciones con Alejandro:
`dixdybot-prototipo-v5-congelado.html`, artifact 555843ca) + **molde vivo en
`SaSS/DIXDY/dixdybot/`** (12 módulos, 474 tests verdes, tsc limpio) + **instancia de
destaperapido en `SaSS/destaperapido/dixdybot-data/`** (184 conversaciones, 3.820 mensajes,
20 pedidos migrados; panel en `127.0.0.1:8793`).

**Hecho:** S1 shim del cerebro (el bot vivo ya consulta `llm.ts` del molde con doble red) ·
S2 módulos embudo+cotizador + migrador + panel real · S3-4 caminos v1, gimnasio
(personas/juez/sombra), la Duda junior→senior, el **orquestador del turno** (H-A atómica,
candado sin puerta de atrás) y las **vistas Caminos y Agentes** del panel con aprobación en
lote · **cierre de S4 (25-jul):** vista *Diseño* real (cero "En construcción" en el panel),
el **veredicto del candado visible ANTES de aprobar** (el mismo `verificarParaActivar` en el
panel, en el CLI `revisar-caminos.ts` y en la aprobación real) y la **sombra diaria** como
servicio, con gate por días de calendario. Dos agujeros graves tapados: el gate se pintaba
verde con el cerebro caído (la enlatada de emergencia puntuaba "mejora") y el lint de cifras
no miraba la plantilla que ve el cliente — ver `HALLAZGOS-25-JUL.md` §4.

**Próximo paso:** que Alejandro **apruebe en lote los 30 caminos destilados** (panel →
Caminos → borradores; informe en `caminos-veredicto.md`: 24 ✅ / 6 ⚠️ / 0 ❌ — **ojo:** el
"0 rechazados" NO significa que no se pisen entre ellos, ver `HALLAZGOS-25-JUL.md` §2 bis)
y luego **S5 cutover** (25-31 ago) — ver
`ronda8/plan-arranque-backend.md` (el plan rector del backend, semana a semana hasta dic).
Decisiones nuevas de producto (prototipo + memorias): pausa junior→senior multi-fase,
caminos con guía conversacional, módulos con APORTES, conexiones con chat+permisos,
tablero/etapas como datos, chats con bautizo/orden-por-atención/dormidos, onboarding de
negocio, correo multi-modo. El proyecto nuevo NACE de cero limpio (repo dixdybot/ en el
maestro, ver `ronda8/esqueleto-proyecto.md`); jamás se clona el bot viejo.

## Qué es

Rediseño del whatsapp-bot vivo de destaperapido (corre en
`~/SaSS/destaperapido/whatsapp-bot/`, FUERA de este clon) hacia **dixdybot**: producto
genérico multi-rubro y multi-canal (WhatsApp hoy, Instagram después), con cerebro Claude y
entrenamiento por **caminos** (conocimiento como rutas condición→acción versionadas, con
pausa-de-tema + pregunta al dueño + aprendizaje en caliente). El bot actual vende HOY: se
evoluciona por etapas en el mismo repo, sin sistema paralelo.

## Requisitos fijados por Alejandro (no negociables)

1. **Genérico-modular:** toda capacidad = módulo activable/configurable desde el panel;
   funciones nuevas de Claude Code nacen administrables; nada cableado al rubro.
2. **Design system único** (arranque de E2): referencias Chatwoot/Fin/Typebot/Linear →
   tokens+componentes en Claude Design (claude.ai/design, DesignSync) → cero variaciones.
3. **IA madre + agentes especialistas** (supervisor/handoff): router barato deriva EN
   SILENCIO al agente del rubro; cada agente carga solo los caminos de su dominio. El campo
   dominio/agente entra al esquema de camino desde el día 1 de E3.
4. **Escepticismo:** ninguna decisión se apoya en una sola fuente; verificar, fechar,
   evaluar encaje con la idea propia.

## El plan (resumen — detalle en ronda2/plan-revisado.md)

E0 cinturón (commit fixes vivos, alarma bot-ciego, circuit breaker, pins, backup sesión,
**verificar entrega real ✓✓ — Error 463 activo en Baileys**) → E1 **prioridad #1**: llm.js
puerta única + failover suscripción→API (por ToS/límites, NO por latencia: medida real del
cerebro 8-18s, total percibido 22,6s mediana = rango humano) → E2 conocimiento como datos +
vista Conocimiento + design system **+ 3 convenciones de plataforma (+2-3 días): convId
canónico (nada nuevo con clave jid), JSON Schema + vista Ajustes renderizada desde schema,
eventos.jsonl** → E3 caminos v1 (arranque en frío 68 reglas→20-30 caminos, pausa-de-tema,
backtesting patrón Fin, validación patrón Decagon, aviso por WhatsApp con código 5 letras)
→ E4 canal-como-enchufe + canal sim + único escritor → E5 canales oficiales Meta
(**Coexistence = ruta objetivo; 30-sep es fecha de DECISIÓN tras piloto en número
secundario, con Baileys de fallback caliente 30-60 días**; Instagram en una tarde) → E6
producto multi-cliente (API key por cliente; tiers 4-6 / 8-12 UF/mes **+ setup fee 5-10
UF**; clon-por-cliente, NO tenant_id) → E7 exploratoria voz (piloto Retell, ~US$0,09-0,15/
min todo incluido). Regla: la fecha del canal manda.

**Fechas duras:** 1-sep tarifas Chile definitivas · 30-sep decisión Coexistence ·
1-oct Meta cobra TODOS los service y utility en ventana 24h (Chile hoy US$0,0200/msg →
~US$20/mes a nuestro volumen; rate card oficial: marketing 0,0889/utility 0,0200) ·
**1-dic-2026 Ley 21.719 de datos**: antes de esa fecha, contrato de encargo de tratamiento
por cliente + derechos ARCO+P en el panel (el art. 8 bis hace del humano-en-el-loop un
requisito legal). HOY ya rige la 19.496: confirmación escrita de compra, retracto 10 días,
información veraz; y presentarse como asistente virtual anticipa la ley de IA en trámite.

## Mapa de documentos (en `mejoras-destaperapido/`)

- `DIXDYBOT-INVESTIGACION.md` — informe maestro ronda 1 (diagnóstico con evidencia,
  caminos validados, canales, Claude Code vs API, plan original E0-E6).
- `DIXDYBOT-RONDA2-TENDENCIAS.md` — ronda 2 (tendencias 2027, 3 supuestos rotos, papeleo
  Meta, referencias diseño/lógica, web-vs-app=PWA, competidores/pricing; §8 = requisitos
  de Alejandro).
- `investigacion-dixdybot/` — 14 informes de detalle ronda 1 (auditorías con cifras de
  logs, investigaciones verificadas, 3 arquitecturas, síntesis del juez).
- `investigacion-dixdybot/ronda2/` — 8 informes ronda 2; **`plan-revisado.md` = el plan
  vigente completo** (leer junto con los ajustes de la ronda 3).
- `DIXDYBOT-RONDA3-CONTRASTE.md` — arbitraje de los deep research externos (ChatGPT y
  Gemini) con fuente primaria: tarifas corregidas, Coexistence ajustado, regulación
  chilena, latencia medida. Detalle en `investigacion-dixdybot/ronda3/` (9 informes).
- `deep-research-report.md` (ChatGPT) y `deep-research-gemini.md` (Gemini) — los informes
  externos crudos; usarlos SOLO a través del arbitraje de la ronda 3.
- `investigacion-dixdybot/ronda4/` — **LA BIBLIOTECA DE PLANOS** (lectura de código real de
  8 repos: NanoClaw, Parlant, vocero-crm, Mastra, BuilderBot, boop-agent,
  whatsapp-agent-bridge, Chatwoot). **`planos-sintesis.md` = lectura OBLIGADA antes de
  construir E1-E5**: pieza→repo/archivo→etapa, 5 planos de oro, decisiones de conflicto
  resueltas, y la lista de lo que ningún repo resuelve (lo genuinamente nuestro).
- `investigacion-dixdybot/ronda5/` — **EL BLUEPRINT FUNDACIONAL**
  (`blueprint-fundacional.md` = EL documento rector de construcción: estructura de
  carpetas, stack verificado — Node 24 LTS + TS estricto nativo sin build + better-sqlite3
  + Hono + Zod, ~6 deps —, los 5 contratos núcleo en TypeScript, módulo ingesta/
  multimodal, orden de construcción S0-S5 mapeado a E0-E7, 16 NOes de sencillez) + los 4
  informes de sustento (stack, media en APIs de Meta, procesamiento IA de media con costos,
  media en repos + evidencia de pérdida real: video de estanques 20-jul respondido a
  ciegas, cotización de 30 baños confirmada por nota de voz ilegible 21-jul).
- `investigacion-dixdybot/ronda6-diseno/` — **EL DESIGN SYSTEM DIXDY**
  (`design-system-dixdy.md` = spec de diseño rectora: tokens, shell L invertida 240px,
  anatomía de las 5 vistas, decálogo anti-ruido ≤40 palabras de chrome) extraído del código
  real de Chatwoot/Typebot, de la app viva de Linear (medida con Playwright + capturas con
  el login de Alejandro) y de Intercom Fin. Regla: TODO el panel se construye desde esta
  spec — cero variaciones.
- Informe visual (artifact): https://claude.ai/code/artifact/002b8dd3-b637-408b-8628-eccee5e2a169
- **Prototipo navegable del panel** (v2 escritorio, iterándose con Alejandro):
  https://claude.ai/code/artifact/555843ca-9568-4c58-8518-afc3eca99e92

## Piezas clave a recordar

- El buzón de dudas (`dudas.js`) y el tarifario en código (`precios.js`) del bot vivo son
  los embriones de los caminos; `enviar.js`/`outbox.js`/`gating.js` se conservan.
- **NanoClaw** (MIT, 30k★) = arquitectura espejo de E1+E4; Parlant = modelo de datos de
  caminos; permission relay de Claude Code Channels = spec del pausa-y-pregunta.
- Editor de caminos: tarjetas + diff + botón Aprobar + historial; SIN canvas de nodos.
- Meta Business Agent no compite (FAQ genérico; "mixed responder" permite terceros);
  pitch: "el agente que OPERA el negocio".
- Pendiente externo: resultados del deep research de Alejandro en Gemini/ChatGPT
  (prompt entregado 23-jul) — verificar antes de integrar.
