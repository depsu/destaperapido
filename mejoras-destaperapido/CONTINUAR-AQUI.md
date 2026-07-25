# CONTINUAR AQUÍ — arranque en frío del backend de dixdybot

**Para qué es este archivo:** que perder la conversación no cueste nada. Si el chat se
resumió, se cortó, o hay que abrir uno nuevo, esto es lo único que hay que leer para seguir
exactamente donde se quedó. **Se actualiza al cerrar cada pieza**, no al final.

**Última actualización:** 25-jul-2026

---

## El prompt para un chat nuevo

> Copiar tal cual en un chat nuevo de Claude Code, parado en
> `~/SaSS/DIXDY/clientes/destaperapido`:

```
Sigo el backend de dixdybot. Lee en este orden y no me preguntes nada antes de leerlos:

1. mejoras-destaperapido/CONTINUAR-AQUI.md   ← empieza por acá, dice qué toca ahora
2. mejoras-destaperapido/REPARTO-SESIONES.md ← qué pieza está libre y qué archivo pisa cada una
3. mejoras-destaperapido/DIXDYBOT-ESTADO.md  ← el estado del proyecto entero

Reglas que no se negocian:
- El bot vivo en ~/SaSS/destaperapido/whatsapp-bot/ es SOLO LECTURA. Es lo que vende hoy.
  Nada de kill, restart, npm, launchctl ni escrituras ahí.
- El molde ~/SaSS/DIXDY/dixdybot/ NO lleva datos de cliente. Credenciales jamás en JSON de
  ajustes: van al .env.local del clon.
- Hay OTRA sesión editando dixdybot/panel/pwa/* (el front). No toques esos archivos.
- Toda función nueva nace como MÓDULO: manifest + configSchema Zod + configDefault +
  aportes, administrable desde el panel, nunca cableada al rubro.
- Sin `pnpm exec tsc --noEmit` y `pnpm exec vitest run` verdes no hay commit.
- Guardián v4: solo se le pregunta a Alejandro por SU PLATA o por gestión externa suya.
  Todo lo demás corre solo.
- Explicarle a Alejandro en simple, sin tecnicismos. Él decide plata y diseño.

Toma la pieza que CONTINUAR-AQUI.md marque como siguiente y avanza.
```

---

## Sobre el contexto: ya está resuelto, no hay que hacer nada

**El auto-compact YA está encendido**, y además afinado. Verificado el 25-jul contra el
binario instalado (`~/.local/share/claude/versions/2.1.220`), no contra documentación:

- `Hc("autoCompactEnabled", !0)` → el valor por defecto es **`true`**. Viene activado de
  fábrica; por eso la clave no aparece en `~/.claude/settings.json`.
- `~/SaSS/DIXDY/.claude/settings.json` ya trae
  `env: { "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "80" }` → **se resume solo al 80%** del
  contexto, sin esperar al límite.
- Nada lo está apagando: `DISABLE_COMPACT`, `DISABLE_AUTO_COMPACT` y
  `CLAUDE_CODE_AUTO_COMPACT` están todas vacías.
- Se ve y se cambia en `/config` → "Auto-compact". Para mirar cuánto queda: `/context`.

**O sea: `/compact` a mano no hace falta.** Se puede seguir usando para cortar donde uno
quiere, pero el automático ya cubre el caso de quedarse sin espacio.

**Lo que de verdad protege el trabajo no es el compact, es esto:** todo lo importante se
escribe en el repo (este archivo, `REPARTO-SESIONES.md`, `DIXDYBOT-ESTADO.md`, los mensajes
de commit), nunca solo en la conversación. Un resumen pierde detalle; un archivo no. La
regla práctica al trabajar: **leer pesado con agentes aparte** (así el volcado de archivos
no entra al contexto principal) y **dejar escrito el resultado**, no la lectura.

---

## Dónde está cada cosa

| Qué | Dónde |
|---|---|
| El molde (lo que se construye) | `~/SaSS/DIXDY/dixdybot/` |
| La instancia con datos reales | `~/SaSS/destaperapido/dixdybot-data/` |
| El bot vivo que vende (SOLO LECTURA) | `~/SaSS/destaperapido/whatsapp-bot/` |
| Panel del molde corriendo | `127.0.0.1:8793` |
| Docs del proyecto | `~/SaSS/DIXDY/clientes/destaperapido/mejoras-destaperapido/` |

Ojo: `dixdybot/` vive **dentro** del repo git del maestro DIXDY, no es un repo aparte. Los
commits van al maestro.

---

## Lo hecho hasta ahora (S5)

| Pieza | Commit | Qué dejó |
|---|---|---|
| P1+P2+P4 adaptador `wa-baileys` + `cli/vincular` | `201b208` | el molde ya puede hablar por el número propio; 28 cicatrices del vivo trasplantadas |
| P5 huecos del migrador | `86615eb` | las 8 preguntas pendientes del bot viejo cruzan el corte; huérfanos clasificados |
| P3 compuerta `gating` | `6de0907` | el bot sabe cuándo callarse; nace la tabla `pausas`; topes desde la base |
| PS la salida del panel | 25-jul | enviar al cliente, contestar la Duda, entrada de prueba: el panel deja de ser un espejo |

**765 tests verdes, tsc limpio.**

---

## Qué toca ahora

> **Esta sección es la que hay que actualizar al cerrar cada pieza.**

**Antes de tomar cualquier pieza, lee en `REPARTO-SESIONES.md` la sección "Lo que el
reconocimiento del 25-jul cambió".** Trae una regla que evita romper la base en producción
(🚨 nunca agregar una columna a `esquema.sql`: pasa tsc, pasa los tests y NO llega a la base
viva), corrige el orden de P12 y desarma dos trampas del cutover.

Candidatas, por valor:

1. **El pushName perdido** — todo chat NUEVO se va a ver como un número. Ojo: pide agregarle
   un campo a `MensajeEntrante` (`src/schemas/canal.ts`), del que depende P14.
2. **P7-a: bautizo y etiquetas** usando SOLO `titulo` y `etiquetas`, que ya existen en la
   base viva → cero migración, cero riesgo. Sin tocar la columna `ficha`.
3. **P12 reducida:** "visto por el dueño" como tabla lateral (patrón `pausas`). G5 ya está
   cerrado por P3; G8 sale de la lista hasta decidir instantáneo-vs-candado.
4. **P6 recortado:** la sección del corte del MANUAL + el rollback de dos comandos.

<details><summary>Lo que se estaba mapeando el 25-jul (ya cerrado)</summary>

Reconocimiento de **P12**, **P6**, **P7** y el **contrato front↔backend** para la
conexión de la noche. Sus conclusiones están arriba y en `REPARTO-SESIONES.md`.
</details>

---

## Lo que sigue pendiente de Alejandro (no lo puede hacer la IA)

1. **Aprobar en lote los 30 caminos** (panel → Caminos → borradores; informe en
   `caminos-veredicto.md`).
2. **Decidir si se carga el servicio de sombra diaria** — consume cuota de suscripción.
3. **La primera conexión real a WhatsApp.** Nunca se ha vinculado un número de verdad: todo
   lo de canal está probado contra un WhatsApp simulado. **Conviene hacerlo con un número
   secundario, no con el que vende.**
4. **Transcripción de audio** — es plata nueva, hoy el bot pide que le escriban.
5. Fechas duras que no se mueven: **30-sep** decisión Coexistence · **1-oct** Meta cobra
   todos los service/utility · **1-dic** Ley 21.719 (ARCO+P en el panel).
