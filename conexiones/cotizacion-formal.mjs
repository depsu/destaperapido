// cotizacion-formal.mjs — CONECTOR FABRICADO de destaperapido (H2, Ruta A del cutover).
// Lo ejecuta el módulo `conexiones` de dixdybot con los args del formulario como JSON
// en el último argv. Llama al sistema de cotizaciones DE SIEMPRE (el mismo python del
// bot antiguo: generar_cotizacion.py + enviar_cotizacion.py vía Resend).
//
// REGLA DE NEGOCIO SAGRADA (Alejandro, 20-jul, igual que en el bot viejo): la cotización
// SIEMPRE va en valores MENSUALES/por período — el plazo elige la tarifa, JAMÁS multiplica.
// Y el precio es POR UNIDAD: el PDF pone cantidad × unitario y el subtotal lo calcula él.
//
// Uso: node cotizacion-formal.mjs '{"nombre":"...","email":"...","precio_neto":140000,...}'
//   args: nombre* · email* · comuna · cantidad (default 1) · plazo (texto) ·
//         precio_neto* (POR BAÑO, en pesos — SIN el flete) · flete (pesos, por única
//         vez: va como SEGUNDA LÍNEA del PDF, jamás mezclado en el unitario) ·
//         factura ("si" = +IVA · "no" = neto · vacío = PENDIENTE, neto y dicho) ·
//         asunto (texto libre para el asunto del correo, si el cliente lo pidió) ·
//         dry ("si" = genera el PDF y NO envía — para probar)
import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { tmpdir } from 'node:os';

const COTIZACIONES_DIR = '/Users/alejandroriveracarrasco/SaSS/destaperapido/cotizaciones-destape-rapido';
const PYTHON = 'python3';

const crudo = process.argv[process.argv.length - 1] ?? '{}';
let args;
try { args = JSON.parse(crudo); } catch { args = null; }
if (args === null || typeof args !== 'object') {
  console.error('args ilegibles: se espera un JSON');
  process.exit(1);
}

/* EL CINTURÓN DE LA CANCELACIÓN (8-sep, CONV 397 y 513): si llega la marca de que el
   cliente canceló, acá NO se genera ni se envía nada. Este conector EMITE (PDF +
   correo); retirar es cosa del aviso al repartidor. Le mandamos la cotización a quien
   acababa de decir «no, ya no, gracias» y el dueño tuvo que disculparse. Salida en 0,
   sin tocar nada. */
if (String(args._cancelacion ?? '').trim().toLowerCase() === 'si') {
  console.log('cancelación del cliente: no se generó ni se envió ninguna cotización');
  process.exit(0);
}

const texto = (v) => (v === undefined || v === null ? '' : String(v).trim());
const nombre = texto(args.nombre);
const email = texto(args.email);
const comuna = texto(args.comuna);
const plazo = texto(args.plazo);
/* CÓMO ESCRIBE PLATA UNA PERSONA (bug real cazado en el QA del 6-ago): escribir
   «130.000» daba $130 porque Number("130.000") = 130 → salía una cotización de ciento
   treinta PESOS. Aquí se entiende como habla un chileno: 130.000 · $130.000 · 130 mil ·
   130mil · 130k · 130 lucas · 130000. Bajo $1.000 se asume que dijo miles. */
function pesosDe(v) {
  const t = String(v ?? '').toLowerCase().trim();
  if (t === '') return 0;
  const conSufijo = /(\d[\d.,]*)\s*(mil|luca|lucas|k)\b/.exec(t);
  const crudo = conSufijo ? conSufijo[1] : t;
  // se quitan los separadores de miles (punto chileno) y el símbolo; la coma también,
  // porque nadie cotiza con decimales en pesos
  const limpio = crudo.replace(/[^\d]/g, '');
  if (limpio === '') return 0;
  let n = Number(limpio);
  if (conSufijo) n *= 1000;
  else if (n < 1000) n *= 1000;      // «130» = 130 mil, como se habla
  return Math.round(n);
}

const cantidad = Math.max(1, Math.round(Number(String(args.cantidad ?? '1').replace(/[^\d]/g, '')) || 1));
const precioNeto = pesosDe(args.precio_neto);
// EL FLETE SEPARADO (17-ago, «el bot anterior podía separarlo»): $30.000 de flete
// mezclados en el unitario hacían que el PDF dijera $170.000 el baño — mentira cara.
const flete = pesosDe(args.flete);
// EL ÍTEM EXTRA (17-ago, caso La Cisterna: baño + CABINA DE DUCHA en una misma
// cotización): una segunda línea genérica con su propio valor — sirve para la ducha,
// una limpieza extra de evento, lo que sea. Mensual como el resto, salvo que el
// título diga otra cosa.
/* «ninguno» NO es un ítem (1-sep, colegio de Colina): el agente anotó item_extra
   «ninguno» para decir «ya no lleva», el valor viejo de la limpieza seguía en la ficha,
   y el PDF salió con la línea «Ninguno — $140.000». Un texto que niega apaga el ítem
   Y su precio, igual que en avisar-repartidor. */
const itemCrudo = texto(args.item_extra);
const itemNegado = /^(no|ninguno|ninguna|nada|sin\s+\S*|0|-)$/i.test(itemCrudo);
const itemExtra = itemNegado ? '' : itemCrudo;
const precioExtra = itemNegado ? 0 : pesosDe(args.precio_extra);
/* LA FACTURA NO SE INFIERE (9-sep, A10 y T24): el campo venía con defecto «si», así que
   una ficha SIN decisión (el 69% de las fichas reales) salía con IVA en el PDF mientras el
   repartidor cobraba el neto — 19% de diferencia discutido en la puerta. Ahora son TRES
   estados: sí (IVA), no (neto) y PENDIENTE (neto, y el PDF lo dice con todas sus letras).
   Único dato que sí decide: que el cliente YA haya entregado sus datos de facturación. */
const facturaCruda = texto(args.factura).toLowerCase();
const datosFactura = texto(args.datos_factura).replace(/\s*\n\s*/g, ' · ');
const facturaDecidida = /^(s[ií]|true|con\b|requiere)/.test(facturaCruda) ? 'si'
  : (/^(no|false|sin\b)/.test(facturaCruda) || /exent/.test(facturaCruda) ? 'no'
    : (datosFactura !== '' ? 'si' : ''));
const conFactura = facturaDecidida === 'si';
const facturaPendiente = facturaDecidida === '';
// QUÉ se cotiza (16-ago): antes siempre decía «baño químico»; ahora el panel puede
// mandar el ítem elegido (ducha portátil, baño sin lavamanos, flete, limpieza extra).
// Singular/plural sin diccionario: «2 ducha portátil x2» sería feo → «x2» al final.
const tipoItem = texto(args.tipo_item) || 'baño químico';
// mayúscula inicial para el PDF («Ducha portátil»); el default queda como siempre
// si el texto YA dice «arriendo de…» no se antepone otra vez (31-ago, PDF de Carlos
// Castro: «Arriendo de Arriendo de baño químico»)
const conArriendoTxt = (t) => (/^arriendos?\s+de/i.test(t) ? t : `Arriendo de ${t}`);
/* QUÉ CLASE DE SERVICIO ES (9-sep, A13): el formulario permite cotizar «flete» o
   «limpieza extra», y el molde los envolvía igual: «Arriendo de limpieza extra», con
   traslado, retiro, papel higiénico y desodorizante incluidos. Un servicio suelto no es
   un arriendo y no incluye nada de eso. */
const esArriendo = !/^(flete|traslado)|limpieza|aseo|^retiro/i.test(tipoItem);
const nombreServicio = (t) => (/^(flete|traslado)/i.test(t) ? 'Servicio de traslado'
  : (/limpieza|aseo/i.test(t) ? 'Servicio de limpieza' : conArriendoTxt(t)));
/* EL EQUIPAMIENTO EN EL TÍTULO (1-sep, caso Felipe Casajuana: pidió expresamente CON
   LAVAMANOS y el PDF para su jefatura decía «baño químico» a secas — lo pactado tiene
   que leerse en el documento). «cualquiera» o vacío = no se imprime nada. */
const equipamiento = texto(args.equipamiento).toLowerCase();
const equipoVisible = equipamiento !== '' && !/cualquiera|da igual|indistinto/.test(equipamiento)
  ? equipamiento : '';
// EL ASEO ACORDADO (17-ago, caso JR Montajes: se negociaron 3 limpiezas semanales y el
// PDF salió con el texto fijo «cada 7 a 10 días» — un documento formal contradiciendo
// el trato). Si la ficha trae un aseo negociado, ESE va; vacío = el estándar de siempre.
const aseo = texto(args.aseo);
const dry = texto(args.dry).toLowerCase() === 'si';
/* SOLO POR WHATSAPP (18-ago, «dar la opción de solo enviar por wsp si se insiste en el
   correo»): cuando el cliente NO quiere dar su correo, se genera el PDF igual y sale por
   WhatsApp (adjuntar_al_chat lo lee de la ruta). Se activa con el flag, o simplemente
   cuando no viene correo. El correo deja de ser obligatorio; todo lo demás igual. */
const soloWhatsapp = texto(args.solo_whatsapp).toLowerCase() === 'si' || email === '';

if (nombre === '' || precioNeto <= 0) {
  console.error('faltan datos: nombre y precio neto por baño son obligatorios');
  process.exit(1);
}
if (!soloWhatsapp && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
  console.error(`ese correo no se ve válido: ${email}`);
  process.exit(1);
}

const clp = (n) => '$' + String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
// el resumen que lee el DUEÑO en la traza 🔧: decía «1 baño» aunque se cotizara un flete
const unidadResumen = !esArriendo ? (cantidad === 1 ? 'servicio' : 'servicios')
  : (cantidad === 1 ? 'baño' : 'baños');

// ── el config del PDF (contrato de generar_cotizacion.py) ─────────────────────
const campos = [['Nombre', nombre]];
/* «, RM» NO SE REGALA (9-sep, A14): la línea añadía «RM» a cualquier ubicación, y el
   negocio ya cotizó San Antonio (CONV 624) — el documento declaraba una región falsa.
   Sin región verificada se imprime la comuna sola. */
if (comuna !== '') campos.push(['Lugar del servicio', comuna]);
if (plazo !== '') campos.push([esArriendo ? 'Período de arriendo' : 'Fecha del servicio', plazo]);
if (email !== '') campos.push(['Email', email]);
/* LOS DATOS DE FACTURA IMPRESOS (1-sep, Felipe Casajuana: dio su RUT para que la
   jefatura aprobara — si el PDF no lo muestra, el documento queda a medias). Una sola
   línea; si la ficha trae varias (razón social + RUT + giro), se aplanan. */
if (datosFactura !== '') campos.push(['Facturación', datosFactura]);
/* EVENTO NO ES ARRIENDO MENSUAL (regla del bot viejo, 14-ago): en un evento de un día
   la limpieza semanal NO aplica, y prometerla por escrito en la cotización es vender algo
   que no se hace. El plazo manda: si dice evento/fiesta/matrimonio/un día, lo incluido es
   traslado, instalación y retiro.
   POR DÍAS, NO POR PALABRAS (9-sep, Alejandro: «si el mensaje es diario… dice limpieza
   incluida de 7 a 10 días, lo cual no tiene lógica»): la lista de palabras dejaba fuera
   «3 días», «5 días» o «una semana», y esos PDF salían prometiendo un ciclo semanal que
   termina después de que el baño ya se retiró. Ahora se mide el plazo: hasta 7 días es
   corto, y ahí el aseo periódico no se nombra. */

/** Cuántos días dura el arriendo, leído como lo escribe una persona. 0 = no se pudo
 *  saber (ahí manda el estándar de siempre, que es el mensual). */
function diasDePlazo(txt) {
  const t = String(txt || '').toLowerCase().trim();
  if (t === '') return 0;
  if (/mensual|permanente|indefinid|\bmes(?:es)?\b/.test(t)) return 30;
  const m = /(\d+)\s*(d[ií]as?|noches?|semanas?|quincenas?)/.exec(t);
  if (m !== null) {
    const n = Number(m[1]);
    if (/^d/.test(m[2]) || /^n/.test(m[2])) return n;
    if (/^s/.test(m[2])) return n * 7;
    return n * 15;
  }
  if (/quincen/.test(t)) return 15;
  if (/fin de semana|s[aá]bado y domingo/.test(t)) return 2;
  /* PLAZOS QUE NO SE ESCRIBEN EN DÍAS (9-sep, revisión): «8 horas», «por el día», «una
     tarde noche», «jornadas salteadas». Son el 7% de las duraciones reales de la base y
     caían en 0, o sea «mensual», y al repartidor le llegaba «Aseo: cada 7 a 10 días»
     para un arriendo de una tarde. Va ANTES del rango de fechas: «de 8 a 17 horas» son
     horas, no del 8 al 17. */
  if (/\bhoras?\b|\bhrs?\b|jornada|por el d[ií]a|\btarde\b|\bnoche\b/.test(t)) return 1;
  /* RANGOS DE FECHAS: «20 al 22 de noviembre», «del 17 de septiembre 11:00 al 20 de
     septiembre 03:00 AM». El segundo extremo tiene que traer su mes, si no «de 8 a 17»
     se leería como diez días. */
  /* EL DÍA DE LA SEMANA EN MEDIO (9-sep, A01): «del viernes 4 de septiembre al jueves
     10 de septiembre» y «miércoles 2 al sábado 5 de septiembre» caían en 0 = mensual, y
     esos dos PDF salieron prometiendo «limpieza cada 7 a 10 días» para 7 y 4 días. Son
     casos REALES de la base. El nombre del día se salta; el resto del rango no cambia. */
  const rango = /(?<![:.\d])(\d{1,2})(?![:.\d])(?:\s*de\s+[a-zá-ú]+)?(?:\s+\d{1,2}[:.]\d{2}(?:\s*(?:am|pm|hrs?|horas?))?)?\s*(?:al|a|-|hasta(?:\s+el)?)\s*(?:el\s+)?(?:(?:lunes|martes|mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo)\s+)?(?<![:.\d])(\d{1,2})(?![:.\d])\s*de\s+[a-zá-ú]+/.exec(t);
  if (rango !== null) {
    const dias = Number(rango[2]) - Number(rango[1]) + 1;
    if (dias > 0 && dias <= 31) return dias;
  }
  if (/un[ao]?\s*(?:d[ií]a|noche)|event|fiesta|matrimonio|cumplea|bautizo/.test(t)) return 1;
  if (/semana/.test(t)) return 7;
  return 0;
}
const diasPlazo = diasDePlazo(plazo);
const esEvento = diasPlazo > 0 && diasPlazo <= 7;
// «semanal», «cada 7 días», «cada 7 a 10 días»: una cadencia, no un acuerdo puntual
const aseoEsPeriodico = (t) => /semanal|cada\s*\d+\s*(?:a\s*\d+\s*)?d[ií]as?|cada\s*semana|7\s*a\s*10/i.test(t);
// en un plazo corto solo sobrevive el aseo ACORDADO (una limpieza pactada, un extra):
// la cadencia estándar heredada de la ficha se descarta en vez de imprimirse
const aseoAcordado = esEvento && aseoEsPeriodico(aseo) ? '' : aseo;
// CON FLETE COBRADO EL TRASLADO NO VA «INCLUIDO» (9-sep): el PDF ya trae su línea propia
// «Flete por única vez», así que decir «Traslado incluido» arriba se contradice solo.
const conFlete = flete > 0;
// si lo acordado EMPIEZA negando («no incluida…»), decir «Aseo incluido: no incluida»
// era una contradicción impresa (31-ago, PDF de Carlos Castro) — la etiqueta se adapta.
// Y si el texto trae un PRECIO (1-sep, Felipe Casajuana: «2 limpiezas, $60.000 cada
// una» cobradas en su propio ítem), «incluido» también mentiría: precio = no incluido.
const rotuloAseo = /^\s*(no|sin)\b/i.test(aseo) || /\$\s*\d|\d+\s*(mil|lucas?)\b/i.test(aseo)
  ? 'Aseo' : 'Aseo incluido';
const lineaAseo = aseo !== '' ? `${rotuloAseo}: ${aseo}.` : 'Limpieza cada 7 a 10 días incluida.';
/* EL TRASLADO NO SE COBRA Y SE «INCLUYE» A LA VEZ (9-sep, A04): decir «Traslado,
   instalación y retiro incluidos» y más abajo cobrar «Flete por única vez» es un
   documento contradiciéndose solo. Sin flete se dice expresamente que no hay cargo. */
const lineaTraslado = conFlete
  ? 'Instalación y retiro incluidos; el traslado va cobrado aparte, en la línea de flete.'
  : 'Entrega, instalación y retiro incluidos, sin cargo adicional de traslado.';
const incluido = esEvento
  ? [lineaTraslado,
    // en un plazo corto la limpieza solo se nombra si se ACORDÓ una (limpieza extra, etc.)
    ...(aseoAcordado !== '' ? [`${rotuloAseo}: ${aseoAcordado}.`] : []),
    'Papel higiénico y desodorizante incluidos.']
  : [lineaTraslado,
    lineaAseo,
    'Papel higiénico y desodorizante incluidos.'];
/* LA UNIDAD COMERCIAL DEL PRECIO, ESCRITA (9-sep, A06): «Período de arriendo: 3 meses»
   al lado de un valor unitario mensual hacía leer que ese valor cubría los tres meses.
   El valor NO se multiplica (regla sagrada): lo que se explicita es a qué corresponde. */
const sustantivoUnidad = /ba[ñn]o/i.test(tipoItem) ? 'baño'
  : (/ducha/i.test(tipoItem) ? 'ducha' : 'unidad');
const lineaUnidad = !esArriendo ? ''
  : (esEvento
    ? `Valor por ${sustantivoUnidad} por todo el período cotizado: ${clp(precioNeto)} neto.`
    : (diasPlazo >= 8 && diasPlazo <= 29 && plazo !== ''
      ? `Valor por ${sustantivoUnidad} por el período de ${plazo}: ${clp(precioNeto)} neto.`
      : `Valor por ${sustantivoUnidad} y por mes: ${clp(precioNeto)} neto.`));
// el equipamiento pactado va pegado al título, salvo que el tipo ya lo nombre
const conEquipo = (t) => (equipoVisible !== '' && !t.toLowerCase().includes(equipoVisible)
  ? `${t} ${equipoVisible}` : t);
const itemTitulo = conEquipo(nombreServicio(tipoItem));
const config = {
  subtitulo: esArriendo
    ? (tipoItem === 'baño químico' ? 'Arriendo de baños químicos' : conArriendoTxt(tipoItem))
    : nombreServicio(tipoItem),
  cliente: { titulo: 'Datos del cliente', campos },
  items: [{
    descripcion_titulo: itemTitulo,
    descripcion_bullets: [
      ...(plazo !== ''
        ? [esArriendo ? `Período de arriendo: ${plazo}.` : `Fecha o período del servicio: ${plazo}.`]
        : []),
      ...(lineaUnidad !== '' ? [lineaUnidad] : []),
      // un servicio suelto (flete, limpieza) NO lleva lo que incluye un arriendo
      ...(esArriendo ? incluido : []),
    ],
    cantidad,
    valor_unitario_neto: precioNeto,
  },
  // el ÍTEM EXTRA acordado (una ducha, una limpieza extra…), con su propia línea
  ...(itemExtra !== '' && precioExtra > 0 ? [{
    descripcion_titulo: itemExtra.charAt(0).toUpperCase() + itemExtra.slice(1),
    descripcion_bullets: [],
    cantidad: 1,
    valor_unitario_neto: precioExtra,
  }] : []),
  // la línea del flete por única vez, aparte y a la vista (como el bot viejo)
  ...(flete > 0 ? [{
    descripcion_titulo: 'Flete por única vez',
    descripcion_bullets: ['Cubre la entrega y el retiro por la ubicación; se cobra una sola vez.'],
    cantidad: 1,
    valor_unitario_neto: flete,
  }] : [])],
  solo_neto: !conFactura,
  /* LAS CONDICIONES QUE EL PDF TRAÍA FIJAS (9-sep, A08 · A09 · A10). Antes iban en el
     generador para TODA cotización, dijeran lo que dijeran el chat y el pedido:
       · «Coordinada dentro de 24 a 48 horas hábiles tras la aceptación» — contradecía
         una entrega para hoy y hacía creer que un evento de octubre se despacha en
         septiembre. Sin fecha acordada, lo honesto es decir que está por coordinar.
       · «Transferencia electrónica o depósito bancario» — el negocio cobra CONTRA
         ENTREGA, en efectivo o transferencia, sin adelanto (persona/base.md). El PDF
         omitía el efectivo y no decía cuándo se paga; CONV 659 terminó preguntando si
         había que transferir primero.
       · «Facturación: Electrónica» aparecía incluso en una cotización SIN factura.
     Estos textos viajan desde acá, que es donde se sabe lo del pedido. */
  condiciones_textos: {
    pago: 'Pago contra entrega, en efectivo o transferencia. No se solicita adelanto para reservar.',
    facturacion: conFactura
      ? 'Electrónica, a la razón social que indique el cliente.'
      : (facturaPendiente
        ? 'Documento tributario pendiente de confirmar. Si se emite factura, se agrega IVA (19%) al total.'
        : 'Sin factura: los valores indicados son netos, sin IVA.'),
    entrega: 'Fecha y horario de entrega pendientes de coordinación.',
  },
  /* A22: el mismo PDF se manda a veces SOLO por WhatsApp, y el recuadro de aceptación
     mandaba a «responder este correo» — una instrucción sobre un correo que no existe. */
  ...(soloWhatsapp ? { aceptacion_texto:
    'Para confirmar el servicio basta con <b>responder por este WhatsApp</b> indicando su '
    + 'conformidad. No es necesario firmar ni imprimir el documento. Apenas tengamos su '
    + 'confirmación, coordinamos la entrega.' } : {}),
};

/* EL NOMBRE DEL ARCHIVO LO LEE EL CLIENTE (14-ago): al mandarse por WhatsApp, el PDF
   aparece con su nombre en la burbuja — «coti-1786732389839.pdf» se veía a desechable.
   Va el nombre del negocio y el del cliente, sin acentos ni espacios raros. La carpeta
   sí lleva el timestamp: así dos cotizaciones para el mismo nombre no se pisan. */
const carpeta = join(tmpdir(), 'dixdybot-cotizaciones', String(Date.now()));
mkdirSync(carpeta, { recursive: true });
const limpio = nombre.normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^A-Za-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40);
const cfgPath = join(carpeta, 'config.json');
const pdfPath = join(carpeta, `Cotizacion-Destape-Rapido${limpio === '' ? '' : `-${limpio}`}.pdf`);
writeFileSync(cfgPath, JSON.stringify(config, null, 2));

const gen = spawnSync(PYTHON,
  [join(COTIZACIONES_DIR, 'scripts', 'generar_cotizacion.py'), cfgPath, pdfPath],
  { encoding: 'utf8' });
if (gen.status !== 0 || !existsSync(pdfPath)) {
  console.error(`no se generó el PDF: ${(gen.stderr || gen.stdout || '').slice(0, 300)}`);
  process.exit(1);
}

if (dry) {
  console.log(`PDF generado (SIN enviar): ${pdfPath}`);
  console.log(`✓ Prueba en seco lista — ${cantidad} ${unidadResumen} · ${clp(precioNeto)} neto c/u${flete > 0 ? ` + flete ${clp(flete)}` : ''}${plazo ? ` (${plazo})` : ''}`);
  process.exit(0);
}

// SOLO POR WHATSAPP: no hay correo que enviar. El PDF ya está generado; la ruta de abajo la
// lee `adjuntar_al_chat` y se lo manda al cliente por WhatsApp. Cero Resend.
if (soloWhatsapp) {
  console.log(`PDF: ${pdfPath}`);
  console.log(`✓ Cotización lista para WhatsApp (sin correo) — ${cantidad} ${unidadResumen} · ${clp(precioNeto)} neto c/u${flete > 0 ? ` + flete ${clp(flete)}` : ''}${plazo ? ` (${plazo})` : ''}`);
  process.exit(0);
}

// ── el correo (mismo canal de siempre: enviar_cotizacion.py → Resend) ─────────
const unidad = tipoItem === 'baño químico'
  ? (cantidad > 1 ? `${cantidad} baños químicos` : 'un baño químico')
  // un servicio suelto se nombra por su nombre, no por la etiqueta del formulario
  : (!esArriendo ? (cantidad > 1 ? `${nombreServicio(tipoItem)} x${cantidad}` : nombreServicio(tipoItem))
    : (cantidad > 1 ? `${tipoItem} x${cantidad}` : tipoItem));
const donde = comuna !== '' ? ` para su proyecto en ${comuna}` : '';
/* EL «TOTAL» QUE NO ERA EL TOTAL (9-sep, A07): la línea decía «total con IVA» sobre el
   puro arriendo, y la ducha, la limpieza extra y el flete aparecían más abajo — el
   cliente tenía que sumar solo, y el número grande del correo no coincidía con el del
   PDF ni con lo que cobra el repartidor. Ahora el correo desglosa igual que el PDF. */
const subtotalArriendo = precioNeto * cantidad;
const montoExtra = itemExtra !== '' && precioExtra > 0 ? precioExtra : 0;
const netoPedido = subtotalArriendo + montoExtra + flete;
const ivaPedido = Math.round(netoPedido * 0.19);
const lineaValor = cantidad > 1
  ? `- ${unidad}: ${clp(precioNeto)} neto c/u · subtotal ${clp(subtotalArriendo)}`
  : `- ${unidad}: ${clp(precioNeto)} neto`;
// A05: «Incluye … aseo (no incluido)» era una contradicción impresa; el rótulo se adapta
// igual que en el PDF, y lo que no está incluido se dice fuera de la lista de incluidos.
const aseoDelCorreo = esEvento ? aseoAcordado : aseo;
const hayAseoAcordado = aseoDelCorreo !== '';
const aseoDentroDeIncluye = hayAseoAcordado && rotuloAseo === 'Aseo incluido';
// el estándar «cada 7 a 10 días» SOLO cuando no hay nada acordado y el plazo lo justifica:
// nombrarlo además del acuerdo dejaba el correo diciendo dos cosas distintas del mismo aseo
const textoAseoIncluye = aseoDentroDeIncluye ? `, aseo (${aseoDelCorreo})`
  : (hayAseoAcordado || esEvento ? '' : ', aseo cada 7 a 10 días');
const lineaIncluye = esArriendo
  ? `- Incluye ${conFlete ? '' : 'traslado, '}instalación, retiro${textoAseoIncluye}, papel higiénico y desodorizante.`
  : '';
const lineaAseoAparte = esArriendo && hayAseoAcordado && !aseoDentroDeIncluye
  ? `- ${rotuloAseo}: ${aseoDelCorreo}.` : '';
const cierreTotal = conFactura
  ? [`- Neto del pedido: ${clp(netoPedido)}`, `- IVA (19%): ${clp(ivaPedido)}`,
    `- Total a pagar con factura: ${clp(netoPedido + ivaPedido)}`]
  : (facturaPendiente
    ? [`- Total a pagar: ${clp(netoPedido)} neto`,
      '- El documento tributario queda pendiente de confirmar: si se emite factura, se agrega IVA (19%).']
    : [`- Total a pagar: ${clp(netoPedido)}, valores netos sin factura`]);
const cuerpo = [
  `Estimado/a ${nombre}:`,
  '',
  `Junto con saludar, le adjunto la cotización formal por ${esArriendo ? `el arriendo de ${unidad}` : nombreServicio(tipoItem).toLowerCase().replace(/^servicio/, 'el servicio')}${donde}.`,
  '',
  lineaValor,
  ...(montoExtra > 0
    ? [`- ${itemExtra.charAt(0).toUpperCase() + itemExtra.slice(1)}: ${clp(precioExtra)} neto.`] : []),
  ...(flete > 0 ? [`- Flete por única vez, entrega y retiro: ${clp(flete)} neto.`] : []),
  ...(plazo !== '' ? [`- ${esArriendo ? 'Período' : 'Fecha del servicio'}: ${plazo}.`] : []),
  ...(lineaIncluye !== '' ? [lineaIncluye] : []),
  ...(lineaAseoAparte !== '' ? [lineaAseoAparte] : []),
  '',
  ...cierreTotal,
  '',
  'El pago es contra entrega, en efectivo o transferencia, sin adelanto.',
  '',
  'El detalle completo está en el PDF adjunto. Para confirmar basta con responder este correo o coordinarlo por WhatsApp, y agendamos la entrega.',
  '',
  'Quedamos atentos a cualquier consulta.',
  '',
  'Saludos cordiales,',
  'Destape Rápido',
  '+56 9 3647 0112 · destaperapido.cl',
].join('\n');
/* EL ASUNTO (9-sep, A13 y A15): era fijo, «Arriendo de baño químico», aunque se cotizara
   una ducha, un flete o una limpieza; y traía raya larga, que en esta casa no se usa.
   Además el cliente puede pedir un asunto suyo («PMGD San Antonio Malvilla», CONV 624):
   el bot prometió mandarlo así y el conector ni siquiera recibía el dato. */
const asuntoPedido = texto(args.asunto);
const asunto = `Cotización Destape Rápido: ${asuntoPedido !== '' ? asuntoPedido : nombreServicio(tipoItem)}`;

const envio = spawnSync(PYTHON, [
  join(COTIZACIONES_DIR, 'scripts', 'enviar_cotizacion.py'), pdfPath, email,
  '--cliente', nombre,
  '--asunto', asunto,
  '--mensaje', cuerpo,
], { encoding: 'utf8' });
if (envio.status !== 0) {
  console.error(`el PDF se generó pero el correo NO salió: ${(envio.stderr || envio.stdout || '').slice(0, 300)}`);
  process.exit(1);
}
console.log((envio.stdout || '').trim().split('\n').slice(-2).join(' · '));
// la ruta del PDF va SIEMPRE (no solo en seco): si la herramienta declara
// `adjuntar_al_chat`, el panel la lee de aquí y le manda el mismo PDF al cliente por
// WhatsApp, como hacía el bot antiguo (correo + WhatsApp).
console.log(`PDF: ${pdfPath}`);
console.log(`✓ Cotización enviada a ${email} — ${cantidad} ${unidadResumen} · ${clp(precioNeto)} neto c/u${plazo ? ` (${plazo})` : ''}`);
