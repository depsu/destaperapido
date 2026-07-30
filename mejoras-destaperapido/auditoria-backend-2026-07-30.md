# Auditoría backend dixdybot — 30-jul-2026

> **ESTADO: E0 (Cinturón) HECHA y en vivo el 30-jul.** Lo que cerró y cómo se verificó está
> al final, en §11. Lo de arriba queda como el retrato del problema. Siguiente: E1
> (historial + volver atrás) y la **Tabla de precios** (§12, idea de Alejandro 30-jul).

Cuatro revisores en paralelo: motor de caminos, historial/versionado, módulos/tablero/agentes,
e instancias vivas (8793 destaperapido · 8794 DIXDY). Cada hallazgo trae archivo:línea del
molde (`~/SaSS/DIXDY/dixdybot/`). Este doc es la lista de implementación: las etapas E0-E5
del final salen de aquí. Versión en simple: en el chat del 30-jul.

**Veredicto:** la base es sólida (módulos genuinamente genéricos — cero rubro en `src/`,
verificado por grep; escritor único; ledger append-only real; ~5.000 líneas de test del
motor; ajustes administrables por JSON Schema desde el panel). Los problemas son de dos
familias: (1) cinco hoyos puntuales serios, dos ya mordieron en producción; (2) un patrón:
**enchufes sin cable** — schema/panel/docs prometen cosas que ningún código ejecuta.

---

## 1 · Hoyos graves (ya mordieron o van a morder)

### 1.1 Crash ×3 por media sin mimetype (producción)
`TypeError: Cannot read properties of null (reading 'mimetype')` en
`src/canales/wa-baileys/normalizar.ts:150` (`extraerMedia`), disparado por flush del
event-buffer de Baileys. Mata el proceso Node; KeepAlive lo relevanta pero el mensaje en
vuelo se puede perder. 3 crashes en `panel.error.log` de destaperapido (stacks por
`canal.ts:262` y `:278`). Fix: guard de `nodo` null + test.

### 1.2 El respaldo diario NO cubre dixdybot
`com.dixdy.respaldo` (restic 05:10, latidos OK) respalda el whatsapp-bot VIEJO
(`auth|data`), `.env.local`, plists — pero los TARGETS de
`~/SaSS/DIXDY/scripts/respaldo.sh:17-24` no incluyen ninguna `dixdybot-data/`: ni `bot.db`,
ni `ledgers/`, ni `auth/` (sesión WhatsApp: perderla = re-vincular). Además
`respaldar()` (`VACUUM INTO`, `src/db/db.ts:73-75`) no tiene ningún caller y el plist
`com.dixdy.respaldo` que su comentario promete no existe en `launchd/` del molde.
Fix: TARGETS += ambas `dixdybot-data/` con snapshot previo de la DB (VACUUM INTO a staging;
no copiar bot.db en caliente con WAL).

### 1.3 Dudas: timeout y aviso por WhatsApp son mentira
- `expirar()` (`src/core/duda-motor.ts:386-396`) **sin callers de producción** → fase
  `expirada` inalcanzable. `dudas.timeout_horas` y `escalada_min`
  (`src/modulos/dudas/modulo.ts:24,31-32`) se copian al payload y nadie los lee.
- Real: 3 dudas pegadas en destaperapido — prjst `pendiente` desde 28-jul 17:44, ockbe y
  baffe `evaluando` (109 h y 46 h al 29-jul); las 3 con `timeoutHoras: 4`.
- Mientras una duda ocupa el cupo `max_dudas_por_chat`, ese chat no abre tarjetas nuevas.
- `avisar_por_wa` ("Avisarte por WhatsApp", `src/modulos/dudas/modulo.ts:27`) solo condiciona
  un `bus.emitir('aviso')` cuyos oyentes son `console.log` y web-push
  (`src/index.ts:373,380-386`). Nunca sale por WhatsApp.
- El aviso dice `Responde "si <id> <respuesta>"` (`src/core/orquestador.ts:681-683`) pero el
  relay no está cableado: `parseCodigoRelay`/`interpretarRelay`
  (`src/core/duda-motor.ts:591,608`) solo tienen callers en tests; todo entrante va directo a
  `orq.atender` (`src/index.ts:348-350`).
Fix E0: expiración perezosa al leer (patrón sesión-agente: calculada en lectura, sin cron
nuevo — doctrina DIXDY) + aviso al expirar; sincerar el texto del aviso (sin "responde si…")
o cablear el relay; knob `avisar_por_wa` se esconde o se cablea.

### 1.4 La prueba dorada del camino aprendido no se persiste → reactivación imposible
`POST /api/dudas/:id/confirmar` crea la prueba `duda-<id>` en memoria
(`src/panel/api.ts:637-654`) pero el único `ajustes.guardar` del handler es al cotizador
(`:679`); ni `confirmarCamino` ni `publicarCaminoYResolverDuda` la escriben al pool
(`caminos.pruebas`). Consecuencia: desactivar un camino aprendido
(`POST /api/caminos/:id/estado`) → `verificarParaActivar` no encuentra `duda-<id>` en el
pool → 409 permanente; y su veredicto en `/borradores` queda ❌ para siempre.
El test de `/confirmar` usa un `confirmarCamino` stub (`src/panel/api.test.ts:1099-1116`),
por eso nunca se vio. Fix: persistir la prueba en el mismo flujo (transacción) + test de
integración de re-activación.

### 1.5 Puerta trasera del candado
`PUT /api/modulos/caminos` (`src/panel/api.ts:943-968`) escribe `ajustes/caminos.json`
entero validando SOLO Zod → se puede publicar `estado:'activo'` con cifra y sin pruebas,
saltándose lint, pruebas doradas y conflictos. Contradice el comentario "no hay puerta de
atrás para activar" (`src/core/orquestador.ts:19-20`). Y no existe endpoint de crear/editar
camino en `api-caminos.ts` (solo GET, `/aprobar`, `/fusionar`, `/:id/estado`) — o sea la
puerta trasera ES la vía de edición actual. Fix en E2/E3: vía sana de edición
(borrador→candado) y el PUT pasa por el mismo lint.

---

## 2 · El cerebro puede romper el estado (filtros baratos que faltan)

- **Id alucinado hacia camino retirado/borrador secuestra el turno** (verificado ejecutando
  el motor): `caminosAplicados` acepta cualquier `^camino:X:` (`src/core/caminos-motor.ts:654`)
  y `resolverConflictos` filtra contra TODO el catálogo, no solo activos (`:708`). Un
  `prioridad_sobre` de un retirado desactiva al legítimo; `pathSiguiente` fija
  `camino_activo='retirado'` que la selección nunca reelige (`:129`) → path envenenado y
  `prepararTurno` deja de armar reglas.
- **`transicion_elegida` se obedece sin validar** (`src/core/orquestador.ts:353-357`):
  camino inexistente se persiste igual; paso inexistente cae a `raiz`
  (`src/core/caminos-motor.ts:210`) → reinicio silencioso del camino, posible loop.
- **`booleanoTolerante` invierte negaciones en prosa** (`src/schemas/turno.ts:38-39`, match
  de cadena completa): `"no corresponde"→true`, `"descartado"→true`, `"no aplica en este
  caso"→true`. Para `aplica` (neutro false) es exactamente al revés de lo que el modelo quiso.
- **Id pelado**: tolerado en `razones` (`src/core/orquestador.ts:566-568`) pero no en
  `caminosAplicados` → traza y conducta discrepan.
- **`caminos.json` inválido deja al bot MUDO**: `caminosEfectivos` llama
  `ajustes.deModulo` sin blindar (`src/core/orquestador.ts:282`; `deModulo` lanza por diseño,
  `src/core/config.ts:66`) — otros módulos sí están blindados (`:270-273,378-381,391-398`).
- **`siempre_estructurado:false` + embudo apagado → `falta_camino` inalcanzable**
  (`src/core/orquestador.ts:531-532`): sin salida estructurada el bot puede inventar precio.
  Hoy lo tapa `embudo.activo` default true.
- Cero tests adversariales de esto (ids inventados, transiciones falsas, negaciones en
  prosa). Fix E0: filtrar aplicados/conflictos a catálogo ACTIVO, validar transición contra
  catálogo+paso, arreglar negaciones por prefijo, blindar `caminosEfectivos`, forzar
  estructurado si caminos activo, + tests.

---

## 3 · Selección y conflictos (motor)

- Puntaje (`src/core/caminos-motor.ts:95-121`): `aciertos*10 + dominio*100 + global*1`;
  corte `maxCandidatos` default 5, tope 20 (`src/modulos/caminos/modulo.ts:242`).
- **El dominio se cuenta dos veces** (token del dominio en `tagsDeCamino:68` y
  `tagsDelTurno:79` → +10 extra) y aplasta a los globales (+1): con ≥5 caminos del dominio
  activo, un global que calza literal (31 pts) queda fuera. Medido: 6 de `ventas` sin
  palabras en común puntúan 110. Latente hoy (dominioActivo=null en producción, ver §6),
  explota cuando exista derivación.
- **Empates favorecen a los viejos**: desempate por orden del archivo (`:131,136`) y
  `fusionarCaminos` pone los publicados al final (`src/modulos/caminos/consultas.ts:61-63`)
  → lo aprendido pierde cupos sistemáticamente.
- Cada candidato aporta 1 línea (disparadores + acción del paso raíz, `:351`); los pasos
  2..N no viajan salvo camino en curso. El prompt NO explota con 100 caminos (medido:
  ~1,5 KB con 5 candidatos; ~5 KB con 20). Lo sin tope: disparadores por camino y
  transiciones del camino vivo (una regla por saliente, `:211-239`).
- `TurnoCaminos.tags` (contexto: etiquetas, embudo) es input muerto: declarado `:39`,
  usado `:80-82`, el orquestador nunca lo pasa (`src/core/orquestador.ts:515-520`).
- `resolverConflictos` (`:698-799`): máx 3 pasadas → **`implica` en cadena se trunca al 3er
  salto en silencio** y el resultado depende del ORDEN de escritura en el archivo
  (verificado con cadena a→b→c→d→e). `desambiguar`/`reevaluar` son decorativos.
- **Path vivo salta a `activos[0]` = primero del ARCHIVO**, no el de mayor puntaje
  (`src/core/orquestador.ts:363-366`; orden de `:772`). Reordenar caminos.json cambia
  conducta.
- **Ids duplicados = doble conteo** (verificado): dos caminos id `dup` gastan 2 cupos,
  proyectan la misma regla y generan 2 `camino.aplicado` + 2 incrementos de uso.
- `resolverConflictos` es no-op en la instancia real: 0 relaciones declaradas en los 30
  caminos (el propio código lo admite, `:385-387`).

## 4 · Validación al publicar (linter que no existe)

`verificarParaActivar` (`src/core/duda-motor.ts:492-525`) chequea 4 cosas (cifra, pruebas
presentes, pruebas pasan, dependencias). NO existe validación de: ids de camino duplicados,
ids de paso duplicados, `via` a paso inexistente (proyecta un cierre inventado,
`caminos-motor.ts:227-228`), ciclos de transiciones, "máx 1 transición sin condición"
(el comentario cita un `lint.ts` que no existe, `src/schemas/camino.ts:61`), relaciones con
typo (silenciosamente muertas salvo `depende_de`).
Inconsistencia entre vías: `lint_cifras`/`solape` los pasa el panel (solo `partesLint`,
nunca `solape`: `api-caminos.ts:489,634,721`), no la vía duda (`duda-motor.ts:553-555`) ni
el orquestador (`orquestador.ts:751-755`); el CLI pasa ambos. `/aprobar` no recalcula
avisos de solape que `/borradores` sí muestra. `ConfigSolape.dominios_globales` duplica
`ConfigCaminos.dominiosGlobales` a mano (`caminos-motor.ts:454-457`).
Fix E2: UN linter de caminos usado por las 3 vías + refine de `ConfigEmbudo`
(etapa_inicial existe, transiciones válidas, ids únicos — hoy cero `.refine`,
`src/schemas/embudo.ts:56-74`; romperlo desde el panel da 200 y revienta runtime:
`ErrorEscritor` en `crearPedido`, `src/core/escritor.ts:730-733`, huérfanos atascados en
`moverPedido`, `:776-781`).

## 5 · Historial / volver atrás (idea 1 de Alejandro) — hoy NO existe

- `Ajustes.guardar` sobrescribe sin rastro (`src/core/config.ts:74-100`): sin autor, sin
  fecha, sin valor anterior, sin evento. 10 call sites, TODOS pasan por esa puerta única.
- El agente IA ya escribe ajustes indistinguible del dueño (contrata/despide especialistas
  `api.ts:1293,1302`; método de vinculación `:1570-1576`).
- Ledger: 32 tipos de evento reales; **los tipos documentados en `esquema.sql:110-118`
  (`camino.editado/descartado/deshecho`, `ensenanza.*`, etc.) NO existen en código**. No
  registra ni edición de caminos ni ningún cambio de config. `camino.publicado` lleva
  metadata, no payload.
- `schemas/borrador.ts` (diff antes/después + "deshacer restaura como borrador") es código
  muerto. `Camino.version` nunca se incrementa. El "historial" de la ficha son ≤2 líneas
  derivadas de timestamps (`api-caminos.ts:384-398`).
- **Trampa del restore**: caminos viven en DOS almacenes y `caminos_publicados` le gana al
  ajuste por siempre (`fusionarCaminos` upsertea por id, `consultas.ts:56-65`). Restaurar
  solo `caminos.json` deja al camino MUDO si hay fila publicada homónima. La foto debe
  capturar ajuste + filas publicadas juntos.

**Diseño E1 (mínimo, respeta "solo tablas nuevas"):**
1. Tabla `puntos_restauracion(id, alcance, foto TEXT, quien, via, que, ts)` + índice
   `(alcance, ts)`, como migración de módulo (patrón `agente-chat/modulo.ts:53-56`).
   `foto` = JSON `{ajustes:{<moduloId>:config}, caminos_publicados:[filas]}`, guardando
   `antes` (volver = 1 registro).
2. Hook `alGuardar?(moduloId, antes, despues, quien, via)` en opciones de `crearAjustes`
   (`config.ts:34-37`), cableado en `index.ts:134` → cubre dueño+IA+CLI sin tocar 10 sitios.
   `quien` discriminable por ruta (endpoints del agente son rutas propias:
   `/api/agentes/guia`, `/api/conexiones/guia`, `/api/chats/:id/agente`).
   Segundo punto de escritura: `escritor.publicarCamino` (`escritor.ts:644-652`).
3. Eventos nuevos `ajuste.cambiado` / `punto.restaurado` al ledger (gratis: `apendear`
   acepta unknown; `bitacoraDe` ignora tipos desconocidos).
4. Restaurar SIEMPRE por las mismas puertas: `ajustes.guardar` (revalida Zod, rename
   atómico) + `publicarCamino` por fila + `estado:'retirado'` para ids sobrantes (jamás
   DELETE). `respaldar()` (VACUUM INTO) antes de todo restore. Foto con sello de versión.
5. UI: vista "Cambios" (backlog panel izquierdo): lista quien/cuándo/qué + botón "volver a
   este punto".

**Riesgos de restore mapeados** (referencias por id SIN FK): pedidos.etapa→config embudo
(huérfano queda atascado: sin transición desde etapa inexistente, y el hero deja de
contarlo `embudo/consultas.ts:157-163`); conversaciones.camino_activo/paso colgantes;
pool de pruebas solo-crece vs candado (`api-caminos.ts:536-545` vs `:715-727` — "volví
atrás y nada se puede publicar"); caminos_publicados.duda_id↔dudas sin cascada;
agente_id/Camino.dominio→especialistas; ids de camino sin correlativo anti-reuso
(pedidos sí lo tienen).

## 6 · Agentes y tablero (idea 3) — estado real

- **Las fichas de Especialista son decorativas**: `personalidad/funcion/ejemplo/descripcion`
  (`agentes/modulo.ts:16-45`) solo se leen desde el panel. El prompt del bot es UNA persona
  global (`data/persona/base.md`, `index.ts:109-115` + `orquestador.ts:261-275`). Cero
  líneas meten al prompt la personalidad del especialista.
- **La derivación no existe**: `conversaciones.agente_id` solo lo escribe el migrador
  (default 'ventas', `migrador/modulo.ts:35-38`, `espejo.ts:845`); `asegurarConversacion`
  inserta sin agente (`escritor.ts:425-428`); `dominio_detectado` del LLM solo etiqueta la
  Duda (`orquestador.ts:600`), nunca se persiste. **Todo chat nuevo corre con
  dominioActivo=null** → solo globales + palabra clave. `Recepcion.activa` no se lee.
  El panel cuenta "derivados" con filas migradas (`agentes/consultas.ts:112-114`).
- **Tablero único por diseño en 6 capas**: `pedidos` sin discriminador
  (`embudo/modulo.ts:21-32`); ajustes 1 config por manifest.id (`config.ts:44-49`) + ids de
  módulo únicos (`indice.ts:52-56`); `Aportes.etapasTablero` plano con dedup
  primera-gana (`schemas/modulo.ts:66`, `indice.ts:112-116`); API `GET /api/tablero` único
  (`api.ts:861-868`); `moverPedido` recibe UN config (`escritor.ts:252`); front un `#board`
  (`app.js:1929-1971`).
- **El tablero es vitrina**: `POST /api/pedidos/:id/mover` existe y está probado
  (`api.ts:876-901`) y el front NUNCA lo llama (tarjetas solo `abrirChat`,
  `app.js:1951-1953`). Sí es administrable por instancia desde el panel (etapas renombrables,
  test `api.test.ts:532-554`) — eso está bien.
- **Manos cerradas ×3 sin abstracción**: `SalidaAgente` enum inline + if/else
  (`api.ts:1771-1775,1855-1866`); guía agentes (`:1209-1215,1283-1304`); guía conexiones
  (`:1312-1340`). Los módulos no pueden aportar manos (`Aportes` = 4 campos, ninguno
  ejecutable); `tiposDecision` se compone y nadie lo consume (`consultas.ts:572-601`).
- **Contrato Modulo con 4 hooks muertos**: `herramientas()`, `alMensaje()`, `rutasPanel()`,
  `iniciar()/detener()` (`schemas/modulo.ts:140-144`) — cero consumidores.
  `ConsultaLLM.herramientas` no se lee en `llm.ts`.
- **Gimnasio sin arranque**: `correrPersona/correrGimnasio/juzgar` solo se llaman desde
  tests; no hay endpoint POST ni CLI → `registrarCorridaGimnasio` sin caller → vista
  Agentes dice "Todavía no ha practicado" porque NO HAY cómo practicar. Además está atado a
  venta (RE_VENTA `personas.ts:145-152`, `esperaVenta`, rúbrica del juez fija con
  `precio-inventado`, `juez.ts:41-60`).
- 8 cerebros LLM distintos, cada uno con prompt cableado en su archivo (bot, agente-chat,
  guía agentes, guía conexiones, resumidor, juez, sombra, gimnasio) + 2 CLI.

## 7 · Aprendizaje (duda→camino) y destilador

- Flujo real: responder → decidir → afinar → confirmar (4 pasos obligatorios, endpoints
  `api.ts:442,470,546,614`) + resumir/seguir opcionales. Nace ACTIVO (no borrador,
  `duda-motor.ts:565`). La estructura la arma una plantilla hardcodeada
  (`caminoDesdeResumen`, `:425-451`); los disparadores salen de partir `alcance` por
  `[·,;/]` (`api.ts:632`) — disparadores pobres tipo "Comuna Lejana".
- `snapshotSuspendido` se escribe y jamás se usa para retomar (`orquestador.ts:645-651`).
- **Destilador ignora la config del clon**: solo lee cotizador (`cli/destilar-caminos.ts:121`);
  `construirPromptDestilacion` sin `grupos` (`:135-139,167-172`) → usa GRUPOS_EJEMPLO del
  molde; `revisarPropuestas` sin opciones (`:198`) → `grupos_cerrados`/`grupo_por_defecto`
  muertos. `archivo_borradores` configurable puede desincronizar panel vs CLI (escribe
  hardcodeado `caminos-propuestos.json`, `:110`).

## 8 · Inventario de enchufes sin cable (cablear o esconder)

Muertos con cero lectores en producción (fuera de lo ya listado):
`Paso.efectos` + schema `Efecto` completo (sin runner — "cómo un camino mueve el mundo");
`paso_completado` (parseado, no leído; su comentario cita `motor/efectos.ts` inexistente);
`Paso.tipo` (el motor no lo mira: `pausa-dueno` NO pausa — la duda la dispara
`falta_camino`; `tool`/`decision` sin un solo lector); `herramientasHabilitadas` (calculada
`caminos-motor.ts:334-339`, nadie la consume — el gating Parlant de tools es decorativo);
`plantilla_id` (pedido en prompt, jamás selecciona plantilla); `ReglaProyectada.continua` /
`.seguimientos`; `Paso.espera_del_cliente` / `.timeout_horas` / `.respuesta_espera` (solo
lint); `PruebaDorada.tipo` (runner decide por `ctx.rigor`); `Camino.version` /
`schema_version`; `embudo.cobrado_cuando` y `embudo.perdido_por_silencio_dias` (muertos;
OJO: `cotizador.ultimo_click` está VIVO — `cotizador/modulo.ts:337`); `dudas.timeout_horas`
/ `escalada_min` / `avisar_por_wa` (§1.3); `TurnoCaminos.tags`; `envios.jsonl` (nunca se
lee); motor `sdk` declarado y no implementado (`llm.ts:270` "la cadena lo salta").
Docs que mienten: `esquema.sql:110-118` (eventos inexistentes), `TODO-BACKEND.md` §dudas
(3 de 4 ítems ya resueltos), `orquestador.ts:19-20` ("no hay puerta de atrás"),
`api-caminos.ts:18` ("nunca heurística paralela" — falso para avisos de solape).
**Regla de casa propuesta: lo que se ve, funciona; lo que no funciona, no se ve.**

## 9 · Datos vivos (29-jul)

- destaperapido: 187 conversaciones, 3.998 mensajes, 25 pedidos, DB 2,0 MB. 30 caminos
  publicados (28 activos, 2 retirados), todos `origen=aprendido`; dominios ventas 21 /
  soporte 4 / general 3 / agenda 2; solape máx Jaccard 0,26 (sano); borradores pendientes 0
  (caminos-propuestos.json = los 30 ya publicados). Pares a vigilar: extra-sin-tarifa ↔
  extras-con-total; neto-iva-factura ↔ empresa-factura; fuera-de-cobertura ↔
  ubicacion-especial.
- Cerebro: 52 llamadas 24→29-jul (cli 50, plantilla 2); 2 cadenas completas
  cli(parse)→api(no_disponible)→plantilla — **el respaldo API nunca estuvo disponible**
  (decisión de plata: ANTHROPIC_API_KEY como respaldo). ~USD 14,4 acumulado estimado.
- Trazas: 24 `turno.evaluado` (todos desde 26-jul); **`razones` pobladas solo 4/24**;
  `camino:null` en 9/20 entradas (concentrado en 2 eventos); aplicados ≥1 en 14/24.
  → reforzar instrucción/schema para que `reglas_aplican` venga siempre que haya candidatos.
- DIXDY (8794): sana, cero errores, 1 conversación, 0 caminos, wa-baileys apagado.
- Ambos procesos estables desde 28-jul ~23:11 (reinicio del deploy push/PWA).

## 10 · Plan propuesto (E0→E5)

| Etapa | Contenido | Tamaño |
|---|---|---|
| **E0 Cinturón** | 1.1 crash guard · 1.2 respaldo (TARGETS + VACUUM INTO staging) · 1.3 expiración perezosa + aviso sincero · 1.4 persistir prueba dorada + test reactivación · §2 completo (filtros anti-alucinación, transición validada, negaciones, blindar caminosEfectivos, estructurado forzado) + tests adversariales | chica |
| **E1 Historial + volver atrás** | tabla `puntos_restauracion` + hook `alGuardar` + `quien` por ruta + eventos `ajuste.cambiado`/`punto.restaurado` + API + vista "Cambios" con botón volver + respaldo pre-restore | mediana |
| **E2 Un solo candado** | linter único de caminos (ids únicos, via válidas, relaciones existentes, máx-1-sin-condición, solape en /aprobar) usado por las 3 vías · endpoints sanos crear/editar (borrador→candado) · PUT modulos/caminos pasa por el linter · refine ConfigEmbudo + agentes | mediana |
| **E3 IA en Caminos** | agente estilo agente-chat en la vista Caminos: explicar camino en simple, proponer_camino (borrador), editar_camino (borrador→candado), activar/retirar vía candado; todo al historial E1 · destilador lee grupos del clon | mediana |
| **E4 Agentes de verdad** | fragmento de persona por especialista al prompt según dominio · derivación real (persistir `dominio_detectado` → `agente_id` vía escritor; `Recepcion.activa`) · corregir contador "derivados" · endpoint POST gimnasio "practicar" → vista Agentes viva · arreglar doble-conteo de dominio en puntaje (§3) antes de encender derivación | mediana |
| **E5 Tableros por flujo** | config multi-tablero + vínculo pedido↔tablero (tabla nueva, no columna) + aportes con clave de tablero + API/front parametrizados + mover pedido desde el panel (el endpoint ya existe) | grande |

Transversal: inventario §8 (cablear o esconder, empezando por lo visible en panel);
`razones` al 100%; sincerar docs que mienten. Pendiente decisión Alejandro: API key de
respaldo del cerebro (plata).

---

## 11 · E0 CINTURÓN — cerrada el 30-jul (977 tests verdes, en vivo en las 2 instancias)

| # | Qué se hizo | Dónde | Verificado con |
|---|---|---|---|
| 1 | Guard de media con contenido `null` (ya existía en el código; le faltaba el test que lo congela) | `src/canales/wa-baileys/normalizar.ts:156-163` | test de regresión de las 3 caídas (`normalizar.test.ts`) |
| 2 | Respaldo cubre dixdybot: glob `$SASS/*/dixdybot-data` + FOTO consistente por instancia (`VACUUM INTO` a `~/Backups/dixdybot-fotos`, nunca copiar bot.db caliente) | `scripts/respaldo.sh` | corrida real: snapshot trae `destaperapido/dixdybot-data/{bot.db,ledgers,auth}` y `DIXDY/dixdybot-data/…`; las 2 fotos con `integrity_check ok` (187 y 1 conversaciones) |
| 3 | Expiración PEREZOSA de dudas, sin cron: en cada turno del bot y en cada carga de Hoy. Solo expira `pendiente` (una `evaluando` es conversación a medias contigo). No borra ni libera cupo: la tarjeta sigue y revive al responder | nuevo `src/modulos/dudas/expirar.ts`; llamada en `orquestador.atender` y en `GET /api/hoy` | **en vivo**: `prjst` (pendiente desde 28-jul 17:44, timeout 4 h) → `expirada` + evento `duda.expirada` en el ledger; `ockbe`/`baffe` (evaluando) intactas |
| 4 | Aviso sincero: se quitó el `Responde "si <código>"` que prometía un relay por WhatsApp inexistente; ahora lleva al panel. El knob `avisar_por_wa` se re-describe como «Avisarte con una notificación» | `orquestador.ts` (rama duda), `modulos/dudas/modulo.ts` | test del aviso (`not.toContain('Responde "si')`) |
| 5 | La prueba dorada `duda-<id>` se PERSISTE al pool al confirmar (`pruebaGuardada` en la respuesta) → el camino aprendido se puede apagar y volver a encender | `POST /api/dudas/:id/confirmar` | test: el pool en disco contiene `duda-abcde`, se suma a las de fábrica y no se duplica al re-confirmar |
| 6 | **Cerco del turno** en `caminosAplicados`: solo aplica un camino cuyas reglas se le OFRECIERON al cerebro (id pelado de candidato real sigue aceptado) | `caminos-motor.ts` | test del cerco + test en vivo del turno: camino retirado con `prioridad_sobre` ya NO secuestra ni el turno ni el path |
| 7 | `implica` solo arrastra caminos ACTIVOS (antes podía resucitar un borrador/retirado del catálogo) | `caminos-motor.ts` resolver (3) | suite de caminos |
| 8 | Salto validado: `transicion_elegida` se obedece solo si el camino existe, está activo y el paso existe; si no, se ignora (antes: camino inventado se persistía; paso inventado reiniciaba el camino en silencio) | `pathSiguiente` en `orquestador.ts` | test de los dos casos: el path queda en el camino real y no reinicia |
| 9 | Negaciones EN PROSA se leen como `false` (`"no corresponde"`, `"descartado: …"`, `"irrelevante"`, `"no se completó"`) — antes un NO del cerebro se leía como SÍ | `schemas/turno.ts` `enderezarBooleano` | test con los 5 casos que invertían la decisión |
| 10 | `caminos.json` ilegible ya no deja MUDO al bot (cae a defaults de fábrica; los aprendidos de la base siguen) | `caminosEfectivos` | test con JSON roto: el cliente igual recibe respuesta |
| 11 | Con caminos publicados el turno es SIEMPRE estructurado → `falta_camino` alcanzable aunque el embudo esté apagado (si no, prosa libre podía inventar precio) | `orquestador.ts` | test con embudo apagado y ningún candidato: la Duda igual se abre |

**Hallazgo NUEVO durante E0 (no estaba en la auditoría) — datos vivos en el repo maestro:**
`~/SaSS/dixdy/dixdybot-data` **ES** `~/SaSS/DIXDY/dixdybot-data` (el disco del Mac no
distingue mayúsculas), o sea la instancia DIXDY del panel público vive DENTRO del repo
maestro, y sus 14 archivos estaban **trackeados en git**: `bot.db`, ledgers, logs,
`sesiones.json` y `push-vapid.json` — una **llave privada**. Contradice la ley del repo
(«el maestro NO contiene datos de ningún cliente»). Se cerró así:
1. `/dixdybot-data/` a `.gitignore` con el porqué escrito.
2. `git rm -r --cached dixdybot-data` (los archivos siguen en disco; la instancia no se tocó).
3. La llave se **rotó** igual (`BJWD1U7i…` → `BKNH1dOj…`, la vieja guardada aparte como
   comprometida): gratis, porque había 0 teléfonos suscritos en ambas instancias.
No hubo filtración: el maestro está **97 commits sin subir** a GitHub, así que la llave
nunca salió del Mac. **La historia local sí la contiene** — por eso se rotó en vez de
reescribir la historia (reescribir es destructivo y no hacía falta).

**Nota operativa:** los avisos push no llegan a ningún teléfono todavía (0 suscripciones en
ambas instancias). El aviso de duda vencida está cableado; falta instalar la PWA y activar
avisos — para destaperapido eso pide publicar 8793 en el túnel (§docs/29, 5 min).

## 12 · Tabla de precios como pieza propia (idea de Alejandro, 30-jul) — diseño

Pedido: subir un Excel/PDF/foto y que la IA lo deje «bonito» como **Tabla de precios**
editable; que entienda variaciones (temporada alta, la semana del 18, rangos por cantidad) y
**recomiende** valores; y decidir DÓNDE vive (sección propia · vista del agente · Caminos) y
si se entrena conversando al crear el agente.

**Lo que ya existe y no hay que reinventar:** el `cotizador` es exactamente esa tabla como
datos (`ConfigCotizador.tarifario` + `tarifas_especiales`, editable por JSON Schema desde el
panel, inyectada al prompt por `fragmentoPersona`, y con `referenciaTarifario` que ya sabe
comparar un precio contra la fila más barata de una zona — es lo que usa la Duda para
discutirle al dueño). La ingesta ya guarda y hace mirar fotos/PDF/audio
(`src/modulos/ingesta/`, con Whisper local). El agente del panel ya tiene el patrón de
«manos» con tarjeta de aprobación. Falta: (a) importar un archivo → propuesta de tabla,
(b) variaciones por fecha, (c) una vista propia.

**Decisión de UX (dónde va):** sección propia en el menú izquierdo, **💲 Precios**. Razón:
un precio no es una regla de conversación (Caminos) ni una persona (Agentes) — es el dato que
el negocio consulta y corrige más seguido, y hoy vive escondido en Ajustes → cotizador, que
es el peor lugar para lo que más se mira. La vista del agente ENLAZA a Precios («este agente
cotiza con esta tabla»), no la duplica.

**Etapas propuestas** (después de E1, que le da el «volver atrás» que hace seguro editar
precios):
- **P1 · La tabla como vista.** `💲 Precios` con la tabla en grande (filas legibles, no
  formulario de JSON), edición en línea, y el historial de E1 por fila («quién cambió qué»).
- **P2 · Importar un archivo.** Subir Excel/PDF/foto → el LLM propone la tabla estructurada →
  **tarjeta de aprobación** lado a lado (lo que leyó vs lo que hay) → se aplica solo si el
  dueño acepta. Reusa ingesta + el patrón de manos. Nada se escribe sin OK, porque un precio
  mal leído es plata.
- **P3 · Variaciones por fecha/temporada.** Tabla nueva de reglas de precio con vigencia
  (`desde`/`hasta`, recargo % o monto, motivo) — «la semana del 18 sube 20%». El cotizador
  las aplica al cotizar y el bot DICE por qué («esa semana tiene recargo de temporada»).
  Sin tocar la tabla base: la variación es una capa, así se enciende y apaga sin miedo.
- **P4 · Recomendar.** El agente propone valores con datos que ya están en casa (historial de
  cierres, margen por fila, comparables de zona) y marca en pantalla qué es dato y qué es
  criterio suyo — la misma honestidad que ya usa en la Duda («esto es criterio mío, NO sale
  de la tabla»).
- **P5 · Entrenar conversando.** Al crear un agente, un chat estilo Claude Code que arma su
  tabla y sus caminos preguntando; todo lo que se acuerde queda reflejado en Precios y en
  Caminos (con el historial de E1 detrás). Va al final porque es la punta del embudo: exige
  P1-P4 + E3 (IA en Caminos) funcionando.
