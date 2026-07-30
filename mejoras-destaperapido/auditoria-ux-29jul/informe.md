# Auditoría de experiencia — dixdybot panel (29-jul-2026)

Método: recorrido real con navegador en escritorio (1280px) y celular (390px), 17
capturas (esta carpeta), más lectura de flujos. Foco: persona nueva NO técnica que
quiere conectar WhatsApp sola, crear su agente, simular, crear caminos y ayudar al bot.

## Los 3 problemas de fondo

1. **No existe la "primera vez".** El panel abre en Hoy (vacío para un negocio nuevo);
   el guía y las misiones viven escondidos en Agentes (+ parámetro). La bienvenida debe
   tomar el centro cuando el negocio está recién nacido.
2. **Cuatro IAs que parecen cuatro personas.** Guía de conexiones, guía de agentes,
   agente del chat y simulador: mismo fondo, cuatro caras. Debe ser UN personaje (el
   guía 🤖) presente en todas partes, con un flotante abajo a la derecha que no pierde
   la conversación al cambiar de vista.
3. **El menú habla técnico y en móvil es un jeroglífico.** "Caminos", "Módulos",
   "Diseño", "Sistema"; en celular quedan 8 iconos SIN texto.

## Hallazgos por misión (persona nueva)

- **Conectar WhatsApp**: la guía funciona; falta la explicación de entrada "2 formas:
  rápida (QR, gratis) vs oficial Meta (estable, para después)". En Módulos, Meta
  aparece DUPLICADO (tarjeta + switch).
- **Crear el agente**: bien en escritorio; en móvil el hero NO SE VE (queda detrás de
  la capa de lista). La guía piensa lento sin atajos instantáneos.
- **Simulador**: banner contradictorio — dice "estos chats no se ven en tu panel" y al
  lado "VISIBLES en el panel" (quedó del default viejo). Falta primera-prueba guiada.
- **Caminos**: la vista nueva por columnas está bien; falta el puente narrativo "los
  caminos nacen de tus respuestas a las dudas".
- **Ayudar al bot (dudas)**: lo más fuerte del panel. Detalles: nombres crudos
  ("sofia", "bot", "Ayudar a bot") en Hoy; banner de avisos empieza sin sujeto
  ("Actívalos y…").
- **Entrenar como trabajador**: el relato existe (contratar/entrenando/despedir);
  sobran tecnicismos: "Gate de calidad", "gate 4", "Derivación silenciosa".

## Móvil (390px)

- **MV1** Menú: iconos sin etiqueta → barra inferior tipo app con texto (5 accesos).
- **MV2** La ficha del chat NO tiene la cara Agente: desde el celular no puedes hablar
  con Sofía ni resolver la duda inline. Grave: el celular es donde más se ayuda.
- **MV3** El estreno/hero de Agentes es invisible (la lista tapa el detalle).
- **MV4** Verificar el pegado al fondo del hilo al abrir chat en móvil.
- **MV5** Abrir la ficha tocando el nombre no es descubrible (sin botón visible).

## Quitar (menos abrumador)

- "Diseño" fuera del menú por defecto (es de constructores; el ajuste ya existe).
- Duplicado de Meta en Módulos.
- Botón "Guardar el nombre" siempre visible → solo al editar.
- Sello de versión "27-07 11:45" junto al logo → al pie.
- 127 peticiones de foto fallidas por carga (pedir solo las que existen).
- "el panel todavía no puede abrirlo" (nota de voz) → texto menos "error".

## Animaciones (cortas, sobrias, respetando "reducir movimiento")

- Celebración única al completar una misión / aprender el primer camino (confeti).
- Contadores de Hoy con subida animada; tarjeta de duda que sale deslizándose al
  resolverse + toast "Sofía aprendió ✨".
- Transición suave entre vistas; personaje con parpadeo ocasional.

## Plan propuesto (aprobar antes de ejecutar)

- **Fase A — palabras y limpieza (rápida)**: textos de Hoy (nombres humanos, banner),
  banner del simulador, duplicado Meta, Diseño oculto por defecto, guardar-nombre solo
  al editar, sello al pie, fotos sin 404, renombres (Módulos→"Qué hace tu bot",
  Gate→"Examen para atender", subtítulos del menú).
- **Fase B — móvil de verdad**: barra inferior con etiquetas, cara Agente en la capa
  del chat, hero/estreno como primera pantalla de Agentes en celular, pegado al fondo.
- **Fase C — el personaje único**: guía flotante persistente (abajo derecha, misma
  conversación en todas las vistas), bienvenida de primera-vez tomando Hoy cuando el
  negocio está vacío (misiones al centro), celebraciones, novedades contadas por el
  personaje (portar "novedades ✨" del maestro), texto 2-conexiones y primera-prueba
  guiada del simulador.
