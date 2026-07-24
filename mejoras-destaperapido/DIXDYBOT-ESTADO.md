# DIXDYBOT — Estado del proyecto y mapa de documentos

**Última actualización:** 24-jul-2026 (post-ronda 8) · **Estado: investigación COMPLETA
(8 rondas, ~70 agentes + 2 deep research externos arbitrados) + DISEÑO CONGELADO
(prototipo v5, 18 iteraciones con Alejandro: `dixdybot-prototipo-v5-congelado.html`,
artifact 555843ca) + esqueleto/contrato/plan de arranque listos
(`investigacion-dixdybot/ronda8/`). Construcción NO iniciada.**
Próximo paso: **Semana 0 en doble carril** (E0 cinturón sobre el bot vivo + pre-etapa Meta
+ esqueleto D1 compilable) cuando Alejandro dé el vamos — ver
`ronda8/plan-arranque-backend.md` (el plan rector del backend, semana a semana hasta dic).
Decisiones nuevas de producto (prototipo + memorias): pausa junior→senior multi-fase,
caminos con guía conversacional, módulos con APORTES, conexiones con chat+permisos,
tablero/etapas como datos, chats con bautizo/orden-por-atención/dormidos, onboarding de
negocio, correo multi-modo. El proyecto nuevo NACE de cero limpio (repo dixdybot/ en el
maestro, ver `ronda8/esqueleto-proyecto.md`); jamás se clona el bot viejo.

## Qué es

Rediseño del whatsapp-bot vivo de destaperapido (corre en
`~/SaSS/destaperapido/whatsapp-bot/`, FUERA de este clon) hacia **dixdybot**: producto
genérico multi-rubro y multi-canal (WhatsApp hoy, Instagram después), con cerebro Claude y
entrenamiento por **caminos** (conocimiento como rutas condición→acción versionadas, con
pausa-de-tema + pregunta al dueño + aprendizaje en caliente). El bot actual vende HOY: se
evoluciona por etapas en el mismo repo, sin sistema paralelo.

## Requisitos fijados por Alejandro (no negociables)

1. **Genérico-modular:** toda capacidad = módulo activable/configurable desde el panel;
   funciones nuevas de Claude Code nacen administrables; nada cableado al rubro.
2. **Design system único** (arranque de E2): referencias Chatwoot/Fin/Typebot/Linear →
   tokens+componentes en Claude Design (claude.ai/design, DesignSync) → cero variaciones.
3. **IA madre + agentes especialistas** (supervisor/handoff): router barato deriva EN
   SILENCIO al agente del rubro; cada agente carga solo los caminos de su dominio. El campo
   dominio/agente entra al esquema de camino desde el día 1 de E3.
4. **Escepticismo:** ninguna decisión se apoya en una sola fuente; verificar, fechar,
   evaluar encaje con la idea propia.

## El plan (resumen — detalle en ronda2/plan-revisado.md)

E0 cinturón (commit fixes vivos, alarma bot-ciego, circuit breaker, pins, backup sesión,
**verificar entrega real ✓✓ — Error 463 activo en Baileys**) → E1 **prioridad #1**: llm.js
puerta única + failover suscripción→API (por ToS/límites, NO por latencia: medida real del
cerebro 8-18s, total percibido 22,6s mediana = rango humano) → E2 conocimiento como datos +
vista Conocimiento + design system **+ 3 convenciones de plataforma (+2-3 días): convId
canónico (nada nuevo con clave jid), JSON Schema + vista Ajustes renderizada desde schema,
eventos.jsonl** → E3 caminos v1 (arranque en frío 68 reglas→20-30 caminos, pausa-de-tema,
backtesting patrón Fin, validación patrón Decagon, aviso por WhatsApp con código 5 letras)
→ E4 canal-como-enchufe + canal sim + único escritor → E5 canales oficiales Meta
(**Coexistence = ruta objetivo; 30-sep es fecha de DECISIÓN tras piloto en número
secundario, con Baileys de fallback caliente 30-60 días**; Instagram en una tarde) → E6
producto multi-cliente (API key por cliente; tiers 4-6 / 8-12 UF/mes **+ setup fee 5-10
UF**; clon-por-cliente, NO tenant_id) → E7 exploratoria voz (piloto Retell, ~US$0,09-0,15/
min todo incluido). Regla: la fecha del canal manda.

**Fechas duras:** 1-sep tarifas Chile definitivas · 30-sep decisión Coexistence ·
1-oct Meta cobra TODOS los service y utility en ventana 24h (Chile hoy US$0,0200/msg →
~US$20/mes a nuestro volumen; rate card oficial: marketing 0,0889/utility 0,0200) ·
**1-dic-2026 Ley 21.719 de datos**: antes de esa fecha, contrato de encargo de tratamiento
por cliente + derechos ARCO+P en el panel (el art. 8 bis hace del humano-en-el-loop un
requisito legal). HOY ya rige la 19.496: confirmación escrita de compra, retracto 10 días,
información veraz; y presentarse como asistente virtual anticipa la ley de IA en trámite.

## Mapa de documentos (en `mejoras-destaperapido/`)

- `DIXDYBOT-INVESTIGACION.md` — informe maestro ronda 1 (diagnóstico con evidencia,
  caminos validados, canales, Claude Code vs API, plan original E0-E6).
- `DIXDYBOT-RONDA2-TENDENCIAS.md` — ronda 2 (tendencias 2027, 3 supuestos rotos, papeleo
  Meta, referencias diseño/lógica, web-vs-app=PWA, competidores/pricing; §8 = requisitos
  de Alejandro).
- `investigacion-dixdybot/` — 14 informes de detalle ronda 1 (auditorías con cifras de
  logs, investigaciones verificadas, 3 arquitecturas, síntesis del juez).
- `investigacion-dixdybot/ronda2/` — 8 informes ronda 2; **`plan-revisado.md` = el plan
  vigente completo** (leer junto con los ajustes de la ronda 3).
- `DIXDYBOT-RONDA3-CONTRASTE.md` — arbitraje de los deep research externos (ChatGPT y
  Gemini) con fuente primaria: tarifas corregidas, Coexistence ajustado, regulación
  chilena, latencia medida. Detalle en `investigacion-dixdybot/ronda3/` (9 informes).
- `deep-research-report.md` (ChatGPT) y `deep-research-gemini.md` (Gemini) — los informes
  externos crudos; usarlos SOLO a través del arbitraje de la ronda 3.
- `investigacion-dixdybot/ronda4/` — **LA BIBLIOTECA DE PLANOS** (lectura de código real de
  8 repos: NanoClaw, Parlant, vocero-crm, Mastra, BuilderBot, boop-agent,
  whatsapp-agent-bridge, Chatwoot). **`planos-sintesis.md` = lectura OBLIGADA antes de
  construir E1-E5**: pieza→repo/archivo→etapa, 5 planos de oro, decisiones de conflicto
  resueltas, y la lista de lo que ningún repo resuelve (lo genuinamente nuestro).
- `investigacion-dixdybot/ronda5/` — **EL BLUEPRINT FUNDACIONAL**
  (`blueprint-fundacional.md` = EL documento rector de construcción: estructura de
  carpetas, stack verificado — Node 24 LTS + TS estricto nativo sin build + better-sqlite3
  + Hono + Zod, ~6 deps —, los 5 contratos núcleo en TypeScript, módulo ingesta/
  multimodal, orden de construcción S0-S5 mapeado a E0-E7, 16 NOes de sencillez) + los 4
  informes de sustento (stack, media en APIs de Meta, procesamiento IA de media con costos,
  media en repos + evidencia de pérdida real: video de estanques 20-jul respondido a
  ciegas, cotización de 30 baños confirmada por nota de voz ilegible 21-jul).
- `investigacion-dixdybot/ronda6-diseno/` — **EL DESIGN SYSTEM DIXDY**
  (`design-system-dixdy.md` = spec de diseño rectora: tokens, shell L invertida 240px,
  anatomía de las 5 vistas, decálogo anti-ruido ≤40 palabras de chrome) extraído del código
  real de Chatwoot/Typebot, de la app viva de Linear (medida con Playwright + capturas con
  el login de Alejandro) y de Intercom Fin. Regla: TODO el panel se construye desde esta
  spec — cero variaciones.
- Informe visual (artifact): https://claude.ai/code/artifact/002b8dd3-b637-408b-8628-eccee5e2a169
- **Prototipo navegable del panel** (v2 escritorio, iterándose con Alejandro):
  https://claude.ai/code/artifact/555843ca-9568-4c58-8518-afc3eca99e92

## Piezas clave a recordar

- El buzón de dudas (`dudas.js`) y el tarifario en código (`precios.js`) del bot vivo son
  los embriones de los caminos; `enviar.js`/`outbox.js`/`gating.js` se conservan.
- **NanoClaw** (MIT, 30k★) = arquitectura espejo de E1+E4; Parlant = modelo de datos de
  caminos; permission relay de Claude Code Channels = spec del pausa-y-pregunta.
- Editor de caminos: tarjetas + diff + botón Aprobar + historial; SIN canvas de nodos.
- Meta Business Agent no compite (FAQ genérico; "mixed responder" permite terceros);
  pitch: "el agente que OPERA el negocio".
- Pendiente externo: resultados del deep research de Alejandro en Gemini/ChatGPT
  (prompt entregado 23-jul) — verificar antes de integrar.
