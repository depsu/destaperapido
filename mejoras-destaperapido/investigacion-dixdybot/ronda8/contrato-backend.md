# EL CONTRATO DEL BACKEND — dixdybot (ronda 8)

**Fecha: 24-jul-2026 · Fuente primaria: `scratchpad/dixdybot-prototipo.html` (bloque DATA
L760-861 + funciones L863-1365, 18 iteraciones con Alejandro) · Se reconcilia con:**
blueprint ronda5 (§4 contratos, §4.4 cinco tablas), planos ronda4 (esquema chatwoot +
disciplina nanoclaw), ronda7 (`flujos-motor-embudo.md` = 6ª tabla `pedidos` + eventos;
`auditoria-modularidad.md` = brecha `aportes`), y las 5 memorias `project_dixdybot-*`.

**Regla de oro:** el prototipo ES el contrato de consumo. Construir el motor = servir las
entidades de §1 y ejecutar los eventos de §2 de modo que las queries de §3 devuelvan
exactamente lo que el HTML hoy saca de `CHATS/CAMINOS/AGENTES/PAUSA/DORMIDOS/REPLAYS`.
El comentario del propio prototipo lo fija (L759): *"DATA SIMULADA — al construir el
backend, solo cambia esta fuente"*. Nada de §1-§3 es opcional; §4 dice dónde vive cada
cosa y qué falta en el plano de datos (GAPS numerados G1-G22).

Convención: los nombres de campo citan el prototipo (`nom`, `prev`, `espera`…) y se
mapean al nombre canónico del almacén en §4. Tipos en notación Zod-like. `⚠ GAP-Gn`
marca lo que el plano de datos vigente aún no modela.

---

## 1. ENTIDADES (tal como el panel las consume)

### 1.1 Conversación (`CHATS[id]`, L760-827; render L879-925)

```
Conversacion {
  id: string                      // slug del prototipo; real: conv_id `canal:idNativo`
  nom: string                     // BAUTIZO: "Carolina · Melipilla" / "Constructora Ranco"
                                  //   — la fila se renombra sola apenas el extractor sabe
                                  //   nombre+comuna+pedido (memoria flujo-chats §1a)
  ini: string(1)                  // derivado de nom (avatar)
  sub: string                     // "WhatsApp · Estación Central · Sofía" =
                                  //   canal.nombre + ficha.comuna + agente.nom  ⚠ GAP-G1 (agente)
  chip: [claseCss, texto]         // clase: 'vivo'|'draft'; texto de estado libre:
                                  //   'confirmó'|'tema en pausa'|'cotizando'|'cerrado'|'por entregar'
  noleido: boolean                // ⚠ GAP-G2 (sin campo visto_por_dueno)
  hra: string                     // ts del último mensaje, formateado relativo ('10:42'|'ayer'|'lun')
  prev: string                    // preview BAUTIZADA del último evento relevante; puede ser:
                                  //   texto, '🎤 0:41 · "…transcripción…"', '📷 · qué respondió',
                                  //   '⏰ seguimiento vie 10:00 · …', o estado ('precio en pausa')
  pto: 'ok'|'esp'|'' + ptip       // punto de estado con tooltip ('Confirmó'|'Resuélvelo en Hoy')
  espera: boolean                 // true → sección "Dudas del bot — necesita tu respuesta" (L893)
  tags: ('grande'|'nuevo'|'urgente')[]  // AUTOMÁTICAS, nunca manuales (grande = monto > umbral)  ⚠ GAP-G3
  accion: string                  // CTA contextual del composer: 'Aprobar cotización'|'Ir a la
                                  //   pausa'|'Ofrecer cotización'|'Reabrir'|'Ver entrega' — derivada
                                  //   del estado (duda viva > pedido esperando OK > pedido en etapa > cerrado)
  correoEnviado: boolean          // dedup del envío de cotización (L1077)
  msgs: Mensaje[]                 // §1.2
  ficha: [seccion: string, [k,v][]][]   // §1.9 — secciones dinámicas: Ficha / Cotización /
                                  //   Potencial / Historial / Seguimiento / Entrega
}
```

**Dormida** (`DORMIDOS` L936-941 + reglas L952): `{ini, nom, razon ('cotizó 1 día, no
respondió · seguimiento agotado'), antiguedad ('12 días')}`. Reglas fijadas: duermen solas
a los **7 días sin actividad ni pendientes (configurable)**; siguen en el buscador;
**despiertan solas arriba con todo su historial si el cliente escribe**. Mapea a
`conversaciones.estado='dormida'` + `snoozed_until` (ya modelado) — la *razón* del sueño
es texto derivado del último evento.

### 1.2 Mensaje (unión discriminada — L763-826, render L906-916)

Siete formas en el hilo; las cinco primeras son mensajes, las dos últimas son
**proyecciones de otras entidades** dentro del hilo:

| Forma | Campos | Notas de consumo |
|---|---|---|
| `cli` | `{de:'cli', t, anota?}` | burbuja gris izq.; `anota` = anotación de ingesta (`<b>Transcrita:</b>…` / `<b>Vista:</b>…`) bajo la burbuja |
| `bot` | `{de:'bot', t, anota?, traza?, ens?}` | burbuja verde der.; click → traza §1.10 (`traza` = ref del turno ⚠ GAP-G9); hover → 💡 enseñar; `ens` = regla enseñada mostrada bajo la burbuja; ✓✓ real inline (estado de entrega) |
| `tu` | `{de:'tu', t}` | burbuja azul der. — habló un humano (rol por color, sin etiquetas) |
| `sys` | `{de:'sys', t, tema?}` | píldora centrada; `tema:true` → ámbar clickeable a la traza de la pausa |
| `correo` | `{correo:true, asunto, estado}` | tarjeta de correo EN el hilo de WhatsApp ('Cotización N°1042…' + 'enviada a… · PDF adjunto · te aviso cuando la abran') ⚠ GAP-G7 |
| `prog` | `{prog:true, cuando, t}` | mensaje PROGRAMADO aún no enviado (borde punteado ámbar, 'se enviará el viernes 26 · 10:00') con acciones Editar (hasta esa hora) y Cancelar ⚠ GAP-G6 |
| `pausaWidget` | `{de:'sys', pausaWidget:true}` | proyección del objeto Duda §1.3 — MISMO estado que la tarjeta de Hoy, renderizado in situ (L907, L1020) |

Regla del blueprint que el prototipo confirma: el texto de un media es placeholder hasta
que la anotación lo reemplaza; el panel muestra el original ('🎤 Nota de voz · 0:41') MÁS
la anotación — o sea la anotación NO pisa el texto, se adjunta (`anota` aparte).

### 1.3 Duda / Pausa junior→senior (`PAUSA` L1019-1062 + memoria pausa-junior-senior)

**Un solo estado, dos proyecciones** (tarjeta en Hoy + widget en su chat — `pausaHTML(ctx)`
pinta ambos del mismo objeto). Máquina de estados:

```
Duda {
  id, convId, agenteId
  fase: 'pendiente' | 'evaluando' | 'checks' | 'resuelta'
  resumen: {                       // junior→senior: el dueño NO lee el chat
    quien: 'Carolina · Melipilla', que: '5 baños mensuales para una obra',
    potencial: 'sobre $1M al mes', falta: 'precio para 5 baños en zona lejana'
  }
  mientras: 'ella junta dirección y fechas'   // el chat SIGUE, solo el tema se pausa
  hilo: [{de:'dueno'|'agente', t}]  // la mini-conversación: respuesta del dueño →
                                    //   contra-argumento CON DATOS ('Buin va a $200.000 y el
                                    //   flete es mayor… yo diría $190.000') → decisión final
  check1: {hecho: bool, detalle}    // ✓ cliente respondido AL TIRO con la decisión
  check2: {hecho: bool, pregunta, opciones}  // afinar el camino con calma (alcance:
                                    //   'Todo el tramo Melipilla' | 'Solo Melipilla')
  decision: {valor, origen: 'propuesta_agente'|'impuesta_dueno'}
  caminoCreado?: caminoId           // al resolver: camino origen:'aprendido', 0 usos,
                                    //   'nació de la pausa de hoy', con pruebas
}
```
⚠ GAP-G19: el `SnapshotSuspendido` del blueprint (schemas/pausa.ts) es de UNA vuelta;
esta entidad exige fase + hilo + 2 checks separados + resumen estructurado.

### 1.4 Decisión (vista Hoy, L364-394 + `resolverDecision` L1065-1074)

Cola unificada de lo que espera al dueño. Tres tipos hoy (extensible por módulo —
`tiposDecision` de la brecha `aportes`):

- **pausa**: proyección de Duda §1.3, con input inline.
- **aprobación**: `{cliente, pedido ('30 baños + 1 accesible'), lugar, fechas, monto
  ('cotización lista · $2.480.000 neto'), acciones: Ver (abre el chat) | Aprobar}`.
- **borrador**: `{chip:'borrador', titulo ('Precios céntricos +10%'), meta ('4 caminos ·
  pruebas OK · lo pediste anoche'), accion: revisar → pop de diffs}`.

**Resuelta**: `{titulo, meta (hora/detalle)}` — colapsan en "Resueltas hoy · n";
el badge del sidebar = COUNT(pendientes). ⚠ GAP-G20 (entidad/query no modelada).

### 1.5 Camino (`CAMINOS` L830-840; cascada L477-493; peek L1229-1254)

```
Camino {
  id, t: string                    // título ('Mensual céntrico · 1 baño', '"Me lo dejan más barato"')
  estado: 'vivo'|'nuevo'           // real: borrador|activo|retirado + origen manual|aprendido
                                   //   ('nuevo' = aprendido + reciente, badge)
  grupo: string                    // 'Precios céntricos'|'Zonas lejanas'|'Cierre y objeciones'
                                   //   — agrupación de la cascada, con contador  ⚠ GAP-G11
  dominio/agenteId                 // tab de la vista ('Sofía · 34' / 'Destapes · 12')
  cuando: string                   // condición en simple (bloque .cuando)
  accion: string                   // acción con la CIFRA RENDERIZADA del tarifario
                                   //   ('$160.000 neto · limpieza semanal') — la cifra es
                                   //   render del módulo Precios, NO texto del camino
  stats: {usos, cierrePct, plataMes, alerta?}  // '34 usos · 52% cierre · $960 mil jul';
                                   //   '20% ⚠ revisar' — cierre bajo dispara sugerencia  ⚠ GAP-G12
  kv: [k,v][]                      // el peek: Cuando / Entonces / Requiere / Cifra ('del
                                   //   tarifario, nunca del modelo') / Conectado ('no puede
                                   //   contradecir a…' = relación) / Regla tuya / Gana sobre
                                   //   (prioridad_sobre) / Nació de / Uso / Sugerencia
  pruebas: {n, resultados: [{nombre, veredicto}]}   // 'Pruebas 5/5 ✓ · ver cuáles' —
                                   //   doradas POR camino, se re-juegan en cada cambio;
                                   //   'si un cambio rompe una prueba, el borrador no puede
                                   //   publicarse' (L1245)  ⚠ GAP-G15
  hist: [{fecha, evento}]          // versiones: 'creado — destilado de tus 68 reglas' /
                                   //   'editado: + "limpieza incluida" (tuyo)' / 'borrador
                                   //   +10% pendiente'; Deshacer → versión anterior COMO
                                   //   BORRADOR (L1252)  ⚠ GAP-G13
}
```

### 1.6 Borrador / changeset (pop L718-731, `publicarBorrador` L1274-1289)

Entidad propia, NO un estado del camino: un cambio que toca **N caminos a la vez**.

```
Borrador {
  id, titulo: 'Precios céntricos +10%'
  origen: 'lo pediste anoche' (chat-IA) | pausa | sugerencia
  caminosTocados: [caminoId]           // 4
  diffs: [{caminoId, antes, despues}]  // 'mensual 1 baño — $160.000' → '$176.000'
  pruebas: {corridas: 12, ok: true, choques: 0}   // CANDADO: rompe una dorada → no publicable
  estado: 'pendiente'|'publicado'|'descartado'
}
```
Publicar = aplicar diffs + `hist.push('publicado: +10% (pedido por chat)')` por camino +
chip 'publicado 10:58'; 'queda en el historial · deshacer restaura como borrador'.
Descartar = 'todo sigue como estaba'. ⚠ GAP-G14.

### 1.7 Agente (`AGENTES` L842-853 + madre L733-742 + `verAgente` L1292-1315)

```
Agente {
  id, nom ('Sofía'), ini, avaStyle
  dom: 'arriendo de baños químicos · desde el 6 jul'   // dominio + fecha de alta
  chip: ['vivo','activa'] | ['draft','practicando']
  mets: [ [valor, label] ×4 ]      // activa:      caminos · nota juez · % cierre · costo hoy ($0)
                                   // practicando: caminos · nota juez · '— sin clientes' · gate ('4,0 para activar')
  presets: [{nombre, desc}]        // personalidad: 'Cercana — sin emojis, trato de usted' /
                                   //   'Precio con confianza' / 'Nunca inventa — cifras solo del tarifario'
  ejemplo: string                  // 'Así suena: "El mensual en Maipú queda en 160mil…"'
  practica: [{estado:'ok'|'esp', titulo, resultado ('5/6 ✓'|'revisar'|'3,2 — practicando'), replayId}]
  gate: 4.0                        // 'se activa solo cuando pase 4,0 (mismo listón que pasó Sofía)'
}
```
⚠ GAP-G16 (sin almacén de agente); costo-hoy exige `agente` en el ledger uso-llm ⚠ GAP-G18.

**IA madre / Recepción** (`pop-madre`): `{atendidosHoy: 7, dudas: 0}` + sus 3 reglas
(obvio → directo sin pensar, por señales, gratis, 0 s; "hola" pelado → saludo neutro y
deriva con la primera señal; ambiguo → UNA aclaración) + invariante: el cliente nunca lo
nota — mismo número, mismo hilo, solo cambia la mochila de caminos, y queda en la traza.

**Replay / corrida del gimnasio** (`REPLAYS` L855-861): `{id, t, guion: [burbujas],
juez: {estrellas|⚠, veredicto con evidencia}, sugerencia?: {texto, cta: 'Crear ese
camino' → guia('nuevo')}}`. ⚠ GAP-G17 (corridas sin almacén).

### 1.8 Pedido y Etapa (tablero L412-428 + `pop-etapas` L744-755)

```
TarjetaPedido {
  identidad: bautizo del chat      // 'Jorge · Buin', 'Constructora Ranco'
  monto: '$200'|'$2.480'|'~$1M'    // neto; '~' = potencial estimado (sin cotización firme)
  detalle: 'mensual · Sofía' | '30+1 · espera tu OK' | 'mañana 9-13 · repartidor avisado'
           | 'lun · efectivo'      // en Cobrado: día + MEDIO DE PAGO
  link: abrirChat | estadoVivoExterno ('Estado del repartidor en vivo (Supabase)')
}
Columna { nombre, count, sumaMontos ('3 · $530mil'); Cobrado filtra MES ('Cobrado · julio') }
EtapaDef { orden, nombre (editable), origen: 'camino'|'tú'|'externo(repartidor)',
           regla: 'entra cuando el camino Ofrecer formal envía la cotización' }
```
Doctrina textual del prototipo (L753): *"Las etapas son **datos de este módulo**, no
código… Un camino nunca mueve directo: **emite la señal, el módulo la valida** y queda en
la traza."* — coincide 1:1 con ronda7 (`moverPedido` única puerta, efectos del paso).
Default destaperapido: Cotizando → Por confirmar → Por entregar → Cobrado (falta Perdido
— brecha ya elevada en ronda7 §2.1).

### 1.9 Ficha (ctx L773-826 + `verFichaConfig` L926-935)

Dos capas:
1. **Valores por conversación** — secciones dinámicas con pares k/v; los valores pueden
   ser estado enriquecido (`'esperando tu precio'` en ámbar, `'lista para tu OK'`).
   Aparecen ANTES de que exista pedido (Carolina cotizando ya tiene ficha). ⚠ GAP-G4.
2. **Esquema por negocio** — `CampoFicha {nombre, activo, aportadoPor: móduloId |
   'propio', tipo?}`: Comuna/Pedido ← Cotizador, Fechas ← Entregas, Correo ← canal
   Correo, Potencial ← Embudo; campos propios ('N° de obra / RUT empresa') los llena el
   bot cuando aparecen en el chat. *"si apagas Entregas, 'Fechas' desaparece de la ficha
   solo"* — depende de la brecha `aportes` del manifest (ronda7). ⚠ GAP-G22.

### 1.10 Traza de un turno (`porQue` L991-1016 + pop-madre + verEntrega)

Cada mensaje del bot es explicable con pasos tipados `{estado: ok|esp, titulo, detalle}`:

1. **Derivación**: 'Recepción → Sofía — pidió baños químicos, dominio de Sofía'.
2. **Datos**: 'comuna ✓ cantidad ✓ fechas ✓ (de la nota de voz transcrita)' — con ORIGEN
   por dato (ingesta).
3. **Caminos aplicados**: 'Evento 4+ baños → $80.000 c/u · No repreguntar · Ofrecer
   cotización formal' (n + cuáles + valores) — es la `Resolution` del resolver.
4. **Fuente de cifra**: '$80.000 sale de la tabla, no del modelo'.
5. **Efecto/señal**: 'Pedido → Por confirmar — señal del camino Detectar confirmación,
   validada por el módulo Embudo' (el paso Efecto de ronda7 §1.5).
6. Variantes: módulo ingesta ('la foto se describió al ingreso: válvula de bola 2"'),
   flujo de pausa (4 pasos), traza de entrega (programada ✓ / repartidor avisado ✓ con
   pin Maps / en ruta — la marca el repartidor / entregado → Cobrado avanza solo).

⚠ GAP-G9/G10: exige `turno` persistido y referenciable desde el mensaje.

### 1.11 Módulo (vista L500-603 + `mod()` L1317 + MODIA L1105-1133)

```
ModuloPanel {
  id, nombre: verbo del dueño      // 'Cotiza', 'Hace seguimiento', 'Ve fotos y oye audios',
                                   //   'Coordina entregas', 'Te pide ayuda cuando no sabe'
  seccion: 'Venta'|'Operación'|'Canales'|'Conexiones'   // ⚠ no mapeada al manifest (ronda7)
  meta: descripción + CONSECUENCIA DE APAGAR             // 'si lo apagas, se van el hero de
                                   //   plata y la etapa Cotizando' — exige `aportes`
  activo: bool                     // apagar: 'su config queda guardada y su rastro
                                   //   desaparece del panel'
  config: kv[]                     // Cotiza: {ultimoClick: 'Siempre yo'|'Solo si no calza'|
                                   //   'Automático', mostrarNeto}; Seguimiento: {esperar: 2d|5d};
                                   //   Ingesta: {voz, fotos, videos}; Entregas: {despachar:
                                   //   'Con mi OK'|'Automático'}; PideAyuda: {avisarWhatsApp,
                                   //   insistir: 30min|1h|nunca}  ⚠ GAP-G8b (insistencia no está
                                   //   en el schema pausa del blueprint)
}
CanalPanel { id, estado: conectado|conectar|pronto, detalle, config }
  // Correo multi-modo: reenvío (recomendado) / Gmail OAuth / IMAP hosting / crear con
  //   dominio / sunegocio@dixdybot.cl (memoria flujo-chats §2)
```
Configuración conversacional (MODIA): descripción del negocio → la IA arma config con el
CATÁLOGO existente + antes/después; **lo inexistente se ENCARGA a Claude Code** (se
fabrica con manifest+pruebas, aparece en el catálogo, el dueño lo activa — *"nada se
activa solo"*). Preset preview reversible sin tocar la instancia real.

### 1.12 Conexión (L589-602 + `verConexion`/`nuevaConexion`/`conexionChat`/`verActividadCx`)

```
Conexion {
  id, nombre ('API del repartidor', 'Supabase')
  origen: 'fabricada'|'catalogo'|'mcp'
  fabricadaPor?: {quien: 'Claude Code', fecha: '8 jul', desde: 'tu descripción', conPruebas: true}
  estado: {ok, ultimaLlamada ('hoy 10:42 ✓'), llamadasSemana (47), errores (0)}
  credencial: {mask ('••••7f2a'), cambiable desde el panel sin tocar código}
  herramientas: [{id ('crear_entrega'), activa, permiso: 'Con tu OK'|'Bot solo'|'Solo tú',
                  usadaPor ('el camino "Despachar con tu OK"')}]
  actividad: [{estado: ok|mal, ts, herramienta, contexto ('chat Ranco · camino X' |
               'tablero (automático)'), error+resolucion ('clave vencida — se reintentó ✓')}]
}
```
Invariantes: *"toda conexión aporta **herramientas** que los caminos usan como acciones —
y eliges cuáles puede tocar **cada agente**"* (permiso por herramienta Y por agente);
*"cada uso queda aquí y en la traza del chat donde ocurrió — nada invisible"*.
Alta por 3 vías: catálogo guiado / pegar un MCP (herramientas autodescubiertas) / API
propia por chat (explora doc en solo-lectura → propone → permisos → 'Fabricar conector').
⚠ GAP-G21 (entidad completa + evento `herramienta.usada` sin modelar).

### 1.13 Negocio (footer L350 + `nuevoNegocio` L1161-1175)

`{id, nombre, estado}` + selector en el footer. Onboarding = **propuesta completa
aprobable**: agente (nombre+personalidad del rubro), módulos on/off con razones, etapas
del tablero con sus reglas ('la seña del 30% mueve a Señado'), campos de ficha DEL RUBRO,
N caminos en borrador + preguntas de precios faltantes, encargos a Claude Code de lo
inexistente. Después: conectar canales + gimnasio + gate 4,0. Invariante: *"cada negocio
es su propio dixdybot: datos, historial, número y caminos completamente separados —
comparten el software, jamás los datos"* = clon-por-cliente. ⚠ GAP-G24 (el selector
multi-negocio en UN panel choca con un-panel-por-clon; decidir shell).

### 1.14 La Guía (chat-IA de Caminos, `GUIA` L1255-1272; y `modIA` en Módulos)

No es entidad: es el contrato conversacional de consulta/comando. Cuatro capacidades que
el backend debe servir con DATOS REALES: (1) pregunta en contexto → responde con los
caminos y números del negocio + deep-link (`seleccionar('mensual2')`); (2) rendimiento →
ranking por plata + nunca-disparan ('¿los archivo?') + bajo-cierre → propuesta de
gimnasio; (3) comando de cambio ('sube los precios 10%') → genera Borrador §1.6; (4)
camino nuevo desde NL → 'la escribo, la pruebo contra las doradas, reviso choques y te
muestro el resultado antes de que viva'.

---

## 2. EVENTOS / ACCIONES del panel (payload → efecto esperado)

Toda mutación pasa por el motor (una vía de escritura, `escritor.ts`); el panel jamás
escribe directo. Cada evento apendea a `eventos.jsonl` con `origen` discriminado
(ronda7 §1.3: `camino|dueno|externo`).

| # | Acción (prototipo) | Payload | Efecto esperado |
|---|---|---|---|
| E1 | `duda.responder` (`pausaResponder`) | `{dudaId, texto}` | fase→`evaluando`; el agente EVALÚA la respuesta (LLM); si objeta → contra-argumento con datos al `hilo`; el dueño siempre puede imponer |
| E2 | `duda.decidir` (`pausaCerrar`) | `{dudaId, decision, origen: propuesta\|impuesta}` | **check1 AL TIRO**: mensaje `bot` al cliente con la decisión (nadie queda esperando); `prev` del chat se actualiza; fase→`checks` |
| E3 | `duda.afinar` (`pausaAfinar`) | `{dudaId, alcance}` | crea `Camino {origen:'aprendido', estado:'activo', pruebas, hist:['creado desde la pausa']}`; fase→`resuelta`; decisión de Hoy → Resueltas con hora; badge decrementa; toast 'Camino creado — nació de esta conversación' |
| E4 | `cotizacion.aprobar` (`aprobarRanco`) | `{pedidoId}` | genera PDF + envía correo → tarjeta `correo` al hilo + mensaje `bot` ('Le acabo de enviar…'); dedup por `correoEnviado`; decisión → Resueltas ('PDF + WhatsApp · repartidor se avisa al confirmar entrega'); aviso futuro al abrirse el correo |
| E5 | `borrador.publicar` | `{borradorId}` | CANDADO: pruebas doradas en verde o rechazo; aplica diffs a N caminos; `hist.push` por camino; chip 'publicado hh:mm' → link al historial; tarjeta de Hoy pasa a 'publicado'; 'Sofía ya cotiza con los precios nuevos' (snapshot al próximo turno) |
| E6 | `borrador.descartar` | `{borradorId}` | nada cambia; chip desaparece; queda evento |
| E7 | `mensaje.ensenar` (`ensGuardar`) | `{convId, msgId, regla}` | regla destilada AL INSTANTE; marca 💡 bajo el mensaje; reversible en Caminos; si choca con un camino → aviso |
| E8 | `chat.enviar_como_dueno` (`enviarTu`) | `{convId, texto}` | mensaje `remitente:humano`; **el bot se calla 30 min EN ESE chat** (silencio temporal, no handoff) ⚠ GAP-G5 |
| E9 | `chat.tomar` | `{convId}` | `asignado='humano'` indefinido ('Sofía se calla — tú lo llevas'); falta el inverso Devolver (ronda7 §2.2) |
| E10 | `chat.reabrir` | `{convId}` | estado `resuelta`→`abierta` |
| E11 | `seguimiento.editar` / `seguimiento.cancelar` | `{progId, texto?}` | edita el texto hasta la hora programada / cancela; píldora de actividad |
| E12 | `etapas.editar` (`guardarEtapas`) | `{etapas: [{id, nombre, orden, regla, origen}]}` | valida (lint inverso ronda7: caminos que referencian, pedidos parados) → escribe `ajustes/embudo.json` → 'el tablero se redibuja con tus etapas' |
| E13 | `pedido.mover` (tarjetas; ronda7) | `{pedidoId, a, origen, porque}` | ÚNICA puerta `moverPedido`: valida transición+`requiere` → etapa + evento + píldora en el hilo |
| E14 | `modulo.toggle` (`mod`) | `{moduloId, activo}` | soft-disable; config guardada; sus `aportes` (columnas, métricas, campos de ficha, decisiones) desaparecen del panel |
| E15 | `modulo.config` | `{moduloId, cambios}` | valida contra `configSchema` → `ajustes/<id>.json` + commit git + snapshot próximo turno |
| E16 | `modulos.configurar_ia` (`modIA`) | `{descripcion}` | propuesta antes/después SOLO con el catálogo; aplicar = E14/E15 en lote; lo inexistente → E22 |
| E17 | `ficha.configurar` / `ficha.campo_nuevo` | `{campos on/off}` / `{nombre, tipo}` | esquema de ficha del negocio; el bot llena el campo propio si aparece en el chat |
| E18 | `conexion.herramienta` | `{conexionId, herramienta, activa, permiso}` | actualiza permisos (por herramienta y por agente) |
| E19 | `conexion.credencial` | `{conexionId, secreto}` | rota credencial sin código; reintento de llamadas falladas |
| E20 | `conexion.fabricar` (`conexionChat`) | `{docsUrl, credencial, herramientas+permisos}` | encargo asíncrono a Claude Code (explora solo-lectura → fabrica con pruebas) → 'aparece aquí al terminar' |
| E21 | `camino.crear_guiado` / `guia.comando` | `{reglaNL}` / `{texto}` | escribe camino/borrador + corre doradas + chequeo de choques → resultado ANTES de vivir (nunca directo a vivo) |
| E22 | `encargo.crear` (Webpay, conector) | `{descripcion}` | cola de fabricación Claude Code; al terminar: módulo/conector en catálogo, INACTIVO hasta que el dueño lo active |
| E23 | `camino.deshacer` (`verHistorial`) | `{caminoId}` | restaura versión anterior COMO BORRADOR (pasa por E5 para vivir) |
| E24 | `negocio.crear` (`nuevoNegocio`) | `{descripcion\|audio\|url}` → confirmar/ajustar | propuesta completa §1.13; confirmar = instanciar clon + agente en `practicando` con gate 4,0 |
| E25 | `agente.crear` | `{rubro}` | 'un rubro nuevo = un agente nuevo con sus caminos'; nace `practicando`, se activa al pasar 4,0 |
| E26 | `gimnasio.crear_camino_desde_fallo` | `{replayId}` | abre E21 pre-cargado con el fallo del juez |
| E27 | (entrante) cliente escribe a chat dormido | — | despierta sola arriba con todo su historial |
| E28 | (externo) repartidor marca en Supabase | — | poller → E13 `origen:externo` → tablero + píldora en el hilo |
| E29 | (interno) señal de etapa desde camino | efecto del paso completado | resolver → E13 `origen:camino` — el LLM solo declara el paso terminado (ronda7 §1.4) |

Eventos del ledger ya canónicos (ronda7): `pedido.creado/movido/actualizado/
cobro_registrado/reabierto/movimiento_rechazado`. **Nuevos que este contrato exige**
⚠: `duda.creada/respondida/evaluada/decidida/afinada`, `camino.aplicado` (G12),
`camino.creado/editado/publicado/descartado/deshecho`, `ensenanza.creada/revertida`,
`herramienta.usada` (G21), `conversacion.bautizada/dormida/despertada/asignada`,
`correo.enviado/abierto`, `encargo.creado/terminado`, `gimnasio.corrida`.

---

## 3. VISTAS como queries

**V1 · Hoy** (una llamada agregada):
- `heroPlata` = Σ `pedidos.monto_neto` en etapas tipo 'abierta' con actividad hoy — CON
  declaración de módulos de origen (auditoría r7: un rubro sin cotización necesita otro
  hero → el hero lo aporta el módulo vía `aportes.metricasHoy`).
- secundarias: chats con actividad hoy · pedidos en `cotizando` · entregas de hoy/mañana.
- `decisiones[]` pendientes (dudas + aprobaciones + borradores), pausas primero.
- `resueltas[]` del día (colapsadas) + `nPendientes` para el badge del sidebar.

**V2 · Chats lista**: secciones ordenadas por ATENCIÓN — `espera=true` ("Dudas del bot")
→ Activos (recencia) → pie Dormidos (count; expandible, opacidad .55). Cada fila: bautizo
+ tags + prev + hra + pto. Filtro por agente (`sel-agente`; agente sin chats → vacío).
Búsqueda full-text sobre nombre+comuna+pedido+contenido+ficha, INCLUYE dormidos ⚠ GAP-G25.

**V3 · Hilo**: mensajes del conv (orden ts) + proyecciones intercaladas: duda viva como
widget, programados pendientes al final, tarjetas de correo del MISMO contacto (G7).
Header: bautizo + sub + chip + Tomar. Composer: placeholder con el nombre del agente +
CTA contextual (`accion`). Ctx: ficha §1.9.

**V4 · Tablero**: columnas desde `ConfigEmbudo.etapas` (orden); por columna COUNT +
Σ monto; 'Cobrado' filtra el mes corriente y muestra medio de pago; tarjeta → chat o
estado externo vivo. Botón Etapas solo en modo tablero.

**V5 · Caminos**: tabs por agente (con counts 34/12); grupos con contador; por camino
stats (usos = `camino.aplicado`; cierre = pedidos ganados atribuidos/usos; plata = Σ
ganados del mes); chip '1 borrador' pendiente; peek = kv + pruebas n/n + historial;
sidebar Caminos = Σ de todos los agentes (46).

**V6 · Módulos**: catálogo (manifest + ajustes + activo) agrupado por sección + canales
con estado + conexiones con pto de salud y tooltip de última llamada.

**V7 · Agentes**: lista (madre con `{derivadosHoy, dudas}` + especialistas con pto
ok/practicando) + detalle (mets, presets, ejemplo, prácticas → replays).

**V8 · Traza de un turno** (por click en mensaje bot): pasos §1.10 desde el turno
persistido (evaluación + resoluciones + efectos + fuentes de datos).

**Contadores sidebar** (endpoint único de resumen, no N llamadas): Hoy (ámbar si >0),
Chats activos, Caminos totales, estado global (punto verde 'Todo funcionando').

---

## 4. MAPEO al plano de datos y GAPS

Almacenes vigentes: **6 tablas SQLite** (`contactos, identidades, canales,
conversaciones, mensajes` del blueprint §4.4 + `pedidos` de ronda7 §1.2) · **ledgers
JSONL** (`uso-llm, eventos, envios`) · **archivos del clon** (`caminos/*.yml`,
`ajustes/<modulo>.json`, `persona/`, `media/ + .anotacion.json`, git = historial).

| Entidad/campo del panel | Almacén | Estado |
|---|---|---|
| Conversación núcleo (estado, dormida, snooze, asignado, camino activo, sesión) | `conversaciones` | ✅ modelado |
| `sub`/filtro por agente (Sofía) | — | ⚠ **G1**: falta `conversaciones.agente_id` (dominio del especialista asignado) |
| `noleido` | — | ⚠ **G2**: falta `visto_por_dueno_ts` (o leído por conversación) |
| `tags` automáticas grande/nuevo/urgente | — | ⚠ **G3**: derivables (monto>umbral config, edad, señal urgencia) — definir reglas+umbral en `ajustes/` y si se materializan o se calculan al leer |
| Bautizo + ficha pre-pedido (Carolina cotizando ya tiene Comuna/Pedido/Plazo) | `pedidos.datos` solo si hay pedido | ⚠ **G4**: falta `conversaciones.ficha` JSON (datos extraídos ANTES del pedido) o crear el pedido temprano — decidir; el bautizo se deriva de ahí |
| Silencio 30 min tras mensaje del dueño | `asignado` es binario | ⚠ **G5**: falta `bot_silencio_hasta` (timestamp) distinto del handoff |
| Mensajes cli/bot/tu/sys + ✓✓ + dedup | `mensajes` (tipo/remitente/estado/source_id) | ✅ modelado |
| Mensaje programado editable/cancelable | — | ⚠ **G6**: falta almacén `programados` (módulo Seguimiento): `{convId, cuando, texto, origen, estado}` — hoy solo existe el patrón 💤 del bot vivo |
| Tarjeta de correo EN el hilo WA | `identidades` une la persona | ⚠ **G7**: las 6 tablas separan conversaciones POR CANAL; el hilo fusionado exige query por `contacto_id` (threads/resource de mastra) o mensajes espejo `tipo:'actividad'` — definir la vía |
| 💡 enseñado por mensaje + regla reversible | — | ⚠ **G8**: falta ledger `ensenanzas.jsonl {convId, msgId, regla, caminoAfectado, revertida}`; y la config 'insistir 30min/1h/nunca' + 'avisar por WhatsApp' no está en el schema pausa (G8b) |
| Traza por mensaje bot | `mensajes` sin ref | ⚠ **G9**: falta `mensajes.turno_id` |
| Turno completo (evaluación+Resolution+efectos+uso) | piezas sueltas (uso-llm, eventos) | ⚠ **G10**: falta almacén nombrado del turno (`trazas.jsonl` o eventos `turno.*` correlacionados por `turnoId`) — sin esto el "por qué" del panel no se reconstruye |
| Camino (cuando/entonces/dominio/relaciones/estado/origen) | `caminos/*.yml` (schema §4.3) | ✅ modelado |
| `grupo` de la cascada | — | ⚠ **G11**: agregar `grupo` al schema Camino (o derivarlo — decisión) |
| Stats por camino (usos/% cierre/$ mes) | — | ⚠ **G12**: falta evento `camino.aplicado {caminoId, convId, turnoId}` + atribución de cierre (pedido ganado → caminos que participaron) — definir la regla de atribución |
| Historial de camino + deshacer→borrador | git del clon | ⚠ **G13**: falta API del panel sobre git (log por archivo, revert como borrador) — el mecanismo existe, el contrato no |
| Borrador multi-camino con candado de pruebas | — | ⚠ **G14**: falta entidad `borradores/<id>.json` (diffs, pruebas, origen, estado) |
| Pruebas doradas POR camino (5/5 con nombres) | gimnasio = 6 personas globales | ⚠ **G15**: falta almacén `pruebas/` por camino + resultado por versión (se re-juegan en cada cambio; bloquean publicación) |
| Agente (persona, presets, gate, estado) | fragmentos de persona por dominio | ⚠ **G16**: falta `data/agentes/<id>.json` (nombre, avatar, presets, ejemplo, estado practicando/activa, gate) — hoy el especialista es solo un `dominio` implícito |
| Corridas del gimnasio / replays / nota juez | — | ⚠ **G17**: falta `gimnasio/corridas.jsonl` (guion, veredicto tipado, sugerencia, delta) — patrón runs de vocero ya elegido en r4, sin aterrizar |
| Costo hoy POR agente | `uso-llm.jsonl` | ⚠ **G18**: agregar `agente/dominio` al ledger de uso |
| Duda multi-fase junior→senior | `schemas/pausa.ts` (una vuelta) | ⚠ **G19**: extender a `{fase, resumen{}, hilo[], check1, check2, decision}` + tabla `dudas` (estado vivo → SQLite por la regla de reparto) proyectable en Hoy Y en el hilo |
| Cola de decisiones de Hoy + resueltas del día | — | ⚠ **G20**: contrato de query sobre dudas+pedidos-esperando-OK+borradores; tipos extensibles por módulo (`aportes.tiposDecision`) |
| Conexión (herramientas, permisos por herramienta Y por agente, credenciales, actividad) | módulos aportan `herramientas()` | ⚠ **G21**: falta `ajustes/conexiones/<id>.json` + evento `herramienta.usada {conexionId, herramienta, convId, caminoId, resultado}` + matriz permiso×agente |
| Ficha configurable / aportes de UI (columnas, métricas, campos, decisiones) | manifest §4.5 | ⚠ **G22**: la brecha `aportes` de ronda7, RATIFICADA — es prerequisito de G20, del hero de Hoy y de 'apagar limpia el panel' |
| Pedido/etapas/transiciones/cobros/perdido | `pedidos` + `ConfigEmbudo` + eventos (ronda7) | ✅ modelado en ronda7 (falta solo ejecutarlo; Perdido y Cobros ya elevados allí) |
| Dormidos (auto 7d, despertar, razón) | `estado='dormida'` + `snoozed_until` | ✅ modelado; la regla de auto-dormir es config (¿de qué módulo? — resolver con G22) |
| Entrega en vivo (Supabase) | origen `externo` ronda7 | ✅ decidido (poller → moverPedido); declarar la conexión con G21 |
| Multi-negocio (selector footer, crear negocio) | clon-por-cliente | ⚠ **G24**: UN panel = UN clon; el selector exige shell/launcher multi-instancia (o dominio por clon) — decisión de producto pendiente, NO agregar tenant_id (NO de sencillez) |
| Búsqueda global (incl. dormidos y ficha) | — | ⚠ **G25**: FTS5 de SQLite sobre mensajes+ficha+contactos no está en el blueprint (es nativo, 0 deps) |

**Los 5 GAPS que bloquean primero** (sin ellos el panel no se puede alimentar):
**G10+G9** (turno/traza persistida — toda la explicabilidad cuelga de ahí), **G19**
(duda multi-fase — el diferenciador del producto), **G22** (aportes del manifest — sin él
no hay genérico-modular real ni Hoy componible), **G12** (stats de caminos — la vista
Caminos entera), **G4+G1** (ficha pre-pedido + agente en conversación — bautizo, orden y
filtro de Chats). El resto (G3, G5-G8, G11, G13-G18, G20-G21, G24-G25) se resuelve al
tocar su módulo.

**Dónde aterrizar cada corrección**: G1/G2/G4/G5 → columnas nuevas en
`conversaciones` (esquema.sql); G9 → columna en `mensajes`; G19 → tabla `dudas`; G10/G8/
G12/G21 → eventos nuevos en `eventos.jsonl` (+ `trazas.jsonl` si el volumen lo pide);
G6/G14/G15/G16/G17 → archivos en `data/` del clon (programados, borradores, pruebas,
agentes, corridas); G11 → schema Camino; G18 → ledger uso-llm; G22 → `ManifestModulo`
(campo `aportes`); G13/G25 → contratos de API del panel (git-log, FTS). Ninguno rompe
los 16 NOes de sencillez: 0 deps nuevas, 1 proceso, 1 escritor.
