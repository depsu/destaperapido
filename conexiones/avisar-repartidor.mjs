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
const dry = texto(args.dry).toLowerCase() === 'si';
const telefonoCliente = texto(args.telefono_cliente);
if (nombre === '' || direccion === '' || fecha === '' || telefonoCliente === '') {
  console.error('faltan datos: nombre, teléfono del cliente, fecha de entrega y la '
    + 'dirección (exacta o link de Maps/Waze/WhatsApp) son obligatorios');
  process.exit(1);
}

// el chat de origen (si el despacho nace de un chat del panel): su jid enlaza la entrega
const convId = texto(args._convId);
const jid = convId.startsWith('wa-baileys:') ? convId.slice('wa-baileys:'.length) : '';

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
const d = {
  direccion,
  fecha_entrega: fecha,
  hora: texto(args.hora) || undefined,
  comuna: texto(args.comuna) || undefined,
  cantidad_banos: Math.max(1, Math.round(Number(args.cantidad) || 1)),
  duracion: texto(args.duracion) || undefined,
  telefono_contacto: telefonoCliente || undefined,
  maps_url: texto(args.maps_url) || undefined,
  aseo: texto(args.aseo) || undefined,
  ...(precioNeto > 0 ? { precio_clp: precioNeto } : {}),
  ...(flete > 0 ? { flete_clp: flete } : {}),
  requiere_factura: conFactura,
};

// La CONFIRMACIÓN AL CLIENTE (12-ago, pedido del dueño: el flujo viejo también se la
// mandaba). Editable vía `mensaje_cliente`; 'no' = no mandarle nada; vacío = la de
// siempre, calcada del panel del CRM viejo (mensajeClienteDefault).
const n = Math.max(1, Math.round(Number(args.cantidad) || 1));
const confirmacionCliente = (() => {
  const pedido = texto(args.mensaje_cliente);
  if (pedido.toLowerCase() === 'no') return '';
  if (pedido !== '') return pedido;
  return ['Le confirmo la entrega ✅', '',
    `🚽 ${n} baño${n === 1 ? '' : 's'} químico${n === 1 ? '' : 's'}`,
    `📅 ${fecha}${texto(args.hora) !== '' ? ` a las ${texto(args.hora)}` : ''}`,
    `📍 ${direccion}${texto(args.comuna) !== '' ? `, ${texto(args.comuna)}` : ''}`, '',
    'Cualquier cambio o duda me avisa por acá. ¡Gracias! 🙌'].join('\n');
})();

try {
  const prep = await prepararEntrega(d, jid, nombre, texto(args.telefono_cliente), { dry });
  const aviso = texto(args.mensaje) || prep.resumen;

  if (dry) {
    console.log('— ASÍ SALDRÍA EL AVISO AL REPARTIDOR (prueba en seco, nada subió) —');
    console.log(aviso);
    if (confirmacionCliente !== '' && jid !== '') {
      console.log('\n— Y ESTA CONFIRMACIÓN LE LLEGARÍA AL CLIENTE —');
      console.log(confirmacionCliente);
    }
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
  if (confirmacionCliente !== '' && convId !== '') {
    try {
      await enviarPorDixdybot(convId, confirmacionCliente);
      confirmacionOk = true;
    } catch (e) {
      console.error(`⚠️ el aviso al repartidor salió, pero la confirmación al cliente no: ${e.message}`);
    }
  }
  // el rastro ANTI-DUPLICADOS del sistema de siempre (yaDespachado lo consulta)
  logEnvio({ jid: jid || 'panel-dixdybot', tipo: 'entrega',
    detalle: { repartidor: prep.repTel, subida: prep.subida, resumen: aviso,
      manual: true, origen: 'dixdybot-panel',
      confirmacion_cliente: confirmacionOk } });
  console.log(`✓ Entrega en el panel del repartidor y aviso enviado a +${prep.repTel} por el canal dixdybot`
    + (confirmacionOk ? '\n✓ Y la confirmación al cliente salió también ✅' : ''));
} catch (e) {
  console.error(`no se pudo preparar la entrega: ${e.message}`);
  process.exit(1);
}
