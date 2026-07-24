# Arbitraje: tarifas de WhatsApp Cloud API para Chile (jul-2026)

Fecha del arbitraje: 2026-07-23. Árbitro verificador (caso dixdybot).
Método: fuente primaria de Meta (rate card CSV oficial + docs de pricing, versión EN y ES),
descargada directamente del CDN de Meta el 23-jul-2026. Regla del dueño cumplida: cada dato
está respaldado por ≥2 artefactos (CSV USD + CSV CLP + página de pricing + página de
non-template messages en inglés y español).

## (a) Tarifa vigente para Chile — VEREDICTO

**Chile tiene fila PROPIA en el rate card de Meta** (ya no se factura por la banda
"Rest of Latin America"). Rate card oficial "Cost per message in USD on the WhatsApp
Business Platform, **effective July 1, 2026**" (CSV descargado del CDN de Meta, enlazado
desde https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/
sección "Rate cards and volume tiers"; copia local: `scratchpad/rates-usd.csv`):

| Mercado | Marketing | Utility | Authentication | Service |
|---|---|---|---|---|
| **Chile (USD)** | **US$0,0889** | **US$0,0200** | **US$0,0200** | n/a (gratis hoy; ver (b)) |
| Chile (CLP, card oficial en CLP) | CLP 78,4917 | CLP 17,6584 | CLP 17,6584 | n/a |
| Rest of Latin America (referencia) | US$0,0740 | US$0,0113 | US$0,0113 | n/a |

- Se cobra **por mensaje entregado** (modelo per-message, vigente desde 1-jul-2025).
- Los "Rest of Latin America" NO incluye a Chile (la lista oficial: Bolivia, Costa Rica,
  R. Dominicana, Ecuador, El Salvador, Guatemala, Haití, Honduras, Jamaica, Nicaragua,
  Panamá, Paraguay, Puerto Rico, Uruguay, Venezuela).
- Meta solo puede actualizar tarifas el día 1 de cada trimestre (1-ene / 1-abr / 1-jul /
  1-oct); esta tabla es la vigente del trimestre jul–sep 2026.

### Quién tenía razón
- **Gemini: CORRECTO.** Marketing US$0,0889 / utility y auth US$0,0200 — coincide exacto
  con el CSV oficial vigente.
- **Nuestra ronda 1: INCORRECTO para Chile.** US$0,074 / US$0,0113 son las tarifas de la
  banda "Rest of Latin America" del mismo rate card — banda a la que Chile ya no pertenece
  (Meta viene sacando mercados de las bandas "Rest of" trimestre a trimestre; a jul-2026
  Chile es mercado independiente).
- **ChatGPT (tabla SleekFlow): INCORRECTO como tarifa de Meta.** US$0,10224 = 0,0889 × 1,15
  exacto, y US$0,023 = 0,0200 × 1,15 exacto → es la tarifa de Meta **con ~15% de recargo de
  BSP/reseller**. La propia página de precios de SleekFlow dice que cobra los mensajes
  "based on SleekFlow [rate card]" (su propia tabla, no la de Meta), y su calculadora ni
  siquiera lista a Chile. No usar cifras de BSP como si fueran de Meta.

## (b) Cambio del 1-oct-2026 — CONFIRMADO EN FUENTE PRIMARIA DE META (no solo Twilio)

Página oficial de Meta "Upcoming pricing updates for Meta Business Agent, service and
utility messages" (developers.facebook.com/documentation/business-messaging/whatsapp/pricing/non-template-messages,
"Updated: Jul 1, 2026"; verificada en versión inglesa original y española el 23-jul-2026).
Citas textuales:

1. **"Effective October 1, 2026 - Meta will charge on a per-message basis for all service
   messages... These messages have not been charged since November 1, 2024."**
   → SÍ: los mensajes de servicio (respuestas libres dentro de la ventana de 24h) **dejan
   de ser gratis el 1-oct-2026** y pasan a cobrarse por mensaje entregado.
2. **"Effective October 1, 2026 - Meta will charge on a per-message basis for utility
   messages sent in response to users (within an open 24-hour customer service window).
   These messages have not been charged since July 1, 2025."**
   → SÍ: los utility dentro de ventana también dejan de ser gratis el 1-oct-2026.
3. **¿A qué tarifa?** "By market, rates for service messages are the same as the rates for
   utility and authentication messages." → Para Chile eso hoy es **US$0,0200/mensaje**
   (CLP 17,6584). **Sin volume tiers** para service. Meta publicará las tarifas definitivas
   que rigen desde el 1-oct-2026 **antes del 1-sep-2026** (compromiso explícito en la página).
4. Extra relevante: desde el **1-ago-2026** los mensajes del nuevo "Meta Business Agent"
   (IA de Meta) se cobran por token: US$2,00 por millón de tokens (~4-5 ¢/mensaje). Un bot
   con IA de terceros (nuestro caso: cerebro propio/Claude) NO cae ahí: sus respuestas
   no-plantilla son categoría **service**.
5. Siguen gratis: los mensajes dentro de la **ventana de 72h de free entry point**
   (click-to-WhatsApp Ads / botón de Facebook).

## (c) Costo mensual del bot (~120 conversaciones/mes × ~8 mensajes de servicio c/u)

Volumen: 120 × 8 = **960 mensajes de servicio/mes** (solo cuentan los mensajes que ENVÍA el
negocio; los del cliente no se cobran).

| Período | Tarifa por mensaje (Chile) | Costo mensual |
|---|---|---|
| Hoy → 30-sep-2026 | US$0 (service gratis en ventana 24h desde nov-2024) | **US$0** |
| Desde 1-oct-2026 | US$0,0200 (= tarifa utility/auth Chile vigente; definitiva antes del 1-sep-2026) | **960 × 0,0200 = US$19,20/mes** (~CLP $16.950 al card CLP oficial de 17,6584 CLP/msg) |

Sensibilidad: si la tarifa definitiva de oct-2026 subiera al nivel que cobra un BSP tipo
SleekFlow (+15%), serían ~US$22/mes. Impuestos (IVA 19%) pueden sumarse según la entidad de
facturación — no incluidos en el rate card.

**Contexto para el plan:** dixdybot HOY corre sobre Baileys (WhatsApp Web no oficial), donde
el costo por mensaje es $0. Estas cifras aplican SOLO si el rediseño migra a Cloud API. Si
se migra, presupuestar ~US$19-20/mes desde oct-2026 para el volumen actual (más marketing:
US$0,0889 por cada plantilla de marketing que se envíe, no incluida en el cálculo porque el
bot solo responde).

## Tabla final vigente (la que debe adoptar el plan)

| Categoría | Chile, por mensaje entregado (USD) | Vigencia | Fuente |
|---|---|---|---|
| Marketing | **US$0,0889** | desde 1-jul-2026 | Rate card CSV oficial Meta (USD), effective July 1, 2026 |
| Utility (fuera de ventana) | **US$0,0200** | desde 1-jul-2026 | ídem |
| Utility (dentro de ventana 24h) | **Gratis → US$0,0200 desde 1-oct-2026** | cambio 1-oct-2026 | Meta, doc non-template-messages (upd. 1-jul-2026) |
| Authentication | **US$0,0200** | desde 1-jul-2026 | Rate card CSV oficial |
| Service (respuestas en ventana 24h) | **Gratis → ~US$0,0200 desde 1-oct-2026** (misma tarifa que utility/auth; definitiva antes del 1-sep-2026) | cambio 1-oct-2026 | Meta, doc non-template-messages |
| Ventana 72h free entry point (ads CTWA) | Gratis (sin cambio anunciado) | — | Meta, pricing page |

### Fuentes primarias (todas consultadas 23-jul-2026)
1. Meta — Pricing on the WhatsApp Business Platform:
   https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/ (Updated: 1-jul-2026)
2. Meta — Rate card oficial USD (CSV, "effective July 1, 2026"), descargado del CDN de Meta
   enlazado desde la página anterior. Copia local: `rates-usd.csv` (Chile: 0.0889/0.0200/0.0200).
3. Meta — Rate card oficial CLP (CSV, mismo origen). Copia local: `rates-clp.csv`
   (Chile: 78,4917 / 17,6584 / 17,6584).
4. Meta — Upcoming pricing updates for Meta Business Agent, service and utility messages:
   https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/non-template-messages
   (Updated: Jul 1, 2026; verificada en EN y ES).
5. SleekFlow — página de pricing y calculadora (23-jul-2026): cobra por su propio rate card;
   su calculadora no lista Chile → sus cifras no son el rate card de Meta.
