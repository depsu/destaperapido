# Arbitraje: papers y repos en disputa (rediseño dixdybot)

Fecha de verificación: 2026-07-23. Método: fuentes primarias (arXiv, OpenReview API, GitHub
repos/issues vía API), mínimo dos fuentes por dato. Sin blogs de vendors.

## 1) Repo oficial de ARIA (arXiv:2507.17131) — CONFIRMADO (Gemini tenía razón)

- **El paper existe:** arXiv:2507.17131 — "Enabling Self-Improving Agents to Learn at Test
  Time With Human-In-The-Loop Guidance" (framework ARIA). Autores: Yufei He, Ruoyu Li, Alex
  Chen, Yue Liu, Yulin Chen, Yuan Sui, Cheng Chen, Yi Zhu, Luca Luo, Frank Yang, Bryan Hooi.
  v1: 2025-07-23, v2: 2025-10-10. Desplegado en TikTok Pay.
  Fuente: https://arxiv.org/abs/2507.17131 (consultado 2026-07-23).
- **El repo existe y es del paper:** https://github.com/yf-he/aria — licencia **MIT**,
  título del README idéntico al paper ("ARIA: Enabling Self-Improving Agents to Learn at
  Test Time With Human-In-The-Loop Guidance"), la página del repo menciona EMNLP'25.
  El dueño `yf-he` es **Yufei He, PhD student en NUS** (grupo de Bryan Hooi) = **primer
  autor del paper** (perfil: https://github.com/yf-he, Google Scholar enlazado). Es repo
  oficial, no un homónimo.
- **Matiz que explica por qué ChatGPT y nuestro agente no lo hallaron:** repo mínimo
  (~1 commit, 7 estrellas, 1 fork), el README no trae bibtex ni enlace a arXiv, y la página
  de arXiv NO enlaza al repo. Señal débil en índices (CatalyzeX) es coherente con eso.
  Conclusión práctica: existe pero es un esqueleto reciente, no una base de código madura
  para apoyarse en producción.

## 2a) EvoTest (ICLR 2026) — CONFIRMADO

- **Paper real:** arXiv:2510.13220 — "EvoTest: Evolutionary Test-Time Learning for
  Self-Improving Agentic Systems". Autores: Yufei He, Juncheng Liu, Yue Liu, Yibo Li, Tri
  Cao, Zhiyuan Hu, Xinxing Xu, Bryan Hooi (NUS + Microsoft Research). Publicado 2025-10-15.
  Fuente: API de arXiv (export.arxiv.org, consulta "EvoTest", 2026-07-23).
- **Aceptación verificada en OpenReview:** forum `JFnnajbkvP`, **aceptado como Poster en
  ICLR 2026** (tres reviewers con score 6). Fuente: api2.openreview.net/notes/search?term=EvoTest
  (2026-07-23). URL humana: https://openreview.net/forum?id=JFnnajbkvP
- **Repo oficial:** https://github.com/yf-he/EvoTest (MIT, 24 estrellas, bibtex con
  arXiv:2510.13220; incluye benchmark J-TTL sobre juegos de texto Jericho).
- **Contenido coincide con lo citado por Gemini:** aprendizaje en tiempo de inferencia sin
  gradientes (dos agentes: Actor y Evolver que reescriben prompt/memoria/hiperparámetros
  entre episodios).
- **Conexión no señalada por nadie:** mismo primer autor (Yufei He) y mismo grupo (Bryan
  Hooi, NUS) que ARIA. Los tres papers en disputa salen del mismo laboratorio.

## 2b) CoNL (ICML 2026) — CONFIRMADO con matiz

- **Paper real:** arXiv:2601.21464 — "Conversation for Non-verifiable Learning:
  Self-Evolving LLMs through Meta-Evaluation". Autores: **Yuan Sui, Bryan Hooi** (NUS; ambos
  coautores de ARIA). v1: 2026-01-29, v2: 2026-05-07. Comments de arXiv: "Accepted by
  ICML'26". Fuente: https://arxiv.org/abs/2601.21464 (2026-07-23).
- **Aceptación corroborada en OpenReview:** forum `Wba6w3pzbj`, submission #14611 de ICML
  2026; dos reviewers subieron a score 4 (accept) tras rebuttal. Fuente:
  api2.openreview.net (2026-07-23). URL humana: https://openreview.net/forum?id=Wba6w3pzbj
- **Matiz importante:** el paper NO es de "habilidades de venta". Es self-play multi-agente
  con meta-evaluación (la calidad de la crítica se premia si ayuda a mejorar al par) para
  tareas **no verificables en general** (escritura creativa, diálogo, razonamiento ético).
  Aplicarlo a ventas es una extrapolación razonable de Gemini, no lo que dice el paper.
  Ninguno de los dos frameworks trae evidencia en dominio de ventas por WhatsApp.

## 3) Error 463 "Reachout Timelock" (WhatsApp/Baileys) — CONFIRMADO (y muy relevante)

Existe con ese número y ese nombre, en múltiples repos independientes:

- **Baileys (WhiskeySockets):**
  - #2707 (2026-07-14) "[BUG] Critical Issue - Error 463 (Reachout Timelock) Causing
    Account Bans": ocurre al enviar a números **sin historial de conversación reciente**;
    WhatsApp exige un **Trusted Contact (TC) Token / privacy token** (~28 días de vida,
    tag `tctoken`); sin él, el envío falla y la repetición lleva a **restricciones y baneos
    temporales**. https://github.com/WhiskeySockets/Baileys/issues/2707
  - #2688 (2026-07-03) "Messages to warm contacts silently not delivered on rc13 error
    463" — exactamente el síntoma "reporta enviado pero no llega".
    https://github.com/WhiskeySockets/Baileys/issues/2688
  - #2698 (2026-07-05) nombre interno "NackCallerReachoutTimelocked"; #2441 (2026-03-25)
    investigación abierta; #2636, #2683 (LID/PN mapping); PRs de mitigación #2446, #2517,
    #2339 (ciclo de vida del tctoken).
- **whatsmeow (tulir, implementación Go independiente — segunda fuente):** #1104
  (2026-03-25) "support for checking message capping and **reachout timelock** limits";
  #1074, #1157 "Error 463 when sending"; #1197 (2026-07-08) "Unable to send message to a
  new contact after July 2nd update". https://github.com/tulir/whatsmeow/issues/1104
- **Ecosistema:** waha #2166 (timelock como evento de primera clase, 2026-07-17),
  fazer-ai/baileys-api #341 (exponer estado de reachout timelock, 2026-06-16).

**Implicación para dixdybot:** el claim de Gemini es real y activo AHORA (issues de julio
2026). Riesgo concreto: mensajes salientes a números fríos que figuran "enviados" pero no
llegan, y baneo por reintentos. Mitigación: bot solo-responde (ya es nuestro caso — el
gating anti-ban existente va en la dirección correcta), no hacer outreach en frío, mantener
Baileys actualizado (los parches de TC/CS token son recientes y aún incompletos según #2698)
y vigilar el estado de entrega real (✓✓) en vez de confiar en el "sent".

## Conclusión para el plan

Gemini acertó en los tres claims fácticos (repo ARIA existe y es oficial; EvoTest ICLR 2026
real; CoNL ICML 2026 real; error 463 real). Dos matices que el plan debe adoptar: (1) los
repos ARIA/EvoTest son del mismo laboratorio (NUS/Bryan Hooi) y son esqueletos de 1-2
commits — sirven de referencia conceptual, no como dependencia de producción; (2) CoNL no es
de ventas: usarlo como inspiración de self-play, sin prometer resultados de dominio. El
punto de mayor impacto operativo inmediato es el error 463: gobierna cualquier idea de
mensajes salientes del bot.
