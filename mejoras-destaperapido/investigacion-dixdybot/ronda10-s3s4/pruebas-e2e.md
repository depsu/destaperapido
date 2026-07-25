# Pruebas E2E — dixdybot (molde) contra la instancia destaperapido

**Fecha:** 2026-07-24
**Rol:** agente de pruebas permanente. Ejercí de verdad lo funcional (S0–S4) como operador real.
**Molde:** `/Users/alejandroriveracarrasco/SaSS/DIXDY/dixdybot`
**Instancia (datos del clon):** `/Users/alejandroriveracarrasco/SaSS/destaperapido/dixdybot-data`
**Bot vivo (solo lectura, candado):** `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/data`

**Veredicto global: VERDE.** Todos los flujos PASAN end-to-end. No toqué el proceso del bot vivo,
no hice git, y dejé la instancia en su estado original (ajustes restaurados, `caminos-propuestos.json`
idéntico, server apagado limpio).

---

## 1 · Verificadores del molde — PASA

```
$ pnpm exec tsc --noEmit
tsc_exit=0

$ pnpm exec vitest run
 Test Files  23 passed (23)
      Tests  304 passed (304)
```

Ambos verdes. Node v22.18.0 (type stripping, `.ts` directo). Sin cambios de código en el repo
(no hubo bug que arreglar; ver §5).

`$ node cli/doctor.ts` (RUTA_DATOS = instancia) → **todo [OK]**: node, 5 deps runtime, 6 tablas
núcleo + migraciones, 10 módulos con manifest/defaults válidos, bot.db abre (esquema v1), los 3
ajustes presentes válidos (rampa, cotizador, panel), resto corre con defaults. "Diagnóstico: todo en orden."

---

## 2 · Panel end-to-end (curl) — PASA

Arranqué el proceso real (`node src/index.ts --datos <instancia>`), puerto 8793 (libre, el de
`panel.json`). Un solo proceso; monta bot + panel Hono + PWA. Apagado limpio con SIGTERM al final.

| Endpoint | Resultado | Evidencia |
|---|---|---|
| `GET /api/salud` | PASA | `{"ok":true,"negocio":"destaperapido","modulos":10,"db":{"conversaciones":184,"mensajes":3820,"pedidos":20,"dudas":0}}` |
| `GET /api/hoy` | PASA | métricas compuestas SOLO de aportes activos: `pedidos-en-juego-hoy=$2.370.001 (20 pedidos abiertos)` · `cotizaciones-hoy`. contadores `{pendientes:0, chatsActivos:108, dormidos:76}` |
| `GET /api/chats` | PASA | `dudas:0 activos:100 dormidos:30 totalDormidos:76 total:184` |
| `GET /api/chats?q=Montaje` | PASA | 11 resultados (JB Montaje Industrial, …); búsqueda LIKE cruza bautizo/contenido |
| `GET /api/chats?q=zzzznoexiste` | PASA | `0` en todas las secciones (sin romper) |
| `GET /api/chats/:id` (real) | PASA | hilo con 24 mensajes; ficha compuesta por secciones (Cotización→Comuna, Pedido→Etapa/Monto neto, Otros datos); `accion:"Ver pedido"` |
| `GET /api/chats/no-existe-jamas` | PASA | `{"error":"ese chat no existe"}` **HTTP 404** |
| `GET /api/tablero` | PASA | `activo:true`, 4 columnas del embudo (Cotizando 13 / Por confirmar 1 / Por entregar 6 / Cobrado 0), huérfanos 0 |
| `GET/PUT /api/modulos` | PASA | ver §3 |

---

## 3 · Administrabilidad servida por API (el criterio #1 del dueño) — PASA

### 3a · Rampa: cambiar el límite Y activar/desactivar → el aporte aparece/desaparece
- Baseline (rampa `activo:false`): `/api/hoy` métricas = `pedidos-en-juego-hoy, cotizaciones-hoy` (sin leads).
- `PUT /api/modulos/rampa {activo:true, limite_diario:50}` → **HTTP 200**. `/api/hoy` ahora incluye
  `leads-atendidos-hoy = "leads atendidos 0/50"` (el **50** viene del ajuste, cero código). El archivo
  en disco quedó con `limite_diario:50, activo:true`.
- `PUT /api/modulos {id:"rampa", config:{activo:false,…}}` (la variante del contrato) → **HTTP 200**.
  `/api/hoy` vuelve a `pedidos-en-juego-hoy, cotizaciones-hoy`: **el aporte desapareció solo**.

### 3b · Embudo: apagar un módulo limpia el panel solo
- `PUT /api/modulos/embudo` con su config completa y `activo:false` → **HTTP 200**.
  `/api/hoy` pierde el hero `pedidos-en-juego-hoy` (queda solo `cotizaciones-hoy`); `/api/tablero`
  responde `{activo:false, columnas:0}`. Al restaurar → tablero vuelve con sus 4 columnas.

### 3c · Cerebro / Dudas / Cotizador / Caminos — administrables por PUT
- `PUT cerebro {cadena, modeloCli:"opus"}` → 200; readback `modeloCli:"opus"` (config leída por turno).
- `PUT dudas {…, escalada_min:7}` → 200; readback `escalada_min:7`.
- `PUT cotizador` (toggle `mostrar_neto`) → 200; readback `mostrar_neto:false`.
- Los 10 módulos exponen `schema` (JSON Schema desde el `configSchema` Zod) para dibujar Ajustes.

**Checklist #1 (configSchema · ajustes sin tocar código · aporte declarado · dos ajustes→dos conductas):
demostrado en vivo por API** (rampa y embudo), y por vitest (`consultar.test.ts`, `arranque.test.ts`,
`gimnasio.test.ts`).

---

## 4 · CLIs y motores S3–S4 — PASA

| Herramienta | Modo | Resultado |
|---|---|---|
| `cli/destilar-caminos.ts` | `--dry-run` (lee vivo real) | PASA · `68 aprendizajes activos · 3920 líneas de chat · 3 trozos · prompt trozo 1 ≈ 9037 chars`. Candado solo-lectura del vivo OK; no llama al modelo. |
| `cli/sombra.ts` | `--dry-run --aperturas` | PASA · `539 pares cliente→bot · muestra 6 · persona 168 chars`. Reconstruye pares reales sin tocar el modelo. |
| Motor de la Duda junior→senior | script contra `src/core/duda-motor.ts` | PASA (15/15). Ver abajo. |
| Gimnasio (persona guionada) | script contra `src/gimnasio/personas.ts` + `crearLlm` real | PASA (7/7). Ver abajo. |

**Duda — pausa completa junior→senior (motor real, `duda-e2e.mjs`):**
`abrirDuda` (falta_camino→pendiente, código relay `abcde`) → `responder("cobrale 150", costo 180)`
→ **evaluando** con contra-argumento sobre datos reales ("Buin va a 200 … Con 150 quedamos bajo el
costo. Yo diría 200. Tú decides.") → `decidir("190 c/u, flete incluido")` → **check1_listo** (cliente
respondido al tiro) → `afinar` → **check2_afinando** → `resumir` (a-ver-si-entendí) →
`caminoDesdeResumen` (nace **borrador/aprendido**, cero cifras en el cuerpo) → `confirmar` con pruebas
pasando → **camino ACTIVO** y duda **resuelta**. Candado verificado: con la prueba FALLANDO el camino
NO se activa (sigue borrador). Relay WhatsApp: `parseCodigoRelay("si abcde 190 cada uno")` → código
`abcde` + resto "190 cada uno"; "Perfecto"→confirmar, "cambia"→seguir.

**Gimnasio (persona guionada real, `gimnasio-e2e.mjs`):** persona **Regateador** (4 líneas) inyectada
por el canal `sim` contra el agente real (`agenteDeLlm` sobre la puerta única `crearLlm`); las 4 líneas
entraron, el agente respondió cada turno (4 globos), el transcript intercala cliente→bot, y la puerta
avisó al dueño en cada respuesta de plantilla (4 avisos). El **juez** (llm inyectado, como el test) con
nota 4,5: **aprueba con gate 4 y NO con gate 5** → el gate es administrable. *Nota de método:* usé el
motor `plantilla` (determinista) para no spawnear `claude -p` anidado; la puerta única y toda la máquina
del gimnasio/sombra son las mismas. La corrida con modelo real queda tras el gate del juez (fuera de
vitest por doctrina, S3-4) y tras `claude` disponible.

---

## 5 · Casos borde de operador — PASA

| Caso | Esperado | Resultado |
|---|---|---|
| `PUT cotizador {activo:"si", tarifario:123}` (tipos inválidos) | 400 sin corromper | **HTTP 400** "…activo: expected boolean, received string…"; disco intacto (`zonas:6`) |
| `PUT embudo {activo:false}` (parcial, faltan required) | 400 sin corromper | **HTTP 400** "etapas/etapa_inicial/transiciones: expected…, received undefined"; no se escribió nada |
| `PUT rampa '{no es json'` (cuerpo roto) | 400 | **HTTP 400** "el cuerpo no es JSON válido" |
| `PUT /api/modulos/inventado` (módulo inexistente) | 404 | **HTTP 404** "no existe el módulo 'inventado'" |
| Buscar `?q=zzzznoexiste` | vacío sin romper | 0 resultados |
| `GET /api/chats/no-existe-jamas` | 404 | **HTTP 404** "ese chat no existe" |
| Apagar un módulo NÚCLEO (`PUT cerebro {activo:false}`) | debe impedirlo | **Impedido**: HTTP 200 pero Zod **descarta** la llave `activo` (no queda en la config) y `estaActivo` fuerza `true` para núcleo → cerebro **sigue activo**. El núcleo no se puede apagar. |

---

## 6 · Observaciones (no bloqueantes, no son bugs)

1. **Ficha con embudo apagado:** al apagar `embudo`, el hero de plata y el tablero desaparecen (aportes
   declarados), pero la sección **"Pedido"** (Etapa/Monto) sigue apareciendo en `/api/chats/:id` cuando el
   pedido existe. Es intencional en `componerFicha` (la sección Pedido se arma directo del `pedido`, no es
   un `camposFicha` declarado por embudo; el nombre de etapa sí cae al id crudo cuando falta la config).
   No viola el contrato de aportes; lo dejo anotado por si el dueño quiere que apagar embudo también oculte
   esa sección.
2. **Apagar núcleo es silencioso:** el impedimento es efectivo (el módulo sigue activo), pero el PUT con
   `activo:false` responde 200 y descarta la llave en vez de avisar "el núcleo no se apaga". Funcional y
   sin riesgo; el aviso explícito sería una mejora de UX del panel.

Ninguna de las dos rompe un flujo → no cambié código (tsc/vitest ya verdes, sin bug real que arreglar).

---

## 7 · Higiene (dejé todo como estaba)

- Ajustes de la instancia **restaurados** desde snapshot: quedan solo `cotizador.json`, `panel.json`,
  `rampa.json` (rampa `activo:false, limite_diario:25`; cotizador `mostrar_neto:true`); borré los
  `cerebro/dudas/embudo.json` que crearon mis PUTs.
- `caminos-propuestos.json` **idéntico** al inicio (los dry-run no escriben).
- Bot vivo **intacto** (los CLIs solo lo leen con candado realpath; no toqué su proceso).
- Server del panel **apagado limpio** (puerto 8793 liberado). Sin git.
