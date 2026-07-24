# Las reglas del minimalismo — dixdybot escritorio

Patrones extraídos de los dashboards B2B de referencia 2025-2026 (Linear, Vercel/Geist,
Stripe, Raycast, Attio) + NN/g (progressive disclosure) + notas de craft de Rauno Freiberg
(Vercel). No es branding: son reglas estructurales. Principio rector: **poca información
visible, mucha disponible**.

## Cómo lo logran los referentes (síntesis)

- **Linear:** listas = filas planas de ~40px con hover-background; cero cards; acciones
  secundarias invisibles hasta el hover; estado = punto de color de 8px; jerarquía por
  hairlines y espacio, no por cajas.
- **Vercel (Geist):** grilla estricta, presets de radio/sombra/borde (nunca ad-hoc), color
  solo para contraste/estado (no decoración), Sans para UI y Mono para datos/números.
- **Stripe:** el número es el protagonista — cifra grande en tabular-nums + delta pequeño +
  sparkline; el label es secundario y gris; la vista "Hoy" responde una sola pregunta.
- **Raycast:** UI transitoria — el detalle aparece en un panel al seleccionar y desaparece;
  sin motion en acciones frecuentes (se sienten instantáneas).
- **Attio:** tablas planas con hairlines; el detalle completo vive en un "side peek" al hacer
  click en la fila, nunca en la tabla misma.
- **NN/g:** lo frecuente va arriba y visible; lo raro, detrás de un click con buen "scent"
  (el label anticipa qué hay dentro). La frecuencia de uso decide qué se ve, no la
  importancia percibida.

## El decálogo anti-ruido (reglas duras y verificables)

1. **Presupuesto de chrome: ≤40 palabras por vista en reposo.** Se cuentan labels, títulos,
   botones y nav; los datos no cuentan. Ninguna frase completa visible en estado de reposo.
   Verificación: contar las palabras que no son datos en un screenshot.

2. **Labels de máximo 2 palabras, sin verbos explicativos.** "Ventas", no "Aquí puedes ver
   tus ventas"; botones con verbo de 1 palabra ("Guardar", no "Guardar los cambios"). Toda
   ayuda didáctica vive en tooltip (delay ~300ms) o en un coach-mark de primera vez
   descartable para siempre — nunca en texto permanente bajo un control.

3. **El número es el protagonista.** Métrica en 28–40px con `font-variant-numeric:
   tabular-nums`; label en 11–12px gris (~60% de contraste) encima o debajo, nunca al lado
   compitiendo. Delta pequeño y sparkline opcional al estilo Stripe. Cero iconos decorativos
   junto a métricas.

4. **Jerarquía sin cajas: máximo 1 tarjeta con borde/sombra por vista** (la protagonista).
   Regla de decisión: **tarjeta** = objeto autónomo y clickeable que merece foco; **fila** =
   elementos homogéneos repetidos (conversaciones, ventas) — plana, 40–48px, hairline de
   1px al 6–8% de opacidad, hover-background; **sección plana** = agrupaciones heterogéneas
   (ajustes) separadas por 24–32px de aire + heading pequeño. Si un contenedor no agrupa
   algo accionable, no lleva borde ni fondo.

5. **Estado del sistema = 1 punto de 8px**, verde/ámbar/rojo junto al nombre del canal/bot.
   Detalle (uptime, cola, último mensaje) solo en hover/click. Prohibido el panel "Todo
   funciona correctamente": **sin noticias = sin píxeles** — los estados sanos no generan
   filas ni tarjetas.

6. **Empty states de una línea: ≤8 palabras + 1 acción.** "Sin conversaciones hoy." o "Aún
   nada. [Conectar WhatsApp]". Sin ilustraciones grandes, sin párrafos que expliquen qué
   habría aquí.

7. **Revelación progresiva en 3 niveles.** L1 vista: números y filas (lo que se mira a
   diario). L2 hover: acciones secundarias aparecen solo al pasar sobre la fila (patrón
   Linear). L3 click: peek lateral o drill-down con TODO el detalle (patrón Attio/Raycast).
   Lo diario vive en L1, lo mensual en L3. Prohibido mostrar botones de acción
   permanentemente en cada fila.

8. **Una métrica hero por vista.** Cada vista responde UNA pregunta con UN número dominante;
   máximo 4 stats secundarias en una sola fila. Prohibido el grid 3×3 de KPIs. Test: si una
   métrica no cambia una decisión del dueño esta semana, va a L3 o se borra.

9. **Densidad de escritorio con aire.** Columna de contenido max-width 1100–1200px centrada
   (no full-bleed); padding de página 32–48px; espaciado en múltiplos de 8. Por pantalla
   1440×900: 1 hero + 1 lista de 6–10 filas; aire ≥30% del viewport. Tipografía: bastan 2
   tamaños de texto (13–14px UI, 12px meta) + 1 tamaño de número grande; números en
   mono/tabular.

10. **Color con presupuesto.** Grises para casi todo; 1 color de acento reservado a la
    acción primaria; semáforo solo para estado. Sin fondos de color en tarjetas de métricas.
    Icono solo si sustituye una palabra (y entonces la palabra desaparece); sin motion en
    interacciones frecuentes — lo frecuente aparece instantáneo (regla Rauno/Raycast).

## Qué cortar del prototipo v1 (aplicación directa)

- Notas didácticas bajo cada control → tooltip `?` o coach-mark de primera vez (regla 2).
- Título "Panel de administración de tu bot" → "Hoy" o el nombre del negocio (regla 1).
- Panel/sección de "estado del sistema" → punto de color en el header (regla 5).
- Card con borde+sombra por cada stat → fila de números sobre fondo plano (reglas 3-4).
- Botones-frase → verbos de 1 palabra (regla 2).
- Grid de KPIs de la portada → 1 hero + máx. 4 secundarias en una fila (regla 8).

## Fuentes

- [Geist — Vercel Design System](https://vercel.com/geist/introduction)
- [Linear Method](https://linear.app/method)
- [NN/g — Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)
- [Rauno Freiberg — Invisible Details of Interaction Design](https://rauno.me/craft/interaction-design)
- Patrones observados de producto: Stripe Dashboard ("Hoy": número grande + sparkline),
  Raycast (detalle transitorio), Attio (side peek sobre tablas planas).
