# "Caminos" de dixdybot vs. el estado del arte — informe de investigación web

Fecha: 2026-07-23. Investigación para el rediseño del auto-respondedor de destaperapido.cl
como "dixdybot" (multi-canal, cerebro Claude Code local vía `claude -p`).

---

## 0. La idea del dueño, descompuesta

El concepto "caminos" tiene 4 componentes que conviene evaluar por separado, porque en la
literatura tienen nombres distintos:

1. **Conocimiento del negocio como rutas explícitas y visibles** ("baño químico mensual
   zona urbana → $X"), editables en un panel y conversando con una IA.
2. **Detección de hueco**: si el cliente pide algo sin camino, el bot lo reconoce (no
   inventa).
3. **Pausa + pregunta al humano**: el chat se congela, el bot explica qué le faltó, el
   humano responde en lenguaje natural.
4. **Aprendizaje en el momento**: la respuesta humana se convierte en un camino nuevo al
   instante (no post-mortem), conectado pero controlado.

---

## 1. (a) ¿Cómo se llama esto en la literatura/industria?

No existe UN nombre único: la idea del dueño es la **combinación** de dos corrientes que la
industria y la academia ya nombraron por separado.

### 1.1 Componente "rutas explícitas en lenguaje natural" — nombres establecidos

- **Dialogflow CX "Playbooks" (Google)**: exactamente la filosofía del componente 1. En vez
  de flujos/páginas/intents, el agente se define con **instrucciones en lenguaje natural**
  (nombre + goal + pasos + ejemplos few-shot + parámetros); cada playbook maneja una tarea y
  puede rutear a otro playbook. Docs: `docs.cloud.google.com/dialogflow/cx/docs/concept/playbook`
  y `/playbook/instruction`. No es open source (Google Cloud), pero es la referencia de
  diseño más madura del patrón "instrucciones NL por tarea".
- **Parlant "Guidelines + Journeys"** (github.com/emcie-co/parlant): guidelines =
  **pares condición→acción en lenguaje natural** ("cuando el cliente pida X, haz Y");
  journeys = SOPs multi-turno paso a paso. El motor carga **solo las guidelines relevantes
  al turno actual** (context engineering dinámico). Es el modelo de datos más parecido a un
  "camino".
- **Rasa CALM (Conversational AI with Language Models)**: "flows" = lógica de negocio en
  pasos declarativos (YAML); el LLM NO decide la lógica, solo **interpreta** el mensaje y
  emite comandos internos ("Dialogue Understanding"); "conversation patterns" = flujos de
  sistema reutilizables para digresión, corrección, clarificación. Docs:
  `rasa.com/docs/learn/concepts/calm/`.
- **"Agent SOPs / Agent Operating Procedures"**: término emergente 2025-2026.
  - Decagon (vendor líder de CX) los llama **AOPs**: "instrucciones en lenguaje natural que
    se compilan en lógica validada", con **versionado de cada cambio y rollback
    instantáneo**; reportan 70-80% de deflexión (`decagon.ai/blog/from-sops-to-agent-operating-procedures`).
  - Grab publicó su **"SOP-driven LLM agent framework"**: la SOP como árbol de
    acciones/decisiones en lenguaje natural indentado
    (`engineering.grab.com/introducing-the-sop-drive-llm-agent-framework`).
  - Paper **Agent-S** (arXiv:2503.15520): "LLM Agentic workflow to automate Standard
    Operating Procedures".
  - **strands-agents/agent-sop** (GitHub, AWS Strands): SOPs como **markdown en lenguaje
    natural** con inputs parametrizados y ejecución con restricciones.

### 1.2 Componente "pausar, preguntar al humano, aprender al instante" — nombres establecidos

- **Human-in-the-loop con interrupts**: el mecanismo de pausa es exactamente el
  `interrupt()` de **LangGraph**: un nodo pausa el grafo, entrega un payload al humano, el
  estado se persiste con un checkpointer, y el valor que devuelve el humano reanuda la
  ejecución (decisiones approve/edit/reject/respond). Docs:
  `docs.langchain.com/oss/python/langchain/human-in-the-loop`. Es el patrón estándar 2025-26.
- **Test-time / interactive knowledge acquisition**: el aprendizaje "en el momento" tiene un
  paper casi calcado: **ARIA** (arXiv:2507.17131, "Enabling Self-Improving Agents to Learn at
  Test Time With Human-In-The-Loop Guidance"). ARIA: (i) evalúa su propia incertidumbre por
  self-dialogue estructurado, (ii) **identifica proactivamente el gap y pide al experto
  humano una explicación o corrección dirigida**, (iii) actualiza un **repositorio interno de
  conocimiento con timestamps**, resolviendo conflictos "mediante comparaciones y consultas
  de aclaración". Está **desplegado en TikTok Pay sirviendo a 150M+ usuarios activos
  mensuales**. Es la validación académica+industrial más fuerte de la idea "caminos".
- **Active learning**: el marco clásico de ML donde el sistema **elige qué preguntar** al
  humano para aprender con el mínimo de preguntas. "Caminos" es active learning aplicado a
  reglas de negocio en vez de a etiquetas.
- **Case-based reasoning (CBR)**: ciclo retrieve→reuse→revise→**retain** (el caso nuevo se
  guarda para el futuro). El review "CBR for LLM Agents" (arXiv:2504.06943) documenta que
  bancos de casos explícitos dan memoria episódica transparente y aprendizaje continuo **sin
  reentrenar**. Un camino = un caso generalizado.
- **Agent Workflow Memory (AWM)** (ICML 2025, Wang et al.): el agente **induce workflows
  reutilizables de su propia experiencia, incluso online sobre las consultas de test**, y los
  inyecta en memoria; +24.6% y +51.1% de éxito relativo en Mind2Web y WebArena. Es la versión
  "sin humano" del mismo bucle: aprender rutas sobre la marcha.
- **"Escalation-driven knowledge capture"**: NO es un término formal establecido (lo
  verifiqué: no aparece como término acuñado). La práctica sí existe en la industria de CX
  ("cada handoff resuelto por humano debe alimentar el conocimiento del AI"), pero casi
  siempre **post-mortem** (analizar la conversación después, redactar artículo de ayuda),
  no en el momento. Ahí es donde "caminos" es más agresivo que la práctica común.

### 1.3 Nombre técnico propuesto

En una frase de industria: **"NL-defined journeys with interrupt-driven, test-time knowledge
acquisition"** — rutas definidas en lenguaje natural (tipo playbooks/AOPs) + adquisición de
conocimiento en tiempo de ejecución vía interrupt humano (tipo ARIA/LangGraph HITL).
Para hablar con Alejandro: "caminos" está bien como marca interna; técnicamente son
**journeys + guidelines (Parlant) con un bucle ARIA de aprendizaje en caliente**.

---

## 2. (b) Proyectos open source VIVOS y reutilizables con cerebro Claude

| Proyecto | Vida | Licencia | Qué aporta a "caminos" | ¿Reutilizable con Claude? |
|---|---|---|---|---|
| **Parlant** (emcie-co/parlant) | 18.2k ⭐, 1.5k forks, v3.3.2 (abr 2026), 5,485 commits en develop | Apache 2.0 | El modelo de datos de camino: guideline condición→acción, journeys, canned responses, relaciones entre guidelines | Sí como referencia de diseño; como runtime exige un `NLPService` custom (SchematicGenerator + Embedder + ModerationService) — envolver `claude -p` es posible pero es un adaptador no trivial. Docs mencionan Anthropic (API) como proveedor recomendado; no hay adaptador CLI. |
| **LangGraph** (LangChain) | Muy activo, estándar de facto | MIT | El mecanismo exacto de pausa/reanudación: `interrupt()` + `Command` + checkpointer persistente (el chat pausado sobrevive reinicios) | Sí (soporta Anthropic API); pero es Python/JS con API key — en el stack actual (Node + claude -p sin API) conviene copiar el PATRÓN, no la librería. |
| **Rasa (CALM)** | Activo | OJO: el core histórico es Apache 2.0, pero **CALM vive en Rasa Pro (licencia comercial, con developer edition gratuita limitada)** | Separación lenguaje/lógica; los "conversation patterns" de reparación (corrección, digresión, clarificación) | Parcial: arquitectura copiable, código no libre para producción. |
| **strands-agents/agent-sop** | Activo (AWS Strands) | OSS (GitHub) | SOPs como markdown puro en lenguaje natural, parametrizadas | Sí: el formato markdown-SOP es directamente digerible por `claude -p`. |
| **ARIA** (arXiv:2507.17131) | Paper 2025, desplegado en TikTok Pay | No encontré repo público | El bucle completo gap→pregunta→repositorio timestampeado→resolución de conflictos | Como especificación a imitar, no como código. |
| **AWM** (ICML 2025) | Paper con código académico | — | Inducción de workflows desde conversaciones pasadas (modo offline: minar los .jsonl existentes para proponer caminos iniciales) | Como técnica: "que Claude destile caminos del historial" es exactamente AWM offline. |
| Dialogflow CX Playbooks | Producto vivo | Propietario (Google) | Estructura de playbook (goal+pasos+ejemplos+parámetros) y ruteo entre playbooks | Solo como referencia de diseño. |

**Conclusión (b):** ningún OSS entrega el bucle completo "pausa→pregunta→camino nuevo al
instante" listo para usar. Lo más honesto con la doctrina DIXDY (no reinventar, sumar a lo
que existe): **quedarse en el stack Node actual e implementar los caminos como DATOS**
(archivos markdown/YAML por camino, git como versionado) copiando el modelo Parlant
(condición/acción/relaciones) y el bucle ARIA (gap→interrupt→regla→timestamp), con
`claude -p` como matcher/compilador. El embrión ya existe en el bot vivo: `src/aprender.mjs`
(correcciones→reglas destiladas con `claude -p`) y el tarifario en `src/precios.js` son
caminos hardcodeados sin panel ni bucle de pausa
(`/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/`).

---

## 3. (c) Estado del arte: reglas en lenguaje natural vs flujos rígidos

Convergencia clarísima 2024-2026: **ni todo-LLM ni todo-flujo; híbrido con separación de
responsabilidades**.

1. **Contra el todo-LLM (prompt gigante)**: Rasa documenta que "la lógica de negocio
   incrustada en prompts causa decisiones inconsistentes e improvisadas" y costos crecientes.
   Parlant documenta **"attention dilution"** (la precisión puede caer hasta ~85% al acumular
   contexto irrelevante) y "lost in the middle" — por eso su motor inyecta **solo las
   guidelines cuya condición coincide con el turno actual**. Lección para caminos: cuando
   haya 100+ caminos, NO van todos al prompt; hace falta un matcher (embeddings o un
   pre-filtro barato) que cargue 3-5 caminos relevantes.
2. **Contra el todo-flujo (árboles NLU clásicos)**: "los árboles grandes se rompen cuando el
   usuario se desvía del camino esperado" (Rasa). La solución CALM: flujos declarativos +
   **patterns de reparación transversales** (corrección de datos, digresión y vuelta,
   clarificación entre 2 flows candidatos) que se manejan UNA vez a nivel sistema, no
   duplicados en cada flujo.
3. **El punto medio ganador**: lenguaje natural como FORMATO de la regla (lo escribe un
   humano no técnico, lo entiende el LLM), estructura mínima como ESQUELETO
   (condición/acción, pasos, parámetros, relaciones). Así lo hacen Playbooks (pasos NL +
   ruteo estructurado), Decagon (NL "compilado a lógica validada"), Parlant (NL + relaciones
   explícitas `depend_on`/`exclude`/`entail`, niveles de criticidad LOW/MEDIUM/HIGH, tags
   para agrupar), Grab (árbol de decisiones escrito en NL indentado).
4. **Momentos críticos = plantillas, no generación**: Parlant usa "canned responses"
   pre-aprobadas para eliminar alucinación donde duele (precios, condiciones legales).
   Aplicado a destaperapido: la CIFRA del camino nunca la redacta el modelo; la inserta el
   sistema desde el dato del camino.

---

## 4. (d) Veredicto

### ¿Es sólida la idea?

**Sí, y está validada por convergencia independiente.** Tres actores llegaron a lo mismo por
caminos distintos: la industria CX (AOPs de Decagon con versionado y 70-80% de deflexión;
Playbooks de Google), el open source (Parlant 18.2k⭐ con guidelines+journeys), y la academia
(ARIA en producción en TikTok Pay con 150M MAU). El dueño no está reinventando una rareza:
re-derivó el patrón dominante 2025-2026.

**Lo genuinamente diferencial de "caminos"** es el bucle síncrono: pausa del chat → pregunta
al humano → regla nueva EN EL MOMENTO. La industria mayoritariamente aprende post-mortem
(analizar escalaciones después); solo ARIA documenta el aprendizaje en caliente en
producción. Es una apuesta razonable para un negocio chico donde el dueño está a un WhatsApp
de distancia; el riesgo es la latencia para el cliente final (ver mitigación abajo).

### Nombre técnico

**"Journeys/guidelines en lenguaje natural con adquisición de conocimiento human-in-the-loop
en tiempo de ejecución"** (en corto, para docs del maestro: *caminos = NL journeys + bucle
ARIA*). Evitar venderlo como "escalation-driven knowledge capture": ese término no existe
formalmente.

### Mejoras del estado del arte a adoptar (concretas)

1. **Esquema Parlant por camino**: `condición` (cuándo aplica) + `acción/pasos` + `cifra
   como dato aparte` + relaciones `depende_de` / `excluye` / `implica` + criticidad. Camino
   = archivo markdown/YAML → **git da versionado y rollback gratis** (lo que Decagon vende
   como feature).
2. **Detección de conflictos al crear un camino** (de ARIA): antes de guardar, `claude -p`
   compara el camino nuevo contra los existentes y, si dos condiciones se solapan con
   acciones distintas, pregunta al humano cuál manda. Nunca guardar en silencio un camino
   que pisa otro.
3. **Timestamp y vigencia** (de ARIA): cada camino con `creado`, `actualizado`, y opcional
   `vence` (precios de temporada). El repositorio de ARIA es explícitamente "timestamped".
4. **Carga selectiva** (de Parlant): al turno entran solo los caminos cuya condición matchea
   — pre-filtro barato primero (keywords/embeddings), juicio de Claude después. Evita la
   attention dilution cuando los caminos escalen a cientos.
5. **Patterns de reparación a nivel sistema** (de Rasa CALM): corrección ("no, era en
   Melipilla"), digresión ("¿y destapes hacen?" en medio de una cotización de baño) y
   clarificación (2 caminos candidatos → preguntar al cliente) se implementan UNA vez, no
   por camino.
6. **Cifras solo desde datos** (canned responses de Parlant): el precio lo inserta el
   sistema desde el camino; el LLM redacta alrededor.
7. **Pausa con estado persistente** (lección LangGraph): el chat pausado se guarda en disco
   (el bot ya tiene jsonl/outbox y recordatorios 💤 — reutilizarlos) y sobrevive reinicios;
   al cliente se le dice algo honesto tipo "déjame confirmarlo y te escribo en unos minutos",
   con timeout que escala a aviso push si el humano no contesta.
8. **Métricas por camino** (práctica AOP/CX): usos, tasa de cierre, última vez usado, y una
   **lista de gaps** (pedidos sin camino, razón de cada pausa) como panel de cobertura — la
   industria insiste en "trackear la razón de cada escalación para cerrar gaps".
9. **Arranque en frío vía AWM offline**: antes del lanzamiento, minar
   `conversaciones.jsonl`/`envios.jsonl` existentes con `claude -p` para proponer los
   primeros 20-30 caminos, que el humano aprueba en lote.

### Riesgos honestos

- El bucle en caliente exige que el humano conteste rápido; sin timeout+fallback, un chat
  pausado es un cliente perdido (el rubro de destapes es de urgencia).
- Reglas en NL puro sin esquema degeneran en el mismo prompt-gigante que la industria ya
  abandonó: el esqueleto condición/acción NO es opcional.
- No encontré repo público de ARIA ni un OSS que entregue el bucle completo llave en mano:
  la parte "pausa→aprende al instante" habrá que construirla (pequeña, sobre el bot actual).

---

## Fuentes

- https://github.com/emcie-co/parlant (18.2k⭐, Apache 2.0, v3.3.2 abr-2026)
- https://www.parlant.io/docs/concepts/customization/guidelines/ (condición/acción, relaciones, attention dilution)
- https://www.parlant.io/docs/advanced/custom-llms/ (NLPService custom: SchematicGenerator/Embedder)
- https://rasa.com/docs/learn/concepts/calm/ y https://rasa.com/docs/learn/concepts/conversation-patterns/ y https://rasa.com/docs/reference/primitives/flows/
- https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook y .../playbook/instruction
- https://decagon.ai/blog/from-sops-to-agent-operating-procedures (AOPs, versionado, 70-80% deflexión)
- https://arxiv.org/abs/2507.17131 (ARIA — test-time learning HITL, TikTok Pay 150M MAU)
- https://arxiv.org/abs/2503.15520 (Agent-S: SOP automation)
- https://github.com/strands-agents/agent-sop (SOPs markdown NL)
- https://engineering.grab.com/introducing-the-sop-drive-llm-agent-framework
- https://docs.langchain.com/oss/python/langchain/human-in-the-loop (interrupt/Command/checkpointer)
- https://arxiv.org/abs/2504.06943 (review CBR para agentes LLM)
- https://proceedings.mlr.press/v267/wang25bx.html (Agent Workflow Memory, ICML; +24.6%/+51.1% Mind2Web/WebArena)
- https://arxiv.org/pdf/2504.14787 (ADL: lenguaje declarativo para chatbots de agentes)
- Contexto local: /Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/src/aprender.mjs y src/precios.js (embrión actual de caminos); /Users/alejandroriveracarrasco/SaSS/DIXDY/docs/24-whatsapp-bot-autoresponder.md
