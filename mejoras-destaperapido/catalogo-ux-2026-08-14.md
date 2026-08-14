# Catálogo UX del panel dixdybot — noche del 14-ago-2026

Objetivo de Alejandro: «listado extenso de mejoras de experiencia de usuario, como lo
hacen las mejores empresas del mercado, mínimo 100, aplicarlas, testearlas, simularlas
en navegador real y en móvil». Método: 8 cazadores de IA leyendo el código real con
lentes de WhatsApp Web, Superhuman, Linear, Stripe, Trello/Pipedrive, Apple HIG,
GOV.UK y Telegram → 172 mejoras crudas → dedup → **133 aplicadas** la primera noche
y **149 con la tanda T9** de la mañana siguiente, en 10 commits
(69d9567 → d64b482), sobre el rediseño previo de la misma noche (97910e6: lista única,
morado, monto/etapa). Cada tanda pasó: `tsc`, vitest (1143 tests), los 4
`_probar-*.cjs`, `_sellar.mjs`, y al final validación en Chrome real (1440×900 y
390×844, consola en cero). Las dos instancias vivas reiniciadas y verificadas
(Baileys conectado, salud ok).

## Aplicadas por tanda (commit · qué trae)

**T1 · Lista de chats — 69d9567 (19)**
1 buscador con X y Escape · 2 pegajoso al scroll (busc-zona) · 3 contador «N chats
calzan» · 4 término resaltado sin acentos (.hl) · 5 dormidos que calzan se abren al
buscar · 6 vacío-búsqueda con «Borrar la búsqueda» · 7 vacío-filtro con «Ver todos los
bots» · 8 vacío-estreno con «Abrir el simulador» · 9 esqueleto de primera carga ·
10 fila nueva entra con toque verde · 11 reorden deslizado (FLIP a mano, ≤40 filas) ·
12 fila del chat abierto siempre a la vista · 13 teclado completo (↓ desde buscador,
↑↓/j/k/Home/End, Enter abre, Escape vuelve) · 14 nombres largos ceden con «…» ·
15 el latido no cierra el select de bots · 16 los «ayer» amanecen bien a medianoche ·
17 avatares lazy con fundido · 18 filtro de bot persistente (y se suelta si el bot ya
no existe) · 19 acción rápida «Ver la ficha» al hover + separadores de tiempo en lista
larga.

**T2 · Hilo y composer — 21e3e56 (18)**
20 «bajar al final» flotante con globo de nuevos · 21 borradores por chat (cierra el
P0: lo escrito para A jamás a B) + «Borrador:» en la fila · 22 composer que crece
hasta 5 líneas · 23 Enviar se enciende y pinta con el acento solo con texto · 24 Enter
táctil = salto de línea (envío = botón) · 25 visor de fotos a pantalla completa con
flechas/contador/caption · 26 copiar cualquier burbuja al hover · 27 hora con fecha
completa al hover en agrupadas · 28 píldora del día pegajosa · 29 velocidad
1×/1,5×/2× recordada en notas de voz · 30 reproducción encadenada · 31 foto rota con
Reintentar · 32 franja de envío fallido con reintento · 33 scroll recordado por chat ·
34 separador morado «Desde aquí es nuevo» · 35 chip «canal caído» → Conexiones ·
36 búsqueda DENTRO de la conversación (contador «3 de 12») · 37 hilos de 300 mensajes
abren al tiro (content-visibility).

**T3 · Navegación y teclado — 7641803 (19)**
38 paleta ⌘K (vistas + acciones + chats por nombre) · 39 atajos g+letra · 40 «/» al
buscador desde cualquier vista · 41 «?» = mapa de atajos (.kbd) · 42 Escape en pila
única (capa por capa) · 43 atrás/adelante del navegador navegan (?v= compartible) ·
44 atrás del sistema cierra la capa en el teléfono · 45 título de pestaña «(2) Chats ·
negocio» · 46 favicon con punto morado · 47 insignias que laten cada 60 s ·
48 banda «Sin conexión…/¡Volvió!» con histéresis · 49 re-click en vista activa = ir
arriba · 50 memoria Lista/Tablero · 51 memoria del filtro + último chat en escritorio ·
52 scroll recordado por vista · 53 el foco viaja con la navegación (aria-label por
sección) · 54 tooltips con su atajo · 55 tooltips también con teclado (focus-visible) ·
56 Enter en buscador abre el primero.

**T4 · Formularios y Precios — 666a8ae (19)**
57 Guardar nace apagado (sucio real) · 58 Descartar · 59 contador «N ajustes
cambiados» · 60 Guardando… → ✓ Guardado verde · 61 toast con Deshacer (re-PUT) ·
62 validación en línea con foco y mensaje humano · 63 JSON avisa mientras escribes ·
64 anillo de foco en switches · 65 ⌘S guarda lo visible · 66 buscador de ajustes con
vacío y sugerencias · 67 la búsqueda aterriza EN el campo (destello, abre Ajustes
finos) · 68 apagar módulo dice su consecuencia + «Volver a prender» · 69 borradores
sobreviven al navegar + aviso · 70 beforeunload con cambios · 71 steppers −/+ en
rangos cortos (44px táctil) · 72 ayudas largas con «ver más» · 73 Precios: celda mala
roja + foco · 74 eco vivo del IVA por celda + aria-label por celda · 75 quitar zona =
tachado con Deshacer (nada se borra hasta guardar) + ✓/Deshacer al guardar precios.

**T5 · Hoy y tablero — 7f60ad4 (16)**
76 cifras con tween y destello al cambiar · 77 Hoy late cada 8 s (frenos: duda
abierta/foco en cotización) · 78 métricas tocables con destino · 79 barra «En juego:
$14,5M en 92 pedidos» · 80 plata por columna en su piso (verde al cobrar) ·
81 columnas plegables con memoria · 82 orden recientes ⇄ más plata · 83 ARRASTRE con
mouse (destinos válidos iluminados, Escape cancela; plata arma doble-toque) ·
84 doble-toque que dice el monto («Confirmar $180mil ganados») · 85 deshacer al mover
(solo si el embudo declara la vuelta) · 86 confeti sobrio al cobrar · 87 rechazo del
motor EN la tarjeta + «abrir el chat y completarlo» · 88 latido del tablero con
destello en lo que cambió · 89 esqueleto de carga · 90 vacío que enseña cómo llega el
primer pedido · 91 snap de una columna en el teléfono + paginador.

**T6 · Móvil — 7090292 (19)**
92 swipe-back desde el borde (hilo/ficha/agente) · 93 pull-to-refresh (lista y Hoy) ·
94 teclado que no tapa el composer (visualViewport) ni deja la barra flotando ·
95 visor con doble-toque zoom + deslizar-abajo cierra · 96 toast sobre la barra
inferior · 97 peek con safe-areas del notch · 98 targets ≥44px (volver 48px, chip con
aura) · 99 touch-action:manipulation (adiós zoom del doble-toque de plata) ·
100 overscroll-behavior:contain (el rebote no recarga) · 101 badges con número solo
donde avisan · 102 bordes de la barra que se desvanecen («sigue al lado») ·
103 pestaña activa centrada sola · 104 PNG 180 para iOS (adiós miniatura trucha) ·
105 maskable para Android · 106 theme-color por tema + status bar translúcida ·
107 atajos del icono (Hoy/Chats/Simulador) · 108 setAppBadge (el «3» sobre el icono) ·
109 compartir la ficha por la hoja nativa · 110 vibración sutil en enviar/mover/armar
plata + copiar con fallback quieto y seleccionado.

**T7 · Accesibilidad y rendimiento — c1831f6 (19)**
111 toast con voz (role=status), que envuelve y dura según el largo · 112 hilo
role=log + aria-busy al volcarse · 113 región viva «Te escribió Marcela» / «Tu bot te
preguntó algo nuevo» · 114 fila con nombre accesible completo (el morado no viaja
solo en color) · 115 ✓✓ con texto para lectores · 116 «Saltar al contenido» ·
117 el foco entra a la capa que se abre · 118 guía como diálogo (Escape, foco de
vuelta, globito con teclado) · 119 punto de salud rojo + aria cuando cae ·
120 switches con nombre, aria-pressed, aria-current, «Hoy — 3 esperándote» ·
121 menú de estado con foco/flechas/Escape (APG) · 122 prefers-contrast:more ·
123 rótulos de grupo pasan AA medido · 124 envío optimista (burbuja al tiro con
reloj; si falla, el texto vuelve) · 125 esqueleto de Hoy sin salto de hero ·
126 revalidación al volver a la pestaña · 127 scroll suave respeta reduced-motion
también desde JS · 128 fotos fijan su ratio real (cero salto) + techo 55vh ·
129 fallback de copiar en flotante seleccionable.

**T8 · Con servidor — 51616da-zona (4)** *(commit «panel/servidor…»)*
130 tira de PROGRAMADOS en el hilo («⏱ Sale mañana a las 08:30…» + Cancelar) ·
131 botón ARCHIVAR la duda a medias (doble toque, sin enviar nada al cliente) ·
132 numerito verde de WhatsApp por fila (noleidoN nuevo en /api/chats) · 133 «Ver los
58 que faltan» en dormidos (?dormidos=todos).

**Remates de la validación — d64b482**: el JSON histórico del hilo plegado en nota
discreta; badges neutros silenciados en la barra móvil. Más los del rediseño base de
la misma noche (97910e6): lista única con morado, monto/etapa/nuevo por fila, la
pregunta de la duda como preview, previews humanizadas en el servidor, sidebar en
3 bloques, ajustes chats_monto/chats_etapa.

**T9 · Las diferidas, aplicadas — mañana del 14-ago (16)** *(pedido de Alejandro:
«aplica las mejoras pendientes»; mapa previo con 3 lectores de IA sobre el código real)*
134 snippet FTS en la búsqueda (el PORQUÉ del resultado: «…Limpia Fosas y ⟦Destape⟧…»
resaltado; marcadores ⟦ ⟧ que un cliente no tipea, escapado en el front) · 135 «vs
ayer» + chispa de 7 días bajo cada contador con historia (declarado en
CONSULTAS_POR_FECHA: solo métricas re-resolvibles por fecha; caché de días cerrados;
fix: entregasHoy ahora corta el día con tope superior) · 136 el hero SE ABRE («ver los
40»: cada pedido que compone la cifra, tocable a su chat — desglose en ValorMetrica) ·
137 pedido ESTANCADO (limite_horas de la etapa viaja en tableroPanel + actualizadoTs
por tarjeta → punto ámbar con «sin moverse hace X» y chip «N estancados» en la barra) ·
138 mandar FOTO desde el panel (clip en el composer → /enviar-foto multipart, archivo
guardado como los entrantes, MISMO mensajero: topes anti-ban, ritmo, acuses;
PedidoEnvio.media + rama enviarMedia; una foto fallida NO se reencola — la cola es
solo-texto) · 139 REINTENTAR el saliente fallido (del bot o tuyo) en su burbuja
(/reenviar/:mensajeId reusa la fila: los ✓✓ llegan al mensaje de siempre; jamás
duplica lo que sí llegó) · 140 barra inferior de 4 + hoja «MÁS» (iOS tab bar: Hoy,
Chats, Precios, Conexión; el resto sube en bottom sheet armada de la propia barra) ·
141 escala tipográfica EN REM (la letra del sistema del dueño por fin se respeta — la
deuda de accesibilidad) · 142 caché de chats visitados (stale-while-revalidate: abre
al tiro, lo fresco repinta solo si difiere; el latido mantiene la caché) · 143 diff
«¿Qué cambié?» antes de guardar (viejo → nuevo en cristiano, con las etiquetas del
panel) · 144 barra de guardado PEGAJOSA multi-módulo («Cambios sin guardar en 2
módulos», guarda en serie con corte limpio si uno falla) · 145 importador de precios
con DIFF (casa zonas por nombre, «100 antes 90» por celda, chip nueva, tus zonas no
mencionadas se CONSERVAN con checkbox — usar una lista nueva ya no borra en silencio;
FUSIÓN: ids y escaleras de evento sobreviven) · 146 bandera «tras reconectar» por
campo (clasificación campo a campo con el código real de wa-baileys/wa-cloud: TODOS
los de wa-cloud son snapshot congelado; carpeta_sesion con advertencia; textos
honestos en numero/nombre_dispositivo) · 147 se RETIRÓ el switch fantasma
ignorar_estados (normalizar bota los estados siempre: un control que no controla,
miente) · 148 los ENSAYOS ya no cuentan en las métricas (ajuste
contar_pruebas_en_metricas, default apagado: la agencia decía «22 tomados a mano» y
13 eran del gimnasio — ahora 9; pausadosAhora aprendió ocultarCanales) · 149 visor
con PELLIZCO (zoom 1–4× alrededor de donde pellizcas, paseo con un dedo sin escaparse
del marco, doble-toque integrado al mismo estado).

Verificación T9: 1162 tests (19 nuevos: media del mensajero con topes, foto multipart
+ rechazo de mime, reenviar reusa fila/409 si llegó, hoy con serie/desglose/default
sin ensayos, tablero SLA administrable, matchFrag), 4 probadores (queda solo el
preexistente de conexiones), sello 202608140938, ambas instancias reiniciadas
(Baileys conectado), Chrome real 1440×900 y 390×844 con 0 errores de consola.

## Diferidas que quedan

- **Importador de precios para la forma catálogo** (tipo_tarifario de la sesión
  paralela dixdy-0b): cuando el cotizador esté en 'catalogo', el importador debe pedir
  servicios {nombre, precio, …} en vez de zonas. Espec de 0b recibida; próxima tanda.
- ~~Cartel de chats abandonados~~ → **HECHO (eb7595a)**: Hoy muestra «Los tomaste tú y
  el cliente sigue esperando» (query takeoversAbandonados de la sesión 0b + nombre
  bautizado + «Devolver al bot» vía despausar). 20 detectados en vivo al estrenar.

## Verificación
- Suite: 57 archivos, 1143 tests verdes (incluye administrabilidad de los ajustes
  nuevos, noleidoN y dormidos=todos).
- Verificadores del panel: borrador ✓, hilo ✓, iconos ✓, render ✓ (queda el
  preexistente de conexiones: 2 campos `herramientas[].muestra` sin forma declarada).
- Navegador real (Chrome/Playwright): Hoy, Chats/lista, hilo, tablero y ⌘K en
  1440×900; lista, chat-capa, tablero-snap y barra inferior en 390×844. Consola: 0
  errores.
- Producción: ambas instancias (8793/8794) reiniciadas 2 veces en la madrugada con
  kickstart -k, verificadas por lsof + /api/salud + wa-baileys conectado.
