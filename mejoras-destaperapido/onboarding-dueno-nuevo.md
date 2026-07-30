# Onboarding del dueño nuevo — «el panel que te enseña a usarse solo»

Visión de Alejandro (28-jul-2026), pensada para personas que no saben nada de
tecnología y quieren usar IA. La experiencia debe sentirse como un JUEGO que te enseña
a jugar (referencia: el aldeano de Clash of Clans que te recibe y te cuenta las
novedades), no como un software que te tira a la piscina.

## La idea madre

La IA conversa con el dueño nuevo DIRECTAMENTE para poner en contexto su negocio, y la
plataforma se adapta con lo que él cuenta. Las primeras tareas son misiones guiadas.

## Los actos (el orden importa)

**Acto 1 — Contrata a tu compañero de trabajo.**
Crear el primer agente NO es un formulario: es una conversación. «Estás contratando a
alguien nuevo al que le tienes que enseñar tu negocio»: nombre de persona, cargo,
personalidad, qué hará. La IA recomienda cómo sacarle el máximo provecho.
→ HECHO EN DURO (28-jul): la vista Agentes sin agentes ya es el hero conversacional
  (saludo del día + caja grande estilo Claude + atajos; se expande a charla al primer
  mensaje; guion local nombre → cargo → cierre). Falta conectarla al cerebro para que
  CREE el agente de verdad (escribir ajustes/agentes.json vía endpoint, con las mismas
  manos/estructura de la guía de conexiones).

**Acto 2 — Pruébalo en el Simulador (y aquí se explican las Dudas).**
La primera misión tras contratar: hablarle al bot como si fueras un cliente. El
simulador se abre en una VENTANITA tamaño teléfono al lado del panel → ves el panel
moverse en tiempo real (el chat aparece en Todos marcado 🤖, la ficha nace sola…).
Cuando el bot no sepa algo, abrirá una Duda → ese es EL momento de explicar el ciclo
junior→senior: «te pregunta en vez de inventar; tu respuesta puede quedar aprendida».
→ HECHO (28-jul): ventanita popup 420×780 desde el menú (respaldo: pestaña si el
  navegador bloquea popups); ensayos visibles en «Todos» por defecto, marcados 🤖;
  las dudas de ensayo ya llegan a Hoy marcadas y siguen el flujo completo.

**Acto 3 — Conecta tu WhatsApp.**
Recién aquí se conecta el canal real. Explicar EN SIMPLE que hay 2 conexiones: la
rápida y gratis (QR/código, no oficial — perfecta para partir) y la oficial de Meta
(de pago, más estable, sin riesgo de baneo — el plan a futuro). Sin problema por
partir con la rápida.
→ EXISTE la guía conversacional de Conexiones (chat con manos reales). Falta: que el
  guion del onboarding la presente como misión 3 y el texto de las 2 conexiones.

## El acompañante permanente (transversal)

- **Chat de IA flotante, abajo a la derecha, SIEMPRE visible**, que no pierde contexto
  ni conversación al cambiar de vista. Es el mismo personaje que el guía del
  onboarding; el flotante es «su lugar de conversar» (su backlog).
- **Novedades como personaje**: al volver al panel tras una actualización, el guía
  aparece (animado, simpático) contando qué hay de nuevo — efecto aldeano de Clash.
  ⚠️ NO reinventar: el panel-cliente del maestro YA tiene el sistema de «novedades ✨»
  (cada mejora se anuncia sola). Promover/portar esa pieza y darle voz de personaje.
- **Misiones/primeras tareas**: una lista corta visible («contrata → simula → conecta»)
  con ✓ al completar, tono de juego, nunca bloqueante.

## Piezas técnicas ya existentes que esto reutiliza (doctrina: sumar, no construir al lado)

- Guía de Conexiones con salida estructurada + manos (patrón a copiar para la guía de
  agentes y el flotante global).
- Agente del chat con manos y tarjetas de aprobación (28-jul).
- Simulador + canal sim + dudas de entrenamiento marcadas.
- Sistema de novedades ✨ del panel-cliente (maestro) para el personaje de novedades.
- ajustes/*.json config-driven: «la plataforma se adapta» = la conversación inicial
  escribe ajustes (negocio, agentes, tarifario), no código.

## Orden sugerido de construcción (cuando se retome)

1. Guía de agentes conectada al cerebro (crear agente de verdad desde el hero).
2. Flotante global persistente (una sesión, viaja entre vistas).
3. Motor de misiones (3 misiones, estado en un ajuste, ✓ al completar).
4. Personaje de novedades (portar novedades ✨ + tono de juego).
5. Conversación inicial «cuéntame de tu negocio» que precarga ajustes.

## Fases regeneradas con la visión de Alejandro (30-jul) — estado

- **Fase A — el robot llega al panel: HECHA (30-jul).** Burbuja 🤖 flotante en todas
  las vistas; chat con backlog EN EL SERVIDOR (tabla guia_mensajes); mano llevar_a que
  navega y destaca la vista (verificado en vivo: «¿dónde veo mis precios?» → explicó y
  llevó a Caminos); globito de bienvenida la primera vez en cada vista; y la limpieza:
  nombres humanos en Hoy (Sofía / tu asistente), Examen en vez de gate, menú «Qué hace
  tu bot», Módulos sin duplicar canales (enlace a Conexiones), Diseño oculto por
  defecto (prendido en la instancia de Alejandro), banner honesto del simulador,
  fotos sin 404, sello de versión al pie, Guardar-nombre solo al editar.
- **Fase B — celular**: barra inferior con nombres, cara Agente en la ficha móvil,
  estreno/hero visible en pantalla chica, robot adaptado (ya es bottom-sheet), pegado
  al fondo del hilo.
- **Fase C — la conversación inicial**: «cuéntame de tu negocio» que personaliza dixdy
  escribiendo los ajustes (negocio, agente, tono) sin nada técnico; misiones tomando
  Hoy cuando el negocio está vacío; celebraciones; novedades contadas por el robot;
  texto 2-conexiones y primera prueba guiada del simulador. El robot flotante de la
  Fase A es el MISMO personaje que conduce todo esto.
