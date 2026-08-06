# QA del 6-ago · clientes reales por el simulador + panel con ojos de no-técnico

Pedido de Alejandro: «puedes hacer pruebas internamente simulando con el simulador… con
data que tenemos con el bot antiguo y ver dónde se está cayendo, y tú hacerte pasar por
alguien que no sabe mucho de tecnología usando la plataforma».

Método: 4 conversaciones REALES del bot antiguo (elegidas por variedad: zona sin tarifa,
cambio de plazo a mitad, urgencia con factura, arriendo largo con preguntas comerciales)
inyectadas mensaje a mensaje por el simulador (canal `sim`, cero riesgo), más una
auditoría de todos los textos del panel.

## 🔴 Bugs encontrados y arreglados

| # | Qué pasaba | Por qué importaba |
|---|---|---|
| 1 | **El loro**: con un tema esperando respuesta del dueño, el bot repetía «Déjame confirmarlo bien y te escribo al tiro» en CADA mensaje (4 veces seguidas en el caso Pirque) mientras el cliente daba plazo, dirección y cantidad | El bot viejo cerró esa misma venta en $170.000. El cerebro no sabía que ya había preguntado; ahora recibe los temas en espera y la orden de seguir con todo lo demás |
| 2 | **Plantilla de emergencia por error de formato**: el cerebro contestó en prosa en vez del JSON pedido y el cliente recibió «Dame un momento, ya te confirmo» — sin seguimiento | Sin motor de respaldo configurado, un tropiezo transitorio costaba el cliente. Ahora se reintenta UNA vez antes de degradar |
| 3 | **El simulador quedaba mudo con el bot apagado** — y hay que apagarlo justo para vincular el número (Fase 1) | Habría parecido roto en el peor momento. El chequeo estaba DUPLICADO (puedeResponder + la re-pregunta del debounce): arreglar uno solo no bastaba |
| 4 | **Precio «130.000» se leía como $130** en el formulario de la cotización formal | Cualquier chileno escribe así. Habría salido una cotización de ciento treinta pesos |
| 5 | La lista «sin monto» de Hoy mostraba ids de máquina («p-15») | Ilegible para el dueño |

## 🟡 Hallazgos de configuración (decisión de Alejandro)

- **3 comunas sin tarifa** que el bot viejo SÍ atendió: **Pirque** (3 clientes, cobró
  $170.000), **Santiago** (2), **Mostazal** (1). Con el bot nuevo abren una pregunta en
  vez de cotizar. Se arregla respondiendo la duda una vez (queda aprendido) o agregando
  la fila al tarifario.
- **Cotizaciones en `automatico`**: para estrenar conviene `tras_racha` — pide OK hasta
  ganarse 3 aprobaciones seguidas sin corrección.
- **`ver_chats_de_prueba` en true**: apagar tras el cutover para que los ensayos no
  ensucien el tablero real.

## ✅ Lo que funcionó bien (verificado con clientes reales)

- **Tono humano**: «Hola, claro que sí. ¿En qué comuna lo necesita?» — sin «¡», corto,
  una pregunta por mensaje. La regla de semanas se respeta.
- **Cotización correcta**: «Para 1 baño en Las Condes por 10 días son 130 mil neto, con
  traslado, instalación y retiro incluidos.»
- **Cambio de plazo a mitad**: entendió 10 días → 10-15 días y respondió «ese plazo queda
  en la misma franja: se mantienen los 130 mil neto».
- **Neto vs IVA**: «Confirmado: 130 mil neto ($154.700 con IVA)» y ofreció la cotización
  formal al correo.
- **No inventa**: en una comuna sin tarifa preguntó al dueño en vez de improvisar precio.

## Experiencia del panel (25 hallazgos, los de más impacto arreglados)

- Los errores hablaban en inglés («Load failed») o en códigos («HTTP 500») en ~25 avisos:
  ahora hay UN traductor con qué hacer en cada caso.
- «Ejecutar» → «Hacerlo ahora»; «Ver el diseño» → «Ver un ejemplo» (+ «no le llega a
  nadie»): la duda paralizaba justo al mandar algo real.
- Mensajes que mandaban a un menú inexistente («Ajustes →») ahora nombran el real.
- «borrador» convivía con «esperando tu OK» para lo mismo: unificado.
- La pantalla donde aprueba lo que su bot dirá («destilador», «rigor», «lote», ms):
  traducida entera.
- La advertencia «que sea un número de pruebas» bloqueaba el onboarding de cualquier
  dueño nuevo: ahora es condicional y explica el porqué.

**Pendiente de esa auditoría** (no bloquea, sí conviene antes de abrir el panel a otros
dueños): sacar la vista «Diseño» del menú (es una pantalla de programador), traducir el
Gimnasio («guionados», «juez», «ronda») y el «Gate del cutover», y completar el
diccionario de campos técnicos (`skills max pasos`, `cwd`, `timeout s`…).

Commits: `3ea78ae` (hallazgos de QA y UX) · `b41a16f` (los dos bugs de conversación).
