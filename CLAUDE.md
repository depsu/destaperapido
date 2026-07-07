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

## Mapa de aplicaciones de este cliente (por completar)

- `api/` — API del cotizador (genera cotizaciones; revisar endpoints antes de tocar).
- `mejoras-destaperapido/` — backlog de mejoras del sitio.
- IDs: ver `administration/dashboard/data/clientes.json` del maestro (ads.customer_id
  3106881217 **VERIFICAR** — lo dedujo la ronda por landing pages).

## Reglas conocidas

- Google Ads: analizar con MCP (lectura GAQL); mutaciones SOLO por scripts del maestro con
  el flujo del Guardián. Campañas apuntan a cliente de ALTA intención.
