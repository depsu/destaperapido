#!/usr/bin/env python3
# sync-repartidor.py: EL REPARTIDOR MANDA (28-ago-2026, regla de Alejandro tras el caso
# Óscar; reescrito el 10-sep-2026, P12): lo que el repartidor marca en su página (Supabase
# `entrega` + `entrega_estado`) es la palabra final sobre cada entrega, y el bot tiene que
# enterarse solo: la FECHA (si allá se reagendó, la ficha se alinea) y el ESTADO (cobrado
# allá = Cobrado acá; entregado, pendiente, pagado por adelantado o borrada quedan como
# chip en la tarjeta del tablero). Todo entra por UN endpoint genérico del molde,
# `POST /api/pedidos/<id>/externo`, que guarda lo informado en la ficha y mueve de etapa
# por el escritor con origen «externo» (el embudo del clon decide qué transiciones acepta).
# Jamás la base a mano: bot.db se abre SOLO en lectura, para saber qué ya se informó.
#
# Lo que parió la reescritura: el sensor viejo solo bajaba la fecha (0 pedidos en Cobrado
# con 68 cobrados en el repartidor, 12 «atrasadas» que ya se habían cobrado) y casaba por
# los últimos 4 dígitos del teléfono, que NO es inequívoco: el 9-sep le cambió la fecha a
# p-251 (Claudia, …9654) con la entrega de Sandra (cuyo respaldo también termina en 9654).
#
# IDENTIDAD pedido ↔ entrega, la primera que calce, en este orden:
#   1. `datos.entrega_id` de la ficha (los migrados lo traen; el endpoint lo rellena al
#      primer informe, así que desde el segundo tick todos resuelven por acá);
#   2. enlaces.json del whatsapp-bot viejo (lo escribe el conector avisar-repartidor:
#      jid del chat → id de la entrega; un chat con dos entregas guarda LA ÚLTIMA). Ese
#      link vale SOLO si la entrega enlazada no está ya hecha (entregado o cobrado) con
#      fecha ANTERIOR a la fecha de la ficha: una entrega hecha no puede ser de un servicio
#      posterior (caso p-155, Catalina Lagos: la ficha del 11-sep tenía el link a la
#      entrega del 04-sep, ya cobrada; el tick la habría mandado a Cobrado y pisado la
#      fecha del evento de mañana). Con el link viejo el chat queda «sin vínculo» y no se
#      toca; cuando el conector selle la entrega nueva, el link se renueva solo.
#   3. la cola de 4 dígitos del teléfono SOLO si además un trozo del nombre del contacto
#      (más de 3 letras) aparece en el id y queda exactamente una candidata (y con el
#      mismo filtro de entrega hecha anterior a la ficha).
#   Si nada calza: «sin vínculo», y no se toca nada.
#
# El panel puede pedir clave (ajuste panel.token_escritura): si no es null, cada POST al
# panel lleva el header x-dixdy-token; sin eso el candado devuelve 401 a todo el tick.
#
# Uso:
#   python3 sync-repartidor.py --dry     # tabla completa de lo que haría, no toca nada
#   python3 sync-repartidor.py           # informa al panel y deja bitácora en sync-repartidor.log
# launchd: com.destaperapido.sync-repartidor (cada 900 s). Sin dependencias (urllib pelado).
from __future__ import annotations

import datetime
import json
import re
import sqlite3
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable, Optional

BASE = Path(__file__).resolve().parent.parent
DB = BASE / 'dixdybot-data' / 'bot.db'
AQUI = Path(__file__).resolve().parent
LOG = AQUI / 'sync-repartidor.log'
# el contador de fallos seguidos del panel (se borra cuando vuelve)
ESTADO = AQUI / 'sync-repartidor.estado.json'
PANEL = 'http://127.0.0.1:8793'
# el ajuste del panel del clon (rige en vivo): de ahí sale la clave de escritura, si hay
PANEL_AJUSTES = BASE / 'dixdybot-data' / 'ajustes' / 'panel.json'
FUENTE = 'repartidor-supabase'
# las credenciales viven donde siempre (la página del repartidor); RLS acota el acceso
GENERADOR = Path('/Users/alejandroriveracarrasco/SaSS/destaperapido/'
                 'cotizaciones-destape-rapido/resumen-repartidor/scripts/generar_listado.py')
# el puente jid → id de entrega que sella el conector avisar-repartidor.mjs
ENLACES = Path('/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/data/enlaces.json')
AVISAR = ['python3', '/Users/alejandroriveracarrasco/SaSS/DIXDY/scripts/avisar.py']
ETAPAS_ENTREGA = ('por-entregar', 'por-confirmar')
FALLOS_PARA_AVISAR = 3            # 3 ticks de 900 s = 45 min sin panel

# El estado del repartidor → la etapa que se le pide al bot. Solo «cobrado» mueve: las
# demás son información (quedan como chip en la tarjeta) y el dueño decide. Semántica del
# carril del repartidor (carril-repartidor.py): entregado + cobro = cobrado;
# pagado-pendiente = cobro adelantado sin entrega.
MAPEO = {
    'cobrado': 'cobrado',
    'entregado': None,
    'pagado-pendiente': None,
    'pendiente': None,
    'en-camino': None,
}
# Las etiquetas TAL CUAL las muestra la página del repartidor (generar_listado.py).
ETIQUETAS = {
    'pendiente': 'Pendiente',
    'en-camino': 'En camino',
    'entregado': 'Entregado',
    'cobrado': 'Cliente ya pagó',
    'pagado-pendiente': 'Pagó · falta entregar',
}
ELIMINADO = 'eliminado'
ETIQUETA_ELIMINADA = 'borrada en el repartidor'
# estados con la entrega ya hecha: un link a una de estas con fecha anterior a la ficha
# es de un servicio pasado del mismo chat, no de este pedido
TERMINADOS = ('entregado', 'cobrado')
VIA_LINK_VIEJO = 'sin vínculo: el link del chat es de una entrega anterior'

Estado = dict[str, Any]


def anotar(msg: str, dry: bool = False) -> None:
    linea = f'{datetime.datetime.now().isoformat(timespec="seconds")} {msg}'
    print(linea)
    if not dry:
        with LOG.open('a') as f:
            f.write(linea + '\n')


def credenciales() -> tuple[str, str]:
    src = GENERADOR.read_text()
    url = re.search(r'SUPABASE_URL = "([^"]+)"', src).group(1)
    bloque = re.search(r'SUPABASE_ANON_KEY = \(\s*((?:"[^"]*"\s*)+)\)', src).group(1)
    key = ''.join(re.findall(r'"([^"]*)"', bloque))
    return url, key


def http_json(url: str, data: Optional[dict] = None, headers: Optional[dict] = None,
              method: str = 'GET', timeout: int = 20) -> Any:
    """Una sola puerta HTTP (los tests la reemplazan). Devuelve el JSON de la respuesta;
    un estado HTTP de error sube como urllib.error.HTTPError."""
    cuerpo = json.dumps(data).encode() if data is not None else None
    cab = {'content-type': 'application/json'} if data is not None else {}
    cab.update(headers or {})
    req = urllib.request.Request(url, data=cuerpo, headers=cab, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        crudo = r.read()
    return json.loads(crudo) if crudo else {}


def cabeceras_panel() -> dict[str, str]:
    """La clave de escritura del panel (ajuste panel.token_escritura), como header. Sin
    archivo o con null: sin header, como hasta ahora."""
    try:
        d = json.loads(PANEL_AJUSTES.read_text())
        token = d.get('token_escritura') if isinstance(d, dict) else None
    except Exception:           # noqa: BLE001: sin ajuste legible = panel sin clave
        token = None
    return {'x-dixdy-token': str(token)} if token else {}


def supa(url: str, key: str, path: str) -> Any:
    return http_json(f'{url}/rest/v1/{path}',
                     headers={'apikey': key, 'Authorization': f'Bearer {key}'})


def slug(s: str) -> str:
    s = unicodedata.normalize('NFD', (s or '').lower())
    return re.sub(r'[^a-z0-9]+', '-', ''.join(c for c in s if not unicodedata.combining(c)))


def a_ms(iso: Optional[str]) -> Optional[int]:
    """'2026-09-07T14:09:12.12345+00:00' → ms desde epoch. A mano porque el Python del
    sistema (3.9) no traga la fracción de 5 dígitos ni la 'Z' de Supabase."""
    if not iso:
        return None
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?'
                 r'(Z|[+-]\d{2}:?\d{2})?$', str(iso).strip())
    if not m:
        return None
    frac = (m.group(7) or '')[:6].ljust(6, '0')
    base = datetime.datetime(*(int(m.group(i)) for i in range(1, 7)), int(frac),
                             tzinfo=datetime.timezone.utc)
    z = m.group(8)
    if z and z != 'Z':
        signo = 1 if z[0] == '+' else -1
        hh, mm = int(z[1:3]), int(z[-2:])
        base -= signo * datetime.timedelta(hours=hh, minutes=mm)
    return int(base.timestamp() * 1000)


# ── lo que hay a cada lado ────────────────────────────────────────────────────
def leer_enlaces() -> dict[str, str]:
    """jid → id de entrega. Si el archivo no está, se sigue sin él (y se anota)."""
    try:
        d = json.loads(ENLACES.read_text())
        links = d.get('links') if isinstance(d, dict) else None
        return {str(k): str(v) for k, v in (links or {}).items() if v}
    except Exception as e:      # noqa: BLE001: sin puente no se cae el sensor
        anotar(f'sin enlaces.json ({e}): identidad solo por entrega_id y cola con nombre')
        return {}


def leer_pedidos(db: Path = DB) -> list[dict]:
    """Los pedidos del bot en etapa de entrega, con lo que hace falta para identificarlos
    y para saber qué ya se informó. SOLO LECTURA."""
    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    try:
        filas = con.execute(
            """SELECT p.id, p.etapa, p.conversacion_id, co.telefono, co.nombre,
                      json_extract(p.datos, '$.fecha_entrega'),
                      json_extract(p.datos, '$.entrega_id'),
                      json_extract(p.datos, '$._externo')
                 FROM pedidos p
                 LEFT JOIN conversaciones c ON c.conv_id = p.conversacion_id
                 LEFT JOIN contactos co ON co.id = c.contacto_id
                WHERE p.etapa IN (?, ?)""", ETAPAS_ENTREGA).fetchall()
    finally:
        con.close()
    pedidos = []
    for pid, etapa, conv_id, telefono, nombre, fecha, entrega_id, externo in filas:
        ext = None
        if externo:
            try:
                ext = json.loads(externo)
            except Exception:   # noqa: BLE001: un _externo ilegible = como si no hubiera
                ext = None
        pedidos.append({'pid': pid, 'etapa': etapa, 'conv_id': conv_id or '',
                        'telefono': telefono or '', 'nombre': nombre or '',
                        'fecha_ficha': (str(fecha)[:10] if fecha else None),
                        'entrega_id': (str(entrega_id).strip() if entrega_id else None),
                        'externo': ext if isinstance(ext, dict) else None})
    return pedidos


def leer_agenda(url: str, key: str) -> tuple[dict[str, dict], dict[str, dict]]:
    """`entrega` (id, fecha base, eliminado) y `entrega_estado` COMPLETOS: sin corte de
    días, con eliminadas, porque una entrega borrada allá también es información."""
    entregas = {e['id']: e for e in supa(
        url, key, 'entrega?select=id,fecha,eliminado,updated_at&limit=10000')}
    estados = {e['id']: e for e in supa(
        url, key, 'entrega_estado?select=id,estado,fecha,eliminado,updated_at,pagada_at&limit=10000')}
    return entregas, estados


# ── identidad y estado ────────────────────────────────────────────────────────
def entrega_anterior_a_la_ficha(pedido: dict, ref: str, agenda: Optional[tuple[dict, dict]]) -> bool:
    """True si la entrega `ref` ya está hecha (entregado/cobrado) con fecha ANTERIOR a la
    fecha de la ficha: entonces es un servicio pasado del mismo chat, no este pedido."""
    fecha_ficha = str(pedido.get('fecha_ficha') or '')
    # solo con fecha ISO en la ficha: con texto libre («01 de septiembre») no se compara
    if agenda is None or not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_ficha):
        return False
    est = estado_de(ref, agenda[0], agenda[1])
    if est is None or est['eliminado'] or est['estado'] not in TERMINADOS:
        return False
    return bool(est['fecha_base']) and str(est['fecha_base']) < fecha_ficha


def resolver(pedido: dict, links: dict[str, str], ids: set[str],
             agenda: Optional[tuple[dict, dict]] = None) -> tuple[Optional[str], str]:
    """(id de entrega, vía) o (None, 'sin vínculo…'). Ver el orden en la cabecera. `agenda`
    = (entregas, estados) para descartar un link a una entrega ya hecha antes de la ficha."""
    if pedido.get('entrega_id'):
        return pedido['entrega_id'], 'entrega_id'
    jid = re.sub(r'^wa-baileys:', '', pedido.get('conv_id') or '')
    if jid and jid in links:
        if entrega_anterior_a_la_ficha(pedido, links[jid], agenda):
            return None, VIA_LINK_VIEJO
        return links[jid], 'enlaces.json'
    cola = (pedido.get('telefono') or '')[-4:]
    if len(cola) == 4:
        trozos = [t for t in slug(pedido.get('nombre') or '').split('-') if len(t) > 3]
        candidatas = [eid for eid in ids
                      if eid.endswith(f'-{cola}') and any(t in eid for t in trozos)
                      and not entrega_anterior_a_la_ficha(pedido, eid, agenda)]
        if len(candidatas) == 1:
            return candidatas[0], 'cola+nombre'
    return None, 'sin vínculo'


def estado_de(ref: str, entregas: dict[str, dict], estados: dict[str, dict]) -> Optional[Estado]:
    """Lo que el repartidor dice de esa entrega, o None si ni siquiera existe allá."""
    entrega = entregas.get(ref)
    est = estados.get(ref)
    if entrega is None and est is None:
        return None
    eliminado = bool((est or {}).get('eliminado')) or bool((entrega or {}).get('eliminado'))
    fecha = (est or {}).get('fecha') or (entrega or {}).get('fecha')
    fecha = str(fecha)[:10] if fecha else None
    ts = a_ms((est or {}).get('updated_at')) or a_ms((entrega or {}).get('updated_at'))
    if eliminado:
        return {'estado': ELIMINADO, 'etiqueta': ETIQUETA_ELIMINADA, 'fecha': None,
                'fecha_base': fecha, 'ts': ts, 'eliminado': True}
    # referencia sin fila en entrega_estado: pendiente con la fecha base (entregas futuras)
    estado = str((est or {}).get('estado') or 'pendiente')
    return {'estado': estado, 'etiqueta': ETIQUETAS.get(estado, estado), 'fecha': fecha,
            'fecha_base': fecha, 'ts': ts, 'eliminado': False}


def cuerpo_de(ref: str, est: Estado, ahora_ms: int) -> dict:
    return {'fuente': FUENTE, 'ref': ref, 'estado': est['estado'],
            'etiqueta': est['etiqueta'], 'fecha': est['fecha'],
            'a': MAPEO.get(est['estado']), 'ts': est['ts'] or ahora_ms}


def ya_informado(externo: Optional[dict], cuerpo: dict) -> bool:
    """Lo que la ficha ya guarda es igual a lo que se iría a informar: nada que hacer."""
    if not externo or externo.get('fuente') != FUENTE:
        return False
    return all(externo.get(k) == cuerpo.get(k) for k in ('ref', 'estado', 'fecha', 'ts'))


# ── el panel ──────────────────────────────────────────────────────────────────
def leer_estado_fallos() -> dict:
    try:
        d = json.loads(ESTADO.read_text())
        return d if isinstance(d, dict) else {}
    except Exception:           # noqa: BLE001: sin archivo = sin fallos
        return {}


def panel_caido(error: str, avisar: Callable[[str], None]) -> None:
    """Cuenta fallos seguidos; al tercero avisa UNA vez. El archivo se borra al volver."""
    d = leer_estado_fallos()
    fallos = int(d.get('fallos') or 0) + 1
    avisado = bool(d.get('avisado'))
    if fallos >= FALLOS_PARA_AVISAR and not avisado:
        avisar('El sensor del repartidor lleva 45 min sin poder sincronizar')
        avisado = True
    ESTADO.write_text(json.dumps({'fallos': fallos, 'avisado': avisado, 'error': error,
                                  'ultimo': datetime.datetime.now().isoformat(timespec='seconds')},
                                 ensure_ascii=False, indent=1))


def panel_volvio() -> None:
    if ESTADO.exists():
        ESTADO.unlink()


def avisar_dueno(msg: str) -> None:
    try:
        subprocess.run(AVISAR + [msg, '--titulo', 'destaperapido'], timeout=30, check=False)
    except Exception as e:      # noqa: BLE001: el aviso no puede tumbar el sensor
        anotar(f'no se pudo avisar: {e}')


def latir(ok: bool, revisados: int, cambiados: int, detalle: Optional[str], ahora_ms: int) -> None:
    try:
        http_json(f'{PANEL}/api/externos/{FUENTE}/latido',
                  data={'ok': ok, 'ts': ahora_ms, 'revisados': revisados,
                        'cambiados': cambiados, 'detalle': detalle},
                  headers=cabeceras_panel(), method='POST')
    except Exception as e:      # noqa: BLE001: un panel viejo sin la ruta no es un error del sensor
        anotar(f'latido no aceptado por el panel ({e})')


# ── la corrida ────────────────────────────────────────────────────────────────
def main(dry: bool = False) -> int:
    ahora_ms = int(datetime.datetime.now().timestamp() * 1000)
    # 0) el panel arriba, o nada que hacer (el sensor jamás escribe a la DB directo)
    try:
        http_json(f'{PANEL}/api/hoy', timeout=5)
    except Exception as e:      # noqa: BLE001: se cuenta y se reintenta al próximo tick
        if not dry:
            panel_caido(str(e), avisar_dueno)
        anotar(f'panel caído ({e}); se reintenta al próximo tick', dry)
        return 0
    if not dry:
        panel_volvio()

    revisados = 0
    cambiados = 0
    try:
        url, key = credenciales()
        entregas, estados = leer_agenda(url, key)
        links = leer_enlaces()
        pedidos = leer_pedidos()
        ids = set(entregas) | set(estados)
        if dry:
            print('pid | vía | ref | estado | eliminado | fecha ficha → repartidor | etapa destino')
        panel_sin_ruta = False
        cabeceras = cabeceras_panel()
        for p in pedidos:
            revisados += 1
            ref, via = resolver(p, links, ids, (entregas, estados))
            if ref is None:
                if via == VIA_LINK_VIEJO:
                    # se anota siempre: es el caso que pisaría una ficha ajena (p-155)
                    anotar(f'{p["pid"]} ({p["nombre"]}): {via}; ficha {p["fecha_ficha"]}, '
                           f'no se toca', dry)
                if dry:
                    print(f'{p["pid"]} ({p["nombre"]}) | {via} | - | - | - | {p["fecha_ficha"]} | -')
                continue
            est = estado_de(ref, entregas, estados)
            if est is None:
                anotar(f'{p["pid"]} ({p["nombre"]}): la referencia {ref} [{via}] no está en la agenda', dry)
                continue
            cuerpo = cuerpo_de(ref, est, ahora_ms)
            if dry:
                print(f'{p["pid"]} ({p["nombre"]}) | {via} | {ref} | {est["estado"]} | '
                      f'{"sí" if est["eliminado"] else "no"} | {p["fecha_ficha"]} → {est["fecha_base"]} | '
                      f'{cuerpo["a"] or "(se queda)"}'
                      f'{" | ya informado" if ya_informado(p["externo"], cuerpo) else ""}')
            if ya_informado(p['externo'], cuerpo):
                continue
            if dry or panel_sin_ruta:
                continue
            try:
                r = http_json(f'{PANEL}/api/pedidos/{urllib.parse.quote(p["pid"])}/externo',
                              data=cuerpo, headers=cabeceras, method='POST')
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    # el panel de antes de P12: sin la ruta no hay nada que informar este tick
                    anotar('el panel no conoce /externo todavía (falta reiniciar el bot); '
                           'este tick no informa nada', dry)
                    panel_sin_ruta = True
                    continue
                raise
            cambiados += 1
            anotar(f'{p["pid"]} ({p["nombre"]}): repartidor {est["estado"]} {est["fecha_base"] or "sin fecha"} '
                   f'[{ref}, {via}] → {"movido a " + str(r.get("etapa")) if r.get("movido") else "no movido"}'
                   f'{": " + str(r["motivo"]) if r.get("motivo") else ""}', dry)
        if cambiados:
            anotar(f'listo: {cambiados} pedido(s) informado(s) al panel de {revisados} revisados', dry)
        if not dry:
            latir(True, revisados, cambiados, None, ahora_ms)
        return 0
    except Exception as e:      # noqa: BLE001: el latido cuenta el fallo; launchd reintenta
        anotar(f'la corrida se cayó: {e}', dry)
        if not dry:
            latir(False, revisados, cambiados, str(e), ahora_ms)
        return 1


if __name__ == '__main__':
    sys.exit(main(dry='--dry' in sys.argv))
