// avisar-repartidor.mjs — CONECTOR FABRICADO de destaperapido (H3, Ruta A del cutover).
// El DESPACHO de una entrega, calcado del flujo del CRM viejo pero disparado desde el
// panel dixdybot: reusa `prepararEntrega` del sistema de siempre (arma la entrega,
// renderiza la tarjeta en python y la sube a Supabase vía bridge/entrega_bridge.py) y
// manda el aviso por el CANAL DEL DIXDYBOT (API del panel) — desde el cutover del
// 13-ago el número vive ahí; el outbox del bot viejo ya no tiene quién lo drene.
// El rastro sigue quedando en envios.jsonl (yaDespachado lo consulta).
//
// Uso: node avisar-repartidor.mjs '{"nombre":"...","direccion":"...","fecha":"...",...}'
//   args: nombre* · direccion* · fecha* (de entrega; entiende español) · hora ·
//         comuna · cantidad (default 1) · duracion (texto: «mensual», «2 semanas») ·
//         telefono_cliente · maps_url · aseo (frecuencia acordada) ·
//         precio_neto (POR BAÑO, SIN flete) · flete (por única vez) · factura ("si"
//         default → el COBRAR va con IVA; "no" = solo neto) — con ellos el aviso trae
//         el 💵 COBRAR con su desglose, como el bot antiguo (17-ago) ·
//         mensaje (reemplaza el aviso automático) ·
//         dry ("si" = arma y muestra TODO sin subir ni avisar) ·
//         _convId (lo inyecta el panel: enlaza el chat de origen)
import { readFileSync, writeFileSync } from 'node:fs';
import { prepararEntrega } from '/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/src/integracion.js';
import { logEnvio } from '/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/src/store.js';

// El panel dixdybot envía por el canal wa-baileys (el dueño del número desde el 13-ago).
// hablarleAlCliente exige que la conversación exista en bot.db — la del repartidor está
// migrada por el espejo, y la del cliente existe porque el despacho nace de su chat.
const PANEL_URL = process.env.DIXDYBOT_PANEL_URL || 'http://127.0.0.1:8793';

async function enviarPorDixdybot(convId, textoMensaje) {
  const res = await fetch(`${PANEL_URL}/api/chats/${encodeURIComponent(convId)}/enviar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ texto: textoMensaje }),
  }).catch((e) => { throw new Error(`el panel dixdybot no contesta (${e.message})`); });
  const cuerpo = await res.json().catch(() => ({}));
  if (!res.ok || cuerpo.ok !== true) {
    throw new Error(`el panel no pudo enviar a ${convId}: ${cuerpo.error || `HTTP ${res.status}`}`);
  }
  // «ok» significa que el panel lo GUARDÓ; «entregado» que de verdad salió. Confundirlos
  // era reportar «✓ aviso enviado» con el mensaje muerto por tope/red y el baño sin
  // repartidor (caso conexiones-ok-true-sin-entregar, minería 14-ago).
  if (cuerpo.entregado !== true) {
    throw new Error(`el panel guardó el aviso a ${convId} pero NO confirmó la entrega`
      + (cuerpo.motivo ? ` (motivo: ${cuerpo.motivo})` : '')
      + ' — revisa el chat del repartidor y reintenta');
  }
  return cuerpo;
}

const crudo = process.argv[process.argv.length - 1] ?? '{}';
let args;
try { args = JSON.parse(crudo); } catch { args = null; }
if (args === null || typeof args !== 'object') {
  console.error('args ilegibles: se espera un JSON');
  process.exit(1);
}
const texto = (v) => (v === undefined || v === null ? '' : String(v).trim());

const nombre = texto(args.nombre);
// la dirección EXACTA o el LINK del mapa (16-ago): al repartidor le sirve cualquiera de
// las dos — un cliente que manda su ubicación por Maps/Waze/WhatsApp no puede frenar el
// despacho por no dictar la calle. Si solo hay link, el link ES la dirección.
const mapsUrl = texto(args.maps_url);
const direccion = texto(args.direccion) || mapsUrl;
const fecha = texto(args.fecha);

/* La fecha COMO SE DICE, no como se guarda (19-ago). Al cliente le llegaba «📅 2026-08-24»
   en su confirmación: un dato de máquina en el único mensaje que él va a releer para saber
   qué día lo esperan. El resumen del repartidor ya la escribía bonita; esta faltaba. */
const DIAS_ES = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
const MESES_ES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
  'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];

function fechaLegible(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(iso || '').trim());
  if (m === null) return String(iso || '');        // ya venía en palabras: se respeta
  const d = new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  if (Number.isNaN(d.getTime())) return String(iso);
  return `${DIAS_ES[d.getDay()]} ${d.getDate()} de ${MESES_ES[d.getMonth()]}`;
}
const dry = texto(args.dry).toLowerCase() === 'si';
/* CANCELACIÓN (23-ago, caso Paola: «me cancelaron la cuestión» y la tarjeta siguió en el
   panel del repartidor, sin aviso — el dueño la sacó a mano). Es un aviso best-effort por
   el jid del chat: NO exige el formulario completo, no crea entrega, y retira la tarjeta
   del sistema del repartidor por la misma vía con la que él la borra (eliminado=true). */
const esCancelacion = texto(args._cancelacion) === 'si';

const telefonoCliente = texto(args.telefono_cliente);
// una NOTA al repartidor (rama corta de abajo) tampoco exige el formulario completo
const esNota = texto(args.nota_cambio) !== '';
if (!esCancelacion && !esNota
  && (nombre === '' || direccion === '' || fecha === '' || telefonoCliente === '')) {
  console.error('faltan datos: nombre, teléfono del cliente, fecha de entrega y la '
    + 'dirección (exacta o link de Maps/Waze/WhatsApp) son obligatorios');
  process.exit(1);
}

// el chat de origen (si el despacho nace de un chat del panel): su jid enlaza la entrega
const convId = texto(args._convId);
const jid = convId.startsWith('wa-baileys:') ? convId.slice('wa-baileys:'.length) : '';
/* Los ENLACES viven ARRIBA de la rama de cancelación a propósito: `const` no se iza y
   la primera versión de esta rama leyó ENLACES_FILE antes de que existiera — el catch se
   tragó el ReferenceError y toda cancelación salía «sin enlace» (el MISMO TDZ que ya
   mordió el 19-ago con esCorreccionCliente; segunda vez, ahora queda dicho). */
const ENLACES_FILE = '/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/data/enlaces.json';

function leerEnlaces() {
  try { return JSON.parse(readFileSync(ENLACES_FILE, 'utf8')); }
  catch { return { links: {}, rechazos: {} }; }
}

function enlaceDe(jidCliente) {
  if (!jidCliente) return null;
  const e = leerEnlaces();
  return (e.links && e.links[jidCliente]) || null;
}

function guardarEnlace(jidCliente, entregaId) {
  if (!jidCliente || !entregaId) return;
  try {
    const e = leerEnlaces();
    e.links = e.links || {};
    e.links[jidCliente] = entregaId;
    writeFileSync(ENLACES_FILE, JSON.stringify(e, null, 2));
  } catch (err) {
    console.error(`⚠️ no pude guardar el enlace de la entrega: ${err.message}`);
  }
}

// LA NOTA AL REPARTIDOR (28-ago, caso Fernando: «ajustar el mensaje al repartidor…
// a las 9:30 más tardar» era imposible sin re-despachar todo). Rama corta: manda el
// aviso por WhatsApp al repartidor con el contexto de la entrega enlazada (si existe)
// y termina. No edita la tarjeta del sistema — eso sigue siendo del despacho-corrección.
const notaCambio = texto(args.nota_cambio);
if (notaCambio !== '' && !esCancelacion) {
  const entregaId = enlaceDe(jid);
  const quien = texto(args.nombre);
  const donde = [texto(args.direccion), texto(args.comuna)].filter(Boolean).join(', ');
  const cabeza = entregaId !== null
    ? `🔄 CAMBIO en una entrega ya agendada${quien ? ` (${quien}` + (donde ? ` — ${donde}` : '') + ')' : ''}:`
    : `📣 Aviso${quien ? ` sobre ${quien}` + (donde ? ` (${donde})` : '') : ''}:`;
  const avisoNota = `${cabeza}
${notaCambio}`;
  if (dry) {
    console.log('— ASÍ SALDRÍA LA NOTA AL REPARTIDOR (prueba en seco) —');
    console.log(avisoNota);
    process.exit(0);
  }
  /* `config` no existe en este archivo (bug 28-ago, primera corrección real): el número
     del repartidor vive en el .env del bot de siempre — la MISMA fuente que ya usa la
     rama de cancelación, así las dos no pueden apuntar a repartidores distintos. */
  const envNota = readFileSync('/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/.env', 'utf8');
  const mNota = /^REPARTIDOR_NUMERO=([0-9+ ]+)/m.exec(envNota);
  const repTelNota = mNota ? mNota[1].replace(/\D/g, '') : '';
  if (!repTelNota) { console.error('no hay número de repartidor configurado'); process.exit(1); }
  await enviarPorDixdybot(`wa-baileys:${repTelNota}@s.whatsapp.net`, avisoNota);
  logEnvio({ jid: jid || 'panel-dixdybot', tipo: 'entrega',
    detalle: { repartidor: repTelNota, nota_cambio: notaCambio,
      entrega_id: entregaId || null, origen: 'dixdybot-nota' } });
  console.log(`✓ Nota avisada al repartidor (+${repTelNota})`
    + (entregaId !== null ? ' sobre su entrega ya agendada'
      : ' — ojo: este chat no tiene entrega en el sistema todavía')
    + '. La tarjeta del sistema NO cambió: si el dato debe quedar ahí, corrige el despacho.');
  process.exit(0);
}

if (esCancelacion) {
  const { execFileSync } = await import('node:child_process');
  const entregaId = enlaceDe(jid);
  const cita = texto(args._cita);
  // 1 · retirar la tarjeta del sistema (soft-delete, la misma vía del botón del dueño)
  let tarjetaFuera = false;
  if (entregaId && !dry) {
    try {
      execFileSync('python3', ['-c', [
        'import sys',
        `sys.path.insert(0, '/Users/alejandroriveracarrasco/SaSS/destaperapido/cotizaciones-destape-rapido/resumen-repartidor/scripts')`,
        'import sync_entregas_supabase as sync',
        `sync.upsert([{'id': '${entregaId}', 'eliminado': True}])`,
        "print('ok')",
      ].join('\n')], { timeout: 30_000 });
      tarjetaFuera = true;
    } catch (e) {
      console.error(`⚠️ no pude retirar la tarjeta del sistema: ${String(e.message || e).slice(0, 200)}`);
    }
  }
  // 2 · el 🚫 al repartidor — el número explícito del .env del bot de siempre manda
  const envViejo = readFileSync('/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/.env', 'utf8');
  const mRep = /^REPARTIDOR_NUMERO=([0-9+ ]+)/m.exec(envViejo);
  const repTel = mRep ? mRep[1].replace(/\D/g, '') : '';
  const partes = [`🚫 CANCELADA — ${nombre || 'una entrega'}${texto(args.comuna) ? ` (${texto(args.comuna)})` : ''}`];
  if (fecha !== '') partes.push(`📅 Era para: ${fechaLegible(fecha)}`);
  if (cita !== '') partes.push(`💬 El cliente: «${cita}»`);
  partes.push('');
  partes.push(tarjetaFuera
    ? 'La tarjeta ya fue retirada de tu lista — no hay que ir.'
    : (dry && entregaId ? 'La tarjeta se retiraría del sistema (prueba en seco).'
      : (entregaId
        ? 'OJO: no pude retirar la tarjeta del sistema — bórrala tú de la lista. No hay que ir.'
        : 'No encontré tarjeta enlazada de este chat — si la ves en tu lista, bórrala. No hay que ir.')));
  const avisoCancel = partes.join('\n');
  if (dry) {
    console.log('— ASÍ SALDRÍA EL 🚫 AL REPARTIDOR (prueba en seco, nada salió) —');
    console.log(avisoCancel);
    console.log(`\n✓ Prueba en seco · entrega enlazada: ${entregaId || 'ninguna'} · repartidor: ${repTel || 'SIN CONFIGURAR'}`);
    process.exit(0);
  }
  if (repTel === '') { console.error('no hay número de repartidor configurado'); process.exit(1); }
  await enviarPorDixdybot(`wa-baileys:${repTel}@s.whatsapp.net`, avisoCancel);
  logEnvio({ jid: jid || 'panel-dixdybot', tipo: 'entrega',
    detalle: { repartidor: repTel, cancelacion: true, entrega_id: entregaId || null,
      tarjeta_retirada: tarjetaFuera, cita, origen: 'dixdybot-cancelacion' } });
  console.log(`✓ Cancelación avisada al repartidor (+${repTel})`
    + (tarjetaFuera ? ' y tarjeta retirada del sistema'
      : (entregaId ? ' — la tarjeta NO se pudo retirar: que la borre del panel' : ' (sin tarjeta enlazada)')));
  process.exit(0);
}

// plata como la escribe una persona (mismo criterio de cotizacion-formal.mjs):
// «140.000» son 140 mil pesos, «30» son 30 mil, «140000» es literal
function pesosDe(v) {
  const t = String(v ?? '').toLowerCase().trim();
  if (t === '') return 0;
  const conSufijo = /(\d[\d.,]*)\s*(mil|luca|lucas|k)\b/.exec(t);
  const limpio = (conSufijo ? conSufijo[1] : t).replace(/[^\d]/g, '');
  if (limpio === '') return 0;
  let n = Number(limpio);
  if (conSufijo) n *= 1000;
  else if (n < 1000) n *= 1000;
  return Math.round(n);
}

// la forma `d` que construirEntrega entiende — las MISMAS llaves del sistema viejo.
// precio_clp/flete_clp/requiere_factura arman el 💵 COBRAR con desglose e IVA en el
// resumen del repartidor; sin ellos el aviso salía sin precio (17-ago).
const precioNeto = pesosDe(args.precio_neto);
const flete = pesosDe(args.flete);
const conFactura = texto(args.factura).toLowerCase() !== 'no';   // con IVA por defecto
// EL EQUIPAMIENTO ACORDADO (27-ago, política del lavamanos): si el cliente lo exigió con
// lavamanos (o aceptó la versión sin), viaja como tipo_uso → notas → «📝 Notas:» del
// resumen del repartidor y la tarjeta — para que no llegue con la unidad equivocada y
// se la devuelvan. Va por el canal de notas a propósito: cero cambios al sistema viejo.
const equipamiento = texto(args.equipamiento);
// EL ÍTEM EXTRA (30-ago, caso Carlos Argomedo): pidió baño + DUCHA plástica y el
// despacho subió solo el baño — el ítem extra de la ficha jamás viajaba. Va por el
// MISMO canal de notas: el repartidor tiene que cargar la ducha en el camión.
const itemExtraCrudo = texto(args.item_extra);
// «no», «ninguno», «sin extras»… no son un ítem: nada que cargar al camión
const itemExtra = /^(no|ninguno|nada|sin( extras?| ítems?| items?)?|n\/a|-+)$/i
  .test(itemExtraCrudo) ? '' : itemExtraCrudo;
const valorItem = pesosDe(args.valor_item_extra);
const notasEquipo = equipamiento !== '' ? `EQUIPO: ${equipamiento.toUpperCase()}` : '';
const d = {
  direccion,
  fecha_entrega: fecha,
  hora: texto(args.hora) || undefined,
  comuna: texto(args.comuna) || undefined,
  cantidad_banos: Math.max(1, Math.round(Number(args.cantidad) || 1)),
  duracion: texto(args.duracion) || undefined,
  telefono_contacto: telefonoCliente || undefined,
  // quién recibe en terreno (1-sep, colegio de Colina: el director recepcionaba y el
  // aviso al repartidor no lo llevaba) — construirEntrega ya sabe pintarlos
  contacto_respaldo: texto(args.contacto_respaldo) || undefined,
  telefono_respaldo: texto(args.telefono_respaldo) || undefined,
  maps_url: texto(args.maps_url) || undefined,
  aseo: texto(args.aseo) || undefined,
  ...(notasEquipo !== '' ? { tipo_uso: notasEquipo } : {}),
  // el ítem extra como EXTRA de verdad (31-ago, caso Carlos Castro: el COBRAR salía
  // sin la limpieza y el repartidor habría cobrado $154.700 en vez de $196.350):
  // integracion.js lo suma al monto, lo desglosa y lo nombra en el servicio
  ...(itemExtra !== '' ? { extras: [{ descripcion: itemExtra, precio_clp: valorItem }] } : {}),
  // …y si es una LIMPIEZA CON FECHA, además entra a la agenda de limpiezas de la
  // tarjeta (1-sep, caso colegio Colina): el repartidor la ve ese día, con su valor y
  // la nota de que ya se cobró junto con la entrega — para que no la cobre de nuevo
  ...(texto(args.fecha_limpieza) !== '' && itemExtra !== '' && /limpieza|aseo/i.test(itemExtra)
    ? { limpiezas: [{ fecha: texto(args.fecha_limpieza).slice(0, 10), etiqueta: itemExtra,
      tipo: 'extra', ...(valorItem > 0 ? { valor: valorItem } : {}),
      nota: 'se cobra junto con la entrega — no cobrar aparte' }] } : {}),
  ...(precioNeto > 0 ? { precio_clp: precioNeto } : {}),
  ...(flete > 0 ? { flete_clp: flete } : {}),
  requiere_factura: conFactura,
};

// LOS DATOS DE LA FACTURA (17-ago, foto de Alfredo): llegan en UNA línea de la ficha
// («razón social · RUT · giro · domicilio») y el resumen del repartidor los pinta en su
// bloque 🧾 — antes decía «datos pendientes» aunque el cliente ya los había mandado.
const datosFactura = texto(args.datos_factura);
if (conFactura && datosFactura !== '') {
  const rut = (/\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b/.exec(datosFactura) || [''])[0];
  const partes = datosFactura.split('·').map((p) => p.trim()).filter((p) => p !== '');
  const sinRut = partes.filter((p) => !rut || !p.includes(rut));
  const giroIdx = sinRut.findIndex((p) => /^giro/i.test(p));
  const giro = giroIdx >= 0 ? sinRut[giroIdx].replace(/^giro:?\s*/i, '') : '';
  const resto = sinRut.filter((_, i) => i !== giroIdx);
  d.factura = {
    ...(resto[0] ? { razon_social: resto[0].replace(/^raz[oó]n social:?\s*/i, '') } : {}),
    ...(rut ? { rut } : {}),
    ...(giro ? { giro } : {}),
    ...(resto[1] ? { direccion: resto.slice(1).join(' · ') } : {}),
  };
}

/* ── CORREGIR UNA ENTREGA, NO DUPLICARLA (19-ago) ────────────────────────────────
   El bot anterior distinguía «entrega nueva» de «cambio»: guardaba el mapa jid → id de
   entrega en data/enlaces.json y, al re-despachar, REUSABA ese id (así el upsert modifica
   la tarjeta en vez de crear otra) y mandaba un WhatsApp distinto, el 🔄 de actualización.
   El conector nuevo no hacía nada de eso: como el id se arma con la fecha de HOY, un
   cambio al día siguiente creaba una SEGUNDA tarjeta y al repartidor le llegaba otro
   «🚚 ENTREGA» idéntico, sin forma de saber cuál valía. Ya pasó de verdad: la clienta
   Dominga tiene dos tarjetas para el mismo trabajo (30-jul y 19-ago).
   Se reusa el MISMO enlaces.json del sistema de siempre: una sola fuente para los dos. */

/** El aviso de CAMBIO: corto y solo con lo que importa. El repartidor ya tiene la tarjeta;
 *  lo que necesita saber es QUÉ cambió, no releer todo. */
function mensajeDeCambio() {
  const partes = [`🔄 CAMBIO en la entrega — ${nombre}`];
  const comuna = texto(args.comuna);
  if (comuna !== '') partes.push(comuna);
  partes.push('');
  partes.push(`📅 Ahora: ${fechaLegible(fecha)}${texto(args.hora) === '' ? '' : ` · ${texto(args.hora)}`}`);
  const n2 = Math.max(1, Math.round(Number(args.cantidad) || 1));
  partes.push(`🚽 ${n2} baño${n2 === 1 ? '' : 's'} químico${n2 === 1 ? '' : 's'}${itemExtra !== '' ? ` + ${itemExtra}` : ''}`);
  if (direccion !== '') partes.push(`📍 ${direccion}`);
  const maps = texto(args.maps_url);
  if (maps !== '') partes.push(`🗺️ ${maps}`);
  partes.push('');
  partes.push('La tarjeta del sistema ya quedó actualizada con este cambio.');
  return partes.join('\n');
}

// La CONFIRMACIÓN AL CLIENTE (12-ago, pedido del dueño: el flujo viejo también se la
// mandaba). Editable vía `mensaje_cliente`; 'no' = no mandarle nada; vacío = la de
// siempre, calcada del panel del CRM viejo (mensajeClienteDefault).
const n = Math.max(1, Math.round(Number(args.cantidad) || 1));
/* La confirmación al cliente se arma ANTES del try, así que pregunta por su cuenta si esto
   es una corrección: «le confirmo» y «le corrijo» no dicen lo mismo, y el cliente que ya
   recibió una confirmación se merece saber que esta la reemplaza. */
const esCorreccionCliente = () => enlaceDe(jid) !== null || texto(args._yaSalio) === 'si';
const confirmacionCliente = (() => {
  const pedido = texto(args.mensaje_cliente);
  if (pedido.toLowerCase() === 'no') return '';
  if (pedido !== '') return pedido;
  // «a las 10:00» pero «en la tarde» sin el «a las» (una franja no es una hora exacta)
  const hora = texto(args.hora);
  const horaTxt = hora === '' ? '' : (/^\d{1,2}:\d{2}$/.test(hora) ? ` a las ${hora}` : `, ${hora}`);
  // EL TIEMPO DE USO en la confirmación (28-ago, pedido de Alejandro con el caso de los
  // 7 baños de Peñalolén): «me gustaría agregar el tiempo de uso... 1 día... 1 mes» —
  // el cliente confirma mejor cuando ve TODO el trato junto, plazo incluido.
  // ⏱ en minúscula y sin re-nombrar fechas que ya van en la línea 📅 (caso Pilar: decía
  // «Por Una noche: sábado 5... 04:00» — el detalle largo queda mejor solo hasta 60 chars)
  let duracionTxt = texto(args.duracion);
  if (duracionTxt !== '') {
    duracionTxt = duracionTxt.charAt(0).toLowerCase() + duracionTxt.slice(1);
    const corte = duracionTxt.search(/[:(]/);
    if (corte > 0) duracionTxt = duracionTxt.slice(0, corte).trim();
  }
  // la comuna solo si la dirección no la trae ya (salía «Providencia, Providencia»)
  const comunaTxt = texto(args.comuna);
  const conComuna = comunaTxt !== ''
    && !direccion.toLowerCase().includes(comunaTxt.toLowerCase());
  return [esCorreccionCliente() ? 'Le corrijo la entrega ✅' : 'Le confirmo la entrega ✅', '',
    `🚽 ${n} baño${n === 1 ? '' : 's'} químico${n === 1 ? '' : 's'}${itemExtra !== '' ? ` + ${itemExtra}` : ''}`,
    ...(duracionTxt !== '' ? [`⏱ Por ${duracionTxt}`] : []),
    `📅 ${fechaLegible(fecha)}${horaTxt}`,
    `📍 ${direccion}${conComuna ? `, ${comunaTxt}` : ''}`, '',
    'Cualquier cambio o duda me avisa por acá. ¡Gracias! 🙌'].join('\n');
})();

try {
  // si este chat YA tiene una entrega en el sistema, se CORRIGE esa (no se crea otra)
  const entregaPrevia = enlaceDe(jid);
  const esCorreccion = entregaPrevia !== null || texto(args._yaSalio) === 'si';
  if (entregaPrevia !== null) d.entrega_id = entregaPrevia;

  const prep = await prepararEntrega(d, jid, nombre, texto(args.telefono_cliente), { dry });
  const avisoOverride = texto(args.mensaje_repartidor);
  const aviso = avisoOverride !== '' ? avisoOverride
    : (esCorreccion ? mensajeDeCambio() : prep.resumen);

  if (dry) {
    console.log('— ASÍ SALDRÍA EL AVISO AL REPARTIDOR (prueba en seco, nada subió) —');
    console.log(aviso);
    if (confirmacionCliente !== '' && jid !== '') {
      console.log('\n— Y ESTA CONFIRMACIÓN LE LLEGARÍA AL CLIENTE —');
      console.log(confirmacionCliente);
    }
    // el bloque parseable para el MODAL DE PREVIEW de la pizarra (28-ago): los dos
    // textos por separado, editables antes de mandar
    console.log('\n===PREVIEW-JSON===');
    console.log(JSON.stringify({ repartidor: aviso, cliente: confirmacionCliente }));
    console.log('===FIN-PREVIEW===');
    console.log(`\n✓ Prueba en seco lista — repartidor: ${prep.repTel || 'SIN CONFIGURAR'} · tarjeta armada, Supabase intacto`);
    process.exit(0);
  }

  if (!prep.repTel) {
    console.error('no hay número de repartidor configurado (REPARTIDOR_NUMERO del bot)');
    process.exit(1);
  }
  const convRepartidor = `wa-baileys:${prep.repTel.replace(/\D/g, '')}@s.whatsapp.net`;
  await enviarPorDixdybot(convRepartidor, aviso);
  // la confirmación al cliente sale por el mismo canal; si falla, el aviso al
  // repartidor YA salió — se dice claro en vez de fingir que falló todo
  let confirmacionOk = false;
  let confirmacionError = '';
  if (confirmacionCliente !== '' && convId !== '') {
    try {
      await enviarPorDixdybot(convId, confirmacionCliente);
      confirmacionOk = true;
    } catch (e) {
      // a STDOUT y no a stderr (28-ago, caso de los 7 baños de Peñalolén): el ⚠️ iba a
      // stderr, la traza 🔧 del panel solo guarda stdout, y el dueño nunca supo que la
      // confirmación no salió — el cliente quedó sin su resumen hasta que él preguntó.
      confirmacionError = e.message;
    }
  }
  // el enlace jid → entrega queda sellado: el próximo despacho de este chat CORRIGE esta
  // tarjeta en vez de crear otra (es el mapa que usaba el sistema de siempre)
  guardarEnlace(jid, prep.entrega?.id || d.entrega_id || null);
  // el rastro ANTI-DUPLICADOS del sistema de siempre (yaDespachado lo consulta)
  logEnvio({ jid: jid || 'panel-dixdybot', tipo: 'entrega',
    detalle: { repartidor: prep.repTel, subida: prep.subida, resumen: aviso,
      manual: true, origen: 'dixdybot-panel', actualizacion: esCorreccion,
      confirmacion_cliente: confirmacionOk } });
  // TODO en la ÚLTIMA línea: la traza 🔧 del panel muestra solo la línea final del
  // stdout, así que el estado de la confirmación viaja ahí mismo — visible siempre.
  const notaConfirmacion = confirmacionOk
    ? ' · ✓ confirmación al cliente enviada'
    : (confirmacionCliente !== '' && convId !== ''
      ? ` · ⚠️ la confirmación al cliente NO salió (${confirmacionError}) — mándasela tú desde el chat`
      : (confirmacionCliente === '' ? ' · (sin confirmación al cliente: se pidió no mandarla)' : ''));
  console.log(`✓ Entrega en el panel del repartidor y aviso enviado a +${prep.repTel} por el canal dixdybot${notaConfirmacion}`);
} catch (e) {
  console.error(`no se pudo preparar la entrega: ${e.message}`);
  process.exit(1);
}
