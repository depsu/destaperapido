# DIXDYBOT — Estado del proyecto y mapa de documentos

> 🆕 **30-jul-2026 · ¿Chat nuevo? Empieza por [`RETOMAR-AQUI.md`](RETOMAR-AQUI.md)** — el
> traspaso corto (dónde quedamos, qué sigue, las leyes de la casa y las dos cuentas de
> Claude Code del Mac). El detalle técnico de lo encontrado y el plan por etapas está en
> [`auditoria-backend-2026-07-30.md`](auditoria-backend-2026-07-30.md); **E0 (Cinturón) ya
> está cerrada y en vivo**. Este documento sigue siendo el mapa largo del proyecto.

**Última actualización:** 26-jul-2026 (S5: el negocio en el panel, el cerebro reparado y
**el pedido que ya nace solo**) · **Estado: CONSTRUCCIÓN EN MARCHA.**

---

## 🎯 QUÉ ES ESTO (léelo antes que cualquier otra cosa)

**dixdybot es un PRODUCTO que se le vende a muchos negocios distintos.** No es el bot de
destaperapido. Una peluquería, un taller, un dentista y un arriendo de baños químicos
tienen que poder usar el mismo software: lo que cambia entre ellos son sus *datos*
(etapas del embudo, tarifario, campos de la ficha, persona del bot), nunca el código.

**destaperapido es el primer cliente y el conejillo de indias.** Paga, usa el bot de
verdad todos los días, y por eso es el que descubre los problemas primero. Que un
requisito venga de él NO lo hace genérico.

**La regla que decide dónde va cada cosa:**

> Si sirve **solo a los baños químicos** → va en los datos del cliente
> (`~/SaSS/destaperapido/dixdybot-data/ajustes/*.json`).
> Si sirve **a cualquier negocio** → va en el molde (`SaSS/DIXDY/dixdybot/src/`).
> Si el molde necesita saber algo del rubro para funcionar, **el diseño está mal**.

Ejemplo real del 26-jul: los checks del despacho. "No despachar sin saber cuánto vale"
sirve a cualquiera → al molde (`Etapa.requiere_monto`). "Cantidad de baños" es del rubro →
al ajuste del clon (`ajustes/entregas.json`), por la puerta `campos_extra` que el módulo
`entregas` abre justo para eso.

### ⚠️ Dos cosas incómodas que hay que saber

1. **Hoy el molde ES el programa que corre en producción.** El servicio launchd arranca
   `SaSS/DIXDY/dixdybot/src/index.ts --datos ~/SaSS/destaperapido/dixdybot-data`. No hay
   copia por cliente todavía, aunque `dixdybot/CLAUDE.md` la describa. **Cada cambio al
   molde es un cambio en vivo al cliente que paga.**
2. **No existe camino para montar el segundo negocio.** Las herramientas de arranque
   (migrador, destilador de caminos) exigen un bot anterior del cual copiar, y el
   tarifario del cotizador solo sabe expresar precios con la forma de destaperapido. Antes
   de vender esto a otro rubro hay que resolver eso — y no es un bug, es trabajo por hacer.

---

## 🚦 EMPIEZA POR AQUÍ (26-jul-2026, noche) — 924 tests verdes, tsc limpio

**Lo más importante que hay que saber antes de tocar nada:**

> ### ✅ EL TO-DO DEL BACKEND QUEDÓ CERRADO (26-jul noche, `3586604`..`69f6fe8`)
>
> La ronda que faltaba antes de la ronda de pruebas. TODO verificado contra el panel
> vivo (8793, reiniciado). Detalle completo para el front:
> `dixdybot/PARA-EL-FRONT-simulador.md` (ANEXO 2). En corto:
>
> 1. **El paso ② de la Duda tiene puerta** (`/api/dudas/:id/{afinar,resumir,seguir,
>    confirmar}`): el motor existía sin endpoints. Confirmar corre el MISMO candado del
>    orquestador y, al activarse, **la tarifa acordada queda escrita en el tarifario**
>    (`cotizador.tarifas_especiales` → bloque «TARIFAS ACORDADAS» que ve el cerebro).
> 2. **La contra-argumentación discute con datos**: `responder` arma la `ReferenciaPrecio`
>    desde el tarifario del clon (`referenciaTarifario`); se acabó el «sin datos duros
>    para objetar» perpetuo. `DecisionPendiente` expone `turnos/evaluacion/decisionFinal/
>    urgente` y el contador de Hoy solo cuenta lo urgente.
> 3. **Bitácora del chat** (`GET /api/chats/:id → bitacora`): consulta sobre el ledger
>    que ya existía, en castellano de persona. Solo en el fetch completo.
> 4. **El resumen vive en la ficha** (`chat_resumenes`, tabla nueva): GET genera solo si
>    hay algo nuevo, regenerar con tope 2/hora, citas validadas contra el hilo, cifra de
>    Plata solo si aparece textual. Probado con el cerebro real: 16 s primera vez, 19 ms
>    después. Lo conversado con el agente también lo desactualiza.
> 5. **Se acabó el slug «sofia»**: `Especialista.alias` (dato del clon) — los 186 chats
>    migrados se PRESENTAN como Sofía sin reescribir la base (el resolver de agente_id
>    NO se volvió a intentar).
> 6. **185 campos con `.describe()`** (el diccionario puente del panel ya puede morir) y
>    el catálogo de Diseño **lee la escala de tokens.css** (etiquetas verdaderas + las 13
>    variables --t*/--p*/--m* servidas).
>
> **Lo que sigue SIN existir, a propósito:** las tarjetas de aprobación y las
> herramientas del agente (`/api/acciones`, deshacer 8 s server-side, voto 👍👎). El
> agente lee y responde; actuar espera las tarjetas.

> ### ✅ EL PEDIDO YA NACE SOLO — bloqueante del cutover RESUELTO (26-jul, `008d8b3`)
>
> Era esto: `crearPedido` tenía **un solo llamador en producción** (el migrador), los 23
> pedidos de la base viva eran todos `p-mig-*` y el sistema nuevo jamás había abierto una
> ficha. Con el número tomado, los clientes iban a conversar bien y el tablero a quedarse
> congelado. Medido entonces en la base viva: **75 chats vivos sin pedido**, 73 de esa
> semana, 62 con 7+ mensajes — negocio sin ficha.
>
> **Cómo quedó** (`src/core/nacimiento.ts`, motor puro + cableado en el orquestador):
> el pedido nace **al primer dato duro**, y la extracción de esos datos viaja en la
> **misma llamada** del turno (`SalidaTurno.datos`) — cero llamadas nuevas, cero plata
> extra. Qué campo es "duro" lo declara el módulo dueño del campo (`AporteCampoFicha.duro`:
> entregas → dirección y fecha; cotizador → pedido) y el clon suma los suyos por
> `campos_extra` (destaperapido: `cantidad_banos`). El ajuste del dueño es
> `embudo.nacimiento` (`modo`, `con_monto`, `campos`) y su lista MANDA.
>
> **Tres decisiones que conviene no revertir sin leer por qué:**
> 1. **La cifra conversada NO es el valor del pedido.** Abre ficha y queda a la vista en
>    `monto_conversado`, pero `montoNeto` sigue en null: las cifras salen del tarifario,
>    jamás del modelo. Un precio inventado pasaría el check de `requiere_monto` y saldría
>    un camión. ⚠️ **Si Alejandro quiere que el precio acordado entre como valor real, es
>    una decisión suya — hoy está deliberadamente frenado.**
> 2. **El bot no pisa al dueño.** `datos_del_bot` (campo reservado) marca qué escribió él:
>    corrige lo suyo cuando el cliente se desdice, nunca lo que el dueño arregló a mano.
> 3. **Abrir sí, mover no.** Nace el origen `bot` y `moverPedido` lo rechaza; no está en el
>    enum de `origenes`, así que tampoco se le puede conceder desde el embudo.json.
>
> **Lo que NO hizo falta, contra lo que decía este documento:** `motor/efectos.ts`. Al
> nacer del DATO y no del paso de un camino, la ficha se abre también fuera de todo camino
> — que es justo donde se perdía el cliente. La cadena de efectos sigue sin existir
> (`Efecto` y `Paso.efectos` están en `schemas/camino.ts`, los caminos declaran cero
> efectos) y ahora es una mejora, no un bloqueante.
>
> **Sigue abierto:** `orquestador.ts` **le pide `paso_completado` al modelo y nunca lee la
> respuesta** (`pathSiguiente` solo usa `sigue` y `transicion_elegida`). Cuesta tokens en
> cada turno y no hace nada: o se usa (con efectos) o se deja de pedir.
>
> **Efecto colateral querido:** un negocio con embudo activo pide salida estructurada en
> TODOS los turnos (ahí viaja la extracción). La prosa simple quedó para el negocio sin
> tablero: apagar el módulo `embudo` ES ese interruptor.

### Lo que se hizo el 26-jul

- **`fea6c39` · los 4 checks del despacho.** Regla de Alejandro: no sale a terreno sin
  dirección, día, cantidad y valor. Los tres primeros son campos de ficha (`requiere` del
  embudo); el VALOR no se podía exigir porque `montoNeto` es COLUMNA del pedido, no ficha
  → `Etapa.requiere_monto` (default `false`, retrocompatible). El rechazo devuelve el
  porqué guardado en `CAMPO_SIN_MONTO`: es una instrucción, no un no. Verificado contra la
  base viva: los 6 pedidos ya despachados pasan los cuatro.
- **`f2d2a56` · módulo `entregas`.** El commit anterior dejó una TRAMPA: exigía `direccion`
  y `cantidad_banos` y **ningún módulo declaraba esos campos** (los únicos del molde eran
  `comuna`/`pedido`/`correo` del cotizador) → el panel no los dibujaba y el dueño no podía
  completarlos a mano. `entregas` declara dirección y fecha, aporta la etapa `por-entregar`
  y trae **`campos_extra`**: la vía para que un CLON declare campos de su rubro sin que el
  molde sepa del rubro (destaperapido suma `cantidad_banos` en
  `dixdybot-data/ajustes/entregas.json`). **Ojo:** los ids de ficha son snake_case, a
  diferencia de los ids de etapa/módulo, que son kebab estricto.
  Incluye **dedup de etapas en `componerAportes`** — embudo y entregas nombran ambos
  `por-entregar` y el tablero la pintaba dos veces; gana la primera (= la del dueño,
  porque `embudo` va antes en `MODULOS`) y hay test que fija ese orden.
- **`3869b2c` · el cerebro volvió a pensar.** Primera prueba de punta a punta contra la
  instancia viva: el bot contestaba la plantilla de emergencia. La sospecha obvia (el
  envoltorio del CLI 2.1.220 cambió) era **FALSA** — se verificó campo por campo. La causa:
  pidiéndole `camino: { sigue, paso_completado }`, el modelo leyó `sigue` como
  "¿CUÁL sigue?" y devolvió el **id del camino** donde iba un booleano; JSON perfecto, con
  la respuesta al cliente ya escrita, tumbado entero por Zod. Arreglo en dos capas: el
  prompt declara los tipos (plan A) y `booleanoTolerante()` endereza (red). **Los negativos
  incluyen los del castellano** (`ninguno`/`ninguna`/`nada`/`no aplica`): el prompt está en
  español y sin eso un `"sigue": "ninguno"` se leía como SÍ — invertir la respuesta es peor
  que perderla. El aviso al dueño ya adjunta el texto que llegó.

### 🧪 EL SIMULADOR (26-jul, `8034aba`) — la forma corta de probar

**http://127.0.0.1:8793/simulador.html**, en una ventana aparte. Varios clientes de
mentira a la vez, cada uno su columna; se les escribe como cliente y se ve llegar la
respuesta. Botón ✕ para borrar un ensayo entero (chat + ficha + preguntas al dueño).

- **Qué es un ensayo:** lo que entra por el CANAL de pruebas (`sim`). No hay marca que
  poner: los 3 ensayos que ya existían quedaron cubiertos solos.
- **Dónde dejaron de ensuciar:** lista de chats, contadores, decisiones de Hoy, resueltas,
  mensajes del día, **el tablero y el hero de plata**. Los dos últimos aparecieron
  probando en vivo: como el pedido nace al primer dato duro, un ensayo con dirección
  abría ficha y se metía en «Cotizando» (pasó con p-1 y p-2).
- **Se ven cuando quieras:** ajuste `panel.ver_chats_de_prueba` (apagado por defecto).
  Esconder NO es borrar: siguen en la base como histórico.
- **Los contadores del día** no se filtran después (la tabla no guarda de qué chat vino
  cada uno): se decide ANTES, con `EntradaTurno.esPrueba`. Todo lo demás del turno corre
  idéntico — si el ensayo no se comportara como un cliente, no probaría nada.
- **Borrar** exige que el chat sea del canal de pruebas (409 si no): es la única defensa
  contra llevarse el chat de un cliente que paga, y está probada.
- **`7a93780`:** el id de un pedido ya no se reusa (tabla `correlativos`, solo sube).
  Con el MAX() de antes, borrar un ensayo liberaba su id y el próximo cliente real lo
  heredaba — con el ledger inmutable, dos historias bajo el mismo nombre.

### 💰 EL BOT YA COTIZA (26-jul, `0ea0a8b`) — decisión: «cotiza solo, con tope»

El agujero estaba escondido: el clon tenía 4,3 KB de precios cargados y **ninguno llegaba
al bot** (`precioPara()` sin llamadores; `fragmentoPersona`, declarado en el contrato de
módulo desde r8, sin que nadie lo llamara). Una prueba real terminó en una duda que decía
*«no hay herramienta de tarifario disponible»*.

Ahora la **voz del bot** = persona del clon + lo que aporta cada módulo ACTIVO
(`Modulo.fragmentoPersona`), compuesta POR TURNO. El cotizador rinde su tabla con el
con-IVA ya calculado, los huecos dichos («NO tiene valor de lista») y el TOPE: comuna
fuera de zona, combinación sin valor, rebaja bajo el piso → `falta_camino`, decide el
dueño. Apagar el módulo borra la tabla de la voz y el bot vuelve a preguntar todo.

Verificado en vivo: *«un baño por un mes en Maipú»* → **160mil neto** (su fila exacta);
*«lo mismo en Valparaíso»* → no inventa, espera honesta y la pregunta queda para él.

⚠️ **Lo aceptado a sabiendas:** el total de N unidades lo multiplica el modelo (una tabla
por cantidad inflaba el prompt). Acotado porque `montoNeto` del pedido nunca sale del
modelo: un total mal sumado se ve en el chat, no entra al tablero.

### 🗣️ EL CARRIL DEL AGENTE ya responde (26-jul, `1a9b44a`)

Era la única puerta que el panel llamaba y no existía. Módulo `agente-chat` (tabla propia,
config en Ajustes, apagable): `POST /api/chats/:id/agente` + `GET .../agente/sesion`.

- **Lee y responde; NO ejecuta acciones.** Sin las tarjetas de aprobación no se manda un
  WhatsApp ni se fija un precio — y el prompt se lo dice al modelo, así que si le piden
  actuar contesta que todavía no puede.
- **Los chips mandan de verdad:** `contextoDe` devuelve el texto del prompt y las piezas en
  el mismo objeto, así que el número del chip no puede divergir del prompt. Las piezas son
  el chat, la ficha y **una por módulo que aporte su fragmento** (hoy `cotizador`): en otro
  rubro serán otras sin tocar código.
- **La señal de vida** (`pensamiento` escrito ANTES de llamar al cerebro) y `viejo`
  calculado al leer, no guardado (sin crons nuevos; un turno muerto se ve viejo solo).
- Probado con un chat real de 35 mensajes: resumió el caso y **avisó solo** que faltaba la
  comuna para poder contrastar los precios con el tarifario.
- **Sigue faltando de §3/§7:** las tarjetas de aprobación con el deshacer de 8 s, la
  bitácora del chat y el resumen que vive en la ficha.

### ⚠️ Lo que la auditoría de configurabilidad dejó abierto (VERIFICADO en código)

1. **La voz del clon no existe como archivo.** `data/persona/base.md` NO está, así que la
   base es la plantilla genérica del molde. **Ojo:** eso NO significa que el bot no sepa
   del negocio — lo que sabe le llega por los CAMINOS (verificado: «aseo semanal, papel
   higiénico» sale de un camino publicado, no lo inventó) y ahora por el tarifario. Falta
   igual: la persona se lee UNA vez al arrancar y no es un módulo, así que no se edita
   desde el panel.
2. **Los caminos no se crean ni se editan desde el panel** (solo aprobar/rechazar), y los
   especialistas de `agentes.json` son decorado: el turno no los usa para elegir caminos.
3. **El bautizo de chats sigue pendiente** (P7): la lista muestra números en vez de
   «Carolina · Melipilla». Ahora es barato — los datos ya se extraen en cada turno.

### Cómo probar HOY (sin WhatsApp, sin cuenta Meta, sin gastar)

1. El servicio corre por launchd: `launchctl kickstart -k gui/501/com.dixdy.dixdybot-panel`.
   Panel en **http://127.0.0.1:8793**. Datos en `~/SaSS/destaperapido/dixdybot-data/`.
2. `panel.entrada_de_prueba` quedó **prendido** en `ajustes/panel.json`. Escribirle al bot
   como si fueras cliente:
   `curl -s -X POST http://127.0.0.1:8793/api/simular/entrante -H 'Content-Type: application/json' -d '{"texto":"...","de":"quien-sea"}'`
   El mismo `de` continúa la MISMA conversación. El canal `sim` se monta solo.
3. Leer el hilo: `GET /api/chats/sim%3A<de>`. El cerebro tarda ~12-30 s (motor `cli`, la
   suscripción de Alejandro; **no hay `ANTHROPIC_API_KEY`** — el motor `api` siempre da
   `no_disponible` y eso NO es un bug).
4. Si sale *"Dame un momento, ya te confirmo."* el cerebro NO pensó: mirar la última línea
   de `dixdybot-data/panel.log`, que ahora dice la causa con el texto recibido.

### Estado de los canales (26-jul)

`wa-baileys`: **apagado**, sin número — nunca se ha vinculado un WhatsApp real.
`wa-cloud`: apagado, le faltan los 4 requisitos de Meta. Único canal vivo: `sim`.

### Decisiones de Alejandro del 26-jul (ya tomadas, no volver a preguntar)

| Tema | Decisión |
|---|---|
| Los chats sin pedido | Se llaman **"cotizando"** — van en esa pestaña (⚠️ **sin implementar**) |
| Checks del despacho | **Los cuatro**: dirección, día, cantidad, valor ✅ hecho |
| Comprobante de pago | **Mueve solo a Cobrado** (eligió el automático sobre avisar-y-confirmar) ⚠️ sin implementar |
| Cuándo nace el pedido | **Al primer dato duro** ✅ hecho (`008d8b3`) — ver el bloque de arriba |

**Sobre el comprobante automático — advertencias que Alejandro ya escuchó y aceptó:**
(1) la transición `por-entregar→cobrado` **no acepta origen `camino`**, solo `dueno`/`externo`;
(2) quien paga por adelantado está en `por-confirmar` y **no existe transición** desde ahí a
`cobrado`; (3) `cobrado_cuando: 'total'` y una foto no prueba el monto. Las dos primeras son
cambios en SU embudo que aún no ha autorizado explícitamente — **pídeselos antes de tocar**.

### Lo que necesita a Alejandro

- **Llave de API de respaldo** (cuesta plata): sin ella, si su suscripción falla el bot
  queda mudo. Hoy la cadena es `cli → api → plantilla` y el eslabón del medio no existe.
- **Vincular un WhatsApp de pruebas** (2 min, con un número secundario, NUNCA el que vende).
- **Aprobar los 30 caminos** en lote (tarea #9) — y ahí se declara en qué paso nace el pedido.
- Expediente Meta (tope **30-sep**) y la decisión del servicio de sombra (cuesta cuota).

### Reglas de esta obra que no se negocian

- **NO tocar el bot vivo** de `~/SaSS/destaperapido/whatsapp-bot/` — es lo que vende hoy.
  Solo lectura. Nada de `kill`, `restart`, `npm`, `launchctl unload`.
- **NUNCA agregar una columna a `src/db/esquema.sql`**: todo es `CREATE TABLE IF NOT
  EXISTS` y SQLite ignora en silencio una columna nueva si la tabla ya existe. Los tests
  usan `:memory:` (verde), tsc verde, commit verde — y la base viva no la recibe. Salida
  probada: tabla lateral en las `migraciones` del módulo. Un `CREATE INDEX IF NOT EXISTS`
  **sí** se aplica en cada arranque.
- **Reparto por ARCHIVOS, no por tema.** El FRONT edita `dixdybot/panel/pwa/*`; el backend
  no los toca. Ver `REPARTO-SESIONES.md`.
- `pnpm exec tsc --noEmit` **y** `pnpm exec vitest run` en verde, o no hay commit.

---

> **Arranque de S5 (25-jul, tarde) — dos agujeros de fondo tapados, 647 tests verdes:**
> **(1) El mensajero** (`core/mensajero.ts` + `modulos/mensajero`, núcleo): el pipeline
> hacía `await canal.enviarTexto(...)` y TIRABA el resultado — un envío fallido dejaba al
> cliente esperando para siempre y al dueño sin enterarse; y los acuses que los canales ya
> emitían al bus no los escuchaba nadie (las 3.979 filas de la instancia tenían `estado`
> vacío). Ahora: ritmo humano por ajuste, topes anti-bloqueo **leídos de la base** (un
> reinicio ya no regala cupo, a diferencia del bot vivo), reintentos solo de lo
> reintentable (`auth` NO se reintenta), acuses **monótonos en el UPDATE**, y nada en
> silencio. **(2) La ingesta** (`modulos/ingesta`, apagable): fotos y documentos se
> guardan y **el cerebro los MIRA por su ruta en el mismo turno** — 1 llamada, $0 de API
> extra, verificado con `claude -p` antes de construir sobre el supuesto. El audio nace
> SIN transcripción (es plata nueva): el bot pide que se lo escriban en vez de inventar.
> Probado con el cerebro real: foto → describió los colores exactos en 28,1 s; audio →
> "no puedo escucharlo, ¿me lo escribes?" en 16,8 s, sin cifras inventadas.
> **(3) El adaptador `wa-baileys`** (25-jul, tarde — `src/canales/wa-baileys/` +
> `cli/vincular.ts`, 706 tests verdes): el molde ya puede hablar por el número propio.
> Construido leyendo el bot vivo en SOLO-LECTURA y trasplantando sus **28 cicatrices**
> documentadas, no reinventándolas. **Reparto núcleo/adaptador:** lo genérico (ritmo,
> topes desde la base, reintentos, escalera de acuses) se queda en `core/mensajero.ts`;
> lo que solo existe en WhatsApp no oficial (reconexión + circuit breaker 8/5min→10min,
> candado cifrado corrupto y su sanación, jid canónico literal incl. `@lid`, presencia
> real) vive en el adaptador — el core nunca ve un vendor. **Decisión que se apartó del
> plan:** el legado del emisor se REESCRIBIÓ en TS conservando cada número y su razón, en
> vez de copiar los `.js` (aceptar JS mezclado abre una excepción permanente en tsconfig).
> Cerrado con test que MUERDE (verificado por mutación deliberada): eco de envíos propios,
> los DOS canales de acuses, 401 sin reintento, sanación con 3 min + 1 reintento + guarda
> de presencia, acuse del reenvío reportado con el id ORIGINAL, filtro del ruido de
> libsignal. `cli/vincular.ts` es proceso APARTE (vincular desde el bot dejaba la sesión
> en 440); marcador de enlace = `me`, no `registered`. Baileys pineado en 6.7.23 (la
> versión probada en producción); es la dep #6 del molde y con diferencia la más pesada.
> **Falta de S5:** el `MANUAL.md` + launchd del cutover (P6), el gate de corte de 5
> condiciones y **la primera conexión real a WhatsApp** (todo lo de canal está probado
> contra un WhatsApp simulado; nunca se ha vinculado un número de verdad — conviene hacerlo
> con un número secundario, no con el que vende).
>
> **Hecho el 25-jul (además del adaptador):**
> - **P5 · el migrador ya no pierde tus preguntas** (commit `86615eb`). El plan pedía que la
>   corrida final trajera las dudas pendientes de `dudas.js` y `espejo.ts` no abría ese
>   archivo: 8 decisiones tuyas en pausa se habrían perdido en el corte. `dudas.jsonl` es un
>   LOG PLEGABLE (alta + líneas de respuesta con el mismo id), así que se pliega por id antes
>   de mirar nada; ningún campo del schema lleva `.default()` porque un default rellena la
>   clave ausente y al plegar borraría las opciones del alta. Solo cruzan las PENDIENTES.
>   Se avisa dentro de cada una que contestarla **no** dispara el envío que allá disparaba
>   (`/api/cotizar` no existe acá). `migrar-huerfanos.jsonl` ganó `clase`: `no-corresponde`
>   (ruido esperado) vs `falta-dato` (trabajo real) — mezclados, 2 problemas dentro de 8
>   líneas se veían como 8.
> - **P3 · la compuerta** (commit `6de0907`). Debounce con presencia real, handoff al dueño
>   (30 min por un toque, indefinido si insiste 3 veces), **topes contados desde la base**
>   —la deuda D5: en el vivo cada reinicio de launchd regalaba cupo y el tope era una
>   lotería—, horario que cruza la medianoche, interruptor general del bot y aviso al topar
>   (el vivo se quedaba mudo sin avisar). Nace la tabla `pausas` y `conversaciones.asignado`
>   deja de ser una columna que nadie leía.
>   Destapó dos huecos que quedaron cerrados: el adaptador de P1 descartaba **todos** los
>   mensajes propios (el core nunca habría visto al dueño entrar al chat), y un takeover
>   indefinido sin endpoint de devolución dejaba el chat mudo para siempre.
>   **Cambio estructural:** `atenderMensaje` agenda y vuelve; el turno corre dentro del
>   agendador, serializado por chat. Lo que el cerebro aún no vio se acumula, así que la
>   foto que llegó antes de "mira esto" no se pierde con el turno cancelado.
>
> **⚠️ Si vas a trabajar el backend en varias sesiones a la vez: lee primero
> `REPARTO-SESIONES.md`** (mapa de las 16 piezas pendientes P1-P16, qué archivo puente toca
> cada una, qué combinaciones se pisan y el tablero de piezas tomadas). El reparto es por
> ARCHIVOS, no por tema: dos sesiones sobre `escritor.ts` o `index.ts` se borran entre sí.
> Nota de calendario: el plan rector fecha S5 en 25-31 ago y el código ya va en S5 el 25-jul
> — vamos ~4 semanas adelantados respecto al documento.
Investigación completa (8 rondas, ~70 agentes + 2 deep research externos arbitrados) +
DISEÑO CONGELADO (prototipo v5, 18 iteraciones con Alejandro:
`dixdybot-prototipo-v5-congelado.html`, artifact 555843ca) + **molde vivo en
`SaSS/DIXDY/dixdybot/`** (12 módulos, 474 tests verdes, tsc limpio) + **instancia de
destaperapido en `SaSS/destaperapido/dixdybot-data/`** (184 conversaciones, 3.820 mensajes,
20 pedidos migrados; panel en `127.0.0.1:8793`).

**Hecho:** S1 shim del cerebro (el bot vivo ya consulta `llm.ts` del molde con doble red) ·
S2 módulos embudo+cotizador + migrador + panel real · S3-4 caminos v1, gimnasio
(personas/juez/sombra), la Duda junior→senior, el **orquestador del turno** (H-A atómica,
candado sin puerta de atrás) y las **vistas Caminos y Agentes** del panel con aprobación en
lote · **cierre de S4 (25-jul):** vista *Diseño* real (cero "En construcción" en el panel),
el **veredicto del candado visible ANTES de aprobar** (el mismo `verificarParaActivar` en el
panel, en el CLI `revisar-caminos.ts` y en la aprobación real) y la **sombra diaria** como
servicio, con gate por días de calendario. Dos agujeros graves tapados: el gate se pintaba
verde con el cerebro caído (la enlatada de emergencia puntuaba "mejora") y el lint de cifras
no miraba la plantilla que ve el cliente — ver `HALLAZGOS-25-JUL.md` §4.

**Próximo paso:** que Alejandro **apruebe en lote los 30 caminos destilados** (panel →
Caminos → borradores; informe en `caminos-veredicto.md`: 24 ✅ / 6 ⚠️ / 0 ❌ — **ojo:** el
"0 rechazados" NO significa que no se pisen entre ellos, ver `HALLAZGOS-25-JUL.md` §2 bis)
y luego **S5 cutover** (25-31 ago) — ver
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

## 2026-08-02 · LA IA MADRE quedó viva (commit 046f894 del maestro)

Alejandro pidió «un Claude Code con interfaz web» y ya existe: la vista «Lo que sabe tu
equipo» es ahora UNA IA global con memoria real (sesión panel:madre), mini-skills de
lectura (chats, tablero, tarifario, caminos, pendientes) con los pasos visibles, y manos
con red (caminos en borrador, mensajes con tarjeta de aprobación). El carril por chat
usa el mismo loop. Probada en vivo con datos reales. Detalle: memoria ia-madre-panel.
