# Veredicto del juez — panel de arquitectura dixdybot

Fecha: 2026-07-23. Propuestas evaluadas: `arq-evolucion.md`, `arq-nucleo-nuevo.md`,
`arq-opensource.md`. Base: los 10 informes hermanos + verificación directa del repo vivo
(`git status` de `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot`: 6
archivos modificados sin commit + `recordatorios.js` nunca commiteado — la propuesta
open source fue la única que lo describió completo; `brainApi` en brain.js:130 y `TIPOS`
en dudas.js:24 existen tal como se citan).

---

## Ranking

### 1º — Evolución incremental (`arq-evolucion.md`) · 8,5/10

**Fortalezas.** Menor riesgo para la producción de las tres: el bot actual ES dixdybot v0,
cada etapa es un commit en el mismo repo/proceso, rollback = git revert, sin sistema
paralelo conviviendo meses. Etapa 0 en 1-2 días cierra los riesgos reales verificados
(fixes sin commit, 401 mudo, backup de auth/, rotación de logs, dedup persistente). La
"pausa de TEMA, no de chat" es la mejor idea de UX de venta del panel completo: el bot
sigue juntando los demás datos mientras espera la regla — en un rubro de urgencia eso
salva ventas. Máxima alineación doctrinal (sección explícita "lo que NO se construye";
llm.js como única puerta; cero crons nuevos; reuso literal de dudas.js/brainApi que
verifiqué existentes). Caminos completos: formato .md+frontmatter, cero cifras en el
cuerpo, selección por turno, conflictos al guardar, git, edición conversacional, métricas
cruzadas con envios.jsonl, arranque en frío 68→20-30.

**Debilidades.** No resuelve de raíz el problema estructural #1 de la auditoría (3
procesos escribiendo 17 JSON sin lock): writeAtomic evita escrituras rotas pero no las
carreras read-modify-write entre procesos (incidentes 16/22-jul). Mantiene tokens mágicos
([[NOSE]]) en vez de salida tipada. El gimnasio sigue como pieza aparte (no formaliza el
"canal sim"). Partir dashboard.mjs endpoint por endpoint puede costar más de lo admitido.

### 2º — Núcleo Nuevo (`arq-nucleo-nuevo.md`) · 8/10

**Fortalezas.** La mejor arquitectura de destino y el mejor diseño de caminos de las tres:
único escritor (resuelve la causa raíz de las carreras), salida tipada con --json-schema
(mata la clase de bugs de parseRules), canal "sim" (el gimnasio entra por el mismo
contrato — mata la lógica duplicada de raíz), evento "turno" con "por qué dijo esto",
esquema de camino más rico (requiere/vigencia/excluye/escenarios ligados como gate),
conflictos en 3 capas, patrones CALM transversales, y la migración en sombra con gate
medible (sombra ≥ vivo 5 días + 0 regresiones). Postura ToS la más honesta: conversacional
→ API delgada como destino, claude -p con Max para el trabajo agéntico del dueño — calca
el veredicto del informe cerebro-claude-code-vs-api.

**Debilidades.** Mayor esfuerzo total y mayor riesgo de quedarse a medias: motor nuevo +
panel nuevo desde cero + proyección de datos + checklist de ~50 endpoints + dos paneles
conviviendo = meses con doble sistema (el clásico riesgo de la reescritura, mitigado pero
real). La sombra consume cupo Max. Event-log + snapshot + re-reduce es más maquinaria de
la necesaria para ~4 chats/día. Primera mejora visible igual de rápida (Etapa 0), pero el
valor del corazón (pausa-y-pregunta en vivo) llega en el mes 2, después que en evolución.

### 3º — Open source (`arq-opensource.md`) · 7/10

**Fortalezas.** La tesis es honesta y correcta ("ningún OSS trae el corazón; adoptar para
lo demás, construir el corazón pequeño") y su censo está verificado. La Etapa 0 es la más
completa y la ÚNICA factualmente exacta sobre lo sin commitear (verificado por mí contra
git status: dashboard.mjs, web/*.html y recordatorios.js incluidos) + pin exacto de
Baileys 6.7.23 + heartbeat al avisos-worker. El laboratorio de vocero-crm (MIT) como
patrón del gimnasio y provider-meta de BuilderBot como referencia para wa-cloud son
adopciones sensatas. "Global por defecto, excepción por chat" corrige bien el bug
conceptual de respuestaPrevia.

**Debilidades.** Su apuesta central del panel es un error estratégico: forkear wacrm
(Next.js 16 + Supabase + Meta Cloud API) para un bot cuyo plano de datos es archivos
locales + Baileys implica destripar la capa de datos del fork — el costo real supera al de
evolucionar el panel actual, y la propuesta lo subestima (aunque admite "semanas, no
días"). Contradicción interna en el tarifario: §5.1 deja las cifras en precios.js (código)
pero §6 promete tarifario "editable desde el panel" — incompatible sin resolver. Adoptar
DeepEval agrega un stack Python paralelo al juez propio que ya existe (contra la doctrina
"imitar, no adoptar" que las otras dos aplican). Caminos algo menos profundos (sin runtime
de paso activo).

---

## Plan recomendado (síntesis)

**Columna vertebral: EVOLUCIÓN.** El bot vivo se transforma en dixdybot por etapas en el
mismo repo, sin sistema paralelo. Es la vía con menos riesgo para la venta de hoy y la más
doctrinal.

**Injertos de NÚCLEO NUEVO (7):**
1. **Único escritor como regla**, adoptada por disciplina dentro del proceso actual (el
   panel deja de escribir `data/` y pasa por la API del bot al llegar la etapa del panel)
   — sin construir un "motor" separado.
2. **Salida tipada** del cerebro (`--json-schema`: responder / silencio / falta_camino) en
   vez de tokens mágicos.
3. **Canal "sim"**: el gimnasio como un canal más del contrato — mata la duplicación
   panel/gym de raíz.
4. **Evento "turno"** (caminos cargados, validadores, modo/modelo/latencia) → vista "por
   qué dijo esto".
5. Extras del **esquema de camino**: `requiere:[datos]`, `vigencia`, escenarios dorados
   ligados que corren como gate al guardar; **conflictos en 3 capas** (determinista + LLM
   + regresión).
6. **Gate de switch medible** para caminos: A/B con juez sobre dorados tras flag
   `CAMINOS_ON`; listón = nota 4,0 del 22-jul.
7. **Postura ToS**: llm.js mide tokens/latencia por rol; el tráfico conversacional migra a
   API Messages delgada (Haiku/Sonnet + caching) como destino; `claude -p` + Max queda
   para el trabajo agéntico de Alejandro (compilar caminos, juez, entrenador). Multi-
   cliente vendido a terceros = API key por cliente, sin excepción.

**Injertos de OPEN SOURCE (4):**
1. Su **Etapa 0 completa** (commitear TODO lo suelto incluidos dashboard.mjs, web/*.html,
   _selftest.mjs y recordatorios.js; pin exacto Baileys 6.7.23; heartbeat→avisos-worker;
   tope de respuestas persistido; MANUAL.md a valores reales).
2. Patrones del **laboratorio vocero-crm** (MIT) para el gimnasio: clientes simulados
   tipificados del rubro + delta histórico tras cada cambio.
3. **provider-meta de BuilderBot** (MIT) como referencia al construir el adaptador
   wa-cloud (plan B de Baileys, presupuestado: ~CLP 9-15 mil/mes post oct-2026).
4. **"Global por defecto, excepción por chat"** al resolver dudas.

**Se rechaza:** fork de wacrm como panel (plano de datos incompatible; el panel actual
evoluciona consumiendo la API del bot, vistas Conocimiento y Ajustes primero); adopción de
DeepEval (se imita con canal sim + juez propio; queda anotado como opción futura);
motor-proceso separado desde el día 1 (doble sistema durante meses).

**Pausa-y-pregunta (el corazón):** pausa de TEMA, no de chat (evolución) + respuesta
enlatada inmediata al cliente + push por avisos-worker + escalada a los 30 min; la
respuesta del dueño se destila en camino global (o excepción del chat), pasa conflictos en
3 capas y regresión de dorados, se commitea en git, y el chat se reanuda en caliente.

**Tarifario:** a `data/tarifario.json` editable desde el panel con `_test-precios.mjs`
como gate al guardar (evolución). Se rechaza dejarlo en precios.js.

**Orden y tiempos:** E0 cinturón (1-2 días, entregable ya) → E1 llm.js única puerta +
failover cli→api + setup-token + pin del CLI (3-4 d) → E2 conocimiento-como-datos:
tarifario.json + persona.md + ajustes.json + vista Conocimiento v1 (4-5 d) → E3 caminos
v1 con arranque en frío 68→20-30, pausa-y-pregunta, gate con juez (2 sem) → E4 canal-como-
enchufe (convId, interfaz Canal, canal sim, único escritor del panel) (1,5 sem) → E5
Instagram SOLO vía API oficial con worker-buzón patrón timbre v2 (papeleo Meta arranca en
E4; 3-14 días hábiles de Meta) → E6 promoción al maestro como `dixdybot/` y segundo
cliente piloto. Mac mini hoy; VPS + API key recién con 2+ clientes.

**Regla transversal:** cada etapa termina en producción con prueba (tests + replay de
dorados + nota del juez ≥ 4,0), huella con `actividad.py`, y rollback de una línea.
