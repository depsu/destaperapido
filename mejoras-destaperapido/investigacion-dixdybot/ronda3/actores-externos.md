# Arbitraje: actores nuevos traídos por ChatGPT DR y Gemini DR (dixdybot)

Fecha de verificación: 2026-07-23. Método: fuente primaria (páginas oficiales) + segunda fuente
cuando fue posible. Buscadores con captcha durante la sesión (DDG lite fue el único usable);
WebSearch agotado a nivel sesión. Cada dato lleva fecha de consulta.

---

## 1. Brote (brote.ai/es) — claim de ChatGPT: CONFIRMADO

- **Existe.** Agente IA para WhatsApp "hecho en LATAM 🇨🇱", orientación clara a ecommerce y
  servicios. Fuente: https://brote.ai/es (consultado 2026-07-23).
- **Onboarding confirmado tal cual lo dijo ChatGPT:** dos caminos — pegar la URL del sitio
  (la IA lee productos/precios/catálogo) o **grabar un audio de hasta 10 minutos** explicando
  el negocio; lema central: *"Del audio al chat — en 15 minutos"*.
- **Precio confirmado:** *"$29"* citado como "el plan más barato (USD/mes)" + **plan Free para
  siempre (50 conversaciones/mes)**. La tabla completa de planes es render JS (no visible en
  /es/precios ni /es/pricing por fetch estático), pero el US$29 y el Free aparecen en la landing.
- **Sesgo ecommerce confirmado:** integraciones Shopify (stock en vivo), Mercado Pago, Flow,
  Khipu, Stripe, Google Calendar, Chilexpress, Starken. Las pasarelas y courriers son chilenos
  → foco Chile/LATAM confirmado.
- **Qué copiarle:** (a) onboarding por audio del dueño — mata la fricción de setup, encaja con
  nuestro flujo "entrenar al bot conversando"; (b) plan Free con tope de conversaciones como
  anzuelo de entrada; (c) integración nativa con pagos chilenos.

## 2. Lelemon (lelemon.cl) — claim de ChatGPT: CONFIRMADO

- **Existe y es chileno:** *"Lelemon Agents es un SaaS B2B chileno (Santiago, Chile)"*, fundador
  Camilo Alaniz. Fuente primaria: https://lelemon.cl (2026-07-23). Segunda fuente: LinkedIn
  /company/lelemon ("IA conversacional… cualquier negocio en Chile") y CB Insights (2026-07-23).
- **Precios EXACTOS como los citó ChatGPT (en UF):**
  - Agente interno: *"Desde 1,5 UF/mes"* + **setup 5 UF única vez** + primer mes gratis, sin contrato.
  - Agente extra: *"0,8 UF/mes"*.
  - Agente público WhatsApp: *"Desde 3,8 UF/mes"* (incluye 500 conversaciones; extra a $100 CLP c/u).
  - Ejemplos combinados publicados: estudio jurídico 1,5+3,8+0,8 = **6,1 UF/mes**; constructora
    1,5+3,8+0,8×2 = **6,9 UF/mes**.
- **Qué copiarle:** es el comparable más directo de dixdybot. (a) Pricing en UF, modular
  (base + WhatsApp público + agentes extra) — valida cobrar en UF; (b) setup fee separado en UF;
  (c) primer mes gratis; (d) cobro por conversación excedente en CLP; (e) narrativa "agentes que
  ejecutan tareas reales" (cobros, agenda), no "chatbot".

## 3. WAI — claim de ChatGPT: NO VERIFICABLE (probable confusión/alucinación)

- **No se encontró ningún "WAI" chileno de agendamiento con planes 1,5/2,5/4,5 UF.** Búsquedas
  (DDG lite + Bing, 2026-07-23) solo arrojan:
  - **WAI de Artechclick** (wai.artechclick.com → artechclick.com/wai-info): agente IA WhatsApp
    con agendamiento (TurnoTap), pero es **colombiano** ("Soporte directo desde Bogotá, Colombia")
    y su único plan es **$45.000 COP/mes** (12.000 créditos IA). Consultado 2026-07-23.
  - **"Wai IA" de iaworker.io**: agentes voz/WhatsApp, precios **en euros** (implementación
    3.490€+IVA, mantención 150€/mes/agente) — europeo, no chileno. Consultado 2026-07-23.
  - wai.cl no resuelve DNS (2026-07-23).
- **Veredicto:** tratar el claim como no confiable hasta que ChatGPT entregue URL. No incorporar
  al mapa competitivo chileno. (Hallazgo colateral útil: herihe.digital vende agente IA de
  agendamiento WhatsApp en Santiago "desde 5 UF + IVA" — otro punto de precio chileno real.)

## 4. Stammer AI (stammer.ai) — claim de Gemini: CONFIRMADO (doble fuente)

- **Existe:** plataforma **white-label** de agentes IA (chat y voz) para agencias, "under your
  own brand". Fuentes: https://stammer.ai/pricing y homepage (ambas 2026-07-23).
- **Precios plataforma:** Agency **US$197/mes** (20+ agentes chat y voz), Full SaaS Mode
  **US$497/mes** (100+), Enterprise custom. Uso aparte: ~$0.001-0.03/mensaje según modelo;
  voz $0.11-0.17/min.
- **0% comisión confirmado:** *"Zero revenue sharing (keep 100% of markup)"*; *"You control the
  price, usage and who gets access"*.
- **Reventa $300-500 confirmada:** FAQ del pricing: agencias *"usually $300–$500 per month per
  agent"*; homepage: ejemplo *"Charge: $499/mo | Your Cost: ~$12/mo | Your Profit: $487/mo"*,
  bundles sugeridos *"$800-$1,200/month"* y *"$2,500 setup fees"*.
- **Qué copiarle:** no el producto sino la **economía**: el mercado de bots gestionados se vende
  a US$300-500+/mes por cliente con costo marginal ínfimo, y cobra setup de ~US$2.500. Valida
  nuestra mensualidad + implementación separada.

## 5. Botsify white-label — claim de Gemini: CONFIRMADO existencia, precio MATIZADO

- **Existe la oferta white-label oficial:** botsify.com/pricing enlaza a
  botsify.com/pricing/whitelabel-ai-agents ("Whitelabel Platform for Agencies", "Pay as you go
  clients", "Unlimited AI Agents", 30.000 créditos/mes). Consultado 2026-07-23.
- **Precio white-label NO publicado en el HTML estático** (la página no muestra cifras de plan;
  solo "$100/Month" como valor referencial de un desarrollo regalado). Tercero (pixelodigital.com,
  2026): Agency **US$199/mes** con 5 client seats. El plan gestionado "Done-for-You" sí es
  público: **US$149/mes o US$1.490/año** con success manager dedicado.
- **Qué copiarle:** el naming/postura **"Done-for-You Agent"** con "dedicated success manager" —
  exactamente la posición de dixdybot (servicio gestionado, no software self-service).

## 6. SuperPyme (superpyme.cl) — claim de Gemini: MATIZADO (existe, escalera real difiere en los tramos altos)

- **Existe y es chileno:** Huérfanos 1055, Santiago; +56 9 9299 2345. Negocio principal:
  tiendas WooCommerce gestionadas ($19.990 a $789.000/mes). Fuente: https://superpyme.cl
  (2026-07-23).
- **Escalera REAL de bots WhatsApp** (superpyme.cl/precios-bot-whatsapp/, IVA incluido,
  2026-07-23):
  | Plan | Mensual | Implementación |
  |---|---|---|
  | Básico sin IA | $14.990 | incluida |
  | IA Starter | $29.990 | desde $49.990 |
  | Ventas/Cotizaciones (más vendido) | $49.990 | desde $79.990 |
  | Pro Integrado | $79.990 | desde $129.990 |
  | A medida | desde $149.990 | desde $390.000 |
- **Vs. el claim de Gemini:** los 3 primeros peldaños ($14.990/$29.990/$49.990) y el rango de
  implementaciones ($49.990-$390.000) **calzan**; los tramos "53-125 mil" y "150-350 mil" NO
  calzan con lo publicado hoy ($79.990 y "desde $149.990"). Corregir las cifras en el plan.
- **Qué copiarle:** (a) separar mensualidad de implementación en toda la escalera; (b) etiquetar
  el plan de cotizaciones como "más vendido"; (c) es el ancla de precio bajo chilena contra la
  que nos van a comparar.

## 7. treble.io vs treble.ai — desambiguación de ChatGPT: CONFIRMADA (con dos matices)

- **Son dos productos distintos, confirmado** (ambos consultados 2026-07-23):
  - **treble.ai**: BSP oficial de WhatsApp Business para LATAM (chatbots IA, campañas masivas,
    HubSpot/Salesforce; clientes Rappi, Platzi, Renault). **Matiz 1:** hoy NO publica precios —
    solo demo. Fuente secundaria dedicada (hackceleration.com/es/labs/treble-precio, actualizado
    jun-2026): plan gratis 5 conversaciones, *"ningún precio Starter, Pro o Advanced publicado"*,
    precios "bajo demo" + tarifas Meta por plantilla. → El "US$99+" de ChatGPT es **no
    verificable** en fuente primaria hoy.
  - **treble.io**: "AI work companion" (briefs diarios, priorización, correo). **Matiz 2:** no es
    software "de real estate"; es asistente general que lista real estate agents como un caso de
    uso. Precios públicos: **US$20/mes individual, US$100/mes team (5 usuarios, +$15 extra)** —
    el rango US$20-100 de ChatGPT calza.
- **Consecuencia:** treble.ai es enterprise/demo-gated → no es competidor directo del segmento
  pyme de dixdybot; solo referencia de techo. No citar "US$99" como dato.

---

## Qué cambia en nuestro análisis de pricing (tiers 4-6 UF / 8-12 UF)

1. **El tier 4-6 UF/mes queda VALIDADO por el mercado chileno real:** Lelemon cobra 3,8 UF solo
   por el agente público de WhatsApp y publica paquetes de 6,1-6,9 UF; herihe.digital parte en
   5 UF + IVA; ScaleTech "desde 6 UF". No estamos caros para un servicio gestionado.
2. **El tier 8-12 UF/mes es defendible pero exige diferenciación:** equivale aprox. al rango
   US$300-500/mes que Stammer documenta como precio de reventa estándar de un agente gestionado
   (y sus bundles $800-1.200 dan techo). Se sostiene SOLO con lo que los baratos no tienen:
   cotizador integrado, panel/CRM, entregas Supabase, entrenamiento continuo y resultados.
3. **Presión a la baja en la entrada:** Brote (US$29 + Free 50 conversaciones) y SuperPyme
   ($29.990-49.990 con IA) comoditizan el peldaño bajo. dixdybot NO debe competir ahí con
   software pelado: el tier de entrada se vende como "Done-for-You" (naming Botsify) con humano
   detrás, o no se vende.
4. **Cobrar implementación por separado queda validado por 3 actores:** Lelemon (5 UF una vez),
   SuperPyme ($49.990-390.000) y Stammer (US$2.500 sugerido). Nuestro plan debe incluir un
   setup fee explícito (sugerido: 5-10 UF según integraciones), cosa que hoy no está en los tiers.
5. **Correcciones a los informes externos:** descartar "WAI chileno en UF" (no existe tal cual);
   corregir la escalera SuperPyme en los tramos 4-5 ($79.990 y desde $149.990); no usar "US$99"
   para treble.ai; treble.io no es "real estate software".
6. **Ideas a robar ya:** onboarding por audio del dueño (Brote) y primer mes gratis + excedente
   por conversación en CLP (Lelemon) — ambas baratas de implementar con lo que ya tenemos.

### Fuentes principales (todas consultadas 2026-07-23)
- https://brote.ai/es
- https://lelemon.cl · linkedin.com/company/lelemon · cbinsights.com/company/lelemon
- https://artechclick.com/wai-info · https://iaworker.io/planes/ (los "WAI" reales encontrados)
- https://stammer.ai · https://stammer.ai/pricing
- https://botsify.com/pricing · https://botsify.com/pricing/whitelabel-ai-agents
- https://superpyme.cl · https://superpyme.cl/precios-bot-whatsapp/
- https://treble.ai · https://treble.io · hackceleration.com/es/labs/treble-precio (jun-2026)
