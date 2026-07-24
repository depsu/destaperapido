# Referencias de diseño y lógica para el panel dixdybot

Fecha: 2026-07-23. Investigación web (búsquedas en inglés y español, julio 2026) para el
rediseño del panel del bot de destaperapido → dixdybot (etapas E0-E6). Complementa
`caminos-estado-del-arte.md` y `auditoria-ux-panel.md` (ambos del 23-jul-2026).

Contexto de uso que manda sobre todo: el panel lo usa **UN dueño de negocio no técnico,
principalmente desde iPhone** (hoy vía Tailscale, :8789), en español. El panel actual es un
HTML único de ~2.700 líneas sin framework. Los "caminos" (E3) viven como archivos
versionados.

---

## (a) UIs open source de inbox/chat: qué robar y qué licencia lo permite

| Proyecto | Licencia | Estado (verificado jul-2026) | Veredicto para robar diseño |
|---|---|---|---|
| **Chatwoot** | MIT (Community Edition); carpeta `/enterprise` propietaria en el mismo repo | Muy activo; apps móviles iOS/Android (React Native) con Captain integrado en el chat móvil (changelog 2025-2026) | ⭐ La mejor referencia de **inbox omnicanal**: lista de conversaciones + hilo + panel lateral de contacto. MIT permite copiar componentes de la parte CE (cuidado: NO copiar nada de `/enterprise`) |
| **Tiledesk** (+ **design-studio**) | MIT (todos los repos, verificado en GitHub) | Mantenido; Angular + Node | Doble referencia: dashboard de inbox **y** builder visual de flujos open source (design-studio, "alternativa a Voiceflow/Botpress"). Stack Angular = robar ideas, no código |
| **Papercups** | MIT | **En maintenance mode**; actividad mínima 2025, cloud apagado | Descartar como referencia viva; solo mirar su minimalismo histórico |
| **Zammad** | AGPLv3 | Activo (helpdesk clásico) | UI densa de tickets, no de chat comercial; AGPL contagiosa → mirar, no copiar código |
| **LibreChat** | MIT | Muy activo 2025-2026 (agentes, MCP, artifacts) | No es inbox: es chat con IA multiusuario. Útil como referencia del patrón "conversar con la IA dentro del panel" |
| **assistant-ui** | MIT | Activo, respaldo YC, ~10k estrellas (2025-2026) | ⭐ **Primitivas React de chat** (Thread, Message, Composer, ThreadList) sobre Radix, con tema shadcn instalable por CLI; streaming, tool-calls y human-in-the-loop de fábrica. Lo mejor si el editor de caminos es "chat con IA" |
| **chatbot-ui** (mckaywrigley) | MIT | Estancado: actividad esporádica 2024, backlog sin dueño (reportes mar-2024 y sep-2024) | Descartar |
| **shadcn/ui chat components** | MIT | **Junio 2026**: shadcn publicó componentes oficiales de chat (MessageScroller, Message, Bubble) en su changelog | ⭐ Muy fresco: primitivas de hilo de mensajes mantenidas por el propio shadcn |

**Lectura práctica:** para el hilo de conversación y el inbox, el patrón consagrado es el de
Chatwoot (3 paneles en desktop que colapsan a navegación por pila en móvil, exactamente lo
que el panel actual ya hace a mano). Para la superficie "editar hablando con la IA",
assistant-ui o los chat components de shadcn (jun-2026) dan el 80% hecho con licencia MIT.

---

## (b) Builders visuales de flujos: patrones de UX y qué le sirve a un dueño no técnico

### Los tres patrones que existen

1. **Canvas libre de nodos** (React Flow/xyflow debajo en casi todos los OSS): Flowise
   (Apache 2.0, Node), Langflow (MIT, DataStax→IBM, Python), Dify (Apache 2.0 con
   restricción anti-competencia), n8n (Sustainable Use License, **NO open source**: prohíbe
   embeberlo en un producto comercial — relevante para E6), Botpress v12 (AGPL,
   **sunset/sin parches**; el Botpress actual es cloud con repo MIT solo de
   SDK/integraciones), Voiceflow (comercial: canvas + panel lateral de configuración por
   bloque, testing que "ilumina" los bloques recorridos — su mejor idea robable).
2. **Canvas híbrido con grupos-lista** — **Typebot** (FSL-1.1-Apache-2.0: libre para
   self-host y uso interno; cada versión pasa a Apache 2.0 a los 2 años; no competir con su
   cloud): su genialidad es que el nodo NO es un bloque suelto sino un **grupo = pila
   vertical de bloques** que se lee de arriba a abajo como una conversación; el canvas solo
   conecta grupos. Gotcha documentado: un bloque sin arista de salida detiene el flujo y el
   editor no avisa. Sus docs de editor (jul-2026) describen solo gestos de mouse/trackpad:
   **cero soporte de edición móvil documentado**.
3. **Lista lineal / cascada** — **ManyChat** mantiene DOS builders: el "Basic Builder"
   (vista lineal mensaje-a-mensaje, para automatizaciones simples) y el Flow Builder
   (canvas, para lo complejo), y en 2025 le sumó un **AI Flow Builder assistant** (describes
   el flujo en texto y te lo arma). Que el líder del mercado SMB mantenga la vista lineal
   como puerta de entrada es el precedente más directo para dixdybot.

### El dato duro que decide: canvas + teléfono no se llevan

React Flow — la base de Flowise, Langflow, Dify, Typebot y casi todo canvas OSS — tiene
soporte táctil **oficialmente pobre**: issues abiertos "React flow is unusable on touch
devices" (#1323), discusiones de mobile support (#1677, #2403) y un issue de 2025 sobre
scroll táctil roto (#5341). Desde v10 hay "tap connect" (tocar dos handles para conectar) y
desde v11.5 arrastre de conexiones táctil, pero la propia documentación recomienda agrandar
handles y conectar por doble tap: parches, no una experiencia. Crear nodos arrastrando desde
un sidebar directamente **no funciona** en touch. Conclusión: cualquier editor de caminos
basado en canvas sería de segunda clase en el iPhone del dueño.

---

## (c) Cómo la industria resuelve "personalidad + conocimiento + reglas + handoff"

- **Intercom Fin — Procedures (2025)**: la referencia conceptual #1 para "caminos". Fin
  separa explícitamente: **Procedures** = instrucciones multi-paso en **lenguaje natural**
  que la IA sigue y adapta (con controles deterministas if/else y conectores de datos
  embebidos), vs **Workflows** = canvas visual de botones y rutas predefinidas. Y el flujo
  de creación estrella es **"draft with AI"**: describes el proceso en tu idioma y Fin
  redacta el Procedure usando tu help center y conversaciones históricas; tú revisas e
  iteras. Es decir: Intercom llegó a "el camino se escribe conversando, no dibujando".
- **Sierra — Agent Studio 2.0 (nov-2025)**: interfaz no-code donde los equipos de CX
  describen "Journeys" **en inglés simple**; el Agent SDK (TypeScript, skills componibles
  triage/respond/confirm) queda para desarrolladores. Mismo patrón: NL para el negocio,
  código para el integrador.
- **OpenAI AgentKit / Agent Builder** (DevDay oct-2025): canvas de nodos
  (Agent/MCP/Guardrail, templates, preview con datos vivos)… y **OpenAI ya lo está
  deprecando: cierre programado 30-nov-2026**, empujando a ChatKit + Agents SDK (código).
  Un canvas de agentes que el propio OpenAI mata en ~13 meses es la señal más fuerte de que
  el canvas NO es el futuro de la configuración de agentes.
- **Dust**: agente = **instrucciones + tools + knowledge** en un formulario simple, y desde
  2026 "Skills" (módulos reutilizables de instrucciones+conocimiento+tools) y el **Agent
  Builder Sidekick**: un copiloto que edita las instrucciones del agente **por diffs inline
  con aprobación de un clic**, sugiere tools y fuentes según el rendimiento real del agente.
  Ese patrón diff-propuesto-por-IA + botón aprobar es oro para dixdybot (calza con el 💡
  "enseñar" que el panel ya tiene).
- **Chatwoot Captain (2025-2026)**: Assistant (bot) + Copilot (asiste al humano) + FAQ con
  embeddings + **Scenarios** (comportamiento especializado por situación, con labels y
  handoff para rutear) + custom tools = endpoints HTTP que el asistente decide invocar. Es
  la versión open source (MIT en CE) más cercana a "personalidad + conocimiento + reglas +
  handoff" en un panel.
- **Relevance AI**: no encontré documentación de detalle de su panel en esta pasada; no lo
  evalúo (dicho honestamente, no invento).
- Cruce con informe previo: Decagon "AOPs" (procedimientos NL **versionados con rollback**)
  y Dialogflow CX Playbooks apuntan igual — ver `caminos-estado-del-arte.md`.

**Síntesis del patrón industrial 2025-2026:** todos convergen en 4 cajones — *Personalidad*
(texto corto), *Conocimiento* (fuentes/FAQ), *Reglas-procedimientos* (lenguaje natural con
controles duros embebidos) y *Handoff* (cuándo escala al humano) — y la edición migra de
canvas → **lenguaje natural asistido por IA con revisión humana**.

---

## (d) Sistemas de diseño gratuitos para un panel móvil-primero en español

- **DaisyUI** (MIT, v5): 65 componentes como **clases CSS sobre HTML normal, cero JS**,
  35 temas por variables CSS (dark mode trivial). Comparativas 2025 lo recomiendan justo
  para dashboards/paneles rápidos; ~829k descargas semanales (≈5x shadcn). Es el **único de
  la lista que encaja con el panel actual sin reescribirlo en React**: se puede tematizar el
  dashboard.html vanilla existente por etapas. Idioma-neutral (tú escribes los textos).
- **shadcn/ui** (MIT, React): componentes copiados a tu repo (no dependencia), accesibles,
  y desde **junio 2026 con componentes oficiales de chat**. Es la opción si el panel dixdybot
  E6 se reescribe en Next.js (stack preferido de Alejandro). assistant-ui trae tema shadcn.
- **Tailwind UI / Tailwind Plus**: de pago — descartado como base (los patrones se pueden
  mirar gratis en demos, el código no).
- **Konsta UI** (componentes Tailwind estilo iOS/Material): lo conozco como opción
  móvil-primero, pero las búsquedas de esta pasada no devolvieron señales de actividad
  2025-2026 — no lo verifiqué, así que no lo recomiendo sin revisar su repo antes.
- Nota: ninguno resuelve "español" per se (todos son idioma-neutrales); lo que importa es
  que los componentes no traigan copy en inglés incrustado — DaisyUI y shadcn no lo traen.

---

## (e) CONCLUSIÓN OPINADA: ¿canvas, cascada o chat+tarjetas?

**Gana: chat con IA como puerta principal + tarjetas de caminos como vista de verdad,
con "cascada" (stepper vertical) para los caminos multi-paso. El canvas pierde — y no por
gusto, sino por tres evidencias:**

1. **Física del teléfono.** Todo canvas OSS serio se apoya en React Flow, y React Flow en
   touch es oficialmente un ciudadano de segunda (issues #1323/#1677/#2403/#5341,
   workarounds de "tap connect"). Typebot, el mejor builder OSS, ni documenta edición móvil
   (jul-2026). Diseñar el editor de caminos como canvas es condenar al dueño a esperar
   estar frente a un computador que no usa.
2. **La industria ya votó.** Intercom (Procedures + draft with AI, 2025), Sierra (Journeys
   en inglés simple, nov-2025), Dust (Sidekick con diffs aprobables, 2026) y ManyChat (AI
   Flow assistant, 2025) convergen en "describe el proceso, la IA lo estructura, tú
   apruebas". Y OpenAI **mata su Agent Builder de canvas en nov-2026** tras un año. El
   canvas sobrevive como vista para equipos técnicos, no como editor para dueños.
3. **El modelo de datos de E3 lo pide.** Los caminos son condición→acción en archivos
   versionados (estilo Parlant/AOPs). Eso mapea 1:1 a **tarjetas con diff y historial**
   (como Dust Sidekick / Decagon con rollback), y muy mal a un grafo espacial: un camino
   nuevo aprendido en caliente no tiene coordenadas x,y naturales; en una lista agrupada por
   tema simplemente aparece arriba con badge "✨ nuevo" — patrón que el panel actual ya usa.

**El diseño concreto que recomiendo apalancar:**

- **Puerta principal = chat con la IA del panel** ("cámbiale el precio al baño mensual",
  "¿qué haces si piden factura?"), construido con assistant-ui o los chat components de
  shadcn (ambos MIT, 2025/jun-2026). Cada cambio propuesto se muestra como **tarjeta de
  diff con botón Aprobar** (patrón Dust Sidekick). Esto además reusa el músculo que el bot
  ya tiene: el flujo 💡 enseñar → regla.
- **Vista de verdad = tarjetas de caminos** agrupadas por tema (precios, cobertura,
  emergencias, handoff), con buscador, badge de origen (dueño / aprendido / semilla) y
  historial por tarjeta. Editar una tarjeta = formulario simple, no canvas. Estructura de 4
  cajones estilo Intercom/Dust: Personalidad · Conocimiento · Caminos · Cuándo llamarme.
- **Caminos multi-paso = cascada**: robarle a Typebot su mejor idea — el grupo como **pila
  vertical de bloques que se lee como conversación** — pero sin el canvas alrededor: un
  stepper vertical (paso 1 → paso 2 → si no contesta → …) es 100% editable con el pulgar.
- **Canvas: solo como vista de solo-lectura opcional en desktop** (un mermaid generado de
  los caminos) para Alejandro cuando audite, nunca como editor. Si algún día se necesita
  editor visual completo, la referencia es Typebot (FSL: mirar y aprender libre; copiar
  código solo de versiones con 2+ años ya convertidas a Apache 2.0) o Tiledesk design-studio
  (MIT, copiable hoy).
- **Inbox/hilo**: mantener la anatomía Chatwoot (MIT) que el panel ya aproxima; para
  estilizar sin reescribir, DaisyUI sobre el HTML actual; si E6 trae reescritura Next.js,
  shadcn/ui + assistant-ui.

**Licencias, en una línea:** copiables hoy = Chatwoot CE, Tiledesk/design-studio, LibreChat,
assistant-ui, chatbot-ui, Langflow, DaisyUI, shadcn (MIT) y Flowise (Apache 2.0); con
condiciones = Typebot (FSL→Apache a 2 años), Dify (Apache con cláusula anti-competencia
cloud), Zammad/Botpress v12 (AGPL, evitar copiar código); **no copiable en un producto** =
n8n (Sustainable Use License) — y Voiceflow/Intercom/Sierra/Dust son comerciales: se roba la
UX, jamás el código.

---

## Fuentes principales (todas consultadas 23-jul-2026)

- https://github.com/chatwoot/chatwoot y https://github.com/chatwoot/chatwoot/blob/develop/LICENSE (MIT CE + /enterprise propietario)
- https://www.chatwoot.com/blog/captain-custom-instructions/ y https://www.chatwoot.com/hc/user-guide/articles/1738101283-captain-_-introduction (Captain, 2025)
- https://github.com/chatwoot/chatwoot-mobile-app (app móvil React Native)
- https://github.com/papercups-io/papercups (maintenance mode)
- https://github.com/Tiledesk/design-studio y https://github.com/tiledesk/tiledesk-dashboard (MIT)
- https://github.com/zammad/zammad (AGPLv3)
- https://github.com/danny-avila/LibreChat (MIT)
- https://github.com/assistant-ui/assistant-ui (MIT, primitivas de chat)
- https://github.com/mckaywrigley/chatbot-ui (estancado)
- https://ui.shadcn.com/docs/changelog/2026-06-chat-components (chat components, jun-2026)
- https://github.com/baptistearno/typebot.io/blob/main/LICENSE (FSL-1.1-Apache-2.0) y https://docs.typebot.com/editor/graph (editor, sin mención móvil)
- https://reactflow.dev/examples/interaction/touch-device · https://github.com/wbkd/react-flow/issues/1323 · https://github.com/xyflow/xyflow/discussions/1677 · https://github.com/xyflow/xyflow/issues/5341 (límites touch)
- https://xyflow.com/blog/react-flow-v-11-5 (drag de conexiones táctil)
- https://docs.n8n.io/sustainable-use-license/ (n8n no-OSS)
- https://github.com/botpress/v12 (AGPL, sunset) y https://github.com/botpress/botpress (MIT, SDK/cloud)
- https://rapidclaw.dev/blog/low-code-ai-agent-platforms-compared-2026 y https://toolhalla.ai/blog/dify-vs-flowise-vs-langflow-2026 (comparativas canvas 2026)
- https://help.manychat.com/hc/en-us/articles/14281166306332-How-to-build-a-Manychat-automation y https://help.manychat.com/hc/en-us/articles/14281200017948-Manychat-AI-Flow-Builder-assistant (Basic vs Flow + AI assistant)
- https://www.intercom.com/help/en/articles/14077835-procedures-vs-tasks-vs-workflows · https://www.intercom.com/help/en/articles/12495167-fin-procedures-explained · https://www.intercom.com/blog/procedures-simulations-updates/ (Fin Procedures, 2025)
- https://sierra.ai/uk/blog/agent-studio-2-0 (Agent Studio 2.0, nov-2025) y https://sierra.ai/product/agent-sdk
- https://openai.com/index/introducing-agentkit/ (oct-2025) y https://developers.openai.com/api/docs/guides/agent-builder (deprecación, cierre 30-nov-2026)
- https://docs.dust.tt/docs/agent-builder-sidekick y https://docs.dust.tt/changelog/skills-share-expertise-across-all-your-agents (Sidekick + Skills, 2026)
- https://daisyui.com/compare/daisyui-vs-shadcn/ y https://www.subframe.com/tips/daisyui-vs-shadcn-25a96 (comparativas 2025)
- https://bigsur.ai/blog/voiceflow-reviews y https://chatimize.com/reviews/voiceflow/ (UX Voiceflow 2025-2026)
