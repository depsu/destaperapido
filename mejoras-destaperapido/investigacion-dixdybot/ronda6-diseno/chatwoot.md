# Chatwoot — patrones de diseño para el panel de escritorio de dixdybot

Fuente: código real clonado en `scratchpad/clones/chatwoot` (rutas citadas relativas a `app/javascript/dashboard/`). Objetivo: extraer PATRONES (no branding) para un inbox de escritorio minimalista, un solo dueño no técnico.

---

## 1. Layout de 3 columnas (`routes/dashboard/conversation/ConversationView.vue`)

Un `<section class="flex w-full h-full min-w-0">` con 3 hijos:

| Columna | Ancho | Fuente |
|---|---|---|
| Lista de conversaciones | **340px fijo**, `412px` en ≥1536px (`w-[340px] 2xl:w-[412px]`, `flex-shrink-0`) | `components/ChatList.vue` L890 |
| Hilo | `flex-1 min-w-0`, separado con `border-l border-n-weak` | `widgets/conversation/ConversationBox.vue` |
| Panel de contexto | **oculto por defecto** (flag `is_contact_sidebar_open` en uiSettings); `320px` en md, `360px` en 2xl; en móvil pasa a overlay `fixed max-w-sm shadow-lg` que cierra con click-outside | `widgets/conversation/ConversationSidebar.vue` |

- Nav global (`components-next/sidebar/provider.js` L8-11): **default 200px, redimensionable 56–320px, colapsa a riel de iconos bajo el umbral de 160px**; el ancho elegido se persiste en uiSettings.
- Existe un layout alternativo "expanded": la lista ocupa todo y al abrir un chat la lista se oculta (patrón móvil llevado a escritorio). El colapso es binario: `showConversationList` / `showMessageView`, nunca 3 columnas apretadas.
- Regla de oro: **solo la columna del hilo es elástica**; lista y contexto son fijos. `min-w-0` en cada nivel para que el truncado funcione.

## 2. Fila de conversación (`widgets/conversation/ConversationCard.vue` L110-245)

Anatomía: avatar 32px arriba-izquierda + bloque de texto flexible + **columna derecha posicionada absolute (`right-3`)** con la hora (`text-xxs` = 10px) y debajo el badge de no-leídos. La hora nunca empuja el texto: el nombre reserva `pr-16`.

Máximo 3 líneas de texto:
1. **Meta** (opcional): icono del canal `size-4` + nombre del inbox — *solo si hay varios inboxes* (`showInboxName`) — + asignado + prioridad, todo 12px `text-n-slate-11`.
2. **Nombre**: 14px `font-medium`, `font-semibold` si hay no-leídos, una línea con ellipsis.
3. **Preview del último mensaje**: una línea `h-6 leading-6` con ellipsis; `text-n-slate-11`, sube a `text-n-slate-12 font-medium` si hay no-leídos. El TIPO de mensaje va como icono inline de 16px: candado = nota privada, flecha = respondió el agente, info = actividad (`MessagePreview.vue`).

- **No-leído = 3 señales tipográficas** (nombre semibold + preview oscuro + pastilla) — nada de fondos chillones en la fila. Badge: `bg-n-teal-9 rounded-full h-4 min-w-4 text-xxs text-white` (`components-next/Conversation/ConversationCard/UnreadBadge.vue`).
- Separador: `border-b border-n-slate-3` que **desaparece en hover y en la fila activa** (`hover:border-n-surface-1`); activa = `bg-n-background` + micro-animación `card-select` (translateX 1px, 0.25s). Hover = `bg-n-alpha-1` (gris translúcido).
- Selección múltiple: el checkbox aparece **como overlay sobre el avatar con `backdrop-blur-[2px]` solo en hover** — cero UI de bulk persistente.
- Altura resultante ≈72–84px con `py-3` y `px-3` laterales.

## 3. Hilo de mensajes (`components-next/message/Message.vue`, `bubbles/Base.vue`, `bubbles/Text/Index.vue`)

- Burbuja: **`max-w-lg` (512px), `px-4 py-3`, `text-sm`, `rounded-xl` con la esquina inferior del lado del emisor en `rounded-sm`** (cola sutil, direccional RTL-aware).
- **Agrupado**: mensajes consecutivos del mismo autor achatan la esquina superior (`.group-with-next`, CSS en `Message.vue` L607-611) y **solo el último del grupo muestra avatar y meta** (`shouldShowMeta`, `shouldGroupWithNext`). Avatar del hilo: **24px, alineado abajo** (`flex items-end`). Separación `mb-2`, `gap-x-2`; margen opuesto `ml-8`/`mr-8` para que las burbujas nunca lleguen al borde contrario.
- **Rol = color de fondo, sin etiquetas** (`bubbles/Base.vue` L46-56, `varaintBaseMap`):
  - cliente: `bg-n-slate-4` (gris)
  - humano/agente: `bg-n-solid-blue` (azul pastel)
  - **bot: `bg-n-solid-iris`** (lila pastel — distinto del humano; clave para un panel de agente IA)
  - **nota privada: `bg-n-solid-amber`** + texto `amber-12` + icono candado en la meta (`MessageMeta.vue`)
  - error: `bg-n-ruby-4`
  Todos pasteles Radix tono ~4; texto siempre `slate-12`.
- **Actividad del sistema NO es burbuja**: píldora centrada `px-3 py-1 rounded-xl bg-n-alpha-1 text-n-slate-11 text-sm`, con el timestamp **solo como tooltip** (`bubbles/Activity.vue`). Máxima des-jerarquización de lo no-conversacional.
- Meta (hora + check de estado): 12px, `text-n-slate-11`, dentro de la burbuja al final del grupo. Badge "N no leídos": píldora flotante centrada con `shadow-lg bg-n-brand` (`MessagesView.vue` L497).

## 4. Composer (`widgets/conversation/ReplyBox.vue` L1254+, estilos L1478-1490)

- **Tarjeta flotante, no barra pegada**: `mb-2 mx-2 border border-n-weak rounded-xl bg-n-solid-1`.
- **Modo nota privada tiñe TODA la tarjeta de ámbar** (`&.is-private { bg-n-solid-amber }`): el modo se ve, no se lee. Mismo ámbar que las burbujas privadas → un solo lenguaje de color.
- Tabs Responder / Nota privada arriba (`ReplyTopPanel`); todo lo demás (emoji, adjuntos, plantillas WhatsApp, artículos) vive en popovers y modales, no inline.
- Cambio de modo con transición fade + translate-y + scale 0.98, 200-300ms.

## 5. Header del hilo (`widgets/conversation/ConversationHeader.vue`)

`h-12` en desktop (una sola fila): avatar 32 + nombre 14px medium + **sublínea 12px "#id • inbox • snoozed"** con `•` como separador. Derecha: solo 2-3 iconos de acción. El resto en un menú "más".

## 6. Design tokens (`theme/colors.js` L107+, `assets/scss/_next-colors.scss`, `assets/scss/_woot.scss` L70-140, `tailwind.config.js`)

- **Paleta = escalas Radix 1-12 como CSS vars RGB** (`--slate-1: 252 252 253` …) bajo namespace `n-*`; **dark mode = clase `.dark` redefiniendo las mismas vars** (superficies 17-28 en vez de blanco). Encima, ~10 tokens semánticos: `--background-color` (247 gris), `--surface-1/2`, `--border-weak/strong`, capas `--alpha-*`.
- **Regla de color**: texto principal `slate-12`, secundario e iconos `slate-11`, bordes `slate-3`/`weak`. Casi todo el UI es gris; el color reservado a estados: teal=no leído, amber=privado/snooze, ruby=error, azul/iris=quién habla.
- **Tipografía**: Inter con pesos intermedios variables (420/440/460/520/620). Escala documentada en `_woot.scss`: body 14px/21px con letter-spacing −0.28px; label-small 12px/16px −0.24px; h1 18px/24px peso 520; `text-xxs` (10px) para timestamps. Fallback system-ui.
- Radios: 12px (`rounded-xl`) para burbujas y composer, 8px para tarjetas internas, `full` para pastillas.

## 7. Qué NO copiar (donde Chatwoot se recarga)

- La meta-fila de la card acumula inbox + asignado + prioridad + SLA + labels (`CardLabels`, `SLACardLabel`) → filas de hasta 5 líneas. Para UN dueño sin equipo: **eliminar asignado/prioridad/SLA/labels; fila de 2 líneas (nombre + preview) + icono de canal + hora + badge**.
- `ChatListHeader` + tabs de asignación ("Mías/Sin asignar/Todas") + folders + filtros avanzados + bulk actions: para un dueño basta título + un filtro de estado.
- Panel de contexto con 6+ acordeones arrastrables (`ContactPanel.vue`): bastan 2-3 secciones fijas colapsables; sí copiar que **cada sección recuerda si quedó abierta o cerrada** (uiSettings).
- 7 colecciones de iconos en `tailwind.config.js` (lucide, ri, ph, material-symbols…): elegir UNA.
- Composer con copilot, macros, canned responses, dashboard-app tabs incrustados: ruido; dejar texto + adjunto + modo nota.
- ~25 tokens `solid-*`/`call-widget-*` ad-hoc: reducir a ~6 semánticos.
