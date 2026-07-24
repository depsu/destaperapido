# Arbitraje: Voice AI en español — cifras de ChatGPT vs Gemini vs Claude

Fecha de verificación: 2026-07-23. Todas las cifras leídas HOY en las páginas oficiales de
pricing y docs (fuentes primarias, mínimo 2 páginas por proveedor). Búsqueda web no disponible
en esta sesión (cupo agotado); todo se verificó por fetch directo a los sitios oficiales, que
es de todos modos la fuente primaria exigida.

## 1. Precios vigentes (verificados 2026-07-23)

### Retell AI — retellai.com/pricing + docs.retellai.com
- Rango oficial en portada: **US$0,07–0,31/min** ("Only pay for the minutes you use").
- Componentes: infraestructura de voz **$0,055/min** + TTS **$0,015/min** (voces
  Retell/Cartesia/Minimax/Fish/OpenAI) o **$0,040/min** (ElevenLabs) + LLM según modelo
  (Gemini 2.5 Flash Lite $0,006 · GPT-4.1 $0,045 · Claude 4.6 Sonnet $0,08 · GPT-5.5 $0,16)
  + telefonía **$0,015/min** (Twilio EE.UU.; varía por país).
- Sin cuota mensual; $10 de crédito gratis al partir; Enterprise a medida.
- **Stack económico en español: ~US$0,09–0,13/min todo incluido.**
- Veredicto: ChatGPT ($0,07–0,31) = literal del sitio, CONFIRMADO. Gemini ($0,055 base →
  total $0,115–0,15) = MATIZADO: el $0,055 es solo el motor de voz; su total es plausible
  pero recorta el rango real.

### Vapi — vapi.ai/pricing + docs.vapi.ai
- Plataforma: **US$0,05/min** + proveedores (STT/LLM/TTS) **at-cost** (o BYO API key = $0
  por esa pata) + telefonía aparte. 10 líneas concurrentes incluidas; extra $10/línea/mes.
- Los docs oficiales (`assistants/model-intelligence/understanding-cost.md`) explican SOLO la
  metodología de estimación; **ninguna página oficial publica un "total real" por minuto**.
- Con stack económico (Deepgram + GPT-4.1-mini/Gemini + Cartesia): ~US$0,10–0,15/min.
  Con stack premium (ElevenLabs TTS + GPT frontier): puede llegar a $0,25–0,33.
- Veredicto: ChatGPT ($0,05 base + at-cost) CONFIRMADO. Gemini ($0,25–0,33 "total") =
  NO-VERIFICABLE como cifra oficial; es el extremo caro, no el típico.

### Bland — bland.ai/pricing + docs.bland.ai
- **Start (sin cuota): $0,14/min** hablado, $0,05/min transferencia, todo incluido (LLM +
  transcripción + voces premium, "no separate token charges"); telefonía aparte/pass-through.
- **Build: $0,12/min + US$299/mes** · **Scale: $0,11/min + US$499/mes** · Enterprise custom.
- Veredicto: Gemini ($0,14/min + planes $299/$499) CONFIRMADO casi textual.

### ElevenLabs Agents — elevenlabs.io/pricing (pestaña agentes) + docs
- Planes/mes con minutos de agente incluidos: Free $0 (15 min) · Starter $6 (75) · Creator
  $22 (275) · Pro $99 (1.238) · **Scale $299 (3.738 min)** · Business $990 (12.375) ·
  Enterprise custom. Overage estándar **$0,08/min** ($0,16 en burst de concurrencia).
- El **LLM se cobra aparte** (pass-through descontado de créditos, según modelo elegido).
- Minuto efectivo en Scale: 299/3.738 ≈ **$0,080/min + LLM** → ~$0,09–0,12/min real.
- Veredicto: ChatGPT ("hasta $299/mes Scale") MATIZADO: Scale $299 existe y está confirmado,
  pero no es el techo (Business $990) y se puede partir desde $6–22/mes; además el LLM va aparte.

### Pipecat — github.com/pipecat-ai/pipecat + docs.pipecat.ai + voiceaiandvoiceagents.com
- Open source real: **BSD-2-Clause, 13,7k estrellas, v1.6.0 del 21-jul-2026** (muy activo).
- Latencia: la guía oficial del equipo Daily/Pipecat fija **1.500 ms como objetivo práctico**
  y solo "hemos demostrado agentes de 500 ms" **co-alojando todos los modelos en un clúster
  GPU propio optimizado**. Regla LLM: TTFT ≤600 ms.
- Veredicto: ChatGPT ("500–800 ms DIY") MATIZADO: el número existe pero es el caso de
  laboratorio, no lo que logra un DIY normal (~1–1,5 s realista). Costo = suma de proveedores
  (~$0,03–0,10/min) **más toda la ingeniería y hosting**, que es el costo real oculto.

## 2. Español (¿y chileno?) — verificado en docs

- **Retell**: 86 idiomas; español como **es-ES y es-419** en todos sus STT (Deepgram, Azure,
  Soniox, AssemblyAI) y TTS. (docs.retellai.com/build/language-support.md, 2026-07-23)
- **Vapi**: español vía Deepgram Nova-2/3 "Multi", Google (125+), Gladia (code-switching);
  TTS Azure/ElevenLabs/PlayHT con voces en español. (docs.vapi.ai/customization/multilingual)
- **Bland**: parámetro `language` acepta **es, babel-es, es-419**. Sin es-CL ni es-MX.
  (docs.bland.ai/api-v1/post/calls, 2026-07-23)
- **ElevenLabs Agents**: **31 idiomas** incl. español (modelo v2.5 Multilingual).
- **es-CL de verdad solo existe vía Azure Speech**: STT es-CL + voces TTS
  **es-CL-CatalinaNeural / es-CL-LorenzoNeural** (learn.microsoft.com, 2026-07-23). Azure es
  proveedor de voz en Vapi y en Pipecat; Retell y Bland ofrecen es-419 (latino neutro), que
  para Chile suena aceptable pero no chileno. Ningún externo mencionó este matiz.

## 3. "Llamada → resumen → WhatsApp" ¿documentada?

- **Ningún proveedor documenta la cadena completa de punta a punta.** Lo que SÍ está
  documentado, por partes:
  - Retell: post-call analysis automático (summary/sentiment/campos custom) + webhooks
    (`call_analyzed`); tiene SMS nativo pero **no WhatsApp**.
  - Vapi: resumen automático (`summaryPrompt` en `analysisPlan`) + webhook
    **`end-of-call-report`** con transcript, grabación y análisis. Sin WhatsApp.
  - Bland: `summary_prompt` + `webhook` al terminar la llamada. Sin WhatsApp.
  - **ElevenLabs Agents: única con integración WhatsApp NATIVA documentada**
    (docs.elevenlabs.io/eleven-agents/whatsapp.md): mensajes in/outbound con plantillas,
    **llamadas de voz entrantes Y salientes por WhatsApp Business**, envío de mensajes con
    tools durante/tras la conversación. Ojo: exige WhatsApp Business (Cloud API de Meta) y
    Meta cobra las salientes fuera de la ventana de servicio.
  - Pipecat: `WhatsAppTransport` documentado (llamadas de voz **entrantes** por WhatsApp
    Business Calling API, WebRTC).
- Conclusión práctica para dixdybot: la pata "→ WhatsApp" **ya la tenemos en casa** (el bot
  Baileys). Cualquier proveedor con webhook post-llamada (los 4) cierra la cadena con ~20
  líneas nuestras: webhook → outbox del bot → WhatsApp al dueño/cliente. No hay que comprarla.

## 4. Cierre: costo real todo incluido y encaje con E7

**Costo real por minuto, agente de voz en español, todo incluido (jul-2026):**
- Retell: **US$0,09–0,13/min** (stack económico; sobre oficial $0,07–0,31) — sin cuota fija.
- Bland: **US$0,14/min** plano sin cuota (el más fácil de presupuestar) + telefonía.
- ElevenLabs: **≈US$0,08/min + LLM** (≈$0,09–0,12) con plan desde $6/mes; sin telefonía si la
  llamada va por WhatsApp.
- Vapi: **US$0,05 + proveedores** → $0,10–0,20 típico ($0,25+ solo con stack premium).
- Pipecat: $0,03–0,10/min en proveedores, pero el costo real es construir y operar (E7 dice
  explorar, NO construir → descartado como primera opción).

Una llamada perdida recuperada dura ~2–4 min → **US$0,25–0,55 por llamada (~CLP $250–550)**.
Contra un destape de CLP $40.000+, el costo por minuto es irrelevante; lo que manda es el
encaje operativo.

**Recomendación para dixdybot E7 (explorar):**
1. **Piloto con Retell**: pricing por componentes transparente, es-419 documentado, post-call
   analysis + webhook, $10 gratis, sin mensualidad. El webhook alimenta el WhatsApp que ya
   opera dixdybot. Presupuesto piloto: ~US$0,10–0,13/min.
2. **Candidato B: ElevenLabs Agents** si algún día se quiere el agente DENTRO de WhatsApp
   (voz + texto nativos), pero implica migrar a WhatsApp Business API oficial — dixdybot hoy
   usa Baileys (no oficial), así que es un cambio de canal, no un plug-in.
3. **Vapi** solo si se exige voz chilena real (Azure es-CL Catalina/Lorenzo vía Vapi).
4. **Pipecat**: monitorear, no construir (E7). Su claim de 500 ms es de laboratorio.

**Sobre los externos**: Gemini sobreestimó Vapi ($0,25–0,33 no es cifra oficial ni el caso
típico) y acertó Bland al peso; ChatGPT citó bien los rangos de portada (Retell, Vapi) pero
le faltaron los matices de ElevenLabs (LLM aparte, Business $990) y vendió la latencia de
laboratorio de Pipecat como DIY. Ninguno de los dos detectó el hallazgo más útil para este
cliente: **ElevenLabs es el único con WhatsApp nativo documentado, y es-CL real solo existe
vía Azure**.

## Fuentes (todas leídas 2026-07-23)
- https://www.retellai.com/pricing · https://docs.retellai.com/build/language-support.md ·
  https://docs.retellai.com/features/post-call-analysis-overview.md · https://docs.retellai.com/llms.txt
- https://vapi.ai/pricing · https://docs.vapi.ai/customization/multilingual ·
  https://docs.vapi.ai/assistants/call-analysis · https://docs.vapi.ai/server-url/events ·
  https://docs.vapi.ai/assistants/model-intelligence/understanding-cost.md
- https://www.bland.ai/pricing · https://docs.bland.ai/api-v1/post/calls
- https://elevenlabs.io/pricing (pestaña Agents) ·
  https://elevenlabs.io/docs/eleven-agents/customization/voice/customization/language.md ·
  https://elevenlabs.io/docs/eleven-agents/whatsapp.md
- https://github.com/pipecat-ai/pipecat (v1.6.0, 21-jul-2026) · https://docs.pipecat.ai/llms.txt ·
  https://docs.pipecat.ai/pipecat/features/whatsapp.md · https://voiceaiandvoiceagents.com
- https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts (es-CL)
