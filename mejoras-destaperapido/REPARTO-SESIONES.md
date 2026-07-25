# Reparto de sesiones — cómo avanzar dixdybot en varios chats sin pisarse

**Creado:** 25-jul-2026 · **Para:** cualquier sesión de Claude Code que vaya a tocar el molde
`SaSS/DIXDY/dixdybot/`. Léelo ANTES de empezar, junto con `DIXDYBOT-ESTADO.md`.

## La regla de oro

El reparto **NO es por tema** ("tú los cobros, yo los seguimientos"). Es **por archivos**.
Dos sesiones que editan el mismo archivo se pisan: la segunda en guardar borra a la primera
y ninguna se entera. Antes de abrir una sesión nueva, mira la tabla de archivos puente y
confirma que nadie más los tiene tomados.

## Archivos puente (los que casi todo toca)

| Archivo | Qué es | Piezas que lo tocan |
|---|---|---|
| `src/index.ts` | cableado del arranque | P1, P3, P7, P10 |
| `src/core/escritor.ts` | el único escritor | P7, P8, P9, P12, P16 |
| `src/db/esquema.sql` | las 6 tablas núcleo | P7, P11, P12 |
| `src/modulos/indice.ts` | registro de módulos | P1, P7, P8, P9, P14 |
| `src/panel/api.ts` | API del panel | P8, P10, P11, P15, P16 |
| `src/panel/consultas-registradas.ts` | registro de métricas | P8, P9 |
| `src/canales/factory.ts` | switch de canales | P1, P14 |
| `tests/arranque.test.ts` | integración | casi todas |

**Ventaja del diseño:** las migraciones NO viven en un archivo común — cada módulo lleva las
suyas en su `modulo.ts` y se enganchan en `indice.ts`. Dos piezas que crean **tablas nuevas**
no chocan. Solo chocan si tocan las 6 tablas núcleo (`esquema.sql`).

## Las piezas pendientes

| # | Pieza | Carpeta propia | Archivos puente que toca |
|---|---|---|---|
| ~~P1~~ | ~~adaptador `wa-baileys`~~ ✅ | `src/canales/wa-baileys/` | factory, indice |
| ~~P2~~ | ~~trasplante legado del emisor (Bad MAC, outbox)~~ ✅ | ídem P1 | — (va con P1) |
| ~~P4~~ | ~~`cli/vincular.ts`~~ ✅ | `cli/` | — |
| ~~P5~~ | ~~huecos del migrador (dudas del vivo)~~ ✅ | `src/modulos/migrador/` | — |
| P6 | MANUAL.md + cutover launchd | raíz | — (va al final) |
| ~~P3~~ | ~~compuerta `gating`~~ ✅ | `src/core/` + `src/modulos/gating/` | index.ts, api, consultas-reg |
| P7 | módulo `ficha` (bautizo + etiquetas, G3+G4) | `src/modulos/ficha/` | esquema, escritor, indice, index |
| P8 | módulo `seguimiento` (G6) | `src/modulos/seguimiento/` | indice, consultas-reg, api, escritor |
| P9 | módulo `cobros` (separar de embudo) | `src/modulos/cobros/` | escritor, indice, consultas-reg |
| P10 | `conexiones/` con permiso (G21) | `src/conexiones/` | **index, llm, orquestador, api** |
| P11 | buscador FTS5 del panel (G25) | `src/panel/buscar.ts` | **esquema**, api, consultas |
| P12 | deltas G2+G5+G8 (no leído, silencio, enseñanzas) | — | **esquema, escritor, api, ledger** |
| P13 | completar `wa-cloud` (media, plantillas, ventana) | `src/canales/wa-cloud/` | **ninguno** ✅ |
| P14 | Instagram DM + CTWA | `src/canales/ig/` | factory, indice (depende de P13) |
| P15 | onboarding de negocio nuevo | `src/panel/` | api (depende de P7) |
| P16 | Ley 21.719 ARCO+P (**dura: 1-dic**) | `src/panel/` | api, escritor |

## Tandas seguras

- **Tanda A (ahora):** `P1+P2+P4` en UNA sesión (misma carpeta, no se pueden separar) ‖
  `P13` ‖ `P5`. Cero colisiones entre las tres.
- **Sacar sola y primero:** `P12`. Bloquea `esquema.sql` **y** `escritor.ts` a la vez;
  después de ella, P7/P8/P9/P11 quedan mucho más libres.
- **Nunca juntas:** P8 con P9 (chocan en `escritor.ts` y `consultas-registradas.ts`);
  P7 con P10 (chocan en `src/index.ts`); P11 con P12 (chocan en `esquema.sql`).
- **Paralelo permanente:** `P13` no toca ningún archivo puente — corre junto a lo que sea.

## Protocolo de cada sesión

**Al abrir:**
1. Leer `DIXDYBOT-ESTADO.md` y este archivo.
2. Anunciar en la tabla de abajo qué pieza toma (editar este archivo y commitear ANTES de
   empezar, para que las otras sesiones lo vean).
3. `git pull` si hay otra sesión activa.

**Al cerrar:**
1. `pnpm exec tsc --noEmit` y `pnpm exec vitest run` verdes, o no hay commit.
2. Commit con la pieza en el mensaje.
3. Actualizar `DIXDYBOT-ESTADO.md` (qué quedó hecho, qué falta).
4. Liberar la pieza en la tabla de abajo.
5. `python3 /Users/alejandroriveracarrasco/SaSS/DIXDY/scripts/actividad.py`.

**Prohibido siempre:** tocar el bot vivo en `~/SaSS/destaperapido/whatsapp-bot/` (es lo que
vende hoy, solo lectura) y meter datos de cliente en el molde.

## Tablero de piezas tomadas

| Pieza | Sesión | Desde | Estado |
|---|---|---|---|
| **P1+P2+P4** (adaptador wa-baileys, legado del emisor, `cli/vincular.ts`) | sesión del 25-jul | 25-jul | ✅ **hecha** (commit `201b208`) |
| **P5** (huecos del migrador: dudas del vivo + clases de huérfanos) | sesión del 25-jul | 25-jul | ✅ **hecha** (commit `86615eb`) |
| **P3** (compuerta `gating`) | sesión del 25-jul | 25-jul | ✅ **hecha** (commit `6de0907`) |
| resto | — | — | libre |

> **P1** liberó `src/canales/factory.ts` y `src/modulos/indice.ts`. **Ojo para P14
> (Instagram):** el `switch` de `factory.ts` ya tiene su `case 'wa-baileys'` como molde a
> copiar, y `OpcionesFabrica` ganó `rutaDatos` (lo usan los canales que guardan sesión).
>
> **P3** liberó `src/index.ts`, `src/panel/api.ts` y `src/panel/consultas-registradas.ts`.
> Lo que dejó cambiado y hay que saber antes de tocar esos archivos:
> - **El pipeline ya NO es lineal.** `atenderMensaje` persiste, pasa por la compuerta y
>   **agenda**; el turno corre después, dentro de `gating.agendar(...)` y serializado por
>   chat con `colaDeTurnos`. Cualquier pieza que quiera meterse "después del cerebro" va
>   DENTRO de ese callback, no debajo de `atenderMensaje`.
> - **`MensajeEntrante` ganó `propio`** (`src/schemas/canal.ts`): el mensaje lo escribió el
>   dueño desde la cuenta del negocio. Todo canal nuevo (P14) debe marcarlo — y descartar
>   siempre el eco de sus propios envíos, que es otra cosa.
> - **`Canal.contactoEscribiendo?()`** es opcional: si el canal no expone presencia, la
>   compuerta no espera. No lo inventes.
> - **`ContextoConsulta` ganó `ahora`** (epoch ms) para métricas de ESTADO, no de día.
> - **Nace la tabla `pausas`** (migración del módulo gating). Es la única verdad sobre qué
>   chats están tomados a mano; `conversaciones.asignado` la refleja y ya no es una columna
>   huérfana. P7/P8/P12 no deberían escribirla por su cuenta.
> - **`wa-baileys.ignorar_propios` ya no existe:** es `escuchar_al_dueno` (sentido inverso).

> P1 liberó `src/canales/factory.ts` y `src/modulos/indice.ts`. **Ojo para P14
> (Instagram):** el `switch` de `factory.ts` ya tiene su `case 'wa-baileys'` como molde a
> copiar, y `OpcionesFabrica` ganó `rutaDatos` (lo usan los canales que guardan sesión).
