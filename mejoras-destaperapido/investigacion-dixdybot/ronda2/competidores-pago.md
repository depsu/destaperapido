# Competidores de pago — plataformas WhatsApp, AI-first y dimensionamiento (para dixdybot)

**Fecha de investigación: 23 de julio de 2026.** Todas las cifras indican de cuándo es la información.
Método: búsquedas web en inglés y español (jul-2026) + fetch directo de páginas de pricing y docs.
Lo que no pude verificar está marcado como tal. Contexto: informe para decidir (a) qué copiar,
(b) si conviene apalancarse en algo pagado, (c) cuánto puede cobrar DIXDY por dixdybot.

---

## A. Plataformas de WhatsApp marketing/ventas para pymes

### Resumen de precios (todos jul-2026, fuentes de 2026)

| Plataforma | Precio base | Modelo | IA incluida | ¿Vende de verdad conversando? |
|---|---|---|---|---|
| **Manychat** | $14–69 USD/mes + add-on IA ~$29/mes | por contactos activos | add-on débil | NO — flows de botones |
| **Wati** | $59 / $119 / $279–349 USD/mes | por plan + usuarios | KnowBot (RAG PDF/URL) | A medias — Q&A de soporte |
| **respond.io** | $79–279 anual ($99–349 mensual) | por MAC (contactos activos) | AI Agent desde plan Growth | Mejor que la media, con créditos |
| **SleekFlow** | Free / $149 / $349 USD/mes | por MAC | AgentFlow (multi-agente, 2026) | El pitch más cercano a venta real |
| **Zoko** | ~$35–50 USD/mes + add-ons | por conversaciones | limitada | NO — comercio Shopify por flows |
| **Trengo** | €299 / €499 mes (anual) | por conversaciones | HelpMate + €0,25/conv IA | NO — soporte, no venta |
| **Callbell** | $15–20 USD/usuario/mes | por asiento | ChatGPT solo Enterprise | NO — inbox multiagente |
| **Treble** | no público (contact sales) | por volumen | chatbot + A/B testing | Campañas/journeys, no venta 1:1 |
| **Leadsales** | ~$84 USD/mes (3 usuarios) | plan fijo + $26/usuario extra | mínima documentada | NO — CRM kanban de WhatsApp |

### Detalle por plataforma

**Manychat** (info mar–jul 2026). Desde marzo 2026 corren dos modelos de precio en paralelo:
Essential $14/mes a Business $69/mes, o Pro desde $15/mes escalando por contactos activos. La IA
es un **add-on de ~$29/mes** (Intention Recognition, AI Step, Flow Builder Assistant). Los reviews
de 2026 son lapidarios para nuestro caso de uso: el AI Step "no puede entrenarse con tus documentos,
no mantiene contexto entre mensajes y devuelve al cliente a los botones"; es "más cercano a keyword
matching que a IA conversacional real". WhatsApp es canal secundario (su core es Instagram/Facebook).
Gasto real reportado: $100/mes un setup simple, $1.000+/mes con WhatsApp+SMS+IA a escala.
**Conclusión: Manychat NO compite con dixdybot en venta conversacional; compite en campañas IG.**

**Wati** (info 2026). Growth $59/mes (tope duro 3–5 usuarios), Pro $119/mes (chatbots avanzados,
IA), Business $279–349/mes (múltiples números, round-robin). Cobra ~20% de markup sobre las tarifas
de Meta por mensaje; el costo real termina 30–50% sobre el precio de lista. Su IA es **KnowBot /
"AI Support Agent"**: subes PDFs (hasta 200 MB) o URLs y responde con modelos de OpenAI. Es RAG de
soporte: responde preguntas, no conduce una venta con estados, precios condicionales ni cierre.
Reclaman ~80% de consultas repetitivas automatizadas.

**respond.io** (info 2026). Starter $79/mes anual ($99 mensual, 5 usuarios, AI Prompt/AI Assist),
Growth $159 anual/$199 mensual (agrega **AI Agent**, broadcasts, workflows, API), Advanced
$279/$349. Modelo por MAC (monthly active contacts) con overages — la "trampa MAC" que denuncian
los comparadores. Su AI Agent se entrena con fuentes de conocimiento y hace calificación de leads +
soporte; es de lo más serio del segmento pyme. Además tiene **integración Dialogflow** y **Custom
Channel API** (webhook bidireccional para conectar un canal propio) — o sea, parcialmente abierto,
pero su AI Agent no es "trae tu propio LLM".

**SleekFlow** (info 2026). Free (50 MAC, 3 usuarios, con IA), Pro AI $149/mes (500–2.000 MAC),
Premium AI $349/mes, Enterprise custom. En 2026 lanzó **AgentFlow**: equipo de agentes IA
especializados por etapa del journey (calificar, vender, post-venta) que "aprenden de conversaciones
reales". Es el competidor SaaS cuyo marketing más se parece a lo que dixdybot ya hace en producción.
Meta fees aparte.

**Zoko** (info jun-2026). Base ~$35–49,99/mes + add-ons: chatbot $6/mes, Shopify $5/mes, Instagram
$9,99/mes, flows custom $5,99/flow/mes, y markup de $0,015 por conversación sobre Meta. 4,8★ en
~373 reviews de Shopify (jun-2026). Es **comercio puro para Shopify**: catálogo en el chat, cobros,
carrito abandonado. Su valor para nosotros es la lista de features de commerce, no su IA.

**Trengo** (info 2026). Boost €299/mes y Pro €499/mes (anual; €349/€599 mensual), modelo por
conversaciones (6.000–18.000/año incluidas) + **recargo de €0,25–0,30 por cada conversación que
atiende la IA** (HelpMate; reclaman 80% de resoluciones repetitivas, 70+ idiomas). Si usas mucho
la IA, el precio real ~se triplica. Orientado a soporte omnicanal europeo, no a venta.

**Callbell** (fetch de su pricing, jul-2026). $15/usuario/mes (Multiagent Chat) y $20/usuario/mes
(Plus); módulo de bot avanzado $22/mes; broadcast WhatsApp $65,55/mes; créditos WhatsApp desde
$54/mes; "ChatGPT Integration" solo en Enterprise a precio custom. Es un inbox multiagente barato,
fuerte en LATAM/Europa; IA casi inexistente en planes normales.

**Treble** (LATAM, info jul-2026). **Precio no público** (Capterra: "contact vendor"); tiers
Starter/Pro/Advanced negociados por volumen, mes de prueba gratis. Partner temprano de Meta en
LATAM, fuerte integración HubSpot, **A/B testing de campañas** y journeys. Es marketing/campañas
masivas con chatbot, no venta conversacional 1:1. No encontré precios concretos publicados — lo digo
explícitamente.

**Leadsales** (LATAM, info jul-2026). ~$83,99 USD/mes con 3 usuarios ($26 por usuario extra),
prueba de 14 días por $7. Plan Básico ~$2.363 MXN/mes y Avanzado ~$6.017 MXN/mes (con 500 créditos
de campaña). Es un **CRM kanban sobre WhatsApp** (embudos, asignación); no encontré un agente IA
conversacional serio documentado. Compite con nuestro Kanban del panel, no con el cerebro.

### Veredicto (a): venta conversacional real
Ninguna de las 9 resuelve de verdad la VENTA conversacional que dixdybot ya hace (cotizar con
tarifario por estado, fecha natural→ISO, despacho, seguimiento). Las que más se acercan en discurso:
SleekFlow AgentFlow y respond.io AI Agent (ambas 2026). El resto son campañas, flows de botones,
RAG de soporte o inbox. **La ventaja de dixdybot es real y verificable en el mercado 2026.**

---

## B. AI-first de atención/venta (Intercom Fin, Ada, Decagon, Sierra, Chatfuel)

**Intercom Fin** (fetch de fin.ai/pricing, jul-2026). **$0,99 por resolución** (también por
procedure-handoff y disqualification); **calificación de lead: $9,99 cada una** — ojo, le ponen
precio 10x a la venta vs el soporte. Handoff simple a humano: gratis. Base "Fin for platforms"
$49/mes con 50 resoluciones incluidas; con helpdesk Intercom, asientos $29–132/mes según plan.
**Sí opera en WhatsApp.** Conocimiento: Knowledge Hub (help center, PDFs, URLs, snippets con reglas
de audiencia) + **Procedures** (dic-2025/2026: instrucciones en lenguaje natural con branching
if/else y bloques de código; "Tasks" se depreca el 12-mar-2026) + Guidance (tono/escalación) +
**testing contra conversaciones históricas antes de encender**. Corporativo: la empresa se renombró
Fin (may-2026, titular de VentureBeat) y fuentes secundarias (Gleap, jun-2026) reportan acuerdo de
adquisición por Salesforce ~$3.6B — **no pude verificar la adquisición en fuente primaria** (429 en
VentureBeat).

**Ada** (info 2026). Sin precio público; señales: ~$30.000/año de entrada, mediana ~$70.001/año
(Vendr), rangos $30k–300k+/año; migró de per-resolution ($1–3,50 reportado) a modelo por
conversación. Entrenamiento: fuentes de conocimiento conectadas + **coaching loop** (revisas
conversaciones pasadas, das feedback de tono/contexto y se aplica a futuras — igual que nuestro
gimnasio) + **Playbooks** (procedimientos multi-paso) + Reasoning Engine con safety checks. En la
guía consultada no aparece WhatsApp como canal destacado. Solo enterprise (300K+ conversaciones/año).

**Decagon** (info 2026). Platform fee $50.000/año + per-conversación (default) o per-resolución
(~$0,50 negociado); contratos reportados $95k–590k/año. Sin self-serve ni free trial. Su pieza
estrella: **AOPs (Agent Operating Procedures)** — instrucciones en lenguaje natural que **compilan
a workflows validados/deterministas**: la IA interpreta el input desordenado del cliente, el logic
compilado garantiza que las acciones críticas se ejecuten igual siempre. **Es exactamente la tesis
de nuestros "caminos" (E3), validada por el enterprise de más caché de 2026.**

**Sierra** (info 2026). Todo custom: fee anual de plataforma + cargo por outcome + servicios
profesionales. Estimaciones de terceros: ~$150k/año y más, setup $50k–200k, año uno $200k–350k+.
Per-resolution reportado $1–2,50 (no confirmado por Sierra). Conversaciones no resueltas o escaladas
no se cobran. Su blog oficial defiende el outcome-based pricing como modelo de la industria.

**Chatfuel** (info 2026). Se movió a **plan único $69/mes** con contactos ilimitados y "Fuely AI"
incluido en WhatsApp, Instagram, Messenger, TikTok y web; CRM y agenda de citas incluidos; sin free
tier (trial 7 días). Meta fees aparte. Es el AI-first "de pyme": barato, pero IA genérica.

### ¿Entrenan el conocimiento mejor que nuestros caminos? (respuesta honesta)
El patrón ganador 2026 en TODOS los serios es el mismo que elegimos en E3: **lenguaje natural →
procedimiento estructurado y validado** (Fin Procedures, Decagon AOPs, Ada Playbooks). Nadie usa
"sube un PDF y reza" en el tier enterprise; eso quedó para Wati/Chatfuel. Dos cosas que ellos tienen
y nuestros caminos aún no: (1) **compilación/validación** del camino antes de activarlo (Decagon) y
(2) **backtesting contra el histórico real de conversaciones** antes de desplegar un cambio (Fin).
Ambas son copiables con lo que ya tenemos (conversaciones.jsonl + juez opus del sistema de calidad).

---

## C. ¿Alguno soporta "cerebro propio" (BYO-LLM) para usar solo su capa de canales/inbox?

- **Chatwoot — SÍ, y es el mejor fit** (docs oficiales, jul-2026): **AgentBot API** = webhook
  `message_created` hacia tu bot, tu lógica (cualquier LLM: OpenAI, Claude, Gemini), respondes por
  su API, y handoff a humano cambiando el estado de la conversación. Funciona sobre sus inboxes,
  incluido WhatsApp. Cloud: Hacker $0 (2 agentes), Startups $19, Business $39/agente/mes (anual);
  o **self-hosted open source gratis**. Su IA propia (Captain) va por créditos (300–800/mes
  incluidos, $20 por 1.000 extra) — pero con AgentBot no la necesitas.
- **respond.io — parcial**: integración Dialogflow y Custom Channel API (canal propio vía webhook),
  pero su AI Agent es cerrado; el BYO-brain se arma con workflows + HTTP, pagando $159–199/mes.
- **Manychat, Wati, SleekFlow, Trengo, Chatfuel, Zoko, Leadsales — NO** hay BYO-LLM documentado;
  su IA es caja negra propia (Wati sobre OpenAI, Trengo HelpMate, SleekFlow AgentFlow). Callbell
  solo "ChatGPT integration" Enterprise, sin traer clave propia documentada.
- Nicho aparte (jul-2026): plataformas chicas tipo Mindlytics/Ainisa aceptan tu API key de
  OpenAI/Claude, pero son actores menores sin track record — no vale la pena depender de ellas.

**Implicancia para DIXDY:** la decisión previa (gateway propio delgado + Cloud API de Meta directa,
que es gratis en ventana de servicio 24h desde el cambio a per-message del 1-jul-2025) sigue siendo
la más barata. Si algún día se quiere inbox multiagente "comprado" sin regalar el cerebro, **la única
opción seria y barata es Chatwoot** ($0 self-hosted o ~$19–39/agente) — y su AgentBot valida
técnicamente nuestra arquitectura E1 (puerta única al cerebro) + E4 (abstracción de canal).

---

## D. Features concretas que vale la pena COPIAR en dixdybot

Ordenadas por relación valor/esfuerzo con lo que ya existe (panel :8789, Supabase, envios.jsonl,
gimnasio, juez opus):

1. **Métricas de conversión por flujo/outcome** (Fin, Sierra): embudo cotizó→confirmó→despachó→cobró
   ya existe en el Kanban; falta la tasa por etapa y por semana, visible en el panel. Barato.
2. **Backtesting contra histórico** (Fin, 2026): antes de activar un camino nuevo, correrlo contra
   conversaciones.jsonl pasadas y comparar respuestas con el juez. Tenemos todas las piezas.
3. **Compilación/validación de caminos** (Decagon AOP, 2026): al guardar un camino, un paso que lo
   valida (condiciones alcanzables, acciones existentes, conflictos con otros caminos) antes de
   activarlo. Refuerza E3.
4. **Precio por outcome como argumento de venta** (Fin $0,99/resolución, $9,99/calificación;
   Sierra): aunque DIXDY cobre plan fijo, reportar "este mes el bot cerró X ventas = $Y" es el
   argumento de renovación. Los enterprise cobran 10x por una calificación de venta vs un ticket:
   confirma que lo nuestro (venta) es el segmento caro.
5. **Catálogo y pagos en el chat** (Zoko): para destaperapido aplica poco, pero para dixdybot
   producto: ficha de servicios con precios + link de pago (Webpay/MercadoPago) al confirmar.
6. **Recuperación de carrito/cotización abandonada** (Zoko, Wati): ya tenemos Dormidos 💤; falta
   la variante automática "cotizó y no contestó en 48h → seguimiento" con plantilla utility (gratis
   en ventana o ~$0,004–0,045 fuera).
7. **A/B testing de mensajes** (Treble): dos variantes de mensaje de cotización, medir cuál cierra
   más. Con envios.jsonl es un campo extra + un reporte.
8. **Atribución de Click-to-WhatsApp Ads** (respond.io, Wati): marcar conversaciones que llegan de
   anuncios y cruzarlas con cierres — encaja directo con la atribución "buen cliente" de DIXDY.
9. **Agenda/citas en chat** (Chatfuel incluye calendario; Trengo comparte booking link): para
   clientes tipo servicios a domicilio, proponer bloques de fecha/hora reales del repartidor.
10. **Reglas de audiencia en el conocimiento** (Fin Knowledge Hub): caminos que aplican solo a
    ciertos segmentos (comuna, tipo de cliente) — nuestros caminos E3 deberían tener scope.
11. **Multi-agente por etapa** (SleekFlow AgentFlow, 2026): no copiar la arquitectura (un cerebro
    con caminos basta), pero sí el reporting "qué etapa del journey atendió la IA".
12. **Créditos de IA como unidad de cobro** (Chatwoot $20/1.000, Trengo €0,25/conv): modelo a
    considerar para el tier alto de dixdybot cuando haya failover a API (E1) con costo real.

---

## E. Dimensionamiento honesto: qué cobrar en Chile por "bot de ventas WhatsApp con IA" administrado

**Referencias de mercado (todas 2026):**
- SaaS DIY internacional: $15–350 USD/mes + Meta fees, y el cliente lo opera solo (Manychat, Wati,
  respond.io, SleekFlow, Chatfuel). Costo real típico reportado: $100–400 USD/mes.
- **Agencias chilenas managed** (herihe.digital, may-2026; digitalmanager.cl; rankaglia, 2026):
  **desde 5 UF/mes + IVA hasta 25 UF/mes + IVA** para pymes (1 UF ≈ $39.000 CLP jul-2026, o sea
  ~$195.000–$975.000 CLP/mes); enterprise multi-canal 25–50 UF/mes. Casos publicados: clínica
  estética ~5,95 UF/mes, taller mecánico ~5,95 UF/mes, ecommerce mediano ~17,85 UF/mes. Setup:
  incluido en managed, o USD 500–2.000 con freelancer; enterprise USD 5.000–15.000 de setup +
  USD 1.500–4.000/mes.
- Proveedores locales sueltos: desde $50.000 CLP/mes soluciones simples; AutomatizaWeb (ojo: es
  cliente adoptado de la red DIXDY, no referencia neutral) lista $150.000–300.000 CLP de setup +
  $15.000/mes de soporte.
- Techo del mercado (enterprise AI-first): $30k–150k+ USD/año (Ada, Decagon, Sierra) — irrelevante
  como competencia directa en pyme chilena, pero demuestra que "IA que resuelve/vende" se paga caro.
- Costo de canal para DIXDY con Cloud API directa: **~$0** en respuestas dentro de la ventana 24h
  (per-message desde 1-jul-2025; utility gratis en ventana), solo marketing/utility fuera de ventana
  se paga por mensaje.

**Recomendación de precio para dixdybot como servicio administrado DIXDY (Chile, pyme):**
- **Tier entrada: 4–6 UF/mes** (~$160.000–240.000 CLP + IVA): bot de ventas IA + panel + soporte.
  Queda en la banda baja del managed chileno (5 UF) siendo MEJOR producto que lo que esa banda
  ofrece hoy (la mayoría vende flows con RAG, no venta conversacional con despacho).
- **Tier completo: 8–12 UF/mes** (~$315.000–475.000 CLP + IVA): + campañas/seguimientos, catálogo,
  atribución de Ads, reportes de cierre. Sigue bajo las 17–25 UF que cobran por ecommerce mediano.
- Setup: $0–150.000 CLP (el mercado local cobra $150k–300k; regalarlo es palanca comercial).
- Margen: con suscripción Max como cerebro (E1) y Cloud API gratis en ventana, el costo variable
  por cliente es cercano a cero hasta que el failover a API se active — el modelo de créditos
  (D.12) protege ese borde.
- Argumento de venta contra el SaaS: "Wati te cuesta $59–119 USD/mes y lo operas tú con un bot que
  responde FAQs; esto se opera solo y te cierra ventas" — con el reporte de outcomes (D.1/D.4)
  como prueba mensual.

---

## Lo que NO encontré / advertencias

- **Treble**: sin precios públicos (Capterra jul-2026: "contact vendor"). No inventé cifras.
- **Adquisición de Fin por Salesforce (~$3.6B)**: reportada por blogs de competidores (jun-2026);
  el rename Intercom→Fin sí está confirmado por titular de VentureBeat (may-2026), pero la
  adquisición NO la pude verificar en fuente primaria (rate-limit al fetch).
- **villelabs.cl**: citada por buscadores con rangos coherentes con herihe, pero el dominio no
  resolvió al fetch directo — usé solo lo que apareció en resultados.
- Cifras de Ada/Decagon/Sierra son **estimaciones de terceros** (Vendr, blogs de competidores);
  ninguno publica pricing.
- Los agregadores de pricing 2026 (Chatarmin, SetSmart, eesel, etc.) son blogs de competidores
  entre sí: crucé al menos dos fuentes por plataforma y el fetch directo donde se pudo (fin.ai,
  callbell.eu, chatwoot.com, herihe.digital, Capterra).

## Fuentes principales

- https://costbench.com/software/live-chat/wati/ y https://chatarmin.com/en/blog/wati-pricing (Wati, 2026)
- https://chatarmin.com/en/blog/manychat-pricing y https://flowgent.ai/blog/manychat-review (Manychat, 2026)
- https://chatarmin.com/en/blog/respond-io-pricing y https://respond.io/blog/respondio-pricing (respond.io, 2026)
- https://help.respond.io/l/en/channels/custom-channel (respond.io Custom Channel API)
- https://www.g2.com/products/sleekflow/pricing y https://www.xpay.sh/saas-pricing/sleekflow-io/ (SleekFlow, 2026)
- https://respond.io/blog/zoko-review y https://splashifypro.com/blog/zoko-pricing-in-2026-plans-fees-amp-the-real-monthly-cost (Zoko, 2026)
- https://www.eesel.ai/blog/trengo-pricing y https://chatarmin.com/en/blog/trengo-pricing (Trengo, 2026)
- https://www.callbell.eu/en/pricing/ (Callbell, fetch directo jul-2026)
- https://www.capterra.com/p/237164/Treble/ (Treble, fetch directo jul-2026)
- https://www.eligetucrm.com/blog/leadsales-precios-2026 (Leadsales, jul-2026)
- https://fin.ai/pricing (Fin/Intercom, fetch directo jul-2026)
- https://www.intercom.com/help/en/articles/14077835-procedures-vs-tasks-vs-workflows (Fin Procedures, 2026)
- https://www.gleap.io/blog/intercom-fin-ai-pricing-2026 (contexto Fin/Salesforce, jun-2026, secundaria)
- https://venturebeat.com/technology/intercom-now-called-fin-launches-an-ai-agent-whose-only-job-is-managing-another-ai-agent (rename a Fin)
- https://www.featurebase.app/blog/ada-cx-pricing y https://www.getmacha.com/blog/ada-ai-complete-guide (Ada, jul-2026)
- https://decagon.ai/product/aop y https://decagon.ai/resources/aop-the-future-of-cx (Decagon AOPs)
- https://fin.ai/learn/decagon-ai-pricing y https://quiq.com/blog/decagon-pricing/ (Decagon pricing, 2026)
- https://quiq.com/blog/sierra-ai-pricing/ y https://sierra.ai/blog/outcome-based-pricing-for-ai-agents (Sierra, 2026)
- https://thatmarketingbuddy.com/pricing/chatfuel y https://chatbotscape.com/reviews/chatfuel-review (Chatfuel, 2026)
- https://www.chatwoot.com/pricing y https://www.chatwoot.com/docs/product/others/agent-bots/ (Chatwoot, fetch directo jul-2026)
- https://www.wati.io/en/wati-knowbot/ y https://support.wati.io/en/articles/11463665 (Wati KnowBot)
- https://chat2desk.com/en/blog/articles/whatsapp-business-api-billing-to-change y https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing (pricing Meta per-message, jul-2025)
- https://herihe.digital/cuanto-cuesta-chatbot-whatsapp-chile/ (Chile, may-2026, fetch directo)
- https://www.digitalmanager.cl/blog/ia-whatsapp-business-automatizar-atencion-clientes-chile (Chile, 2026)
