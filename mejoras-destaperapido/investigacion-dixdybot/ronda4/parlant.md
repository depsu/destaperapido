# Parlant (emcie-co/parlant) — planos para los "caminos" de dixdybot (E3)

- **Repo:** https://github.com/emcie-co/parlant (~18k★)
- **Licencia:** Apache-2.0 (verificada en `LICENSE` del clon). Permite copiar patrones y hasta código con atribución + aviso de cambios. Copyright 2026 Emcie Co Ltd en cada archivo.
- **Clon leído:** `/private/tmp/claude-501/-Users-alejandroriveracarrasco-SaSS-DIXDY-clientes-destaperapido/5acfd0ef-e8b4-49b2-965d-26a7a76d1c5b/scratchpad/clones/parlant`
- **Stack de ellos:** Python asyncio, server FastAPI, motor "alpha", doc-DB + vector-DB propios, 24 adapters de LLM.

---

## (a) Modelo de datos exacto

### Guideline — `src/parlant/core/guidelines.py`

```python
@dataclass(frozen=True)
class GuidelineContent:          # líneas 47-51
    condition: str               # "cuándo" (lenguaje natural)
    action: Optional[str]        # "qué hacer" (None => guideline observacional)
    description: Optional[str]

@dataclass(frozen=True)
class Guideline:                 # líneas 54-67
    id: GuidelineId
    creation_utc: datetime
    content: GuidelineContent
    enabled: bool                # apagar sin borrar
    tags: Sequence[TagId]        # scoping: agente / journey / global
    metadata: Mapping[str, JSONSerializable]  # bolsa extensible (ver lifecycle)
    criticality: Criticality     # low | medium | high
    title: Optional[str]
    labels: Set[str]             # etiquetas libres que se propagan a la sesión
    composition_mode: Optional[CompositionMode]  # override por-guideline del modo de respuesta
    track: bool                  # si True, se recuerda que "ya se aplicó" en la sesión
    priority: int                # prioridad numérica (0 default)
```

Su `__str__` es literal: `"When {condition}, then {action}"` — la guideline ES una frase condición→acción, todo lo demás es gobierno.

Claves de `metadata` que el sistema escribe/lee (descubiertas por uso):
- `continuous: bool` — la acción aplica en todos los turnos mientras la condición siga viva (no se marca "ya aplicada").
- `customer_dependent_action_data: {is_customer_dependent: bool, ...}` — la acción necesita algo del cliente (cambia el batch de matching).
- `agent_intention_condition: str` — condición reescrita cuando el "cuándo" es una intención del agente.
- `internal_action: str` — acción propuesta por IA para guidelines observacionales.
- `journey_node: {...}` — marca que la guideline es una proyección de un nodo de journey (ver (a2)).

### Journey — `src/parlant/core/journeys.py`

```python
@dataclass(frozen=True)
class Journey:                   # líneas 87-98
    id, creation_utc
    description: str
    triggers: Sequence[GuidelineId]  # ¡las condiciones de entrada SON guidelines!
    title: str
    root_id: JourneyNodeId       # nodo raíz del grafo
    tags, composition_mode, labels, priority

@dataclass(frozen=True)
class JourneyNode:               # líneas 59-68 — ESTADO
    id, creation_utc
    action: Optional[str]        # qué hace el agente en este paso
    tools: Sequence[ToolId]      # herramientas habilitadas SOLO en este paso
    metadata, description, composition_mode, labels

@dataclass(frozen=True)
class JourneyEdge:               # líneas 74-84 — TRANSICIÓN
    id, creation_utc
    source: JourneyNodeId
    target: JourneyNodeId
    condition: Optional[str]     # lenguaje natural; None = transición incondicional
    metadata
```

Constantes: `JourneyStore.END_NODE_ID = "end"` y `DEFAULT_ROOT_ACTION = "<<JOURNEY ROOT: start the journey at the appropriate step based on the context>>"` (líneas 122-126). El SDK (`src/parlant/sdk.py` ~línea 1495) prohíbe crear dos aristas salientes sin condición desde el mismo nodo.

### (a2) El truco central: journey → guidelines proyectadas — `src/parlant/core/journey_guideline_projection.py`

`project_journey_to_guidelines()` (línea 38) hace BFS del grafo y convierte **cada par (arista, nodo destino)** en una Guideline transitoria:
- `id = "journey_node:<node_id>:<edge_id>"` — parseable (`extract_node_id_from_journey_node_guideline_id`, línea 19).
- `condition = edge.condition`, `action = node.action`, `criticality = HIGH`.
- `metadata["journey_node"] = {follow_ups: [ids de guidelines de las aristas salientes], index, journey_id, labels, tool_ids}`.

Resultado: **un solo motor de matching sirve para reglas sueltas Y para pasos de journey** — el journey no es un runtime aparte, es azúcar sobre guidelines. Este es el patrón más robable para dixdybot E3.

---

## (b) Relaciones entre guidelines

### Esquema — `src/parlant/core/relationships.py`

```python
class RelationshipKind(Enum):    # líneas 43-68, con docstring semántico cada una
    ENTAILMENT      # si SOURCE activa => TARGET se activa también
    PRIORITY        # si ambas activan => solo SOURCE queda
    DEPENDENCY      # SOURCE solo vive si TARGET también activa (AND entre targets)
    DEPENDENCY_ANY  # ...si AL MENOS UN target del mismo group_id activa (OR)
    DISAMBIGUATION  # si SOURCE + ≥2 targets activan => preguntar al cliente cuál
    REEVALUATION    # cuando corre la tool TARGET => re-evaluar guideline SOURCE
    OVERLAP         # tools SOURCE y TARGET se evalúan en el mismo batch

@dataclass(frozen=True)
class Relationship:              # líneas 106-115
    id, creation_utc
    source: RelationshipEntity   # {id, kind: GUIDELINE | TAG_ALL | TAG_ANY | TOOL}
    target: RelationshipEntity
    kind: RelationshipKind
    group_id: Optional[str]      # agrupa los OR de DEPENDENCY_ANY
```

Las relaciones no solo unen guidelines: pueden apuntar a un **tag** (o sea, "todas/alguna de las guidelines con este tag") y a **tools**. El tag de un journey (`Tag.for_journey_id`) permite "esta guideline depende de que el journey X esté activo".

### Evaluación — `src/parlant/core/engines/alpha/relational_resolver.py`

El `RelationalResolver.resolve()` (línea 264) corre un **loop hasta estabilizar (MAX_ITERATIONS=3)** con 4 pasos por iteración (docstring del módulo, líneas 15-34):
1. **Dependencias**: resuelve targets, **orden topológico con Kahn** (`_topological_sort`, línea 867) y evalúa en ese orden — así una caída cascadea en una sola pasada.
2. **Priorización relacional**: filtra deprioritizadas por guideline/tag/journey ganador, con filtrado transitivo de sus dependientes (`_filter_deprioritized_dependents`, línea 1204).
3. **Prioridad numérica**: se queda solo con el nivel máximo (`find_highest_priority_entities`, línea 473); las entailed quedan exentas para no matar a su entailer.
4. **Entailment**: activa guidelines implicadas (transitivo, `indirect=True`).

Detalle de oro para el panel del dueño: **cada decisión queda registrada** como `Resolution(kind ∈ {NONE, UNMET_DEPENDENCY_ALL, UNMET_DEPENDENCY_ANY, DEPRIORITIZED, ENTAILED}, details={descripción humana, relationship, counterparts})` (líneas 112-153) — explicabilidad de por qué una regla no disparó, lista para UI.

---

## (c) El matcher: qué guidelines carga y cómo decide

### Paso 1 — candidatas por TAGS, no por embeddings

`src/parlant/core/entity_cq.py::find_guidelines_for_context` (línea 118): une 4 listas — guidelines con tag del agente, globales (sin tag), con los tags del agente, con tags de journeys activos — **más** las proyectadas de cada journey activo. Sin similaridad: el scoping es determinista por tags.

### Paso 2 — activación de journeys

`engines/alpha/engine.py` (líneas 1464-1517): un journey está activo si (1) tiene `journey_path` en curso en el estado de sesión, o (2) alguno de sus `triggers` (guidelines-condición) matcheó este turno. El path recorrido se **persiste por sesión** en `AgentState.journey_paths: Mapping[JourneyId, Sequence[GuidelineId|None]]` junto a `applied_guideline_ids` (`core/sessions.py`, líneas 243-246). Ranking de journeys por relevancia sí usa embeddings (`journeys.py::find_relevant_journeys`, línea 1264, k=5 default) pero solo como orden, no como filtro duro.

### Paso 3 — decisión por LLM con salida tipada, en batches por "naturaleza"

`generic_guideline_matching_strategy.py::create_matching_batches` (línea 161) clasifica cada guideline en un tipo de batch con **prompt especializado**:
- observacionales (sin action) / accionables / accionables ya-aplicadas (si `track` y su id está en `applied_guideline_ids` del último turno) / ya-aplicadas dependientes-del-cliente / baja criticidad / grupos de desambiguación / **selección de nodo de journey** (un batch por journey activo).
- Journey step selection: `journey/journey_next_step_selection.py` — el LLM devuelve `{journey_continues, current_step_completed_rationale, current_step_completed, next_step_rationale, applied_condition_id}` (líneas 43-49): decide si el paso actual terminó y **qué arista** seguir; soporta backtrack (`journey_backtrack_check.py`).

Cada batch = 1 llamada LLM con schema JSON `{checks: [{guideline_id, condition, rationale, applies}]}` (`guideline_actionable_batch.py`, líneas 53-61) — **rationale ANTES del booleano**, 3 reintentos con temperaturas [0.15, 0.3, 0.1] (`optimization_policy.py`, línea 124). Tamaño de batch (línea 76): con ≤10 guidelines → 1 por llamada (!), ≤20 → 2, ≤30 → 3, después 5; low-criticality hasta 10 por llamada. O sea: Parlant paga MUCHAS llamadas por turno a cambio de precisión — con `claude -p` eso es inviable, dixdybot debe meter todas las condiciones en UNA llamada por turno (ver (g)).

Contexto inyectado por batch: historial de interacción, variables de contexto, glosario, eventos de tools staged, journeys activos y paths (`GuidelineMatchingContext`, `guideline_matcher.py` líneas 227-238) — construido con un `PromptBuilder` de secciones nombradas.

---

## (d) Canned responses: cifras desde datos, no del modelo

### Modelo — `src/parlant/core/canned_responses.py`

```python
@dataclass(frozen=True)
class CannedResponse:            # líneas 71-98
    id, creation_utc
    value: str                   # plantilla Jinja2: "Tu destape cuesta {{std.variables.precio}}"
    fields: Sequence[CannedResponseField]   # {name, description, examples}
    signals: Sequence[str]       # frases extra que se embeben para el retrieval
    tags: Sequence[TagId]        # scoping: por agente, journey, guideline o NODO de journey
    field_dependencies: Sequence[str]
    metadata
```

Vive en doc-DB **y** vector-DB (contenido + signals embebidos). `entity_cq.py::find_canned_responses_for_context` (línea 332) las junta por tag de agente + globales + por journey + **por guideline/nodo matcheado** (`Tag.for_guideline_id` / `Tag.for_journey_node_id`, línea 365) — puedes atar respuestas aprobadas a un paso concreto del camino.

### Modos de composición — `core/agents.py` líneas 48-52

`FLUID` (LLM libre) | `CANNED_FLUID` | `CANNED_COMPOSITED` | `CANNED_STRICT` (solo plantillas aprobadas salen al cliente). El modo se define por agente y se puede **sobreescribir por guideline y por nodo**; gana el más restrictivo (`canned_response_generator.py`, líneas 613-621).

### Flujo de selección — `engines/alpha/canned_response_generator.py`

1. El LLM genera un **draft** libre de la respuesta (con guidelines aplicables).
2. Shortlist por embeddings: `max_count=30` similares (línea 2271; store `find_relevant`, `canned_responses.py` línea 794).
3. Otro LLM **clasifica** la plantilla más fiel al draft. El prompt (líneas 2110-2117) tiene la regla de oro: *"If the deviation between the draft and the template is quantitative in nature (e.g., the draft says '5 apples' and the template says '10 apples'), you should assume that the template has it right"* — **el modelo nunca gana en números**; la cifra vive en la plantilla o en un field.
4. Render Jinja2 con cadena de extractores de fields (líneas 207-330):
   - `StandardFieldExtraction`: `{{std.customer.name}}`, `{{std.variables.X}}` (variables de contexto), `{{std.missing_params}}`, glosario — datos duros del contexto.
   - `ToolBasedFieldExtraction`: busca `tool_call.result["canned_response_fields"][field]` en los eventos de tools — **la tool entrega la cifra, no el LLM**.
   - `AdditionalFieldExtraction`: providers registrados por guideline/nodo.
   - `GenerativeFieldExtraction`: solo campos marcados `{{generative.x}}` los redacta el LLM (texto flexible, nunca la cifra crítica).
5. Sin match en modo estricto → `NoMatchResponseProvider` con plantilla fija: `"Not sure I understand. Could you please say that another way?"` (línea 82) — nunca sale texto libre.

---

## (e) Ciclo de vida / versionado de una guideline

- **Creación con evaluación previa**: `core/evaluations.py` — se encola una `Evaluation(status: PENDING→RUNNING→COMPLETED|FAILED, progress, invoices)` con `GuidelinePayload{content, tool_ids, operation: ADD|UPDATE, action_proposition, properties_proposition, journey_node_proposition}`. El `BehavioralChangeEvaluator` (`core/services/indexing/behavioral_change_evaluation.py`, líneas 102-170) corre proposers LLM (¿es continua? ¿la acción depende del cliente? ¿es intención del agente? ¿es solo-tool?) y emite un `Invoice{checksum, state_version, approved, data.properties_proposition}`. Solo invoices aprobadas materializan la guideline, y las propiedades inferidas quedan en `metadata`. **Patrón robable**: la IA clasifica la regla nueva ANTES de activarla, y esa clasificación decide cómo se evalúa después.
- **Activar/retirar**: `enabled: bool` (soft-disable), tags para scope, `delete_guideline` borra también sus asociaciones de tags. No hay historial de versiones de contenido de una guideline individual.
- **Versionado de esquema**: cada store tiene `VERSION` (guidelines va en 0.11.0) y una clase `GuidelineDocument_v0_X_0` por versión con conversores encadenados (`guidelines.py` líneas 196-516, `DocumentMigrationHelper`). Migración lazy al cargar el documento. Para dixdybot basta un campo `schema_version` en el JSONL + una función de upgrade — la idea sí, la maquinaria no.
- **Memoria de aplicación**: `track: bool` + `AgentState.applied_guideline_ids` por sesión — así "ofrece el descuento" no se repite en cada turno, y las ya-aplicadas se re-evalúan con un prompt distinto (¿reactivar o no?).

---

## (f) Qué NO copiar

- **Todo el server**: FastAPI (`src/parlant/api/`), contenedor DI, sesiones/eventos propios — dixdybot ya tiene su loop Baileys + JSONL.
- **La capa NLP**: 24 adapters (`src/parlant/adapters/nlp/`: openai, anthropic, ollama…) con `SchematicGenerator[T]` tipado — nuestro E1 `llm.js` es la puerta única equivalente; no reinventar.
- **Doble persistencia doc-DB + vector-DB** con embeddings para canreps/journeys — para el volumen de dixdybot, un shortlist por keywords/tags en JSONL basta al inicio.
- **Una clase TypedDict por versión de esquema** (11 clases para Guideline): pesadísimo; un `schema_version` + upgraders.
- **El costo del matcher**: batch de 1-5 guidelines por llamada LLM + 3 reintentos + batches paralelos por tipo = decenas de llamadas por turno. Con `claude -p` por CLI es inviable en latencia y costo. La precisión de Parlant viene del prompt especializado por tipo; nosotros tomamos la **taxonomía** (observacional / accionable / ya-aplicada / continua) como campos del schema y evaluamos todo en una sola llamada.
- **networkx** para los grafos de relaciones (relationships.py línea 22): Kahn son 20 líneas, ya copiadas arriba.

---

## (g) Propuesta: esquema de "camino" para dixdybot (JSON/YAML, E3)

Traducción de los planos a nuestro mundo (JSONL/YAML en disco, panel-editable, IA madre → agentes por dominio):

```yaml
# conocimiento/caminos/venta-destape.yml
camino:
  id: venta-destape
  version: 3                      # entero simple; historial = git del clon
  titulo: "Venta de destape exprés"
  descripcion: "Cotizar, confirmar y agendar un destape"
  dominio: ventas                 # ← agente especialista de la IA madre que lo opera
                                  #   (ventas | cobranza | logistica | soporte | ...)
  prioridad: 0                    # desempate numérico entre caminos activos (Parlant: Journey.priority)
  habilitado: true                # soft-disable desde el panel (Parlant: enabled)
  disparadores:                   # condiciones de entrada = guidelines observacionales (Parlant: triggers)
    - "el cliente pregunta precio o pide cotización de destape"
    - "el cliente describe un desagüe tapado"
  raiz: saludo

  pasos:                          # nodos (Parlant: JourneyNode)
    - id: saludo
      accion: "saluda y pregunta qué desagüe está tapado y en qué comuna"
      criticidad: media           # low|media|alta (Parlant: Criticality)
      continua: false             # si true, no se marca 'ya aplicado' (Parlant metadata.continuous)
      espera_del_cliente: "comuna y tipo de desagüe"   # (Parlant: customer_dependent_action_data)
      herramientas: []            # tools habilitadas SOLO en este paso (Parlant: node.tools)
      respuestas:                 # canned responses atadas AL PASO (Parlant: canreps por journey-node tag)
        - plantilla: "¡Hola! Claro que sí. ¿En qué comuna estás y qué desagüe se tapó?"
    - id: cotizar
      accion: "entrega el precio según tarifario y ofrece agendar"
      herramientas: [precios.buscar]
      modo_respuesta: estricto    # fluido|estricto por paso (Parlant: composition_mode por nodo)
      respuestas:
        - plantilla: "El destape de {{tipo}} en {{comuna}} cuesta {{datos.precio}} con IVA. ¿Te agendo?"
          campos:                 # (Parlant: CannedResponseField + ToolBasedFieldExtraction)
            tipo:  {origen: contexto}
            comuna: {origen: contexto}
            "datos.precio": {origen: tool, tool: precios.buscar}  # la CIFRA sale de la tool, jamás del modelo
    - id: pausa-dueno             # ← nuestra extensión: pausa-y-pregunta (Parlant no la tiene como nodo)
      tipo: pausa
      pregunta_al_dueno: "Cliente pide destape industrial fuera de tarifario: ¿precio?"
      timeout_horas: 4
      respuesta_espera: "Déjame confirmarlo y te escribo al tiro 👍"
    - id: fin
      tipo: fin                   # (Parlant: END_NODE_ID="end")

  transiciones:                   # aristas (Parlant: JourneyEdge)
    - de: saludo,  a: cotizar,     si: "ya se sabe comuna y tipo de desagüe"
    - de: saludo,  a: pausa-dueno, si: "pide un servicio fuera del tarifario"
    - de: cotizar, a: fin,         si: "confirma o rechaza"
    # regla Parlant (sdk.py): máx. UNA transición sin 'si' por paso

  relaciones:                     # (Parlant: RelationshipKind, subconjunto útil)
    - tipo: prioridad_sobre       # PRIORITY
      objetivo: camino:seguimiento-dormidos
    - tipo: depende_de            # DEPENDENCY
      objetivo: regla:horario-atencion
    - tipo: implica               # ENTAILMENT
      objetivo: regla:registrar-lead
```

Reglas sueltas (guidelines fuera de caminos) con el mismo ADN:

```yaml
regla:
  id: horario-atencion
  condicion: "el cliente escribe fuera del horario de atención"
  accion: "avisa el horario y ofrece dejar agendado"
  dominio: soporte
  criticidad: alta
  continua: true
  habilitado: true
  prioridad: 5
```

**Runtime (una llamada por turno, no N batches):** el motor arma el estado con (1) reglas del dominio activo + globales, (2) caminos cuyo `disparador` matchee o con `camino_path` vivo en la conversación (persistir `{camino_id: [paso, paso, ...]}` en conversaciones.jsonl, calcado de `AgentState.journey_paths`), (3) para el camino activo: paso actual + sus transiciones salientes (los `follow_ups` de Parlant). El cerebro devuelve UN JSON: `{reglas_aplican: [{id, razon, aplica}], camino: {sigue, paso_completado, transicion_elegida}, respuesta|plantilla_id}` — razón siempre antes del booleano. Después, un resolver determinista (portar el orden dependencias→prioridad→implicaciones del `relational_resolver`, con Kahn) filtra y registra cada decisión con su porqué, que es exactamente lo que el panel del dueño necesita mostrar.

**Explicabilidad para el panel:** guardar por turno el equivalente de `Resolution{kind, description, counterparts}` — "esta regla no disparó porque X tuvo prioridad" — en el JSONL del turno.
