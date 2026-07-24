# Procesar audio/imagen/video/documentos con IA — estado julio 2026, para dixdybot

**Fecha de investigación: 23-jul-2026.** Caso de uso: cliente de destape manda foto del baño
tapado o del terreno, nota de voz en español chileno con dirección/pedido, video corto del
problema, o PDF/boleta. Volumen: ~120 conversaciones/mes, ~20% con media (~24 conv/mes).
Nota: la sesión agotó el cupo de WebSearch; todo lo de abajo viene de **fetch directo a docs
oficiales** (fechados 23-jul-2026) o de archivos del propio proyecto.

---

## (a) Claude API: ¿acepta audio en 2026? NO. Solo texto + imagen + PDF

**Verificado en docs oficiales (23-jul-2026):** la página de modelos de Anthropic dice
textual: *"All current Claude models support text and image input, text output"*. Ni la
página de Vision ni la de PDF ni el catálogo de modelos mencionan audio o video como
entrada. El FAQ de Vision confirma que Claude es *"an image understanding model only"* (no
genera ni acepta otras modalidades). **Conclusión: para notas de voz se necesita un
transcriptor externo, sí o sí.**

### Visión Claude — cifras oficiales (23-jul-2026)

- **Tokenización:** parches de 28×28 px → `⌈ancho/28⌉ × ⌈alto/28⌉` tokens visuales.
- **Dos tiers de resolución:**
  - **High-res** (Fable 5, Opus 4.8/4.7, Sonnet 5): lado largo máx 2576 px, tope 4784
    tokens/imagen. Automático, sin beta.
  - **Estándar** (Haiku 4.5 y anteriores): lado largo máx 1568 px, tope 1568 tokens/imagen.
- **Ejemplos oficiales:** foto 1920×1080 = 1560 tokens (estándar) / 2691 (high-res); foto
  4K = 1560 / 4784. Una foto de WhatsApp (comprimida ~1600×1200) ≈ 1,5k tokens en tier
  estándar, ~2,5-3,9k en high-res.
- **Costo por foto** (input): en Sonnet 5 ($3/MTok) ≈ **US$0,005-0,012/foto**; en Haiku 4.5
  ($1/MTok) ≈ US$0,0016/foto. Doc oficial: 1000×1000 px ≈ $1,30 por mil imágenes en Haiku.
- **Caching:** `cache_control` funciona sobre bloques `image` como cualquier bloque
  (lectura ~0,1×, escritura 1,25×). Para nuestro caso (imagen única por conversación) el
  caching relevante es el del system prompt, no el de la imagen.
- **Límites por request:** hasta **100 imágenes** (modelos 200k) / **600** (modelos 1M);
  >20 imágenes activa límite estricto de 2000 px por lado. Máx 10 MB por imagen (base64),
  8000×8000 px, request total 32 MB. Formatos: JPEG, PNG, GIF, WebP.
- **Bonus sencillez:** en modo cerebro `claude -p` (suscripción, el modo actual del bot),
  Claude Code **lee imágenes por ruta de archivo** con su tool Read → costo marginal $0
  hasta el failover a API.

## (d) Documentos: PDF nativo en Claude (verificado 23-jul-2026)

- Bloque `document` base64, **sin beta**; también por Files API o URL.
- Límites: **32 MB por request; 600 páginas** (100 si el contexto es <1M tokens). PDF
  estándar sin contraseña.
- **Costo:** cada página se procesa como texto extraído + imagen de la página:
  **1.500-3.000 tokens de texto/página** + tokens de imagen (regla de visión). Sin fee
  adicional. Doc oficial: PDF de 3 páginas ≈ 7.000 tokens (~US$0,02 en Sonnet 5). Una
  boleta de 1 página ≈ 3-8k tokens ≈ US$0,01-0,03.
- Cacheable con prompt caching; compatible con Batches (50% dcto, no aplica a chat en vivo).

## (b) Transcripción de notas de voz en español — comparativa (precios verificados 23-jul-2026)

| Opción | Precio | Notas (fechadas 23-jul-2026) |
|---|---|---|
| **Groq whisper-large-v3-turbo** | **$0,04/hora** (≈$0,00067/min), mínimo 10 s/request | 216x tiempo real (una nota de 60 s se transcribe en <1 s de cómputo). Multilingüe (es). **Acepta `ogg` directo** — el formato de las notas de voz de WhatsApp (OGG/Opus vía Baileys) → sin conversión ffmpeg. Máx 25 MB (free) / 100 MB (dev). |
| Groq whisper-large-v3 | $0,111/hora | Misma familia, algo más preciso, 189x. |
| **OpenAI gpt-4o-transcribe** | ≈**$0,006/min** ($2,50/MTok audio in) | Mejor WER que whisper clásico en benchmarks de OpenAI; **no acepta ogg** → habría que convertir con ffmpeg. `gpt-4o-mini-transcribe` ≈$0,003/min. |
| Deepgram Nova-3 | $0,0077/min pre-grabado (mono) / $0,0092 multilingüe; streaming $0,0048-0,0058/min (promo) | Español dentro de 45+ idiomas. Nova-2 descontinuado. Fuerte en streaming/voz en vivo (más relevante para E7 voz que para notas). |
| AssemblyAI | Universal-2 **$0,15/hora**; Universal-3.5 Pro $0,21/hora | Español soportado. Slam-1 y nano deprecados. |
| ElevenLabs Scribe v2 | **$0,22/hora** (todos los planes); Scribe v2 Realtime $0,39/hora | Con diarización; el más caro de la lista para batch. |
| Gemini 2.5 Flash (audio nativo) | Audio = 32 tokens/s (1 min = 1.920 tokens) × $1,00/MTok ≈ **$0,0019/min** + output | No es solo transcripción: entiende el audio en contexto. Flash-Lite: $0,30/MTok audio ≈ $0,0006/min. Pero es un **proveedor nuevo** solo para esto. |
| **Whisper large-v3-turbo LOCAL (whisper.cpp, Mac)** | **$0** | Viable: whisper.cpp es "Apple Silicon first-class citizen" (NEON, Accelerate, Metal, Core ML); encoder en ANE = ">3x más rápido que solo-CPU" (README oficial, cifra cualitativa — benchmarks numéricos viven en el issue #89, no verificados aquí). Soporta large-v3-turbo. Memoria: modelo large ~3,9 GB RAM (turbo menor, no listado). Contra: binario + modelo + mantención = infra nueva en el Mac. |

**Calidad en español chileno:** ninguna fuente verificable hoy publica WER específico
"es-CL". Whisper large-v3 es el estándar de facto multilingüe y es la base de Groq; para
notas de voz cortas con dirección/pedido cualquier opción de la tabla sirve — el
diferenciador real es formato (ogg directo), latencia y sencillez, no el WER.

## (c) Video (clips 10-30 s): frames + visión Claude vs Gemini nativo

- **Gemini nativo** (verificado 23-jul-2026): video ≈ **300 tokens/s** (default) o 100
  tokens/s (low-res), audio del video incluido (1 fps + audio 1Kbps). Clip de 30 s ≈ 9-10k
  tokens → en Gemini 2.5 Flash ($0,30/MTok) ≈ **$0,003/clip**. Baratísimo, PERO es un
  tercer proveedor de IA solo para un caso marginal.
- **Frames + Claude** (reusa proveedores existentes): ffmpeg extrae 6-8 frames (re-escalados
  a ≤1092 px ≈ 1,5k tokens c/u) + pista de audio → Groq. Clip de 30 s ≈ 9-12k tokens ≈
  **$0,03-0,04/clip en Sonnet 5** (o $0 en modo suscripción `claude -p`). ffmpeg ya es
  dependencia habitual del stack Baileys.
- **Veredicto:** a 2-3 clips/mes, la diferencia es de centavos. **Frames+Claude gana por
  sencillez** (cero proveedores nuevos); Gemini queda anotado como plan B si el volumen de
  video explota (×100).

## (e) Patrón 2026 de los productos serios

- **Normalizar al ingreso, siempre — no bajo demanda.** El costo de transcribir/describir
  es tan bajo (tabla arriba) que el patrón dominante es convertir TODA media entrante a
  **texto anotado en el hilo** en el momento de recepción: `[🎤 nota de voz: "..."]`,
  `[📷 foto: baño con WC rebalsado, agua en el piso]`. Razones estructurales que aplican
  1:1 a dixdybot: (1) la ventana de contexto del cerebro (HISTORY_LIMIT=60) es texto; (2)
  los loops de aprendizaje, dedup (envios.jsonl) y el panel operan sobre texto; (3) el
  binario NO debe viajar por el bus — exactamente el plano `guardarMedia(msg)` bajo demanda
  de builderbot ya adoptado en `ronda4/planos-sintesis.md` (binario a disco, referencia en
  el evento).
- **La imagen se manda al modelo UNA vez** (al ingreso) y al hilo va la anotación de texto;
  el archivo queda en disco para re-análisis bajo demanda (p.ej. si el especialista de
  cotización necesita más detalle, segundo pase de visión con pregunta específica).
- **Hallazgo de la ronda 4 (23-jul-2026):** ninguno de los 8 repos OSS leídos (NanoClaw,
  Parlant, Mastra, BuilderBot, Chatwoot, etc.) procesa media con IA — solo la guardan/
  reenvían. El pipeline de media-a-texto es de lo "genuinamente nuestro".
- El bot vivo hoy solo lee el **caption** de imageMessage/videoMessage
  (`whatsapp-bot/src/index.js:49-50`) — la media en sí se ignora: todo esto es capacidad
  nueva.

## (f) Recomendación para dixdybot — pipeline por tipo (SENCILLEZ: 1 solo proveedor nuevo)

**Proveedores: Claude (ya existe) + Groq (único nuevo). Nada local obligatorio, nada de
Gemini.** Todo entra por un módulo `media.js` administrable desde el panel (on/off por tipo,
requisito genérico-modular), que corre ANTES del cerebro y deja texto anotado en el hilo.

1. **🖼️ Foto** → guardar a disco (guardarMedia) → re-escalar a ≤1568 px lado largo →
   modo `cli`: pasar la RUTA al cerebro (Claude Code la lee; costo $0 suscripción); modo
   API: bloque `image` base64 en el turno. Anotación de 1-2 líneas al hilo. ~$0,01/foto
   en API.
2. **🎤 Nota de voz** → el OGG/Opus de Baileys **directo a Groq whisper-large-v3-turbo**
   (`language: "es"`, sin ffmpeg) → transcripción al hilo como texto del cliente.
   Latencia ~1-2 s total: invisible dentro de la mediana de 22,6 s del bot.
   **Fallback sin segundo proveedor:** si Groq falla, el bot responde "no pude escuchar tu
   audio, ¿me lo escribes? 🙏" (pausa-y-pregunta; a 10-20 notas/mes un segundo transcriptor
   es sobre-ingeniería). Opción futura documentada: whisper.cpp local en el Mac (privacidad
   Ley 21.719, $0) — más infra, solo si Groq molesta.
3. **🎬 Video 10-30 s** → ffmpeg: 6-8 frames + pista de audio → frames a visión Claude,
   audio a Groq → una anotación combinada al hilo. ~$0,03/clip.
4. **📄 PDF/boleta** → bloque `document` de Claude (sin beta, base64) → resumen anotado al
   hilo. ~$0,01-0,03/doc.
5. **Regla transversal:** binario a disco con referencia en eventos.jsonl; al bus y al hilo
   solo texto; anotar SIEMPRE al ingreso.

**Costo mensual estimado a nuestro volumen** (24 conv con media/mes ≈ 20 fotos + 10 notas
de voz de ~45 s + 2-3 videos + 1-2 PDFs): Groq ≈ **US$0,01** · visión/PDF Claude ≈
US$0,25-0,35 (y **$0 mientras el cerebro corra por suscripción `claude -p`**) → **total
< US$0,50/mes**; con tráfico ×10 sigue bajo US$5/mes. El costo de media es ruido frente al
cerebro; la decisión se toma por sencillez, no por precio.

**Encaje en el plan:** el módulo media entra natural en **E2** (conocimiento como datos +
convenciones: eventos.jsonl ya define dónde anotar) o como sub-entrega de **E1** (llm.js
puerta única: la anotación de media es un pre-paso del mismo pipeline). No requiere
infraestructura nueva (sin colas, sin workers): una función async antes del cerebro.

---

## Fuentes

- https://platform.claude.com/docs/en/build-with-claude/vision.md (fetch 23-jul-2026)
- https://platform.claude.com/docs/en/build-with-claude/pdf-support.md (fetch 23-jul-2026)
- https://platform.claude.com/docs/en/about-claude/models/overview.md (fetch 23-jul-2026 — "text and image input" única modalidad de entrada)
- https://groq.com/pricing/ y https://console.groq.com/docs/speech-to-text (fetch 23-jul-2026)
- https://deepgram.com/pricing (fetch 23-jul-2026)
- https://developers.openai.com/api/docs/pricing (fetch 23-jul-2026)
- https://www.assemblyai.com/pricing (fetch 23-jul-2026)
- https://elevenlabs.io/pricing/api (fetch 23-jul-2026)
- https://ai.google.dev/gemini-api/docs/pricing · /docs/audio · /docs/video-understanding (fetch 23-jul-2026)
- https://github.com/ggml-org/whisper.cpp (README, fetch 23-jul-2026)
- /Users/alejandroriveracarrasco/SaSS/DIXDY/clientes/destaperapido/mejoras-destaperapido/investigacion-dixdybot/ronda4/planos-sintesis.md
- /Users/alejandroriveracarrasco/SaSS/DIXDY/clientes/destaperapido/mejoras-destaperapido/DIXDYBOT-ESTADO.md
- /Users/alejandroriveracarrasco/SaSS/DIXDY/whatsapp-bot/src/index.js (líneas 49-50)
