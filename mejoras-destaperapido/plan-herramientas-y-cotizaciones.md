# Plan · Herramientas conectadas + Cotizaciones formales + Confianza ganada

**Visión de Alejandro (1-ago-2026), en sus palabras:** herramientas por cliente en el
panel (el panel del repartidor como primera), cada una con su API conversando con el bot;
lo que es plata la marca un humano en el panel, jamás la IA; cotizaciones formales (PDF)
visibles en el panel con su plantilla y sus campos variables; y el último click de las
cotizaciones que se GANA: tras 3 confirmaciones seguidas buenas el bot sigue solo, y si
se equivoca una, el contador vuelve a cero. Herramientas personalizadas = servicio pagado
extra de dixdy por cliente.

## Lo que YA existe (no se reinventa — doctrina DIXDY)

| Pieza de la visión | Dónde ya vive |
|---|---|
| Herramientas con permisos | `dixdybot/src/schemas/conexion.ts`: permiso POR herramienta — `bot` (la usa sola, con traza) · `con-ok` (propone, humano aprueba) · **`solo-dueno` (JAMÁS el cerebro; solo botón del panel)** ← la regla «la plata la marca un humano» ya es contrato |
| Herramientas fabricadas por cliente (el negocio pagado) | `Conexion.origen: 'fabricada'` — «chat de conexión → Claude Code fabrica el conector CON pruebas en el clon». Es el modelo de negocio escrito en el schema |
| La plata solo humana, en el motor | `OrigenMovimiento`: el bot puede ABRIR un pedido pero jamás moverlo de etapa ni registrar cobro (escritor.moverPedido lo rechaza) — la ley ya corre |
| El último click de cotizaciones | `cotizador.ultimo_click` ('siempre_yo' | 'solo_si_no_calza' | 'automatico') — ⚠️ HOY ES UN ENCHUFE SIN CABLE: promete «toda cotización espera tu OK» pero solo alimenta `tiposDecision`, el canal muerto del §8. El bot cotiza solo aunque diga 'siempre_yo' |
| Cotizaciones PDF de destaperapido | `~/SaSS/destaperapido/cotizaciones-destape-rapido/` + `agente-cotizaciones/` — sistema completo (plantilla, config, correo) llamable desde Node. Es DEL CLIENTE: entra como herramienta fabricada, no al molde |
| Panel del repartidor | Ya vive con el bot viejo (API solo-lectura + Supabase). Candidata a primera conexión fabricada del dixdybot |

## El orden de construcción

### H1 · El último click que se GANA (molde — cablear el knob que hoy miente)
- Detectar la cotización del turno (el contador `anotarCotizacion` ya marca el momento) y,
  según `ultimo_click`: **siempre_yo** → el mensaje NO sale: tarjeta de aprobación en Hoy
  (aprobar = sale al cliente; corregir = sale tu versión). **automatico** → como hoy.
- Modo NUEVO **`tras_racha`** (la regla de Alejandro): parte como siempre_yo; cada
  aprobación sin corrección suma; con `racha_meta` (default 3) seguidas el bot pasa a
  automático **y el panel lo dice** («el bot se ganó tu confianza en cotizaciones»); una
  corrección → contador a CERO y vuelve a preguntar. El contador vive visible en Precios.
- ⚠️ Decisión previa de Alejandro: al cablearlo, la instancia real debe elegir modo
  EXPLÍCITO (hoy su ajuste hereda 'siempre_yo' que nunca se cumplió — cablearlo tal cual
  FRENARÍA de golpe todas las cotizaciones del bot de prueba). Opciones: partir en
  'automatico' (conducta actual) y que él suba a 'tras_racha' cuando quiera rodarlo.

### H2 · Cotizaciones formales en el panel (cliente, vía herramienta fabricada)
- Vista «Cotizaciones» del clon: la plantilla PDF de ejemplo visible + los campos
  variables (cliente, comuna, cantidad, plazo, precios) + «generar desde este pedido».
- Genera con el sistema python existente; el ENVÍO (correo) pasa por la tarjeta de
  aprobación de H1 — mismo flujo, misma racha.

### H3 · Vista «Herramientas» (molde: el runtime de Conexiones fabricadas)
- La vista lista las conexiones del clon con sus herramientas y permisos EN SIMPLE
  («Entregas: el bot avisa, TÚ marcas entregado/cobrado»). Botones del panel para las
  `solo-dueno`; las `con-ok` crean tarjeta de aprobación; las `bot` quedan en la traza.
- Primera conexión real: el panel del repartidor de destaperapido (su API ya existe).
- Es la vitrina del servicio pagado: «¿quieres que el bot también haga X? se fabrica
  la herramienta para tu negocio».

### H4 · La migración del número real (transversal, ya definida)
- Rodaje con la sombra diaria midiendo nuevo-vs-viejo + racha de cotizaciones en verde
  → cutover del número cuando Alejandro dé el OK con los números a la vista.

## Reglas que amarran todo
- La IA jamás marca plata: cobro/entrega/pagado = botón humano (permiso `solo-dueno`).
- Toda automatización nueva parte pidiendo OK y se GANA el automático con racha — el
  patrón de H1 se reusa para cualquier herramienta con-ok.
- Lo específico del rubro (PDF, repartidor) vive en el clon como conexión fabricada;
  el molde solo conoce el contrato.
