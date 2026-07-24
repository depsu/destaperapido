# Informe de patrones: LINEAR (linear.app) → panel dixdybot

Fuentes: medición directa con Playwright sobre la app real en vivo (sesión linear.app/dixdy,
tema claro) y el sitio público (tema oscuro), más el artículo oficial del rediseño
("How we redesigned the Linear UI"). Los valores en px son estilos computados reales, no
estimaciones. Objetivo: extraer PATRONES (no branding) para un panel de administración
minimalista usado por un dueño de negocio no técnico.

## a) Gramática del shell

- **Chrome en "L invertida"**: sidebar izquierdo + banda superior; todo lo demás es contenido.
  Linear lo declara explícitamente en su rediseño: el chrome se rebaja, el contenido manda.
- **Sidebar: 244 px** (medido). Sin borde derecho visible (`border-right: 0`): la separación
  la hace el COLOR, no una línea — sidebar `lch(95.94% 0.5 282)` vs área base
  `lch(98.94% 0.5 282)`; el contenido es ~3 puntos de luminosidad más claro y se lee como
  panel elevado.
- **Items del sidebar: 28 px de alto, border-radius 8 px, label 13 px / weight 500**,
  color secundario `lch(38.4 1.25 282)` (medido). Icono + texto, nada más: sin descripciones.
  Los contadores (Inbox **1**) son un número desnudo al final de la fila, sin chip.
- **Encabezados de sección del sidebar: 12 px / 500, 15 px de alto**, mismo gris secundario,
  sin uppercase (medido: `text-transform: none`). Agrupan: Workspace / equipos / extras.
- **Header de vista: 44 px de alto**, borde inferior hairline `1px solid lch(96.24 0 282)`
  (medido). Contenido: solo el título de la vista (breadcrumb corto) a la izquierda y
  controles de filtro/display a la derecha. Nunca hay "hero" ni subtítulos dentro de la app.
- **Marketing header** (referencia de barra superior): 73 px, `position: fixed`, fondo
  transparente + `backdrop-filter: blur(20px)`, borde inferior `1px solid rgba(255,255,255,0.08)`.

## b) Densidad y tipografía

- **Fuente: Inter Variable** en todo (medido). El rediseño añadió Inter Display solo para
  titulares de marketing. Clave: usan **pesos intermedios de fuente variable — 450, 510, 550 —**
  en vez de saltar de 400 a 700; así logran jerarquía sin ennegrecer la UI.
- **Censo tipográfico real de la app** (frecuencia de font-size/weight computados):
  `12px/500` domina, luego `12px/450`, `13px/500`, `11px/400`, `14px/550`, `16px/400`.
  Es decir: **la UI vive entre 11 y 14 px**; 13 px para labels de navegación y filas,
  12 px para metadatos, 11 px para lo terciario, 14-16 px solo para títulos de vista.
- **Alturas**: fila de navegación 28 px; header de vista 44 px. La densidad viene de filas
  bajas + tipografía pequeña + line-height apretado, no de quitar padding lateral.
- Marketing: H1 64 px con weight 510, letter-spacing −1.4 px (−2.2%), line-height 1.0 —
  el patrón "titular grande, peso medio, tracking negativo".

## c) Color: rico con paleta casi neutra

- **Sistema LCH con 3 variables por tema** (artículo oficial): color base, color de acento y
  contraste; de ahí se GENERAN las ~98 variables del tema. Los neutros llevan un susurro de
  croma (0.5–1.25 en LCH, matiz 282 = azul-violeta) — por eso el gris de Linear se ve "caro"
  y no plomo puro.
- **Tokens reales medidos (tema claro)**: fondo base `lch(98.94% 0.5 282)`, sidebar
  `lch(95.94% 0.5 282)`, borde `lch(89.49% 0 282)`, texto primario `lch(9.89 0 282)`,
  texto secundario `lch(38.4 1.25 282)`. Tema oscuro (sitio): fondo `#08090A`, texto
  `#F7F8F8`, secundario `#8A8F98`.
- **El acento vive en casi nada**: selección activa, focus, botón primario y links; el resto
  es escala de grises. El estado se marca con **iconos-punto de 12-14 px con color semántico**
  (círculo de progreso naranja = en curso, verde = hecho, prioridad como icono de barras),
  nunca con chips de texto grandes ni fondos de fila coloreados.
- **Hairline > sombra**: bordes de 1 px a ~90% de luminosidad (o `rgba(255,255,255,0.08)` en
  oscuro) para separar; las sombras se reservan para capas flotantes (popovers, command menu,
  modales). Las superficies planas jamás llevan sombra.

## d) Revelación progresiva

- **La fila muestra ~6 átomos**: prioridad (icono), ID corto, punto de estado, título (única
  palabra con peso), 0-2 labels y avatar + fecha a la derecha. TODO lo demás (descripción,
  actividad, sub-issues) vive al abrir, en vista dividida o completa.
- **Empty state mínimo** (medido en vivo): una línea gris ("No issues assigned to you") +
  un solo botón + el atajo como pista: "Go to my issues **G** then **M**". El atajo de
  teclado es decoración funcional: chips `kbd` diminutos en tooltips, menús y estados vacíos.
- **Todo tiene tooltip con su atajo**; los menús contextuales listan la acción a la izquierda
  y el atajo a la derecha en gris terciario.
- La navegación completa se opera por teclado (G+M, Cmd+K); la app entera navegó por atajos
  durante la medición — hasta Settings se abre así.

## e) Microinteracciones sobrias

- **Hover = cambio de fondo sutil** (un paso de luminosidad, mismo radio de 8 px del item),
  nunca borde nuevo ni sombra ni movimiento.
- **Cmd+K command menu** como techo de la interacción: un solo campo que busca/ejecuta todo;
  permite que la UI visible quede mínima porque lo raro se busca, no se muestra.
- Transiciones cortas (~100-150 ms) solo en opacidad/fondo; los cambios de datos son
  optimistas e instantáneos — la velocidad ES la estética.
- Pastilla/botón de marketing: radius 9999 px, texto 13 px; en la app los radios son 8 px
  (items) y 4-6 px (controles pequeños).

## Las 10 reglas Linear para dixdybot

1. **Shell en L invertida**: sidebar de ~240 px + header de vista de 44 px; el resto es
   contenido. Cero heros, cero subtítulos dentro del panel.
2. **Separar con color, no con líneas**: sidebar 3 puntos de luminosidad más oscuro que el
   contenido; borde derecho 0. Hairlines de 1 px (~90% L) solo donde haya lista o header.
3. **Escala tipográfica 11/12/13/14**: 13 px labels y filas, 12 px metadatos, 11 px terciario,
   14-16 px títulos de vista. Una sola fuente variable (Inter) con pesos 450/500/550 — nunca 700.
4. **Filas de 28-36 px**: navegación 28 px con radius 8 px; filas de datos ≤ 40 px. Un icono
   (14-16 px), un título, metadatos grises, contador como número desnudo.
5. **Tema = 3 variables LCH** (base, acento, contraste) y generar el resto; neutros con
   croma 0.5-1.25 para que el gris se vea rico. Oscuro: fondo #08090A, no negro puro.
6. **El acento en un solo lugar por vista** (activo/CTA); estado siempre como punto/icono de
   12-14 px con color semántico, jamás chips grandes ni filas coloreadas.
7. **Sombra solo a lo que flota** (menús, modales, Cmd+K); superficies planas con hairline o
   diferencia de fondo.
8. **Fila = 6 átomos máximo**; el detalle se abre (split o vista completa), no se apila en la
   fila. Tooltip para todo icono sin texto.
9. **Empty state de una línea gris + un botón + el atajo como pista**; el atajo (`kbd` chip)
   es la única "decoración" permitida.
10. **Hover = un paso de fondo, 100-150 ms, sin mover nada**; y un buscador global tipo Cmd+K
    para que lo infrecuente se busque en vez de ocupar UI.
