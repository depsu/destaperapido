# Referencias de diseño para dixdybot: Typebot (vista Caminos) + Intercom Fin (vista Agente)

Extracción de PATRONES (no branding) para un panel minimalista de un agente de ventas IA,
usado por un dueño de negocio no técnico. Fuentes: código real de Typebot
(`apps/builder`, clon en scratchpad) y documentación pública de Intercom Fin (fin.ai +
help center).

---

## 1. TYPEBOT — anatomía de la cascada vertical (vista Caminos)

Código leído: `apps/builder/src/features/graph/components/nodes/{group,block}/*`,
`features/graph/constants.ts`, `packages/ui/src/{theme,colors}.css`.

### 1.1 El grupo: una tarjeta angosta de ancho FIJO

- `groupWidth = 300px` — constante, nunca fluida. La angostura fuerza lectura vertical
  tipo conversación y permite varias columnas en el canvas.
- Tarjeta: `rounded-xl` (12px), borde 1px (`gray-6`), fondo `gray-1` (el fondo de app
  más claro de la escala), `px-4 pt-4 pb-2` (16px lados/arriba, 8px abajo).
- Título del grupo: editable INLINE (componente Editable, click para escribir),
  `font-medium`, sin botón de "editar". Si está vacío, deja una zona de click invisible.
- Estados con UN solo canal visual — el color del borde: normal `gray-6`; hover
  `shadow-md` (sin cambiar borde); seleccionado/conectando/menú abierto = borde
  `orange-8` (accento). Nada de rellenos ni glows.
- Toolbar contextual (play/duplicar/borrar) aparece SOLO con el grupo enfocado,
  flotando encima de la tarjeta (`absolute -top-12.5 right-0`), nunca fija.

### 1.2 El bloque: una fila de icono + preview

- Fila `p-3` (12px), `rounded-lg` (8px), `flex gap-2 items-start`, fondo `gray-2`
  (exactamente un paso más oscuro que la tarjeta madre — jerarquía por un solo paso de
  escala, no por sombras), borde 1px. Altura libre según contenido, mínimo ~44px.
- Anatomía: icono a la izquierda (con `mt-1` para alinear con la primera línea) +
  contenido textual. Sin título de bloque, sin descripciones: el contenido ES el preview
  de su configuración (el placeholder del input, la primera línea del mensaje, la URL).
- Bloque vacío = texto placeholder en `gray-9` al 50% de opacidad. Bloque configurado =
  texto normal. El estado de configuración se lee sin badges.
- Selección: borde 2px `orange-8` con `-m-px` de compensación para que el layout no
  salte. Mismo accento que el grupo.
- **Color del icono codifica la CATEGORÍA del bloque** (semántica fija, no decorativa):
  contenido/burbujas = `gray-12` (neutro), inputs/preguntas = `orange-9` (accento),
  lógica = `purple-9`, integraciones = logo real de la marca. Iconos `stroke-2`.
- Puntos de conexión (endpoints): absolutos fuera de la fila (`left:-34px` /
  `right:-34px`), solo el último bloque del grupo es conectable por defecto.

### 1.3 Edición: inline para texto, popover anclado para opciones

- Texto simple se edita EN EL LUGAR: el bloque se transforma en editor (TextBubbleEditor
  reemplaza a la fila). Cero navegación.
- Bloques con opciones abren un POPOVER anclado al costado del bloque (`side="left"`):
  `p-4`, `min/max-width 400px`, `max-h 60vh`. Expandible con un botón (en una hover-bar
  que aparece ENCIMA del popover solo al pasar el mouse) a casi pantalla completa
  (`available-width - 42px`, `max-h 80vh`). Dos niveles de detalle, mismo anclaje.
- Regla de revelación progresiva resultante: canvas → preview en la fila → popover
  400px → expandido. Nunca una página nueva.

### 1.4 Drag & drop silencioso

- Entre bloques viven placeholders de 4px de alto (padding 2px) invisibles en reposo;
  al arrastrar se expanden a 50px (padding 8px) como zona de drop. La lista no muestra
  ningún "soltar aquí" hasta que hace falta.
- El bloque arrastrado flota en un portal con `rotate(-2deg)` — señal física de
  "levantado" sin sombras dramáticas.

### 1.5 Tokens de tema

- Escalas tipo Radix de 12 pasos por color con roles fijos: 1 = fondo app, 2 = fondo de
  elemento, 6 = borde por defecto (global: `* { border-color: gray-6 }`), 8 =
  borde hover/focus/selección, 9 = sólido/accento, 12 = texto.
- UN solo accento de marca (naranja) para foco, selección y primary; el resto neutro.
- Variables semánticas (`--background, --card, --popover, --border, --primary,
  --muted-foreground...`) redefinidas bajo `.dark` — dark mode sin tocar componentes.
- `--radius: 0.625rem` (10px) base; spacing base 4px; dos familias tipográficas
  (display + sans), el builder usa solo la sans.

---

## 2. INTERCOM FIN — configurar un agente IA sin abrumar (vista Agente)

Fuentes: fin.ai/{train,procedures,testing} y help center de Intercom (artículos de
Guidance, Procedures, versions/publishing, previews, identity, tone of voice).

### 2.1 Arquitectura de la configuración: 4 secciones máximo

Todo el entrenamiento del agente cabe en: **Identidad/Personalidad · Conocimiento
(contenido) · Reglas (guidance) · Procedimientos** (+ escalación/handoff vive dentro de
reglas y como herramienta dentro de procedimientos). Nunca un formulario gigante.

### 2.2 Identidad y tono: presets con UNA línea, no texto libre

- Identidad: nombre + avatar (hover para cambiar) + toggles binarios cada uno con una
  descripción de UNA línea ("Mostrar 'Redactado por IA' en el pie del correo").
- Tono de voz: 5 presets nombrados, cada uno descrito en una línea de tres adjetivos
  ("Amistoso — entusiasta, cálido, alentador"). Largo de respuesta: 3 presets RELATIVOS
  (Conciso = ~30% más corto, Estándar, Extenso = ~30% más largo), default Estándar.
- Cada preset se demuestra con una RESPUESTA DE EJEMPLO lado a lado en el preview, no
  con explicación abstracta. Patrón: elegir > redactar; mostrar > describir.

### 2.3 Guidance (reglas): tarjetas cortas con toggle

- Una regla = título (obligatorio) + texto natural (tope 2.500 chars) + categoría
  (5 fijas: estilo de comunicación, contexto/aclaración, contenido/fuentes, spam, otras)
  + canal + audiencia opcional + **toggle on/off** (apagar sin borrar).
- Botón 💡 "optimizar": la IA revisa la regla buscando ambigüedad, redundancia y
  contradicciones y sugiere la reescritura. Cupo duro: 100 reglas vivas.

### 2.4 Procedures: lista sobria + editor documento

- **Lista**: nombre + badge de estado + canal/audiencia + métricas de uso (frecuencia,
  resolución, escalación). Cinco estados con badge: Draft / Live / Live con draft /
  Paused / Paused con draft.
- **Abierto** (editor tipo documento, no diagrama): título · "cuándo usar esto"
  (256 chars, con ejemplos de entrenamiento e inclusiones/exclusiones) · canvas de pasos
  en lenguaje natural. Herramientas se insertan escribiendo `@` (menú buscable:
  condición IF/ELSE —sin anidar—, llamar API, traspasar a humano, sub-procedimiento,
  terminar con mensaje). Regla de escritura: verbos concretos (preguntar, revisar,
  enviar), un paso = una unidad coherente de acciones, no microescalones.
- **Draft con IA**: el dueño describe su proceso en texto libre (hasta 5.000 chars o
  pega su SOP) → la IA hace preguntas aclaratorias opcionales → genera borrador →
  botones Keep / Clear / Try again. Un "AI reviewer" marca huecos (ramas sin manejar,
  referencias rotas) con sugerencias accionables.

### 2.5 Draft/Live con memoria: nada se rompe editando

- Tres capas SIEMPRE: sin guardar → borrador → vivo. Editar algo vivo jamás toca lo que
  ven los clientes hasta apretar "Publicar cambios".
- Publicar exige un resumen "¿qué cambió?" (50–500 chars) → changelog automático.
- Historial de versiones en side panel; rollback restaura una versión anterior COMO
  BORRADOR (segunda confirmación antes de vivir). Solo se registran versiones que
  estuvieron vivas.

### 2.6 Preview omnipresente

- Panel lateral de preview disponible desde CUALQUIER pantalla de configuración:
  simulador de chat (lo que ve el cliente) + pestaña "Event log" (por qué: qué regla,
  qué personalidad, qué procedimiento aplicó). Confianza por transparencia.
- Refleja borradores sin guardar al instante. Dropdown "Testing as" para impersonar un
  cliente o audiencia. Toggle chat/email para ver el formato por canal.

---

## 3. Síntesis: anatomía propuesta para dixdybot

**Vista Caminos** = canvas con tarjetas de 300px de ancho fijo (grupo = etapa del
camino de venta), cada una con título editable inline y una pila de filas-bloque
(icono coloreado por categoría + preview de una línea de su contenido). Detalle SOLO al
click, en popover de 400px anclado al bloque, expandible. Estados por color de borde
(1 accento), placeholders de 4px→50px para reordenar.

**Vista Agente** = 4 secciones (personalidad · conocimiento · reglas · procedimientos).
Personalidad con presets de una línea demostrados con respuesta de ejemplo; reglas como
tarjetas título+toggle; procedimientos como lista con badge de estado y editor tipo
documento con `@`-herramientas y "borrador con IA" (describe tu proceso → Keep/Clear/
Try again). Draft/live en todo lo público, publicar pide "¿qué cambió?", y un preview
lateral con chat + "por qué" visible desde cualquier pantalla.
