// avisar-repartidor.mjs — CONECTOR FABRICADO de destaperapido (H3, Ruta A del cutover).
// El DESPACHO de una entrega, calcado del flujo del CRM viejo pero disparado desde el
// panel dixdybot: reusa `prepararEntrega` del sistema de siempre (arma la entrega,
// renderiza la tarjeta en python y la sube a Supabase vía bridge/entrega_bridge.py) y
// manda el aviso por el CANAL DEL DIXDYBOT (API del panel) — desde el cutover del
// 13-ago el número vive ahí; el outbox del bot viejo ya no tiene quién lo drene.
// El rastro sigue quedando en envios.jsonl (yaDespachado lo consulta).
//
// Uso: node avisar-repartidor.mjs '{"nombre":"...","direccion":"...","fecha":"...",...}'
//   args: nombre* · direccion* · fecha* (de entrega; entiende español) ·
//         hora (franja o hora confirmada, TAL CUAL la dijo el cliente: «entre 10 y 12»,
//         «viernes en la tarde», «10:00») · hora_tope (límite: «09:30» → «antes de las
//         09:30»; franja, tope y hora confirmada son TRES cosas distintas y viajan
//         separadas) ·
//         acceso (referencia o link del portón) · recibe + telefono_recibe (quién
//         recepciona en terreno) · paga + telefono_paga (quién paga, si es otra
//         persona) · forma_pago («efectivo contra entrega», «transferencia») ·
//         retiro_acordado (fecha o franja de retiro YA acordada; sin esto el retiro
//         se avisa como pendiente de coordinar, nunca inferido) ·
//         comuna · cantidad (default 1) · duracion (texto: «mensual», «2 semanas») ·
//         telefono_cliente · maps_url · aseo (frecuencia acordada; en plazos de
//         hasta 7 días el aseo periódico no se promete: ver «EL ASEO SEGÚN EL PLAZO») ·
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

async function enviarPorDixdybot(convId, textoMensaje, citaDe) {
  const res = await fetch(`${PANEL_URL}/api/chats/${encodeURIComponent(convId)}/enviar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ texto: textoMensaje,
      ...(citaDe === undefined ? {} : { citaDe }) }),
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

/* RESPONDER CITANDO EL AVISO ORIGINAL (2-sep, pedido de Alejandro: «auto responder a
   nuestros mensajes, así él tiene el contexto entero»): un ajuste sobre una entrega sale
   como RESPUESTA de WhatsApp al aviso 🚚/🔄 de ESA entrega — el repartidor toca la cajita
   y ve de cuál se habla. Se busca en el hilo el último mensaje nuestro que nombre al
   cliente o la cola del id. La cita es un extra: si algo falla, el aviso sale igual. */
async function idAvisoOriginal(convIdRep, pistas) {
  try {
    const res = await fetch(`${PANEL_URL}/api/chats/${encodeURIComponent(convIdRep)}`);
    if (!res.ok) return undefined;
    const { mensajes } = await res.json();
    if (!Array.isArray(mensajes)) return undefined;
    const limpias = pistas.map((p) => String(p || '').trim().toLowerCase()).filter((p) => p.length >= 4);
    if (limpias.length === 0) return undefined;
    for (let i = mensajes.length - 1; i >= 0; i--) {
      const m = mensajes[i];
      if (m.de !== 'tu' || m.id === undefined || m.id === null) continue;
      const t = String(m.texto || '').toLowerCase();
      if (!/entrega|🚚|🔄/.test(t)) continue;
      if (limpias.some((p) => t.includes(p))) return Number(m.id);
    }
  } catch { /* sin cita no se cae nada */ }
  return undefined;
}

/* EL LINK CORTO CON ANCLA (2-sep): destaperapido.cl/entregas redirige a la página del
   repartidor, y #<cola del id> hace que SU tarjeta se centre y pulse unos segundos. */
const linkEntrega = (entregaId) => {
  const cola = String(entregaId || '').replace(/[^0-9a-z]/gi, '').slice(-4);
  return cola === '' ? 'destaperapido.cl/entregas' : `destaperapido.cl/entregas#${cola}`;
};

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
  // El AÑO solo cuando no es el actual (9-sep): «jueves 11 de septiembre» para una
  // entrega de noviembre del año que viene no identifica nada.
  const anio = d.getFullYear() === new Date().getFullYear() ? '' : ` de ${d.getFullYear()}`;
  return `${DIAS_ES[d.getDay()]} ${d.getDate()} de ${MESES_ES[d.getMonth()]}${anio}`;
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

/* SOLTAR EL ENLACE AL CANCELAR (9-sep, A21/T19): `enlaces.json` conservaba el link
   aunque la entrega se hubiera cancelado y la tarjeta ya no existiera. Consecuencia: el
   cliente que volvía a arrendar recibía «Le corrijo la entrega» de un pedido muerto, y
   el re-despacho escribía encima de una tarjeta borrada en vez de crear la nueva. */
function borrarEnlace(jidCliente) {
  if (!jidCliente) return;
  try {
    const e = leerEnlaces();
    if (!e.links || e.links[jidCliente] === undefined) return;
    delete e.links[jidCliente];
    writeFileSync(ENLACES_FILE, JSON.stringify(e, null, 2));
  } catch (err) {
    console.error(`⚠️ no pude soltar el enlace de la entrega cancelada: ${err.message}`);
  }
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
/* RESPUESTA CITADA → NOTA EN LA TARJETA (2-sep, pedido de Alejandro: «responder al
   mensaje del repartidor y dejarlo como nota en el sistema… que seleccione el mensaje
   donde sale la ficha»). El gancho `al_citar` del panel nos llama con `cita_texto` (el
   aviso 🚚/🔄 citado) y `nota_cambio` (lo que el dueño escribió). El WhatsApp YA salió
   como respuesta citada — acá solo queda escribir la nota en la tarjeta del sistema.
   La entrega se ubica por la cola del link «entregas#xxxx» del aviso citado; los avisos
   viejos sin link caen al nombre del cliente. */
const citaTexto = texto(args.cita_texto);
if (citaTexto !== '' && notaCambio !== '' && !esCancelacion) {
  const { execFileSync } = await import('node:child_process');
  // tres pistas, en orden: el link «entregas#xxxx» (avisos nuevos) · el teléfono del
  // cliente en la ficha (el id de la entrega termina en su cola) · el nombre del cliente
  const mTel = /Tel[eé]fono cliente:\s*\+?([\d\s]{8,15})/i.exec(citaTexto);
  const colaTel = mTel ? mTel[1].replace(/\D/g, '').slice(-4) : '';
  const cola = (/entregas#([a-z0-9]{4})/i.exec(citaTexto) || [])[1] || colaTel;
  // el separador de la cabecera pasó de «—» a «·» (9-sep): los avisos viejos del hilo
  // siguen trayendo la raya, así que el buscador entiende los dos
  const mNombre = /(?:ENTREGA|CAMBIO en la entrega)\s*[—·]\s*([^\n(]+)/i.exec(citaTexto);
  const nombreCita = mNombre ? mNombre[1].trim() : '';
  if (cola === '' && nombreCita === '') {
    console.log('El mensaje citado no trae ni el link de la tarjeta ni el nombre del '
      + 'cliente: la nota salió por WhatsApp pero no supe a qué tarjeta anotarla.');
    process.exit(0);
  }
  try {
    const salida = execFileSync('python3', ['-c', [
      'import sys, json, urllib.request, urllib.parse',
      'from datetime import datetime',
      `sys.path.insert(0, '/Users/alejandroriveracarrasco/SaSS/destaperapido/cotizaciones-destape-rapido/resumen-repartidor/scripts')`,
      'import sync_entregas_supabase as sync',
      'import generar_listado as gl',
      `cola = ${JSON.stringify(cola)}`,
      `nombre = ${JSON.stringify(nombreCita)}`,
      `nota = ${JSON.stringify(notaCambio)}`,
      'q = f"id=like.*{cola}" if cola else f"id=like.*{urllib.parse.quote(nombre.lower().replace(chr(32), chr(45)))}*"',
      'url = f"{gl.SUPABASE_URL}/rest/v1/entrega?{q}&eliminado=eq.false&select=id,informado_at,data&order=informado_at.desc&limit=1"',
      'req = urllib.request.Request(url, headers={"apikey": gl.SUPABASE_ANON_KEY, "authorization": "Bearer " + gl.SUPABASE_ANON_KEY})',
      'filas = json.load(urllib.request.urlopen(req, timeout=20))',
      'if not filas:',
      '    print("SIN-TARJETA"); raise SystemExit',
      'e = filas[0]["data"]',
      'sello = datetime.now().strftime("%d-%b %H:%M")',
      'previa = str(e.get("notas") or "").strip()',
      'e["notas"] = (previa + " · " if previa else "") + f"📝 {nota} ({sello})"',
      'sync.upsert([sync.fila_de(e, filas[0]["informado_at"])])',
      'print("ANOTADA:" + filas[0]["id"])',
    ].join('\n')], { encoding: 'utf8', timeout: 30_000 }).trim();
    if (salida.includes('SIN-TARJETA')) {
      console.log('No encontré la tarjeta de esa entrega en el sistema — la nota salió '
        + 'por WhatsApp igual, pero anótala a mano si debe quedar en la página.');
    } else {
      const idAnotada = (salida.split('ANOTADA:')[1] || '').trim();
      console.log(`✓ Nota escrita en la tarjeta del sistema (${idAnotada}) — el repartidor `
        + `la ve en destaperapido.cl/entregas#${idAnotada.replace(/[^0-9a-z]/gi, '').slice(-4)}`);
    }
  } catch (e) {
    console.log(`⚠️ La nota salió por WhatsApp, pero no pude escribirla en la tarjeta: `
      + String(e.message || e).slice(0, 180));
  }
  process.exit(0);
}
if (notaCambio !== '' && !esCancelacion) {
  const entregaId = enlaceDe(jid);
  const quien = texto(args.nombre);
  const donde = [texto(args.direccion), texto(args.comuna)].filter(Boolean).join(', ');
  const cabeza = entregaId !== null
    ? `🔄 CAMBIO en una entrega ya agendada${quien ? ` (${quien}` + (donde ? ` · ${donde}` : '') + ')' : ''}:`
    : `📣 Aviso${quien ? ` sobre ${quien}` + (donde ? ` (${donde})` : '') : ''}:`;
  /* DÓNDE QUEDÓ LA CORRECCIÓN (9-sep, B9/T22): esta rama manda el WhatsApp y NO toca la
     tarjeta del sistema. Antes el texto terminaba con «📋 Su tarjeta: …», que se lee como
     «ahí está el cambio»: el repartidor abría la tarjeta y veía el dato viejo. Y si el
     chat no tiene entrega enlazada, se dice: es un aviso suelto, no hay nada que buscar. */
  const pieNota = entregaId !== null
    ? `\n\nEsta nota NO cambia la tarjeta: para esta entrega manda lo que dice acá.`
      + `\n📋 Su tarjeta (con los datos anteriores): ${linkEntrega(entregaId)}`
    : '\n\nEste cliente todavía no tiene tarjeta en tu lista: es un aviso suelto, '
      + 'no hay entrega que buscar.';
  const avisoNota = `${cabeza}
${notaCambio}` + pieNota;
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
  const convRepNota = `wa-baileys:${repTelNota}@s.whatsapp.net`;
  const citaNota = await idAvisoOriginal(convRepNota,
    [quien, String(entregaId || '').slice(-4)]);
  await enviarPorDixdybot(convRepNota, avisoNota, citaNota);
  logEnvio({ jid: jid || 'panel-dixdybot', tipo: 'entrega',
    detalle: { repartidor: repTelNota, nota_cambio: notaCambio,
      entrega_id: entregaId || null, cita: citaNota ?? null, origen: 'dixdybot-nota' } });
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
  /* IDENTIFICAR CUÁL Y QUÉ HACER (9-sep, B10/T20): «🚫 CANCELADA — Benja» sin fecha ni
     dirección no le dice al repartidor cuál de sus tarjetas se cayó, y «no hay que ir» no
     cubre las otras dos etapas posibles (el camión ya salió, o el baño ya está puesto). */
  const partes = [`🚫 CANCELADA · ${nombre || 'una entrega'}${texto(args.comuna) ? ` (${texto(args.comuna)})` : ''}`];
  partes.push(fecha !== '' ? `📅 Era para: ${fechaLegible(fecha)}`
    : '📅 Era para: fecha no registrada en el aviso');
  if (direccion !== '') partes.push(`📍 ${direccion}`);
  if (entregaId) partes.push(`📋 Tarjeta: ${linkEntrega(entregaId)}`);
  if (cita !== '') partes.push(`💬 El cliente: «${cita}»`);
  partes.push('');
  partes.push(tarjetaFuera
    ? 'La tarjeta ya salió de tu lista. No despachar.'
    : (dry && entregaId ? 'La tarjeta se retiraría del sistema (prueba en seco). No despachar.'
      : (entregaId
        ? 'OJO: no pude retirar la tarjeta del sistema, bórrala tú de la lista. No despachar.'
        : 'No encontré tarjeta enlazada de este chat: si la ves en tu lista, bórrala. No despachar.')));
  partes.push('Si el equipo ya salió, avísame antes de llegar. Si ya está instalado, '
    + 'el retiro se coordina aparte.');
  const avisoCancel = partes.join('\n');
  if (dry) {
    console.log('— ASÍ SALDRÍA EL 🚫 AL REPARTIDOR (prueba en seco, nada salió) —');
    console.log(avisoCancel);
    console.log(`\n✓ Prueba en seco · entrega enlazada: ${entregaId || 'ninguna'} · repartidor: ${repTel || 'SIN CONFIGURAR'}`);
    process.exit(0);
  }
  if (repTel === '') { console.error('no hay número de repartidor configurado'); process.exit(1); }
  await enviarPorDixdybot(`wa-baileys:${repTel}@s.whatsapp.net`, avisoCancel);
  // el chat deja de tener entrega vigente: si este cliente vuelve a arrendar, es un
  // arriendo NUEVO y no «una corrección» de lo que se canceló (A21)
  borrarEnlace(jid);
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

/* ── LAS MARCAS DE LA FICHA (9-sep, B2/B3/B4/B6/A18) ──────────────────────────────
   El objeto `entrega` del sistema de siempre no tiene campo propio para «quién recibe
   en terreno», «quién paga», «cómo se entra», «forma de pago» ni «retiro acordado»: los
   trae el conector y hasta hoy se perdían (o el equipamiento caía al final, dentro de
   «📝 Notas», que es el peor lugar para el dato que decide qué unidad sube al camión).
   Viajan como marcas «CLAVE: valor» dentro de `tipo_uso` → `notas`, y el resumen del
   repartidor (`resumen_repartidor.separar_notas`) las saca de ahí y las pinta en su
   lugar. Cero cambios al sistema viejo, y la tarjeta web las conserva en sus notas. */
const telLegible = (v) => {
  const d = texto(v).replace(/\D/g, '');
  if (d === '') return '';
  return `+${d.length === 9 && d.startsWith('9') ? `56${d}` : d}`;
};
// un « · » dentro de un valor partiría la marca en dos: se neutraliza al armarla
const marca = (clave, valor) => {
  const v = texto(valor).replace(/·/g, '-').replace(/\s+/g, ' ').trim();
  return v === '' ? '' : `${clave}: ${v}`;
};
const quienRecibe = [texto(args.recibe), telLegible(args.telefono_recibe)]
  .filter((t) => t !== '').join(' ');
const quienPaga = [texto(args.paga), telLegible(args.telefono_paga)]
  .filter((t) => t !== '').join(' ');
const marcasFicha = [
  marca('EQUIPO', equipamiento.toUpperCase()),
  marca('ACCESO', args.acceso ?? args.referencia),
  marca('RECIBE', quienRecibe),
  marca('PAGA', quienPaga),
  marca('PAGO', args.forma_pago),
  marca('RETIRO', args.retiro_acordado),
].filter((t) => t !== '').join(' · ');

/* ── FRANJA, HORA TOPE Y HORA CONFIRMADA SON TRES COSAS (9-sep, A17) ──────────────
   «entre 10 y 12» no es una cita a las 10, y «antes de las 9:30» no es «a las 9:30».
   El conector NO convierte nada: pasa el texto tal cual lo dijo el cliente, y el tope
   viaja como su propia parte de la línea. `resumen_repartidor.lineas_horario` los
   separa en «⏰ INSTALAR antes de…», «🕐 Franja solicitada…» y «🕐 Hora confirmada…». */
const horaTope = texto(args.hora_tope);
const horaFicha = [
  texto(args.hora),
  horaTope === '' ? ''
    : (/antes de|m[aá]s tardar/i.test(horaTope) ? horaTope : `antes de las ${horaTope}`),
].filter((t) => t !== '').join(' · ');

/* ── EL ASEO SEGÚN EL PLAZO (9-sep, Alejandro: «si el mensaje es diario, al repartidor a
   veces dice limpieza incluida de 7 a 10 días, lo cual no tiene lógica») ───────────────
   El resumen del repartidor pinta «🧽 Aseo:» con lo que venga y, si viene vacío, cae al
   estándar «Aseo semanal (cada 7 a 10 días)» (resumen_repartidor.py). Un ciclo semanal
   en una entrega de uno o tres días es una promesa que nadie va a cumplir: el baño ya se
   retiró. Con un plazo CORTO (hasta 7 días) el aseo periódico NO corre — se dice lo que
   de verdad incluye el servicio — y una frecuencia solo se nombra si la ficha trae una
   ACORDADA de verdad (una limpieza pactada, un extra de evento). Con mensual, todo sigue
   igual que siempre. */

/** Cuántos días dura el arriendo, leído como lo escribe una persona. 0 = no se pudo
 *  saber (ahí manda el estándar de siempre, que es el mensual). */
function diasDePlazo(txt) {
  const t = String(txt || '').toLowerCase().trim();
  if (t === '') return 0;
  // «mensual», «1 mes», «3 meses», «indefinido»: largo, sin más análisis
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
  const rango = /(?<![:.\d])(\d{1,2})(?![:.\d])(?:\s*de\s+[a-zá-ú]+)?(?:\s+\d{1,2}[:.]\d{2}(?:\s*(?:am|pm|hrs?|horas?))?)?\s*(?:al|a|-|hasta(?:\s+el)?)\s*(?:el\s+)?(?<![:.\d])(\d{1,2})(?![:.\d])\s*de\s+[a-zá-ú]+/.exec(t);
  if (rango !== null) {
    const dias = Number(rango[2]) - Number(rango[1]) + 1;
    if (dias > 0 && dias <= 31) return dias;
  }
  if (/un[ao]?\s*(?:d[ií]a|noche)|evento|fiesta|matrimonio|cumplea|bautizo/.test(t)) return 1;
  if (/semana/.test(t)) return 7;
  return 0;
}

// «semanal», «cada 7 días», «cada 7 a 10 días»: una cadencia, no un acuerdo puntual
const aseoEsPeriodico = (t) => /semanal|cada\s*\d+\s*(?:a\s*\d+\s*)?d[ií]as?|cada\s*semana|7\s*a\s*10/i.test(t);

const diasPlazo = diasDePlazo(texto(args.duracion));
const plazoCorto = diasPlazo > 0 && diasPlazo <= 7;
const aseoFicha = texto(args.aseo);
// en plazo corto solo sobrevive un aseo ACORDADO: ni la cadencia estándar ni un «no»
const aseoAcordado = plazoCorto
  && (aseoFicha === '' || aseoEsPeriodico(aseoFicha) || /^\s*(?:no|sin)\b/i.test(aseoFicha))
  ? '' : aseoFicha;
// con flete cobrado el traslado NO va «incluido»: se dice que se cobra aparte (ya viaja
// desglosado en el 💵 COBRAR, así el repartidor no promete gratis lo que va en la boleta)
const aseoLinea = !plazoCorto ? aseoAcordado
  : (aseoAcordado !== '' ? aseoAcordado
    : `Sin aseo programado (${diasPlazo} día${diasPlazo === 1 ? '' : 's'}): incluye `
      + (flete > 0 ? 'instalación y retiro, el traslado se cobra aparte'
        : 'traslado, instalación y retiro'));

const d = {
  direccion,
  fecha_entrega: fecha,
  hora: horaFicha || undefined,
  comuna: texto(args.comuna) || undefined,
  cantidad_banos: Math.max(1, Math.round(Number(args.cantidad) || 1)),
  duracion: texto(args.duracion) || undefined,
  telefono_contacto: telefonoCliente || undefined,
  // quién recibe en terreno (1-sep, colegio de Colina: el director recepcionaba y el
  // aviso al repartidor no lo llevaba) — construirEntrega ya sabe pintarlos
  contacto_respaldo: texto(args.contacto_respaldo) || undefined,
  telefono_respaldo: texto(args.telefono_respaldo) || undefined,
  maps_url: texto(args.maps_url) || undefined,
  aseo: aseoLinea || undefined,
  ...(marcasFicha !== '' ? { tipo_uso: marcasFicha } : {}),
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
      nota: 'ya se cobró junto con la entrega, no cobrar aparte' }] } : {}),
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

/** Plata como se lee: 154700 → «$154.700». */
const clpTxt = (v) => '$' + String(Math.round(Number(v) || 0))
  .replace(/\B(?=(\d{3})+(?!\d))/g, '.');

/* LA VERSIÓN ANTERIOR DE LA TARJETA (9-sep, B8/T21): para decir QUÉ cambió hay que
   tener con qué comparar. Se lee la fila de Supabase que el re-despacho está por pisar.
   Es best-effort: si Supabase no contesta, el aviso sale igual, diciendo que no se pudo
   comparar (mentir sobre el cambio es peor que reconocer el hueco). */
async function datosEntregaPrevia(entregaId) {
  if (!entregaId) return null;
  try {
    const { execFileSync } = await import('node:child_process');
    const salida = execFileSync('python3', ['-c', [
      'import sys, json, urllib.request',
      `sys.path.insert(0, '/Users/alejandroriveracarrasco/SaSS/destaperapido/cotizaciones-destape-rapido/resumen-repartidor/scripts')`,
      'import generar_listado as gl',
      `eid = ${JSON.stringify(entregaId)}`,
      'h = {"apikey": gl.SUPABASE_ANON_KEY, "authorization": "Bearer " + gl.SUPABASE_ANON_KEY}',
      'req = urllib.request.Request(f"{gl.SUPABASE_URL}/rest/v1/entrega?id=eq.{eid}&select=data", headers=h)',
      'filas = json.load(urllib.request.urlopen(req, timeout=15))',
      'print(json.dumps(filas[0]["data"] if filas else None, ensure_ascii=False))',
    ].join('\n')], { encoding: 'utf8', timeout: 25_000 }).trim();
    const previa = JSON.parse(salida);
    return previa && typeof previa === 'object' ? previa : null;
  } catch { return null; }
}

/** El aviso de CAMBIO: corto y solo con lo que importa. El repartidor ya tiene la tarjeta;
 *  lo que necesita saber es QUÉ cambió, no releer todo.
 *
 *  Hasta el 9-sep repetía fecha, cantidad y dirección sin marcar ninguna diferencia, se
 *  saltaba el precio y el aseo, y cerraba afirmando que la tarjeta «ya quedó actualizada»
 *  aunque la subida hubiera fallado. Ahora compara contra la versión anterior y dice la
 *  verdad sobre dónde quedó el cambio. */
function mensajeDeCambio(nueva, previa, subida) {
  const partes = [`🔄 CAMBIO en la entrega · ${nombre}`
    + (texto(args.comuna) !== '' ? ` (${texto(args.comuna)})` : '')];
  const pagoNuevo = (nueva || {}).pago || {};
  const pagoPrevio = (previa || {}).pago || {};
  const dirNueva = [direccion, texto(args.comuna)].filter((t) => t !== ''
    && !direccion.toLowerCase().includes(texto(args.comuna).toLowerCase())).join(', ');
  const cantidadNueva = Math.max(1, Math.round(Number(args.cantidad) || 1));
  const campos = [
    ['Fecha', previa ? fechaLegible(previa.fecha || '') : '', fechaLegible(fecha)],
    ['Horario', previa ? String(previa.hora || '') : '', horaFicha],
    ['Cantidad', previa ? String((previa.cantidad || '')) : '', String(cantidadNueva)],
    ['Dirección', previa ? String(previa.direccion || '') : '', dirNueva || direccion],
    ['Qué se carga', previa ? String(previa.servicio || '') : '', String((nueva || {}).servicio || '')],
    ['Aseo', previa ? String(previa.aseo || '') : '', String((nueva || {}).aseo || '')],
    ['A cobrar', pagoPrevio.monto == null ? '' : clpTxt(pagoPrevio.monto),
      pagoNuevo.monto == null ? '' : clpTxt(pagoNuevo.monto)],
  ];
  const cambios = campos
    .filter(([, antes, ahora]) => ahora !== '' && antes !== ahora)
    .map(([etq, antes, ahora]) => `· ${etq}: ${antes === '' ? 'sin dato' : antes} → ${ahora}`);
  partes.push('');
  if (previa === null) {
    partes.push('No pude leer la versión anterior de la tarjeta, así que no puedo marcar '
      + 'qué cambió. Vale ESTA versión:');
    partes.push(`· Fecha: ${fechaLegible(fecha)}`);
    if (horaFicha !== '') partes.push(`· Horario: ${horaFicha}`);
    partes.push(`· Qué se carga: ${(nueva || {}).servicio || `${cantidadNueva} baño(s)`}`);
    partes.push(`· Dirección: ${dirNueva || direccion}`);
    if (pagoNuevo.monto != null) partes.push(`· A cobrar: ${clpTxt(pagoNuevo.monto)}`);
  } else if (cambios.length === 0) {
    partes.push('Se re-despachó la misma entrega: no cambió ningún dato de la tarjeta.');
  } else {
    partes.push('Cambió esto:');
    partes.push(...cambios);
    partes.push('');
    partes.push('El resto sigue igual que en la tarjeta.');
  }
  const maps = texto(args.maps_url);
  if (maps !== '') partes.push(`🗺️ ${maps}`);
  partes.push('');
  // A20: el puente puede devolver ok con `subida:false` y la tarjeta quedar en lo viejo.
  partes.push(dry ? 'Prueba en seco: la tarjeta del sistema no se tocó.'
    : (subida === true ? 'Tarjeta del sistema actualizada con este cambio.'
      : 'OJO: la tarjeta del sistema NO se pudo actualizar y sigue mostrando lo anterior. '
        + 'Para esta entrega manda lo que dice este mensaje.'));
  return partes.join('\n');
}

// La CONFIRMACIÓN AL CLIENTE (12-ago, pedido del dueño: el flujo viejo también se la
// mandaba). Editable vía `mensaje_cliente`; 'no' = no mandarle nada; vacío = la de
// siempre, calcada del panel del CRM viejo (mensajeClienteDefault).
//
// REESCRITA EL 9-SEP (T18-T22). Lo que tenía mal:
//   · «⏱ Por mensual» y «⏱ Por hasta fin de mes» no son español;
//   · emojis y «¡Gracias! 🙌», los dos prohibidos por las reglas de estilo del negocio;
//   · decía «baño químico» aunque fuera una ducha, y NUNCA el equipamiento acordado
//     (con o sin lavamanos), que es justo lo que se reclama en la puerta;
//   · no decía el monto ni la forma de pago, mientras el repartidor sí llegaba con un
//     «COBRAR» con IVA: los dos lados del mismo trato leían cosas distintas.
// El monto sale del MISMO objeto que se le manda al repartidor, no de una cuenta paralela.
const n = Math.max(1, Math.round(Number(args.cantidad) || 1));
/* «Le confirmo» y «le actualizo» no dicen lo mismo, y el cliente que ya recibió una
   confirmación se merece saber que esta la reemplaza. Ojo (A21): una entrega CANCELADA
   suelta su enlace (ver borrarEnlace), así que un cliente antiguo que vuelve a arrendar
   recibe una confirmación NUEVA y no la «actualización» de un pedido muerto. */
const esCorreccionCliente = () => enlaceDe(jid) !== null || texto(args._yaSalio) === 'si';

/** «mensual» → «Arriendo mensual»; «3 días» → «Por 3 días»; el resto, «Plazo: …». */
function fraseDuracion(bruto) {
  let t = texto(bruto);
  if (t === '') return '';
  // el detalle largo entre paréntesis o tras dos puntos ya viaja en la línea de la fecha
  const corte = t.search(/[:(]/);
  if (corte > 0) t = t.slice(0, corte).trim();
  if (t === '') return '';
  if (/^(arriendo\s+)?mensual|^mes a mes$/i.test(t)) return 'Arriendo mensual';
  if (/^(\d|una?\b|dos\b|tres\b|cuatro\b|cinco\b|seis\b|siete\b)/i.test(t)) {
    return `Por ${t.charAt(0).toLowerCase()}${t.slice(1)}`;
  }
  return `Plazo: ${t.charAt(0).toUpperCase()}${t.slice(1)}`;
}

/** El horario en palabras del cliente: franja, tope y hora confirmada, cada uno como es. */
function fraseHorario() {
  const partesHora = horaFicha.split('·').map((h) => h.trim()).filter((h) => h !== '');
  const frases = partesHora.map((h) => {
    if (/antes de|m[aá]s tardar/i.test(h)) return `instalado ${h}`;
    if (/^\d{1,2}:\d{2}$/.test(h)) return `a las ${h}`;
    return h;
  });
  const hayExacta = partesHora.some((h) => /^\d{1,2}:\d{2}$/.test(h));
  return { sufijo: frases.length === 0 ? '' : `, ${frases.join(', ')}`, hayExacta };
}

function armarConfirmacionCliente(entregaNueva) {
  const pedido = texto(args.mensaje_cliente);
  if (pedido.toLowerCase() === 'no') return '';
  if (pedido !== '') return pedido;
  // la comuna solo si la dirección no la trae ya (salía «Providencia, Providencia»)
  const comunaTxt = texto(args.comuna);
  const conComuna = comunaTxt !== ''
    && !direccion.toLowerCase().includes(comunaTxt.toLowerCase());
  // QUÉ RECIBE: cantidad, equipamiento acordado y el ítem extra, con su nombre real
  let queRecibe = `${n} baño${n === 1 ? '' : 's'} químico${n === 1 ? '' : 's'}`;
  if (equipamiento !== '') queRecibe += ` ${equipamiento.toLowerCase()}`;
  if (itemExtra !== '') queRecibe += `, más ${itemExtra.toLowerCase()}`;
  const { sufijo, hayExacta } = fraseHorario();
  const plazo = fraseDuracion(args.duracion);
  const monto = (entregaNueva || {}).pago ? (entregaNueva.pago.monto ?? null) : null;
  const formaPago = texto(args.forma_pago);
  return [
    esCorreccionCliente() ? 'Le actualizo la entrega.' : 'Le confirmo la entrega.', '',
    `Servicio: ${queRecibe}`,
    ...(plazo !== '' ? [plazo] : []),
    `Entrega: ${fechaLegible(fecha)}${sufijo}`,
    ...(hayExacta ? [] : ['Hora exacta: pendiente de confirmar']),
    `Dirección: ${direccion}${conComuna ? `, ${comunaTxt}` : ''}`,
    ...(monto === null || monto === 0 ? []
      : [`Total a pagar: ${clpTxt(monto)}${conFactura ? ' con IVA' : ' (sin factura)'}`
        + (formaPago !== '' ? `, ${formaPago}` : '')]), '',
    'Cualquier cambio o duda me avisa por acá.',
  ].join('\n');
}

try {
  // si este chat YA tiene una entrega en el sistema, se CORRIGE esa (no se crea otra)
  const entregaPrevia = enlaceDe(jid);
  const esCorreccion = entregaPrevia !== null || texto(args._yaSalio) === 'si';
  if (entregaPrevia !== null) d.entrega_id = entregaPrevia;

  // la versión ANTERIOR se lee ANTES de que el re-despacho la pise (para el diff del 🔄)
  const previa = esCorreccion ? await datosEntregaPrevia(entregaPrevia) : null;

  const prep = await prepararEntrega(d, jid, nombre, texto(args.telefono_cliente), { dry });
  // el monto que ve el cliente sale del MISMO objeto que ve el repartidor
  const confirmacionCliente = armarConfirmacionCliente(prep.entrega);
  const avisoOverride = texto(args.mensaje_repartidor);
  const idParaLink = prep.entrega?.id || d.entrega_id || null;
  const aviso = (avisoOverride !== '' ? avisoOverride
    : (esCorreccion ? mensajeDeCambio(prep.entrega, previa, prep.subida) : prep.resumen))
    + (idParaLink !== null ? `\n\n📋 Su tarjeta: ${linkEntrega(idParaLink)}` : '');

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
  // un CAMBIO sale citando el aviso original de esa entrega (contexto entero de un toque)
  const citaCambio = esCorreccion
    ? await idAvisoOriginal(convRepartidor, [nombre, String(idParaLink || '').slice(-4)])
    : undefined;
  await enviarPorDixdybot(convRepartidor, aviso, citaCambio);
  /* EL OVERRIDE SIGUE AL RE-DESPACHO (3-sep, caso Joel): la vista del repartidor pinta
     la fecha de `entrega_estado` (la movida manual del panel) POR ENCIMA de la tarjeta.
     Un re-despacho con fecha nueva dejaba ese override viejo mandando para siempre: la
     tarjeta decía lunes 7 y la vista seguía en jueves 3 (o al revés). El despacho es la
     palabra más fresca del negocio: si hay override con OTRA fecha, se alinea. */
  if (esCorreccion && idParaLink !== null && fecha !== '' && !dry) {
    try {
      const { execFileSync } = await import('node:child_process');
      execFileSync('python3', ['-c', [
        'import sys, json, urllib.request',
        `sys.path.insert(0, '/Users/alejandroriveracarrasco/SaSS/destaperapido/cotizaciones-destape-rapido/resumen-repartidor/scripts')`,
        'import generar_listado as gl',
        `eid = ${JSON.stringify(idParaLink)}`,
        `fnueva = ${JSON.stringify(fecha)}`,
        'h = {"apikey": gl.SUPABASE_ANON_KEY, "authorization": "Bearer " + gl.SUPABASE_ANON_KEY}',
        'req = urllib.request.Request(f"{gl.SUPABASE_URL}/rest/v1/entrega_estado?id=eq.{eid}&select=fecha", headers=h)',
        'filas = json.load(urllib.request.urlopen(req, timeout=20))',
        'if filas and filas[0].get("fecha") and filas[0]["fecha"] != fnueva:',
        '    cuerpo = json.dumps({"fecha": fnueva}).encode()',
        '    p = urllib.request.Request(f"{gl.SUPABASE_URL}/rest/v1/entrega_estado?id=eq.{eid}", data=cuerpo, method="PATCH", headers={**h, "content-type": "application/json", "prefer": "return=minimal"})',
        '    urllib.request.urlopen(p, timeout=20)',
        '    print("override " + filas[0]["fecha"] + " -> " + fnueva)',
      ].join('\n')], { timeout: 30_000 });
    } catch (e) {
      console.log(`⚠️ no pude alinear la fecha manual de la vista del repartidor: `
        + String(e.message || e).slice(0, 150) + ' — revísala en la página');
    }
  }
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
