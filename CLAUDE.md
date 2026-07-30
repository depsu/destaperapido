# destaperapido.cl

Cliente DIXDY: destapes exprés + cotizador. Este CLAUDE.md nació en la mudanza (jul 2026);
complétalo al trabajar aquí.

> **🧭 Doctrina DIXDY (obligatoria):** este clon es parte del sistema DIXDY. NO agregues APIs
> de Anthropic, loops, crons ni workers nuevos sin revisar primero los motores que YA existen
> (rondas de correo/ads/scout, cola única, timbre v2): lee
> `/Users/alejandroriveracarrasco/SaSS/DIXDY/docs/23-doctrina-dixdy.md`. Guardián v2: OK de
> Alejandro SOLO para plata o gestión externa. Registra lo que hagas con
> `python3 /Users/alejandroriveracarrasco/SaSS/DIXDY/scripts/actividad.py` y promueve al
> maestro toda mejora reutilizable.

## 🛣️ Proyecto dixdybot (rediseño del whatsapp-bot) — LEER ANTES de tocar el bot

Investigación completa (34 agentes, jul-2026) y plan por etapas E0-E7 para evolucionar el
bot vivo (que corre en `~/SaSS/destaperapido/whatsapp-bot/`, fuera de este clon) a un
producto genérico multi-rubro. **Empieza por `mejoras-destaperapido/DIXDYBOT-ESTADO.md`**
(estado, requisitos no negociables de Alejandro — genérico-modular, design system único,
IA madre multi-agente, escepticismo de fuentes — mapa de documentos y fechas duras; el plan
vigente completo está en `mejoras-destaperapido/investigacion-dixdybot/ronda2/plan-revisado.md`).
No agregues features al bot fuera de ese plan sin revisarlo primero.

## Mapa de aplicaciones de este cliente (por completar)

- `api/` — API del cotizador (genera cotizaciones; revisar endpoints antes de tocar).
- `mejoras-destaperapido/` — backlog de mejoras del sitio.
- IDs: ver `administration/dashboard/data/clientes.json` del maestro (ads.customer_id
  3106881217 **VERIFICAR** — lo dedujo la ronda por landing pages).

## Reglas conocidas

- Google Ads: analizar con MCP (lectura GAQL); mutaciones SOLO por scripts del maestro con
  el flujo del Guardián. Campañas apuntan a cliente de ALTA intención.

## Contexto rápido: grafo del maestro 🕸️

El mapa de conocimiento de TODO el sistema (método, scripts, skills, workers) vive en el
maestro — este clon NO genera grafo propio. Antes de explorar a ciegas:
`graphify explain "X" --graph /Users/alejandroriveracarrasco/SaSS/DIXDY/graphify-out/graph.json`
(o `graphify path "A" "B" --graph <misma ruta>`). Vista visual: dashboard → 🕸️ Grafo.
