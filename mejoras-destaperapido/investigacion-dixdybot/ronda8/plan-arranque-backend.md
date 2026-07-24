# EL PLAN DE ARRANQUE DEL BACKEND — dixdybot (ronda 8, documento de cierre)

**Fecha: 24-jul-2026 · Planificador del arranque.** Reconcilia y NO reemplaza: el plan
E0-E7 vigente (`ronda2/plan-revisado.md` + ajustes ronda 3 en `DIXDYBOT-ESTADO.md`), el
calendario S0-S5 del blueprint (`ronda5/blueprint-fundacional.md` §7) y los 3 informes de
esta ronda (`esqueleto-proyecto.md`, `auditoria-funcional-prototipo.md`,
`contrato-backend.md`). Las fechas duras quedan intactas: **19-ago** métricas LLM midiendo ·
**31-ago** Sonnet 5 probado con juez · **1-sep** tarifas Chile definitivas · **30-sep**
decisión Coexistence (tras piloto en número secundario; Baileys fallback caliente 30-60
días) · **1-oct** fin del responder gratis en Cloud API · **1-dic** Ley 21.719 (contrato de
encargo + ARCO+P en el panel; el art. 8 bis vuelve el humano-en-el-loop requisito legal).

**La regla de contingencia sigue mandando:** la fecha del canal manda sobre el orden de
etapas — si S3-4 (caminos) se atrasa contra el 30-ago, S5/E5 le pasan por encima.

---

## 0. Las 10 decisiones del arranque

| # | Decisión | Detalle en |
|---|---|---|
| 1 | **Semana 0 en doble carril (jue 24 – dom 27 jul):** E0 cinturón sobre el bot VIVO + pre-etapa Meta arrancan el mismo día que el pre-carril de diseño/contrato y el esqueleto D1 compilable. Nada espera a nada. | §1, §2-S0 |
| 2 | **Ronda 8 se commitea al clon ANTES de todo:** prototipo + 4 informes viven hoy en un scratchpad borrable (`/private/tmp/...`). Primer acto: `mejoras-destaperapido/investigacion-dixdybot/ronda8/` + actualizar `DIXDYBOT-ESTADO.md`. Doctrina deja-huella. | §1.1 |
| 3 | **El prototipo se congela como contrato v5** tras aplicar SOLO los arreglos P0/P1 de la auditoría (charset, scroll `vcol`, `recontar()`, los 6 fixes de máquina de estados, coherencia de números). Cero features nuevas: las brechas de la matriz r7 se resuelven en el panel real, no en el prototipo. | §1.2-1.3 |
| 4 | **El contrato se firma como schema, no como intención:** los 5 gaps bloqueantes del contrato (G10+G9 turno/traza, G19 duda multi-fase, G22 aportes, G12 `camino.aplicado`, G4+G1 ficha/agente en conversaciones) entran a `esquema.sql` y `schemas/` el DÍA 1. Ningún gap bloqueante se deja "para después". | §1.4 |
| 5 | **`migrar.ts` nace en S2 como espejo re-ejecutable, no en S5:** importador idempotente (dedup `INSERT OR IGNORE` por `source_id`) del JSONL del vivo → `bot.db`. El panel real muestra datos REALES de destaperapido tres semanas antes del cutover, y el migrador llega ensayado al día del corte. | §2-S2 |
| 6 | **Del prototipo se trasplanta el HTML/CSS, jamás el JS:** `tokens.css` + los componentes (fila, chip, pto, traza, diff, sw, burbujas, prog-card, correo-card) se copian tal cual; `app.js` se REESCRIBE como render-desde-API usando las funciones del prototipo como spec de interacción. | §4 |
| 7 | **El panel real reemplaza al prototipo vista por vista, siempre con datos reales:** Módulos (dibujada desde schema) + Hoy v1 + Chats/tablero en S2 · Caminos/Dudas/Agentes/Gimnasio en S3-4 · ✓✓ reales y muerte total del prototipo en el cutover S5. | §2, §4 |
| 8 | **Los personajes del prototipo no se botan: se vuelven pruebas doradas.** Carolina (duda junior→senior), Ranco (aprobar cotización + correo en hilo), Jorge (seguimiento programado), El Monte (foto anotada), regateo Baños King → guiones del gimnasio y `data/pruebas/*.yml`. El demo aprobado ES la batería de aceptación. | §4.3 |
| 9 | **Toda semana termina con destaperapido operando y un criterio "quedó viva" verificable** (tsc + vitest verdes + el hito de la semana en producción o en sombra + registro en `actividad.py`). Si un viernes el criterio no se cumple, la semana siguiente NO avanza de etapa: se cierra la anterior. | §2 |
| 10 | **Los 3 riesgos del arranque tienen seguro comprado antes de que ocurran:** ban de Baileys (E0 + expediente Meta precargado), metering de Anthropic (S1 primero + failover probado con juez antes del 31-ago), y estancamiento del estrangulador (semanas vivas + rollback launchd + vivo congelado 30 días). | §3 |

---

## 1. ANTES de la primera línea del motor (el pre-carril, 24-26 jul)

Cuatro actos, en este orden, todos ANTES de escribir `src/` (el esqueleto D1 incluido).
Duración total: ~48 h de trabajo IA + 2 decisiones cortas de Alejandro.

### 1.1 La huella primero (2 h)

- Copiar del scratchpad al clon: `dixdybot-prototipo.html` + `esqueleto-proyecto.md` +
  `auditoria-funcional-prototipo.md` + `contrato-backend.md` + este plan →
  `mejoras-destaperapido/investigacion-dixdybot/ronda8/`. Commit.
- Actualizar `DIXDYBOT-ESTADO.md`: estado pasa de "investigación completa" a
  **"arranque en curso — plan ronda 8"**, con el mapa de la ronda 8.
- Registrar en `actividad.py`. Motivo: hoy TODO el diseño maduro vive en un tmp que
  macOS puede borrar; es el único punto de fallo total del proyecto y cuesta 2 horas.

### 1.2 Arreglos funcionales del prototipo, priorizados (medio día)

Se aplican SOLO los que convierten el prototipo en un contrato coherente y compartible.
De la auditoría (20 hallazgos), entran en 3 tandas:

- **P0 — bloquean el recorrido o el archivo** (auditoría #1, #2): `<meta charset="utf-8">`
  primera línea; clase `vcol` en `#v-hoy`, `#v-modulos`, `#v-diseno`.
- **P1 — el contrato no puede mentir** (auditoría #3-8, #11-13, #15 y el patrón raíz):
  `recontar()` que deriva TODOS los contadores/totales de DATA (cnt-hoy, "7 chats"→real,
  totales de columnas, hero con composición declarada); estados de un solo disparo
  (aprobarRanco, publicar/descartar borrador con estado `pendiente|publicado|descartado`);
  limpieza de flags `espera` al resolver; filtro de agente real (`agenteFiltro` respetado
  por render/abrir/composer); `abrirChat` → `vistaChats('lista')` + scroll al fondo;
  números coherentes (El Monte $400, Ranco accesible $80.000, total de columnas
  computado); contadores de caminos que suben al nacer el camino de la pausa.
- **P2 — pulido barato que la demo agradece** (auditoría #10, #14, #16-18, #19a-c, #20):
  Peñalolén abre el chat de Pía; dormidos en el buscador con strip de tags; Escape cierra
  flotantes; 💡 accesible por teclado; contraste del badge en dark; guardarEtapas
  renombra columnas; Cancelar elimina la prog-card; Tomar/Devolver con banner; borrar
  markup muerto de la pausa y REPLAYS vacíos.
- **NO se hace en el prototipo:** ninguna brecha de la matriz r7 (gimnasio grande, camino
  multi-paso visible, embudo con tasas, feedback 👍👎 por mensaje, historial navegable
  completo, icono multi-canal). Todo eso ya tiene casa en el panel REAL (S2-S4); dibujarlo
  en el prototipo sería construirlo dos veces. El prototipo v5 es la última versión: se
  ETIQUETA y no se toca más.

### 1.3 Congelar el diseño (medio día)

- `panel/pwa/tokens.css` se extrae del `<style>` del prototipo v5 (líneas 1-335) y queda
  como EL archivo canónico del design system (decisión del esqueleto, D1). La vista
  Diseño del prototipo es su documentación viva.
- Publicar el sistema congelado en **Claude Design** vía DesignSync (skill
  `/design-sync`), como fijó la memoria `dixdybot-design-system`: tokens n1-n12 +
  ac/ámbar/rojo/azul + los 9 componentes de la vista Diseño. Regla escrita en el CLAUDE.md
  del proyecto nuevo: **ningún componente nace fuera de la vista Diseño / tokens.css**.
- El prototipo v5 congelado se publica como artifact para que Alejandro y futuros clientes
  lo naveguen sin tocar el código real.

### 1.4 Firmar el contrato (medio día, la parte de pensar ya está hecha)

`contrato-backend.md` queda declarado **anexo vinculante del blueprint r5** (donde chocan,
manda el contrato: es posterior y baja al detalle de consumo). Firmarlo significa tres
cosas concretas:

1. **Los 5 gaps bloqueantes entran al día 1** (ninguno se difiere): `mensajes.turno_id` +
   turno persistido correlacionado por `turnoId` (G10+G9) · tabla `dudas` + schema Duda
   multi-fase (G19) · campo `aportes` en el manifest v2 (G22) · evento `camino.aplicado`
   en el vocabulario del ledger (G12) · columnas `agente_id`, `ficha`, `visto_por_dueno_ts`,
   `bot_silencio_hasta`, `titulo`, `etiquetas` en `conversaciones` (G4+G1+G2+G5+deltas).
2. **Los gaps no bloqueantes quedan asignados a su semana** (G3, G6-G8, G11, G13-G18,
   G20-G21, G25 → S2-S4 según el módulo que tocan; G24 selector multi-negocio → decisión
   de producto diferida a E6, con el NO de `tenant_id` reafirmado).
3. **Los 16 NOes de sencillez se re-verifican contra el esqueleto** (ya auditado: 0 deps
   nuevas, 1 proceso, 1 escritor, 6 deps runtime) y quedan pegados en el `SETUP.md` del
   repo nuevo.

Con la firma, la definición de terminado del backend es una sola frase: **el panel real
sirve las entidades de §1, ejecuta los eventos de §2 y responde las queries de §3 del
contrato, con el prototipo v5 como referencia visual pixel-comparable.**

### 1.5 En paralelo desde el jueves 24: E0 + pre-etapa Meta (sobre el bot vivo)

Sin esto, todo lo anterior es un castillo sobre un bot que puede morir mañana:

- **E0 cinturón (1-2 días):** commit de los fixes vivos, alarma de muerte silenciosa
  401/healthcheck, circuit breaker de reconexión, backup de `auth/`, pins, rotación de
  logs, dedup/topes persistentes, verificación de entrega real ✓✓ (Error 463 activo),
  chequeo Opus 4.7 fast (muere el 24-jul), y `guardar.js` de media (~40 líneas con
  `reuploadRequest`) — desde el día 1 no se pierde ni un binario.
- **Pre-etapa Meta (papeleo, ~45 min de Alejandro repartidos):** Business Manager del
  cliente + app + número de prueba + Worker `meta-buzon` (plantilla del maestro) + system
  user/token + expediente de verificación precargado. La gestión externa la pide el
  Guardián, como siempre.

### 1.6 El esqueleto D1 (sábado-domingo 26-27 jul)

Checklist §5 del informe esqueleto, al pie de la letra: árbol `[D1]` completo, 6 deps
pineadas, los 8 schemas núcleo (mensaje, llm, camino v2, manifest v2 con aportes, duda,
conexion, pedido, borrador), `esquema.sql` con las 6 tablas + deltas firmados en §1.4,
`db.ts`/`escritor.ts`/`ledger.ts`/`bus.ts`/`config.ts`, canal `sim` ciudadano pleno,
`doctor.ts`, `tokens.css` copiado, 1 guion de gimnasio determinista. **`pnpm install &&
tsc --noEmit && vitest run` verdes en el primer commit.**

**Criterio de salida de la semana 0:** bot vivo blindado y sin pérdida de binarios ·
expediente Meta en curso · ronda 8 commiteada · prototipo v5 congelado y publicado ·
contrato firmado · `dixdybot/` compila con tests verdes.

---

## 2. Semana a semana

Formato por semana: **archivos del esqueleto** que se escriben · **órgano** que se
trasplanta · **panel: qué pasa de DATA simulada a datos reales** · **criterio "esta
semana quedó viva"** — siempre con destaperapido vendiendo sin interrupción.

### S0 · jue 24 – dom 27 jul — Fundación (E0 + pre-carril)

Es el §1 completo. Panel: nada real todavía (el prototipo v5 ES el panel de referencia).
Órganos: ninguno (solo `guardar.js` nuevo EN el vivo). **Vive si:** criterio §1.6.

### S1 · lun 28 jul – dom 3 ago — E1, la puerta única (prioridad #1 del plan)

- **Archivos:** `core/llm.ts` completo (cola por conversación, snapshot de config, cadena
  `sdk→cli→api→plantilla`, clasificación tipada de errores, sesión persistida en `init`,
  rotación, topes por turno) + `core/cola.ts` + ledger `uso-llm.jsonl` con campo `agente`
  (G18) · evaluación del Agent SDK como backend del modo `cli` (con juez, reversible) ·
  tools internas con contratos MCP-compatibles.
- **Órgano/estrangulamiento:** clon del núcleo a `~/SaSS/destaperapido/dixdybot/`;
  **`brain.js` del vivo queda de shim (~20 líneas) llamando a `llm.ts`** — commit
  reversible. El vivo sigue mandando; el núcleo es su motor LLM.
- **Panel:** sin cambios (prototipo v5). Se define la forma del endpoint `/api/resumen`
  (contadores del sidebar) para S2.
- **Vive si:** el bot vivo VENDE un día completo a través de `llm.ts` sin degradación
  (mediana de respuesta en el rango medido 8-18 s) · el failover `api` se dispara en
  prueba controlada y el ledger lo registra · métricas LLM midiendo (holgura de 2 semanas
  al 19-ago) · rollback ensayado (revertir el shim = 1 commit).

### S2 · lun 4 – dom 10 ago — E2, el conocimiento sale del código y el panel real NACE

- **Archivos:** contrato `Modulo` v2 + `config.ts` en uso real · `modulos/` embudo (con
  `migracion.sql` → tabla `pedidos` + `escritor.moverPedido` única puerta), ficha
  (bautizo + etiquetas automáticas), precios (tarifario-en-datos + `precioCoherente`),
  cotizador, cobros, seguimiento (tabla `seguimientos`) · `conexiones/` (registro,
  permisos, catálogo supabase; la conexión repartidor declarada con credencialRef) ·
  `ingesta/` completa (imagen, audio vía Groq — **OK de plata de Alejandro por el
  Guardián**, documento; video solo-ficha) · `panel/servidor.ts` + `api/` (hoy, chats,
  modulos, embudo, conexiones, onboarding esqueleto) + `pwa/` (shell + vistas Hoy, Chats,
  Módulos) · **`cli/migrar.ts` en modo espejo re-ejecutable** (decisión #5: JSONL del
  vivo → `bot.db` idempotente, corrida diaria/manual).
- **Órganos:** `extraer.js` → `src/organos/` (extractor + `fechaISO`, alimenta el bautizo)
  · `integracion.js` → `src/organos/` (cotizar/PDF/Supabase/repartidor, transitorio).
- **Datos trasplantados:** `precios.js` → `data/ajustes/precios.json` · `BOT_PERSONA` →
  `data/persona/base.md` · etapas reales de destaperapido → `data/ajustes/embudo.json`
  (Cotizando → Por confirmar → Por entregar → Cobrado **+ Perdido con motivo**, la brecha
  r7 cerrada de nacimiento).
- **Panel — muere la primera DATA:** `CHATS` (lista con bautizo/orden por atención/
  buscador FTS5 incl. dormidos), tablero (desde `pedidos` del espejo), `DORMIDOS`
  (estado real), vista Módulos **renderizada desde `z.toJSONSchema`** (la prueba reina de
  genérico-modular), Hoy v1 (hero y métricas compuestos desde `aportes`; decisiones de
  aprobación). Quedan simulados: dudas, caminos, agentes, replays, trazas.
- **Vive si:** Alejandro abre la PWA en el iPhone y ve SUS chats y SU tablero reales (vía
  espejo) · el bot vivo VE fotos y OYE audios (los dos casos perdidos de julio, resueltos:
  la anotación entra por el shim antes del cerebro) · apagar el módulo Entregas en un clon
  de prueba hace desaparecer columna+campos sin tocar código de panel.

### S3-S4 · lun 11 – dom 24 ago — E3, el corazón: motor + agentes + gimnasio

- **Archivos:** `motor/` completo (proyector, evaluador de UNA llamada, resolver con
  Resolution, **efectos.ts** determinista, **duda.ts** máquina junior→senior con relay de
  código 5 letras, **guia.ts** → Borrador tipado, lint.ts con lint inverso del embudo) ·
  `agentes/` (madre con los 3 casos del pop-madre, especialista, componer, **gate 4,0**) ·
  `gimnasio/` (6 personas deterministas, juez tipado, replay/forkSession + backtesting
  patrón Fin) · `panel/api/` caminos, guia, dudas, agentes, gimnasio + sus vistas ·
  persistencia del TURNO (evaluación+Resolution+efectos+uso por `turnoId` → trazas del
  panel) · eventos nuevos del contrato (`camino.aplicado`, `duda.*`, `ensenanza.*`,
  `herramienta.usada`).
- **Datos trasplantados:** las 68 reglas → 20-30 caminos YAML **con dominio desde el día
  1** (sofia = baños; destapes nace `practicando`) · casos de `_test-*.mjs` + correcciones
  del gimnasio vivo + **los personajes del prototipo** → `data/pruebas/*.yml` doradas.
- **Panel — muere la segunda DATA:** `PAUSA` → Dudas reales (tarjeta de Hoy y píldora del
  hilo = el MISMO objeto, vía `/api/dudas`), `CAMINOS` (cascada con stats reales de
  `camino.aplicado` + atribución de cierre), `GUIA` responde con caminos y números del
  negocio, borradores con candado de pruebas, `AGENTES` + `REPLAYS` (corridas reales del
  gimnasio), trazas porQue desde turnos persistidos.
- **Vive si:** una duda REAL de destaperapido recorre junior→senior de punta a punta
  (resumen → respuesta de Alejandro desde panel O WhatsApp → contra-argumento → check1
  respuesta al cliente → check2 camino nuevo con badge) **en sombra con el canal sim
  re-jugando el log** · caminos activables tras flag `CAMINOS_ON` con gate juez ≥4,0 ·
  publicar un borrador que rompe una dorada es RECHAZADO.
- **Checkpoint de contingencia (vie 22-ago):** si el gate del juez no da ≥4,0, S5 se
  ejecuta igual (E4 no depende de E3) y los caminos siguen madurando tras el flag.

### S5 · lun 25 – dom 31 ago — E4, el cutover: el núcleo ES el bot

- **Archivos:** `canales/wa-baileys/adaptador.ts` (backoff + circuit breaker + LID) +
  `media.ts` · `cli/vincular.ts` (de `link-code.mjs`) · `cli/migrar.ts` corrida FINAL
  (incluye dudas pendientes de `dudas.js`) · `MANUAL.md`.
- **Órganos (los últimos):** `enviar.js` + `outbox.js` → `wa-baileys/legado/` (candado
  anti-jid + auto-sanación Bad MAC) · `gating.js` → `organos/`.
- **Gate de corte (nada se corta sin esto):** gimnasio verde (6 personas) + juez ≥4,0 +
  tsc/vitest verdes + **48 h de sombra** con el sim re-jugando conversaciones reales +
  **Sonnet 5 probado con el juez ANTES del 31-ago** (fecha dura del failover).
- **El corte:** launchd pasa a `dixdybot/src/index.ts`; el vivo queda CONGELADO 30 días
  (rollback = re-apuntar el .plist); los JSONL quedan de archivo histórico solo-lectura.
- **Panel — muere la última DATA:** ✓✓ reales por `estado_envio`, prog-cards editables,
  tarjetas de correo del contacto en el hilo, "quién cotizó" desde el dato. **El
  prototipo v5 muere como interfaz** (§4.2) y queda de museo en ronda8/.
- **Vive si:** destaperapido opera un día completo SOBRE el núcleo sin intervención ·
  doctor verde · el rollback está ensayado y documentado.

### Septiembre (1-14: colchón · 15-30: E5) — Canales oficiales de Meta

- Semana 1-2 de sep: **colchón deliberado** para lo que se haya corrido (regla de
  contingencia) + endurecer lo cortado + tarifas Chile del 1-sep al business case.
- E5: `wa-cloud/` (adaptador + ventana real + `enviarPlantilla` + webhook HMAC) contra
  `meta-buzon` · **piloto en número secundario** · **decisión Coexistence el 30-sep** con
  Baileys de fallback caliente 30-60 días · Instagram DM en una tarde · seguimiento de
  cotización abandonada con plantilla utility · atribución CTWA al ledger.
- **Vive si:** el número vivo responde por Cloud API antes del 1-oct (o la decisión
  documentada de por qué no, con Baileys endurecido y el expediente listo).

### Octubre-noviembre — E6 producto + Ley 21.719 (fecha dura 1-dic)

- `SETUP.md` de clonado formalizado · API key por cliente con expiración · Cloudflare
  Access · pricing 4-6 / 8-12 UF + setup 5-10 UF · verificación Tech Provider arranca ·
  onboarding `nuevoNegocio` end-to-end (el segundo negocio real valida el molde).
- **Ley 21.719 antes del 1-dic:** contrato de encargo de tratamiento por cliente +
  derechos ARCO+P como vista del panel. Argumento de venta: la Duda junior→senior ES el
  humano-en-el-loop que el art. 8 bis exige — compliance de fábrica.
- E7 (voz): solo carpeta de evidencia. No se construye.

---

## 3. Los 3 riesgos principales del arranque y su mitigación

1. **Baileys muere a mitad de la construcción (ventana jul-sep, el riesgo que no avisa).**
   Un ban permanente del número vivo con el núcleo a medias sería la tormenta perfecta.
   *Mitigación comprada en la semana 0:* E0 con circuit breaker (los crash-loops son el
   vector verificado) + expediente Meta precargado + Worker `meta-buzon` listo → la
   emergencia se vuelve una migración Coexistence de HORAS, no semanas. Y el orden del
   plan protege: desde S1 el cerebro ya está detrás de `llm.ts`, así que un cambio de
   canal de emergencia no toca el motor.
2. **Anthropic reactiva el metering de `claude -p` con poco aviso (el cerebro vive de esa
   gracia).** *Mitigación:* S1 es la PRIMERA semana de código de producción (no la
   tercera): cadena `sdk→cli→api→plantilla` operativa, ledger midiendo desde el día 1
   (fecha dura 19-ago), y el candidato API (Sonnet 5 vs Haiku) elegido con el juez antes
   del 31-ago, mientras dura el precio intro. El presupuesto de septiembre se decide con
   `uso-llm.jsonl`, no a ciegas.
3. **El estrangulador se estanca: dos sistemas a medias para siempre.** Es EL riesgo
   específico de este arranque (shim + espejo + panel nuevo conviviendo con el vivo
   durante 5 semanas): la tentación de pulir el panel pixel-perfect, o de dejar el cutover
   "para cuando esté todo". *Mitigación estructural:* (a) el criterio "quedó viva" de cada
   semana es un hito de PRODUCCIÓN, no de código — si no se cumple, no se avanza de
   etapa; (b) el prototipo congelado mata el scope-creep de diseño (nada nuevo se dibuja:
   ya está aprobado); (c) el gate de corte de S5 es una lista cerrada de 5 condiciones,
   no un juicio estético; (d) cada movimiento es reversible barato (shim = 1 commit;
   cutover = re-apuntar launchd; vivo congelado 30 días); (e) la regla de contingencia
   fija QUÉ cede si algo se atrasa (E3 cede, el canal jamás).

---

## 4. La muerte del prototipo y el nacimiento del panel real

**Decisión: el prototipo NO se reusa como base del panel y NO se reescribe desde cero.
Se desguaza en tres herencias distintas, y muere en dos tiempos.**

### 4.1 Las tres herencias (qué vive de él, y en qué forma)

1. **El CSS vive completo:** el `<style>` (335 líneas) ES el design system destilado de
   la ronda 6 — pasa tal cual a `panel/pwa/tokens.css` el día 1 y no se re-deriva. Los
   patrones de markup de los componentes (`.fila`, `.chip`, `.pto`, `.traza`, `.diff`,
   `.sw`, burbujas, `.prog-card`, `.correo-card`, `.decision`, `.bloque`) se copian como
   biblioteca de componentes del panel real. Razón: encarnan 18 iteraciones APROBADAS por
   Alejandro; reescribirlos reabriría conversaciones de diseño que están cerradas, contra
   la regla "cero variaciones".
2. **El JS muere entero, pero como SPEC, no como basura:** las funciones del prototipo
   (`renderLista`, `abrirChat`, `pausaHTML`, `seleccionar`, `verBorrador`…) son la
   especificación de interacción del `app.js` real — qué pinta cada vista, qué abre cada
   click, qué estados existen. El código en sí NO se porta: es pegamento de demo con
   estado hardcodeado y los 20 defectos de la auditoría lo prueban (contadores fijos,
   funciones de un solo disparo, flags que no se limpian). Portarlo importaría sus bugs;
   reescribir cada render contra la API real (que el contrato ya mapea query por query)
   es más barato que destriparlo. El `app.js` real es delgado: `fetch('/api/…')` →
   pintar en el MISMO markup heredado.
3. **La DATA muere como datos y renace como pruebas:** el bloque DATA (CHATS, CAMINOS,
   AGENTES, PAUSA, REPLAYS, DORMIDOS) se destila en §S3-4 a `data/pruebas/*.yml` y
   guiones del gimnasio — Carolina es LA prueba dorada de la Duda; Ranco, la de aprobar
   cotización; Jorge, la del seguimiento visible; El Monte, la de ingesta de foto. Así el
   panel real se acepta contra los mismos casos con que se diseñó.

### 4.2 Los dos tiempos de la muerte

- **Tiempo 1 — semana 0: muere como documento editable.** Con los arreglos P0/P1/P2
  aplicados se etiqueta **v5-congelado**, se commitea a ronda8/ y se publica como
  artifact. Desde ese momento NADIE lo edita: todo cambio de diseño que surja durante la
  construcción se hace en el panel real y, si es de sistema, en `tokens.css` + vista
  Diseño. (El prototipo deja de ser fuente de verdad de DISEÑO futuro; sigue siendo
  fuente de verdad del CONTRATO hasta el tiempo 2.)
- **Tiempo 2 — cutover S5 (25-31 ago): muere como interfaz.** El reemplazo es vista por
  vista y siempre con datos reales (S2: Módulos, Hoy, Chats/tablero — desde el espejo;
  S3-4: Caminos, Dudas, Agentes, Gimnasio; S5: ✓✓ y estados de envío). El día del
  cutover, el panel real sirve las 6 vistas + Diseño desde `bot.db` y el prototipo pasa a
  museo. La comparación de aceptación es literal: cada vista real, lado a lado con su
  vista del prototipo, debe ser pixel-comparable en tokens y jerarquía (no en datos).

### 4.3 Por qué no las alternativas

- **¿Reusar el HTML entero como base del panel (evolucionarlo in situ)?** No: su JS es
  simulación de un solo recorrido (estado global de demo, funciones one-shot), no separa
  datos de render, y el panel real necesita PWA/manifest/sw/push y rutas de API que el
  prototipo no tiene. El costo de "limpiarlo" supera al de reescribir el JS delgado
  sobre el mismo markup — y dejaría el pecado original del Frankenstein en el proyecto
  que nació justamente para no heredarlo.
- **¿Reescribir todo sobre el design system "de cero"?** No: regenerar CSS/markup desde
  la spec r6 produciría una segunda interpretación del mismo diseño (variaciones — lo
  prohibido) y botaría el único artefacto que Alejandro ya aprobó visualmente. El CSS del
  prototipo ES la spec r6 compilada; se hereda como órgano sano, igual que `enviar.js`.
- La decisión es coherente con el principio del dueño: **el proyecto nace de cero, y los
  órganos sanos se trasplantan como archivos escogidos** — del bot vivo se trasplantan
  emisor/outbox/gating/extractor; del prototipo se trasplantan el CSS, los componentes y
  los personajes. El JS de ambos muere.

---

## Fuentes

- `scratchpad/informes8/esqueleto-proyecto.md` (árbol [D1]-[S5], contratos v2, trasplantes)
- `scratchpad/informes8/auditoria-funcional-prototipo.md` (los 20 arreglos, patrón raíz `recontar()`)
- `scratchpad/informes8/contrato-backend.md` (entidades/eventos/queries, gaps G1-G25, los 5 bloqueantes)
- `ronda2/plan-revisado.md` + `DIXDYBOT-ESTADO.md` (E0-E7 vigente, fechas duras, ajustes ronda 3)
- `ronda5/blueprint-fundacional.md` §7 (calendario S0-S5, gate de corte, 16 NOes)
- `ronda7-gapcheck/matriz-vision-prototipo.md` (brechas que se resuelven en el panel real)
- `ronda6-diseno/design-system-dixdy.md` + memoria `dixdybot-design-system` (Claude Design/DesignSync)
- `scratchpad/dixdybot-prototipo.html` v4 completo (DATA L760-861, funciones L863-1365, NOTAS)
