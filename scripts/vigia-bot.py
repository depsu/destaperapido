#!/usr/bin/env python3
"""Vigía del dixdybot — auditoría automática de los patrones que YA nos mordieron.

Nace el 3-sep-2026 del reclamo de Alejandro («todos los días salen bugs... ¿es posible
crear una auditoría?»). No adivina bugs nuevos: vigila los PATRONES reales del historial
de esta semana, los que se repitieron:

  1. PROMESA SIN CUMPLIR — el bot dice «se la mando de inmediato» y la cotización nunca
     sale (casos Felipe Hernández y Sebastián de Batuco, mismo patrón 2 veces).
  2. FICHA COMPLETA SIN PRECIO DE LISTA — correo+comuna+duración listos, monto NULL por
     más de 1 h: el auto-envío está trabado por lo que sea («un día» no parseado, etc.).
  3. FAMILIA DEL ÍTEM SUCIA — item_extra negado («ninguno»/«no») con valor_item_extra o
     fecha_limpieza vivos (el PDF «Ninguno — $140.000» del colegio de Colina).
  4. SOSPECHA DE IVA DOBLE — monto_conversado ≈ monto_neto × 1.19 (el $254.898 de Batuco).

Solo LECTURA sobre bot.db (WAL: abrir readonly no molesta al escritor). Avisa por la
bandeja (avisar.py) SOLO si encuentra algo nuevo; deduplica por caso en vigia-bot-estado.json
para no ladrar dos veces lo mismo. Sensor barato 🚨 de la doctrina: el juicio caro lo
pone Alejandro (o la sesión de turno) cuando llega el aviso.
"""
import json
import re
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

CLON = Path('/Users/alejandroriveracarrasco/SaSS/DIXDY/clientes/destaperapido')
DB = CLON / 'dixdybot-data' / 'bot.db'
ESTADO = CLON / 'scripts' / 'vigia-bot-estado.json'
AVISAR = '/Users/alejandroriveracarrasco/SaSS/DIXDY/scripts/avisar.py'

VENTANA_H = 24          # cuántas horas hacia atrás mira cada corrida
PROMESA_MIN = 30        # minutos de gracia antes de acusar una promesa sin cumplir
# Solo la promesa FIRME («de inmediato/al tiro»): la oferta condicionada («le mando la
# cotización, ¿a qué correo?») no cuenta — el cliente aún debe algo (1ª corrida: Humberto).
RE_PROMESA = re.compile(r'se l[ao] (?:mando|env[ií]o) (?:de inmediato|al tiro)', re.I)
# 5 · PLANTILLA DE DEGRADACIÓN sin respuesta real después (3-sep, caso Miguel: el cerebro
# tuvo 20 min de timeouts, 3 clientes recibieron «Dame un momento, ya te confirmo» y
# nadie volvió a escribirles). El texto vive en cerebro/ajustes; se cazan las conocidas.
RE_PLANTILLA = re.compile(r'^Dame un momento, ya te confirmo\.?$'
                          r'|^D[eé]jame confirmarlo bien y te escribo al tiro\.?$', re.I)
RE_CUMPLIDA = re.compile(r'Cotizaci[oó]n formal|Cotizaci[oó]n enviada|cotizaci[oó]n en PDF', re.I)
RE_NEGADO = re.compile(r'^(no|ninguno|ninguna|nada|sin\s+\S*|0|-)$', re.I)


def cargar_estado() -> dict:
    try:
        return json.loads(ESTADO.read_text())
    except Exception:
        return {'avisados': []}


def hallazgos(db: sqlite3.Connection) -> list[tuple[str, str]]:
    """Lista de (clave-dedup, texto humano)."""
    ahora = int(time.time() * 1000)
    desde = ahora - VENTANA_H * 3600_000
    out: list[tuple[str, str]] = []

    # 1 · promesas de cotización sin cumplir
    filas = db.execute(
        """SELECT m.id, m.ts, m.conversacion_id, c.conv_id, ct.nombre
             FROM mensajes m
             JOIN conversaciones c ON c.id = m.conversacion_id
             LEFT JOIN contactos ct ON ct.id = c.contacto_id
            WHERE m.tipo = 'saliente' AND m.ts > ? AND m.ts < ?""",
        (desde, ahora - PROMESA_MIN * 60_000)).fetchall()
    for mid, ts, conv_num, conv_id, nombre in filas:
        texto = db.execute('SELECT texto FROM mensajes WHERE id = ?', (mid,)).fetchone()[0]
        if not RE_PROMESA.search(texto):
            continue
        despues = db.execute(
            """SELECT count(*) FROM mensajes WHERE conversacion_id = ? AND ts > ?
                AND (tipo = 'actividad' OR tipo = 'saliente')""", (conv_num, ts)).fetchone()[0]
        # el cumplimiento puede llegar ANTES que la frase (carrera de 30 s del caso
        # Carolina, 1ª corrida): se busca desde 10 min antes de la promesa
        cumplida = db.execute(
            """SELECT count(*) FROM mensajes WHERE conversacion_id = ? AND ts > ?
                AND texto LIKE '%otizaci%'""", (conv_num, ts - 600_000)).fetchone()[0]
        if cumplida == 0:
            quien = nombre or conv_id[-12:]
            out.append((f'promesa-{mid}',
                        f'🕳️ PROMESA SIN CUMPLIR: el bot le dijo a {quien} que mandaba la '
                        f'cotización «de inmediato» hace más de {PROMESA_MIN} min y no hay '
                        f'rastro del envío. Revisar el chat y mandarla.'))
        _ = despues  # (conteo disponible si se quiere afinar el criterio)

    # 5 · plantilla de degradación sin respuesta real después (el cliente quedó colgado)
    for mid, ts, conv_num, conv_id, nombre in filas:
        texto = db.execute('SELECT texto FROM mensajes WHERE id = ?', (mid,)).fetchone()[0]
        if not RE_PLANTILLA.match(texto.strip()):
            continue
        real_despues = db.execute(
            """SELECT count(*) FROM mensajes WHERE conversacion_id = ? AND ts > ?
                AND tipo = 'saliente'""", (conv_num, ts)).fetchone()[0]
        # una DUDA abierta cubre el caso: el «te confirmo» de las dudas tiene dueño
        duda_viva = db.execute(
            """SELECT count(*) FROM dudas WHERE conversacion_id = ?
                AND fase != 'resuelta' AND creada_ts > ?""",
            (conv_num, ts - 300_000)).fetchone()[0]
        if real_despues == 0 and duda_viva == 0:
            quien = nombre or conv_id[-12:]
            out.append((f'colgado-{mid}',
                        f'🕳️ CLIENTE COLGADO: a {quien} se le dijo «{texto.strip()[:45]}» '
                        f'hace más de {PROMESA_MIN} min y nadie volvió a escribirle (ni hay '
                        f'duda abierta) — típico de una caída del cerebro. Forzar el turno '
                        f'con «que el bot responda ahora» o contestarle a mano.'))

    # 2-3-4 · invariantes de ficha en pedidos activos
    pedidos = db.execute(
        """SELECT id, monto_neto, datos, actualizado_ts FROM pedidos
            WHERE etapa IN ('cotizando', 'por-confirmar') AND actualizado_ts > ?""",
        (desde - 6 * 24 * 3600_000,)).fetchall()
    for pid, monto, datos_crudo, act_ts in pedidos:
        try:
            d = json.loads(datos_crudo)
        except Exception:
            continue
        v = lambda k: str(d.get(k) or '').strip()          # noqa: E731

        if (monto is None and v('correo') and v('comuna') and v('duracion')
                and act_ts < ahora - 3600_000):
            out.append((f'sinlista-{pid}',
                        f'🕳️ FICHA COMPLETA SIN PRECIO: {pid} tiene correo, comuna y '
                        f'duración («{v("duracion")[:40]}») hace más de 1 h y el monto '
                        f'sigue vacío — el auto-envío está trabado. Fijar el monto a mano '
                        f'o revisar por qué el tarifario no lo lee.'))

        if RE_NEGADO.match(v('item_extra')) and (v('valor_item_extra') not in ('', '0')
                                                 or v('fecha_limpieza') != ''):
            out.append((f'familia-{pid}',
                        f'🕳️ ÍTEM NEGADO CON RESTOS: {pid} dice item_extra '
                        f'«{v("item_extra")}» pero el valor o la fecha de limpieza siguen '
                        f'vivos — un PDF podría imprimir «Ninguno — $X». Vaciar los campos.'))

        try:
            conversado = float(re.sub(r'\D', '', v('monto_conversado')) or 0)
        except Exception:
            conversado = 0
        if monto and conversado and abs(conversado - monto * 1.19) < monto * 0.01:
            out.append((f'ivadoble-{pid}',
                        f'🕳️ SOSPECHA DE IVA DOBLE: en {pid} lo conversado '
                        f'(${conversado:,.0f}) es exactamente el monto + IVA — si un PDF '
                        f'sale de lo conversado, cobrará IVA dos veces.'))
    return out


def main() -> None:
    db = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    estado = cargar_estado()
    nuevos = [(k, t) for k, t in hallazgos(db) if k not in estado['avisados']]
    if not nuevos:
        print('vigía: sin hallazgos nuevos')
        return
    for k, t in nuevos:
        print(t)
        estado['avisados'].append(k)
    estado['avisados'] = estado['avisados'][-500:]
    ESTADO.write_text(json.dumps(estado))
    if '--sin-aviso' not in sys.argv:
        resumen = f'Vigía del bot: {len(nuevos)} hallazgo(s) — ' \
            + ' · '.join(t.split(':', 1)[0].replace('🕳️ ', '') for t, in [(t,) for _, t in nuevos][:4])
        subprocess.run(['python3', AVISAR, resumen, '--titulo', 'Vigía dixdybot'],
                       timeout=30, check=False)


if __name__ == '__main__':
    main()
