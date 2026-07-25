# Veredicto del candado — caminos por aprobar

**30 de 30 se pueden aprobar hoy** · 0 necesita(n) un arreglo antes.

Esto es una REVISIÓN EN SECO: nada se activó, nada se publicó. Es el mismo candado
que corre al apretar "Aprobar" en el panel, solo que mirando.

| Veredicto | Caminos |
| --- | ---: |
| ✅ Pasan | 19 |
| ⚠️ Pasan con avisos | 11 |
| ❌ Rechazados | 0 |
| **Total revisado** | **30** |

Revisado el 25 de julio de 2026, 12:01 p. m. · instancia `/Users/alejandroriveracarrasco/SaSS/destaperapido/dixdybot-data`
Propuestas leídas de `/Users/alejandroriveracarrasco/SaSS/destaperapido/dixdybot-data/caminos-propuestos.json`
Se midieron contra 3 camino(s) ya activo(s) · el candado tardó 22.3 ms en revisarlos todos.

> **Ojo con lo que significa "pasa".** Hoy la exigencia a los ejemplos está en *declarada*: se revisa que el ejemplo esté completo (lo que dice el cliente, lo que responde el bot y cómo saber si estuvo bien), pero **nadie los jugó todavía** contra el bot. Si lo pones en modo exigente, ninguno se activa hasta que el gimnasio apruebe al agente de cada tema.

## ⚠️ Pasan, pero mira esto antes (11)

Se pueden aprobar igual — el aviso es para que sepas qué va a pasar, no un error.

### cobertura · ventas

**Comuna fuera de cobertura: cerrar con puente, nunca en seco**  
`cam-fuera-de-cobertura` · cuando La comuna no está en ninguna zona del tarifario o El cliente pide servicio fuera de la Región Metropolitana

- ⚠️ se pisa con 'cam-ubicacion-especial': los dos se activan casi con lo mismo (50% parecido) — el tuyo dice "La comuna no está en ninguna zona del tarifario" y el otro "La comuna no aparece en las zonas del tarifario". Pero terminan distinto: uno para a preguntarte a ti y el otro le contesta solo al cliente, así que NO los juntes: mira cuál tiene que ganar cuando pasen los dos y déjalo escrito (puede ser que uno sea la excepción del otro).

### cotizacion · ventas

**Con el kit completo: precio de tabla al tiro, en valor mensual y con lo incluido gratis**  
`cam-cotizar-kit-completo` · cuando Ya están comuna, cantidad y tiempo o El cliente pide el valor y el kit está completo

- ⚠️ se pisa con 'cam-precio-kit-completo': los dos se activan casi con lo mismo (89% parecido) — el tuyo dice "Ya están comuna, cantidad y tiempo" y el otro "Ya están comuna, cantidad y tiempo en la conversación". Y mandan hacer casi lo mismo: es la misma regla escrita dos veces, júntalas en una y el bot deja de gastar dos cupos en el mismo consejo.
- ⚠️ se pisa con 'cam-precio-exacto-neto': los dos se activan casi con lo mismo (55% parecido) — el tuyo dice "Ya están comuna, cantidad y tiempo" y el otro "Ya tienes comuna, cantidad y tiempo y toca dar el valor". Y mandan hacer casi lo mismo: es la misma regla escrita dos veces, júntalas en una y el bot deja de gastar dos cupos en el mismo consejo.

**El precio sale exacto del tarifario y se dice neto**  
`cam-precio-exacto-neto` · cuando Ya tienes comuna, cantidad y tiempo y toca dar el valor o El cliente pregunta si el valor está con IVA incluido o La combinación pedida no existe en la tabla

- ⚠️ se pisa con 'cam-neto-iva-factura': los dos se activan casi con lo mismo (75% parecido) — el tuyo dice "El cliente pregunta si el valor está con IVA incluido" y el otro "El cliente pregunta si el valor incluye IVA". Y mandan hacer casi lo mismo: es la misma regla escrita dos veces, júntalas en una y el bot deja de gastar dos cupos en el mismo consejo.
- ⚠️ se pisa con 'cam-cotizar-kit-completo': los dos se activan casi con lo mismo (55% parecido) — el tuyo dice "Ya tienes comuna, cantidad y tiempo y toca dar el valor" y el otro "Ya están comuna, cantidad y tiempo". Y mandan hacer casi lo mismo: es la misma regla escrita dos veces, júntalas en una y el bot deja de gastar dos cupos en el mismo consejo.
- ⚠️ se pisa con 'cam-precio-kit-completo': los dos se activan casi con lo mismo (50% parecido) — el tuyo dice "Ya tienes comuna, cantidad y tiempo y toca dar el valor" y el otro "Ya están comuna, cantidad y tiempo en la conversación". Y mandan hacer casi lo mismo: es la misma regla escrita dos veces, júntalas en una y el bot deja de gastar dos cupos en el mismo consejo.

**Kit completo (comuna, cantidad, plazo) → valor de tabla al tiro y en neto**  
`cam-precio-kit-completo` · cuando El cliente pregunta cuánto sale / cuánto vale / precio o Ya están comuna, cantidad y tiempo en la conversación o El cliente confirma un plazo que existe como fila del tarifario para esa zona

- ⚠️ se pisa con 'cam-cotizar-kit-completo': los dos se activan casi con lo mismo (89% parecido) — el tuyo dice "Ya están comuna, cantidad y tiempo en la conversación" y el otro "Ya están comuna, cantidad y tiempo". Y mandan hacer casi lo mismo: es la misma regla escrita dos veces, júntalas en una y el bot deja de gastar dos cupos en el mismo consejo.
- ⚠️ se pisa con 'cam-extra-sin-tarifa': los dos se activan casi con lo mismo (60% parecido) — el tuyo dice "El cliente pregunta cuánto sale / cuánto vale / precio" y el otro "El cliente pregunta cuánto sale agregar una limpieza". Pero terminan distinto: uno para a preguntarte a ti y el otro le contesta solo al cliente, así que NO los juntes: mira cuál tiene que ganar cuando pasen los dos y déjalo escrito (puede ser que uno sea la excepción del otro).
- ⚠️ se pisa con 'cam-precio-exacto-neto': los dos se activan casi con lo mismo (50% parecido) — el tuyo dice "Ya están comuna, cantidad y tiempo en la conversación" y el otro "Ya tienes comuna, cantidad y tiempo y toca dar el valor". Y mandan hacer casi lo mismo: es la misma regla escrita dos veces, júntalas en una y el bot deja de gastar dos cupos en el mismo consejo.

**El valor es neto: IVA solo si preguntan o facturan, y jamás como descuento**  
`cam-neto-iva-factura` · cuando El cliente pregunta si el valor incluye IVA o El cliente pide factura o el total final o El bot iba a mencionar el IVA por iniciativa propia o El cliente pide rebaja

- ⚠️ se pisa con 'cam-precio-exacto-neto': los dos se activan casi con lo mismo (75% parecido) — el tuyo dice "El cliente pregunta si el valor incluye IVA" y el otro "El cliente pregunta si el valor está con IVA incluido". Y mandan hacer casi lo mismo: es la misma regla escrita dos veces, júntalas en una y el bot deja de gastar dos cupos en el mismo consejo.
- ⚠️ se pisa con 'cam-consulta-sobre-cotizacion-enviada': los dos se activan casi con lo mismo (60% parecido) — el tuyo dice "El cliente pregunta si el valor incluye IVA" y el otro "Pregunta si el valor incluye traslados, limpiezas o retiro". Pero terminan distinto: uno para a preguntarte a ti y el otro le contesta solo al cliente, así que NO los juntes: mira cuál tiene que ganar cuando pasen los dos y déjalo escrito (puede ser que uno sea la excepción del otro).
- ⚠️ se pisa con 'cam-gesto-buen-cliente': los dos se activan casi con lo mismo (57% parecido) — el tuyo dice "El cliente pide rebaja" y el otro "El cliente pide rebaja o un valor fuera del tarifario". Pero terminan distinto: uno para a preguntarte a ti y el otro le contesta solo al cliente, así que NO los juntes: mira cuál tiene que ganar cuando pasen los dos y déjalo escrito (puede ser que uno sea la excepción del otro).

### excepciones · general

**Tarifa o condición que no está en el tarifario: parar y pedir el OK del dueño**  
`cam-excepcion-fuera-tarifario` · cuando El cliente pide una modalidad que la tabla no tiene para esa zona (ej. evento o quincena en zona lejana que solo tiene mensual) o Pide un descuento especial, un servicio adicional o una condición de pago fuera de lo estándar o Pide el total por todo el período o una limpieza extra sin valor en tabla

- ⚠️ en medio de este camino el bot te pregunta a ti antes de seguir

### excepciones · ventas

**Recinto o zona especial: el equipo confirma el valor hoy mismo**  
`cam-ubicacion-especial` · cuando El servicio es en aeródromo, fundo, faena aislada o parcela sin dirección clara o La comuna no aparece en las zonas del tarifario o El plazo pedido no existe para esa zona lejana

- ⚠️ se pisa con 'cam-fuera-de-cobertura': los dos se activan casi con lo mismo (50% parecido) — el tuyo dice "La comuna no aparece en las zonas del tarifario" y el otro "La comuna no está en ninguna zona del tarifario". Pero terminan distinto: uno para a preguntarte a ti y el otro le contesta solo al cliente, así que NO los juntes: mira cuál tiene que ganar cuando pasen los dos y déjalo escrito (puede ser que uno sea la excepción del otro).
- ⚠️ en medio de este camino el bot te pregunta a ti antes de seguir

**Un extra sin tarifa nunca frena el precio principal**  
`cam-extra-sin-tarifa` · cuando El cliente pide un extra sin tarifa: limpieza adicional, visita extra, servicio especial o El cliente pregunta cuánto sale agregar una limpieza o Ya se tiene el kit para cotizar el baño

- ⚠️ se pisa con 'cam-precio-kit-completo': los dos se activan casi con lo mismo (60% parecido) — el tuyo dice "El cliente pregunta cuánto sale agregar una limpieza" y el otro "El cliente pregunta cuánto sale / cuánto vale / precio". Pero terminan distinto: uno para a preguntarte a ti y el otro le contesta solo al cliente, así que NO los juntes: mira cuál tiene que ganar cuando pasen los dos y déjalo escrito (puede ser que uno sea la excepción del otro).
- ⚠️ en medio de este camino el bot te pregunta a ti antes de seguir

### seguimiento · soporte

**Dudas sobre una cotización ya enviada: aclarar ítems sin recalcular**  
`cam-consulta-sobre-cotizacion-enviada` · cuando El cliente pregunta qué incluye un ítem de la cotización que recibió o Pregunta si el valor incluye traslados, limpiezas o retiro o Pide confirmar a qué corresponde un valor del documento

- ⚠️ se pisa con 'cam-neto-iva-factura': los dos se activan casi con lo mismo (60% parecido) — el tuyo dice "Pregunta si el valor incluye traslados, limpiezas o retiro" y el otro "El cliente pregunta si el valor incluye IVA". Pero terminan distinto: uno para a preguntarte a ti y el otro le contesta solo al cliente, así que NO los juntes: mira cuál tiene que ganar cuando pasen los dos y déjalo escrito (puede ser que uno sea la excepción del otro).
- ⚠️ en medio de este camino el bot te pregunta a ti antes de seguir

### upsell · ventas

**Todo extra se cotiza aparte y con total antes de cerrar**  
`cam-extras-con-total` · cuando El cliente pide más frecuencia de limpieza que la incluida o El cliente pide horarios, retiros o condiciones especiales o Vas a confirmar, cerrar o agendar el servicio

- ⚠️ en medio de este camino el bot te pregunta a ti antes de seguir

**Gesto en el extremo bajo del rango, nunca descuento genérico**  
`cam-gesto-buen-cliente` · cuando El cliente cotiza varios baños o es cliente recurrente y se ofrece un servicio extra con rango o El cliente pide rebaja o un valor fuera del tarifario

- ⚠️ se pisa con 'cam-neto-iva-factura': los dos se activan casi con lo mismo (57% parecido) — el tuyo dice "El cliente pide rebaja o un valor fuera del tarifario" y el otro "El cliente pide rebaja". Pero terminan distinto: uno para a preguntarte a ti y el otro le contesta solo al cliente, así que NO los juntes: mira cuál tiene que ganar cuando pasen los dos y déjalo escrito (puede ser que uno sea la excepción del otro).
- ⚠️ en medio de este camino el bot te pregunta a ti antes de seguir

## ✅ Pasan el candado (19)

Estos están sanos: puedes aprobarlos tal cual.

### calificacion · ventas

**Completar el kit mínimo antes de cotizar (ubicación → tiempo → cantidad)**  
`cam-calificar-kit-minimo` · cuando El cliente pide precio o arriendo y falta comuna, cantidad o tiempo o Habla de obra o evento sin decir dónde o Dice 'baños' sin dar un número

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

**Cantidad: asumir cuando es obvia, cotizar por unidad cuando es rango**  
`cam-cantidad-obvia-o-rango` · cuando El cliente no dijo cuántos baños pero el contexto es de una casa, familia o un maestro o El contexto sugiere varios baños (obra, evento, harta gente) o El cliente dio un rango de cantidad ('1 o 2', '3 a 5')

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

### cierre · agenda

**Derivar al equipo o repartidor con un próximo paso concreto**  
`cam-derivar-entrega` · cuando El cliente confirma la reserva o el pago o Hay que coordinar día, hora o dirección de entrega o retiro

- ✅ sin peros: 1 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

**Sin dirección exacta no hay cierre: reservar y pedir lo que falta**  
`cam-cierre-sin-direccion` · cuando El cliente dice 'ya, dale', 'quedamos así' o acepta el trato o El cliente dice que confirma la dirección después o Faltan dirección exacta, fecha o correo para agendar

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

### cierre · ventas

**Cotización formal: pedir el correo y esperar el aviso del sistema antes de decir que se envió**  
`cam-cotizacion-formal-correo` · cuando 'Mándeme la cotización formal', 'me la envía por correo', 'necesito el documento'

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

### confianza · soporte

**Respaldo sanitario, residuos y datos formales**  
`cam-respaldo-sanitario` · cuando El cliente pregunta por permisos, certificación o resolución sanitaria o El cliente pregunta cómo se disponen los residuos o El cliente pide cotización formal, factura o datos para transferir

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

### cotizacion · ventas

**Dato nuevo a mitad de cotización: recalcular con la tabla y recién ahí pedir la reserva**  
`cam-recalcular-dato-nuevo` · cuando El cliente agrega unidades o entrega el dato que faltaba después de recibir un valor o Cambia la cantidad, la comuna o el período ya cotizado

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

**Cada plazo tiene su propia tarifa: nunca los juntes**  
`cam-cada-plazo-su-tarifa` · cuando El cliente duda entre dos plazos ('una semana o dos') o Vas a mencionar más de un plazo en la misma respuesta

- ✅ sin peros: 1 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

**Lo incluido se ajusta al plazo real pedido**  
`cam-incluido-segun-plazo` · cuando Vas a listar lo que incluye el arriendo o El pedido es un evento o arriendo de pocos días o El pedido es mensual o de varias semanas

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

**Señal de empresa que factura: cotizar con IVA y pedir datos tributarios**  
`cam-empresa-factura` · cuando Menciona capex, evaluación de proyecto, orden de compra o razón social tipo S.A./SpA/Ltda. o Pide el PDF para presentarlo en una compra formal o licitación o Declara que la empresa necesita factura

- ✅ sin peros: 1 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

**Ofrecer la cotización formal en los dos momentos correctos**  
`cam-formal-dos-momentos` · cuando El cliente dice que está cotizando, comparando o que debe presentar valores o El cliente acepta el valor o quiere avanzar o El hilo de venta iba a terminar sin próximo paso

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

### estilo · general

**Ritmo humano: esperar, no repetir y cerrar siempre con el próximo paso**  
`cam-ritmo-humano-siguiente-paso` · cuando El cliente escribe varios mensajes cortos seguidos ('hola', 'buenas', 'consulta') o El bot está por repetir un precio o algo ya dicho o El cliente responde 'ok', 'gracias', 'ya' y el trato no está cerrado

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

**Nada de loops: no repreguntar lo dicho ni insistir con ofertas**  
`cam-sin-loops` · cuando El cliente ya entregó un dato y el bot iba a pedirle confirmarlo o El cliente rechaza la recomendación de sumar baños o El cliente repite el mismo mensaje de cierre dos o más veces

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

### estilo · ventas

**Sin eco: un solo mensaje, una sola pregunta**  
`cam-sin-eco-un-mensaje` · cuando El cliente acaba de enviar dirección, fechas, cantidad o comuna o Falta un dato del kit mínimo (comuna, cantidad, tiempo) para poder cotizar o Es el primer contacto y falta información

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

**Relee todo el historial antes de preguntar**  
`cam-relee-historial` · cuando Vas a preguntar comuna, cantidad, plazo o uso o Vas a cerrar el mensaje con la pregunta de avance por defecto o La respuesta depende de un dato que aún no tienes

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

### objeciones · ventas

**Objeción de precio: reafirmar lo incluido y usar el segundo baño como gancho real**  
`cam-objecion-precio` · cuando 'Está caro', 'es mucho', 'lo voy a pensar por el precio' o El cliente compara con otra empresa o duda del valor o Cliente de zona lejana que duda por el precio de un baño

- ✅ sin peros: 1 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

### seguimiento · soporte

**Después del precio: dejarlo preguntar y responder toda duda con calidez**  
`cam-dudas-post-precio` · cuando El cliente acaba de recibir el valor o Pregunta por limpiezas, IVA, traslados, medidas, horarios, formas de pago, residuos o certificación sanitaria o Pregunta algo cuyo dato exacto no tienes

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

**Cotización que aún no llega: respuesta corta, sin prometer hora**  
`cam-cotizacion-pendiente` · cuando El cliente pregunta por una cotización que no ha recibido o El cliente pregunta cuándo llega el valor que quedó con el equipo o El cliente reclama que no le llegó el correo o el PDF

- ✅ sin peros: 1 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

### upsell · ventas

**'¿Y si se llenan?' es oportunidad de venta, no tranquilizador**  
`cam-se-llenan-upsell` · cuando El cliente pregunta qué pasa si los baños se llenan o cuánto aguantan o El cliente pregunta por limpieza o mantención durante un evento

- ✅ sin peros: 2 ejemplo(s) de conversación, cero precios escritos a mano, sin choques con otros caminos

---

### Cómo leer esto

- **Ejemplo de conversación** (prueba dorada): un mini diálogo cliente↔bot guardado que
  sirve de examen. Un camino sin ninguno no se puede publicar: nadie podría saber si
  un cambio futuro lo rompió.
- **Precio escrito a mano**: el texto del camino no puede traer cifras. Los valores
  salen de tu tarifario, así cambiar un precio se hace en un lugar y no en veinte.
- **Choque entre caminos**: dos caminos que calzan con el mismo mensaje. El bot resuelve
  con las prioridades que tengan escritas; el aviso es para que sepas cuál va a mandar.
- Cada camino se midió **como si lo activaras solo**. Si los apruebas todos de una,
  los choques entre ellos aparecen marcados con "si apruebas todo el lote junto".

