# Noticias que afectan el plan dixdybot — semana 16–23 julio 2026 + último mes

Investigación hecha el 23 de julio de 2026 con búsquedas reales en inglés y español (WebSearch + verificación de fuentes primarias con WebFetch, incluida la documentación oficial de Meta). Cada ítem trae fecha, fuente y qué significa para dixdybot.

**Veredicto general de la semana 16–23 de julio:** relativamente tranquila en anuncios NUEVOS. Lo que hay son *deadlines* que se acercan de anuncios hechos a fines de junio / principios de julio — y esos deadlines son grandes. Las dos bombas del mes (fin de mensajes de servicio gratis en WhatsApp desde octubre, y el vaivén de Anthropic con el uso de suscripciones para automatización) se anunciaron antes del 16 de julio pero definen el plan dixdybot más que cualquier cosa de esta semana.

---

## 1. Meta / WhatsApp Business — LO MÁS GRANDE DEL MES

### 1.1 🔴 Fin de los mensajes de servicio gratis: desde el 1 de octubre de 2026 se cobra la respuesta en la ventana de 24h
- **Fecha del anuncio:** ~1–2 de julio de 2026 (cobertura de Analytics Insight fechada 2 jul 2026; documentación oficial de Meta ya actualizada).
- **Fuente primaria (verificada):** documentación oficial de Meta — "Effective October 1, 2026, Meta will charge for utility messages sent in response to users within an open 24-hour customer service window". Los "service messages" (respuestas de texto libre, humanas o de bot de terceros) pasan a cobrarse **por mensaje**, a la misma tarifa que utility/authentication de cada país. Eran gratis desde noviembre de 2024.
  - https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/non-template-messages
- **Detalles clave (corroborados en YCloud, Chakra, Delto, Chattigo, WAD.chat — esta última chilena):**
  - Tarifas país por país se publicarán **antes del 1 de septiembre de 2026**.
  - La **ventana gratuita de 72h** por Click-to-WhatsApp Ads / botones de Facebook e Instagram **se mantiene gratis**.
  - Da igual si el mensaje lo escribe una persona o una IA de terceros: se cobra igual. **El Meta Business Agent está exento** (paga por tokens, no por mensaje).
- **Qué significa para dixdybot:** rompe el supuesto de E5 ("Cloud API ~gratis para responder en ventana 24h") — desde octubre cada respuesta del bot en Cloud API cuesta plata por mensaje, así que el business case de E5 hay que recalcularlo con las tarifas de Chile cuando salgan (antes del 1-sep), y las campañas Click-to-WhatsApp (ventana 72h gratis) pasan a ser palanca de costo, algo que DIXDY ya sabe hacer con Google Ads/Meta Ads.

### 1.2 🔴 Meta Business Agent: competidor directo dentro de WhatsApp, con billing por tokens desde el 1 de agosto
- **Fechas:** disponibilidad global anunciada el **3 de junio de 2026** (TechCrunch, verificado; tras ~2 años de pruebas en India y México). Billing por tokens desde el **1 de agosto de 2026**: **US$2 por millón de tokens**, ~20.000–25.000 tokens por interacción típica ≈ **US$0,04–0,05 por conversación**, tarifa universal (no varía por país). Artículo de TechTimes del **16 de julio de 2026** (dentro de la semana objetivo): la ventana de prueba gratis termina en días.
- **Fuentes:** https://techcrunch.com/2026/06/03/metas-ai-agent-for-whatsapp-business-is-now-available-globally/ · https://www.techtimes.com/articles/320787/20260716/meta-business-agent-billing-starts-aug-1-free-test-window-ends-days.htm · https://www.ycloud.com/blog/whatsapp-service-messages-24-hour-window-pricing
- **Qué es:** agente de IA de Meta que responde preguntas, recomienda productos del catálogo, agenda citas, califica leads y deriva a humano — en WhatsApp e Instagram DM, sin escribir una línea de código.
- **Qué significa para dixdybot:** Meta se mete de lleno en el negocio de dixdybot y **se favorece a sí misma en el pricing** (su agente exento del cobro por mensaje de servicio; los bots de terceros pagan doble: su LLM + el mensaje de WhatsApp). La defensa de dixdybot es lo que Meta no hace: conocimiento profundo del negocio (caminos E3), integración a Supabase/PDF/repartidor/correo, y control total del dueño.

### 1.3 🟡 Actualización de tarifas y plataforma del 1 de julio de 2026
- **Fecha:** 1 de julio de 2026.
- **Qué cambió:** tarifas por mensaje actualizadas en mercados selectos (Italia, España, Polonia, Reino Unido, etc. — Chile no aparece entre los mencionados), migración a facturación en moneda local para India y Brasil, e **in-app signup global**: deeplink para que el usuario haga opt-in a mensajes de WhatsApp desde Facebook, Instagram, email, sitio web o un Canal.
- **Fuentes:** https://woztell.com/whatsapp-pricing-changes-july-2026/ · https://d7networks.com/blog/metas-july-2026-whatsapp-business-update/
- **Qué significa para dixdybot:** el deeplink de opt-in es una pieza gratis y oficial para alimentar la base de contactos de destaperapido cuando se migre a Cloud API (E5).

### 1.4 🟡 Recordatorio de contexto: desde el 15 de enero de 2026 están prohibidos los chatbots de IA "de propósito general" en la API — los bots de negocio siguen permitidos
- **Fecha:** política efectiva 15 de enero de 2026 (anunciada nov–dic 2025).
- **Qué dice:** fuera ChatGPT, Copilot, Perplexity y asistentes generales del WhatsApp Business API; **permitidos** los bots que dan servicio estructurado del negocio: soporte, reservas, tracking, ventas.
- **Fuentes:** https://respond.io/blog/whatsapp-general-purpose-chatbots-ban · https://www.techtimes.com/articles/313010/20251127/metas-whatsapp-bans-third-party-ai-chatbots-including-chatgpt-copilot.htm
- **Qué significa para dixdybot:** dixdybot es exactamente el tipo de bot permitido (ventas/soporte de un negocio concreto); usar Claude como cerebro detrás de un bot de negocio en Cloud API no viola la política. Refuerza que E5 es viable.

### 1.5 🟠 Baileys / APIs no oficiales: enforcement escalado durante 2026
- **Fechas:** reportes acumulados feb–jul 2026 (issues de GitHub en openclaw/openclaw, análisis de ingenieros, guías anti-ban).
- **Qué se reporta:** WhatsApp escaló la detección de clientes basados en Baileys en 2026, con **bans permanentes sin apelación** incluso en cuentas con uso aparentemente limpio; disparadores conocidos: loops de reconexión (crash-loops que generan miles de conexiones/hora), IP de servidor activa 24/7, mensajes idénticos a muchos destinatarios. Un blog (Kraya AI, fuente única — tomar con cautela) afirma que en 2026 WhatsApp además rastrea mensajes sin respuesta en 48h en ventana móvil de 30 días. Cifra de contexto: ~8 millones de cuentas baneadas al mes globalmente.
- **Fuentes:** https://github.com/openclaw/openclaw/issues/4376 · https://github.com/openclaw/openclaw/issues/16270 · https://zenvanriel.com/ai-engineer-blog/openclaw-whatsapp-risks-engineers-guide/ · https://blog.kraya-ai.com/whatsapp-automation-ban-risk
- **Qué significa para dixdybot:** valida la urgencia de E0 (cinturón de seguridad del Baileys vivo: circuit breaker anti-reconexión, gating, número no personal) y de tener E5 (Cloud API) como destino antes de que un ban decida por nosotros. El bot vivo de destaperapido ya tiene gating anti-ban, pero el crash-loop de reconexión es un vector concreto a revisar en E0.

### 1.6 🟢 Menor: features de consumidor de WhatsApp (22 de julio de 2026)
- Meta anunció mejoras de app: CarPlay mejorado, crear cuenta desde iPad, más multi-dispositivo. Voice Chat de grupos disponible desde ~14 de julio. Sin impacto directo en dixdybot.
- **Fuente:** https://about.fb.com/news/2026/07/new-whatsapp-features-keep-up-with-the-way-you-actually-live/

---

## 2. Anthropic / Claude — afecta el cerebro del bot y el failover E1

### 2.1 🔴 El vaivén de la automatización con suscripción: cambio anunciado, PAUSADO — pero volverá
- **Cronología (verificada en digitalapplied + cobertura VentureBeat/InfoWorld):**
  - **4 de abril de 2026:** Anthropic cortó el uso de suscripciones Claude con herramientas agénticas de terceros (OpenClaw y similares), citando presión de cómputo. Luego lo reinstauró con condiciones (VentureBeat: "with a catch"; no pude leer el detalle por rate-limit del sitio).
  - **14 de mayo de 2026:** anuncio formal: desde el **15 de junio** el Agent SDK, **`claude -p` (headless)** y apps de terceros vía ACP saldrían del pool de suscripción a un **crédito mensual separado** (US$20–200 según plan) facturado a precios API, sin rollover.
  - **15 de junio de 2026:** Anthropic **pausó el cambio** ("no longer happening"): todo sigue tirando del pool de suscripción como antes, y prometió aviso previo antes de relanzar una versión revisada. Motivo de fondo: suscriptores de $20/mes consumían $300–600 equivalentes de API con loops automatizados (subsidio 15–30x).
- **Fuentes:** https://www.digitalapplied.com/blog/anthropic-claude-credit-overhaul-june-15-2026 · https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html · https://venturebeat.com/technology/anthropic-reinstates-openclaw-and-third-party-agent-usage-on-claude-subscriptions-with-a-catch · https://www.techtimes.com/articles/317625/20260602/anthropic-ends-subscription-subsidy-agents-june-15-credit-pool-replaces-flat-rate-access.htm
- **Qué significa para dixdybot:** el cerebro actual (`claude -p` con suscripción Max) **hoy sigue funcionando igual**, pero Anthropic ya intentó dos veces en 2026 sacar la automatización del pool de suscripción y avisó que lo reintentará con otra forma. **E1 (puerta única al cerebro con failover suscripción→API) deja de ser "nice to have" y pasa a ser la prioridad #1 del plan** — es el seguro contra un cambio de términos con poco aviso.

### 2.2 🟡 Claude Sonnet 5: modelo más barato para agentes (candidato para el failover API de E1)
- **Fecha:** 30 de junio de 2026 (Anthropic + TechCrunch).
- **Qué es:** modelo mediano enfocado en tareas agénticas. Precio introductorio **US$2/M input y US$10/M output hasta el 31 de agosto de 2026**, luego $3/$15. Modelo por defecto en Free y Pro.
- **Fuentes:** https://www.anthropic.com/news/claude-sonnet-5 · https://techcrunch.com/2026/06/30/anthropic-launches-claude-sonnet-5-as-a-cheaper-way-to-run-agents/
- **Qué significa para dixdybot:** si E1 activa el failover a API, Sonnet 5 es el candidato natural costo/calidad para conversaciones de venta (a $3/$15 una conversación típica de bot cuesta centavos); comparar contra el juez opus actual del sistema de calidad.

### 2.3 🟡 Claude Code: promo de límites +50% extendida hasta el 19 de agosto; Fable 5 entra a Max al 50% de límites (20 de julio)
- **Cronología:** promo de +50% de límites semanales activa desde el 13 de mayo; extendida el 7 y el 13 de julio hasta el 19 de julio; **el 18 de julio se extendió hasta el 19 de agosto de 2026** (Pro, Max, Team, Enterprise por asiento). Desde el **20 de julio**, **Fable 5 queda incluido en Max y Team Premium hasta el 50% de los límites semanales** (mismo pool compartido; requiere Claude Code v2.1.170+); Pro y Team Standard pierden el acceso incluido y pasan a créditos medidos con **US$100 one-time** (luego $10/$50 por Mtok).
- **Fuentes:** https://www.helpnetsecurity.com/2026/07/13/claude-code-weekly-limits-promotion-extended/ · https://www.digitalapplied.com/blog/claude-code-limits-raised-fable-5-max-team-premium-2026 · https://apidog.com/blog/claude-code-weekly-limits-50-percent-increase-july-2026/ · https://news.ycombinator.com/item?id=48883064
- **Qué significa para dixdybot:** con el plan Max de Alejandro, el bot y las rondas DIXDY tienen holgura extra hasta el 19 de agosto (después los límites vuelven a la base — presupuestar consumo del bot para septiembre); y Fable 5 queda disponible dentro de Max si algún flujo del bot lo amerita.

### 2.4 🟡 API de Claude: deadline el 24 de julio (mañana) y mejoras de límites
- **Fecha:** julio de 2026 (cobertura byteiota, verificada).
- **Qué cambia:** **Opus 4.7 fast mode se descontinúa el 24 de julio de 2026** (las llamadas con `speed:"fast"` a `claude-opus-4-7` darán error; migrar a Opus 4.8 fast, que además baja de $30/$150 a $10/$50). Las **API keys ahora pueden tener expiración** configurable (3h a 30d o custom, con avisos por correo). Rate limits consolidados en 3 tiers (Start/Build/Scale) con límites subidos; Sonnet y Haiku igualan los RPM/ITPM/OTPM de Opus; **los tokens de caché ya no cuentan para ITPM**.
- **Fuente:** https://byteiota.com/claude-api-july-2026-rate-limits-key-expiry/
- **Qué significa para dixdybot:** si algún script DIXDY llama a Opus 4.7 fast por API, migrarlo antes del 24-jul; para E1/E6, keys con expiración = mejor higiene para las API keys por cliente, y el caché gratis para rate limits abarata prompts largos de persona/caminos.

### 2.5 🟢 Semana 16–23 de julio en el newsroom de Anthropic: tranquila en producto
- Verificado en anthropic.com/news: 20–22 de julio solo hubo anuncios de investigación económica, donación a Public First Action y grants de ciencia. Lo relevante a producto fue antes: Claude for Teachers (14-jul), Cowork a la nube/móvil (7-jul), "Making of Claude Code" (6-jul), redeploy global de Fable 5 + Sonnet 5 (30-jun).
- **Fuente:** https://www.anthropic.com/news

---

## 3. Agentes de IA para pymes / contexto LATAM

### 3.1 🟡 Los agentes despegan como historia de OPERACIONES, no de developers
- **Fecha:** julio de 2026 (datos de sesiones de Cowork publicados este mes; Cowork salió del desktop el 7-jul y OpenAI lanzó ChatGPT Work el 9-jul).
- **Dato:** en 1,2M de sesiones de Cowork en 600.000+ organizaciones: 33,4% procesos de negocio, 16,4% contenido, solo 8,7% desarrollo de software.
- **Fuentes:** https://arrow-ai.us/blog/ai-news-july-2026/ · https://www.lilachbullock.com/ai-news-this-week-19-july-2026/
- **Qué significa para dixdybot:** el mercado pyme está siendo educado en "agente que hace el trabajo" — buen viento de cola para vender dixdybot como producto (E6), con el ángulo de proceso completo (cotiza→confirma→despacha→cobra), no "chatbot".

### 3.2 🟡 LATAM: WhatsApp sigue siendo EL canal, y la prensa en español ya digirió el cambio de octubre
- **Fecha:** julio de 2026.
- **Qué se ve:** cobertura en español (Chattigo, Delto, Riqra, WAD.chat de Chile, foros) explicando el cobro de mensajes de servicio desde octubre y cómo prepararse; contexto de adopción: >90% de penetración de WhatsApp en adultos de CO/MX/BR/AR, conversión 3–5x vs email (cifras de vendors, orden de magnitud razonable).
- **Fuentes:** https://blog.chattigo.com/whatsapp-business/nuevo-cobro-whatsapp-business-api-meta-2026 · https://www.delto.com/blog/whatsapp-cobro-mensajes-servicio-octubre-2026 · https://www.wad.chat/es/wad/recursos/nuevo-cobro-meta-whatsapp-business-octubre-2026.html
- **Qué significa para dixdybot:** los competidores BSP de la región ya están reposicionando su pricing; si dixdybot llega a E6 con costos claros post-octubre, llega con ventaja de timing.

### 3.3 🟡 Instagram DM (para E5): reglas 2026 endurecidas
- **Fecha:** cambio efectivo 27 de abril de 2026.
- **Qué cambió:** tags `CONFIRMED_EVENT_UPDATE` deprecados; fuera de la ventana de 24h se exigen Utility Templates; tope de ~200 DMs automatizados/hora por cuenta; permiso `instagram_business_manage_messages` obligatorio.
- **Fuentes:** https://www.keyapi.ai/blog/instagram-messaging-api-policy/ · https://www.spurnow.com/en/blogs/instagram-dm-automation-rules
- **Qué significa para dixdybot:** el diseño E4/E5 (abstracción de canal) debe modelar la ventana de 24h + templates como concepto de primera clase, porque aplica igual en WhatsApp Cloud API e Instagram.

---

## 4. Síntesis: impacto en el plan dixdybot por etapa

| Etapa | Noticia que la toca | Efecto |
|---|---|---|
| E0 (cinturón Baileys) | Enforcement escalado 2026, crash-loops como vector de ban | **Sube de urgencia**; añadir circuit breaker de reconexión |
| E1 (puerta única + failover) | Anthropic pausó (no canceló) el metering de `claude -p`; Sonnet 5 barato; API keys con expiración | **Prioridad #1 del plan**; failover a Sonnet 5 por API |
| E2/E3 (conocimiento/caminos) | Meta Business Agent genérico global | El diferencial de dixdybot es justo E3; acelerar |
| E5 (Cloud API + Instagram) | **1-oct: fin de mensajes de servicio gratis**; 72h de CTWA sigue gratis; bots de negocio permitidos; reglas IG 27-abr | Rehacer el business case con tarifas Chile (salen antes del 1-sep); CTWA como palanca |
| E6 (producto multi-cliente) | Token billing del Business Agent ($0.04–0.05/conv) como precio ancla; mercado pyme educándose en agentes | Referencia de pricing y viento de cola comercial |

**Fechas para el calendario DIXDY:** 24-jul (muere Opus 4.7 fast en API) · 1-ago (empieza token billing del Meta Business Agent) · 19-ago (termina promo +50% de Claude Code) · 31-ago (termina precio intro de Sonnet 5) · 1-sep (Meta publica tarifas país por país de mensajes de servicio) · **1-oct (se acaba el "responder gratis" en la ventana de 24h de WhatsApp API)**.

---

## 5. Notas de confiabilidad
- Confirmado en fuente oficial: cobro de mensajes de servicio desde 1-oct-2026 (docs de Meta), newsroom de Anthropic (fechas de Sonnet 5, Cowork, Teachers), pricing de Sonnet 5.
- Corroborado en 3+ fuentes independientes: token billing del Business Agent (1-ago, $2/M), promo Claude Code (+50% hasta 19-ago), pausa del credit overhaul de Anthropic.
- Fuente única / tomar con cautela: la métrica "mensajes sin respuesta en 48h, ventana 30 días" como señal de ban (Kraya AI); el detalle exacto del "catch" en la reinstauración de agentes de terceros (VentureBeat devolvió 429 dos veces).
- No encontré: cambios regulatorios chilenos específicos de bots/WhatsApp en la ventana 16–23 de julio, ni noticias de bans masivos nuevos esta semana concreta.
