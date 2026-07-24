# MATRIZ VISIÓN → PROTOTIPO v4 (dixdybot-prototipo.html)

**Fecha:** 23-jul-2026 · Contraste del prototipo navegable contra la visión original de
Alejandro y los requisitos de `DIXDYBOT-ESTADO.md` / blueprint r5 / design system r6.

**Veredicto global:** el prototipo comunica muy bien lo ESTRUCTURAL de la visión
(pausa-y-pregunta, trazas de porqué, multimodal, tablero punta a punta, módulos, multi-agente,
design system). El eje más débil es exactamente el corazón declarado de la visión:
**"entrenamiento CONFIABLE / humano e IA aprendiendo juntos"** — el gimnasio quedó reducido a
2 filas, no hay feedback por mensaje, ni replay, ni juez navegables, y la edición
conversacional muestra el resultado pero no la conversación.

---

## 1. La matriz

| # | Elemento de la visión / requisito | Veredicto | Qué se ve | Qué NO se ve |
|---|---|---|---|---|
| 1 | **Pausa-y-pregunta** (bot pausa el tema, pregunta al dueño EN el momento, aprende, crea el camino) | **CUMPLE** (lo mejor del prototipo) | Decisión en Hoy con input "Respóndele como a una persona…" + botón Enseñar → nace el camino con badge "nuevo" en Caminos → contador baja → toast "Sofía lo aprendió". Píldora ámbar en el hilo "tema en pausa — Sofía te preguntó, el chat siguió" clickeable → traza de 5 pasos del flujo, incluida la respuesta por WhatsApp con código ("si TQKMV") | La **reanudación no aparece en el hilo** (tras Enseñar el chat no muestra a Sofía retomando); la **respuesta enlatada que ve el cliente** mientras espera; la **escalada a 30 min**; "primera respuesta gana" panel-vs-WhatsApp |
| 2 | **Edición conversacional de caminos** ("sube los precios 10%" → antes/después → confirmar) | **PARCIAL** | Input flotante "Pide un cambio en simple…" en la cascada; borrador "Precios céntricos +10% · lo pediste anoche" en Hoy; diff $160.000→$176.000 con Publicar/Descartar; "deshacer restaura como borrador" | El botón **Pedir solo lanza un toast** — la conversación con la IA no se simula (ni un intercambio); el borrador dice "**4 caminos**" pero el diff muestra **solo 1** (inconsistencia); no hay resumen "¿qué cambió?" al publicar (spec r6) |
| 3 | **Métricas por camino** | **PARCIAL** | "Uso: 34 veces · 52% cierre" + "Pruebas 5/5 ✓" en el peek de UN camino; contadores por grupo y por agente | Uso/cierre **por bloque en la cascada** (la spec r6 pedía "41 esta semana" por fila); ranking (qué camino vende más, cuál nunca dispara); métricas del camino recién aprendido; evolución en el tiempo |
| 4 | **Entrenamiento / gimnasio** (confiable, hasta vender mejor que él) | **FALTA** (quedó muy chico) | Sección "Práctica de anoche" con 2 filas (5/6 ✓ y "revisar", toasts) + métrica "nota juez 4,0" | **No hay botón Probar ▸** (chat simulado + impersonar cliente, spec r6 §3.3 y §3.5); replay solo como toast; **veredicto del juez sin vista** (hallazgos, evidencia); el **gate ≥4,0** para publicar/activar no se explica; el gimnasio vivo (rol de cliente, correcciones→reglas) no tiene equivalente |
| 5 | **Ciclo aprender-juntos** (feedback por mensaje, replay, juez) | **FALTA** | Solo la puerta de la pausa (fila 1) y "Práctica de anoche" | **👍👎/corregir sobre una burbuja del bot** en el hilo (el dashboard vivo YA lo tiene — es regresión visual frente a lo existente); enseñar desde una respuesta mala del chat; resumen semanal de calidad |
| 6 | **Caminos = conocimiento visible en cascada** | **PARCIAL** | Vista Caminos con 3 grupos (Precios céntricos, Zonas lejanas, Cierre y objeciones), tarjetas 300px, peek con Cuando/Entonces/Requiere/Cifra-del-tarifario | **Todos los bloques son reglas de 1 salto** — no existe ni un camino multi-paso con pasos y transiciones (stepper vertical, esquema E3); estados borrador/vivo/retirado solo parciales; sin lista con historial |
| 7 | **Multi-agente / IA madre que deriva en silencio** | **CUMPLE** (con brechas menores) | Vista Agentes: "Derivación silenciosa · 7 hoy · 0 dudas" + especialistas Sofía (activa) y Destapes (punto ámbar "en entrenamiento") + "+ Agente"; tabs por agente en Caminos ("Sofía · 34 / Destapes · 12"); la traza abre con "Recepción → Sofía" | La madre **no es navegable** (dominios, mensaje ambiguo, errores de ruteo); no se ve **cómo Destapes pasa de "practicando" a "activa"** (gate del juez); detalle de Destapes solo toast |
| 8 | **Tracking punta a punta** (cotiza→confirma→entrega→cobra) | **CUMPLE** en tablero / **PARCIAL** en embudo | Chats → Tablero con 4 columnas: Cotizando ($530mil) → Por confirmar ($2,48M) → Por entregar → Cobrado·julio ($1,1M) con método de pago; Hoy con "$450mil en juego"; ficha del chat con estado de cotización; entregas "repartidor avisado" | **Embudo con TASAS** chat→cotización→cierre→cobro y vista semana/mes (feature E2 "que el dueño VEA qué vende el bot"); detalle de Cobrado (quién marcó, cuándo) solo toast; columna Dormidos 💤 del Kanban vivo no está |
| 9 | **Multimodal** (ver fotos, oír voz, leer PDF) | **CUMPLE** | 🎤 nota de voz con anotación "Transcrita: …30 baños…" y 📷 foto con "Vista: explanada techada…" EN el hilo (y la traza usa esos datos); módulo "Ojos y oídos" con switches voz/fotos/videos | El caso de **fallo explícito** ("no pude escuchar tu audio"); PDF/video en el hilo; prompt de visión por rubro (configurable, blueprint §5) |
| 10 | **Multi-canal** (WhatsApp hoy, Instagram después) | **PARCIAL** | Instagram en sidebar ("Pronto") y en Módulos→Canales con "Conectar · te guío — son 45 min"; Voz "llamadas perdidas → WhatsApp · pronto"; sublínea "WhatsApp" en el hilo | Todo es **promesa (toasts)**: ningún chat de otro canal, sin icono de canal en filas, sin ventana 24h/plantillas (E5) |
| 11 | **Genérico multi-rubro** (cada empresa su dixdybot) | **CUMPLE** | Dos agentes de rubros distintos (baños / destapes) con caminos propios; módulos con nombre genérico; "+ Agente: un rubro nuevo = un agente nuevo" | Nada crítico — el branding "destaperapido" en footer basta como instancia |
| 12 | **Toda mejora nace configurable/desactivable desde el panel** (req #1 ESTADO) | **CUMPLE** | Módulos con switch + config expandible ≤4 controles (Cotizador "Último click: Siempre yo", Seguimiento, Ojos y oídos, Entregas "Despachar: Con mi OK") | Estado ámbar "necesita config" (spec §3.4); que la vista se dibuja sola desde el schema es invisible (aceptable en prototipo) |
| 13 | **Personalidad configurable** | **PARCIAL** | Presets con descripción (Cercana, Precio con confianza, Nunca inventa) + "Así suena:" con ejemplo real | Selección de preset no interactiva; falta **largo** (Conciso/Estándar/Extenso); **"Nunca inventa" es una REGLA, no personalidad** — las secciones Reglas y Procedimientos de la spec §3.5 no existen |
| 14 | **Trazas de por-qué** (Resolution explicable) | **CUMPLE** | Burbuja del bot clickeable → "Por qué respondió esto": 5 pasos (dominio → datos completos → 3 caminos aplicados → cifra del tarifario → respondió); traza de la pausa | Solo 1 burbuja la tiene; el lado negativo de Resolution ("esta regla NO disparó porque X tuvo prioridad") no se muestra |
| 15 | **Handoff bot↔humano** | **CUMPLE** | Botón "Tomar" ("Sofía se calla en este chat") + composer "Escribe y Sofía se calla…" | Burbuja azul del dueño definida en Diseño pero nunca usada en un hilo; modo Nota ausente |
| 16 | **Design system único, cero variaciones** (req #2 ESTADO) | **CUMPLE** | Shell L invertida 240px, tokens r6, puntos 8px, chips vivo/borrador, ≤40 palabras de chrome, dark mode; **vista Diseño** con la regla "ningún componente nuevo fuera de esta página" | Desvíos menores de la spec (sin lista izq en Caminos, nav con 2 grupos extra); aceptables |
| 17 | **Historial / versionado / deshacer** | **PARCIAL** | Textos: "al publicar queda en el historial · deshacer restaura como borrador"; "publicado 10:58" tras aprobar | Ninguna vista de historial navegable (quién cambió qué, cuándo, rollback real) — es parte del contrato de confianza |
| 18 | **Costo/uso del cerebro visible** | **CUMPLE** (mínimo justo) | "$0 costo hoy" en métricas del agente; tooltip del footer "WhatsApp · cerebro · $0 hoy" | Nada más hace falta a este nivel |

---

## 2. Las brechas priorizadas para conversar con el dueño (8-12)

1. **El gimnasio quedó muy chico** — la visión dice "entrenamiento confiable hasta que venda
   mejor que él" y el prototipo lo despacha en 2 filas. Falta: botón **Probar ▸** (chat
   simulado + impersonar cliente + Por qué, spec r6), **replay navegable** y **veredicto del
   juez con hallazgos**. Es la brecha #1 porque toca el corazón declarado de la visión.
2. **Sin feedback por mensaje en el hilo** (👍👎 / corregir sobre burbuja del bot). El
   dashboard vivo YA lo tiene: el prototipo es una regresión frente a lo existente. Sin esto,
   "aprender juntos" se reduce a la pausa.
3. **La edición conversacional no conversa** — "Pedir" lanza un toast; hay que simular al
   menos un intercambio (pedido → la IA resume y muestra el diff → confirmar). Además el
   borrador dice "4 caminos" y el diff muestra 1: inconsistencia que confundirá en la demo.
4. **Métricas por camino casi ausentes** — solo en el peek de un camino. Poner uso/cierre por
   bloque en la cascada + un ranking (qué camino vende, cuál nunca dispara).
5. **No existe ningún camino multi-paso** — todos los bloques son condición→precio de 1
   salto; sin un ejemplo con pasos y transiciones (stepper vertical) no se entiende qué
   diferencia un "camino" de una regla suelta.
6. **La reanudación no se ve** — tras Enseñar, el hilo no muestra a Sofía retomando el tema;
   tampoco la respuesta enlatada que ve el cliente ni la escalada a 30 min. El flujo se
   CUENTA (traza) pero no se MUESTRA donde importa: el chat.
7. **Falta el embudo con tasas** — el tablero es la foto de hoy; no hay
   chat→cotización→cierre→cobro con porcentajes ni vista semana/mes (feature E2: "que el
   dueño VEA qué vende el bot").
8. **IA madre sin profundidad** — "Derivación silenciosa" no es clickeable: no se ven
   dominios, qué pasa con un mensaje ambiguo, ni cómo un agente pasa de "practicando" a
   "activa" (gate juez ≥4,0).
9. **Agentes sin Reglas ni Procedimientos** — la spec §3.5 tenía 4 secciones; "Nunca
   inventa" está archivada como personalidad siendo una regla con toggle.
10. **"Pruebas 5/5 ✓" es texto muerto** — el backtesting (re-jugar conversaciones históricas,
    patrón Fin) no es navegable; es la base técnica del "entrenamiento confiable".
11. **Historial solo prometido** — "deshacer restaura como borrador" sin vista de historial.
12. **Multi-canal solo como promesa** — bastaría un icono de canal en filas y un chat de
    ejemplo IG para que la visión multi-canal se vea, no solo se lea.

## 3. Lo que el prototipo hace MUY bien (defenderlo en la conversación)

- **Pausa-y-pregunta punta a punta**: decisión en Hoy → Enseñar → camino "nuevo" en cascada →
  traza del flujo con el código WhatsApp. Es el diferenciador de producto y es lo más pulido.
- **Trazas de por-qué** (turno y pausa): exactamente el Resolution explicable del blueprint.
- **Multimodal en el hilo** con anotaciones que la traza reutiliza (la nota de voz de los 30
  baños — el caso real perdido del 21-jul, ahora resuelto a la vista).
- **Tablero cotiza→confirma→entrega→cobra** con plata por columna.
- **Módulos administrables** y **vista Diseño** como guardián del "cero variaciones".
- Detalles de confianza: "cifra del tarifario, nunca del modelo", "$0 costo hoy", ✓✓ real.
