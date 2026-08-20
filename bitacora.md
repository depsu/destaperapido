# Bitácora de destaperapido

Relato en simple de lo que las rondas y sesiones de la IA hacen por este cliente
(lo nuevo ARRIBA). Las propuestas accionables viven en la cola del dashboard (🎯 Tareas);
aquí queda la historia. La escriben ronda-ads, ronda-correo y las sesiones.

---

## 2026-08-20 · 🚨 sesión · El WhatsApp de fosas y destapes parece no existir como cuenta

Revisando las 100 grabaciones de Clarity del 19 de agosto (se descartaron 33 de
limpiafosasydestape y 16 de baños químicos: quedaron **51 sesiones de destapes y fosas**)
apareció algo más grande que las grabaciones.

- **Lo que muestran las grabaciones del 19:** de las **9 visitas que llegaron por Google Ads**,
  **6 no tocaron nada** y varias duraron 4 a 8 segundos. Solo 3 hicieron algún clic. En el
  total de las 51, **el 66% no hizo ni un clic** y 38 vieron una sola página.
- **La pista que lo cambia todo:** el enlace de WhatsApp de baños químicos
  (`wa.me/56936470112`) devuelve **«Business Account»** y el nombre del negocio,
  **«Limpia Fosas y Destape»**. El de fosas y destapes (`wa.me/56965889226`) devuelve
  **exactamente la misma respuesta que un número inventado**: descripción genérica de
  WhatsApp, sin nombre de cuenta.
- **Ese número está en las 7 landings de los anuncios de fosas y destape y en 421 enlaces del
  sitio.** Y no aparece en ninguna configuración del sistema —ni bot, ni correo, ni canales—:
  solo como texto en las páginas.
- **Encaja con todo:** en agosto Google Ads contó **58 clics de WhatsApp** de fosas y destape
  (6 el 19) y el dueño dice que no le llegó ninguno. **El clic se cuenta en el sitio, ANTES de
  que WhatsApp abra.** Si al abrir sale «este número no está en WhatsApp», la conversión queda
  registrada igual y el cliente nunca escribe.
- **Lo que falta y es tuyo, Alejandro (10 segundos):** abrir `https://wa.me/56965889226` en un
  teléfono con WhatsApp. Si dice que el número no está en WhatsApp, está confirmado. Hay que
  decirlo honesto: una cuenta personal (no Business) tampoco muestra nombre en esa
  comprobación, así que la prueba del teléfono es la que zanja.
- **Mientras tanto**, cada peso de Ads que compra un clic de WhatsApp de destape se está
  perdiendo. Encolado como `critico-destaperapido-whatsapp-6588-9226`.

---

## 2026-08-20 · 💬 sesión · Ahora el WhatsApp llega diciendo qué necesita el cliente

- **Lo que pasaba:** de los 560 botones de WhatsApp del sitio, **344 abrían el chat en blanco
  o con un «Hola, necesito ayuda»**. Quien atiende recibía un mensaje que no dice nada: ni de
  qué comuna, ni qué servicio, ni si venía de un anuncio pagado o de un artículo del blog.
- **Por qué importa más de lo que parece:** la línea de destapes **no tiene bot** y Analytics
  **no está midiendo los contactos**. Ese texto es hoy lo único que identifica de dónde viene
  cada cliente.
- **Lo que se hizo:** cada página abre ahora el chat con su propio mensaje. Las de comuna dicen
  la comuna («necesito limpieza de fosa séptica en Melipilla», «necesito un destape en Ñuñoa»),
  las de servicio dicen el servicio, y los 30 artículos del blog dicen el problema del que
  hablan («tengo raíces en las cañerías», «tengo el baño inundado»). **344 enlaces en 87
  páginas.** Quedan **cero** en blanco y **cero** genéricos.
- **Los números quedaron auditados** contra la regla de Alejandro: todo lo de fosas y destapes
  al **+56 9 6588 9226** (421 enlaces) y baños químicos junto con la portada al
  **+56 9 3647 0112** (139). Ninguna de las 120 páginas mezcla números.
- **Un detalle honesto:** como la portada va a la línea de baños químicos por decisión tuya,
  su botón ahora dice «necesito un destape o limpieza de fosa» y ese mensaje llega al bot de
  baños. Es mejor que el «necesito ayuda» de antes —al menos se sabe qué pide— pero conviene
  que el bot sepa derivarlo.
- **Comprobado:** el cambio se midió con `auditar-web.mjs` **antes y después** sobre la misma
  página: 79 fallas en los dos casos, o sea no se rompió nada. Esas 79 son deuda vieja del
  sitio (botones chicos para el dedo y un contraste flojo) y quedaron encoladas aparte.

---

## 2026-08-20 · 🔌 sesión · Fosas y destape estuvo sin publicidad 15 de los últimos 50 días

Mirando **solo fosas y destape** (sin baños químicos, que es otro negocio y tapa el problema
cuando se suman):

- **Las campañas se apagan en bloques.** Cero apariciones y cero gasto el 1-3 de julio, el
  10-15 de julio, el 4-5 de agosto y el **13-16 de agosto**. En total **15 días de 50: casi un
  tercio del tiempo sin publicidad**.
- **No fue una falla ni un problema de pago.** El historial de la cuenta muestra que las pausó
  y las devolvió a mano la cuenta de Alejandro: pausadas el **12 de agosto a las 22:55** y
  reactivadas el **17 a las 09:31**. La campaña de baños químicos siguió corriendo esos mismos
  días con toda normalidad.
- **Esto es lo que hay detrás del «no me llega nadie».** Cuando las campañas corren, el negocio
  recibe **unos 7 contactos al día** (93 contactos en los 13 días activos de agosto: 32
  llamadas y 58 mensajes de WhatsApp). Cuando están apagadas, recibe cero de publicidad.
- **El 19 en particular:** las campañas ya estaban de vuelta y trajeron **6 contactos**, todos
  por WhatsApp y **ninguna llamada**. Ese día no es raro por sí solo — más de la mitad de los
  días del mes no entra ni una llamada telefónica.
- **Corrección de la entrada de ayer:** ahí dije que en el bache del 14-16 «el negocio no
  perdió nada» porque hubo 5, 6 y 5 contactos. Esos contactos eran **de baños químicos**. Por
  el lado de fosas y destape esos días fueron cero, porque las campañas estaban apagadas.
- **Queda para Alejandro** (`ads-destaperapido-apagones-fosas-destape`): decir si los apagones
  son a propósito. Si son para controlar el gasto, conviene **bajar el tope diario** en vez de
  apagar y prender, porque cada encendido reinicia el aprendizaje de Google. Tocar presupuesto
  es plata: no se aplica nada sin su OK.

---

## 2026-08-20 · 🔎 sesión · «No recibí ningún llamado el 19»: llegaron 8 clientes nuevos, pero ninguno llamó por teléfono

- **Lo que sí pasó el 19 de agosto:** fue uno de los mejores días del mes. **32 visitas desde
  Google** (1.563 apariciones, el récord de agosto), **31 clics de los anuncios** con 29.700
  pesos gastados, y en el WhatsApp entraron **8 conversaciones nuevas** que abrieron
  **9 cotizaciones**. De día muerto, nada.
- **Lo que es verdad:** ese día **nadie apretó el botón de llamar**. Cero, en las tres
  campañas. Pero eso no es una falla nueva: también fue cero el 13, el 14 y el 16 de agosto.
  El botón de llamar se usa entre 0 y 8 veces al día, mientras el de WhatsApp se usa
  **13 a 17 veces todos los días**. En simple: **este negocio ya no recibe llamadas, recibe
  mensajes.**
- **Dónde fue a parar cada contacto del 19:** los **8 de baños químicos** entraron al número
  que atiende el bot y quedaron atendidos con cotización abierta. Los **6 de destape** que
  vinieron de los anuncios se fueron al otro número (el 6588 9226), que no tiene bot: los
  atiende una persona. Si el reclamo viene de ese lado, ahí hay que mirar.
- **Hallazgo 1 — el panel le está mintiendo.** Google Analytics **no está midiendo ni un solo
  contacto**: en toda la semana solo registró visitas y scroll, ningún clic a WhatsApp ni a
  llamar. Por eso el panel muestra **0 contactos en 28 días** con 2.130 visitas. Google Ads sí
  los mide (por eso sabemos los números de arriba), pero esa medición vive solo dentro del
  GTM y no llega a Analytics. **Si el cliente mira su panel, ve un cero y concluye que no
  llegó nada.** Encolado como `tracking-destaperapido-ga4-sin-leads`. Ojo: para arreglarlo por
  programa falta habilitar la API de Tag Manager en la consola de Google — un clic de Alejandro.
- **Hallazgo 2 — la portada manda los destapes al bot de baños.** 111 páginas del sitio llevan
  al número de destapes y 10 al de baños químicos: las 8 de baños (correcto) **más la portada
  y la página de contacto**, desde un cambio hecho a mano el 11 de agosto. Quien busca
  «destape», entra por la portada y escribe, le está escribiendo al bot de baños. El 19 no se
  coló ninguno, así que por ahora es una gotera y no una inundación. Como el cambio fue
  deliberado, no se revierte solo: queda como decisión en
  `decision-destaperapido-numero-portada`.

---

## 2026-08-19 · 🚨 sensor + sesión · La caída de Google fue un bache de tres días y ya se arregló sola

- **Qué avisó el panel:** el 15 de agosto llegaron 12 visitas desde Google cuando lo normal
  son unas 28. El cliente quedó en rojo.
- **Qué pasó de verdad:** fueron **tres días malos seguidos y nada más** — viernes 14, sábado
  15 (feriado) y domingo 16: 12, 12 y 16 visitas. El **lunes 17 volvió con 34**, el mejor día
  en dos semanas, y el martes 18 con 21. El puesto promedio en Google también volvió a su
  lugar (había pasado de 5,7 a 7,0 y ya está en 5,8).
- **No fue culpa del sitio.** La web responde en menos de un segundo, no tiene ningún bloqueo
  para Google, el mapa del sitio está bien y **esos días no se publicó ni un cambio en la web**
  (lo del 14 fueron papeles internos, no páginas).
- **La prueba que lo cierra:** Google siguió **mostrando** el sitio exactamente igual (unas
  1.050 apariciones al día, sin caer). Lo que bajó fue cuánta gente hizo clic. Y el sitio
  hermano **limpiafosasydestape.cl** —otro dominio, otro servidor— cayó **los mismos tres días**
  y se recuperó el mismo lunes. Dos sitios distintos cayendo el mismo día = fue el buscador
  (fin de semana largo con el feriado del 15 y un reacomodo pasajero de los resultados), no
  nosotros.
- **Los contactos de esos días** fueron 5, 6 y 5, contra 1 y 2 del 12 y 13. ⚠️ **Corrección
  del 20-ago:** esos contactos eran de **baños químicos**. Las campañas de **fosas y destape
  estuvieron apagadas del 13 al 16**, así que por ese lado el negocio sí perdió esos días
  (ver la entrada del 20-ago). El mes orgánico sigue creciendo:
  **803 visitas en 28 días contra 695 del período anterior (+16%)**.
- **Qué se hizo:** nada en la web, a propósito. Cambiar títulos por un bache de fin de semana
  es justo lo que arruina lo que ya funciona. Quedó encolado en la cola única
  (`mejora-sensor-trafico-episodio-y-red`) el arreglo del sensor, con dos cosas: que este mismo bache hizo sonar la alarma **dos veces** (el 17 por el día
  14 y el 18 por el día 15), y que cuando **dos clientes caen el mismo día** corresponde un
  solo aviso «esto fue Google», no una emergencia por cliente.
- **Lo único que sigue esperando es tuyo:** los tres precios que se contradicen entre páginas
  (WC, alcantarillado y fosa séptica). Sigue en la cola desde el 21 de julio.

---

## 2026-08-19 · 🔎 investigación · La «caída de tráfico» era un sábado — pero Google sí movió el ranking

- **La alarma:** el sensor marcó rojo por los **12 clics del 15-ago** contra un promedio de ~27/día.
  El 15 de agosto de 2026 fue **sábado y feriado en Chile** (Asunción), y en este sitio los findes
  rinden la mitad que un lunes (sáb 8-ago: 23, dom 9-ago: 24, lunes 10-ago: 40). Esa parte era ruido.
- **Lo que SÍ pasó, y no era el sitio:** desde el **12-ago** la posición media empeoró de **5,7 a 7,0**,
  y con ella el CTR. Pero las **impresiones no cayeron: subieron** (1.048 el 15-ago; 1.559 el 17-ago,
  récord). O sea Google no dejó de mostrar el sitio: lo bajó un escalón.
- **La prueba de que es Google y no nosotros:** los **cuatro** sitios de la red pierden posición el
  MISMO día 12-ago — destaperapido 5,9→6,8, destapando 8,0→12,3, limpiafosasydestape 6,6→8,0,
  asvrgruas 12,0→14,7. Un cambio nuestro no puede mover cuatro dominios distintos a la vez.
- **Ya está rebotando:** el lunes **17-ago volvió a 34 clics** con posición 6,3. La caída duró el fin
  de semana largo del ajuste.
- **Falsa alarma de la página de fosas:** `/servicios/limpieza-fosas-septicas` figura cayendo de la
  posición 13,6 a la 33,0, pero es un espejismo: empezó a **aparecer en búsquedas nuevas y muy
  competidas** («limpia fosas», «limpia fosas copiapó») donde va en el puesto 60-80, y eso arrastra el
  promedio. En sus búsquedas de siempre subió, y de hecho **ganó un clic**.
- **Revisión técnica:** las 4 páginas de más tráfico responden 200, sin `noindex`, con el canonical
  correcto. Nada roto.
- **Lo que se arregló (en el maestro):** `scripts/sensor-trafico.py` comparaba un día suelto contra el
  promedio de todos los días revueltos, así que **gritaba casi cada fin de semana**. Ahora compara
  sábado con sábado y día hábil con día hábil (28 días de muestra), y mira las impresiones: si Google
  sigue mostrando el sitio igual, exige un desplome mucho mayor para hablar y avisa que el problema es
  de CTR/posición, no de visibilidad. Probado contra los días reales del 14 y 15-ago (ya no grita por
  el sábado) y contra tres casos de avería de verdad (desindexación, cero impresiones, pérdida de top):
  esos siguen alertando.
- **Para ti, Alejandro (encolado):** lo único que hoy frena los clics de verdad es que el sitio da
  **tres precios distintos** al mismo servicio, y por eso no se puede poner el número en Google. Van
  **29 días** esperando esa definición.

---

## 2026-08-19 · 📣 ronda-ads · baños químicos manda; «03 Urbano» se dio vuelta

- La cuenta completa: **85 contactos a 1.814 pesos**. Baños químicos es el mejor negocio de toda la red:
  **1.002 el contacto**, y aun así se queda fuera de la mitad de las búsquedas por el tope diario.
- **«03 Urbano» retrocedió**: de casi respetar su techo (+2,3%) a **+39%** (4.858 contra 3.500). No es la
  plata: pierde 4 de cada 10 apariciones porque el anuncio no gana la subasta.
- Sigue pagando por gente que busca la **máquina** (hidrojet, camión) y no el servicio: negativas listas
  para aplicar en la cola, en modo prueba.
- La gente pregunta el precio del baño químico ~30 veces por semana y no hay página que le responda.

## 2026-08-16 · 👷 constructor · La página de precios de fosas está primera en Google y nadie hace clic: falta el número

- **Lo que pasa:** el artículo «cuánto cuesta limpiar una fosa séptica» aparece **2.709 veces
  al mes** y va en el puesto 3,7 — muy arriba. Pero de cada 100 personas que lo ven, solo
  **3,4 entran**. Y hay algo más llamativo: en varias búsquedas está **primero de todos**
  («camión limpia fosas valor», «cuál es el valor») y se lleva **cero clics**.
- **Por qué:** la gente que escribe eso quiere ver **un precio en pesos** en el resultado de
  Google. El nuestro no muestra ninguno.
- **Por qué no se lo pusimos:** porque el sitio tiene **tres precios distintos** para el mismo
  servicio y el mismo tamaño de fosa — la tabla de precios dice *desde $150.000*, la página
  del servicio dice *desde $90.000* y este artículo dice *desde $80.000*. Poner cualquiera de
  los tres en Google sería prometer algo que otra página nuestra desmiente.
- **Lo que hace falta (y es tuyo, Alejandro):** decir **cuál es el precio de verdad**. Con eso
  se unifican las tres páginas y recién ahí el número puede salir en Google. Está esperando
  desde el **21 de julio, 26 días**.
- **Lo que NO se hizo, a propósito:** cambiarle el titular otra vez. Ya se probaron **tres
  versiones en 26 días** y el resultado no se movió ni una décima (3,92% → 3,37% → 3,36%).
  Insistir por ahí es gastar pasadas en algo que ya sabemos que no es el problema.
- **De paso, una duda que quedó cerrada:** una revisión anterior había dejado anotado que las
  «5 estrellas con 30 opiniones» que el sitio declara podían ser inventadas. **No lo son:**
  Google devuelve 5,0 con **40 opiniones** reales. O sea el sitio está declarando **menos** de
  las que tiene. No es un riesgo; a lo más, se está quedando corto.

---

## 2026-08-15 · 👷 constructor · El artículo del mal olor ahora promete la solución, no el índice

- **Lo que pasaba:** el artículo «olor a alcantarilla en casa» aparece **6.515 veces al mes**
  en Google en el puesto 5, pero solo **1 de cada 75** personas que lo ven hace clic (lo normal
  en ese puesto sería 1 de cada 25). El titular decía *«8 causas según dónde huele»*: describe
  el índice del artículo, no lo que la persona quiere, que es **que el olor se vaya**.
- **Lo que se hizo:** el titular pasó a *«Olor a alcantarilla en casa: 8 causas y cómo
  eliminarlo»* (el mismo que ya tenía el artículo por dentro) y el resumen ahora nombra los
  cuatro casos que la página resuelve de verdad: baño, cocina, patio y «solo de noche», más el
  «por qué vuelve a los pocos días». Ni una coma del contenido se tocó.
- **Honestidad de la pasada:** el cambio lo hizo la pasada de las 02:21 de esta madrugada, que
  **murió antes de dejarlo anotado** (octava vez que pasa, aunque esta vez del lado bueno: el
  trabajo sí estaba publicado). Esta pasada revisó de nuevo la página ya publicada —las 8
  causas están y cada una trae su solución—, avisó a los buscadores y escribió el registro.
- **Lo que hay que decir igual:** el registro del 8-ago pedía **no volver a tocar este titular**
  (van 5 versiones desde el 30-jul y ninguna movió la aguja). Revertir sería una sexta versión,
  así que se deja, pero **esta página queda congelada hasta el 29-ago**. Si para esa fecha los
  clics siguen planos, la lectura correcta es que el problema no es el titular: buena parte de
  esas 6.515 apariciones son búsquedas informativas («qué es el nonenal») que nunca iban a
  llamar a un destapador. Ahí conviene mover el esfuerzo a otra página.

---

## 2026-08-13 · 👷 constructor · Puente Alto salía en Google sin decir la palabra que la gente busca

- **Lo que pasaba:** la página de Puente Alto aparece 37 veces al mes cuando alguien busca
  «destape de alcantarillado puente alto», en el puesto 9… y en un mes se llevó **un solo
  clic**. El motivo, mirado de cerca, era tonto: el título que muestra Google decía «Destape
  de Cañerías en Puente Alto». La palabra **alcantarillado** estaba en el titular de la
  página, en las preguntas frecuentes y en el texto — en todos lados menos en la vitrina.
- **Lo que se hizo:** título y descripción nuevos con la palabra que la gente escribe, sin
  perder «cañerías» ni el 24/7, y nombrando los sectores que la página ya atiende (Bajos de
  Mena, Andes Cordillera, Eyzaguirre, Las Vizcachas). No se inventó ningún dato: el «llegada
  45-75 min» lo declara la propia página. **Publicado y comprobado en vivo**, y avisado a
  los buscadores.
- **Por qué esta página y no otra:** las tres que la tarea nombraba primero ya estaban
  arregladas en pasadas de la semana pasada y todavía se están midiendo — retocar un título
  dos veces seguidas borra la medición. Y Puente Alto rinde poco para lo que es: Melipilla,
  una comuna cinco veces más chica, trae **16 clics al mes** porque su página sí aparece
  arriba.
- **Para ti (no se tocó):** el sitio responde **tres precios distintos** a la misma pregunta
  según por dónde entre el cliente — la página de precios dice alcantarillado desde $75.000,
  pero las preguntas frecuentes de 7 comunas dicen $60.000-$150.000 y WC desde $35.000
  (la oficial dice $45.000). Google puede mostrar cualquiera de los tres. Con que me digas
  los dos números reales (WC y alcantarillado), lo dejo parejo en todo el sitio de una vez.

## 2026-08-12 · 📣 ronda-ads · las tres campañas se quedaron sin techo de precio

- **Lo que hay que mirar:** las tres campañas activas están en «maximizar conversiones» **sin objetivo
  de costo**. La semana pasada registré 1.900 en baños químicos y 3.500 en urbano. O alguien los quitó,
  o mi lectura anterior estaba mal — hay que averiguar cuál de las dos. Sin techo de precio, Google
  compra el contacto al precio que sea, que es justo lo que se ve en «03 Urbano».
- La foto del cliente: **110 contactos a 2.303 pesos**. Pero adentro conviven lo mejor y lo peor de toda
  la red: **baños químicos a 872** el contacto y **«03 Urbano» a 4.723**.
- **«03 Urbano» es el punto flojo:** se lleva el 16% de la plata de la red y devuelve el 9,5% de los
  contactos, y es la única campaña que pierde fuerte por las dos causas a la vez (se le acaba el
  presupuesto **y** pierde subastas). Antes de tocar plata, toca higiene.
- **Baños químicos:** con el 10% de la plata hace el 31% de los contactos. Sigue pegado al techo los
  siete días. **Ya no te propongo subirlo** — me dijiste el 11 de agosto que no querías gastar más por
  conversión, así que queda como dato, no como propuesta.
- Encolé **8 negativas** de bricolaje para «03 Urbano» (cinta, manguera, máquina, hidrolavadora…):
  gente que quiere comprar la herramienta, no contratar el servicio. Nada aplicado.

## 2026-08-11 · 📣 ronda-ads · el mejor y el peor negocio de la red viven en la misma cuenta

- **Baños químicos sigue siendo el campeón**: 68 contactos a **864 CLP** cuando se le pide 1.900.
  Lleva siete días seguidos pegado a su tope y ya deja fuera al **52,8%** de sus búsquedas (era 50,2%).
  Con el 10% de la plata de toda la red trae el 30% de los contactos. Subirle el tope es plata: tú decides.
- **«03 Urbano» se soltó**: su contacto pasó de 3.957 a **5.301 CLP**, un 51% sobre el objetivo que ya tiene
  puesto. Como el techo de precio existe y no se cumple, lo que toca es mejorar anuncio y landing, no la puja.
- Los dos días sin gasto de «01 Rural» y «03 Urbano» **no fueron una caída**: las pausaste tú el 3-ago y las
  reactivaste el 6-ago. Queda anotado para que ninguna ronda lo lea como alarma.
- Casi te reporto que esas campañas habían perdido su objetivo de costo. Era un error mío de consulta
  (Google no devuelve ese dato cuando se pide junto con las fechas). Verificado de nuevo: los objetivos están.

## 2026-08-08 · 👷 constructor · el artículo del mal olor ahora responde la pregunta del baño

Hoy tocó el artículo de **mal olor a alcantarilla**, el más visto del blog: lo ven cerca de
5.800 personas al mes, pero solo 90 entran. Ya le habíamos cambiado el título cuatro veces
buscando que la gente pinchara, y los números dicen que no sirvió de nada: sigue igual de
bajo. Así que esta vez no tocamos el título.

Miramos qué escribe la gente en Google y apareció algo obvio que faltaba: **mucha gente
pregunta literalmente "por qué mi baño huele a alcantarilla"**, y para esas búsquedas el
artículo salía en la página 2 — o sea, casi nadie lo veía. El artículo explicaba las 8 causas,
pero ninguna parte respondía esa pregunta tal como la persona la hace.

Le agregamos una sección que va por partes del baño: si huele en la rejilla o la ducha, si
huele en el WC y peor al tirar la cadena, si huele en el lavamanos, o si huele parejo en todo
el baño. Cada caso lleva de la mano a la explicación que el artículo ya tenía. Nada inventado:
todo salía del mismo texto, solo estaba desordenado para quien llega con esa duda.

Publicado y comprobado en vivo. Si en dos semanas esas búsquedas suben de la página 2 pero el
resto no se mueve, la conclusión honesta es dejar este artículo tranquilo: la mayoría de sus
visitas son búsquedas sueltas que llegan de rebote, no gente buscando un servicio.

## 2026-08-08 · 📣 ronda-ads · la mejor y la peor campaña de la red están en la misma cuenta

- **Baños químicos** volvió a bajar su récord: **896 pesos por contacto** (objetivo 1.900), y
  trae el 29% de los contactos de toda la red gastando el 11% de la plata. Sigue con el tope
  más chico (8.000) y deja pasar casi la mitad de sus búsquedas por falta de presupuesto.
- **01 Rural** es la más cara de las seis: **6.461 por contacto**, y descubrimos que tampoco
  tiene objetivo de costo. Además se pelea las mismas búsquedas rurales con fullfosas.
- El 4 y 5 de agosto sus dos campañas de destape quedaron mudas (0 impresiones), sin explicación.
- Encolado: subir el tope de baños químicos y poner volante a Rural. Nada aplicado.

## 2026-08-02 · 👷 constructor · el artículo del pozo ahora se presenta antes de asustar

Hoy tocó el artículo del **pozo absorbente saturado**. Lo ven cerca de 1.900 personas al mes
y aparece sexto en Google, pero el titular que mostraba era puro problema: «Pozo Absorbente
Saturado: 7 Señales (y Por Qué Vaciarlo No Sirve)». El detalle es que mucha gente que busca
esto todavía **no sabe qué es un pozo absorbente** ni si es lo mismo que la fosa séptica —
y el artículo sí lo explica, en su primera sección, pero el titular nunca lo decía.

Así que el titular pasó a ser **«Pozo absorbente: qué es y 7 señales de que está saturado»**,
y el textito de abajo ahora promete las tres cosas que la página de verdad entrega: qué es,
en qué se diferencia de la fosa, y por qué vaciarlo da alivio solo por unas semanas. Nada de
eso es invento: cada promesa se fue a buscar al texto antes de publicar (las señales son 7,
contadas una por una, y lo de las semanas lo dice la propia página).

También se sacó del textito la promesa de «con costos», porque los precios todavía no
coinciden entre las páginas del sitio — ese es el tema que espera tu decisión desde el 21 de
julio. El contenido del artículo no se tocó: solo cómo se presenta en Google. Publicado y
comprobado en vivo, y avisado a los buscadores.

Detalle chico pero importante: el trabajo estaba a medio hacer en el computador, de una
pasada de la madrugada que se cortó antes de publicar. Se revisó de nuevo entero antes de
darle el visto bueno; ya van cinco veces que pasa lo mismo, así que ahora la regla es
publicar primero y anotar después.

---

## 2026-08-01 · 👷 constructor · el artículo de precios ahora muestra de qué se trata (y encontramos su techo)

Hoy tocaba el artículo **«Cuánto cuesta limpiar una fosa séptica»**. Sale tercero o cuarto en
Google, lo ven más de 2.200 personas al mes… y solo 3 de cada 100 hacen clic. Debería ser el
doble.

**Qué cambiamos.** El textito que Google muestra debajo del título prometía «rangos de precio»
pero no mostraba nada concreto — era una promesa vacía compitiendo contra otros resultados.
Ahora dice qué hay adentro de verdad: los cuatro tamaños de fosa que cubre el artículo, los tres
factores que suben el valor y la parte de cómo pedir la cotización para que no te cobren de más.
Todo eso ya estaba escrito en la página; solo faltaba decirlo afuera. Publicado y comprobado en
vivo.

**Dos tareas que decidimos NO hacer, y por qué.** La lista de pendientes traía dos «urgencias»
que resultaron falsas alarmas al mirar los números de verdad:

- **La portada.** El reporte decía que su titular rendía mal. No es cierto: la portada de verdad
  (la dirección con *www*) rinde **8,7%**, más del doble de lo esperado. Lo que baja el promedio
  son las otras dos versiones de la dirección (sin *www* y en *http*), que Google todavía cuenta
  aparte. El desvío ya está arreglado desde el 17 de julio y funciona — Google simplemente tarda
  unas semanas en juntarlas. Tocar el titular habría sido arreglar algo sano.
- **El artículo de olor a alcantarilla.** Su titular se cambió anteayer y todavía se está
  midiendo. Volver a moverlo ahora sería no dejar que el test termine.

**Lo importante: encontramos el techo de la página de precios.** Hay búsquedas donde tu sitio
sale **primero** y aun así nadie entra — cosas como «camión limpia fosas valor». Cuando alguien
busca un precio y estás primero pero no te hacen clic, casi siempre es porque el resultado no
muestra ningún número. Y no podemos ponerlo todavía: **el precio de limpiar una fosa de casa
aparece distinto en tres páginas tuyas** ($150.000 en la tabla de precios, $90.000 en la página
del servicio y desde $80.000 en el blog). Elegir cuál es el bueno es plata, así que es decisión
tuya — está esperando desde el 21 de julio. Te lo volvimos a avisar al celular. Mientras no se
unifique, esta página no puede subir más.

---

## 2026-07-31 · 👷 constructor · «huele a alcantarilla, pero solo de madrugada»: esa pregunta ya tiene respuesta

Ayer le cambiamos el gancho al artículo de **olor a alcantarilla** (el que más gente ve de tu
sitio). Hoy tocaba lo otro: el gancho ya se probó cuatro veces y siempre rinde parecido, así
que la palanca que queda no es el titular sino **el contenido**. Le sumamos dos cosas que la
gente pregunta de verdad y el artículo no respondía:

**1. Por qué el olor aparece de noche.** Mucha gente cuenta lo mismo: durante el día nada, y a
las tres de la mañana la casa huele a drenaje. No es que el problema aparezca de noche — es que
de noche se junta todo: pasan diez horas sin que corra agua (y los sifones terminan de secarse),
la casa está cerrada sin ventilación, y en el dormitorio uno huele mucho más. Le dejamos una
prueba casera de tres noches para que la persona misma sepa si es solo eso o si hay algo más
abajo — y si es algo más abajo, ahí sí aparece tu inspección con cámara.

**2. «¿Esto es alcantarilla o una fuga de gas?»** Es la duda que asusta, y nadie la responde.
Ahora se explica cómo distinguirlas (de dónde sale el olor y a qué huele cada una) y, si hay
cualquier duda, se le dice que lo trate como fuga de gas: no tocar interruptores, ventilar,
cortar la llave, salir y llamar desde afuera a Bomberos. Le decimos claramente cuándo **no** es
un problema tuyo. Eso no te quita trabajo: te da credibilidad con quien después sí te va a
llamar.

**Detalle de oficio:** el trabajo estaba a medio hacer en el computador desde ayer (la pasada se
cortó antes de guardar). No lo publicamos a ciegas: lo revisamos entero de nuevo y encontramos
que una de las dos preguntas estaba declarada para Google pero no se veía en la página. La
agregamos, y recién ahí lo publicamos. Verificado en la web en vivo, y avisado a Bing.

## 2026-07-30 · 👷 constructor · el artículo que más gente ve por fin cambia de gancho (y lo publicamos de verdad)

La página de **olor a alcantarilla** es la que más gente ve en Google de todo tu sitio: 5.001
veces apareció en el último mes. El problema es que de cada 100 personas que la ven, solo 1,6
entran — deberían entrar unas 4. Le habíamos cambiado el gancho tres veces con la misma
fórmula («8 causas y cómo eliminarlo») y las tres rindieron casi igual de mal: ya está probado
que por ahí no es.

Así que esta vez cambiamos **la promesa, no el número**: ahora dice «**8 causas según dónde
huele**». Es lo único que tu artículo tiene y ningún competidor ofrece — una tabla que te
manda directo a tu caso según si el olor está en el baño, la cocina, el patio o en toda la
casa. Además el resumen que sale en Google ahora menciona *por qué el olor vuelve a los pocos
días*, que es justo lo que la gente pregunta y nadie responde.

De paso arreglamos un hueco real: la causa 4 (una fisura en una cañería dentro del muro) te
decía cómo **encontrarla** pero nunca qué **hacer** después. Ahora también lo dice.

Dos cosas honestas: (1) el intento de anoche había quedado escrito pero **sin publicar** — se
cortó a mitad de camino; esta pasada lo revisó de nuevo y ahora sí está en vivo. (2) Si en una
semana el porcentaje sigue igual, dejamos de tocar el título de esta página: el problema estará
en la posición, no en el gancho.

## 2026-07-30 · 📣 ronda-ads · los baños son tu mejor negocio y llevan 7 días con la plata agotada

Un contacto de **baños químicos te cuesta 1.402 pesos**. El de destapes urbanos, 4.277; el de
fosas de tu socio, 6.020. Es **cuatro veces más barato** y esta semana se quedó sin plata **los
siete días** (tope 8.000, gastó entre 8.190 y 9.278 cada día). Por eso **la mitad de la gente
que busca baños químicos no te ve**.

Hay una salida sin gastar un peso más: mover parte del tope desde «03 Urbano», que esta semana
pasó de 2.534 a 4.277 pesos por contacto, hacia los baños. **Esa decisión es tuya, es plata.**

Lo bueno de la semana: las fosas rurales mejoraron (de 4.616 a 3.606 por contacto) y no se
quemó nada en búsquedas basura. Una duda para ti: **¿arriendas duchas portátiles o lavamanos?**
Hay gente buscándolo; si los tienes, es plata sobre la mesa.

## 2026-07-29 · 📣 ronda-ads · los baños siguen siendo tu mejor negocio, y siguen apretados

Un contacto de **baños químicos te cuesta 1.316 pesos**. Uno de destapes urbanos, 5.032. Es
casi cuatro veces más barato, y esta semana fue **el único frente que mejoró** mientras todo
lo de destapes se encarecía.

El problema es que a los baños se les acaba la plata todos los días: con tope de 8.000 diarios
se está gastando 8.648, y **la mitad de la gente que busca baños químicos no te ve** por eso.
Hay una salida sin gastar un peso más: mover parte del tope desde «03 Urbano» (que esta semana
duplicó su costo por contacto) hacia los baños. Esa decisión es tuya, es plata.

## 2026-07-26 · 👷 constructor · el post del líquido azul deja de hablar de «riesgos» y pasa a hablar como busca la gente

Trabajé la tarea t34: el artículo del líquido azul está en posición 5,8 con **912 apariciones
en Google y solo 6 clics**. Fui a mirar QUÉ escribe la gente para llegar ahí y el artículo
estaba contestando otra pregunta:

- «que es el liquido azul de los baños portatiles» — 63 apariciones, **posición 4, cero clics**
- «líquido azul **para** baños portátiles» — 57 apariciones
- y varias más con «para»: para baños, para baño portátil, para limpiar baños

Dos cosas: la gente dice **baños portátiles**, no «baños químicos», y pregunta **qué es y para
qué sirve**, no «qué riesgo tiene». El título decía «Qué tiene, mitos y riesgo real». Quedó:
**«Líquido azul para baños portátiles: qué es y qué tiene hoy»**.

Y le agregué arriba una guía chica de cuatro caminos («¿arriendas baños?, ¿lo quieres comprar?,
¿es para un motorhome?, ¿te preocupa si hace mal?») que manda a cada quien a la parte que le
sirve. Eso es lo que faltaba: el artículo entero estaba escrito desde el ángulo del susto y
la mitad de la gente llega buscando comprar o entender.

También le puse un enlace desde el post de «cuántos baños necesita un evento», que es fuerte,
y le saqué un «100% biodegradables» que estaba sin respaldo (ya no digo el número).

Publicado en la web. En 2-3 semanas se re-mide: la apuesta es que suba de esos 6 clics.

**Cierre (01:56).** Esta parte quedó a medias: el cambio estaba escrito en los archivos y
anotado acá, pero **nunca se subió** — la web seguía mostrando el título viejo. La pasada
siguiente lo revisó de nuevo (que nada de lo nuevo fuera inventado, que los enlaces internos
llegaran a alguna parte, teléfono correcto) y **ahora sí está publicado y verificado en la
web**. Aprendizaje para adentro: no anotar «publicado» hasta que la página en vivo lo muestre.

## 2026-07-26 · 📣 ronda-ads · tu mejor negocio es el que tiene menos plata

Tres cosas de esta semana:

**1) Baños químicos es tu joya y está apretada.** 40 contactos a **1.303 pesos cada uno** — el
más barato de tus seis frentes, casi 5 veces mejor que las grúas. Y es justo **la campaña con
menos presupuesto de todas** (8.000 al día, cuando destapando tiene 19.000). Por eso pierde
**más de la mitad de las búsquedas**: se le acaba la plata, no le falta calidad. Esta decisión
es tuya y está esperándote en el tablero.

**2) Destapes urbanos cambió de problema.** Antes le faltaba presupuesto; ahora le pesa más
quedar abajo en el resultado. Eso se puede mejorar gratis antes de pedirte plata.

**3) Tus negocios se están peleando entre ellos y esta semana empeoró.** El lado de las fosas
subió un 35% en un día: entre destaperapido y fullfosas van **70 mil pesos** pujando por las
mismas búsquedas. Ejemplo concreto: por «limpia fosas calera de tango», fullfosas pagó **8.663
por UN clic** y tú 1.395 por lo mismo. Es plata que se van entre ustedes.

## 2026-07-25 · 📣 ronda-ads · «baños químicos» es tu mejor negocio y está a media máquina

Los números: baños químicos trajo **40 contactos por 50 mil pesos (1.263 cada uno)** — el
más barato de todas tus campañas — y aun así **se queda fuera de la mitad de las búsquedas
por falta de presupuesto**. Es la propuesta más clara del mes: subir de 8.000 a 12.000 al día.
Eso es plata tuya, así que queda encolada esperando tu OK.

Lo otro, importante: tus propios negocios se están peleando las mismas búsquedas. Destapes
urbanos choca con destapando y Rural choca con fullfosas — juntos, unos **135 mil pesos por
semana** subiéndose el precio entre ellos. Necesita una decisión tuya de cómo repartir.

## 2026-07-24 · 👷 constructor · el post «por qué se tapa el desagüe de cocina» pasa a hablar de «lavaplatos» y le saco un dato inventado

Trabajé la tarea t33: el artículo `/blog/por-que-se-tapa-desague-cocina` está en posición 6,3
con 1.251 impresiones. En el disco había un cambio a medio hacer de una pasada anterior que
cambiaba el título a «¿Por qué se tapa el lavaplatos? 5 causas y cómo destaparlo» — un buen
cambio, porque la gente busca «lavaplatos», no «desagüe de la cocina», y el artículo de verdad
tiene 5 causas. **Pero no lo publiqué a ciegas:** ese borrador también prometía en Google que
«en el 50% de los casos el tapón está en el sifón», y ese número no lo respalda nada (el propio
artículo decía que estaba «medido en nuestra guía práctica», pero esa guía es otro artículo
nuestro que solo repite el mismo número sin fuente). Es el mismo problema del «90%» que sacamos
la semana pasada. Así que **corregí el título/meta buenos y saqué las cifras inventadas** (tanto
del texto como del resultado de Google), dejándolo en lenguaje honesto: «la mayoría de las veces
el tapón está justo en el sifón». También sumé un enlace desde la página de precios hacia este
artículo. Publicado. Anoté que el artículo hermano de «7 métodos» tiene el mismo número sin
fuente, para arreglarlo cuando le toque.

## 2026-07-24 · 👷 constructor · el post del pozo absorbente ahora explica «qué es» y «qué no debe llegarle» (rescate de trabajo huérfano)

**Qué pasó:** el constructor tomó UNA tarea de la cola y la terminó completa. Las de mayor
puntaje (los títulos con CTR bajo de la home y los blogs) todavía están «en observación»:
se reescribieron hace pocos días y Google aún no mide el cambio, así que re-tocarlas sería
dar vueltas en falso. Bajó entonces a la mejor tarea con la palanca libre: **subir en Google
el artículo del pozo absorbente saturado** (posición 5,8 con 1.288 impresiones al mes).

**Qué se hizo:** una pasada anterior (21-jul, interrumpida) había dejado este contenido
escrito en el disco pero sin revisar ni publicar. Esta pasada lo verificó frase por frase
contra lo que el propio artículo ya dice y lo publicó: una sección nueva **«Qué es un pozo
absorbente (y en qué se diferencia de la fosa)»** —con el recorrido del agua de la casa— y
**«Qué NO debería llegar nunca al pozo»** (aguas lluvias, riego del jardín y la grasa de una
fosa mal mantenida). Responde justo lo que la gente busca antes de llamar. No se inventó ni
un dato ni un precio; los títulos y el snippet quedaron intactos.

**Publicado** a `depsu/destaperapido` (push → Vercel). El resto del trabajo huérfano en el
disco (otro título de blog + dos enlaces) quedó intacto para las próximas pasadas.

---

## 2026-07-23 · 👷 constructor · el artículo estrella ahora responde «¿y por qué vuelve el olor?» (rescate de trabajo huérfano)

**Qué pasó:** una pasada anterior (21-jul, interrumpida) dejó trabajo hecho en el disco pero
sin verificar, sin registrar y sin publicar. Esta pasada tomó UNA de esas piezas — la del
artículo con más impresiones del sitio (t16, quick-win) — la verificó afirmación por
afirmación contra el contenido ya publicado (todas con respaldo textual) y la publicó:
sección nueva «¿Por qué vuelve el olor a los pocos días?» con 6 rutas síntoma→causa y un
enlace al post de pozo absorbente. El título NO se tocó (el test del 20-jul sigue midiendo).
**Por qué esta y no otra:** t1-t4 (score 29) están todas en ventana de verificación
(títulos reescritos 18-21 jul; el scout aún mide los viejos) — re-tocarlas sería churn.
**Ojo:** queda MÁS trabajo huérfano en el disco (título nuevo de por-que-se-tapa, contenido
de pozo-absorbente, 2 enlaces) — anotado en `nota_constructor` de t18/t19; cada pieza se
verificará y publicará en su propia pasada, no en bloque. Gates: Google ✓ + backlog ✓
(fila en cambios-seo.md). Publicado: commit quirúrgico + push (Vercel) bajo
«publicar-mejoras-seo» + ping IndexNow.

## 2026-07-23 · 📣 ronda-ads · las campañas rinden pero el presupuesto les queda chico

«Urbano» hizo 39 contactos a ~2.500 c/u y «baños químicos» 38 a ~1.200, pero **más de la
mitad de las búsquedas de Urbano quedan fuera por presupuesto** (55%). Subir presupuesto es
plata → la decisión está encolada en Tareas para ti. También sigue la nota de no negativar
preguntas «raras»: una («como se llama la persona que destapa cañerias») convirtió esta semana.


## 2026-07-20 · 👷 constructor · la portada ya está publicada (y una pregunta para ti)

**Qué pasó:** el cambio de la portada estaba hecho pero se había quedado **sin publicar** —
listo en el computador, invisible en internet. Lo revisé, pasó los controles y lo publiqué.
Ya está en línea.

**Qué dice ahora la portada en Google:** antes el título hablaba solo de «alcantarillado»,
pero cuando uno mira lo que la gente escribe de verdad para llegar a la portada, pide otras
cosas: destape de cañerías, de desagües, de baños, de WC. Varias de esas búsquedas nos ponen
entre los tres primeros y **nadie hace clic** — porque el título no les responde. Ahora dice
«Destape de Cañerías y Alcantarillado en Santiago · 24/7», que es lo que realmente hacemos.

También sacamos del texto de Google la promesa de «45 minutos»: la propia página, más abajo,
dice que llegamos «en menos de 90 minutos en zona urbana». Prometer 45 arriba y 90 abajo
decepciona al que llega. Lo de «garantía de 30 días» sí se mantuvo, porque está respaldado en
las páginas de preguntas frecuentes y de precios.

**Lo que necesito de ti (no lo toqué):** el letrero grande de la portada, el que ve la gente
al entrar, sigue diciendo **«Llegamos en 45 min»**. Eso es una promesa comercial tuya, no una
decisión mía. ¿El compromiso real es 45 minutos o 30 a 90? Me dices y lo dejo parejo en todo
el sitio.

---

## 2026-07-20 · 👷 constructor · le sacamos un «90%» que nos habíamos inventado

**Qué se hizo:** la tarea del día era el artículo del olor a alcantarilla — la página con más
apariciones en Google de todo el sitio (4.184 en un mes) pero pocos clics: aparece quinta y
solo 1 de cada 60 personas entra.

Antes de reescribir el título fui a mirar qué escribe la gente de verdad para llegar ahí. La
búsqueda que manda es **«olor a alcantarilla en casa»**, y nuestro título decía «en la Casa».
Chico, pero es la diferencia entre que Google vea que le respondes exacto o no. Además el
título estaba escrito Con Todas Las Palabras En Mayúscula, que es costumbre del inglés: en
español se lee raro y Google a menudo lo reescribe por su cuenta. Ahora dice, simple:
**«Olor a alcantarilla en casa: 8 causas y cómo eliminarlo»**.

**Y algo más importante que el título:** el texto que sale en Google decía «90% de las veces
NO es la alcantarilla». Fui a buscar de dónde salía ese 90%… y no salía de ningún lado — ni
de las fuentes del artículo, ni de un dato nuestro. Era una precisión inventada, y llevaba
cinco días publicada en la cara del buscador. La saqué de ahí y del texto de arriba del
artículo. Ahora dice «casi siempre», que es lo que el artículo sí demuestra (el sifón seco
está explicado como la causa número 1). Perdemos un poco de gancho y ganamos algo que no se
negocia: no decimos números que no podemos respaldar.

**Lo que NO se tocó, a propósito:** el ángulo de «8 causas» se estrenó el 15 de julio y aún
está en medición. Cambiarlo de nuevo cinco días después haría imposible saber qué funcionó,
así que se mantuvo la promesa y solo se corrigió la forma. El H1 y el contenido quedaron
intactos.

**Estado:** publicado (ya se ve en vivo) y avisado a los buscadores por IndexNow. El detalle
técnico, con los dos gates de Google, está en `cambios-seo.md`.

**Cómo saber si funcionó:** en 1-2 semanas el CTR de esta página debería subir del 1,67%
actual hacia el ~4% que se espera para la posición 5.

---

## 2026-07-17 · 👷 constructor · la portada estaba viviendo en tres direcciones a la vez

**Qué se hizo:** la tarea de hoy decía «la portada está en el puesto 5,6 y le va mal en clics
(1,53%)». Antes de tocar el título fui a mirar el dato crudo en Google… y la tarea estaba
midiendo un fantasma.

Tu portada existe hoy en **tres direcciones distintas**: la buena
(`https://www.destaperapido.cl/`) y dos copias (`destaperapido.cl` sin *www*, y la misma en
*http*). El reporte las suma como si fueran una sola, y ahí nace el número feo. Separadas, la
foto real es otra:

- **La portada buena:** 261 apariciones y 20 clics → **7,7% de clics**, casi el DOBLE de lo
  esperado (~4%). No está mala: está bien.
- **Las dos copias:** 1.632 apariciones y 9 clics entre ambas → 0,55%. Son ellas las que
  hunden el promedio.

O sea: **el 86% de las veces que Google muestra tu portada, muestra una copia** — y la copia
casi no se clickea. Nadie tenía que arreglar el título; había que arreglar la duplicación.

**La causa (un detalle de una línea):** el sitio ya tenía la orden de mandar todo desde la
dirección sin *www* a la buena… pero esa orden **funcionaba en todas las páginas menos en la
portada**. Lo comprobé en vivo: `/precios-orientativos` y `/blog` saltan correctamente, la
raíz `/` no saltaba. Por eso la portada era la única página con copias sueltas dando vueltas
por Google. Agregué la regla que faltaba para la raíz.

**Por qué importa:** Google reparte la fuerza de tu portada entre tres direcciones en vez de
concentrarla en una. Al unirlas, esa fuerza se junta — y de paso el reporte deja de mentir,
así que las próximas tareas no van a perseguir el mismo fantasma (el título de la portada ya
se reescribió dos veces este mes persiguiéndolo: 08-jul y 14-jul).

**Ojo:** esto explica el número del CTR, no el puesto. La portada canónica está en el puesto
~10, y ese sigue siendo el trabajo de fondo pendiente.

**Publicado:** sí (commit + Vercel). Cambio de una línea, reversible.

---

## 2026-07-17 · 👷 constructor · el artículo más visto ahora se puede leer «por síntoma»

**Qué se hizo:** la página que más gente ve de todo el sitio es el artículo del mal olor a
alcantarilla (casi 4.000 apariciones en Google al mes, en el puesto ~5,7). Le faltaba algo
simple: **entrar por dónde te huele**. El artículo listaba las 8 causas ordenadas de la más
simple a la más compleja, que es el orden del técnico, no el de la persona que llega asustada
buscando «me huele a alcantarilla en el baño».

Ahora, apenas empieza el artículo, hay un cuadro «¿Dónde se siente el olor? Empieza por ahí»:
si te huele en un baño que no usas, en el dormitorio, en el patio, cuando llueve… cada caso
te lleva de un clic a su causa. **No se inventó nada:** cada fila sale de lo que el propio
artículo ya explicaba.

**Por qué se hizo así:** le pregunté a Google Search Console qué escribe exactamente la gente
que llega a esa página, y la mayoría describe *el lugar* («olor a alcantarilla en el baño»,
«olor a cloaca en el dormitorio», «olor a pozo en la casa») — casi todas con cero clics. El
artículo respondía esas dudas, pero no se notaba. De paso ayuda a otro problema conocido: solo
el 13% de la gente bajaba en la página.

**Lo que NO se tocó, a propósito:** el título y la descripción que salen en Google. Se
reescribieron hace dos días (15-jul) y hay que dejar pasar 2-3 semanas para saber si esa
apuesta funcionó. Cambiarlos otra vez ahora sería quedarse sin saber qué sirvió.

**Estado:** publicado y verificado en vivo · avisado a Bing/IndexNow · a re-medir desde el
~7 de agosto. Detalle técnico y gate de Google en `cambios-seo.md`.

---

## 2026-07-17 · 👷 constructor · pasada sin cambios publicados (y un hallazgo)

Las dos tareas de la cola que tocaban a este cliente (t1 y t2, las de mayor score) **ya
estaban hechas**: el título del post de mal olor se reescribió el 15-jul y el de la home el
14-jul. Google todavía no alcanza a mostrar si sirvieron (las tareas piden re-medir en 1-2
semanas), así que el constructor **no tocó nada**: reescribir de nuevo a los 2 días borraría
la medición. Se anotó en ambas tareas para que la próxima pasada no vuelva a intentarlo.

**El hallazgo:** buscando cómo subirle el CTR a la home apareció que el sitio se contradice
solo. La home dice en sus preguntas frecuentes (y en el código que lee Google) que un destape
de alcantarillado **parte en $45.000**, pero la página de precios dice que alcantarillado
**parte en $75.000** — los $45.000 son del destape de WC. Google está leyendo dos respuestas
distintas a la misma pregunta dentro del mismo sitio.

Eso importa porque la gente busca **precio** («destape de alcantarillado precio» es la
consulta que más tráfico trae) y la única página que muestra el precio en el título rinde
**9,09% de CTR** contra el **1,53%** de la home. Poner el precio en el título de la home es
la palanca obvia, pero mientras el dato no sea uno solo y verdadero, hacerlo sería prometer
un precio que no es. Se dejó anotado y se le preguntó a Alejandro cuál es el correcto:
con esa respuesta, la IA corrige el FAQ y el título en una pasada.

---

## 2026-07-15 — 👷 Constructor: título y meta del post de mal olor reescritos, 3er intento (publicado)

Tarea t1 de la cola (CTR-bajo, score 29; ganó el desempate por impresiones: 3.900):
`/blog/mal-olor-alcantarilla-casa-causas-soluciones`. Posición 5,8 pero CTR 1,51% (esperado
~4% en esa posición) — seguía bajo pese a los dos ajustes previos (07-jul y 08-jul), ambos
con el mismo gancho «Test de 3 Minutos + Solución» que no logró subir el CTR. Reescribí
título, meta description, og:title/og:description, twitter:title/twitter:description y el
headline/description del schema BlogPosting probando un ángulo distinto: número concreto en
vez del test — «Olor a Alcantarilla en la Casa: 8 Causas Reales (y Cuál Es la Tuya)» / «90%
de las veces NO es la alcantarilla: es un sifón seco o la ventilación tapada. Identifica tu
causa entre las 8 posibles con este test de 3 minutos y su solución.» Mismos datos que ya
están en el H1 (que ya decía «8 causas») y en el cuerpo del artículo (90% sifón/ventilación,
test de 3 min); no toqué H1 ni contenido (fuera del alcance de esta tarea puntual de CTR).
Gates: (1) Google ✓ — dato ya sustentado en el H1/cuerpo, sin keyword stuffing, sin datos
inventados; (2) backlog ✓ — fila en `cambios-seo.md`. Publicado: commit + `git push`
(Vercel-Git publica), bajo `publicar-mejoras-seo` (libre poder 2026-07-07). Verificación:
re-medir el CTR de esta página en 1-2 semanas (~29-jul); si sigue sin subir, el problema
puede no ser el título sino el snippet que Google arma solo (frecuente en posición >5).

## 2026-07-14 — 👷 Constructor: título y meta del post de cocina reescritos (publicado)

Tarea t3 de la cola (CTR-bajo, score 29): `/blog/por-que-se-tapa-desague-cocina`. Posición
6,7 pero CTR 0,32% (esperado ~4% en esa posición) con 945 impresiones — bajó respecto a la
pasada anterior pese al ajuste del 08-jul, señal de que ese título («Causas y solución») no
enganchó lo suficiente. Reescribí título, meta description, og:title/og:description,
twitter:title/twitter:description y el headline/description del schema BlogPosting: nuevo
título «¿Por qué se tapa el desagüe de la cocina? Causas y precio del arreglo» y meta que
suma el precio real («desde $55.000, sin romper cañerías ni usar químicos agresivos» — el
mismo dato que ya está en el cuerpo, enlazado a `/precios-orientativos`). No toqué H1 ni
contenido (fuera del alcance de esta tarea puntual de CTR). Gates: (1) Google ✓ — precio ya
sustentado en la página, sin keyword stuffing, sin datos inventados; (2) backlog ✓ — fila en
`cambios-seo.md`. Publicado: commit + `git push` (Vercel-Git publica), bajo
`publicar-mejoras-seo` (libre poder 2026-07-07). Verificación: re-medir el CTR de esta
página en 1-2 semanas (~28-jul).

## 2026-07-14 — 👷 Constructor: título y meta de la home reescritos (publicado)

Tarea t2 de la cola (CTR-bajo, score 29; empató con t3 pero ganó el desempate por
impresiones: 1.775 vs 945): `/` (home). Posición 5,7 pero CTR 1,35% (esperado ~4% en esa
posición) con 1.775 impresiones — el título viejo («Destape de Alcantarillado Santiago: 45
Min | Destape Rápido») terminaba en relleno de marca sin gancho. Reescribí título, meta
description, og:title/og:description y twitter:title/twitter:description: nuevo título
«Destape de Alcantarillado en Santiago: Llegamos en 45 Min», nueva descripción con dolor +
urgencia + garantía + CTA («Cañería o WC tapado no espera. Vamos a tu casa en 45 min, sin
romper pisos y con garantía de 30 días. Revisa precios reales y cotiza gratis por
WhatsApp.»). Saqué el precio «$45.000» del snippet a propósito: en `/precios-orientativos`
el destape de **alcantarillado** parte en $75.000 (el $45.000 es solo el WC) — ponerlo en
el título de la keyword «alcantarillado» hubiera sido un dato inexacto (Gate 1). Pasó los
DOS gates (detalle en `cambios-seo.md`) → publicado directo (ledger `publicar-mejoras-seo`,
2026-07-07): commit + `git push` (Vercel-Git). Verificación: re-medir el CTR de la home en
1-2 semanas.

## 2026-07-14 — 👷 Constructor: pasada sin cambios nuevos (t1 ya estaba hecha)

Tarea t1 de la cola (CTR-bajo, score 29, ganó el desempate por impresiones: 3.828):
`/blog/mal-olor-alcantarilla-casa-causas-soluciones`. Verifiqué el archivo real y el
título/meta/og/twitter/headline **ya son** los reescritos el 2026-07-07 («Huele a
Alcantarilla en Casa: Test de 3 Minutos + Solución», con el dato real de 90% sifón/ventilación
y test de 3 min ya en el cuerpo) — nada quedó a medias, no repetí el cambio. Search Console
sigue sin reflejar el CTR nuevo bajo el título nuevo (van más de 2 semanas; es más lento de lo
esperado, pero el mecanismo de verificación sigue siendo correcto: la tarea se recrea sola
mientras la métrica siga mal). Marqué `hecha_por: constructor` (fecha 2026-07-14) en
`tareas.json` del maestro para dejarlo trazado. Sin publicación (nada nuevo que publicar) → no
aplica gate 2 de esta pasada.

---

## 2026-07-14 · 📣 Ronda de Ads: la demanda de «baños quimicos» cede un poco, «03 Urbano» ya quedó en cero total
- «baños quimicos» (la única campaña activa) bajó de 85 a 73 conversiones/semana y el CPA
  subió un poco (~1.618 vs ~1.503) — igual sigue gastando 41% sobre su tope de presupuesto
  (venía 53%), así que la señal de "presupuesto chico para la demanda" se mantiene, solo
  algo menos urgente esta semana.
- «03 Urbano - Destapes Santiago» (pausada) ya no arrastra NADA de actividad en el reporte
  de 7 días — confirma que la pausa lleva bastantes semanas. «01 Rural Fosas» sigue en el
  mismo camino, cada vez con menos rastro.
- En negativas: reapareció «baños quimicos ventas» (gente que busca comprar, no arrendar) —
  sigue siendo candidata débil, sin urgencia. Nada nuevo grave.

## 2026-07-12 · 📣 Ronda de Ads: las negativas candidatas se siguen cayendo
- Ventana casi idéntica a la pasada anterior: «baños quimicos» sigue sola, con récord vigente
  y topando presupuesto (ver `ads-rescate-4`); «01 Rural» y «03 Urbano» siguen pausadas.
- «rimak baños quimicos» volvió a convertir (2ª vez) → descartada como negativa; «para
  fiestas» y «arriendo baños para eventos» también convirtieron → eventos/fiestas no se tocan.
- Única candidata nueva (débil): «baños quimicos ventas» (piden comprar; el negocio arrienda).
  Actualizada `ads-rescate-5` con la lista depurada.

## 2026-07-11 (13ª pasada) · 📣 Ronda de Ads: matiz en las negativas candidatas
- Ventana idéntica a la pasada anterior (récord de «baños quimicos» sigue vigente, tope de
  presupuesto también — ver `ads-rescate-4`).
- Matiz: «rimak baños quimicos» (marca competidora) muestra 1 conversión en la ventana y
  «baños portatiles para fiestas» también convirtió — las candidatas a negativa de
  `ads-rescate-5` pierden fuerza; solo «para eventos» sigue con gasto sin convertir.


## 2026-07-11 · 📣 Ronda de Ads: «baños quimicos» marcó récord y su presupuesto quedó chico
- Récord de la campaña: 76,3 conversiones/sem con CPA ~1.665, gastando ~18,2k/día contra un
  tope de 12k (un 50% pasado). La demanda sigue subiendo y es la ÚNICA campaña activa del
  cliente («01 Rural» y «03 Urbano» siguen pausadas).
- Subir ese presupuesto es la palanca más clara ahora — es plata, así que espera el OK de
  Alejandro (tarea `ads-rescate-4`, score máximo de la cola).
- «baños portatiles» volvió a convertir: confirmado que NO va como negativa.

## 2026-07-10 — 👷 Constructor: 6 casos reales des-orfanados (publicado)

Tarea `crawl-drapido-casos-reales` de la cola (enlazado, score 22): los 6 casos reales
(`/casos-reales/*`) estaban en el sitemap y en el ItemList del schema del índice, pero
ninguna página los enlazaba — invisibles para Google y prueba social desperdiciada. El repo
tenía este trabajo casi listo de un pase anterior sin terminar (sin commitear): grilla
«Casos documentados paso a paso» con las 6 tarjetas en `/casos-reales/` + 5 enlaces
contextuales desde páginas afines (cocina/grasa → Providencia, edificios → Las Condes,
fosas → Chicureo, mantención → Ñuñoa, Pirque → Pirque). Se verificó tarjeta por tarjeta
que cada cifra del anchor sale del propio caso (gate Google ✓) y se completó el 6º enlace
que faltaba: hidrojet → planta industrial Quilicura (operación nocturna, camión 15.000 L).
Cada caso queda con ≥2 enlaces entrantes (grilla + contextual). Detalle por URL en
`cambios-seo.md`. Publicado vía git push→Vercel bajo «publicar-mejoras-seo» (libre poder
con gates, 2026-07-07) + ping IndexNow (clave viva desde 07-09).

## 2026-07-10 — 👷 Constructor: pasada sin cambios nuevos (todo lo ejecutable ya estaba hecho)

Cola regenerada hoy (08:31) volvió a mostrar t1/t2/t3 (ctr-bajo) y t11-t15 (quick-win) con
las mismas métricas de siempre (esperado: Search Console tarda 1-2 semanas en reflejar el
CTR/posición bajo el título nuevo). Empecé por t1 (score 29, ganó el desempate por
impresiones: 3.342) y por error reescribí título/meta/og/twitter/headline de nuevo antes de
revisar la bitácora — lo noté a tiempo y revertí el archivo a la versión del 2026-07-07 sin
publicar nada. Verifiqué también t2, t3 y t11-t15 contra el sitio real: los 8 ya tienen el
título/meta/H1/enlazado descritos en `cambios-seo.md` (07-07/07-08), nada quedó a medias. El
resto de la cola (reseñas/maps/clarity/ads-\*/sin-conversión/engagement) es de Alejandro o no
es tipo ejecutable; `t19` (crear-contenido, destapando.cl) es de Alejandro (🎨, esfuerzo alto,
landings nuevas con decisiones de diseño). Marqué `hecha_por: constructor` en las 8 tareas del
`tareas.json` maestro para dejarlo trazado; si en 1-2 semanas el CTR/posición sigue igual, ahí
sí hay que revisar de verdad. Sin publicación → no aplica gate 2 de esta pasada.

## 2026-07-09 (3ª pasada) · Ronda Ads (solo lectura) — CAMBIO

- ⚠️ «01 - Rural - Fosas y Parcelas» (23302036223) ahora está PAUSADA (en la pasada anterior de hoy mismo estaba ENABLED). Junto con «03 Urbano» (ya pausada hace días), destaperapido hoy **solo pauta «baños quimicos»** — 2 de 3 campañas con historial dormidas. → nueva tarea `ads-rescate-6` (¿reactivar o intencional? decide Alejandro), reemplaza a `ads-rural-fosas`.
- baños quimicos (23710767076): sigue fuerte — 57 conv/sem, ~13,2k/12k (sigue pasada del tope), rank -27,3%/budget -25,0% (ads-rescate-4).
- Negativas: sin cambios — ninguna candidata reapareció en el top de gasto (ads-rescate-5).

## 2026-07-09 — 👷 Constructor: pasada sin cambios nuevos (t1 ya estaba hecha)

Tarea t1 de la cola (CTR-bajo, score 29, mayor impresiones del empate): `/blog/mal-olor-alcantarilla-casa-causas-soluciones`.
Verifiqué el archivo y el título/meta actual **ya es** el que se reescribió el 2026-07-07
(«Huele a Alcantarilla en Casa: Test de 3 Minutos + Solución», con la evidencia de 90%
sifón/ventilación y test de 3 min ya en el cuerpo) — no hacía falta ni se repitió ningún
cambio. También reconfirmé que t2, t3 y las quick-win t11-t15 (todo el resto de lo ejecutable
de esta pasada) ya están hechas desde el 07-07/07-08. La cola las vuelve a mostrar porque
Search Console tarda 2-3 días en reflejar el CTR nuevo bajo el título nuevo — es el mecanismo
de verificación esperado (docs/23), no un fallo del constructor. Marqué t1 con
`hecha_por: constructor` en tareas.json para dejarlo trazado; si en 1-2 semanas el CTR real
sigue igual, ahí sí hay que revisar de verdad. Sin publicación (nada que publicar) → no aplica
gate 2 de esta pasada (no hay URL nueva tocada).

## 2026-07-08 — 👷 Constructor: quick-win «inspección con cámara» (publicado)

Tarea t15 de la cola (quick-win, score 28): `/servicios/inspeccion-camara-alcantarillado`
rankea posición 9.4 con 506 impresiones y 23 clics. El H1 no tenía la keyword «alcantarillado»
(solo decía «Inspección con Cámara de Video») — se corrigió a «Inspección de Alcantarillado
con Cámara de Video». Título+meta reescritos con el precio real (desde $80.000, ya en el FAQ
schema de la página). De paso encontré que el FAQPage de esta página prometía 2 preguntas
(precio y «sirve para reclamar a constructora») que no estaban visibles en el body — las
agregué al FAQ visible para que el schema sea honesto. El enlazado interno ya era fuerte (nav,
grilla de «otros servicios», 4 posts del blog dedicados al tema) así que no agregué más para
no forzarlo. Gates: reglas de Google ✓ (dato ya sustentado en el propio JSON-LD, sin stuffing)
+ backlog ✓ (cambios-seo.md). Publicado vía git push→Vercel bajo «publicar-mejoras-seo»
(libre poder con gates, 2026-07-07). Sin INDEXNOW_KEY activo en este clon (el `.txt` de la
clave sigue sin desplegar, ver `indexnow.md`) → se saltó el ping.

## 2026-07-08 — 👷 Constructor: quick-win «líquido azul de baños químicos» (publicado)

Tarea t14 de la cola (quick-win, score 28, ganó el desempate por impresiones: 677 vs 506 de
t15): `/blog/liquido-azul-banos-quimicos-que-tiene-riesgos` rankea posición 6.5 con 677
impresiones y solo 3 clics. El archivo ya tenía el título y H1 mejorados de un pase anterior
sin terminar (sin commitear) — los revisé, están bien alineados con la intención de búsqueda
y la keyword se lee natural, así que los dejé. Agregué 2 enlaces internos de refuerzo desde el
propio post (arriendo de baños químicos, tabla de cálculo por evento) y un enlace recíproco
desde `/servicios/banos-quimicos` (página fuerte) hacia el post. Gates: reglas de Google ✓
(anchors descriptivos y variados, sin stuffing, sin datos inventados) + backlog ✓
(cambios-seo.md). Publicado vía git push→Vercel bajo «publicar-mejoras-seo» (libre poder con
gates, 2026-07-07). Sin `INDEXNOW_KEY` en este clon → se saltó el ping (Google se entera por
sitemap).

## 2026-07-08 — 👷 Constructor: quick-win «desagüe de cocina tapado» (publicado)

Tarea t13 de la cola (quick-win, score 28, la de mayor impresiones entre las empatadas sin
`hecha_por`): `/blog/por-que-se-tapa-desague-cocina` rankea posición 6.7 con 877 impresiones
y solo 3 clics. Encontré el título+meta+H1 y dos secciones de contenido nuevas
("¿Cuánto cuesta destapar el desagüe de la cocina?" con el precio real de
`/precios-orientativos`, y "¿Y si el agua ya no baja?" con enlaces a la guía de 7 métodos y
al servicio de destape de cocina) ya hechas sin commitear de un pase anterior sin terminar:
calzaban justo con esta tarea, así que las tomé y las terminé — solo actualicé el
`dateModified` a hoy. Sumé además el enlace de refuerzo que faltaba: desde la página fuerte
`/servicios/destape-desagues-cocina-y-grasa` (que no enlazaba a este post) hacia la guía,
con anchor «por qué se tapa el desagüe de la cocina». Dejé sin tocar los cambios sin
commitear de liquido-azul-banos-quimicos y banos-quimicos.html (tarea t14, otra pasada).
Gates: reglas de Google ✓ (sin stuffing, precio y enlaces ya sustentados en el sitio) +
backlog ✓ (cambios-seo.md). Publicado vía git push→Vercel bajo «publicar-mejoras-seo» (libre
poder con gates, 2026-07-07). Sin `INDEXNOW_KEY` en este clon → se saltó el ping.

## 2026-07-08 — 👷 Constructor: quick-win «/» home (publicado)

Tarea t12 de la cola (quick-win, score 28, la de mayor impresiones entre las empatadas
sin `hecha_por`): la home (/) rankea posición 5.7 con 1.647 impresiones. Encontré el H1
del hero sin commitear de un pase anterior sin terminar («Destape y Limpieza de Fosas en
Santiago» → «Destape de Alcantarillado y Limpieza de Fosas en Santiago»): calzaba justo con
esta tarea, así que lo tomé y lo terminé. El título/meta ya estaban alineados con esa keyword
(tarea t3) y el contenido (FAQ «¿Cuánto cuesta un destape de alcantarillado en Santiago?»,
bloque de servicios) ya cubría la intención con enlaces internos a
`/servicios/destape-alcantarillado`, así que no hizo falta agregar más — solo el H1 estaba
desalineado. Dejé sin tocar los demás cambios sin commitear del pase anterior
(por-que-se-tapa-desague-cocina, liquido-azul-banos-quimicos, baños químicos): pertenecen a
otras tareas de la cola (t13/t14) y la regla es una tarea completa por pasada. Gates: reglas
de Google ✓ (H1 describe un servicio real de la página, sin stuffing) + backlog ✓
(cambios-seo.md). Publicado vía git push→Vercel bajo «publicar-mejoras-seo» (libre poder con
gates, 2026-07-07). Sin INDEXNOW_KEY en este clon → se saltó el ping (Google se entera por
sitemap).

## 2026-07-08 — 👷 Constructor: quick-win «mal olor a alcantarilla» (publicado)

Tarea t11 de la cola (quick-win, score 28, la de mayor impresiones entre las empatadas):
la página /blog/mal-olor-alcantarilla-casa-causas-soluciones rankea posición 6.1 con 3.342
impresiones. Encontré cambios ya hechos (sin publicar) de un pase anterior sin terminar que
calzaban justo con esta tarea: H1 reformulado como pregunta («¿Mal olor a alcantarilla en
casa? 8 causas y cómo eliminarlo», mejor match de intención) y un enlace interno agregado en
la causa #5 hacia /servicios/destape-alcantarillado. Sumé el enlace de refuerzo que pedía la
tarea desde una página fuerte: en /servicios/destape-alcantarillado (página de servicio)
agregué una frase que enlaza de vuelta al post con anchor «causas del mal olor a alcantarilla
en casa», para que quien solo tiene olor (sin rebalse) revise las causas antes de contratar
destape. Dejé sin tocar los demás cambios sin commitear del pase anterior (index.html,
por-que-se-tapa-desague-cocina, liquido-azul-banos-quimicos, baños químicos): pertenecen a
otras tareas de la cola (t13/t14) y la regla es una tarea completa por pasada. Gates: reglas
de Google ✓ (anchors descriptivos y distintos entre sí, sin stuffing, contenido real) +
backlog ✓ (cambios-seo.md). Publicado vía git push→Vercel bajo «publicar-mejoras-seo» (libre
poder con gates, 2026-07-07). Sin INDEXNOW_KEY en este clon → se saltó el ping (Google se
entera por sitemap).

## 2026-07-08 — 👷 Constructor: título+meta de «/» (home, publicado)

Tarea t3 de la cola (CTR-bajo, score 29): la home (/) rankea posición 5.7 con 1.647
impresiones pero CTR 1.03% (esperado ~4%). Se reescribió título + meta description (más
atractivos, con urgencia y beneficio: «45 Min», garantía, precio desde $45.000 — mismo dato
real del cuerpo: hero «Llegamos en 45 min. Sin romper. 24/7.», FAQ con precio desde $45.000 y
garantía total) y se alinearon og:/twitter:. Gates: reglas de Google ✓ + backlog ✓
(cambios-seo.md). Publicado vía git push→Vercel bajo «publicar-mejoras-seo» (libre poder con
gates, 2026-07-07). Sin INDEXNOW_KEY en este clon → se saltó el ping (Google se entera por
sitemap). Nota: el archivo tenía un cambio sin commitear de otra tarea (H1, de un pase
anterior sin terminar) — se dejó intacto y sin publicar, no es parte de esta tarea.

## 2026-07-08 — 👷 Constructor: título+meta de «/precios-orientativos» (publicado)

Tarea t2 de la cola (CTR-bajo, score 29): la página /precios-orientativos rankea posición
4.2 con 2.177 impresiones pero CTR 4.82% (esperado ~7%). Se reescribió título + meta
description (más atractivos, mismo dato real del cuerpo: WC desde $45.000, cocina $55.000,
alcantarillado $75.000, garantía 30 días, sin romper pisos) y se alinearon og:/twitter:.
Gates: reglas de Google ✓ + backlog ✓ (cambios-seo.md). Publicado vía git push→Vercel bajo
«publicar-mejoras-seo» (libre poder con gates, 2026-07-07). Sin INDEXNOW_KEY en este clon →
se saltó el ping (Google se entera por sitemap). Nota: el repo tenía cambios sin commitear
de otro pase anterior sin terminar (index.html, servicios/*, blog/*) — se dejaron intactos y
sin publicar, no son parte de esta tarea.

## 2026-07-07 — 👷 Constructor: título+meta de «mal olor a alcantarilla» (publicado)

Tarea t1 de la cola (CTR-bajo, score 29): la página /blog/mal-olor-alcantarilla-casa-causas-soluciones
rankea posición 6.1 con 3.342 impresiones pero CTR 1.5% (esperado ~4%). Se reescribió título +
meta description (más atractivos, mismo dato real del cuerpo: 90% sifón/ventilación, test de
3 min) y se alinearon og:/twitter:/JSON-LD BlogPosting. Gates: reglas de Google ✓ + backlog ✓
(cambios-seo.md). Publicado vía git push→Vercel bajo «publicar-mejoras-seo» (libre poder con
gates, 2026-07-07). Sin INDEXNOW_KEY en este clon → se saltó el ping (Google se entera por
sitemap). Nota: el archivo tenía cambios sin commitear de otra tarea (H1 + enlace interno, de
un pase anterior sin terminar) — se dejaron intactos y sin publicar, no son parte de esta tarea.

## 2026-07-07 — Enlazado interno: 5 huérfanas rescatadas (publicado)

El crawler detectó 5 posts del blog sin NINGÚN enlace entrante (la grilla listaba 28 de
35). Se completó la grilla y se agregaron 9 enlaces contextuales desde 7 páginas (detalle
por URL en cambios-seo.md). Gates: reglas de Google ✓ + backlog ✓. Publicado vía git
push→Vercel bajo el permiso «publicar-mejoras-seo» (libre poder con gates, 2026-07-07).

## 2026-07-06 — 📣 Ronda de Ads (v1 solo-lectura)
- 03 Urbano (23950664619): 18 conv/sem. Budget-lost bajó 57,1%→41,7% (la plata ayudó) pero apareció 38,3% perdido por RANKING — señal nueva. Gasta 8,6k/10k. → ads-rescate-2.
- baños quimicos (23710767076): ranking volvió a subir 19,6%→25,0%; budget-lost bajó 56,6%→36,5% gastando solo 2,8k/12k (señal rara persiste). → ads-rescate-4.
- 01 Rural Fosas (23302036223): budget-lost 66,3%→45,3% pero solo 3 conv/sem, CPA ~16,7k, gasta 7,2k/19k. Diagnosticar antes de escalar. → ads-rural-fosas.
- Negativas: única con gasto real sigue siendo «aguas andinas destape de alcantarillado» (637 CLP, 0 conv). Resto (duchas/eventos) con 0 gasto. → ads-rescate-5.
- Todas encoladas como PLATA (requieren OK de Alejandro). Correr --dry-run primero.

## 2026-07-06 · Ronda Ads (solo lectura)
- 03 Urbano: 18 conv/sem, budget -41,7%, rank -38,3%, ~8,6k/10k (ads-rescate-2).
- baños quimicos: 8 conv, rank 25,0%, budget -36,5% gastando solo 2,8k/12k (ads-rescate-4).
- 01 Rural Fosas: 4,7 conv/sem, CPA ~10,7k (sostenido), budget -45,3% con 7,2k/19k (ads-rural-fosas).
- Negativas candidatas confirmadas: aguas andinas, duchas, eventos (ads-rescate-5).

## 2026-07-06 (21:06) · Ronda Ads (solo lectura) — CAMBIO
- ⚠️ «03 Urbano - Destapes Santiago» (23950664619) ahora está PAUSADA. Era la que más convertía (48 conv/30d, ~18/sem) y es el servicio central. Hoy destaperapido NO pauta destapes urbanos — solo «01 Rural» y «baños quimicos». → ads-rescate-2 reconvertida a ALERTA (¿reactivar o intencional? decide Alejandro).
- baños quimicos (23710767076): sin cambios — rank 25,0%, budget -36,5%, 8 conv/sem, ~2,9k/12k (ads-rescate-4).
- 01 Rural Fosas (23302036223): sin cambios — 4,7 conv/sem, CPA ~10,7k, budget -45,3%, 7,2k/19k (ads-rural-fosas).
- Negativas: sin cambios — «aguas andinas destape de alcantarillado» sigue como única con gasto (637 CLP, 0 conv); duchas/eventos con 0 gasto (ads-rescate-5).

## 2026-07-07 · Ronda Ads (solo lectura)
- «03 Urbano» (23950664619) SIGUE PAUSADA pero trajo 21 conv en 7d antes de la pausa. Destapes urbanos sin pauta (ads-rescate-2, decide Alejandro).
- baños quimicos (23710767076): DESPEGÓ — 27 conv/sem (venía en 8), CPA ~1,7k, budget -24,3%, rank -27,8%, ~6,4k/12k. Oportunidad de escalar (ads-rescate-4).
- 01 Rural Fosas (23302036223): 6 conv/sem, CPA ~10,8k, budget -33,1%, rank sano 7,6%, ~9,3k/19k. Términos geo por comuna gastan sin convertir → revisar landings (ads-rural-fosas).
- Negativas: + marcas competencia «disal» y «sanicer»; siguen «aguas andinas» (637 CLP), duchas y eventos. NO tocar términos de precio (ads-rescate-5).

## 2026-07-10 · 👷 Constructor — enlazado: des-orfanar /nosotros, /testimonios y /ruta-buin (crawl-drapido-nav-paginas)
- Qué: `/nosotros` y `/testimonios` existían e indexaban pero ninguna página las enlazaba estáticamente. Ahora: footer del home (columna «Empresa», anchors «Quiénes somos» / «Testimonios de clientes») + 2 enlaces contextuales en `/por-que-elegirnos` (hero → nosotros; nota de verificación de reseñas → testimonios). Cada una queda con 2 enlaces entrantes.
- `/ruta-buin` (seguimiento referencial del camión): +1 enlace contextual desde `/zonas/rural/buin-paine` (sección de emergencia, anchor «seguimiento referencial del camión hacia Buin»). ⚠️ Duda anotada: es página operativa tipo tracking, igual que la de fullfosas que espera decisión (¿evergreen o noindex?); si Alejandro decide noindex, quitar el enlace.
- Gates: (1) Google ✓ — anchors descriptivos y variados, contenido propio real, nada inventado; (2) backlog ✓ — 3 filas en cambios-seo.md.
- Publicado: commit + git push (Vercel publica) bajo `publicar-mejoras-seo` (libre poder 2026-07-07). Verificación: re-crawl `--site https://www.destaperapido.cl` → las 3 deben salir de `huerfanas`.

## 2026-07-11 · 👷 Constructor — pasada sin cambios (todo en ventana de verificación)
- La cola trae de vuelta t1-t3 (ctr-bajo) y t11-t15 (quick-win), pero TODAS ya se ejecutaron
  y publicaron entre el 07 y 08-jul (títulos/meta/H1/contenido/enlaces — ver cambios-seo.md).
  El scout las regeneró con datos GSC que aún no reflejan los cambios (rezago 2-3 días).
- Decisión: NO re-tocar (sería churn de títulos, malo para SEO). Se anotó `nota_constructor`
  en t1 y t2 con la fecha de re-evaluación (~21/22-jul). Si el CTR sigue bajo entonces,
  corresponde la siguiente iteración.

## 2026-07-22 · 📣 Ronda de Ads (solo lectura)

- Las 3 campañas convierten (36 + 32 + 17 conv/7d) pero «03 Urbano» pierde el 57,4% de
  las búsquedas por PRESUPUESTO — la decisión de plata quedó encolada para Alejandro.
- Buena noticia: la fuga de «arriendo baño quimico» se cerró sola (6 conversiones esta
  semana en esas búsquedas) — se eliminó esa tarea de la cola.
- Nuevo lote de negativas informacionales encolado («desatorador», «quien destapa»,
  «como se llama», ~2.570 CLP/sem). Nada aplicado; detalle en `cambios-ads.md`.

## 2026-07-23 · 👷 Constructor — t17 quick-win home: enlazado interno a WC/baños y desagües de cocina (publicado)
- Selección: t1-t4 (score 29) siguen en ventana de verificación (~28-jul); entre los
  quick-wins score 28, t17 ganó el desempate por impresiones (2.228 vs 1.216/1.202/841).
- Palanca: la ÚNICA libre de la home era el enlazado/contenido — title/meta en vuelo (t2,
  20-jul), H1 ya alineado (08-jul), hero PROPUESTO esperando a Alejandro (45 vs 90 min).
- Hallazgo: las consultas top-3 con CTR 0% de la home («destape de baños», «destape wc a
  domicilio», «destape de desagues», documentadas el 20-jul) tienen páginas de servicio
  exactas (`/servicios/destape-wc-y-banos`, `/servicios/destape-desagues-cocina-y-grasa`)
  pero la home solo las mencionaba en el JSON-LD — cero enlaces visibles.
- Cambio: +8 enlaces en 4 puntos con patrones existentes (menú desktop con fa-bath/fa-sink,
  menú móvil, footer Servicios, 2 anchors contextuales en la tarjeta «Destapes Urbanos»).
  Cero CSS nuevo (clases verificadas en output.css); title/meta/H1/schema intactos.
- Gates: (1) Google ✓ — anchors descriptivos y variados = query objetivo, páginas destino
  reales (~85-89 KB con FAQ), sin cifras nuevas, HTML ahora coincide con el schema;
  (2) backlog ✓ — fila en cambios-seo.md.
- Publicado: commit quirúrgico SOLO de index.html + registros (el trabajo huérfano de
  t18/t19 sigue intacto en disco) → git push → Vercel. IndexNow: ping a la home con la
  clave de indexnow.md.
- Verificación: CTR de esas consultas y clics de las 2 páginas de servicio en 2-3 semanas.
