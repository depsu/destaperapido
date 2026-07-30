# RETOMAR AQUÍ — traspaso al 30-jul-2026

Documento de **arranque en frío**: si abres un chat nuevo de Claude Code (misma cuenta u
otra) y no sabes nada de lo anterior, lee esto y ya puedes trabajar. Es la puerta de
entrada; el mapa largo del proyecto sigue en `DIXDYBOT-ESTADO.md`.

---

## 1 · Qué pegar en el chat nuevo

> Trabajo en dixdybot (bot de WhatsApp genérico multi-rubro, primer cliente
> destaperapido). Lee, en este orden:
> `~/SaSS/DIXDY/clientes/destaperapido/mejoras-destaperapido/RETOMAR-AQUI.md`,
> después `auditoria-backend-2026-07-30.md` del mismo directorio.
> Explícame en simple, sin tecnicismos: yo decido plata y diseño.
> Cuando tengas claro dónde quedamos, propón el siguiente paso y ejecútalo.

Con eso basta. Los `CLAUDE.md` (global, maestro y clon) se cargan solos.

## 2 · Dónde está todo

| Cosa | Ruta |
|---|---|
| Molde (código, ES producción) | `~/SaSS/DIXDY/dixdybot/` |
| Datos del cliente destaperapido | `~/SaSS/destaperapido/dixdybot-data/` · panel **8793** · launchd `com.dixdy.dixdybot-panel` |
| Datos de la instancia DIXDY (panel público) | `~/SaSS/dixdy/dixdybot-data/` = **la misma carpeta** que `~/SaSS/DIXDY/dixdybot-data` (el disco no distingue mayúsculas) · panel **8794** · launchd `com.dixdy.dixdybot-panel-dixdy` · https://panel.dixdy.cl |
| Auditoría + plan por etapas | `mejoras-destaperapido/auditoria-backend-2026-07-30.md` |
| Mapa largo del proyecto | `mejoras-destaperapido/DIXDYBOT-ESTADO.md` |
| Bot VIEJO que aún vende | `~/SaSS/destaperapido/whatsapp-bot/` — **solo lectura, no tocar** |

## 3 · Estado al 30-jul

- **977 tests verdes**, `tsc` limpio, 6 verificadores del front OK.
- **Etapa 0 (Cinturón) CERRADA y en vivo** en las dos instancias. Qué cerró: §11 de la
  auditoría (respaldo que cubre dixdybot, dudas que vencen sin cron, prueba dorada
  persistida, aviso sin relay falso, y 6 filtros para que el cerebro no envenene el estado).
- Ambos paneles sanos. En destaperapido hay 3 dudas vivas: `prjst` (expirada, la nueva
  conducta), `ockbe` y `baffe` (en `evaluando`, esperando que el dueño decida).

## 4 · Qué sigue (en orden)

1. **E1 · Historial + volver atrás** — hoy un cambio de ajuste PISA el anterior sin dejar
   rastro (ni qué, ni cuándo, ni si fue el dueño o la IA). Diseño ya hecho en §5 de la
   auditoría: tabla nueva `puntos_restauracion` + hook `alGuardar` en `core/config.ts` +
   eventos al ledger + vista «Cambios» con botón *volver a este punto*.
   **Trampa documentada:** los caminos viven en DOS almacenes y `caminos_publicados` le gana
   al ajuste — la foto debe llevar los dos juntos o el camino restaurado queda mudo.
2. **💲 Precios** (idea de Alejandro, diseño en §12): sección propia en el menú; subir
   Excel/PDF/foto → propuesta con tarjeta de aprobación; variaciones por fecha como capa
   aparte; recomendar marcando qué es dato y qué es criterio.
3. **E2 un solo candado** → **E3 IA en Caminos** → **E4 agentes de verdad** → **E5 tableros
   por flujo**. Detalle en §10.

### Pendientes que necesitan a Alejandro
- **Plata:** `ANTHROPIC_API_KEY` como respaldo del cerebro (2 de 2 veces que falló el
  principal, el respaldo no existía y el cliente recibió una enlatada).
- **5 minutos suyos:** publicar el panel de destaperapido (8793) en el túnel, como
  `panel.dixdy.cl` — sin eso los avisos push no llegan a ningún teléfono (hoy: 0 suscritos).

## 5 · Leyes que rigen acá (no negociables)

- `pnpm exec tsc --noEmit` y `pnpm exec vitest run` **en verde o no hay commit**; además
  `node panel/pwa/_probar-*.cjs` si se tocó el front.
- **NO agregar columnas a tablas existentes** en `src/db/esquema.sql` — SQLite las ignora en
  silencio. Tablas NUEVAS y `CREATE INDEX IF NOT EXISTS`, sí.
- **NO tocar** `~/SaSS/destaperapido/whatsapp-bot/` (es el bot que vende hoy).
- Cada cambio al molde es un **cambio en vivo** a los dos paneles → reiniciar ambos:
  `launchctl kickstart -k "gui/$(id -u)/com.dixdy.dixdybot-panel"` y
  `…-panel-dixdy`.
- Doctrina DIXDY: nada de crons/loops/workers nuevos sin revisar los motores que ya existen;
  registrar lo hecho con `scripts/actividad.py`; verificar sin navegador primero.

## 6 · Comprobación rápida de que todo está vivo

```bash
for p in 8793 8794; do curl -s http://127.0.0.1:$p/api/salud | head -c 120; echo; done
cd ~/SaSS/DIXDY/dixdybot && pnpm exec tsc --noEmit && pnpm exec vitest run
```

## 7 · Las dos cuentas de Claude Code en este Mac

Ya está montado en `~/.zshrc` — **no hay que configurar nada, solo usar el alias**:

| Comando | Cuenta | Carpeta de config |
|---|---|---|
| `claude982` | rivera.ale982@gmail.com | `~/.claude` |
| `claude98` | rivera.ale98@gmail.com | `~/.claude-ale98` |

**El truco es el llavero del Mac:** las sesiones NO viven en un archivo, viven en el
Keychain, con una entrada por cuenta (`Claude Code-credentials-<hash de la carpeta>`). Por
eso las dos quedan recordadas al mismo tiempo y cambiar de cuenta **no pide login de nuevo**:
abres otra terminal, escribes el otro alias y ya estás dentro con la otra cuenta.

Cada carpeta lleva su propia memoria y su propio historial de chats, así que **la memoria del
proyecto NO se comparte entre cuentas**. Por eso existe este documento: es lo que hace que la
otra cuenta arranque sabiendo lo mismo. Si quieres compartir la memoria de verdad:

```bash
# desde la cuenta que NO tiene la memoria (una sola vez)
ln -s ~/.claude-ale98/projects/-Users-alejandroriveracarrasco-SaSS-DIXDY-clientes-destaperapido/memory \
      ~/.claude/projects/-Users-alejandroriveracarrasco-SaSS-DIXDY-clientes-destaperapido/memory
```

Comprobar con qué cuenta estás corriendo, sin adivinar:

```bash
echo "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
python3 -c "import json,os;p=os.environ.get('CLAUDE_CONFIG_DIR',os.path.expanduser('~/.claude'))+'/.claude.json';\
print(json.load(open(p)).get('oauthAccount',{}).get('emailAddress'))" 2>/dev/null \
 || python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.claude.json'))).get('oauthAccount',{}).get('emailAddress'))"
```

Y el modelo se elige dentro del chat con `/model fable` (o `/model opus`). El `/model` se
guarda por cuenta, así que en la cuenta nueva hay que elegirlo una vez.

> Contexto: son **dos suscripciones pagadas por separado**, ambas de Alejandro, y cada
> cuenta corre con su propio límite. Alternar entre ellas cuando una se agota es usar lo
> que se pagó, no esquivar nada.
