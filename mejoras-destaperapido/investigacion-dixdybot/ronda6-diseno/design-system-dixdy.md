# DESIGN SYSTEM DIXDY v1 — panel de escritorio de dixdybot

Spec para construir. Un dueño no técnico, un principio: **poca información visible, mucha
disponible**. Síntesis de linear.md (shell, tipografía, color), chatwoot.md (inbox),
referencias-typebot-fin.md (caminos y agente), minimalismo.md (decálogo).

---

## 1. TOKENS (CSS custom properties, listo para pegar)

```css
:root {
  /* ── Neutros: 12 pasos, hue 165 (susurro esmeralda), roles FIJOS ──
     1=fondo app · 2=fondo elemento · 3=hairline · 4=hover fuerte/burbuja cliente
     6=borde default · 8=foco neutro · 9=sólido · 11=texto secundario · 12=texto */
  --n-1:  #FAFBFA;   --n-2:  #F3F5F4;   --n-3:  #E8EBEA;   --n-4:  #DEE3E1;
  --n-5:  #D1D7D5;   --n-6:  #C2C9C6;   --n-7:  #A8B1AD;   --n-8:  #8A948F;
  --n-9:  #6D7773;   --n-10: #5C6662;   --n-11: #59625E;   --n-12: #151918;
  --bg-app:     var(--n-1);
  --bg-sidebar: #EFF2F1;             /* ~3 puntos L más oscuro que --bg-app; SIN borde */

  /* ── Acento único: esmeralda dixdy ── */
  --ac-subtle: #E9F5F0;   /* selección nav, diff añadido, hover de lo activo */
  --ac-pastel: #D6EDE3;   /* burbuja del bot */
  --ac-border: #9ED0BE;
  --ac-solid:  #0E7A5F;   /* botón primario, foco, no-leídos, punto "vivo" */
  --ac-hover:  #0B664F;
  --ac-text:   #0B5F4A;   /* links y texto acentuado sobre claro (≥4.5:1) */
  --ac-on:     #FFFFFF;

  /* ── Semáforo + roles (presupuesto de color COMPLETO del sistema) ── */
  --ok:          var(--ac-solid);          /* UN solo verde en todo el panel */
  --warn:        #D97706;  --warn-subtle: #FBF1DE;  --warn-text: #7A4E08;
  --err:         #DC2626;  --err-subtle:  #FBEBEA;  --err-text:  #A61B1B;
  --humano:      #2563EB;  --humano-pastel: #DCE7F8;   /* burbuja del dueño */
  --nota-pastel: #F7ECD2;  --nota-text: #6B5316;       /* nota privada, tiñe composer */

  /* ── Tipografía: UNA fuente, pesos intermedios, nunca 700 ── */
  --font-ui: "Inter Variable", Inter, system-ui, -apple-system, sans-serif;
  --fw-regular: 450;  --fw-medium: 500;  --fw-semi: 550;  /* fallback 400/500/600 */
  --fs-11: 11px; --lh-11: 16px;   /* terciario, labels de métrica, chips */
  --fs-12: 12px; --lh-12: 16px;   /* metadatos, sublíneas, headers de sección */
  --fs-13: 13px; --lh-13: 20px;   /* BASE: labels, filas, botones, body */
  --fs-14: 14px; --lh-14: 20px;   /* nombres, títulos de fila */
  --fs-16: 16px; --lh-16: 24px;   /* título de vista (único “grande” de texto) */
  --fs-num: 32px; --lh-num: 36px; /* métrica hero; font-variant-numeric: tabular-nums */
  --fs-10: 10px;                  /* SOLO horas en filas de conversación */
  --ls-ui: -0.01em;

  /* ── Espaciado (múltiplos de 4) ── */
  --sp-1: 4px; --sp-2: 8px; --sp-3: 12px; --sp-4: 16px;
  --sp-6: 24px; --sp-8: 32px; --sp-12: 48px;

  /* ── Radios ── */
  --r-sm: 6px;    /* inputs chicos, kbd, tooltip */
  --r-md: 8px;    /* filas, bloques, botones */
  --r-lg: 12px;   /* tarjetas, burbujas, composer, popover, peek */
  --r-full: 999px;/* pastillas, puntos, switch */

  /* ── Bordes y sombras ── */
  --border-hairline: 1px solid var(--n-3);   /* separar listas y headers */
  --border-default:  1px solid var(--n-6);   /* tarjetas, inputs, composer */
  --ring-select: 2px solid var(--ac-solid);  /* + margin -1px: el layout no salta */
  --shadow-float: 0 8px 24px rgba(12,14,13,.10), 0 2px 6px rgba(12,14,13,.06);
  /* REGLA: sombra SOLO a lo que flota (popover, modal, peek-overlay, menú).
     Superficies planas: jamás sombra; separan color o hairline. */

  /* ── Motion (lo frecuente = 0ms, optimista) ── */
  --t-hover: 100ms;  /* cambio de fondo en hover */
  --t-fade:  150ms;  /* aparecer/desaparecer acciones L2, tooltips */
  --t-pop:   200ms;  /* popover, cambio de modo del composer */
  --t-panel: 250ms;  /* peek lateral, colapso de sidebar */
  --ease: cubic-bezier(.25,.6,.25,1);

  /* ── Layout ── */
  --sidebar-w: 240px;  --header-h: 44px;  --content-max: 1120px;
  --list-w: 340px;     --ctx-w: 320px;    --grupo-w: 300px;
  --pop-w: 400px;      --peek-w: 420px;
  --z-header:10; --z-peek:20; --z-pop:30; --z-modal:40; --z-toast:50;
}

.dark {
  --n-1:  #0E100F;   --n-2:  #141716;   --n-3:  #1C201E;   --n-4:  #232827;
  --n-5:  #2C3230;   --n-6:  #363D3A;   --n-7:  #4A524E;   --n-8:  #5E6763;
  --n-9:  #778079;   --n-10: #8A938E;   --n-11: #9BA49F;   --n-12: #F2F5F4;
  --bg-app: var(--n-1);  --bg-sidebar: #0B0D0C;   /* nunca negro puro */
  --ac-subtle: #0F2A21;  --ac-pastel: #143A2D;  --ac-border: #1F5A47;
  --ac-solid: #17936F;   --ac-hover: #1CA87F;   --ac-text: #46C39C;  --ac-on: #FFFFFF;
  --warn: #F59E0B; --warn-subtle: #2E2410; --warn-text: #F0B454;
  --err:  #EF4444; --err-subtle:  #331716; --err-text:  #F08A8A;
  --humano: #5B8DEF; --humano-pastel: #15263E;
  --nota-pastel: #322812; --nota-text: #E8C877;
  --shadow-float: 0 8px 24px rgba(0,0,0,.45), 0 2px 6px rgba(0,0,0,.30);
}
```

Reglas de uso de color (cierran el presupuesto):
- Texto `--n-12`, secundario e iconos `--n-11`, hairlines `--n-3`, bordes `--n-6`.
- Esmeralda = acción primaria, foco/selección, no-leídos, "bot habló", "vivo". Nada más.
- Ámbar = privado/pausado/atención. Rojo = error. Azul = "habló un humano". Punto final.
- Cero fondos de color en métricas; cero iconos decorativos; icono solo si sustituye
  una palabra (y la palabra desaparece). UNA sola colección de iconos, stroke 2, 16px.

---

## 2. SHELL DESKTOP (L invertida)

```
┌────────────┬─ header 44px ────────────────────────────────────────┐
│  sidebar   │  Título 16/550          [control] [Verbo]            │ ← hairline abajo
│  240px     ├──────────────────────────────────────────────────────┤
│  bg-sidebar│                                                      │
│  sin borde │        contenido · max-width 1120px centrado         │
│            │        padding 32–48px · aire ≥30%                   │
│  footer ●  │        (Chats y Caminos: full-bleed, sin max-width)  │
└────────────┴──────────────────────────────────────────────────────┘
```

**Sidebar (240px, `--bg-sidebar`, border-right: 0** — separa el COLOR, no una línea):
- Arriba: nombre del negocio 13/550 + **punto global 8px** (esmeralda=bot vivo,
  ámbar/rojo=algo pide atención; detalle en hover). Es el ÚNICO "estado del sistema".
- Nav: 5 items — Hoy · Chats · Caminos · Módulos · Agentes. Fila 28px, radius 8px,
  icono 16 + label 13/500 `--n-11`; activa = `--ac-subtle` + texto `--n-12`.
  Contador (chats sin leer, decisiones) = número desnudo al final, sin chip.
- Headers de sección (si hicieran falta): 12/500 `--n-11`, 15px alto, sin uppercase.
- Footer: canal con problema (solo si lo hay: "WhatsApp ●" ámbar) + avatar del dueño
  + ⚙. Canales sanos NO aparecen (sin noticias = sin píxeles).

**Header de vista (44px, hairline inferior):** título 16/550 a la izquierda (una
palabra: "Hoy", "Chats"…), máximo 2 controles a la derecha (1 filtro + 1 botón-verbo).
Prohibido: heros, subtítulos, breadcrumbs de más de un nivel, frases.

**Colapso a móvil:**
- 1024–1279px: sidebar → riel de iconos 56px (labels en tooltip).
- <1024px: sidebar → overlay (hamburguesa en barra superior 48px). Chats se apila:
  lista full → hilo full con "‹ volver"; contexto → overlay `max-w-sm` + sombra,
  cierra con click-outside. Peek L3 → sheet a pantalla completa. Nunca 3 columnas
  apretadas: el colapso es binario.

---

## 3. ANATOMÍA POR VISTA

### 3.1 HOY — "¿algo espera mi decisión y cómo vamos?"

```
│ Hoy                                                  [Semana ▾] │
├─────────────────────────────────────────────────────────────────┤
│   $184.000                                                      │  ← hero 32px tabular
│   ventas hoy · ↑3 vs ayer  ▁▂▄▂▆                                │  ← label 11px n-11
│                                                                 │
│   12          9           2          4 min                      │  ← ≤4 secundarias,
│   chats       resueltos   ventas     respuesta                  │    una sola fila
│                                                                 │
│   Decisiones · 2                                                │  ← 12/500 n-11
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Cotización $95.000 a Marcela            [Ver]  [Aprobar]  │  │  ← tarjeta-solo-
│  └───────────────────────────────────────────────────────────┘  │    cuando
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Reembolso pedido #218                   [Ver]  [Aprobar]  │  │
│  └───────────────────────────────────────────────────────────┘  │
```

- 1 métrica hero + máx 4 secundarias (números 14/550 tabulares, labels 11 gris).
- "Decisiones" solo existe si hay pendientes; si no hay, la sección NO se renderiza
  (nada de "todo al día ✅"). Máx 3 tarjetas visibles + "n más" → L3.
- Tarjeta de decisión = 1 línea de hecho + 2 botones-verbo. [Ver] abre peek con el
  chat/contexto; [Aprobar] es instantáneo y optimista.
- Día vacío: hero en $0 + "Sin actividad aún." (empty state, ≤8 palabras).

### 3.2 CHATS — 3 columnas (Chatwoot destilado)

```
│ lista 340px      │ hilo flex-1 min-w-0             │ contexto 320px │
├──────────────────┼─────────────────────────────────┼────────────────┤
│ ○ Marcela    2m ●│ ○ Marcela · WhatsApp · abierto  │ Datos       ⌄ │
│   ¿Precio del…   │─────────────────────────────────│ Pedido      ⌄ │
├──────────────────│  ┌ cliente (gris) ┐             │ Notas       ⌄ │
│ ○ Jorge      1h  │  └────────────────┘             │                │
│   ↳ Gracias!     │        ┌ bot (esmeralda pastel)┐│ (oculta por    │
├──────────────────│        └───────────────────────┘│  defecto,      │
│ ○ Ana        3h  │     ·· se unió el repartidor ·· │  persistida)   │
│   🔒 revisar boleta       ┌ dueño (azul pastel) ┐  │                │
│                  │        └─────────────────────┘  │                │
│                  │ ┌─────────────────────────────┐ │                │
│                  │ │ Responder | Nota    …  [➤]  │ │ ← composer     │
│                  │ └─────────────────────────────┘ │   flotante     │
```

- **Fila de conversación (72px, 2 líneas):** avatar 32 + nombre 14/500 (semibold si
  no-leído) + preview 1 línea con ellipsis; columna derecha absoluta: hora 10px +
  pastilla esmeralda h-16/min-w-16 con el conteo. No-leído = 3 señales tipográficas,
  jamás fondo de color. Icono de canal 16px SOLO si hay >1 canal. Tipo del último
  mensaje como icono inline 16px (🔒 nota, ↳ respondió, ⓘ actividad).
  Separador hairline `--n-3` que desaparece en hover y en la activa.
  Hover = fondo translúcido; activa = `--bg-app` + translateX 1px 250ms.
  Header de lista: solo un filtro de estado (Abiertos ▾). Sin tabs, sin folders.
- **Hilo:** burbuja max-w 512px, px16 py12, 13px, radius 12 con esquina inferior del
  emisor en 4px; consecutivos del mismo autor se agrupan (solo el último muestra
  avatar 24 alineado abajo + hora 12 `--n-11`). Rol por fondo pastel SIN etiquetas:
  cliente `--n-4` izq · bot `--ac-pastel` der · dueño `--humano-pastel` der ·
  nota `--nota-pastel`+🔒 · error `--err-subtle`. Texto siempre `--n-12`.
  Actividad del sistema = píldora centrada px12 py4 `--n-2` texto `--n-11`,
  timestamp solo en tooltip. Nunca burbuja.
- **Composer:** tarjeta flotante mx8 mb8, `--border-default`, radius 12. Tabs
  Responder | Nota. En modo Nota TODA la tarjeta se tiñe `--nota-pastel` (el modo se
  ve, no se lee). Adjuntos/plantillas en popover, nunca inline.
- **Header del hilo (48px):** avatar 32 + nombre 14 + sublínea 12 "canal · estado"
  con `·`. Derecha: 3 iconos máx (resolver ✓, contexto ⓘ, más ⋯).
- **Contexto (320px):** oculta por defecto, persistida. 3 secciones colapsables
  (Datos, Pedido/Cotización, Notas) que recuerdan su estado abierto/cerrado.

### 3.3 CAMINOS — cascada Typebot + detalle con draft/vivo estilo Fin

```
│ Caminos                                              [+ Camino] │
├───────────────┬──────────────────────────┬──────────────────────┤
│ Ventas   VIVO │   ┌── 300px ───────────┐ │ Probar ▸             │
│ Postventa BORR│   │ Saludo             │ │ ┌──────────────────┐ │
│ Reclamos VIVO·│   │ ✉ ¡Hola! Soy…      │ │ │ chat simulado    │ │
│ (filas 48px)  │   │ ? ¿Qué necesitas?  │ │ │ + pestaña Por qué│ │
│               │   └─────────┬──────────┘ │ └──────────────────┘ │
│               │   ┌─────────▼──────────┐ │ Borrador · 3 cambios │
│               │   │ Cotizar            │ │ + verde / – rojo     │
│               │   │ ⚙ calcular precio  │ │ [Descartar][Publicar]│
│               │   │ ✉ Tu precio es…    │ │  → "¿Qué cambió?"    │
│               │   └────────────────────┘ │     (50–500 chars)   │
```

- **Lista (izq):** fila 48px = nombre 13/500 + chip de estado + uso 12 `--n-11`
  ("41 esta semana"). Click → cascada.
- **Cascada (centro):** tarjetas de grupo de **300px fijos**, radius 12, borde
  `--n-6`, p16/16/8, título editable inline (sin botón editar). Bloque = fila p12
  radius 8, fondo `--n-2` (exactamente UN paso más oscuro que la tarjeta: jerarquía
  por escala, no sombras). El contenido del bloque ES el preview de su config
  (primera línea del mensaje, placeholder de la pregunta); vacío = placeholder gris
  50% opacidad, sin badges. Color del icono = categoría: mensaje `--n-12` ·
  pregunta `--ac-solid` · lógica/integración `--humano` (se reusa el azul).
- **Estados solo por borde con el único acento:** hover tarjeta = borde `--n-8`;
  seleccionado/conectando = `--ring-select` con margin -1px. Sin glows ni rellenos.
- **Edición = revelación progresiva:** texto inline en el lugar; opciones en popover
  400px (p16, max-h 60vh) anclado al bloque, expandible a 80vh. JAMÁS otra página.
  Reordenar: placeholders 4px→50px solo al arrastrar; bloque levantado rota -2°.
- **Draft/vivo (der):** editar crea borrador; lo vivo no se toca hasta [Publicar],
  que exige resumen "¿qué cambió?" y muestra el diff. Rollback restaura COMO
  borrador. Preview con "Por qué" (qué regla/camino aplicó) siempre disponible.

### 3.4 MÓDULOS — filas con switch, config al expandir

```
│ Módulos                                                         │
├─────────────────────────────────────────────────────────────────┤
│   Cotizador                                              [⬤  ]  │ ← 48px
├─────────────────────────────────────────────────────────────────┤
│   Recordatorios 💤                                       [⬤  ]  │
│      Días de espera [ 3 ▾ ]     Hora [ 10:00 ]                  │ ← expandida:
│      Mensaje  [ Hola {nombre}, ¿seguimos con…        ]          │   ≤4 controles
├─────────────────────────────────────────────────────────────────┤
│ ● Encuestas                                              [  ◯]  │ ← ámbar: necesita
└─────────────────────────────────────────────────────────────────┘   config; texto n-11
```

- Fila 48px plana con hairline: nombre 13/500 + switch a la derecha. SIN descripción
  visible (vive en tooltip 300ms sobre el nombre). Punto 8px SOLO si el módulo pide
  atención (ámbar) o falla (rojo); sano = sin punto.
- Click en la fila (no en el switch) expande acordeón inline: máx 4 controles,
  labels ≤2 palabras, ayuda en tooltip. Una expandida a la vez.
- Apagado = texto de la fila baja a `--n-11`. El switch es instantáneo (optimista).

### 3.5 AGENTES — 4 secciones estilo Fin

```
│ Agentes › Vendedor                                  [Probar ▸]  │
├─────────────────────────────────────────────────────────────────┤
│ ◉ Vendedor      Personalidad · Conocimiento · Reglas · Proced.  │ ← tabs 13/500
│                                                                 │
│ Tono      (◉ Cercano — cálido, directo   │ "¡Hola! Sí, tenemos…"│ ← preset 1 línea
│           (○ Formal — sobrio, preciso    │ "Buen día. Confirmo…"│   + ejemplo al lado
│ Largo     ( Conciso | ◉ Estándar | Extenso )                    │
│                                                                 │
│ Reglas · 4                                            [+ Regla] │
│ ┌ Nunca prometer hora exacta ✦                          [⬤ ] ┐  │ ← tarjeta título
│ └──────────────────────────────────────────────────────────── ┘  │   + toggle
│                                                                 │
│ Procedimientos                                        [+ con IA]│
│   Confirmar pedido      VIVO·borrador    41×  ▸                 │ ← fila 48 + chip
│   Derivar reclamo       PAUSADO           3×  ▸                 │
```

- **Nunca un formulario gigante:** todo el agente cabe en 4 secciones; el handoff
  vive dentro de Reglas y como herramienta de Procedimientos.
- **Personalidad por presets, no texto libre:** 5 tonos (1 línea de 3 adjetivos) y
  3 largos relativos; cada preset demostrado con respuesta de ejemplo al lado.
- **Regla = tarjeta:** título obligatorio + texto natural (≤2.500 chars, colapsado)
  + toggle apagar-sin-borrar + botón ✦ (IA detecta ambigüedad/redundancia).
- **Procedimiento:** fila con chip de 5 estados + uso; abierto = documento con
  "cuándo usarlo" (256 chars) + pasos en lenguaje natural + herramientas con `@`.
  Borrador con IA: el dueño describe su proceso (≤5.000 chars o pega su SOP) →
  la IA pregunta lo que falta → Conservar / Limpiar / Otra vez.
- **[Probar ▸]** abre el peek de preview (chat simulado + Por qué + impersonar
  cliente) desde CUALQUIER pestaña; refleja borradores sin guardar.
- Draft/vivo idéntico a Caminos: publicar pide "¿qué cambió?"; rollback → borrador.

---

## 4. DECÁLOGO ANTI-RUIDO (reglas duras del sistema, verificables)

1. **Chrome ≤40 palabras por vista en reposo** (labels+títulos+botones+nav; los datos
   no cuentan). Ninguna frase completa visible. Se verifica contando en screenshot.
2. **Labels ≤2 palabras; botones = 1 verbo.** Ayuda solo en tooltip (300ms) o
   coach-mark de primera vez descartable. Cero texto didáctico permanente.
3. **El número es el protagonista:** 32px tabular-nums, label 11px gris debajo;
   delta pequeño + sparkline opcional; cero iconos junto a métricas.
4. **Máximo 1 tipo de tarjeta por vista.** Tarjeta = objeto autónomo clickeable;
   fila = homogéneos repetidos (hairline 1px); sección plana + 24–32px de aire =
   heterogéneos. Contenedor que no agrupa algo accionable no lleva borde ni fondo.
5. **Estado = punto de 8px** (esmeralda/ámbar/rojo) junto al nombre; detalle en
   hover/click. **Sin noticias = sin píxeles:** lo sano no genera filas, tarjetas
   ni "todo funciona bien".
6. **Empty state ≤8 palabras + 1 acción.** Sin ilustraciones, sin párrafos.
7. **Revelación en 3 niveles:** L1 vista (lo diario) · L2 hover (acciones
   secundarias aparecen a 150ms, sin mover nada) · L3 click (peek 420px o popover
   400px con TODO). Prohibidos botones permanentes por fila; lo mensual vive en L3.
8. **1 métrica hero + ≤4 secundarias por vista.** Prohibido el grid de KPIs. Test:
   si un dato no cambia una decisión del dueño esta semana → L3 o se borra.
9. **Densidad con aire:** columna 1120px centrada, padding 32–48, múltiplos de 8,
   aire ≥30% del viewport; por vista: 2 tamaños de texto + 1 de número.
10. **Color y motion presupuestados:** neutros + esmeralda + semáforo + azul-humano;
    sombra solo a lo que flota; hover = un paso de fondo a 100ms; lo frecuente es
    instantáneo y optimista (0ms), la velocidad ES la estética.

---

## 5. INVENTARIO DE COMPONENTES

**Fila de lista** — base: hover un paso de fondo (100ms), activa `--ac-subtle`,
hairline `--n-3` entre filas (desaparece en hover/activa), ≤6 átomos, truncado con
`min-w-0`. Variantes:
| Variante | Alto | Anatomía |
|---|---|---|
| nav | 28px | icono 16 + label 13/500 + contador desnudo |
| dato (camino, procedimiento) | 48px | nombre 13/500 + chip estado + métrica 12 gris + ▸ |
| módulo | 48px | [punto solo si warn/err] + nombre 13/500 + switch |
| conversación | 72px | avatar 32 + 2 líneas (nombre 14 / preview) + hora 10 + pastilla |

**Punto de estado** — 8px, radius full. Esmeralda=vivo/ok · ámbar=atención ·
rojo=caído. Siempre con tooltip (detalle). Variante 12px con anillo de progreso para
"en curso". Nunca acompañado de la palabra que ya representa.

**Chip de estado** — SOLO para el ciclo draft/vivo (nunca para salud del sistema):
pastilla 11/500, radius full, px6 h-16, fondo subtle + texto oscuro del semántico.
Estados: BORRADOR (`--n-2`/`--n-11`) · VIVO (`--ac-subtle`/`--ac-text`) ·
VIVO·borrador (VIVO + punto ámbar 6px) · PAUSADO (`--warn-subtle`/`--warn-text`) ·
ERROR (`--err-subtle`/`--err-text`).

**Switch** — 32×18px, thumb 14px, on=`--ac-solid`, off=`--n-6`, disabled=`--n-4`;
transición del thumb 120ms; sin texto on/off; cambio optimista.

**Diff** — línea añadida: fondo `--ac-subtle` + barra 2px `--ac-solid` a la
izquierda; eliminada: fondo `--err-subtle` + tachado `--n-11`. Resumen = pastilla
"Borrador · n cambios". Modal Publicar: diff + textarea "¿Qué cambió?" obligatoria
(50–500 chars) + [Publicar]. Rollback siempre restaura como borrador.

**Tarjeta-solo-cuando** — radius 12, `--border-default`, fondo `--bg-app`, p16;
hover = borde `--n-8` (sin sombra); selección = `--ring-select` margin -1px. Usos
permitidos (únicos): decisión pendiente (Hoy), grupo de camino, regla del agente,
preset de personalidad. Todo lo demás es fila o sección plana.

**Tooltip** — delay 300ms, fondo `--n-12`, texto `--n-1` 12px, radius 6, px8 py4,
1 línea máx + chip kbd opcional (11px, fondo `--n-2`, borde `--n-3`, radius 4).
OBLIGATORIO en todo icono sin texto. Es el único lugar donde vive la ayuda.

**Empty state** — centrado, 13px `--n-11`, ≤8 palabras + 1 botón-verbo o pista kbd.
"Sin conversaciones hoy." · "Aún nada. [Conectar]". Sin ilustraciones.

**Átomos de apoyo** — Botón: h-32, radius 8, 13/500; primario `--ac-solid`/blanco,
secundario borde `--n-6`, fantasma texto `--n-11`; peligro solo dentro de modales.
Burbuja: ver §3.2. Popover: 400px, p16, max-h 60vh→80vh, radius 12, shadow-float.
Peek L3: 420px desde la derecha, border-l hairline (sombra solo si es overlay).
Píldora de sistema: px12 py4 `--n-2` texto `--n-11` centrada.
