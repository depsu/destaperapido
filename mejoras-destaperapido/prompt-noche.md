# Prompt para dejarlo trabajando de noche

**Cómo se lanza** (en una terminal que puedas dejar abierta):

```bash
claude982 --permission-mode bypassPermissions      # o claude98, la cuenta con cupo
```

Dentro del chat: `/model fable`, `cd ~/SaSS/DIXDY/clientes/destaperapido` si hace falta, y
pegar el prompt de abajo tal cual.

`bypassPermissions` es lo que evita que se quede pegado a las 3 AM esperando un permiso.
La red de seguridad no es el permiso: es que **cada pieza va en su propio commit con los
tests verdes**, así que en la mañana cualquier cosa se revierte sola.

**Una sesión de noche, no dos.** Si dejas las dos cuentas trabajando el mismo repo se van
a pisar en los commits.

---

## El prompt (copiar de aquí para abajo)

/loop Trabajas solo toda la noche en dixdybot. Nadie te va a contestar hasta la mañana: si
algo necesita una decisión de Alejandro, NO preguntes — anótalo en el diario y sigue con lo
siguiente.

ARRANQUE (una sola vez): corre `bash mejoras-destaperapido/briefing.sh --tests` y lee
`mejoras-destaperapido/RETOMAR-AQUI.md`. Tu carril es BACKEND; el plan está en
`mejoras-destaperapido/auditoria-backend-2026-07-30.md`.

ORDEN DE TRABAJO — una cosa por vuelta, en este orden, sin inventar otras:

1. **E1 · Historial + volver atrás** (§5 de la auditoría): tabla nueva `puntos_restauracion`,
   hook `alGuardar` en `core/config.ts`, eventos `ajuste.cambiado` / `punto.restaurado` al
   ledger, API, y vista «Cambios» con botón *volver a este punto*. Cuidado con la trampa ya
   documentada: la foto tiene que llevar el ajuste Y las filas de `caminos_publicados`
   juntos, o el camino restaurado queda mudo. Antes de restaurar, llama a `respaldar()`.
2. **💲 Precios P1** (§12): el tarifario del cotizador como vista propia en el menú, con
   filas legibles y edición en línea — no un formulario de campos técnicos.
3. **💲 Precios P2** (§12): subir Excel/PDF/foto → la IA propone la tabla → tarjeta de
   aprobación lado a lado. Nada se escribe sin que Alejandro acepte: un precio mal leído es
   plata. Reusa la ingesta y el patrón de manos que ya existen.
4. **E2 · Un solo candado** (§4): un linter de caminos usado por las TRES vías (panel, duda,
   orquestador), cerrar la puerta trasera de `PUT /api/modulos/caminos`, y `.refine` a
   `ConfigEmbudo` (que `etapa_inicial` exista, transiciones válidas, ids únicos).
5. Si sobra noche: §8 (enchufes sin cable), de menor a mayor riesgo, empezando por lo que se
   VE en el panel. Regla: lo que se ve funciona; lo que no funciona, no se ve.

LEY DE CADA PIEZA:
- Pasos chicos. Cada pieza terminada = su propio commit, con mensaje en español que explique
  el PORQUÉ (no el qué).
- `pnpm exec tsc --noEmit`, `pnpm exec vitest run` y los 6 `node panel/pwa/_probar-*.cjs` en
  VERDE o no hay commit. Todo lo que agregues lleva su test.
- Si algo queda rojo y no lo arreglas en 3 intentos: revierte esa pieza, anótalo en el diario
  y pasa a la siguiente. No te quedes toda la noche en lo mismo.
- Nunca termines una vuelta con el repo sucio: o commiteas, o reviertes.
- Reinicia los dos paneles SOLO con el candado verde
  (`launchctl kickstart -k "gui/$(id -u)/com.dixdy.dixdybot-panel"` y `…-panel-dixdy`) y
  comprueba con `curl` que los dos responden antes de seguir.

PROHIBIDO, sin excepciones:
- Escribirle a un cliente real. Para probar, SOLO el canal `sim:` del simulador.
- Responder o decidir las dudas abiertas (`prjst`, `baffe`, `ockbe`): son decisiones de plata
  de Alejandro.
- Tocar `~/SaSS/destaperapido/whatsapp-bot/` (el bot que vende hoy).
- Tocar lo del otro carril (`auditoria-ux-29jul/`, `onboarding-dueno-nuevo.md`, el robot guía
  y las vistas de onboarding): hay otra sesión trabajando ahí.
- Agregar columnas a tablas existentes de `src/db/esquema.sql` (tablas NUEVAS sí).
- `git push`, borrar datos de cualquier instancia, comprar o contratar nada, tocar la API key.
- Cambiar ajustes reales de destaperapido (precios, tarifario, horarios).

DIARIO — es lo primero que Alejandro va a leer en la mañana. Al terminar CADA pieza actualiza
`mejoras-destaperapido/diario-noche.md`, en simple y sin tecnicismos: qué quedó funcionando y
cómo lo comprobaste, qué quedó a medias y por qué, qué necesita su decisión, y en qué commit
quedó cada cosa. Que se lea como el parte de un colega que trabajó de noche, no como un log.

Registra lo hecho con `python3 ~/SaSS/DIXDY/scripts/actividad.py`. Cuando termines el orden
completo, para y cierra el diario con un resumen de una página.
