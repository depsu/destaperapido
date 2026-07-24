# Bitácora de destaperapido

Relato en simple de lo que las rondas y sesiones de la IA hacen por este cliente
(lo nuevo ARRIBA). Las propuestas accionables viven en la cola del dashboard (🎯 Tareas);
aquí queda la historia. La escriben ronda-ads, ronda-correo y las sesiones.

---

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
