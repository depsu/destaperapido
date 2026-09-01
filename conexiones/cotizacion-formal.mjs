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
//         factura ("si" default → +IVA en el PDF) ·
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
const conFactura = texto(args.factura).toLowerCase() !== 'no';   // con IVA por defecto
// QUÉ se cotiza (16-ago): antes siempre decía «baño químico»; ahora el panel puede
// mandar el ítem elegido (ducha portátil, baño sin lavamanos, flete, limpieza extra).
// Singular/plural sin diccionario: «2 ducha portátil x2» sería feo → «x2» al final.
const tipoItem = texto(args.tipo_item) || 'baño químico';
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

// ── el config del PDF (contrato de generar_cotizacion.py) ─────────────────────
const campos = [['Nombre', nombre]];
if (comuna !== '') campos.push(['Comuna', `${comuna}, RM`]);
if (plazo !== '') campos.push(['Período de arriendo', plazo]);
if (email !== '') campos.push(['Email', email]);
/* LOS DATOS DE FACTURA IMPRESOS (1-sep, Felipe Casajuana: dio su RUT para que la
   jefatura aprobara — si el PDF no lo muestra, el documento queda a medias). Una sola
   línea; si la ficha trae varias (razón social + RUT + giro), se aplanan. */
const datosFactura = texto(args.datos_factura).replace(/\s*\n\s*/g, ' · ');
if (datosFactura !== '') campos.push(['Facturación', datosFactura]);
/* EVENTO NO ES ARRIENDO MENSUAL (regla del bot viejo, 14-ago): en un evento de un día
   la limpieza semanal NO aplica, y prometerla por escrito en la cotización es vender algo
   que no se hace. El plazo manda: si dice evento/fiesta/matrimonio/un día, lo incluido es
   traslado, instalación y retiro. */
const esEvento = /event|fiesta|matrimonio|cumplea|un d[ií]a|1 d[ií]a|fin de semana/i.test(plazo);
// si lo acordado EMPIEZA negando («no incluida…»), decir «Aseo incluido: no incluida»
// era una contradicción impresa (31-ago, PDF de Carlos Castro) — la etiqueta se adapta.
// Y si el texto trae un PRECIO (1-sep, Felipe Casajuana: «2 limpiezas, $60.000 cada
// una» cobradas en su propio ítem), «incluido» también mentiría: precio = no incluido.
const rotuloAseo = /^\s*(no|sin)\b/i.test(aseo) || /\$\s*\d|\d+\s*(mil|lucas?)\b/i.test(aseo)
  ? 'Aseo' : 'Aseo incluido';
const lineaAseo = aseo !== '' ? `${rotuloAseo}: ${aseo}.` : 'Limpieza semanal (cada 7 a 10 días) incluida.';
const incluido = esEvento
  ? ['Traslado, instalación y retiro incluidos.',
    // en un evento la limpieza solo se nombra si se ACORDÓ una (limpieza extra, etc.)
    ...(aseo !== '' ? [`${rotuloAseo}: ${aseo}.`] : []),
    'Papel higiénico y desodorizante incluidos.']
  : ['Despacho, instalación y retiro incluidos.',
    lineaAseo,
    'Papel higiénico y desodorizante incluidos.'];
// mayúscula inicial para el PDF («Ducha portátil»); el default queda como siempre
// si el texto YA dice «arriendo de…» no se antepone otra vez (31-ago, PDF de Carlos
// Castro: «Arriendo de Arriendo de baño químico»)
const conArriendo = (t) => (/^arriendos?\s+de/i.test(t) ? t : `Arriendo de ${t}`);
// el equipamiento pactado va pegado al título, salvo que el tipo ya lo nombre
const conEquipo = (t) => (equipoVisible !== '' && !t.toLowerCase().includes(equipoVisible)
  ? `${t} ${equipoVisible}` : t);
const itemTitulo = conEquipo(tipoItem === 'baño químico'
  ? 'Arriendo de baño químico'
  : conArriendo(tipoItem));
const config = {
  subtitulo: tipoItem === 'baño químico'
    ? 'Arriendo de baños químicos'
    : conArriendo(tipoItem),
  cliente: { titulo: 'Datos del cliente', campos },
  items: [{
    descripcion_titulo: itemTitulo,
    descripcion_bullets: [
      ...(plazo !== '' ? [`Período de arriendo: ${plazo}.`] : []),
      ...incluido,
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
    descripcion_bullets: ['Traslado por la ubicación; se cobra una sola vez.'],
    cantidad: 1,
    valor_unitario_neto: flete,
  }] : [])],
  solo_neto: !conFactura,
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
  console.log(`✓ Prueba en seco lista — ${cantidad} baño(s) · ${clp(precioNeto)} neto c/u${flete > 0 ? ` + flete ${clp(flete)}` : ''}${plazo ? ` (${plazo})` : ''}`);
  process.exit(0);
}

// SOLO POR WHATSAPP: no hay correo que enviar. El PDF ya está generado; la ruta de abajo la
// lee `adjuntar_al_chat` y se lo manda al cliente por WhatsApp. Cero Resend.
if (soloWhatsapp) {
  console.log(`PDF: ${pdfPath}`);
  console.log(`✓ Cotización lista para WhatsApp (sin correo) — ${cantidad} baño(s) · ${clp(precioNeto)} neto c/u${flete > 0 ? ` + flete ${clp(flete)}` : ''}${plazo ? ` (${plazo})` : ''}`);
  process.exit(0);
}

// ── el correo (mismo canal de siempre: enviar_cotizacion.py → Resend) ─────────
const unidad = tipoItem === 'baño químico'
  ? (cantidad > 1 ? `${cantidad} baños químicos` : 'un baño químico')
  : (cantidad > 1 ? `${tipoItem} x${cantidad}` : tipoItem);
const donde = comuna !== '' ? ` para su proyecto en ${comuna}` : '';
const totalNeto = precioNeto * cantidad;
const lineaValor = cantidad > 1
  ? `- ${unidad}: ${clp(precioNeto)} neto c/u · total ${clp(totalNeto)}${conFactura ? ', más IVA 19% (ver PDF)' : ''}`
  : (conFactura
    ? `- ${unidad}: ${clp(precioNeto)} neto (total con IVA: ${clp(Math.round(precioNeto * 1.19))})`
    : `- ${unidad}: ${clp(precioNeto)}`);
const cuerpo = [
  `Estimado/a ${nombre}:`,
  '',
  `Junto con saludar, le adjunto la cotización formal por el arriendo de ${unidad}${donde}.`,
  '',
  lineaValor,
  ...(itemExtra !== '' && precioExtra > 0
    ? [`- ${itemExtra.charAt(0).toUpperCase() + itemExtra.slice(1)}: ${clp(precioExtra)} neto.`] : []),
  ...(flete > 0 ? [`- Flete por única vez: ${clp(flete)}${conFactura ? ' neto' : ''}.`] : []),
  ...(plazo !== '' ? [`- Período: ${plazo}.`] : []),
  esEvento
    ? `- Incluye traslado, instalación, retiro${aseo !== '' ? `, aseo (${aseo})` : ''}, papel higiénico y desodorizante.`
    : `- Incluye traslado, instalación, retiro, ${aseo !== '' ? `aseo (${aseo})` : 'aseo semanal (cada 7 a 10 días)'}, papel higiénico y desodorizante.`,
  '',
  'El detalle completo está en el PDF adjunto. Para confirmar basta con responder este correo o coordinarlo por WhatsApp, y agendamos la entrega.',
  '',
  'Quedamos atentos a cualquier consulta.',
  '',
  'Saludos cordiales,',
  'Destape Rápido',
  '+56 9 3647 0112 · destaperapido.cl',
].join('\n');

const envio = spawnSync(PYTHON, [
  join(COTIZACIONES_DIR, 'scripts', 'enviar_cotizacion.py'), pdfPath, email,
  '--cliente', nombre,
  '--asunto', 'Cotización Destape Rápido — Arriendo de baño químico',
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
console.log(`✓ Cotización enviada a ${email} — ${cantidad} baño(s) · ${clp(precioNeto)} neto c/u${plazo ? ` (${plazo})` : ''}`);
