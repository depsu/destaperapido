# Auditoría de modularidad — prototipo v4 del panel dixdybot

**Fecha:** 23-jul-2026 · **Contra:** requisito #1 de Alejandro (DIXDYBOT-ESTADO) + contrato
`Modulo`/manifest del blueprint (§4.5, §6.1) + design-system §3.4.
**Prototipo auditado:** `scratchpad/dixdybot-prototipo.html` (vistas Hoy, Chats
lista+tablero, Caminos, Módulos, Agentes, Diseño).

**Veredicto en una línea:** la vista Módulos del prototipo cubre 4 módulos + 3 canales,
pero el resto del panel muestra **al menos 9 capacidades sin fila ni switch** (cobros,
tarifario, embudo, métricas de Hoy, pausa-y-pregunta, gimnasio/juez, derivación madre,
correo, ficha de datos), y el contrato `Modulo` del blueprint **no tiene cómo declarar los
aportes de UI** (columnas de tablero, métricas, secciones de ficha, tarjetas de Hoy) que
harían que apagar un módulo limpie el panel solo.

---

## 1. MAPA módulo → elementos visibles

### 1.1 Módulos CON fila en la vista Módulos

**Cotizador** (Venta · switch ON · config: "Último click", "Mostrar neto")
- Hoy: métrica secundaria "3 cotizaciones"; tarjeta de decisión Ranco ("cotización lista ·
  $2.480.000 neto" + botón Aprobar).
- Tablero: columnas **Cotizando** (3 · $530mil) y **Por confirmar** (1 · $2,48M) con montos
  por tarjeta.
- Hilo: botón "Aprobar cotización" en el composer; respuesta del bot con precio.
- Ctx: sección completa "Cotización" (Estándar ×30 / Accesible "esperando tu precio" /
  Estado "lista para tu OK").
- `aprobarRanco()`: "PDF + WhatsApp" (la generación de PDF es de este módulo).
- **Si un rubro lo apaga** (rubro Y no cotiza): desaparecen 2 de las 4 columnas del
  tablero, la métrica, la sección Cotización del ctx, el botón del composer y el tipo de
  tarjeta de decisión "aprobar cotización". El hero "$450mil en juego" queda sin fuente
  principal. **Nada de esto está especificado**: el prototipo no muestra el estado apagado
  de ninguna vista.

**Seguimiento** (Venta · switch OFF · config: "Esperar")
- Coherente: está apagado y NO hay elementos visibles (sin columna Dormidos 💤, sin
  recordatorios). Falta definir qué superficie aparece al encenderlo (columna/sección
  Dormidos del Kanban vivo actual).

**Ojos y oídos / ingesta** (Operación · switch ON · config: voz/fotos/videos)
- Lista de chats: previews "🎤 0:41 · '…serían 30 baños…'" y "📷 · Sofía respondió con la
  ficha de la válvula".
- Hilo: anotaciones "**Transcrita:** …" (voz) y "**Vista:** explanada techada…" (foto).
- Traza: paso "Datos completos … (de la nota de voz transcrita)".
- **Si se apaga:** los previews/anotaciones degradan a "🎤 Nota de voz · 0:41" pelado y el
  bot pide reenvío por texto (pausa-y-pregunta). Degradación no dibujada, pero el módulo y
  sus sub-switches existen. ✔ el mejor mapeado del prototipo.

**Entregas** (Operación · switch ON · config: "Despachar")
- Hoy: métrica "1 entrega".
- Tablero: columna **Por entregar** (repartidor avisado, "estado del repartidor en vivo").
- Lista: preview de Rodrigo "Entrega mañana 9-13 · repartidor avisado".
- Toast de aprobarRanco: "repartidor se avisa al confirmar entrega".
- **Si un rubro lo apaga** (rubro X sin repartidor): cae la columna Por entregar y la
  métrica — pero HOY la columna **Cobrado** dice "Marcado por el repartidor en su panel":
  el cobro quedó acoplado a Entregas. Un negocio sin repartidor igual cobra →
  acoplamiento indebido (ver huérfano Cobros).

**Canales** (WhatsApp ok · Instagram Conectar · Voz pronto)
- Footer del sidebar ("WhatsApp · cerebro · $0 hoy"), ✓✓ de estado de envío en el hilo,
  sublínea "WhatsApp · Estación Central" del hilo.
- **Falta config por canal**: la fila WhatsApp no expande nada, pero el esquema (tabla
  `canales`) ya contempla `bot_activo` y `horario` por canal — no hay dónde tocarlos.
- El item "Instagram" del sidebar (grupo Pronto) **duplica** la fila de Canales: dos
  fuentes de verdad; el sidebar debería derivar de la config de canales.

### 1.2 Núcleo declarado (sin switch, correcto que no lo tengan — pero hay que DECIRLO)

- **Motor de caminos** (vista Caminos: cascada, grupos, bloques, peek, ciclo
  borrador→publicar→historial, contadores del sidebar) — core E3.
- **Trazas "por qué"** (porQue precio/pausa, componente traza de Diseño) — es la
  `Resolution` explicable del resolver; core.
- **Handoff** (botón "Tomar", composer "Escribe y Sofía se calla…", burbuja azul "tú") —
  core (`conversaciones.asignado`); el comportamiento "humano escribe → bot se calla y
  cuándo vuelve" merece config, hoy no existe.
- **Chat-IA de caminos** ("Pide un cambio en simple…" + tarjeta "Cambios en borrador" de
  Hoy + diff Publicar/Descartar) — entrada de edición conversacional, core del panel E2-E3.
- **Vista Diseño** — sistema, correcto bajo grupo "Sistema"; pero un dueño de negocio no
  la necesita: falta el flag "visible solo en modo DIXDY/admin".
- Recomendación: en la vista Módulos, una sección "Base" de solo-lectura que liste el
  núcleo (motor de caminos, trazas, handoff, panel) para que el mapa mental "todo lo que
  ves pertenece a algo" cierre también para lo no-apagable.

---

## 2. HUÉRFANOS — visible sin módulo ni switch (priorizados)

1. **Cobros** — columna "Cobrado · julio (6 · $1,1M)", medios de pago "efectivo /
   transferencia", y quién marca cobrado (hoy: "el repartidor en su panel"). No hay módulo
   Cobros; está fusionado con Entregas. Un rubro sin repartidor rompe el cierre del embudo.
   Config mínima: quién marca (repartidor/dueño/bot), medios de pago, IVA/neto.
2. **Precios/Tarifario** — el peek de camino dice "Cifra: **del tarifario**, nunca del
   modelo" y el blueprint tiene `modulos/precios/` (tabla + validador precioCoherente),
   pero el panel NO tiene dónde ver/editar el tarifario ni apagar/configurar el validador.
   Peor: los bloques de caminos muestran cifras en el cuerpo ("$160.000 neto"), cuando
   `lint.ts` exige CERO cifras en el cuerpo — si es render del valor resuelto desde el
   tarifario, la UI debe marcarlo como tal; si es texto del camino, contradice la doctrina.
   El pedido "sube los precios 10%" del chat-IA debería aterrizar en el tarifario, no en
   texto de caminos.
3. **Tablero/embudo como capacidad** — el switch Lista/Tablero y las 4 etapas están
   cableados al rubro (Cotizando→Por confirmar→Por entregar→Cobrado). Las etapas deben
   derivarse de los módulos activos (cada módulo aporta su columna) o ser editables por
   rubro. Sin Cotizador ni Entregas el tablero queda en 1 columna sin definición.
4. **Métricas de Hoy** — hero "$450mil en juego" (¿suma de qué etapas?) y las secundarias
   (7 chats · 3 cotizaciones · 1 entrega) son agregados de módulos sin declaración de
   origen ni config de qué mostrar. Un rubro sin cotización necesita otro hero.
5. **Pausa-y-pregunta / aprendizaje en caliente** — tarjeta de decisión con input
   "Enseñar", píldora "tema en pausa", flujo en la traza ("te preguntó en Hoy y por
   WhatsApp"). Es core E3, pero sus perillas son configurables por diseño
   (`timeout_horas`, `respuesta_espera`, relay por WhatsApp del dueño on/off, quién puede
   responder) y no existen en el panel.
6. **Gimnasio/juez** — "Práctica de anoche" con replays y la métrica "nota juez 4,0" en
   Agentes. El juez es una llamada LLM (cuesta plata) y la práctica nocturna es un proceso
   programado: módulo Calidad con on/off, frecuencia y gate ≥4,0. Sin fila.
7. **Derivación silenciosa (IA madre)** — sección "Recepción" en Agentes ("7 hoy · 0
   dudas") y paso "Recepción → Sofía" de la traza. Con UN solo especialista no aplica y
   debería auto-ocultarse; el ack "<2 s" y la frase corta del rubro son config. Sin fila.
8. **Correo saliente** — "¿A qué correo le envío la cotización?" y "Cotización enviada a
   obras@ranco.cl". Enviar cotización por email es una capacidad (en DIXDY ya existe el
   agente-correos) con credenciales propias. No aparece ni en Venta ni en Canales.
9. **Ficha de datos del cliente** — el ctx pide Comuna/Pedido/Fechas/Correo: campos del
   rubro chileno de servicios, cableados. El set de campos que el bot junta (y que gatilla
   "Datos completos ✓" en la traza) debe ser schema del módulo correspondiente
   (cotizador/extractor), no fijo.

Menores: sección de config del canal WhatsApp inexistente (horario/bot_activo);
"52% cierre" en caminos/agentes sin definición de qué evento cuenta como cierre cuando el
rubro no cotiza (el outcome lo debe aportar un módulo); duplicado Instagram
sidebar-vs-Canales; categorías Venta/Operación/Canales de la vista Módulos no mapeadas a
nada del manifest (¿`dominio`? ¿campo nuevo `categoria`?).

---

## 3. Filas que FALTAN en la vista Módulos del prototipo

| # | Fila nueva | Sección | Config mínima visible |
|---|---|---|---|
| 1 | **Precios** (tarifario) | Venta | editar tabla · IVA/neto por defecto · validador precioCoherente on/off |
| 2 | **Cobros** | Venta u Operación | quién marca cobrado · medios de pago · corte mensual |
| 3 | **Tablero** (embudo) | Panel/Venta | etapas activas (derivadas de módulos) · nombres por rubro |
| 4 | **Métricas de Hoy** | Panel | qué hero · qué secundarias (o "cada módulo aporta la suya", declarado) |
| 5 | **Aprendizaje** (pausa-y-pregunta) | Base/Operación | escalada (30 min) · respuesta de espera · responder por WhatsApp del dueño on/off |
| 6 | **Calidad** (gimnasio+juez) | Base | práctica nocturna on/off · frecuencia · gate del juez |
| 7 | **Derivación** (IA madre) | Agentes/Base | auto-oculta con 1 agente · frase de ack del rubro |
| 8 | **Correo** | Canales o Venta | remitente · enviar cotización por email on/off |
| 9 | Config del canal **WhatsApp** (expandir fila existente) | Canales | horario · bot activo · número |
| 10 | Sección **"Base"** solo-lectura | — | núcleo no-apagable declarado: motor de caminos, trazas, handoff, panel |

**Brecha de contrato (promover al blueprint, no solo al prototipo):** el contrato
`Modulo` (§4.5) tiene `fragmentoPersona`, `herramientas`, `alMensaje` y `rutasPanel`, pero
**no tiene cómo declarar aportes de UI**. Propuesta: agregar al manifest un campo
`aportes` — `{ metricasHoy[], etapasTablero[], seccionesFicha[], tiposDecision[],
camposDatos[] }` — para que el panel componga Hoy, el tablero y el ctx SOLO desde los
módulos activos, y apagar un módulo limpie sus columnas, métricas y secciones sin código.
Es la única forma estructural de cumplir "todo lo visible pertenece a un módulo" para
cualquier rubro; hoy ni el prototipo ni el blueprint lo resuelven.

**Regla de aceptación sugerida para v5 del prototipo:** cada elemento visible lleva (en
modo auditoría) la etiqueta de su módulo de origen, y existe un preset "rubro sin
entregas/sin cotización" que demuestre el panel degradado con módulos apagados.
