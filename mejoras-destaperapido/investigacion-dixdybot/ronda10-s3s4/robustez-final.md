# Auditoría de robustez FINAL — dixdybot S3-S4 · 2026-07-24

**Firma:** Arquitecto de Robustez. **Alcance nuevo (S3-S4):** `src/core/caminos-motor.ts`,
`src/core/duda-motor.ts`, `src/modulos/caminos/` (modulo, destilar), `src/gimnasio/`
(personas, juez, sombra, modulo) + sus CLIs (`cli/destilar-caminos.ts`, `cli/sombra.ts`).
Re-verificación de la auditoría base (`robustez-base.md`). Ojo: 24/7 con plata real, en el
Mac donde vive el bot vivo.

**Línea base (antes y después de mis arreglos):**
- `pnpm exec tsc --noEmit` → **0** (limpio)
- `pnpm exec vitest run` → **304 passed** (eran 301; +3 tests de mi fix)
- `node cli/doctor.ts` → esquema + 10 módulos OK

**Restricciones respetadas:** NO toqué el proceso del bot vivo, NO hice git. El fix nuevo
respeta el checklist de administrabilidad (es mecanismo inyectable, no config de negocio;
default = comportamiento histórico). Cero datos de cliente en el molde.

---

## VEREDICTO

**Sí es robusto para producción con plata real**, con UNA condición dura sobre el
orquestador que aún no existe (H-A abajo). Los motores nuevos son **puros, deterministas y
muy bien probados** (juez/sombra/gimnasio/caminos/duda). Los tres frentes que la doctrina
teme están CERRADOS por construcción:

- **La sombra NO puede enviar a un cliente real: IMPOSIBLE por construcción.** El gimnasio
  importa SOLO `canales/sim/canal-sim.ts` (verificado por grep: cero import de Baileys/Meta/
  índice). `MotorSombra.responder` y `Agente.responder` devuelven texto; nunca tocan un canal.
  Los CLIs de sombra/destilar arman un bus SIN listener de canal → aunque el LLM emitiera algo,
  nadie lo envía. Teléfonos sintéticos `56990000001..`, jamás reales.
- **`claude -p` en loop SIN límite: no ocurre.** Gimnasio (personas de guion FIJO), juez (1
  llamada/conversación), sombra (muestra acotada), destilar (trozos finitos) → todos loops
  finitos y SECUENCIALES (await en serie). Además la puerta única trae el techo global de
  concurrencia (H2 de la base, sigue puesto: `maxTurnosConcurrentes`).
- **El destilador JAMÁS activa solo.** `propuestaACamino`, `caminoDesdeResumen` y
  `revisarPropuestas` nacen SIEMPRE en `estado:'borrador'`; el único paso a `'activo'` es
  `confirmar()`, y solo tras pasar el candado (`verificarParaActivar`: lint de cifras +
  pruebas doradas verdes + conflictos). JSON roto / basura del modelo → fail-soft
  (`extraerPropuestas` rescata el bloque, valida propuesta-por-propuesta, salta las malas;
  `revisarPropuestas` descarta las sin disparador). Doctrina anti-tapón intacta.

**Re-verificación de la base:** H1 (persistirSesiones tolerante) y H2 (semáforo global de
concurrencia) SIGUEN en el código (`grep` confirmó `maxTurnosConcurrentes`, `adquirirCupo`,
`liberarCupo` en `llm.ts`, y el try/catch en `escritor.ts`). H3-H12 sin cambios (documentados).

---

## HALLAZGOS NUEVOS

### [MEDIO · ARREGLADO] N1 — Colisión del código de 5 letras de la Duda (PK del relay) rompe la apertura en 24/7
**Dónde:** `src/core/duda-motor.ts` `abrirDuda` / `codigoAleatorio`; el INSERT en
`src/core/escritor.ts` `crearDuda` (`INSERT INTO dudas ...`, SIN `OR IGNORE`).

**Qué rompía:** el `id` de la Duda es a la vez el código del relay ("si abcde" por WhatsApp)
y la **PRIMARY KEY** de la tabla `dudas`. `abrirDuda` lo generaba con `codigoAleatorio()`
(5 letras, 26⁵ ≈ 11,88 M) **sin comprobar si ya existe**. Como las dudas RESUELTAS conservan
su código para siempre (`avanzarDuda` hace UPDATE, nunca borra), el espacio se va llenando y
la **colisión de cumpleaños** llega alrededor de √(11,88 M) ≈ **3.400 dudas de vida** — muy
alcanzable en un par de años de operación. Cuando el código nuevo choca con uno ya en la
tabla, `crearDuda` hace un INSERT que **lanza `SQLITE_CONSTRAINT`** → la apertura de la duda
revienta a media conversación → el bot no escala la pregunta de precio → lead mal atendido, y
el error sube al orquestador.

**Failure scenario concreto:** negocio con ~3-5 dudas/día durante ~2 años → ~3.000 dudas
acumuladas → una duda nueva saca un código que ya usó una duda vieja resuelta → INSERT
rechazado → la escalada de precio no se abre.

**Fix aplicado:** `DepsAbrir` gana un predicado inyectable `existe?: (codigo) => boolean` y un
helper puro `codigoUnico(generar, existe, maxIntentos=50)` que reintenta hasta hallar un código
LIBRE; si el universo está agotado o el generador degenera, **lanza `ErrorDuda`** (un error
visible es mejor que un INSERT roto). El orquestador pasa `existe: (c) => dudaExiste(c)`
(consulta síncrona a la DB, evaluada justo antes de `crearDuda` → sin carrera, el proceso es
single-thread). Sin el predicado, el comportamiento es el histórico (una sola generación), así
que ningún test viejo cambia. El motor sigue PURO (el predicado se inyecta, no toca la DB).

**Checklist de administrabilidad:** es MECANISMO (unicidad del id), no config de negocio — no
lleva ajuste (como `codigoAleatorio`); default idéntico al anterior; cubierto por test.

**Tests (+3):** `duda-motor.test.ts` → "con `existe`, esquiva el código ya tomado", "sin
universo libre LANZA", "codigoUnico devuelve el primer libre".

---

## RIESGOS DE CONTRATO PARA EL ORQUESTADOR (aún NO existe; no se pueden cerrar en los motores puros)

Los motores de S3-S4 son PUROS a propósito: la persistencia la hará un orquestador de turno
(pipeline) que todavía no está cableado (grep: nadie llama `confirmar/abrirDuda/correrSombra`
fuera de tests y CLIs). Estos puntos son la **especificación dura** que ese orquestador debe
cumplir; los dejo escritos porque son el verdadero riesgo de plata:

### [ALTO · para el orquestador] H-A — Activar el camino + resolver la duda debe ser UNA transacción
`confirmar()` devuelve el `camino` en `'activo'` Y una `transicion` a `resuelta`. Son DOS
escrituras (guardar el camino en `caminos.json`/módulo + `avanzarDuda(resuelta)`). El
orquestador **debe envolverlas en una sola transacción SQLite**. Si no:
- Si el proceso muere entre ambas → camino activo + duda huérfana en `check2_afinando`.
  **Auto-sanable** si el "publicar" es idempotente por id (ver H-B): el dueño re-confirma y la
  duda resuelve. Pero sin idempotencia, se ensucia.
- La **doble-resolución de la DUDA ya está blindada**: `escritor.avanzarDuda` valida
  `TRANSICIONES_DUDA` (`resuelta: []`) → un segundo `confirmar` lanza. Y JS single-thread +
  escritor síncrono ⇒ dos canales (panel + WhatsApp) no interleavean: el segundo lee la duda ya
  resuelta y su guardia (`fase !== 'check2_afinando'`) lanza. **No hay doble-resolución.**

### [ALTO · para el orquestador] H-B — "Publicar" un camino debe ser UPSERT por id y RE-CORRER el lint
Dos rutas llevan un camino a `'activo'`: `confirmar()` (que SÍ corre `verificarParaActivar`) y
el futuro botón "publicar" del panel sobre un borrador destilado. El destilador **marca** (no
descarta) los borradores con cifra en el cuerpo (`calidad.marcadosCifra`). Si el panel activa
un borrador con un simple flip de `estado`, una **cifra literal podría ir a producción**
saltándose el lint. Regla dura: TODA activación pasa por `verificarParaActivar`, y el merge del
camino en la config es **upsert por `id`** (no `push`), o `seleccionarCandidatos` vería el
mismo camino dos veces (benigno pero sucio; `resolverConflictos` ya deduplica por Map).

---

## HALLAZGOS MENORES (documentados, sin arreglo — bajo impacto)

- **[BAJO] N2 — CLI de sombra sin tope de `--muestra` (costo).** `cli/sombra.ts` toma
  `--muestra` con `aEntero` (positivo, SIN máximo); el schema del módulo lo capa en 500. Un
  `--muestra 100000` correría 100.000 `claude -p` secuenciales = plata. Es operador-invocado,
  con logs de progreso e interrumpible (Ctrl-C), y `reconstruirPares` lo acota a los pares
  reales del log. Recomendación: capar en 500 (como el schema) o avisar sobre un umbral.
- **[BAJO] N3 — `prioridad_sobre` de un camino consigo mismo se auto-elimina.** En
  `resolverConflictos`, `{de:X, prioridad_sobre, a:X}` con X activo hace `activos.delete(X)`
  ("X no disparó porque X tiene prioridad"). Dato que controla el dueño; footgun raro. Sin
  crash. `implica` a sí mismo NO cicla (guardia `!activos.has`); `depende_de` a sí mismo se
  satisface solo.
- **[BAJO] N4 — El loop del resolver estabiliza en máx 3 pasadas.** Cadenas `implica` de largo
  ≥ 4 con orden adverso podrían sub-propagar. Para configs reales (pocas relaciones) sobra; es
  un tope de seguridad conocido (evita loops). Sin infinito, sin crash.
- **[BAJO] N5 — `parsePrecio('2 baños')` → 2.** Una cantidad suelta en la respuesta libre del
  dueño se lee como precio (2 miles) y `evaluarRespuesta` podría objetar "bajo el costo".
  Contexto: el texto es una respuesta de PRECIO del dueño; ruido improbable. Sin efecto grave.
- **Perf 0/500 caminos:** con 0 caminos `seleccionarCandidatos`/`prepararTurno` devuelven vacío
  sin crash; con 500, la selección es O(N log N) + `tagsDeCamino` recomputado por turno
  (~1-2 ms) y `maxCandidatos` (≤20 por schema) evita la dilución. Determinista (desempate por
  índice original). Todo dentro de presupuesto.

---

## Verificado SANO (para que conste)
- **Sombra/gimnasio = sandbox por construcción:** solo `canal-sim`, teléfonos sintéticos,
  `MotorSombra`/`Agente` devuelven texto. Enviar a un cliente real es imposible.
- **Máquina de la Duda:** cada transición con guardia de fase (throw si no corresponde);
  `TRANSICIONES_DUDA` del escritor la re-valida en la persistencia; `resuelta` es terminal
  (sin doble-resolución); `expirada → evaluando` revive; `check2` sin pruebas verdes NO nace el
  camino (fail-closed). Cobertura: 31 tests (máquina completa + integración escritor/ledger).
- **Destilador fail-soft:** JSON roto o propuesta inválida se salta sin tumbar el lote; todo
  nace borrador; el candado de activación corre el lint de cifras + pruebas doradas.
- **Juez:** una llamada por conversación por la puerta única; si el JSON no valida → `fallo`
  (excluido del score, JAMÁS aprueba); el gate es config (`gate_nota`) → administrable.
- **Administrabilidad (checklist #1) de los módulos nuevos:** `caminos` y `gimnasio` traen
  configSchema Zod + configDefault + aportes config-driven + test "dos ajustes → dos conductas"
  y "un .json inválido no opera a medias: falla en simple".

## Cambios de código (solo N1, tests verdes)
- `src/core/duda-motor.ts` — `DepsAbrir.existe?` + helper `codigoUnico`; `abrirDuda` usa código
  libre cuando se inyecta el predicado.
- `src/core/duda-motor.test.ts` — 3 tests (esquiva colisión / lanza sin universo / primer libre).

`tsc --noEmit` = 0 · `vitest run` = 304 passed · `doctor` OK.
