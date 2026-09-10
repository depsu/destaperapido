#!/usr/bin/env python3
# Tests del sensor del repartidor (P12, 10-sep-2026). Sin red y sin tocar bot.db: se
# reemplazan la puerta HTTP (http_json), la lectura de pedidos, los enlaces y el aviso.
# Los casos son los REALES del 10-sep (ids de entrega y pedidos del clon), porque el
# error que se corrige (p-251 pisada con la entrega de Sandra) solo se ve con ellos.
#   python3 sync-repartidor.test.py
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('sync_repartidor', AQUI / 'sync-repartidor.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

ENTREGAS = {
    '2026-09-09-tono-7799': {'id': '2026-09-09-tono-7799', 'fecha': '2026-09-09', 'eliminado': False,
                             'updated_at': '2026-09-09T12:00:00+00:00'},
    '2026-09-10-sandra-9654': {'id': '2026-09-10-sandra-9654', 'fecha': '2026-09-10', 'eliminado': False,
                               'updated_at': '2026-09-10T12:00:00+00:00'},
    '2026-07-30-dominga-8022': {'id': '2026-07-30-dominga-8022', 'fecha': '2026-07-31', 'eliminado': False,
                                'updated_at': '2026-07-30T12:00:00+00:00'},
    '2026-08-19-dominga-8022': {'id': '2026-08-19-dominga-8022', 'fecha': '2026-08-19', 'eliminado': False,
                                'updated_at': '2026-08-19T12:00:00+00:00'},
    '2026-09-12-deyanira-0609': {'id': '2026-09-12-deyanira-0609', 'fecha': '2026-09-12', 'eliminado': False,
                                 'updated_at': '2026-09-01T12:00:00.12345+00:00'},
    '2026-07-21-cliente-1182': {'id': '2026-07-21-cliente-1182', 'fecha': '2026-08-22', 'eliminado': False,
                                'updated_at': '2026-07-21T12:00:00Z'},
    # el primer servicio de Catalina (30 baños en Buin, 04-05 sep), cobrado el 07-sep; el
    # chat guarda ESTE link aunque la ficha viva ya es el evento del 12-09 (montaje 11-09)
    '2026-09-04-catalina-lagos-gc-3468': {'id': '2026-09-04-catalina-lagos-gc-3468', 'fecha': '2026-09-04',
                                          'eliminado': False, 'updated_at': '2026-09-03T12:00:00+00:00'},
    # y p-47 (Alfredo): dos entregas en un chat, el link guarda la última (27-ago) y la ficha
    # dice 17-ago: la entrega es POSTERIOR a la ficha, así que el link sigue valiendo
    '2026-08-27-alfredo-0775': {'id': '2026-08-27-alfredo-0775', 'fecha': '2026-08-27', 'eliminado': False,
                                'updated_at': '2026-08-26T12:00:00+00:00'},
}
ESTADOS = {
    '2026-09-09-tono-7799': {'id': '2026-09-09-tono-7799', 'estado': 'cobrado', 'fecha': None,
                             'eliminado': False, 'updated_at': '2026-09-09T20:30:00.5+00:00', 'pagada_at': None},
    '2026-09-10-sandra-9654': {'id': '2026-09-10-sandra-9654', 'estado': 'cobrado', 'fecha': None,
                               'eliminado': False, 'updated_at': '2026-09-10T15:00:00+00:00', 'pagada_at': None},
    '2026-07-30-dominga-8022': {'id': '2026-07-30-dominga-8022', 'estado': 'cobrado', 'fecha': None,
                                'eliminado': False, 'updated_at': '2026-07-31T15:00:00+00:00', 'pagada_at': None},
    '2026-08-19-dominga-8022': {'id': '2026-08-19-dominga-8022', 'estado': 'cobrado', 'fecha': None,
                                'eliminado': True, 'updated_at': '2026-08-20T15:00:00+00:00', 'pagada_at': None},
    '2026-07-21-cliente-1182': {'id': '2026-07-21-cliente-1182', 'estado': 'pagado-pendiente', 'fecha': None,
                                'eliminado': True, 'updated_at': '2026-07-22T15:00:00+00:00', 'pagada_at': None},
    '2026-09-04-catalina-lagos-gc-3468': {'id': '2026-09-04-catalina-lagos-gc-3468', 'estado': 'cobrado',
                                          'fecha': None, 'eliminado': False,
                                          'updated_at': '2026-09-07T14:09:12.12345+00:00',
                                          'pagada_at': '2026-09-07T14:09:12+00:00'},
    '2026-08-27-alfredo-0775': {'id': '2026-08-27-alfredo-0775', 'estado': 'cobrado', 'fecha': None,
                                'eliminado': False, 'updated_at': '2026-08-28T15:00:00+00:00', 'pagada_at': None},
}
# nota: 2026-09-12-deyanira-0609 NO tiene fila en entrega_estado (entrega futura)

LINKS = {'143306029842440@lid': '2026-09-09-tono-7799',
         '105737934102556@lid': '2026-09-10-sandra-9654',
         '17654321098765@lid': '2026-09-12-deyanira-0609',
         '266391840112774@lid': '2026-09-04-catalina-lagos-gc-3468',
         '99000000000047@lid': '2026-08-27-alfredo-0775'}
AGENDA = (ENTREGAS, ESTADOS)

P303 = {'pid': 'p-303', 'etapa': 'por-entregar', 'conv_id': 'wa-baileys:143306029842440@lid',
        'telefono': '56991077799', 'nombre': 'Toño', 'fecha_ficha': '2026-09-09',
        'entrega_id': None, 'externo': None}
P251 = {'pid': 'p-251', 'etapa': 'por-confirmar', 'conv_id': 'wa-baileys:55491631788168@lid',
        'telefono': '56965979654', 'nombre': 'Claudia Parada', 'fecha_ficha': '2026-09-11',
        'entrega_id': None, 'externo': None}
DOMINGA = {'pid': 'p-mig-ms7qgkig-bc7fd0', 'etapa': 'por-entregar', 'conv_id': 'wa-baileys:1@lid',
           'telefono': '56912348022', 'nombre': 'Dominga', 'fecha_ficha': '2026-07-31',
           'entrega_id': '2026-07-30-dominga-8022', 'externo': None}
DEYANIRA = {'pid': 'p-153', 'etapa': 'por-entregar', 'conv_id': 'wa-baileys:17654321098765@lid',
            'telefono': '56900000609', 'nombre': 'Deyanira', 'fecha_ficha': '2026-09-12',
            'entrega_id': None, 'externo': None}
BEAA = {'pid': 'p-mig-mru28sfr-88ed30', 'etapa': 'por-entregar', 'conv_id': 'wa-baileys:2@lid',
        'telefono': '56992021182', 'nombre': 'Beaa', 'fecha_ficha': '2026-08-01',
        'entrega_id': '2026-07-21-cliente-1182', 'externo': None}
# p-155 REAL (refutación del 10-sep): $1.585.000, 25 baños + 2 puntos de hidratación en
# Estación Central, montaje 11-09; el chat enlaza la entrega del 04-sep ya cobrada
P155 = {'pid': 'p-155', 'etapa': 'por-entregar', 'conv_id': 'wa-baileys:266391840112774@lid',
        'telefono': '56900003468', 'nombre': 'Catalina Lagos GC', 'fecha_ficha': '2026-09-11',
        'entrega_id': None, 'externo': None}
P47 = {'pid': 'p-47', 'etapa': 'por-entregar', 'conv_id': 'wa-baileys:99000000000047@lid',
       'telefono': '56900000775', 'nombre': 'Alfredo', 'fecha_ficha': '2026-08-17',
       'entrega_id': None, 'externo': None}


class Panel:
    """Un panel de mentira: responde /api/hoy, guarda los POST y puede estar caído."""

    def __init__(self, caido: bool = False, sin_ruta: bool = False, supa_roto: bool = False,
                 clave: 'str | None' = None):
        self.caido = caido
        self.sin_ruta = sin_ruta
        self.supa_roto = supa_roto
        self.clave = clave
        self.posts: list[tuple[str, dict]] = []
        self.latidos: list[dict] = []
        self.cabeceras: list[dict] = []

    def __call__(self, url, data=None, headers=None, method='GET', timeout=20):
        if url.startswith(mod.PANEL):
            if self.caido:
                raise urllib.error.URLError('connection refused')
            if url.endswith('/api/hoy'):
                return {'ok': True}
            # el candado del panel (api.ts): con clave, todo POST sin el header da 401
            self.cabeceras.append(dict(headers or {}))
            if self.clave and (headers or {}).get('x-dixdy-token') != self.clave:
                raise urllib.error.HTTPError(url, 401, 'unauthorized', {}, None)
            if url.endswith('/latido'):
                self.latidos.append(data)
                return {'ok': True}
            if url.endswith('/externo'):
                if self.sin_ruta:
                    raise urllib.error.HTTPError(url, 404, 'not found', {}, None)
                self.posts.append((url.split('/api/pedidos/')[1].split('/')[0], data))
                return {'ok': True, 'movido': data.get('a') == 'cobrado', 'etapa': data.get('a') or 'por-entregar',
                        'motivo': None}
        if '/rest/v1/entrega?' in url:
            if self.supa_roto:
                raise RuntimeError('supabase 500')
            return list(ENTREGAS.values())
        if '/rest/v1/entrega_estado?' in url:
            return list(ESTADOS.values())
        raise AssertionError(f'URL inesperada: {url}')


def correr(pedidos, panel=None, dry=False, avisar=None, estado_dir=None, ajustes_panel=None):
    """`ajustes_panel`: el contenido de panel.json del clon de mentira (None = sin archivo)."""
    panel = panel or Panel()
    avisar = avisar if avisar is not None else mock.Mock()
    tmp = Path(estado_dir) if estado_dir else Path(tempfile.mkdtemp())
    if ajustes_panel is not None:
        (tmp / 'panel.json').write_text(json.dumps(ajustes_panel))
    with mock.patch.object(mod, 'http_json', panel), \
         mock.patch.object(mod, 'leer_pedidos', lambda db=None: [dict(p) for p in pedidos]), \
         mock.patch.object(mod, 'leer_enlaces', lambda: dict(LINKS)), \
         mock.patch.object(mod, 'credenciales', lambda: ('https://supa.test', 'k')), \
         mock.patch.object(mod, 'avisar_dueno', avisar), \
         mock.patch.object(mod, 'LOG', tmp / 'log.txt'), \
         mock.patch.object(mod, 'PANEL_AJUSTES', tmp / 'panel.json'), \
         mock.patch.object(mod, 'ESTADO', tmp / 'estado.json'):
        codigo = mod.main(dry=dry)
    return codigo, panel, avisar, tmp


class Identidad(unittest.TestCase):
    def test_p303_resuelve_por_enlaces_y_pide_cobrado(self):
        _, panel, _, _ = correr([P303])
        self.assertEqual([p[0] for p in panel.posts], ['p-303'])
        cuerpo = panel.posts[0][1]
        self.assertEqual(cuerpo['ref'], '2026-09-09-tono-7799')
        self.assertEqual(cuerpo['a'], 'cobrado')
        self.assertEqual(cuerpo['estado'], 'cobrado')
        self.assertEqual(cuerpo['etiqueta'], 'Cliente ya pagó')
        self.assertEqual(cuerpo['fecha'], '2026-09-09')
        self.assertEqual(cuerpo['fuente'], 'repartidor-supabase')
        self.assertEqual(cuerpo['ts'], mod.a_ms('2026-09-09T20:30:00.5+00:00'))

    def test_p251_no_se_casa_con_sandra_por_la_cola_del_telefono(self):
        # la cola 9654 calza con 2026-09-10-sandra-9654, pero «claudia»/«parada» no están en el id
        ref, via = mod.resolver(P251, {}, set(ENTREGAS))
        self.assertIsNone(ref)
        self.assertEqual(via, 'sin vínculo')
        _, panel, _, _ = correr([P251])
        self.assertEqual(panel.posts, [])

    def test_la_cola_con_nombre_sigue_valiendo_como_red(self):
        p = dict(P303, conv_id='wa-baileys:otro@lid', entrega_id=None)
        self.assertEqual(mod.resolver(p, {}, set(ENTREGAS)), ('2026-09-09-tono-7799', 'cola+nombre'))

    def test_dominga_resuelve_por_entrega_id_aunque_haya_dos_8022(self):
        ref, via = mod.resolver(DOMINGA, {}, set(ENTREGAS))
        self.assertEqual((ref, via), ('2026-07-30-dominga-8022', 'entrega_id'))
        _, panel, _, _ = correr([DOMINGA])
        self.assertEqual(panel.posts[0][1]['ref'], '2026-07-30-dominga-8022')
        self.assertEqual(panel.posts[0][1]['a'], 'cobrado')

    def test_p155_no_se_casa_con_la_entrega_anterior_del_mismo_chat(self):
        # el link del chat apunta a la entrega del 04-sep, ya cobrada; la ficha viva es el
        # evento del 12-09 (montaje 11-09): una entrega hecha no puede ser de un servicio
        # posterior, así que queda sin vínculo, sin POST, y la fecha del 11 no se pisa
        ref, via = mod.resolver(P155, LINKS, set(ENTREGAS), AGENDA)
        self.assertIsNone(ref)
        self.assertEqual(via, mod.VIA_LINK_VIEJO)
        _, panel, _, tmp = correr([P155])
        self.assertEqual(panel.posts, [])
        self.assertEqual(panel.latidos[-1]['revisados'], 1)
        self.assertEqual(panel.latidos[-1]['cambiados'], 0)
        self.assertIn('p-155 (Catalina Lagos GC): sin vínculo: el link del chat es de una entrega anterior',
                      (tmp / 'log.txt').read_text())
        # sin la agenda (como en la firma vieja) el link se sigue leyendo tal cual
        self.assertEqual(mod.resolver(P155, LINKS, set(ENTREGAS)),
                         ('2026-09-04-catalina-lagos-gc-3468', 'enlaces.json'))

    def test_p47_la_entrega_posterior_a_la_ficha_sigue_valiendo(self):
        # dos entregas en un chat: la ficha dice 17-ago y el link guarda la del 27-ago
        # (cobrada). Es posterior a la ficha, así que el repartidor manda y se mueve
        self.assertEqual(mod.resolver(P47, LINKS, set(ENTREGAS), AGENDA),
                         ('2026-08-27-alfredo-0775', 'enlaces.json'))
        _, panel, _, _ = correr([P47])
        self.assertEqual([p[0] for p in panel.posts], ['p-47'])
        self.assertEqual(panel.posts[0][1]['a'], 'cobrado')
        self.assertEqual(panel.posts[0][1]['fecha'], '2026-08-27')

    def test_el_filtro_de_entrega_anterior_solo_aplica_a_hechas_y_con_fecha_iso(self):
        entregas = dict(ENTREGAS, **{'2026-09-04-catalina-lagos-gc-3468': dict(
            ENTREGAS['2026-09-04-catalina-lagos-gc-3468'])})
        # pendiente (sin fila de estado) con fecha anterior: no es «hecha», el link vale
        estados = {k: v for k, v in ESTADOS.items() if k != '2026-09-04-catalina-lagos-gc-3468'}
        self.assertEqual(mod.resolver(P155, LINKS, set(entregas), (entregas, estados))[1], 'enlaces.json')
        # ficha con fecha en texto libre: no se compara, el link vale
        libre = dict(P155, fecha_ficha='11 de septiembre')
        self.assertEqual(mod.resolver(libre, LINKS, set(ENTREGAS), AGENDA)[1], 'enlaces.json')
        # ficha sin fecha: idem
        sin = dict(P155, fecha_ficha=None)
        self.assertEqual(mod.resolver(sin, LINKS, set(ENTREGAS), AGENDA)[1], 'enlaces.json')
        # la cola+nombre tampoco se casa con una entrega hecha anterior a la ficha
        suelto = dict(P155, conv_id='wa-baileys:otro@lid')
        self.assertEqual(mod.resolver(suelto, {}, set(ENTREGAS)), ('2026-09-04-catalina-lagos-gc-3468', 'cola+nombre'))
        self.assertEqual(mod.resolver(suelto, {}, set(ENTREGAS), AGENDA), (None, 'sin vínculo'))


class EstadoDelRepartidor(unittest.TestCase):
    def test_referencia_sin_fila_en_entrega_estado_es_pendiente_con_la_fecha_base(self):
        est = mod.estado_de('2026-09-12-deyanira-0609', ENTREGAS, ESTADOS)
        self.assertEqual(est['estado'], 'pendiente')
        self.assertEqual(est['fecha'], '2026-09-12')
        self.assertEqual(est['etiqueta'], 'Pendiente')
        _, panel, _, _ = correr([DEYANIRA])
        self.assertEqual(panel.posts[0][1]['a'], None)
        self.assertEqual(panel.posts[0][1]['estado'], 'pendiente')

    def test_fila_eliminada_no_mueve_ni_manda_fecha(self):
        _, panel, _, _ = correr([BEAA])
        cuerpo = panel.posts[0][1]
        self.assertEqual(cuerpo['estado'], 'eliminado')
        self.assertEqual(cuerpo['etiqueta'], 'borrada en el repartidor')
        self.assertIsNone(cuerpo['a'])
        self.assertIsNone(cuerpo['fecha'])

    def test_referencia_inexistente_no_revienta(self):
        p = dict(DOMINGA, entrega_id='2026-01-01-nadie-0000')
        codigo, panel, _, _ = correr([p])
        self.assertEqual(codigo, 0)
        self.assertEqual(panel.posts, [])

    def test_fechas_de_supabase_en_ms(self):
        import datetime
        base = int(datetime.datetime(2026, 9, 9, 20, 30, tzinfo=datetime.timezone.utc).timestamp() * 1000)
        self.assertEqual(mod.a_ms('2026-09-09T20:30:00+00:00'), base)
        self.assertEqual(mod.a_ms('2026-09-09T20:30:00Z'), base)
        self.assertEqual(mod.a_ms('2026-09-09T20:30:00.12345+00:00'), base + 123)
        self.assertEqual(mod.a_ms('2026-09-09T17:30:00-03:00'), base)
        self.assertIsNone(mod.a_ms(None))
        self.assertIsNone(mod.a_ms('ayer'))


class Idempotencia(unittest.TestCase):
    def test_segunda_corrida_con_el_mismo_externo_no_postea(self):
        _, panel, _, _ = correr([P303])
        informado = panel.posts[0][1]
        ya = dict(P303, externo={k: informado[k] for k in ('fuente', 'ref', 'estado', 'etiqueta', 'fecha', 'ts')})
        _, panel2, _, _ = correr([ya])
        self.assertEqual(panel2.posts, [])
        self.assertEqual(panel2.latidos[-1]['cambiados'], 0)
        self.assertEqual(panel2.latidos[-1]['revisados'], 1)

    def test_si_cambia_algo_alla_vuelve_a_informar(self):
        _, panel, _, _ = correr([P303])
        informado = panel.posts[0][1]
        viejo = dict(informado, ts=informado['ts'] - 1000)
        ya = dict(P303, externo={k: viejo[k] for k in ('fuente', 'ref', 'estado', 'etiqueta', 'fecha', 'ts')})
        _, panel2, _, _ = correr([ya])
        self.assertEqual(len(panel2.posts), 1)

    def test_dry_no_postea_nada(self):
        _, panel, _, _ = correr([P303, DOMINGA], dry=True)
        self.assertEqual(panel.posts, [])
        self.assertEqual(panel.latidos, [])


class PanelCaido(unittest.TestCase):
    def test_escribe_el_estado_no_postea_y_avisa_una_sola_vez_al_tercer_fallo(self):
        tmp = tempfile.mkdtemp()
        avisar = mock.Mock()
        for i in range(1, 5):
            _, panel, _, _ = correr([P303], panel=Panel(caido=True), avisar=avisar, estado_dir=tmp)
            self.assertEqual(panel.posts, [])
            estado = json.loads((Path(tmp) / 'estado.json').read_text())
            self.assertEqual(estado['fallos'], i)
        self.assertEqual(avisar.call_count, 1)
        self.assertIn('45 min', avisar.call_args[0][0])
        # el panel vuelve: el contador se borra
        correr([P303], estado_dir=tmp)
        self.assertFalse((Path(tmp) / 'estado.json').exists())

    def test_panel_viejo_sin_la_ruta_no_revienta_y_late_igual(self):
        codigo, panel, _, _ = correr([P303, DOMINGA], panel=Panel(sin_ruta=True))
        self.assertEqual(codigo, 0)
        self.assertEqual(panel.posts, [])
        self.assertEqual(panel.latidos[-1]['cambiados'], 0)


class ClaveDelPanel(unittest.TestCase):
    def test_con_clave_en_panel_json_todo_post_lleva_el_header(self):
        ajustes = {'ver_chats_de_prueba': False, 'host': '127.0.0.1', 'token_escritura': 'clave-larga-del-dueno'}
        codigo, panel, _, _ = correr([P303], panel=Panel(clave='clave-larga-del-dueno'), ajustes_panel=ajustes)
        self.assertEqual(codigo, 0)
        self.assertEqual([p[0] for p in panel.posts], ['p-303'])
        self.assertTrue(panel.latidos and panel.latidos[-1]['ok'])
        # el POST /externo y el latido: los dos con la clave
        self.assertEqual(len(panel.cabeceras), 2)
        for cab in panel.cabeceras:
            self.assertEqual(cab.get('x-dixdy-token'), 'clave-larga-del-dueno')

    def test_sin_clave_null_no_manda_header(self):
        ajustes = {'ver_chats_de_prueba': False, 'host': '127.0.0.1', 'token_escritura': None}
        _, panel, _, _ = correr([P303], ajustes_panel=ajustes)
        self.assertEqual(len(panel.posts), 1)
        for cab in panel.cabeceras:
            self.assertNotIn('x-dixdy-token', cab)
        # sin archivo de ajustes tampoco
        _, panel2, _, _ = correr([P303])
        self.assertEqual(len(panel2.posts), 1)

    def test_con_clave_alla_y_sin_clave_aca_la_corrida_cae_y_el_latido_lo_dice(self):
        # el caso que temía el refutador: el panel con clave y el sensor sin ella; ya no
        # pasa por el ajuste, pero si pasara el latido no puede quedar mudo para siempre
        codigo, panel, _, _ = correr([P303], panel=Panel(clave='otra'))
        self.assertEqual(codigo, 1)
        self.assertEqual(panel.posts, [])


class Latido(unittest.TestCase):
    def test_latido_final_con_revisados_y_cambiados(self):
        ya = dict(DOMINGA, externo={'fuente': 'repartidor-supabase', 'ref': '2026-07-30-dominga-8022',
                                    'estado': 'cobrado', 'etiqueta': 'Cliente ya pagó', 'fecha': '2026-07-31',
                                    'ts': mod.a_ms('2026-07-31T15:00:00+00:00')})
        _, panel, _, _ = correr([P303, P251, ya])
        latido = panel.latidos[-1]
        self.assertTrue(latido['ok'])
        self.assertEqual(latido['revisados'], 3)
        self.assertEqual(latido['cambiados'], 1)
        self.assertIsNone(latido['detalle'])

    def test_latido_con_ok_false_si_la_corrida_se_cae(self):
        codigo, panel, _, _ = correr([P303], panel=Panel(supa_roto=True))
        self.assertEqual(codigo, 1)
        self.assertEqual(panel.latidos[-1]['ok'], False)
        self.assertIn('supabase 500', panel.latidos[-1]['detalle'])


if __name__ == '__main__':
    unittest.main(verbosity=1)
