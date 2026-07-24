# Escalabilidad de dixdybot — ¿aguanta 100 mensajes/día? ¿Dónde está el techo real?

**Fecha: 24-jul-2026 · Analista de escalabilidad (informes ronda 9)**

Fuentes primarias: latencias medidas (`ronda3/latencia-real.md`), gating del bot vivo
(`SaSS/destaperapido/whatsapp-bot/.env` + `src/config.js` + `src/gating.js`, leídos hoy),
tarifas Meta Chile arbitradas (`ronda3/tarifas-cloud-api-chile.md`), Error 463
(`ronda3/arbitro-papers-repos.md`), límites del plan Max (`cerebro-claude-code-vs-api.md`
§d, verificado ronda 1), throughput Cloud API (`ronda3/coexistence.md`), contrato del
backend SQLite/FTS5 (`ronda8/contrato-backend.md`), precios API vigentes (skill oficial
claude-api, 24-jul: Haiku 4.5 $1/$5 · Sonnet 5 $3/$15, intro $2/$10 hasta 31-ago ·
Opus 4.8 $5/$25 · cache reads ≈0,1×), y el log vivo `data/conversaciones.jsonl`
(re-medido hoy: 3.663 msgs · 179 chats · 6→24 jul).

---

## Los números base (medidos, no supuestos)

| Parámetro | Valor | Fuente |
|---|---|---|
| Ratio mensual de referencia | ~2.617 msgs / 105 chats/mes → **~25 msgs/chat** | serie histórica destaperapido |
| Ratio re-medido hoy (17 días) | 3.663 msgs / 179 chats → **20,5 msgs/chat** | conversaciones.jsonl 06–24 jul |
| Reparto por remitente (hoy) | cliente 42% · bot 19% · dueño 39% | ídem (operación mixta humano+bot) |
| Msgs del cliente por chat | ~8,6 (1.537/179) | ídem |
| Latencia del cerebro (`claude -p`, opus) | mediana **8–18 s**, p90 16,6 s, máx 25,2 s; 0 timeouts | ronda3/latencia-real.md (n=30 + 3 corridas directas) |
| Delays deliberados anti-ban | debounce 30 s (1ª) / 12 s (sig.) ±30% + tipeo 1,5–9 s | .env + gating.js |
| Topes anti-ban vivos | **40 salientes/hora · 200/día** (globales), 12 respuestas/chat | config.js L89-90 (defaults; no sobreescritos en .env) |
| Plan Max | ~300 invocaciones/día caben en Max 5x (justo si es Opus) | cerebro-claude-code-vs-api §d |
| Cloud API Meta | 80 msg/s default (hasta 1.000 por upgrade auto; 20 con Coexistence); 250 conversaciones INICIADAS/día sin verificar (las respuestas NO cuentan) | coexistence.md + canales-whatsapp-2026 |
| Tarifas Meta Chile | service/utility **US$0,0200/msg entregado** (gratis en ventana 24h SOLO hasta 30-sep; se cobra desde el **1-oct-2026**); marketing US$0,0889 | tarifas-cloud-api-chile.md (rate card CSV oficial) |

Los dos ratios (25 y 20,5 msgs/chat) acotan el cálculo; uso 20–25 msgs/chat con ~40% del
tráfico siendo mensajes del cliente.

---

## (a) 100 mensajes/día = ¿cuántas conversaciones y turnos? ¿Cabe en Max? ¿Cuánto por API?

Interpretando "100 mensajes/día" como **100 mensajes ENTRANTES de clientes/día** (el caso
duro; si fueran 100 totales, todo es ~2,5× más holgado):

- **Conversaciones:** 100 ÷ 8,6 msgs-cliente/chat ≈ **10–12 chats/día** (~330/mes — hoy
  destaperapido mueve ~105/mes: es 3× el volumen actual).
- **Turnos de cerebro:** el debounce agrupa ráfagas (el cliente manda 1,3–1,7 mensajes por
  turno de respuesta) → 100 entrantes ≈ **60–80 turnos de cerebro/día**. Sumando extractor
  de ficha (~1/chat cotizado ≈ 10/día) y misceláneos (juez, recordatorios):
  **~70–90 invocaciones/día, redondeo 100/día**.

**¿Cabe en Max?** Sí, con 3× de margen. La ronda 1 verificó que ~300 invocaciones/día de
30–60 s (≈17–35 h Claude Code/semana) caben en Max 5x — justo o corto **si el cerebro es
Opus** (15–35 h/sem de tope Opus). A 100 invocaciones/día son ~6–12 h/sem: cómodo incluso
en Opus y compartiendo la cuenta con el uso interactivo de Alejandro. Riesgos que no
desaparecen: buckets de 5 h en ráfagas, límites "aproximados" modificables por Anthropic,
y la zona gris de ToS de un bot comercial 24/7 en suscripción (si dixdybot se vende a
terceros, la doc obliga API key por cliente).

**Costo si fuera API directa** (prompt delgado ~6k in / 4k cacheables / 400 out — escenario
A de la ronda; precios skill claude-api 24-jul):

| Modelo | 100 invocaciones/día | 300/día (techo Max) |
|---|---|---|
| Haiku 4.5 ($1/$5) | **≈ US$9–13/mes** | ≈ US$27–40/mes |
| Sonnet 5 intro ($2/$10, hasta 31-ago) | ≈ US$18–27/mes | ≈ US$55–80/mes |
| Sonnet 5 pleno ($3/$15) | ≈ US$27–40/mes | ≈ US$80–120/mes |
| Opus 4.8 ($5/$25) | ≈ US$65–90/mes | ≈ US$190–270/mes |

OJO: pagar `claude -p` (harness completo, 20–50k tokens/invocación) por API sería
US$250–900/mes — la peor combinación. El plan B barato exige el camino API **delgado**.

## (b) Baileys a 100 entrantes/día: ¿bajo los topes 40/h y 200/d?

Salientes esperados: 60–80 turnos × 1,5–2 globos/turno ≈ **100–140 globos/día** (+
recordatorios 💤 y outbox). Contra los topes:

- **200/día: pasa, con margen fino** (~60–100 de holgura). El tope diario se vuelve la
  restricción dominante alrededor de **~150 entrantes/día** (~15 leads/día).
- **40/hora: pasa en promedio, roza en picos.** Si el 25–30% del tráfico cae en la hora
  peak (mediodía), son 25–42 globos/hora → el gate global puede activarse y el bot **calla
  hasta que baje** (comportamiento seguro por diseño: los entrantes no se pierden, la
  respuesta se atrasa).
- **Ajuste para picos:** subir `MAX_ENVIOS_HORA` de 40 → **60** manteniendo 200/día
  (sigue siendo perfil conservador: 60/h de RESPUESTAS a chats calientes no se parece a
  spam), y consolidar globos por turno (2→1) recupera ~40% de holgura gratis.
- **Riesgo con perfil solo-responde:** el Error 463 "Reachout Timelock" (confirmado
  activo jul-2026 en Baileys y whatsmeow) castiga envíos a números **sin historial
  reciente** (token TC ~28 días). El bot que solo responde dentro de conversaciones vivas
  tiene el token fresco → riesgo bajo. Lo que SÍ queda expuesto: los seguimientos 💤 a
  chats fríos >28 días (pueden figurar "enviados" sin llegar, y reintentar escala a ban).
  Regla: recordatorios solo a chats con actividad <21 días y vigilar el ✓✓ real, nunca el
  "sent". El riesgo de ban arbitrario de Baileys no baja a cero por cumplir topes — crece
  con el volumen total; a 100/día sostenidos ya conviene tener la salida Cloud agendada.

## (c) El cuello real del cerebro: latencia × chats simultáneos

Presupuesto de espera antes de degradar (>90 s percibidos): 90 − debounce 12–30 s − tipeo
1,5–9 s ≈ **~50–75 s disponibles para pensar+cola**. Con servicio de 8–18 s (uso 13 s
promedio):

- **Aun asumiendo cerebro estrictamente SERIAL** (peor caso; en realidad cada chat arma su
  propio timer y puede lanzar `claude -p` en paralelo): capacidad ≈ 3.600/13 ≈ **275
  turnos/hora**. Para que un turno espere >50 s de cola se necesitan **~4–5 turnos
  simultáneos en la misma ventana de 13 s**.
- A 100 entrantes/día, la hora peak trae ~14–20 turnos/hora → utilización ρ ≈ 0,05–0,07.
  Concurrencia esperada = λ×S ≈ 0,06 turnos. La probabilidad de 5 simultáneos es
  despreciable (Poisson, p < 10⁻⁵). **A 100/día el cerebro nunca es el cuello.**
- El cuello aparece recién a **~200–220 turnos/hora sostenidos (ρ≈0,8)** ≈ 2.000–2.600
  entrantes/día — 20–25× la meta. Antes de eso golpean el tope de Max (~300
  invocaciones/día) y el gating de Baileys (200 salientes/día).
- Confiabilidad medida: 0 timeouts (120 s) y 0 fallos en los logs vigentes; la cola por
  conversación garantiza además que un chat lento no bloquea la UX de otro.

**Conclusión (c): la latencia de 8–18 s queda enmascarada por los delays anti-ban
deliberados; el sistema aguanta ~4–6 chats pensando EN EL MISMO INSTANTE antes de pasar
de 90 s, y ese instante estadísticamente no ocurre bajo ~1.000 msgs/día.**

## (d) Cloud API: techo y costo mensual

**Techo técnico: irrelevante para esta escala.** 80 msg/s default (= 288.000/hora; hasta
1.000 msg/s por upgrade automático; 20 msg/s si se usa Coexistence — igual sobra). El
límite operativo real sin verificación de empresa son 250 conversaciones INICIADAS por el
negocio/día — **las respuestas no cuentan**, y dixdybot solo responde → sin techo práctico.

**Costo (Chile, rate card oficial; se cobra por mensaje SALIENTE entregado):**

| Escenario | Salientes/mes | Hoy → 30-sep | Desde 1-oct-2026 (US$0,02/msg) |
|---|---|---|---|
| Volumen actual (~120 chats/mes × 8) | ~960 | US$0 | **US$19/mes** (~CLP 17.000) |
| **100 entrantes/día**, globos como hoy (~120/día) | ~3.600 | US$0 | **US$72/mes** (~CLP 64.000) |
| 100 entrantes/día, globos consolidados (1/turno) | ~2.100 | US$0 | **US$42/mes** (~CLP 37.000) |
| **1.000 entrantes/día**, consolidado | ~21.000 | US$0 | **US$420/mes** (~CLP 370.000) |
| 1.000/día sin consolidar | ~36.000 | US$0 | US$720/mes (~CLP 640.000) |

Notas: los clicks de ads CTWA abren ventana de 72 h GRATIS (sin cambio anunciado) — con
tráfico de Google/Meta Ads parte del volumen no se cobra. Marketing (US$0,0889) no aplica:
el bot no inicia. Meta publica la tarifa definitiva post-oct antes del 1-sep — recalcular
en septiembre. **La consolidación de globos pasa de manía estética a ahorro directo de 40%
en Cloud API.**

## (e) SQLite/panel a 3.000 y a 30.000 msgs/mes

Con ~0,5 KB/fila (texto + metadata) y FTS5 (~2× el tamaño):

| Volumen | Filas/año | Tamaño/año (con FTS5) | Veredicto |
|---|---|---|---|
| 3.000 msgs/mes (meta 100/día) | 36.000 | ~35 MB | Trivial |
| 30.000 msgs/mes (1.000/día) | 360.000 | ~350 MB | Cómodo — SQLite maneja millones de filas; FTS5 responde en ms |

Las vistas del panel (V1–V8 del contrato ronda8) son lookups indexados + un endpoint
agregado de contadores — a 360k filas/año siguen en milisegundos. **El que NO escala es el
esquema actual**: `conversaciones.jsonl` se lee COMPLETO en operaciones como
`newestPersistedMs()` y la hidratación (O(n) por archivo); a 30.000 msgs/mes eso es re-leer
cientos de MB al año por reinicio y se nota. El contrato ronda8 (6 tablas SQLite + FTS5
nativo, 0 deps, 1 escritor) resuelve exactamente esto y queda holgado hasta ~10× más.
**El almacenamiento no es un techo en ninguna configuración.**

## (f) La RAMPA de aprendizaje (límite de leads/día, default 10)

**Validación con números — el caso "empresa con demasiados leads mientras entrena":**

- 10 leads nuevos/día × 8,6 msgs-cliente ≈ **86 entrantes/día ≈ exactamente la meta de
  100/día**. El default 10 no es arbitrario: es la meta del dueño expresada en leads.
- Carga resultante: ~55–70 turnos de cerebro/día (cabe 4× en Max), ~90–120 salientes/día
  (bajo el gating 40/200 sin tocar nada), ~2.600 msgs/mes (la escala EXACTA que el panel y
  SQLite ya digieren hoy).
- Carga de supervisión: 10 conversaciones/día es lo que un dueño revisa en ~20–30 min en
  el panel/gimnasio — el volumen que permite ENSEÑAR (💡 por mensaje, pausas
  junior→senior) sin ahogarse. Con 50 leads/día entrenando, ni el dueño ni el juez
  alcanzan a corregir: la rampa protege la calidad del aprendizaje, no solo la infra.
- Mientras tanto los leads sobre el límite siguen el flujo actual (los atiende el humano o
  esperan), y el número/cuenta Meta se configura en paralelo sin presión — las respuestas
  no cuentan contra las 250 conversaciones/día del número sin verificar.

**Criterio de graduación propuesto** (mismo listón 4,0 que ya usa el contrato ronda8 para
activar agentes practicantes):

> Subir el límite un escalón (10 → 25 → 50 → 100) cuando, en ventana de 7 días o ≥50
> conversaciones (lo que tarde más): **nota del juez ≥ 4,0 promedio** Y **≥80% de los
> chats resueltos sin pausa al dueño** (pausas/dudas < 20%) Y **0 correcciones graves**
> (precio inventado, dato falso). Si la nota cae bajo 3,5 en cualquier ventana, se baja un
> escalón automáticamente (reversible, como todo camino).

Techo de la rampa en Baileys: **no graduar más allá de ~15–20 leads/día (~150–200
entrantes)** — ahí golpean el gating de 200/día y la zona de riesgo de ban. Ese escalón es
el gatillo para conmutar a Cloud API, no para tocar los topes.

## (g) VEREDICTO

**100 mensajes/día es CÓMODO en las tres configuraciones.** Ningún componente pasa del 35%
de su capacidad: cerebro ~30% del cupo Max, salientes ~50–70% del gating (el único
ajuste fino), latencia a 5% de utilización, SQLite a <1%.

**Techo real de cada configuración (mensajes entrantes/día sostenidos):**

| Configuración | Techo | Qué lo fija | Costo mensual en el techo |
|---|---|---|---|
| **Baileys + Max** (hoy) | **~150–200/día** (~15–20 leads) | Gating 200 salientes/día + riesgo de ban creciente + Error 463 en seguimientos fríos | US$0 marginal (Max ya pagada) |
| **Cloud API + Max** | **~350–450/día** (~40 leads) | Cupo Max ~300 invocaciones/día (justo si el cerebro es Opus); Meta ya no limita | US$0 hasta 1-oct; luego ~US$40–90 en mensajes |
| **Cloud API + API delgada** (Haiku/Sonnet + caching) | **miles/día** (el primer límite técnico serio: ~2.000–2.600/día si el cerebro fuera serial; 80 msg/s de Meta y SQLite quedan lejos) | El presupuesto, no la técnica: costo LINEAL ≈ US$1–1,3 por cada 10 entrantes/día/mes en Haiku + US$0,02/saliente | a 1.000/día: ~US$90–130 cerebro + ~US$420 Meta |

**El camino del dueño (Baileys unas semanas para entrenar → Meta oficial) es correcto y
tiene fecha natural:** la ventana gratis de Meta muere el 1-oct-2026, y el blueprint ya
fija la migración del número vivo en la 2ª quincena de septiembre. Baileys queda como
rampa de entrenamiento y de clientes nuevos.

**Las 3 perillas que hay que tocar al crecer (en orden):**

1. **El límite de leads/día de la rampa** (default 10): la perilla de arranque y de
   calidad. Se gradúa 10→25→50→100 con el criterio juez ≥4,0 + <20% pausas + 0 graves;
   se degrada sola si la nota cae. Gratis, reversible, y protege el entrenamiento.
2. **El canal**: Baileys → Cloud API al pasar ~15 leads/día o el 30-sep, lo que llegue
   primero. Elimina gating anti-ban, Bad MAC y ban arbitrario (ban-con-proceso + acks por
   webhook); presupuestar US$0,02/saliente desde el 1-oct y **consolidar globos por turno**
   (−40% de la cuenta Meta). Mientras siga en Baileys, el único retoque es
   `MAX_ENVIOS_HORA` 40→60 para picos.
3. **El cerebro**: `claude -p` + Max ($0 marginal) → API delgada Haiku/Sonnet con caching
   al acercarse a ~300 invocaciones/día, o ANTES si dixdybot se vende a terceros (ToS
   exige API key por cliente). El wrapper ya está diseñado para que sea cambiar una
   variable de entorno; a estos volúmenes Haiku por API (US$27–40/mes a 300/día) cuesta
   menos que una Max 5x.

Fuera de las perillas: el backend SQLite/FTS5 del contrato ronda8 hay que construirlo de
todos modos (el JSONL actual es lo único del stack que degrada a 30.000 msgs/mes), y el
juez/replay del gimnasio son los que hacen creíble el criterio de graduación — son
prerequisito de la perilla 1, no un extra.
