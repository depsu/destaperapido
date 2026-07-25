# Hallazgos del 25-jul-2026 — revisión propia de los datos migrados

Revisión hecha a mano sobre la instancia de destaperapido (`dixdybot-data/bot.db`, 20 pedidos)
y la bitácora del bot vivo, contrastando lo que el panel MUESTRA contra lo que los datos DICEN.
No salió de ningún agente: salió de mirar los números uno por uno.

---

## 1. El titular del panel esconde plata (≈$390.000, un 16%)

El panel abre con **"$2.370.001 en juego (20 pedidos abiertos)"**. Ese número está mal por dos
motivos distintos:

**a) Un trabajo de $270.000 que vale $0 en el titular.**
German Sánchez (Fluintek Ltda., Colina) está en *por entregar*: $170.000 el baño + $100.000 la
ducha portátil. En la base su monto está **vacío**. ¿Por qué? Porque ese pedido entró por un
mensaje de **confirmación**, y el migrador solo levanta el precio de los registros de tipo
*cotización*. Un pedido que se cerró sin pasar por cotización formal queda sin monto.
→ Es un hueco real del molde, no un dato malo del cliente.

**b) Un trabajo de $120.000 anotado como $1.**
Oscar Pontigo (Vitanova Constructora, San Bernardo) — la limpieza de dos estanques del 20-jul.
El registro del bot vivo dice literalmente `"precio": 1`. El migrador copió fiel ese 1.
Es el ".001" que se ve al final del titular.

La causa está **documentada y ya arreglada en el bot vivo** (`src/dashboard.mjs`, comentario
sobre la línea 1200): el formulario de cotización exigía que el precio del baño fuera mayor a
cero, así que para cotizar una limpieza sola había que poner **$1 en el baño** y el valor real
en *Extras*. Esa validación ya se corrigió — hoy acepta precio 0 si hay extras. Fue **1 caso de
23 cotizaciones**, del 20-jul, y no puede repetirse.

Lo que queda es que **la migración arrastró el registro viejo**: el espejo toma `detalle.precio`
y no mira los extras, así que se trajo el $1 y dejó afuera los $120.000. Es decir, el bug es del
molde nuevo, no del bot viejo.

**Qué NO hay que hacer:** rellenar el monto adivinando. En un pedido el `precio_clp` de la ficha
es el valor por unidad y en otro es el total (p. ej. hay uno de $255.000 que son 3 × $85.000).
Adivinar cambiaría un número faltante por un número falso, que es peor.

**Qué hacer:** que el panel diga la verdad — el total **más** "2 sin monto por confirmar", y que
un monto absurdamente bajo respecto al tarifario (como el $1) levante una duda al dueño en vez de
entrar callado. El umbral, administrable desde el panel como todo lo demás.

---

## 2. Los 30 caminos vienen sanos, pero mal ordenados

Revisión estructural, uno por uno:

- **30 de 30 traen pruebas doradas.** Ninguno va a caer por falta de pruebas.
- **0 de 30 llevan una cifra escrita a mano** en sus pasos. Ninguno va a caer por el lint de
  precios. Los precios se piden al tarifario, como debe ser.

Pero el destilador inventó los nombres de grupo sobre la marcha: **17 grupos para 30 caminos**,
con duplicados evidentes — `precio` y `precios`, `cotizacion` y `cotizacion-formal`, `estilo` y
`estilo_conversacion` y `conversacion`. Alejandro tendría que revisar 30 reglas repartidas en 17
cajones, casi todos de una o dos. La cascada del panel pierde su gracia.

Y hay **solape de contenido**, no solo de nombre. Tres caminos dicen casi lo mismo:

- *"Con el kit completo: precio de tabla al tiro…"*
- *"El precio sale exacto del tarifario y se dice neto"*
- *"Kit completo (comuna, cantidad, plazo) → valor de tabla al tiro y en neto"*

Los tres se disparan con "ya están comuna, cantidad y tiempo". Es **una** regla escrita tres veces,
heredada de tres reglas viejas distintas. Importa porque el bot solo carga 3-5 caminos por turno:
si tres cupos se gastan en la misma instrucción, desplazan a otras que sí hacían falta.

**Qué hacer:** fusionarlos en uno (sumando sus disparadores y sus pruebas), no descartarlos —
perder la regla sería peor que tenerla repetida. Y que la lista de grupos sea cerrada y
administrable, para que el destilador no vuelva a inventar cajones.

---

## 2 bis. El "0 rechazados" del candado promete más de lo que cumple

El informe automático dice **"30 de 30 se pueden aprobar hoy · 0 necesita un arreglo"**. Es cierto,
pero significa mucho menos de lo que suena, y esto hay que decirlo antes de que se apruebe nada.

El candado revisa tres cosas: que no haya cifras escritas a mano, que existan las pruebas, y que
no haya **conflictos**. Fui a ver qué considera "conflicto" y son exactamente tres casos, todos
**relaciones declaradas a mano** en el propio camino: que otro camino lo desplace por prioridad,
que dependa de uno que no está activo, o que quedó aplicado.

Después conté: **0 de los 30 caminos declara ninguna relación.** Es decir, la revisión de
conflictos no tenía nada que mirar. El "0 rechazados" estaba garantizado antes de correr.

Mientras tanto, midiendo el parecido de los disparadores, hay **13 pares de caminos que se
disparan con lo mismo** en más de un 45%, y el más alto (56%) es justamente el par que ya había
detectado leyendo: *cotizar-kit-completo* y *precio-exacto-neto*.

Y hay un segundo matiz que el informe declara con honestidad: la exigencia a las pruebas está en
modo **"declarada"** — se revisa que el ejemplo esté completo, pero **nadie lo jugó todavía contra
el bot**. Con el modo exigente activado, ninguno de los 30 se activa hasta que el gimnasio apruebe.

**Traducción:** los 30 se pueden aprobar sin miedo a que inventen precios (eso sí está blindado y
lo probaron saboteando cuatro caminos a propósito). Lo que NO está cubierto es que se pisen entre
ellos. Eso hoy lo tiene que ver un humano — o le enseñamos al candado a detectar solape de
disparadores, que es lo que corresponde.

---

## 3. Los "8 huérfanos" de la migración eran 2

El archivo `migrar-huerfanos.jsonl` asusta con 8 líneas, pero **6 no son huérfanos**: son mensajes
de seguimiento y de confirmación, que por definición no son pedidos. Solo 2 son de verdad: los dos
pedidos del punto 1. El archivo mezcla "esto nunca fue un pedido" con "a este pedido le falta un
dato", y eso hace que parezca un problema cuatro veces más grande de lo que es.

---

## 4. Dos agujeros que sí eran graves (encontrados en la revisión adversarial, ya tapados)

Estos dos NO salieron de mirar datos: salieron de un agente al que se le pidió romper lo
construido. Los verifiqué a mano antes de darlos por buenos.

**a) El semáforo del cambio se ponía VERDE justo cuando el cerebro nuevo estaba MUERTO.**

Todas las madrugadas el bot nuevo responde en sombra las conversaciones reales del día y se
compara con lo que contestó el bot que vende hoy. Cinco días buenos seguidos = luz verde para
que el bot nuevo tome el teléfono. El problema: si el cerebro no está disponible (se acabó el
límite de la suscripción a las 04:00, se cayó, no está instalado), el sistema responde una
enlatada — *"Dame un momento, ya te confirmo."* — y la comparación **la contaba como si el bot
hubiera contestado**. Peor: frente a un bot vivo que soltó un precio, la enlatada caía en la
regla *"el nuevo no cotizó donde el vivo sí"* y puntuaba **mejora**. Cinco noches con el cerebro
caído = "5 de 5, listo para el cambio" con el motor nuevo inexistente.

Lo peligroso no es la caída total (esa se notaría), sino la **parcial**: 3 de 12 conversaciones
que degradan por saturación inflan el puntaje en silencio.

Arreglado: una respuesta que salió de la enlatada se marca aparte, cuenta como *distinto* y
**bloquea el día**. El tope de degradadas es un ajuste del panel, en 0 por defecto.

**b) El candado de precios miraba la instrucción, no lo que llega al cliente.**

Un camino tiene dos textos: la instrucción que lee el cerebro y la **plantilla**, que es
literalmente el mensaje que recibe el cliente. El lint de cifras —la única defensa contra
precios inventados— miraba solo la instrucción. Un camino con la instrucción impecable y la
plantilla *"El destape sale $85.000"* pasaba con luz verde y quedaba activo.

Hoy no estaba explotado (los 30 borradores reales tienen 0 cifras en plantillas), pero era la
puerta abierta. **Lo probé yo mismo** después del arreglo, con tres caminos: precio solo en la
plantilla → frenado; precio en la instrucción → frenado; con el campo `{precio}` → pasa limpio.

---

## Estado del bot vivo al momento de esta revisión

Sano. Latido `conexion-sana`, el proceso que reporta es el mismo que tiene cargado su servicio.
El panel nuevo del dueño quedó como servicio del Mac y revive solo (probado matándolo).
