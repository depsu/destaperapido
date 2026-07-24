# DIXDYBOT — Ronda 2: tendencias 2027, papeleo Meta, referencias y plan revisado

**Fecha:** 23 de julio 2026 · **Cómo se hizo:** 15 agentes — 7 investigadores (tendencias en
foros de EE.UU., noticias del 16-23 de julio, onboarding de Meta, referencias de
diseño/lógica, competidores de pago, web vs app, frameworks) + 7 verificadores adversariales
que castigan información vieja + 1 arquitecto revisor que enfrentó el plan E0-E6 a toda la
evidencia nueva. Detalle en `investigacion-dixdybot/ronda2/` (el plan actualizado completo
está en `ronda2/plan-revisado.md`).

---

## 1. Veredicto a la pregunta "¿de verdad es la mejor solución?"

**El plan resiste 2027 — con ajustes, no con vuelta atrás.** La columna vertebral (evolución
del bot vivo, gateway de canales propio y delgado, cerebro Claude tras una puerta única con
failover, caminos con humano en el loop, Mac mini hoy) quedó **ratificada y hasta
reforzada** por la evidencia fresca:

- **OpenAI mató su Agent Builder no-code a los 8 meses** (se apaga el 30-nov-2026) →
  valida "gateway propio + código" sobre plataformas no-code.
- **Los AI-first del mercado convergen en nuestro mismo patrón de caminos** (Fin
  "Procedures", Decagon "AOPs", Ada "Playbooks": lenguaje natural que se compila a
  procedimiento estructurado) — **y nadie tiene el aprendizaje en caliente**. Seguimos
  siendo originales en el corazón.
- **El backlash anti-IA es real** (85% prefiere humano; Gartner proyecta >40% de proyectos
  de agentes cancelados a 2027) → el diseño con pausa-y-pregunta al humano no es un lujo,
  es EL argumento de venta.
- **MCP ganó como estándar** (donado a la Linux Foundation, adoptado por OpenAI, Google,
  Microsoft, AWS) → exponer las herramientas del bot como MCP es el seguro anti-lock-in.
- Los VCs financian exactamente esta tesis: agentes verticales para oficios. **Avoca (voz
  para gasfitería/HVAC) se hizo unicornio en abril 2026** — señal directa para este rubro.

## 2. Pero TRES supuestos operativos cambiaron (por eso valía preguntar)

1. **El "responder ~gratis" de la API oficial muere el 1-oct-2026.** Meta anunció (~1-jul)
   que cobrará los mensajes de servicio en la ventana de 24h, tarifa por país (referencias
   US$0,01-0,025/mensaje; cifras de Chile antes del 1-sep). Sigue siendo marginal para el
   negocio (~$5-15 mil CLP/mes al volumen actual, y la ventana de 72h por anuncio
   click-to-WhatsApp sigue gratis), pero ya no es ~$0: la economía de E5 se recalculó.
2. **Anthropic ya intentó dos veces sacar `claude -p` del pool de la suscripción** (anuncio
   14-may para el 15-jun: crédito mensual separado de US$20-200; lo pausó el mismo 15-jun
   prometiendo aviso previo). Hoy el cerebro en Max sigue igual, pero volverá →
   **E1 (failover suscripción→API) pasa a prioridad #1**, justo después del cinturón E0.
3. **El enforcement contra Baileys escaló en 2026** (reportes feb-jul de bans permanentes
   sin apelación; vectores: crash-loops de reconexión, IP de servidor, mensajes idénticos)
   → el papeleo de Meta se adelanta a HOY como pre-etapa, con **fecha límite interna
   30-sep-2026** para migrar por Coexistence, y E0 suma un circuit breaker de reconexión.

**Y una novedad mayor: Meta lanzó su propio "Business Agent"** dentro de WhatsApp/IG
(global 3-jun-2026; cobra desde el 1-ago US$2/millón de tokens, ~4-5¢/conversación; incluido
en tiers Premium ~US$5-15/mes). ¿Nos come? **No**: es un contestador de FAQ genérico — no
cotiza con tarifario propio, no genera PDF, no despacha repartidores, no aprende del dueño.
Y su plataforma soporta explícitamente el **"mixed responder model"**: agente de Meta +
agentes de terceros + humanos conviviendo con traspasos. O sea: el chatbot básico se volvió
commodity regalado, y dixdybot debe venderse como lo que es — **el agente que OPERA el
negocio** (cotiza→confirma→despacha→cobra), no "un chatbot". La política de WhatsApp del
15-ene-2026 prohíbe asistentes de propósito general (ChatGPT etc.) pero permite
expresamente bots de negocio como el nuestro.

## 3. El papeleo de Meta: sí se puede agilizar con DIXDY

- **La IA automatiza ~70% del alta**: webhook (Worker de Cloudflare), plantillas por API,
  token permanente, expediente de verificación precargado. A Alejandro le quedan **~45-60
  minutos de clicks** (login Facebook + 2FA, código del número, subir documentos, tarjeta)
  + esperas de Meta de 1-3 días.
- **Coexistence (global desde may-2026, Chile OK): el MISMO número en la app y en la API a
  la vez.** Se activa escaneando un QR (minutos), sincroniza hasta 6 meses de chats.
  Requisitos/límites: 7+ días de uso previo en la app, abrir la app cada ~13 días, tope
  20 msg/s, sin grupos por API. **Al migrar se pierde la sesión Baileys en el acto** (los
  dispositivos vinculados se desvinculan) — la migración es una tarde, no un drama.
- **La verificación del negocio NO es necesaria para partir** (responder es ilimitado; sin
  verificar solo limita a 250 conversaciones iniciadas por la empresa/día). En Chile demora
  12-72h hábiles con constitución + RUT en un PDF.
- **Patrón dual ratificado** (es lo que hace el ecosistema con Evolution API): cliente
  nuevo parte con chip + app + Baileys **el día 1** (cero papeleo, la velocidad que hoy
  tenemos), la IA deja el expediente Meta precargado esa misma semana, los 7 días de
  Coexistence corren solos, y al validar migra en una tarde. **Si hay ban antes, el
  expediente convierte la emergencia de semanas en horas.**
- **Instagram DM: se monta en UNA TARDE** para una cuenta que DIXDY administra (cuenta
  profesional + login del dueño + webhook; Standard Access sin App Review). El App Review
  con verificación (5-10 días) queda solo para cuando dixdybot se venda como SaaS (E6,
  rol "Tech Provider" de Meta con Embedded Signup: onboardear un cliente en 5-15 min).

## 4. Más de dónde apalancarse (lo que pediste: diseño y lógica)

**El hallazgo mayor: NanoClaw** (30.316 ⭐, MIT, commit del 21-jul-2026) — asistente
WhatsApp/Telegram/Slack con cerebro **Claude Agent SDK**, adaptador Baileys v7, router y
colas SQLite con un escritor por archivo. **Es el plano de nuestras etapas E1+E4 ya
construido y legible en una tarde.** Se usa como arquitectura espejo, no se adopta.

- **Claude Agent SDK** (Anthropic) supera a `claude -p` pelado como backend del cerebro:
  sesiones con memoria por cliente (mata el HISTORY_LIMIT artesanal), forkSession para el
  gimnasio, hooks de permiso, costo por mensaje. Ojo legal verificado: producto para
  terceros = API key sí o sí.
- **Claude Code Channels**: como runtime de producción no encaja (preview, una sola cola),
  pero su **"permission relay"** es la especificación exacta de nuestro pausa-y-pregunta:
  el bot te escribe por WhatsApp "¿apruebo? responde si/no + código de 5 letras". Se copia
  la spec.
- **Mastra** (26k ⭐, Apache-2.0): el mejor diseño de memoria (historial que se resume solo
  cuando crece) y de pausas que sobreviven reinicios. **VoltAgent** (10k ⭐, MIT): código
  de suspend/resume copiable literal. **Vercel AI SDK v7** (25k ⭐): la capa delgada ideal
  para el failover API.
- **UX del editor de caminos — decidido con evidencia**: para un dueño no técnico en
  iPhone gana **chat con IA + tarjetas de caminos con diff y botón "Aprobar" + historial**
  (patrón Intercom Fin / Dust / Decagon), con lista vertical tipo cascada para caminos
  multi-paso (patrón Typebot). **SIN canvas de nodos**: React Flow es de segunda clase en
  táctil (issues abiertos) y la muerte del Agent Builder de OpenAI enterró esa apuesta.
  Para tematizar el panel actual sin reescribirlo: DaisyUI (MIT, CSS puro).
- Descartes con causa: Dify (su licencia prohíbe multi-tenant → chocaría con E6), n8n
  (prohíbe embeber/revender), Papercups y chatbot-ui (muertos).

## 5. ¿Web o app? — decidido: PWA, sin app nativa

- La PWA instalada en el iPhone da push, ícono, badge y pantalla completa desde iOS 16.4;
  iOS 26 además abre como app todo sitio agregado al inicio. **DIXDY ya tiene web push
  funcionando** (avisos-worker): darle push a los paneles es reutilizar, no construir.
- La app nativa costaría US$99/año + revisión de 24-72h por cada update (mata la iteración
  diaria con IA), y Apple rechaza apps que son una web envuelta. Lo único que daría de
  verdad (widgets, GPS en segundo plano) no está en el plan.
- Todos los competidores venden panel web con login; ninguno obliga app. Para clientes
  futuros: Cloudflare Access (gratis hasta 50 usuarios).

## 6. ¿De pago? — nada que comprar, mucho que copiar, y hay negocio

- **Nada pagado conviene para el canal**: los SaaS pyme (Manychat, Wati, respond.io,
  SleekFlow, Trengo…) cuestan US$14-349/mes + 30-50% de sobrecostos reales, y **ninguno
  resuelve la venta conversacional real** — son flows de botones o RAG de soporte. Solo
  Chatwoot permite "cerebro propio" en serio (queda como plan B de inbox).
- **Features que sí les copiamos** (con etapa asignada): embudo de conversión por etapa
  (E2), backtesting de caminos contra conversaciones históricas antes de activar (patrón
  Fin, E3), validación del camino al guardar (patrón Decagon, E3), seguimiento de
  cotización abandonada + atribución click-to-WhatsApp (E5).
- **El dato de negocio**: Intercom Fin cobra US$0,99 por resolución de soporte pero
  **US$9,99 por calificación de VENTA** — el mercado le pone precio 10x a lo que dixdybot
  hace. En Chile las agencias cobran **5-25 UF/mes** por bots administrados mucho más
  tontos. Precio sugerido dixdybot: **tier entrada 4-6 UF/mes, tier completo 8-12 UF/mes**
  (+IVA), con margen alto porque el costo variable es casi cero.

## 7. Calendario de fechas duras (entra al plan)

| Fecha | Qué pasa |
|---|---|
| 24-jul-2026 | Muere Opus 4.7 fast en la API (verificar que ningún script lo use) |
| 1-ago-2026 | Meta empieza a cobrar su Business Agent (fin de la prueba gratis) |
| 19-ago-2026 | Fin de la promo +50% de límites de Claude Code (presupuestar septiembre) |
| 31-ago-2026 | Fin del precio intro de Sonnet 5 ($2/$10) — probar como failover antes |
| 1-sep-2026 | Meta publica las tarifas por país de los mensajes de servicio (Chile) |
| **30-sep-2026** | **Meta interna DIXDY: migración del número por Coexistence lista** |
| 1-oct-2026 | Fin del "responder gratis" en la ventana de 24h de la Cloud API |

Regla de contingencia: **la fecha del canal manda** — si los caminos (E3) se atrasan, la
migración de canal (E4-E5) le pasa por encima; no dependen entre sí.

## 8. Requisitos de Alejandro fijados después de la investigación (23-jul-2026)

Tres requisitos de primera clase que amarran el diseño de E2-E6:

1. **Genérico y modular:** dixdybot sirve a cualquier rubro; toda capacidad es un módulo
   que se activa/desactiva y configura desde el panel. Las funciones nuevas que Claude Code
   desarrolle nacen administrables (manifiesto + schema de config + switch), jamás
   cableadas a un rubro.
2. **Design system único (E2, antes de construir el panel):** referencias Chatwoot / Fin /
   Typebot / Linear → extraer patrones (no branding) → tokens + componentes publicados en
   Claude Design (claude.ai/design vía DesignSync) y espejados en el repo. Regla dura:
   toda vista usa solo ese sistema — cero variaciones, fluidez especificada (motion,
   optimistic UI, skeletons).
3. **IA madre + agentes especialistas (arquitectura supervisor/handoff):** un router barato
   (portero, sin LLM cuando se puede) deriva EN SILENCIO al agente del rubro correcto
   (ej. Sofía = baños químicos; otro = destapes/limpiezas), y cada agente carga SOLO los
   caminos de su dominio — es la respuesta estructural a la dilución de atención. Esquema:
   cada camino declara su dominio/agente desde el día 1 de E3; la madre multi-agente se
   activa como módulo en E4-E6. Un agente = nombre + persona + sus caminos + sus módulos;
   una o varias "caras" ante el cliente es configuración del negocio.

## 9. Refutaciones de la verificación (transparencia)

Dos claves de la ronda quedaron REFUTADAS por los verificadores y se retiraron del plan:
el supuesto endurecimiento de Instagram DM del 27-abr-2026 y el "in-app signup" global del
1-jul-2026. El plan solo se apoya en lo verificado directo en docs de Meta. También quedó
como no-verificable en fuente primaria la compra de Intercom/Fin por Salesforce (solo el
rename está confirmado).
