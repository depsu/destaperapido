# Plan dixdybot REVISADO — 23-jul-2026 (tras la segunda ronda de investigación)

Revisión del plan E0-E6 de `sintesis-juez.md` (23-jul) contra los 7 informes nuevos
(tendencias-2027, noticias-julio-2026, papeleo-meta, referencias-diseno-logica-panel,
competidores-pago, web-o-app, mas-logica-reutilizable). Cada etapa marca qué **[CAMBIA]**,
qué es **[NUEVO]** y qué queda **[RATIFICADO]** respecto a ayer.

**Veredicto en una línea:** el plan resiste — la columna vertebral (evolución incremental,
gateway propio delgado, cerebro Claude tras una puerta única, caminos como diferenciador,
Mac mini hoy) sale RATIFICADA por toda la evidencia nueva; pero tres supuestos operativos
cambiaron (el "responder ~gratis" de la Cloud API muere el 1-oct, Anthropic ya intentó dos
veces medir `claude -p`, y el enforcement contra Baileys escaló), y eso obliga a ejecutar
más rápido en dos frentes (E1 y el papeleo Meta) y a ponerle fecha a la salida de Baileys.
No hay que repensar el plan: hay que apurarlo donde el mundo se movió.

---

## 1. Qué cambió respecto a ayer (resumen ejecutivo)

1. **[CAMBIA] E1 pasa a prioridad #1 explícita.** Anthropic anunció (14-may) mover
   `claude -p`/Agent SDK a un crédito mensual separado, lo pausó el 15-jun y prometió
   reintentarlo con aviso. El cerebro del bot vive de esa gracia. El failover
   suscripción→API deja de ser "etapa 1 en orden" y pasa a ser el seguro que se construye
   inmediatamente después del cinturón E0.
2. **[NUEVO] Papeleo Meta se adelanta de E4 a AHORA** (corre en paralelo a E0-E1): el
   expediente precargado convierte un ban de Baileys en horas de emergencia en vez de
   semanas, la verificación es el paso lento (12-72 h hábiles, hasta 14 días), y la IA
   hace ~70% del trabajo (Alejandro: ~45 min de clicks repartidos).
3. **[CAMBIA] E5 se rehace: de "Instagram" a "Canales oficiales de Meta"**, con fecha
   límite interna: **migración del número vivo a Cloud API vía Coexistence lista antes del
   30-sep-2026** (aprovecha los service messages aún gratis hasta el 1-oct y le gana al
   enforcement). Economía recalculada: responder deja de ser gratis el 1-oct pero es
   marginal (~CLP 5-15 mil/mes al volumen actual; cifras Chile antes del 1-sep). Instagram
   DM queda dentro de E5 y se monta en una tarde (Standard Access, sin App Review).
4. **[NUEVO] Fechas duras entran al plan** (calendario §2): 24-jul, 1-ago, 19-ago, 31-ago,
   1-sep, 30-sep (meta interna), 1-oct.
5. **[CAMBIA] E0 suma dos ítems:** circuit breaker de reconexión (los crash-loops son
   vector de ban verificado) y chequeo de que ningún script use Opus 4.7 fast por API
   (muere el 24-jul).
6. **[NUEVO] El UX del editor de caminos queda definido** (pregunta d): tarjetas con diff
   + botón Aprobar + historial, stepper vertical para multi-paso, chat con IA como entrada
   principal, **sin canvas** (React Flow táctil pobre; la muerte del Agent Builder de
   OpenAI valida la decisión). Detalle en §3.2.
7. **[NUEVO] Web/PWA/app queda decidido** (pregunta e): panel = PWA instalable en iPhone,
   push sigue por avisos-worker, **no habrá app nativa**; Cloudflare Access (gratis ≤50
   usuarios) como login de clientes en E6. Detalle en §3.1.
8. **[CAMBIA] E3 adopta tres piezas con nombre y apellido:** el *permission relay* de
   Claude Code Channels como spec del "pausa y pregunta" (responder también por WhatsApp
   con "si/no <código>"), *backtesting* contra conversaciones históricas al editar un
   camino (patrón Fin), y *validación al guardar* (patrón Decagon) — las tres sobre el
   replay/juez que ya existe, sin librerías nuevas.
9. **[NUEVO] E1 evalúa el Claude Agent SDK** como implementación del modo `cli` detrás de
   llm.js (sesión con `resume` por chat = adiós al re-armado manual del historial /
   HISTORY_LIMIT; `forkSession` para el gimnasio; `total_cost_usd` por mensaje). Con
   advertencia legal: producto para terceros = API key sí o sí (doc oficial jul-2026).
10. **[CAMBIA] E6 gana pricing y pitch:** tier entrada 4-6 UF/mes, completo 8-12 UF/mes
    (+IVA), setup casi regalado — banda baja del managed chileno (5-25 UF) siendo mejor
    producto. Pitch reposicionado frente al Meta Business Agent: "el agente que OPERA el
    negocio (cotiza→confirma→despacha→cobra)", nunca "un chatbot". Verificación del
    negocio DIXDY (paso lento del Tech Provider) arranca temprano.
11. **[NUEVO] E7 exploratoria: voz.** Avoca (agentes de voz para gasfitería/HVAC) levantó
    US$125M a valorización US$1.000M — un "recuperador de llamadas perdidas" en español
    que derive a WhatsApp es el siguiente paso natural del rubro urgencias 24/7. Solo
    carpeta de investigación; no se construye.
12. **[RATIFICADO×todo lo demás]** — lista completa en §6.
13. **Se retiran 2 afirmaciones refutadas** por la verificación: el "endurecimiento de
    Instagram DM del 27-abr" y el "in-app signup global del 1-jul". E5/IG se apoya SOLO en
    lo verificado directo en docs de Meta (papeleo-meta.md del 23-jul).

---

## 2. Calendario de fechas duras (nuevo, transversal)

| Fecha | Qué pasa | Qué hace DIXDY |
|---|---|---|
| **24-jul** | Muere Opus 4.7 fast en la API | Chequeo en E0: ningún script DIXDY debe llamarlo (migrar a 4.8 fast si aparece) |
| **1-ago** | Meta Business Agent empieza a cobrar por tokens (~US$0,04-0,05/conv) | Nada que construir; ancla de pricing para E6 |
| **19-ago** | Termina la promo +50% de límites de Claude Code | `llm-metricas.jsonl` (E1) ya debe estar midiendo para presupuestar el consumo del bot en septiembre |
| **31-ago** | Termina el precio intro de Sonnet 5 ($2/$10 → $3/$15) | Si el failover API va a usar Sonnet 5, probarlo con el juez ANTES de esta fecha |
| **1-sep** | Meta publica tarifas por país de los service messages | Recalcular el business case E5 con cifras Chile reales |
| **30-sep** | **Meta interna DIXDY**: migración Coexistence lista | El número vivo responde por Cloud API antes de que empiece el cobro y antes de que un ban decida por nosotros |
| **1-oct** | Fin del "responder gratis" en la ventana 24h de la Cloud API | Ya migrado; costo marginal presupuestado |

**Regla de contingencia (nueva):** la fecha del canal manda sobre el orden de etapas. Si el
30-ago E3 (caminos) viene atrasada, **E4+E5 se adelantan por encima de E3** — la migración
de canal no depende de los caminos (E4 depende de E1, no de E3) y E3 puede continuar
después. Lo que no se negocia es llegar al 30-sep con la salida de Baileys lista.

---

## 3. Decisiones que hoy se CIERRAN

### 3.1 Web vs app: **PWA, caso cerrado** (pregunta e)

- El panel del dueño y el del repartidor son **PWA instalables** en pantalla de inicio:
  iOS da push + badge + pantalla completa desde 16.4, iOS 26 abre por defecto como web
  app, y las web apps instaladas están exentas del borrado de datos a 7 días de Safari.
- **El push sigue por avisos-worker** (VAPID ya operativo): el panel :8789 va por
  Tailscale en HTTP y el push directo exige HTTPS — no se construye nada nuevo
  (`tailscale serve` con HTTPS queda anotado como opción, no como tarea).
- **No habrá app nativa**: US$99/año + revisión por update + Apple rechaza webs envueltas
  (guideline 4.2) + TestFlight caduca a 90 días. Si algún día se necesitara GPS en segundo
  plano o Live Activities (no está en E0-E7), la vía es Expo/React Native, no Swift.
- Vender dixdybot no requiere app: todos los competidores (respond.io, Wati, SleekFlow,
  Trengo, Chatwoot) son panel web con login. **Cloudflare Access (gratis ≤50 usuarios)**
  será el login de los primeros clientes en E6.

### 3.2 UX del editor de caminos: **lista de tarjetas + diff + Aprobar, sin canvas** (pregunta d)

Convergen tres evidencias: el mercado serio abandona el canvas (OpenAI mata Agent Builder
el 30-nov-2026; Intercom Fin separa Procedures en lenguaje natural del canvas; Sierra
describe "Journeys" en inglés simple; ManyChat va "lista primero, canvas opcional"), React
Flow es de segunda clase en táctil (el dueño opera desde iPhone), y el modelo de datos de
E3 (archivos versionados condición→acción) mapea 1:1 a tarjetas con historial y muy mal a
un grafo espacial (un camino aprendido en caliente no tiene coordenadas; en una lista
aparece arriba con badge "nuevo").

Patrón definitivo para la vista 🧠 Conocimiento (E2-E3):

- **Tarjeta por camino**, agrupadas por tema; las recién aprendidas arriba con badge
  "nuevo". Cada tarjeta: cuándo aplica / qué hace / desde cuándo / uso y cierres.
- **Todo cambio propuesto = diff con botón Aprobar** (patrón Dust Sidekick / el "enseñar"
  que el panel ya tiene): la edición conversacional del plan de ayer genera antes/después
  y un toque confirma (commit). Alejandro jamás ve el frontmatter.
- **Caminos multi-paso = stepper/cascada vertical** (la idea robable de Typebot: el grupo
  como pila vertical que se lee como conversación). Nada de nodos.
- **Canvas: a lo sumo vista de solo-lectura en desktop, algún día.** No se construye ahora.
- **Tematización barata:** DaisyUI (MIT, clases CSS sin JS) permite ordenar el look del
  dashboard vanilla actual sin reescribir en React; opcional en E2, nunca bloqueante.
  (assistant-ui / shadcn quedan anotados SOLO si E6 justificara reescritura Next.js.)

### 3.3 Amenaza Meta Business Agent: real, y se responde con posicionamiento, no con pánico (pregunta f)

Existe, es global desde el 3-jun, cobra desde el 1-ago (~US$0,04-0,05/conversación,
exento del cobro por mensaje de servicio — Meta se favorece a sí misma) y viene incluido
en tiers Premium para pymes: **el chatbot básico de FAQ ya es commodity regalado**. Lo que
exige apurar: **E1-E3, el foso** — el agente de Meta no cotiza con PDF, no habla con
Supabase ni con el repartidor, no registra cobros, no aprende los caminos del negocio ni
le pregunta al dueño. Además la plataforma de Meta soporta el **mixed responder model**
(agente de Meta + agentes de terceros + humanos con handoffs): dixdybot puede enchufarse
oficialmente en E5-E6 en vez de competir contra Meta. Y la política del 15-ene-2026
prohíbe los bots de propósito general pero **permite expresamente** los bots de negocio
con propósito: dixdybot es exactamente el tipo permitido. Argumento comercial extra: el
propio chatbot de soporte de Meta fue explotado en mayo para secuestrar cuentas — los
guardrails propios (tarifario fuera del LLM, precioCoherente, Guardián) se venden como
diferencial de seguridad. El backlash anti-IA (85% prefiere humano; Gartner: >40% de
proyectos cancelados a 2027) confirma que la pausa-de-tema + humano en el loop de E3 es
EL diferenciador, no un lujo.

---

## 4. Las etapas, revisadas

### Pre-etapa (paralela a E0-E1, desde esta semana) — "Expediente Meta" **[NUEVO — adelantado desde E4]**

Nada de esto toca el bot vivo; es papeleo + un Worker gratis. La IA hace ~70%; lo humano
son ~45 min repartidos en 1-3 días (gestión externa → la pide el Guardián, como siempre):

1. Meta Business Manager del negocio (datos legales reales) + app con caso de uso
   WhatsApp. **OJO verificado: el Business Manager que se use en Coexistence queda fijo
   para siempre para ese número** → se usa el BM del PROPIO cliente (destaperapido), que
   además es lo que permite operar con Standard Access sin App Review.
2. Número de prueba + token temporal → primer mensaje por Cloud API el mismo día (sandbox).
3. Worker CF `meta-buzon` (plantilla en el maestro, patrón timbre v2 del correo-worker):
   webhook verificado + cola en D1 + GET para polling del Mac. Sirve para WhatsApp e
   Instagram (dos endpoints).
4. System User + token permanente en `.env.local`; display name propuesto (aprobación
   minutos-48 h); 2-3 plantillas utility creadas por API (revisión ≤24 h).
5. Expediente de verificación del negocio precargado (PDF único: constitución + RUT
   coherente con el admin). La verificación NO es necesaria para responder (gratis e
   ilimitado responder a quien escribe primero; 250 conversaciones iniciadas/24 h sin
   verificar) — se lanza en paralelo porque es el paso lento y habilita escalar después.
6. La elegibilidad Coexistence ya se cumple (número con meses en la app WhatsApp
   Business); queda documentado el runbook de migración (§E5).

**Por qué ahora:** si Baileys muere mañana (bans permanentes en semanas reportados todo
2026), el expediente convierte la emergencia en horas; y si no muere, la migración del
30-sep ya tiene todo listo.

### E0 — "Cinturón de seguridad" (1-2 días) **[CAMBIA: +2 ítems]**

Todo lo de ayer intacto (commitear lo vivo, aviso de muerte silenciosa 401 + healthcheck,
backup de auth/, rotación de logs, dedup y topes persistentes, persona.md) más:

- **[NUEVO] Circuit breaker de reconexión:** los crash-loops (miles de conexiones/hora)
  son vector de ban verificado en 2026. Tras N reconexiones en M minutos, el bot se
  detiene solo, avisa por avisos-worker y espera intervención — mejor un bot detenido 1 h
  que un número baneado para siempre. (El backoff actual ayuda; el breaker lo remata.)
- **[NUEVO] Chequeo Opus 4.7 fast:** grep por `speed.*fast`/`opus-4-7` en scripts DIXDY
  antes del 24-jul; migrar a 4.8 fast lo que aparezca.

### E1 — "Una sola puerta al modelo" (3-4 días) **[CAMBIA: prioridad #1 + evaluación Agent SDK]**

Ayer era la etapa 1 en orden; hoy es **la prioridad #1 del plan** (el vaivén de Anthropic
de abril-junio demuestra que el metering de `claude -p` volverá en alguna forma; habrá
aviso, pero el seguro se construye antes del incendio):

- `src/core/llm.js` única puerta (cola, prioridades, timeouts por rol, métricas) — igual
  que ayer. Los 4 spawns adoptan la puerta en 4 commits reversibles.
- **Failover automático cli→api** — igual que ayer (brainApi con Haiku 4.5 ya escrito;
  solo cablear) **[NUEVO]** + probar **Sonnet 5 como candidato del failover
  conversacional** con el juez ANTES del 31-ago (precio intro $2/$10; enfocado en
  agentes; a $3/$15 una conversación de venta sigue costando centavos). La métrica decide
  Haiku vs Sonnet, no la corazonada.
- `claude setup-token` (1 año) + canal stable + minimumVersion — igual que ayer.
- **[NUEVO] Evaluación Claude Agent SDK como backend del modo `cli`** (mismo contrato
  `runLLM`, decidido con juez + llm-metricas, reversible): `resume` por session_id = un
  hilo persistente POR CHAT (hoy el bot re-arma historial a mano con HISTORY_LIMIT=60 y
  pierde el trato en chats largos — esto lo resuelve de raíz), `forkSession` para el
  gimnasio/replay, hooks PreToolUse in-process (guardián), `total_cost_usd` por mensaje.
  Cuidados verificados: el paquete TS se rige por Commercial Terms (no OSS), la V2
  session API fue removida (no diseñar sobre `createSession`), y la doc legal exige API
  key para productos de terceros — para el negocio propio es la misma zona gris tolerada
  que `claude -p`; para E6, API key obligatoria (sin cambio).
- **[NUEVO, liviano] Contratos MCP-compatibles:** las herramientas internas (tarifario,
  entregas, cotizar) se diseñan con contratos exponibles como MCP server sin reescritura.
  MCP ganó como estándar (Linux Foundation, dic-2025; ~97M descargas/mes) — es el seguro
  anti-lock-in. No se monta ningún server hoy; solo se cuida la forma.
- **[NUEVO] Medición con fecha:** `llm-metricas.jsonl` operativo antes del 19-ago (fin de
  la promo +50%) para presupuestar el consumo del bot en septiembre con números.

### E2 — "El conocimiento sale del código" (4-5 días) **[CAMBIA: +embudo, UX definido]**

Igual que ayer (tarifario.json + persona.md + ajustes.json + vistas Conocimiento v1 y
Ajustes v1) más:

- **[NUEVO] Vista embudo por etapa** en el panel (patrón Intercom Fin, primer feature
  robado a competidores): chat → cotización → entrega → cobro desde envios.jsonl (el
  evento "cobro" del plan de ayer completa el ledger). Que el dueño VEA qué vende el bot.
- **[NUEVO] La vista Conocimiento nace ya con el patrón §3.2** (tarjetas; nada de canvas,
  para no construir dos veces). DaisyUI opcional para tematizar, nunca bloqueante.

### E3 — "Caminos v1" (2 semanas, el corazón) **[CAMBIA: +3 piezas con spec]**

Igual que ayer (caminos .md+frontmatter, selección por turno ≤8, migrar-reglas 68→20-30,
TIPOS.CAMINO, pausa de TEMA no de chat, respuesta enlatada inmediata, push, aprendizaje en
caliente con reanudación, conflictos en 3 capas, git, edición conversacional, métricas,
flag CAMINOS_ON con gate del juez ≥4,0) más:

- **[NUEVO] Permission relay estilo Channels** como segunda superficie de respuesta del
  dueño: el push de una duda lleva un **código de 5 letras tecleables**; Alejandro puede
  contestar desde el panel O por su WhatsApp con "si abcde / no abcde" (+texto libre para
  la regla); **primera respuesta gana**; campos del cliente tratados como no confiables.
  Es la spec oficial de Anthropic robada sin adoptar Channels (~50 líneas sobre el
  WhatsApp de Alejandro que ya existe). Channels como runtime queda descartado (preview +
  una sesión = una cola: mezclaría los chats de N clientes).
- **[NUEVO] Backtesting al editar** (patrón Fin): además del replay de los 6-10 dorados,
  al editar un camino se re-juegan las conversaciones históricas que lo habrían gatillado
  (matching sobre conversaciones.jsonl) y el juez compara antes/después. Reusa replayChat;
  cero librerías.
- **[NUEVO] Validación al guardar** (patrón Decagon): lint del camino (frontmatter
  completo, cero cifras en el cuerpo, ámbito válido, sin solaparse con `retirado`) ANTES
  de la detección de conflictos. Barato y mata errores tontos.
- **[Referencia de diseño]** Para chats largos, el modelo de memoria de Mastra
  (observational log que reemplaza historial crudo) es la solución de diseño al
  HISTORY_LIMIT **si** E1 no adopta el Agent SDK (cuyo `resume` lo resuelve por sesión).
  Una de las dos vías, decidida en E1; no se construyen ambas.

### E4 — "Canal como enchufe" (1-1,5 semanas) **[CAMBIA: ventana+plantillas de primera clase]**

Igual que ayer (mensaje.js/convId, turno.js, canales/whatsapp/, identidad.json, outbox con
campo canal, el panel consume la API del bot) más:

- **[CAMBIA] La interfaz Canal modela ventana-de-respuesta y plantillas como conceptos de
  primera clase:** `politica.ventanaRespuesta` (ya estaba) + **`enviarPlantilla(convId,
  plantilla, vars)`** (nuevo, no-op en Baileys). Motivo: en la Cloud API responder fuera
  de la ventana de 24 h EXIGE plantilla pagada — el seguimiento de cotización abandonada
  (feature E5) depende de esto. Se diseña en E4 para no re-abrir la interfaz en E5.
- **[NUEVO, referencia] NanoClaw (MIT, 30k★)** es el plano E1+E4 ya construido y legible
  en una tarde: host router + inbound.db/outbound.db con UN escritor por archivo + sesión
  por chat + adaptadores (Baileys v7 incluido). No se adopta (la evolución incremental
  sigue); se usa como espejo para validar el diseño del turno/router y como cantera si el
  jsonl mostrara contención (colas SQLite un-escritor). La disciplina "único escritor" del
  plan de ayer queda ratificada por el proyecto Agent-SDK más grande que existe.

### E5 — "Canales oficiales de Meta" (2ª quincena de septiembre) **[REHECHA]**

Ayer: "Instagram por la puerta oficial". Hoy: **la salida de Baileys del número vivo +
Instagram**, con fecha.

1. **WhatsApp Cloud API vía Coexistence (la pieza nueva central):**
   - El número actual (meses en la app WhatsApp Business: califica) se conecta a la Cloud
     API escaneando un QR — minutos, conserva la app en el teléfono y sincroniza hasta 6
     meses de chats 1:1. **La sesión Baileys muere en ese momento** (los dispositivos
     acompañantes se desvinculan): el corte es Baileys→wa-cloud, no una convivencia.
     **No se diseña nada que dependa de Baileys + Cloud API a la vez en el mismo número**
     (whatsmeow #916: terreno pantanoso).
   - `canales/whatsapp-cloud/adaptador.js` contra el Worker `meta-buzon` (polling timbre
     v2, sin puertos abiertos en el Mac). Referencias: provider-meta de BuilderBot (MIT) y
     el patrón de instancias conmutables de Evolution API (copiar el patrón, no adoptar).
   - Reglas operativas de Coexistence que se documentan en MANUAL.md: abrir la app en el
     teléfono al menos cada 13-14 días (queda pieza viva, igual que hoy), tope 20 msg/s
     (sobra), sin grupos por API (el bot no usa), sin OBA/verificación estándar (para un
     respondedor, irrelevante).
   - **Qué se gana:** cero riesgo de ban por ToS, webhooks confiables, y se acaban Bad
     MAC / 440 / QR / sanación de sesión — la mitad del cinturón E0 se vuelve innecesaria.
   - **Economía (recalculada, supuesto roto de ayer):** desde el 1-oct cada respuesta en
     ventana 24 h se cobra a tarifa utility del país (referencias hoy US$0,01-0,025;
     Chile utility actual US$0,0113). Al volumen actual (~300-600 respuestas/mes) son
     **~CLP 5-15 mil/mes** — marginal frente a un destape, pero ya no $0. Cifra final con
     las tarifas Chile (se publican antes del 1-sep). La **ventana de 72 h por
     Click-to-WhatsApp sigue gratis**: las campañas CTWA (DIXDY ya opera Ads) pasan a ser
     palanca de costo Y de atribución (el referral llega en el webhook — cosa que Baileys
     no da limpio).
2. **Instagram DM (si el negocio activa su cuenta):** una tarde, sin esperas de Meta —
   cuenta profesional + producto Instagram en la misma app + login del dueño (scopes
   instagram_business_basic + manage_messages) + webhook al mismo Worker. Standard Access
   sin App Review mientras la cuenta sea propia/administrada. Reglas: solo responder,
   ventana 24 h, divulgar que es bot, HUMAN_AGENT jamás. IG **nunca** por vía no oficial.
   (Las afirmaciones refutadas del 27-abr no se usan; esto viene de docs de Meta directas.)
3. **Features de competidores que entran aquí:** seguimiento de cotización abandonada con
   plantilla utility fuera de ventana (~CLP 11/mensaje — seguimiento.js ya existe, solo
   cambia el transporte) y atribución CTWA en envios.jsonl.
4. **Baileys no muere como código:** queda como rampa de entrada de clientes nuevos
   (día 1 = chip + app + Baileys, cero papeleo, bot vivo en horas) y fallback documentado.
   El patrón operativo por cliente: Baileys día 1 → expediente precargado esa semana →
   los 7 días de Coexistence corren solos → migración al validar, en una tarde.

### E6 — "dixdybot producto" (continuo) **[CAMBIA: pricing, pitch, papeleo DIXDY]**

Igual que ayer (promoción al maestro como `dixdybot/`, datos del cliente solo en el clon,
docs/24 actualizado, cliente nuevo = clonar + formulario, API key por cliente obligatoria)
más:

- **[NUEVO] Pricing:** tier entrada **4-6 UF/mes** (~$160-240 mil CLP +IVA), tier completo
  **8-12 UF/mes** (~$315-475 mil CLP +IVA), setup casi regalado. Entra en la banda baja
  del managed chileno real (5-25 UF/mes; casos publicados 5,95-17,85 UF) siendo mejor
  producto, con margen alto (cerebro por suscripción/API a centavos + canal ~CLP 5-15
  mil/mes). El Meta Business Agent (~US$0,05/conv) es el ancla narrativa: eso compra un
  contestador de FAQ; dixdybot opera el negocio.
- **[NUEVO] Pitch:** "el agente que opera el negocio" — cotiza→confirma→despacha→cobra,
  con el dueño en el loop (E3). Nunca "chatbot". Es la tesis que financian a16z/Sequoia
  (presupuesto de TRABAJO, no de software) y la defensa exacta contra el commodity de
  Meta. El backlash anti-IA se responde con el humano-en-el-loop como feature de venta.
- **[NUEVO] Papeleo producto:** la **verificación del negocio DIXDY** (paso lento del
  programa Tech Provider) arranca al inicio de E6, no al final. Con 1-4 clientes NO hace
  falta Tech Provider (Standard Access con la app en el BM de cada cliente); Embedded
  Signup + App Review recién para el onboarding self-service.
- **[NUEVO] Higiene:** API keys por cliente **con expiración configurable** (feature nueva
  de la API de Claude, jul-2026) + tokens de caché ya no cuentan para rate limits (abarata
  prompts largos de persona+caminos por API). Login de paneles de clientes: Cloudflare
  Access gratis ≤50 usuarios.
- **[Backlog E6]** (features de competidores que necesitan volumen): A/B de mensajes de
  cotización (Treble) y agenda de citas/visita técnica en chat. Con ~4 chats/día aún no
  pagan su construcción; se anotan, no se construyen.

### E7 — "Voz" (exploratoria, NO se construye) **[NUEVA]**

La señal más fuerte del rubro: Avoca — agentes de voz para gasfitería/HVAC que contestan
llamadas perdidas y agendan — levantó US$125M a valorización US$1.000M (abr-2026, 800+
clientes). Para un negocio de urgencias 24/7, un **recuperador de llamadas perdidas en
español que derive a WhatsApp** ("no pudimos contestar, ¿le cotizamos por acá?") es el E7
natural: convierte la llamada perdida (hoy venta muerta) en un chat donde dixdybot ya
opera. Acción hoy: SOLO carpeta `investigacion-dixdybot/voz/` con esta evidencia; se
revisa cuando E5-E6 estén vivos. Agentic commerce (ACP/AP2/x402): inmaduro y replegándose
— vigilar sin construir; el sitio ya avanza lo único accionable (precios claros y datos
estructurados = negocio legible para agentes, trabajo SEO que ya se hace).

---

## 5. Respuestas directas a las preguntas del encargo

- **(a) ¿Algo invalida una decisión?** Ninguna decisión de fondo. Un supuesto económico
  (E5 ~gratis) quedó roto → recalculado y sigue barato; una urgencia cambió de grado (E1
  por el vaivén de Anthropic; salida de Baileys por enforcement). Canal, cerebro, panel,
  caminos, despliegue y producto: ratificados con mejoras puntuales.
- **(b) ¿El onboarding Meta cambia E4-E5?** Sí: el papeleo se adelanta a HOY (pre-etapa),
  E5 se rehace alrededor de Coexistence con fecha 30-sep, y E4 gana `enviarPlantilla` +
  ventana como primera clase. El orden E0→E6 se mantiene, con la regla de contingencia de
  que la fecha del canal manda sobre E3 si hay atraso.
- **(c) ¿Qué features de competidores entran?** Embudo por etapa (E2), backtesting +
  validación al guardar (E3), seguimiento de cotización abandonada con plantilla utility +
  atribución CTWA (E5), pricing y reporte de outcomes (E6), A/B y agenda (backlog E6).
- **(d) ¿UX del editor definido?** Sí: tarjetas + diff + Aprobar + historial; stepper
  vertical; chat con IA como entrada; sin canvas (§3.2).
- **(e) ¿Web/PWA/app decidido?** Sí: PWA + push por avisos-worker; sin app nativa;
  Cloudflare Access en E6 (§3.1).
- **(f) ¿Meta Business AI exige apurar algo?** Existe y cobra desde el 1-ago. Exige apurar
  el FOSO (E1-E3) y afila el pitch de E6; no cambia la arquitectura. El mixed responder
  model convierte a Meta en plataforma donde dixdybot se enchufa, no solo en competidor
  (§3.3).

## 6. Lo que la evidencia nueva RATIFICA (sin cambio)

1. **Evolución incremental del bot vivo** (nada de reescritura ni motor paralelo) — nada
   la contradice; NanoClaw es espejo de referencia, no cambio de rumbo.
2. **Gateway de canales propio y delgado; copiar patrones, no adoptar plataformas** — la
   muerte del Agent Builder de OpenAI, la licencia de n8n (prohíbe embeber/revender), la
   licencia multi-tenant de Dify (chocaría con E6) y los markups 30-50% de los SaaS pyme
   la refuerzan por los cuatro costados.
3. **Caminos E3 con pausa-de-tema + humano en el loop como diferenciador** — el patrón
   ganador del mercado es idéntico (Fin Procedures, Decagon AOPs, Ada Playbooks), nadie
   tiene el aprendizaje en caliente, y el backlash anti-IA lo vuelve argumento de venta.
4. **Cerebro Claude tras llm.js única puerta con failover cli→api** — el vaivén de
   Anthropic lo confirma como EL seguro correcto (cambia la urgencia, no el diseño).
5. **Baileys endurecido hoy como rampa + Cloud API oficial como destino** — ratificado,
   ahora con fecha (30-sep) y ruta concreta (Coexistence).
6. **Instagram SOLO por vía oficial** — ratificado (Standard Access, una tarde, cuenta
   administrada; jamás no-oficial).
7. **Mac mini hoy / VPS recién con 2+ clientes** — ratificado (el Mac es el servidor; el
   dueño opera por iPhone/PWA; nada de Electron/menubar).
8. **API key por cliente en E6, sin excepción** — reforzado por la doc legal del Agent
   SDK y las keys con expiración.
9. **Precios y validaciones fuera del LLM** (tarifario.json + precioCoherente como
   segunda muralla) — el exploit del chatbot de Meta lo convierte además en argumento
   comercial.
10. **WhatsApp como canal primario en LATAM; la abstracción E4 basta como cobertura** —
    RCS crece pero no toca a la pyme chilena; Google no tiene producto ahí.
11. **Pausa-y-pregunta con respuesta enlatada inmediata + push + escalada 30 min** — el
    permission relay le agrega superficie (WhatsApp del dueño), no le cambia el diseño.
12. **DeepEval se imita, no se adopta; el juez propio manda** — backtesting y validación
    entran sobre replayChat/juez existentes, cero stack nuevo.

## 7. Riesgos actualizados

1. **Ban de Baileys antes de la migración** (ventana jul-sep): mitigado por E0 reforzado
   (circuit breaker) + expediente precargado desde YA (emergencia = horas). Es el riesgo
   que justifica la pre-etapa.
2. **Anthropic reactiva el metering con poco aviso**: mitigado por E1 primero (failover
   probado con juez antes del 31-ago). Presupuesto post-promo se decide con
   llm-metricas.jsonl, no a ciegas.
3. **Slippage de E3 contra la fecha del canal**: regla de contingencia — E4+E5 pasan por
   encima; E3 se retoma después.
4. **Tarifas Chile peores que la referencia** (se publican antes del 1-sep): incluso al
   doble (US$0,025) el canal cuesta ~CLP 15 mil/mes al volumen actual; si el volumen se
   multiplica, el costo crece con las ventas (aceptable por diseño).
5. **Coexistence tiene letra chica operativa** (app cada 13-14 días, BM fijo para
   siempre): se documenta en MANUAL.md y se elige el BM del cliente con esa conciencia.
6. **Meta Business Agent mejora más rápido de lo previsto**: vigilancia trimestral; la
   defensa estructural es la integración profunda (E2-E4) y el mixed responder model
   permite coexistir en vez de competir frontalmente.
