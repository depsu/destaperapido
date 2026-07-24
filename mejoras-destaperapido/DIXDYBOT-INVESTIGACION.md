# DIXDYBOT — Investigación profunda y plan de rediseño

**Fecha:** 23 de julio 2026 · **Cómo se hizo:** 19 agentes de IA en 4 oleadas — 5 auditaron
el código vivo del bot línea por línea (incluyendo logs reales), 5 investigaron en la web
(GitHub, docs de Meta y Anthropic, papers), 5 verificadores adversariales trataron de
refutar cada hallazgo, y 3 arquitectos + 1 juez diseñaron y compararon planes de rediseño.
Los 14 informes completos están en `investigacion-dixdybot/`.

---

## 1. Diagnóstico: por qué pasa cada cosa (con evidencia, no con teorías)

### 1.1 "El bot queda ciego" — causa MIXTA, ya casi domada, pero sin alarma

- Entre el 6 y el 11 de julio los logs registran **81.917 desconexiones en 5 días**
  (un bucle de reconexión propio sin espera progresiva). Tras los arreglos de esa semana,
  hoy el bot se cae solo **6-7 veces al día y se recupera en 2 segundos**. Esa parte está resuelta.
- Lo que sigue vivo es el **"Bad MAC"** (candado de cifrado corrupto: el mensaje llega pero
  es indescifrable → invisible). Es un defecto conocido de Baileys, documentado en 36 issues
  de GitHub; la causa raíz es la migración "LID" de WhatsApp. Solo el 22 de julio hubo
  **2.631 casos**. La auto-sanación que ya construimos es exactamente el parche que usa la
  comunidad.
- **El hoyo más peligroso hoy:** si WhatsApp cierra la sesión (error 401), el proceso queda
  **vivo pero mudo, y nadie avisa**. No existe ninguna alarma de "bot ciego". Eso se arregla
  con un latido al avisos-worker (ya tenemos esa infraestructura).
- **Riesgo operacional grave encontrado:** los arreglos críticos de conexión de los últimos
  días están **sin commit en git** (7 archivos). Un `git checkout` accidental los borraría.

### 1.2 "Mensajes duplicados" — causa MIXTA, mitigada con riesgo residual

- Duplicados reales al cliente: el vigilante de sanación **reenviaba mensajes que SÍ habían
  llegado**, porque los acuses de ciertos chats (@lid) llegan tarde y por otro canal.
  Desde el 11 de julio hubo 25 reenvíos, hasta 5 al mismo chat. Ya mitigado (espera de 180s,
  máximo 1 reenvío, criterio de presencia), pero el riesgo residual existe.
- Duplicados solo en el panel: el **eco de los envíos propios** se procesaba como mensaje
  nuevo (incidente del 22 de julio, corregido).

### 1.3 "El bot se pausa solo" — era un BUG nuestro (corregido) + pausas por diseño sin explicación

- El mismo eco de arriba contaba como "el dueño contestó" y con la regla de 3 strikes
  forzaba **pausa indefinida chat tras chat**. Corregido.
- Además hay pausas **por diseño** (soporte de cliente antiguo, topes, 30 min tras tu
  mensaje manual) que el panel **no explica** — por eso parecen misteriosas. Falta una vista
  "por qué está pausado este chat".

### 1.4 "Es un enredo entrenar al bot" — el diagnóstico más importante

El sistema aprende, pero **acumula parches planos en vez de conocimiento estructurado**:

- **68 reglas activas se inyectan TODAS a TODOS los chats**, sin condición ni ámbito. El
  propio análisis interno admite "dilución": bajo presión, las reglas del montón pesan menos.
- **Evidencia dura del "aprende algo y choca con otra cosa":** la política del IVA dio 3
  vueltas en 4 días (reglas del 17, 20 y 21-jul hoy apagadas), y **el conflicto sigue vivo
  HOY**: la persona del bot ordena cotizar "$190.400 IVA incluido" mientras 7 reglas y el
  tarifario mandan "neto". Se resuelve por azar de posición en el prompt.
- El destilador automático llegó a poner **reglas corruptas en producción** (un `[]`, un
  bloque de código) y reglas con **precios de ejemplo que el bot cobró como reales** ("el
  140 fantasma", 2 veces).
- **No hay** detección de conflictos, ni historial de versiones, ni tests de regresión: al
  activar una regla, nada verifica que no rompa lo que ayer funcionaba.
- Dato revelador: la mejora real medible (nota del juez 2,44 → 4,0) vino sobre todo de
  **mover conocimiento del prompt a código con tests** (el tarifario en `precios.js`), no
  del loop de reglas. Esa es la lección que funda los "caminos".
- El entrenamiento está repartido en **5 entradas distintas** del panel y las reglas se
  administran en 2 pantallas con vocabulario distinto ("Deshacer/Reactivar" vs
  "Apagar/Prender"). Nadie puede ver la persona del bot ni el tarifario desde el panel.

### 1.5 Panel y arquitectura — lo revuelto tiene explicación

- Son 3 procesos (bot, panel, aprendizaje) que se comunican **solo por 17 archivos JSON en
  disco**, sin árbitro: las carreras entre procesos ya causaron incidentes (16 y 22-jul).
- El panel (1.897 líneas + 191 KB de HTML) **re-implementa** lógica del bot (detección de
  comuna DISTINTA a la del bot → pueden mostrar cosas diferentes del mismo chat).
- La ficha de un cliente concentra ~25 acciones; el precio se edita en 3 lugares de la
  misma tarjeta; conviven 2 embudos que no calzan (5 etapas atrás, 4 columnas adelante).
- **El jid de WhatsApp es la clave primaria de TODO** → nada funcionaría con Instagram tal
  cual. No existe abstracción de canal.

---

## 2. Tu idea de los "caminos": está validada, y tiene nombre (casi)

Tu idea combina **dos corrientes reales** del estado del arte:

1. **Rutas de negocio en lenguaje natural** — la industria las llama *playbooks*
   (Dialogflow CX de Google), *guidelines y journeys* (Parlant), *Agent Operating
   Procedures* (Decagon, que logra 70-80% de casos resueltos sin humano), *flows*
   (Rasa CALM). Reglas del tipo "condición → acción" escritas como se habla, que el sistema
   selecciona por relevancia en cada turno (nunca las 68 juntas — eso evita la dilución).
2. **Aprendizaje en el momento con humano en el loop** — un paper de 2025 (ARIA,
   arXiv:2507.17131) implementa casi exactamente tu bucle: el agente detecta que le falta
   conocimiento, pregunta al experto, guarda la regla con fecha resolviendo conflictos…
   y está **en producción en TikTok Pay con 150 millones de usuarios**. Tu intuición
   compite con lo que hacen los grandes.

**Lo genuinamente tuyo:** el aprendizaje **EN CALIENTE** (pausa → pregunta → camino nuevo →
el mismo chat se reanuda). Los vendors aprenden de escalaciones post-mortem. **Ningún
proyecto open source entrega ese bucle completo** — verificado repo por repo. Esa pieza hay
que construirla, pero es pequeña si los caminos son datos (archivos markdown/YAML) y el
compilador es Claude.

**Mejoras del estado del arte a adoptar:**
- Caminos como archivos con estructura mínima (condición, acción, requiere, vigencia) —
  git regala el versionado y el rollback que Decagon vende caro.
- **Detección de conflictos al crear cada camino** (compararlo con los existentes ANTES de
  guardar — lo que le faltó a las 68 reglas).
- **Cifras siempre desde el dato del camino, nunca redactadas por el modelo** (mata el "140
  fantasma" para siempre — es la generalización de lo que ya hace `precios.js`).
- **Escenarios dorados como candado**: cada camino liga conversaciones de prueba que deben
  seguir pasando; un camino nuevo que rompe una vieja no entra.
- **Pausa de TEMA, no de chat** (idea ganadora del panel de arquitectos): si falta el precio
  de "baño por 1 día", el bot lo dice honesto ("déjame confirmarlo, te escribo en unos
  minutos"), te llega un push, y MIENTRAS TANTO sigue juntando comuna y fecha. En un rubro
  de urgencia no se puede congelar la venta.
- **Arranque en frío**: minar los chats reales + las 68 reglas actuales con Claude para
  proponer los primeros 20-30 caminos, y tú los apruebas en lote.
- Métricas por camino: usos, tasa de cierre, huecos detectados (tu "cascada" visible).

---

## 3. La conexión WhatsApp: veredicto verificado

- **Cambiarse a otra librería no oficial NO arregla nada**: whatsapp-web.js, WPPConnect y
  WAHA van sobre el mismo protocolo reverse-engineered y sufren los mismos males (hay
  reportes de cuentas bloqueadas con 7 mensajes/hora). Baileys sigue siendo la referencia
  (10.233 estrellas, actividad diaria).
- El riesgo de ban con cualquier vía no oficial es **real e impredecible**: 5 bots baneados
  en una semana según un issue de oct-2025, dos con 3+ años funcionando. Nuestro perfil
  solo-respondedor es el de menor riesgo, pero nunca cero.
- **La joya de la investigación: la API oficial de Meta (Cloud API) hoy es casi gratis para
  nuestro caso.** Desde jul-2025 cobra por plantilla, pero **responder dentro de la ventana
  de 24 horas es gratis e ilimitado** (texto, fotos, PDF), y los chats que llegan por
  anuncio click-to-WhatsApp dan 72 horas gratis. Nuestro flujo (el cliente escribe, el bot
  responde y cotiza) costaría **~$0**; con avisos al repartidor y recordatorios,
  **menos de $10.000 CLP/mes**. A cambio: **cero ban, cero Bad MAC, cero QR, cero "ciego"**,
  entrega por webhook (un Worker de Cloudflare, infraestructura que ya dominamos).
- Desde may-2025 existe **"Coexistence"**: el mismo número puede seguir en la app WhatsApp
  Business del teléfono Y en la API a la vez.
- **Recomendación por etapas:** hoy endurecer Baileys (commit, pin de versión, backup de
  sesión, alarma de ciego); en paralelo abrir la cuenta Cloud API; y el rediseño se hace
  agnóstico del canal para enchufar la oficial cuando esté lista. Instagram después, por la
  misma Graph API de Meta.

## 4. Instagram: solo por la vía oficial

- Se automatiza legalmente con la **Messaging API oficial**. Desde 2024 ya no exige página
  de Facebook: cuenta profesional + 2 permisos + webhooks. Si la app solo atiende cuentas
  que DIXDY administra, **no necesita App Review** (eso es solo para venderlo como SaaS a
  terceros, y son 5-10 días hábiles de verificación cuando llegue el momento).
- Igual que WhatsApp oficial: el bot **solo responde** (el cliente escribe primero), ventana
  de 24 horas. Encaja perfecto con nuestro modelo solo-respondedor.
- Las vías no oficiales de Instagram tienen **15-30% de suspensión anual** y Meta ya emitió
  avisos legales contra esas librerías. Descartadas.
- Bonus: WhatsApp oficial e Instagram comparten la misma plataforma de Meta → un solo
  webhook, un solo patrón.

## 5. "Todo por Claude Code, no por APIs" — la validación honesta

Esto había que validarlo y la respuesta tiene matices importantes:

- **Técnicamente es oficial y sólido**: `claude -p` headless está documentado por Anthropic
  (salida JSON tipada, sesiones, costo por invocación). Para servidores existe
  `claude setup-token` (token de 1 año, no caduca como el login normal).
- **PERO los términos de Anthropic dicen**: los límites Pro/Max asumen "uso ordinario e
  individual"; quien construye **productos o servicios debe usar API key**, y está
  **prohibido** enrutar peticiones de terceros por una suscripción. Traducción: el bot de
  TU propio negocio con TU Max es zona gris tolerada hoy (no se encontró ningún caso de
  baneo por usar el CLI oficial a bajo volumen con suscripción propia); **un dixdybot
  vendido a otras empresas colgando de tu Max sería zona prohibida** → cada cliente con su
  API key.
- **El plan sensato (validado por el juez):** hoy seguir con `claude -p` + Max, pero con un
  **envoltorio de failover automático**: si la suscripción se agota o el servicio cae, el
  mismo binario conmuta solo a `ANTHROPIC_API_KEY` (la API de pago) — es trivial porque la
  API key siempre gana si está presente, y `claude -p` emite eventos tipados que distinguen
  "límite agotado" de "caída transitoria". Anthropic también soporta Bedrock/Vertex como
  respaldo del respaldo. Con eso queda resuelto tu "¿y si se cae Anthropic?".
- **A futuro**: el tráfico conversacional (responder chats, el 90% del volumen) conviene
  evolucionarlo a llamadas API delgadas con caché — a nuestro volumen costaría **~$27-40
  USD/mes con Haiku o ~$80-120 con Sonnet** — y reservar Claude Code/Max para lo que de
  verdad brilla: el trabajo agéntico tuyo (entrenar, crear caminos, administrar, aprender).
  Claude Code sigue siendo el cerebro del SISTEMA; la API es solo el músculo barato de
  responder mensajes.
- **Gotcha crítico encontrado**: una versión futura del CLI hará default un modo que NO lee
  la suscripción (`--bare`), y el CLI se auto-actualiza → hay que **fijar la versión** del
  CLI del bot o un update silencioso lo dejaría mudo.
- **Dato feliz**: Anthropic lanzó en marzo 2026 **"Claude Code Channels"** (Telegram,
  Discord, iMessage nativos) y hay un canal WhatsApp comunitario MIT en el marketplace
  oficial — el patrón "cerebro = Claude Code local" ahora tiene carril oficial. Vamos en la
  dirección correcta.

## 6. ¿Mac mini o VPS?

- Claude Code corre en **Linux como plataforma de primera clase** (Ubuntu/Debian, 4 GB RAM).
  En un VPS se pierde poco: el Keychain de Mac (las credenciales quedan en un archivo
  protegido), launchd (se reemplaza por systemd) y el ecosistema ya montado en tu Mac.
- **Veredicto del juez: Mac mini hoy, VPS recién cuando haya 2+ clientes** (y ahí con API
  key, no suscripción). Razones: todo el sistema DIXDY ya vive en el Mac (launchd, scripts,
  rondas), la sesión de WhatsApp es portable, y tu plan de Mac mini con batería/solar +
  datos móviles cubre el riesgo real (cortes de luz/internet) a costo bajo. La migración a
  VPS es un proyecto conocido y documentado para cuando toque, no una urgencia.

## 7. Qué reutilizar de la comunidad (censo verificado repo por repo)

| Proyecto | Qué es | Qué le tomamos |
|---|---|---|
| **Parlant** (18.2k ⭐, Apache-2.0, vivo) | El framework más parecido a los "caminos": guidelines condición→acción, journeys, relaciones entre reglas, selección por turno | Su **modelo de datos**, no su motor (asume API propia). Es el plano de cómo estructurar caminos |
| **vocero-crm** (MIT, en español, vivo) | CRM de WhatsApp con "Laboratorio de auto-evaluación": clientes simulados vs bot real en sandbox, juez con nota 0-100, delta histórico | El **patrón del gimnasio** soñado — legible entero en una tarde |
| **BuilderBot** (2.9k ⭐, MIT, comunidad hispana) | Framework con la abstracción *Provider*: mismo flujo sobre Baileys, Meta Cloud API o Twilio | La **costura exacta** "WhatsApp no-oficial hoy, oficial mañana" |
| **crisandrews/claude-whatsapp** (MIT, marketplace oficial) | Canal WhatsApp para Claude Code Channels | El **contrato de canal** (reply, unreplied, catch_up…) |
| **Chatwoot** (34.7k ⭐, open-core, vivo) | Bandeja omnicanal con WhatsApp+Instagram oficiales y handoff IA-humano | El **mapa de ruta** si DIXDY escala a 5+ clientes con atención humana; hoy pesa demasiado (Rails+Postgres+Redis) |

También: el patrón de arquitectura tiene nombre — *Channel Adapter → mensaje canónico → bus
→ cerebro → outbox por canal* (Enterprise Integration Patterns). Y nuestro bot **ya tiene el
embrión**: `outbox.js`, `gating.js`, `brain.js` y el buzón de dudas son las piezas; volverse
multi-canal es refactor, no obra nueva.

**Veredicto sobre adoptar una plataforma entera: NO.** El diferencial de dixdybot es el
cerebro (caminos + pausa-y-aprende) y ninguna plataforma lo trae. Gateway de canales propio
y delgado, robando planos de los de arriba.

---

## 8. El plan (síntesis del juez, 3 arquitecturas comparadas)

**Columna vertebral: evolución incremental** — el bot vivo ES dixdybot v0 y se transforma
por etapas en el mismo repo, sin sistema paralelo, porque vende HOY y romperlo cuesta plata.
Se injertan las mejores piezas de las otras dos propuestas (salida tipada del cerebro, canal
de simulación para el gimnasio, "un solo escritor" de los datos, Etapa 0 exhaustiva).

- **E0 — Cinturón de seguridad (1-2 días):** commitear los 7 archivos con fixes vivos, pin
  de Baileys 6.7.23 y del CLI de Claude, backup atómico de la sesión, dedup persistente,
  **alarma de "bot ciego"** vía avisos-worker (latido cada X min).
- **E1 — Una sola puerta al cerebro (3-4 días):** todas las llamadas a Claude pasan por un
  `llm.js` único (hoy hay 4 distintas, una sin timeout) con **failover automático
  suscripción → API key**, `setup-token`, y medición de costo por invocación.
- **E2 — Conocimiento como datos (4-5 días):** persona, tarifario y reglas salen del .env y
  del código a archivos versionados en git; nace la vista **"Conocimiento"** del panel donde
  POR FIN ves y editas qué sabe tu bot. De paso se salda el conflicto del IVA vivo hoy.
- **E3 — Caminos v1 (2 semanas):** el corazón. Esquema de camino (condición → acción →
  requiere → vigencia → escenarios dorados), arranque en frío destilando las 68 reglas + los
  chats reales en 20-30 caminos que apruebas en lote, **pausa de tema + push + aprendizaje
  en caliente**, detección de conflictos al guardar, y el chat del panel para editar caminos
  conversando ("sube los precios 10%" → muestra el antes/después → confirmas → commit).
- **E4 — Canal como enchufe (1,5 semanas):** identidad de conversación abstracta (muere el
  jid como clave de todo), el gimnasio entra como un canal más (muere la duplicación
  panel/bot), un solo proceso escribe los datos (mueren las carreras). Papeleo de Meta en
  paralelo.
- **E5 — Canales oficiales:** WhatsApp Cloud API como segundo transporte del mismo bot
  (Coexistence permite convivir), Instagram DM por la misma plataforma de Meta, vía un
  worker-buzón patrón timbre v2 (infra que ya existe).
- **E6 — Promoción al maestro:** dixdybot/ como módulo genérico multi-cliente (persona +
  caminos + tarifario por cliente), segundo cliente piloto, API key por cliente.

Cada etapa termina en producción con tests + replay de escenarios dorados + nota del juez,
huella con `actividad.py` y rollback de una línea.

---

## 9. Qué sobrevive y qué muere del bot actual

**Sobrevive (está bien hecho):** `enviar.js` (anti Bad-MAC), `outbox.js` (cola
anti-duplicados), `gating.js` (anti-ban), `dudas.js` (el embrión exacto de los caminos),
`precios.js` como patrón "números en código, el modelo redacta", el extractor, el juez/actor
del gimnasio, `fechaISO` y `precioCoherente` (los dos guardianes), y todo el pipeline de
integración (PDF, correo, Supabase, repartidor) que ya es agnóstico del canal.

**Muere:** el panel monolítico que duplica lógica (renace consumiendo la API del bot), la
persona de 10.600 caracteres en una línea del .env (renace como caminos + archivos), el jid
de WhatsApp como identidad universal, las 4 formas distintas de llamar a Claude, y las 68
reglas planas (renacen como 20-30 caminos con estructura).

---

*Informes de detalle (14) en `investigacion-dixdybot/`: auditorías (arquitectura, conexión
con cifras de logs, cerebro, panel, integraciones), investigaciones verificadas (canales
WhatsApp, multicanal/Instagram, estado del arte de caminos, Claude Code vs API, censo open
source), las 3 propuestas de arquitectura completas y la síntesis del juez.*
