# Diario de la noche — 30-jul-2026

Parte de trabajo del turno de noche (carril backend). Se actualiza al cerrar cada pieza.

---

## ✅ Pieza 1 · Historial + volver atrás (E1) — TERMINADA y en vivo

**Qué quedó funcionando:** desde ahora, cada vez que tú (o la IA, o el sistema) cambia un
ajuste o un camino, queda guardada una **foto de cómo estaba todo justo antes**. En el menú
del panel hay una vista nueva, **«Cambios»** (grupo Sistema), que lista esos puntos — quién
hizo qué y hace cuánto — y cada uno trae un botón **«Volver aquí»** (pide doble toque). Al
volver, TODO regresa a ese momento: los ajustes y también los caminos del bot.

**Las redes de seguridad que trae por dentro:**
- Volver también deja su propia foto → **volver tiene vuelta atrás**.
- Antes de restaurar se guarda un respaldo de la base en `data/respaldos/`.
- Nada se borra jamás: un camino que hoy existe y en la foto no, queda «retirado».
- O vuelve todo, o no vuelve nada (jamás un negocio a medias).

**Cómo lo comprobé:** 13 pruebas nuevas del ciclo completo (cambiar → foto → volver →
estado restaurado, incluida la trampa de los dos almacenes de caminos), 990 pruebas en
verde, y los dos paneles reiniciados respondiendo con la vista nueva.

**Commit:** `cd09671`. **Nada quedó a medias.**

**Detalle honesto:** la lista parte vacía — las fotos nacen desde ahora, no hay historia
hacia atrás (no existía dónde mirarla). El primer cambio que hagas ya deja su punto.

---

## ✅ Pieza 2 · Vista 💲 Precios (P1) — TERMINADA y en vivo

**Qué quedó funcionando:** «Precios» es ahora una vista propia del menú (ya no hay que
bucear en Ajustes → Cotiza). La tabla por zonas se ve como tabla de verdad: cada plazo en
su celda editable, las comunas y el nombre de la zona también en línea, el flete, quitar y
agregar zonas, y las tarifas especiales que nacieron de tus dudas — con su origen a la
vista y su botón «Quitar» (con deshacer). Una celda **vacía** significa «sin precio de
lista: el bot te pregunta a ti», y la vista lo explica.

**El detalle que importa:** guardar precios usa exactamente la misma puerta validada de
siempre, y gracias a la pieza 1 **cada guardado deja un punto en «Cambios»** — el botón
mismo te lo dice. Editar precios dejó de ser un salto sin red.

**Cómo lo comprobé:** arnés sin navegador (8 chequeos del render con una config de
ejemplo), los 6 verificadores del panel y el test de la PWA, todo verde. Paneles
reiniciados; el botón «Precios» ya se sirve en el HTML vivo.

**Commit:** `7d98c1f`. **Nada quedó a medias.**

**Convivencia:** la otra sesión (carril experiencia) está trabajando esta misma noche
sobre `app.js` — sus dos arreglos del robot guía viajaron en mi commit porque compartimos
archivo (está dicho en el mensaje del commit). Nos estamos turnando sin pisarnos.

---

## ✅ Pieza 3 · Traer la lista y que la IA la ordene (P2) — TERMINADA y en vivo

**Qué quedó funcionando:** en la vista Precios hay un botón **«📥 Traer mi lista»**. Pegas
tu lista como la tengas — las celdas de un Excel se pegan solas, el texto de un PDF, tus
apuntes — y la IA la ordena y te muestra **qué entendió**: la tabla propuesta, los huecos
como «—» (jamás los rellena) y sus dudas anotadas a la vista.

**La regla de plata, dos veces:** ordenar **no guarda nada** (el servidor solo devuelve la
propuesta), y «Usar esto en mi tabla» solo llena la tabla editable — guardar sigue siendo
un botón aparte, tuyo, que además deja su punto en «Cambios». Un precio mal leído es
plata; por eso nada camina solo.

**Nota honesta:** por ahora es **pegar** (que cubre Excel y PDF vía copiar-pegar). Subir
la foto de un papel para que la IA la *mire* necesita conectar la visión — quedó anotado
como siguiente paso de Precios, no lo inventé a medias.

**Cómo lo comprobé:** 13 chequeos del render sin navegador + tests del endpoint con
cerebro falso (verifican que NO escribe nada y que el prompt prohíbe inventar cifras).
**Commit:** `edf289f`.

---

## ✅ Pieza 4 · Un solo candado (E2) — TERMINADA y en vivo

**Qué quedó funcionando:** el revisor de caminos que los comentarios prometían ahora
existe de verdad (`caminos-lint`), y **todas las puertas usan el mismo juez**:
- Se acabaron: dos caminos con el mismo nombre (contaban doble), saltos desde pasos que no
  existen, dos saltos sin condición desde el mismo paso (el bot no sabía cuál tomar), y
  relaciones con nombres mal escritos que morían en silencio.
- **La puerta trasera quedó cerrada:** la vía normal de edición del panel se saltaba el
  candado entero — por ahí entraba un camino activo con el precio escrito adentro. Lo
  probé en vivo contra la instancia de práctica: ahora responde «el camino está activo con
  una cifra escrita en su cuerpo — las cifras viven en el tarifario, jamás en el camino».
- El tablero de pedidos también valida su coherencia al guardar (etapa inicial que exista,
  movimientos entre etapas reales, sin ids repetidos) — antes se guardaba roto con cara de
  éxito y reventaba después, con pedidos atascados.

**Importante:** verifiqué ANTES de encender que las configs reales de tus dos instancias
pasan las reglas nuevas — nada se rompió en vivo. **Commit:** `4920292`.

---

## ✅ Pieza 5 · Lo que se ve, funciona (§8) — TERMINADA y en vivo

**Qué quedó funcionando:** se retiraron del panel las tres perillas que prometían cosas
que ningún código hacía — «Cuándo cuentas la plata», «Proponer darlo por perdido tras» y
«Cada cuánto te insiste». Estaban a la vista en Ajustes y eran mentiras chicas: tocarlas
no cambiaba nada. Donde estaban quedó escrito el porqué, y cada una vuelve el día que
exista su cable. De paso se sinceró el último texto mentiroso: la ayuda de «Avisarte por
WhatsApp» seguía prometiendo responder por WhatsApp con un código — ahora dice lo que es
(una notificación; se responde en el panel).

**Sin sustos:** tus archivos de ajustes viejos traen esas claves y siguen leyéndose igual
(lo desconocido se descarta). Verificado en vivo: el panel ya no sirve esas perillas.

**Commit:** `90e3d1a`.

---

## ✅ Pieza 6 (extra, tras tu OK de la mañana) · E3: la guía de Caminos VIVE

**Qué quedó funcionando:** la caja de la vista Caminos que decía «la guía llega con el
asistente» ahora ES el asistente. Le preguntas por tus caminos en simple («¿qué hace
cam-fuera-de-cobertura?») y te contesta con el catálogo real; le pides un camino nuevo
(«crea un camino para cuando preguntan por el horario») y **lo deja como BORRADOR en tu
cascada, con su prueba de calidad ya escrita en el pool**. Activarlo sigue siendo tuyo,
desde la ficha, pasando el candado — nada que la IA escriba cambia la conducta viva.
Un camino ACTIVO se niega a editarlo («páusalo primero o pídeme una copia»). Todo pasa
por el lint de E2 y deja su punto en «Cambios» como *la IA*.

**Probado en vivo con el cerebro real:** le pregunté por `cam-fuera-de-cobertura` en tu
panel y lo explicó perfecto en 9 segundos, sin tocar nada. 1009 tests en verde.
**Commit:** `7b9072a`.

---

# 🌅 Resumen de la noche (léeme primero)

**Las 5 piezas del encargo quedaron terminadas, probadas y corriendo en los dos paneles:**

1. **«Cambios»** — cada ajuste deja una foto de cómo estaba todo antes; botón «Volver
   aquí» con doble toque; volver también tiene vuelta atrás. *(commit `cd09671`)*
2. **«Precios»** — el tarifario salió de Ajustes y es una vista propia: tabla editable en
   línea, zonas, flete y tarifas especiales. Guardar deja punto en Cambios. *(`7d98c1f`)*
3. **«Traer mi lista»** — pegas tu lista como esté, la IA la ordena y te muestra la
   propuesta; nada se escribe sin tu doble OK. *(`edf289f`)*
4. **Un solo candado** — el lint de caminos existe, las tres vías lo comparten, la puerta
   trasera cerrada, y el embudo ya no se puede guardar roto. *(`4920292`)*
5. **Lo que se ve, funciona** — fuera las 3 perillas muertas del panel y el último texto
   que mentía sobre el aviso por WhatsApp. *(`90e3d1a`)*

**Números:** 1005 pruebas en verde (eran 990 al empezar la noche) · tipos limpios · 6
verificadores del panel OK · ambos paneles reiniciados y sanos tras cada pieza · repo
limpio, cada pieza en su commit.

**Lo que quedó anotado como siguiente paso (no a medias, simplemente siguiente):** subir
la FOTO de un papel a Precios (necesita conectar la visión del cerebro); y del inventario
§8 quedan los enchufes NO visibles en el panel (efectos de pasos, pausa-dueno,
herramientas por paso) — esos son cableado grande, no limpieza de una noche.

**Nada necesita tu decisión urgente.** Siguen pendientes de otras noches: la API key de
respaldo del cerebro (plata, tuya) y publicar el panel 8793 en el túnel para los avisos
push. Las 3 dudas de destaperapido siguen intactas esperándote (no las toqué, como
ordenaste).

**Para probar en 2 minutos cuando despiertes:** abre el panel → «Precios» (mira tu tabla),
cambia un precio y guarda → ve a «Cambios» y mira el punto que quedó → toca «Volver aquí»
y mira cómo se deshace. Esa es toda la historia de la noche en un gesto.
