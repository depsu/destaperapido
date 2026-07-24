# Flujos del motor — dónde viven las etapas y quién mueve los pedidos (ronda 7)

**Pregunta del dueño:** "la definición de las etapas del tablero debe vivir en alguna
parte" y "¿cómo un camino decide mover un pedido a la siguiente etapa?". Respuesta
canónica con el blueprint (contratos §4, 5 tablas, eventos.jsonl, efectos) + brechas de
flujos + interacciones mínimas para el prototipo.

---

## 1. Respuesta canónica

### 1.1 Las etapas son DATOS del módulo Embudo (por negocio)

El Embudo es un módulo más del contrato `Modulo` (§4.5 del blueprint): `manifest` +
`configSchema` Zod + `configDefault`. La instancia vive en **`data/ajustes/embudo.json`
del clon** — cada rubro define sus columnas ahí, el panel las dibuja desde
`z.toJSONSchema()`, y editarlas es el mismo patrón diff+Aprobar de los caminos
("agrega la etapa Visita técnica entre Cotizando y Por confirmar" → antes/después →
Publicar → commit en el git del clon).

Schema concreto (`modulos/embudo/schema.ts`):

```ts
export const Etapa = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/),       // 'cotizando', 'por-confirmar'…
  nombre: z.string(),                          // el título de la columna
  tipo: z.enum(['abierta', 'ganada', 'perdida']),  // semántica terminal → métricas
  orden: z.number().int(),
  requiere: z.array(z.string()).default([]),   // datos de ficha exigidos al ENTRAR
                                               //   p.ej. por-entregar requiere ['fecha_entrega']
  limite_horas: z.number().nullable().default(null), // SLA: punto ámbar si se pasa
});

export const ConfigEmbudo = z.object({
  activo: z.boolean().default(true),
  etapas: z.array(Etapa).min(2),
  etapa_inicial: z.string(),
  transiciones: z.array(z.object({
    de: z.string(), a: z.string(),
    origenes: z.array(z.enum(['camino', 'dueno', 'externo'])).min(1),
  })),
  cobrado_cuando: z.enum(['total', 'primer_abono']).default('total'),  // regla de cobro parcial
  perdido_por_silencio_dias: z.number().nullable().default(null),      // propuesta automática, no auto-move
});
```

Default de destaperapido: `cotizando → por-confirmar → por-entregar → cobrado` +
`perdido` (tipo 'perdida'). El Kanban actual de 4 columnas ES este JSON con otra ropa.

### 1.2 Brecha del blueprint: falta la entidad "pedido" (6ª tabla)

Las 5 tablas modelan conversaciones, no negocios: el tablero muestra **pedidos** y hoy no
tienen dónde vivir (un contacto que repite compra rompería `conversaciones.estado`).
Propuesta: tabla `pedidos` aportada por el módulo Embudo (migración propia, escrita SOLO
vía `escritor.ts`):

```sql
CREATE TABLE pedidos (
  id TEXT PRIMARY KEY,                -- 'p-218'
  conversacion_id INTEGER REFERENCES conversaciones(id),  -- NULL = pedido manual sin chat
  contacto_id INTEGER REFERENCES contactos(id),
  etapa TEXT NOT NULL,                -- estado ACTUAL materializado; la historia va al ledger
  monto_neto INTEGER, saldo INTEGER,
  datos TEXT NOT NULL DEFAULT '{}',   -- ficha JSON (fechas, comuna, ítems)
  motivo_cierre TEXT,                 -- obligatorio si etapa tipo 'perdida'
  creado_ts INTEGER NOT NULL, actualizado_ts INTEGER NOT NULL
);
```

La verdad del "por qué está aquí" NO es la columna `etapa`: es **eventos.jsonl** (event
sourcing liviano — SQLite guarda el presente, el ledger guarda la historia).

### 1.3 Transiciones = EVENTOS con 3 orígenes y UNA sola vía de escritura

`escritor.ts` expone la única puerta: `moverPedido(pedidoId, a, origen, porque)` que
(1) valida contra `ConfigEmbudo.transiciones` — de→a permitido Y el origen habilitado;
(2) valida `requiere` de la etapa destino contra la ficha; (3) actualiza `pedidos.etapa`;
(4) apendea el evento al ledger; (5) emite al bus (panel/tablero al día, y el hilo gana
una píldora de actividad). Inválido = rechazo + evento `pedido.movimiento_rechazado` +
aviso. **Nadie más escribe `etapa`**: ni el camino, ni el panel, ni el poller de Supabase.

Nombres canónicos de eventos (eventos.jsonl):

| Evento | Cuándo |
|---|---|
| `pedido.creado` | efecto `crear_pedido` de un camino (cotización generada) o alta manual del dueño |
| `pedido.movido` | de→a con `origen` + `porque` (el evento estrella) |
| `pedido.actualizado` | cambia ficha/monto/fecha SIN cambiar etapa (reagendar) |
| `pedido.cobro_registrado` | monto + medio + saldo restante (cobro parcial = N eventos) |
| `pedido.reabierto` | de etapa 'perdida' vuelve a abierta (cliente resucita) |
| `pedido.movimiento_rechazado` | intento inválido — combustible del lint y de avisos |

Forma del origen (discriminada, Zod):

```jsonl
{"tipo":"pedido.movido","ts":…,"pedidoId":"p-218","convId":"wa-baileys:5691…",
 "de":"cotizando","a":"por-confirmar",
 "origen":{"clase":"camino","caminoId":"confirmar-pedido","pasoId":"cierre","turnoRef":"…"},
 "porque":"el cliente confirmó 30+1 y entregó correo"}
```

- `{clase:'camino', caminoId, pasoId, turnoRef}` — efecto de un paso completado.
- `{clase:'dueno', via:'panel'|'whatsapp', gesto:'arrastre'|'boton'|'codigo'}` — arrastre
  en el tablero, botón Aprobar, o "si abcde" por WhatsApp.
- `{clase:'externo', fuente:'repartidor-supabase'|'webhook-pago'|'timeout', ref}` — el
  poller que ya lee Supabase traduce "entregado/cobrado" del repartidor a `moverPedido`.

### 1.4 Cómo un camino mueve un pedido: EFECTOS del paso, nunca el LLM

Agregar al `Paso` del schema de camino (§4.3):

```ts
efectos: z.array(z.object({
  tipo: z.enum(['crear_pedido', 'mover_pedido', 'registrar_cobro',
                'programar_seguimiento', 'avisar_dueno']),
  a: z.string().optional(),            // etapa destino (mover_pedido)
})).default([])
```

Flujo por turno: el **evaluador** (1 llamada LLM) devuelve `paso_completado: true` → el
**resolver** (determinista, gratis) recoge los `efectos` del paso completado → cada
efecto llama a `escritor.moverPedido(...)` → evento + traza. Doctrina idéntica a "cifras
del tarifario, nunca del modelo": **el LLM solo declara que el paso terminó; el
movimiento es un efecto determinista de DATOS, validado contra la tabla de transiciones.**

`lint.ts` cierra el círculo en las dos direcciones: al guardar un camino, todo
`mover_pedido` debe apuntar a una etapa existente con transición `origen: camino`
permitida; al editar `embudo.json` (borrar/renombrar etapa), lint inverso: qué caminos la
referencian y qué pedidos están parados ahí → bloquear o proponer remapeo (decisión del
dueño, mismo patrón diff).

### 1.5 El paso extra de la traza

A la traza del turno ("Recepción → Sofía / Datos completos / 3 caminos / Cifra del
tarifario / Respondió") se agrega el paso **Efecto**:

> ⚙ **Pedido → Por confirmar** — lo movió el paso "cierre" del camino *Confirmar pedido*;
> transición permitida por el embudo.

Y cada tarjeta del tablero responde su propio "¿por qué está aquí?" con el último
`pedido.movido` (mini-traza de 3 líneas: quién, cuándo, porqué). Las transiciones de
origen dueño/externo aparecen además como píldora de actividad EN el hilo ("·· el
repartidor marcó entregado — pedido → Cobrado ··"): el chat y el tablero cuentan la misma
historia desde el mismo ledger.

---

## 2. Flujos de negocio que el prototipo aún no muestra (priorizados)

1. **Perder un pedido** — no existe columna ni gesto "Perdido"; sin él, el embudo miente
   (el % de cierre por camino necesita los perdidos). Necesita: etapa terminal con
   `motivo` obligatorio (precio/silencio/otro, 1 toque); efecto `mover_pedido` a perdido
   desde el camino de objeciones; y el módulo Seguimiento PROPONE "perdido por silencio"
   a los N días (el dueño confirma — nunca auto-move silencioso).
2. **Handoff humano→bot de vuelta** — hay "Tomar" pero no "Devolver a Sofía". Necesita:
   botón Devolver en el header del hilo cuando `asignado=humano`, evento
   `conversacion.asignada` con origen, y píldora en el hilo; Sofía retoma leyendo lo que
   el humano escribió (ya está en el mismo hilo — sin mecanismo extra).
3. **Chat que no es venta** — número equivocado, proveedor, reclamo. Canónico: el pedido
   nace SOLO con el efecto `crear_pedido` → un chat sin pedido jamás ensucia el tablero.
   El prototipo debería mostrar un chat en la lista que no tiene tarjeta en el tablero.
4. **Cobro parcial** — 50% de anticipo es normal en el rubro (el Ranco de $2,48M lo
   tendría). `pedido.cobro_registrado` ×N + `saldo`; tarjeta muestra "$1,24M de $2,48M";
   `cobrado_cuando` decide la columna.
5. **Reagendar / actualizar entrega** — ya existe en el bot vivo (modo Actualización) y
   el prototipo no lo muestra: `pedido.actualizado` + píldora + repartidor re-avisado.
   Demuestra que no todo evento de negocio es un cambio de columna.
6. **Pedido sin chat** (llamada/persona) — alta manual en el tablero, origen dueño,
   tarjeta sin conversación vinculada. Anotar, puede esperar.
7. **Contacto que repite** — 2º pedido del mismo cliente; lo resuelve la tabla `pedidos`
   (1.2); la Ficha del contexto gana "Pedidos anteriores · n".

---

## 3. Interacciones mínimas para validar con el dueño (sin abrumar)

**Núcleo (3 — responden SU pregunta):**

1. **Tarjeta del tablero → "¿Por qué está aquí?"**: click muestra mini-traza del último
   `pedido.movido` ("Movido por el paso 'cierre' del camino Confirmar pedido — 'confirmó
   30+1 y dio correo' — 10:47"). Valida: cada movimiento tiene origen y porqué.
2. **Traza del turno con el paso Efecto** (agregar 1 paso al `porQue('precio')`
   existente): "⚙ Pedido → Por confirmar — lo movió el paso del camino; el embudo lo
   permite". Valida: cómo un camino mueve un pedido, en sus palabras.
3. **Mover a mano con transiciones acotadas**: click en tarjeta → menú con SOLO las
   etapas permitidas + "Perdido…" (pide motivo en 1 toque) → toast "quedó anotado
   también en el chat". Valida: gesto del dueño = misma vía, y el flujo perder.

**Segunda pasada (3):**

4. **Píldora externa en el hilo**: "·· el repartidor marcó entregado — pedido →
   Cobrado ··" clickeable → origen externo (Supabase). Valida el 3er origen.
5. **Fila Embudo en Módulos**: expandir muestra las etapas como lista editable
   ("Cotizando · Por confirmar · Por entregar · Cobrado · Perdido" + [+ Etapa]) — la
   prueba visible de que "la definición vive en alguna parte" y es suya.
6. **Devolver a Sofía**: botón en el header del hilo tras "Tomar" + píldora "·· dejaste
   el chat con Sofía ··".

La edición conversacional del embudo ("agrega Visita técnica") NO necesita UI nueva: es
el mismo chat-IA + diff + Publicar que el prototipo ya muestra para caminos.
