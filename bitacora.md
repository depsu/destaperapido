# Bitácora de destaperapido

Relato en simple de lo que las rondas y sesiones de la IA hacen por este cliente
(lo nuevo ARRIBA). Las propuestas accionables viven en la cola del dashboard (🎯 Tareas);
aquí queda la historia. La escriben ronda-ads, ronda-correo y las sesiones.

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
