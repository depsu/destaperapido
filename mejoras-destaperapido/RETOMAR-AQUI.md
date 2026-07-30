# RETOMAR AQUÍ — traspaso al 30-jul-2026

Documento de **arranque en frío**: si abres un chat nuevo de Claude Code (misma cuenta u
otra) y no sabes nada de lo anterior, lee esto y ya puedes trabajar. Es la puerta de
entrada; el mapa largo del proyecto sigue en `DIXDYBOT-ESTADO.md`.

---

## 1 · Qué pegar en el chat nuevo

> Trabajo en dixdybot (bot de WhatsApp genérico multi-rubro, primer cliente
> destaperapido). Para arrancar:
> 1. corre `bash mejoras-destaperapido/briefing.sh --tests` y mírame el resultado;
> 2. lee `mejoras-destaperapido/RETOMAR-AQUI.md` completo;
> 3. según el carril que te diga abajo, lee su plan (§4).
> Explícame en simple, sin tecnicismos: yo decido plata y diseño.
> Cuando tengas claro dónde quedamos, propón el siguiente paso y ejecútalo.
> **Mi carril esta vez: <experiencia / backend>.**

Con eso basta. Los `CLAUDE.md` (global, maestro y clon) se cargan solos, y el briefing
pone en pantalla el estado VIVO (cuenta, paneles, dudas esperando, últimos commits).

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
- **Hay DOS CARRILES trabajando en paralelo sobre el mismo molde** (cada uno en su
  cuenta de Claude Code, commiteando al mismo repo, sin pisarse hasta ahora):
  · **Backend / robustez** — auditoría E0-E5 + Precios (`auditoria-backend-2026-07-30.md`).
  · **Experiencia del dueño nuevo** — auditoría UX con navegador y onboarding en 3 fases
    (`auditoria-ux-29jul/informe.md` + `onboarding-dueno-nuevo.md`). **Fase A cerrada el
    30-jul:** el ROBOT GUÍA flotante (burbuja 🤖 en todas las vistas, chat con su memoria
    en la tabla `guia_mensajes`, mano `llevar_a` que navega y destaca la vista, globito de
    bienvenida por vista) + limpieza para no técnicos (nombres humanos en Hoy, «Examen
    para atender» en vez de gate, menú «Qué hace tu bot», Módulos sin duplicar canales,
    Diseño oculto por defecto, banner honesto del simulador, fotos sin 404, sello al pie).

## 4 · Qué sigue (por carril — pregúntale a Alejandro cuál toca)

### Carril EXPERIENCIA (el del robot guía) — plan en `onboarding-dueno-nuevo.md`

1. **Fase B · Celular de verdad** (lo más urgente de este carril, medido con navegador a
   390px): el menú son 8 iconos SIN texto → barra inferior tipo app con etiquetas; **la
   ficha del chat en móvil no tiene la cara Agente**, así que desde el teléfono no se
   puede hablar con el agente ni resolver la duda (grave: el celular es donde más se
   ayuda al bot); el hero/estreno de Agentes queda invisible detrás de la lista;
   verificar el pegado al fondo del hilo al abrir un chat.
2. **Fase C · La conversación que personaliza dixdy**: «cuéntame de tu negocio» →
   el robot escribe los ajustes (nombre del negocio, primer agente, tono) sin que el
   dueño toque nada técnico; las 3 misiones (contrata → simula → conecta) tomando Hoy
   cuando el negocio está vacío; celebraciones al completar; novedades contadas por el
   personaje (**portar** el sistema «novedades ✨» del `panel-cliente/` del maestro, no
   reinventarlo); texto de las 2 conexiones (rápida vs Meta) y primera prueba guiada del
   simulador. El robot de la Fase A es el MISMO personaje que conduce todo esto.

### Carril BACKEND — plan en `auditoria-backend-2026-07-30.md`

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

**Un solo comando** (parado en el clon, `~/SaSS/DIXDY/clientes/destaperapido`):

```bash
bash mejoras-destaperapido/briefing.sh --tests
```

Imprime: con qué cuenta corres · los dos paneles con sus números · las preguntas que
esperan al dueño · los últimos commits · si otra sesión dejó cambios sin commitear · y
el candado (tsc + vitest + los 6 verificadores del front). Sin `--tests` es instantáneo.

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

### Pasarle a la otra cuenta la conversación ENTERA (no un resumen)

Las conversaciones son archivos sueltos por cuenta
(`<config>/projects/<carpeta-del-proyecto>/<id>.jsonl`), así que se pueden mudar:

```bash
bash mejoras-destaperapido/pasar-sesion.sh          # la última de esta cuenta
bash mejoras-destaperapido/pasar-sesion.sh <id>     # una en particular
# imprime el comando listo, del estilo:
#   claude982 --resume <id> --fork-session
```

`--fork-session` le da un id nuevo: **la original queda intacta** y las dos siguen por su
lado sin pisarse. Copia lo que hay hasta ese segundo; si la conversación de origen sigue
viva, vuelve a correrlo al terminar.

**Cuál usar:** el fork para seguir la MISMA tarea a medio hacer (despierta sabiendo todo lo
hablado, pero llega con el contexto medio gastado); el briefing de §6 para empezar un
trabajo nuevo (arranca limpio y ve el estado real, no el recuerdo). No compiten.

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

## 8 · Dejarlo trabajando de noche (y que no choque con la otra sesión)

**Antes de dormir, tres cosas:**

1. **Un carril por sesión.** Los dos carriles escriben en el MISMO molde
   (`~/SaSS/DIXDY/dixdybot`). Dos sesiones editando a la vez terminan pisándose el mismo
   archivo. Si de verdad quieres las dos, la segunda trabaja en un árbol aparte:
   `git -C ~/SaSS/DIXDY/dixdybot worktree add /tmp/dixdybot-noche -b noche` y ahí no se
   pisan (después se junta con un merge). Si va a ser una sola, díselo explícito: *«esta
   noche solo el carril de experiencia, no toques el backend»*.
2. **Permisos.** Una sesión que se queda esperando un «¿permites?» duerme igual que tú y
   no avanza nada. Deja la sesión en un modo que no la detenga (⇧Tab elige el modo de
   permisos, «aceptar ediciones»). El Guardián sigue puesto: pregunta solo por plata y
   por borrar cosas en vivo, así que lo importante sigue protegido.
3. **Que termine cada vuelta con el candado verde y un commit.** Es la única forma de que
   al despertar puedas leer qué hizo. Pídeselo en el prompt: *«cada tarea termina con tsc
   + vitest + verificadores en verde y su commit; si algo queda rojo, lo dejas revertido
   y me lo cuentas»*.

**Para que trabaje solo por tandas** existe `/loop` (repite un pedido cada cierto rato):

```
/loop 45m Sigue la Fase B del carril EXPERIENCIA (mejoras-destaperapido/RETOMAR-AQUI.md §4).
Una mejora por vuelta, con el candado verde y su commit. Verifica en el navegador a 390px
antes de decir que quedó lista. Registra con scripts/actividad.py.
```

Y al despertar, para saber qué pasó sin leer todo el chat:

```bash
cd ~/SaSS/DIXDY/clientes/destaperapido && bash mejoras-destaperapido/briefing.sh --tests
git -C ~/SaSS/DIXDY/dixdybot log --oneline --since=midnight
```

> Ojo con el gasto: una sesión suelta toda la noche consume harto. Si el objetivo es
> avanzar 2-3 mejoras concretas, sale más barato dejarle la lista corta y clara que
> pedirle «mejora todo lo que puedas».
