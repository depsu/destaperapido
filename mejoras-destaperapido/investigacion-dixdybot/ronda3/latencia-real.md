# Latencia real del cerebro por CLI (`claude -p`) — bot vivo de destaperapido

**Claim de Gemini:** un cerebro por CLI tiene "latencia inaceptable de 5-10 segundos" para mensajería.
**Veredicto: REFUTADO en la conclusión, MATIZADO en la cifra.** La cifra real es incluso mayor
(mediana ~8 s estimada en producción, 15-18 s en medición directa), pero en un bot de WhatsApp
que **agrega 12-30 s de espera deliberada anti-ban** y donde un humano tarda 30-90 s en
responder, esa latencia no solo es aceptable: sobra margen.

## Fuentes (datos reales, no opinión)

- `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/bot.log` — 100 turnos reales
  del cerebro (líneas `→ Respondido a …`). El log NO trae timestamps, así que la latencia se
  reconstruyó cruzando cada turno con `data/conversaciones.jsonl` (que sí guarda `ts` ISO de
  cada mensaje cliente/bot). 30 turnos emparejables (el resto cae fuera de la ventana del
  jsonl actual, rotado el 22-jul).
- `bot.error.log` — solo ruido de descifrado Signal (Bad MAC); **0 timeouts del cerebro**
  (`excedió 120s`: 0 apariciones), **0 fallos** (`terminó con código`: 0).
- **Medición directa en vivo** (3 corridas del MISMO comando que usa `brain.js`:
  `claude -p <persona 10.6 KB + transcript> --output-format text --model opus`):
  **15.2 s, 16.1 s, 18.2 s** (incluye ~2-4 s de arranque del CLI).
- Script de reconstrucción: `scratchpad/latencia.py` (mismo directorio base del scratchpad).

## Método de reconstrucción

`gap = ts(primer globo del bot) − ts(último mensaje del cliente)`, y de ahí
`cerebro ≈ gap − debounce nominal − simulación de tipeo nominal`, donde los delays
deliberados son conocidos por código y `.env`:

- Debounce anti-ban (`gating.js`): **30 s** primera respuesta del chat, **12 s** las
  siguientes, con jitter ±30% (por eso 5/30 estimados salen negativos: ruido de ±3.6-9 s
  por turno; la mediana lo absorbe).
- Simulación de tipeo (`index.js`): `clamp(len×45 ms, 1.5 s, 9 s)` por globo — calculable
  por turno porque el texto del globo está en el jsonl.

## Resultados (n=30 turnos de producción)

| Métrica | GAP total (lo que vive el cliente) | CEREBRO estimado (sin delays deliberados) |
|---|---|---|
| Mediana | **22.6 s** | **8.2 s** |
| p90 | **46.5 s** | **16.6 s** |
| Máximo | **60.6 s** | **25.2 s** |

Por tipo de turno: primera respuesta (debounce 30 s, n=6) cerebro mediana 13.7 s;
siguientes (debounce 12 s, n=24) mediana 7.1 s, p90 16.6 s.

La medición directa (15-18 s con opus, prompt frío de 10.6 KB) sugiere que la mediana
"real" del proceso `claude -p` completo está entre la estimada (8 s) y los 18 s; el rango
honesto para el cerebro es **~8-18 s típico, 25 s peor caso observado**, con timeout duro
de 120 s + 1 reintento que en los logs actuales **nunca se disparó**.

## Evaluación del claim

1. **La cifra "5-10 s" se queda corta**, no larga: el cerebro real (CLI + opus) tarda más
   que eso en frío. Si Gemini quería asustar con la magnitud, el dato real es peor y aun
   así no importa (punto 2).
2. **"Inaceptable" es falso en este dominio.** El bot ESPERA A PROPÓSITO 12-30 s antes de
   responder (anti-ban + chance a que conteste el humano) y luego simula tipeo 1.5-9 s.
   El cerebro piensa dentro/alrededor de esa ventana: quitarle latencia al cerebro NO
   aceleraría la respuesta percibida, porque el cuello es el delay deliberado.
3. **Contexto humano:** una persona tarda 30-90 s en contestar un WhatsApp comercial. El
   gap total real del bot (mediana 22.6 s, p90 46.5 s, máx 60.6 s) está **dentro o por
   debajo** de ese rango — responder más rápido sería sospechoso (el jitter existe
   exactamente por eso, comentario en `gating.js:32`).
4. **Confiabilidad:** 0 timeouts y 0 fallos del cerebro en los logs vigentes; el diseño
   ya cubre el peor caso (timeout 120 s + reintento único + `[[SILENCIO]]`).
5. **Dónde SÍ tendría razón Gemini:** en un canal de chat en vivo tipo webchat con
   expectativa de respuesta <2 s, o para features tipo "escribiendo..." en streaming, un
   CLI sin streaming sería lento. Ese no es este caso de uso.

**Conclusión para el plan:** mantener `BRAIN_MODE=cli`. La latencia del CLI es un
no-problema para WhatsApp: queda enmascarada por los delays anti-ban deliberados y el
resultado total imita bien a un humano. Migrar a API por latencia sería optimizar el
componente equivocado (y contradiría la doctrina DIXDY de no reinventar infraestructura).
