# Regresión del teléfono — veredicto del juez visual

**Fecha:** 2026-07-25 · **Juez:** sesión de verificación independiente (no arregló el teléfono).
**Panel medido:** `http://127.0.0.1:8793` tras `launchctl kickstart -k gui/501/com.dixdy.dixdybot-panel` (200 OK).
**Archivos medidos (huella al cierre):**

| archivo | md5 |
| --- | --- |
| `panel/pwa/app.js` | `7a90f6c54ed094464093e50fde3b37de` |
| `panel/pwa/index.html` | `4f6c7ca5b4b37fd23b7231e5682bd000` |
| `panel/pwa/tokens.css` | `a7e0f4214a1be354a8ee6c7fa590b0a3` |

---

## 0. Cómo se midió (y por qué NO se comparó contra las fotos de `visual-nuevo/`)

La consigna pedía comparar contra `/…/scratchpad/visual-nuevo/`. **Esa comparación no sirve, y hay
que decirlo:** las fotos son de las 10:36 y **la base de datos del cliente cambió a las 10:41**
(`bot.db` mtime 10:41, `migrar-huerfanos.jsonl` 10:42). El panel pasó de 108 chats a 98, de $2,4M a
$5,3M, de "2 sin monto" a "1 sin monto", y apareció una decisión pendiente que antes no estaba. Un
diff de píxeles contra esas fotos mide el cambio de DATOS, no el cambio de código: da 114.620
píxeles distintos en Hoy y no prueba nada.

Lo que se hizo en su lugar, que es más estricto:

1. Se sacó del commit `HEAD` la copia **pre-tanda** de `index.html`, `tokens.css` y `app.js`
   (verificado: el `app.js` de `HEAD` es byte a byte el respaldo `kb-backup/app.js` que el propio
   agente 2 guardó a las 10:59 antes de tocar nada).
2. Se sirvió esa copia en el puerto **8899** con un proxy que reenvía `/api/*` **al panel vivo del
   8793**. Así el "antes" y el "después" leen **exactamente los mismos datos, en el mismo minuto**.
3. Se compararon las dos versiones de dos maneras: **huella de cajas** (etiqueta + clase + x,y,w,h
   de CADA elemento visible del `.shell`, con 2 decimales) y **diff de píxeles** de la captura.

También hay que decir que **los archivos siguieron cambiando durante la revisión** (había un tercer
agente trabajando: `index.html` cambió a las 11:38, `tokens.css` a las 11:43). Todas las cifras de
este informe son de la pasada final, con los archivos ya quietos (verificado 40 s seguidos sin
cambio) y con los md5 de arriba.

---

## 1. LA PREGUNTA PRINCIPAL: ¿se rompió el escritorio?

# NO. El escritorio no se movió ni un píxel de sitio.

**Huella de cajas — antes vs. después, mismos datos, mismo minuto:**

| vista | 1440 × 900 | 1024 × 768 |
| --- | --- | --- |
| hoy | ✅ misma geometría (76 cajas) | ✅ misma geometría (76 cajas) |
| chats | ✅ misma geometría (802 cajas) | ✅ misma geometría (802 cajas) |
| caminos | ✅ misma geometría (95 cajas) | ✅ misma geometría (95 cajas) |
| modulos | ✅ misma geometría (157 cajas) | ✅ misma geometría (157 cajas) |
| agentes | ✅ misma geometría (114 cajas) | ✅ misma geometría (114 cajas) |
| diseno | ✅ misma geometría (656 cajas) | ✅ misma geometría (656 cajas) |

Cero cajas sólo-antes, cero cajas sólo-después, en las 12 celdas. Los 4 elementos nuevos del
`index.html` (2 checkbox ocultos + 2 barras «← volver») miden 0×0 en escritorio: no existen para el
diseño.

**Diff de píxeles — antes vs. después:**

| vista | 1440 | 1024 | qué es |
| --- | --- | --- | --- |
| hoy | 36 px (máx 16/255) | 36 px (máx 16/255) | dientes de sierra del icono «Diseño» y del punto del pie |
| chats | 24.377 px (máx 19/255) | 5.241 px (máx 19/255) | **el composer apagado** — el arreglo pedido |
| caminos | 73.190 px (máx 217/255) | 73.190 px (máx 217/255) | **el botón «Preguntar» apagado** — el arreglo pedido |
| modulos | 1 px (máx 1/255) | 0 px | ruido invisible |
| agentes | 0 px | 0 px | idénticas |
| diseno | 42 px (máx 1/255) | 0 px | ruido invisible (sale igual comparando la MISMA versión consigo misma) |

**Los dos bloques grandes son exactamente lo que se pidió arreglar (defecto 6):** el botón
«Preguntar» era verde sólido y no hacía nada; ahora es gris. El composer de Chats, igual. Se
verificó recortando y mirando: la caja es idéntica al píxel, sólo cambia el color. Eso no es
romper el escritorio, es el encargo.

**Los 36 píxeles de Hoy/agentes SÍ son reales y NO los declaró nadie.** Se cazó la causa
experimentalmente: al `index.html` de antes se le inyectó **sólo** un `<input type="checkbox" hidden>`
y el diff pasó a ser idéntico al de la versión nueva (36 px, misma caja). Es decir: la mera
presencia de un control de formulario en la página cambia cómo el navegador suaviza los bordes de
dos círculos del menú lateral (el icono «Diseño» y el punto de estado, ambos de 8-24 px). Fondo y
relleno idénticos; sólo el borde antialiado, con 16/255 de diferencia máxima. **Es invisible al
ojo, no mueve nada y no es corregible desde el CSS** — pero la frase del agente 1, "NI UN PÍXEL
movido", es literalmente falsa: son 36 píxeles de suavizado. La geometría, que es lo que importa,
sí está intacta.

---

## 2. Tabla ancho × vista: ¿algún contenedor mide más que su hueco?

Medido con `getBoundingClientRect()` sobre **todos** los elementos de la vista activa (la prueba del
scroll del body no sirve: `body` lleva `overflow:hidden` en `tokens.css:47` y siempre da igual).
El número es el borde derecho más lejano que alcanza cualquier elemento.

| vista | 320 (iPhone SE) | 390 (iPhone) | 768 (tablet) | 1024 | 1440 |
| --- | --- | --- | --- | --- | --- |
| hoy | ✅ 320 | ✅ 390 | ✅ 768 | ✅ igual que antes | ✅ igual que antes |
| chats | ✅ 320 | ✅ 390 | ✅ 768 | ✅ igual que antes | ✅ igual que antes |
| caminos | ✅ 320 † | ✅ 390 | ✅ 768 | ✅ igual que antes | ✅ igual que antes |
| modulos | ✅ 320 | ✅ 390 | ✅ 768 | ✅ igual que antes | ✅ igual que antes |
| agentes | ✅ 320 | ✅ 390 | ✅ 768 | ✅ igual que antes | ✅ igual que antes |
| diseno | ✅ 320 † | ✅ 390 † | ✅ 768 | ✅ igual que antes | ✅ igual que antes |

† corregido por este juez (ver §4). **18 de 18 celdas del teléfono/tablet: nada se sale.**

**De dónde venía (medido en la copia pre-tanda, mismos datos):** a 390 desbordaban 5 de 6 vistas —
hoy 432, chats 416, caminos 454, agentes 688, diseño 984. Los dos números que el agente 1 corrigió
a la base (agentes 688 en vez de 424, caminos 454 en vez de 424) **son correctos**: los verifiqué.
La base los tenía mal.

**A 320 nadie había mirado nunca**, y el estado pre-tanda era peor: hoy 432, chats 416, caminos 454,
agentes 688, diseño 984 (los mismos, porque el desborde no dependía del ancho).

---

## 3. Los 8 puntos del encargo, uno por uno

| # | qué se pidió | 390 | 320 | veredicto |
| --- | --- | --- | --- | --- |
| 1 | nada más ancho que su hueco | ✅ | ✅ | pasa (con la corrección de §4) |
| 2 | la cuarta métrica de Hoy se ve | ✅ x72 y145 | ✅ x165 y145 | pasa — se envuelve a segunda fila, entera y dentro |
| 3 | abrir un chat, leerlo y **volver** | ✅ | ✅ | pasa — camino completo recorrido |
| 4 | nota del juez y gate en Agentes | ✅ | ✅ | pasa — «Gate de calidad · nota — · mínimo 4 para atender clientes», 0 desbordes |
| 5 | el chip «sin monto» abre, cierra y lleva al chat | ✅ | ✅ | pasa |
| 6 | los apagados se distinguen, claro y oscuro | ✅ | ✅ | pasa |
| 7 | teclado en Caminos | ✅ | — | pasa |
| 8 | consola en cero | ✅ | ✅ | pasa — 0 mensajes |

**Detalle de los que tenían trampa:**

**3 · Chats, el camino completo.** Lista (98 filas) → toco una fila → el hilo ocupa los 334 px (264
en el SE) con sus 59 burbujas y la barra «← Chats» arriba → toco la barra → vuelvo a la lista.
Probado también **desde el chip de Hoy** y **desde el Tablero**: los dos abren el hilo directamente
en la capa correcta. Ojo: la "limitación honesta" que declaró el agente 1 (que abrir un chat desde
Hoy o el Tablero te dejaba en la lista) **ya no existe** — `app.js` tiene `capaTelefono()` y la
llama en `abrirChat` y en el cambio a Tablero. Alguien la tapó después de que él escribiera su
informe.

**5 · El chip.** Hoy dice "1 sin monto" (los datos cambiaron, ya no son 2). Abre un diálogo real
(`role=dialog`, `aria-modal`), el foco entra, **Escape lo cierra y el foco vuelve al chip**, y
«ver chat» te deja en el hilo de Alejandro con la lista ya replegada. Igual a 320.

**6 · Apagados.** Medido el color calculado, no de vista:

| | claro | oscuro |
| --- | --- | --- |
| botón apagado | fondo `rgb(231,235,233)` · letra `rgb(105,118,111)` | fondo `rgb(31,37,35)` · letra `rgb(124,137,131)` |
| contraste de su letra | 3,95:1 | 4,28:1 |
| botón vivo al lado | verde `rgb(14,122,95)` con letra blanca | verde `rgb(59,199,150)` |

La trampa del tema oscuro que declaró el agente 1 **está realmente arreglada**: la letra del
apagado es gris legible, no casi negra. La vista Diseño muestra los dos ejemplos apagados
("Todavía no", "Sin permiso"), el interruptor bloqueado, y ofrece la tercera clase copiable
`btn[disabled]`. **Ya no dice que le falte el estado apagado** (queda un "Le falta al sistema · 1
campo de texto suelto", que es otro hueco distinto y legítimo).

**7 · Teclado en Caminos.** Las 3 tarjetas `.bloque` tienen `role="button"`, `tabindex="0"` y
nombre. Tab llega a las tres. **Enter** abre el camino; **Espacio** también y **no desplaza la
página** (`scrollY` 0). El flotante de revisión en lote: **0 fugas de foco en 20 tabuladores**,
Escape lo cierra y el foco vuelve a `#chip-borrador`. Correcciones a la base confirmadas: `#in-guia`
y `#btn-guia` están `disabled` y no reciben foco, así que la cuenta de paradas de la base estaba mal.

**8 · Consola.** Cero mensajes en la pasada final (las 6 vistas, los dos anchos, abriendo chats,
flotantes y el peek). Los dos `ERR_CONNECTION_REFUSED` que aparecen en el registro son del segundo
en que el panel estaba reiniciándose, no del código.

**Extra · avatares (defecto 8).** 98 avatares servidos, **0 rotos**. Los nombres que empiezan con
emoji muestran la letra ("🏋️ Práctica libre" → "P") y el chat que se llama sólo "☺️😉😁😊" muestra
el ☺️ completo con su modificador (`263a fe0f`), no partido. La decisión de cortar por grafema
funciona.

---

## 4. Lo que arreglé yo (2 reglas, sólo `panel/pwa/tokens.css`, dentro del `@media ≤700px`)

Ninguno de los dos es un roto NUEVO de esta tanda: son **restos del defecto viejo que el arreglo no
alcanzó a cubrir en 320 px**, un ancho que nadie había probado. Los dos viven dentro del bloque del
teléfono, así que **no pueden tocar el escritorio** — y se volvió a comprobar después (§1: la
huella de cajas y el diff de píxeles se midieron con estas reglas ya puestas).

**a) La cascada de Caminos se salía 30 px en el SE.**
`.cascada-grid` pedía columnas de `minmax(280px,1fr)`; en 320 el hueco real es 236, así que la
tarjeta medía 280 y el borde derecho quedaba **recortado y sin manera de alcanzarlo** (con
`body{overflow:hidden}` no hay barra que lo rescate). Misma cura que ya se le había hecho a
`.specs`:

```css
.cascada-grid { grid-template-columns:minmax(0,1fr); }
.grupo-c, .bloque { min-width:0; }
```

Caminos a 320: 350 → **320**. Diseño (que dibuja una cascada de ejemplo): 366 → 356.

**b) El campo y el composer de EJEMPLO del catálogo se salían 36 px.**
Dentro de `.spec .demo` llevan `flex:none` (correcto en la vista real, donde mandan ellos), pero de
ejemplo se negaban a encoger:

```css
.spec .demo .composer, .spec .demo .g-input { flex:1 1 auto; min-width:0; }
```

Diseño a 320: 356 → **320**. Y de paso arregla los 6 px que se cortaban a 390.

---

## 5. Lo que queda roto (NO es de esta tanda, y no lo toqué)

**La tarjeta de decisión de Hoy es ilegible en un iPhone SE (320).** La carta es una fila:
avatar (32) + texto + botón «Ver chat» (76). El botón no encoge, así que al texto le quedan
**64 px** — unas cinco letras por línea, 39 líneas para un párrafo.

| | ancho de la columna de texto | alto del párrafo |
| --- | --- | --- |
| 320, antes de la tanda | 32 px | 1131 px |
| 320, ahora | 64 px | 761 px |
| 390, ahora | 134 px | 332 px (se lee bien) |

O sea: **la tanda lo mejoró al doble, pero sigue sin leerse a 320.** No lo arreglé porque no es un
roto nuevo y porque la cura cambia también el dibujo a 390 (el botón se iría a su propia línea), y
eso ya es decisión de diseño. Si Alejandro lo quiere, son dos líneas dentro del `≤700px`:

```css
.decision { flex-wrap:wrap; }
.decision .cuerpo { flex:1 1 180px; }
```

---

## 6. Verificación final

- `npx tsc --noEmit` → **limpio** (salida vacía, código 0).
- `npx vitest run` → **39 archivos, 612 pruebas, todo verde** (3,12 s).
  Los agentes reportaron 38/592; el número creció porque siguió entrando trabajo de un tercer
  agente mientras se revisaba. Con los archivos ya quietos, verde entero.
- Consola del navegador: **0 mensajes**.
- Navegador dejado en Hoy, sin flotantes abiertos, sin tema forzado.

## 7. Fallos de puntería de los informes (para no repetirlos)

1. **"NI UN PÍXEL movido"** (agente 1) y **"0 píxeles de diferencia en escritorio"** (agente 2): no
   es literal. Son 36 px de suavizado en dos círculos del menú, causados por meter un `<input>` en
   la página. Invisibles, pero medibles. La afirmación correcta es la que sí se sostiene: **misma
   geometría, caja por caja, en las 2.000 cajas de las 6 vistas**.
2. **La "limitación honesta" del agente 1 ya no aplica** — otro agente la tapó con `capaTelefono()`.
   Los informes envejecen en horas cuando hay tres manos sobre los mismos archivos.
3. **Nadie probó 320.** Dos vistas seguían saliéndose y una tarjeta sigue sin leerse. 390 no es el
   piso: el iPhone SE existe.
4. **Nadie avisó de que los datos cambiaron a las 10:41.** Cualquier comparación visual contra las
   fotos de las 10:36 iba a mentir; conviene fechar y congelar los datos antes de fotografiar.
