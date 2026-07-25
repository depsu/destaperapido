# Auditoría del detector de solape — ¿son de fiar sus avisos?

**Fecha:** 25-jul-2026 · **Medido contra:** los 30 caminos reales del clon
(`/Users/alejandroriveracarrasco/SaSS/destaperapido/dixdybot-data/caminos-propuestos.json`),
leídos disparador por disparador y paso por paso, no por el porcentaje.

## Respuesta corta

**No entrenaba a ignorar el ámbar por ruido: entrenaba a ignorarlo por decir siempre lo mismo.**

De los 9 pares, **7 valían la pena y 2 eran ruido: 22 % de falsos positivos.** Eso no es
"el ámbar ya no significa nada" — 7 de cada 9 avisos apuntaban a algo real.

El defecto grave era otro y es peor que el ruido: **los 9 avisos decían la misma frase**,
"los dos arrancan casi con lo mismo", y la propuesta de fusión remataba con "dicen casi lo
mismo". Para el par `fuera-de-cobertura ↔ ubicación-especial` eso es **falso y peligroso**:
esos dos arrancan con la misma frase y hacen lo CONTRARIO (uno cierra la conversación, el
otro promete que el equipo confirma el valor hoy). El detector estaba invitando, en ámbar y
con confianza, a juntar dos caminos que jamás deben juntarse. Un aviso que da el consejo
equivocado quema más confianza que uno que sobra.

**Corrección de dato:** eran **11** caminos marcados, no 13. Verificado contra
`GET /api/caminos/borradores` y recontando los ids únicos de los 9 pares.

## Los 9 pares, uno por uno

| % | Par | Dictamen | Por qué (el texto, no el número) |
|---|---|---|---|
| 89 % | `precio-kit-completo` ↔ `cotizar-kit-completo` | **Duplicado real** | Los dos disparan con "Ya están comuna, cantidad y tiempo" y los dos mandan lo mismo: pedirle el valor a la herramienta del tarifario y entregarlo en el MISMO mensaje, sin inventar cifras. Es una regla escrita dos veces. |
| 75 % | `precio-exacto-neto` ↔ `neto-iva-factura` | **Duplicado real** | El disparador es literalmente el mismo escrito distinto ("pregunta si el valor está con IVA incluido" / "pregunta si el valor incluye IVA") y las dos acciones dictan la misma política: el valor es neto, el IVA solo si factura, y la cifra la pone la herramienta. **Este no estaba en la lectura previa y es tan duplicado como el trío.** |
| 60 % | `neto-iva-factura` ↔ `consulta-sobre-cotización-enviada` | **Falso positivo** | Solo comparten el andamiaje "pregunta si el valor incluye…". El objeto de la pregunta es otro: uno habla del impuesto, el otro de qué cubre cada ítem del documento ya enviado. Distinto dominio (ventas / soporte) y acciones que no se parecen en nada (17 %). |
| 60 % | `precio-kit-completo` ↔ `extra-sin-tarifa` | **Legítimo, pero es una EXCEPCIÓN** | "cuánto sale agregar una limpieza" es un caso de "cuánto sale". El primer movimiento es igual (dar el valor de tabla del baño al tiro, en neto), pero `extra-sin-tarifa` **para y le pregunta al dueño** porque el extra no está en el tarifario. Terminan distinto: no se juntan, se ordena cuál manda. |
| 57 % | `neto-iva-factura` ↔ `gesto-buen-cliente` | **Legítimo — choque real** (contradice la lectura previa) | No es ruido: `neto-iva-factura` lleva como cuarto disparador la frase exacta **"El cliente pide rebaja"**, y `gesto-buen-cliente` dispara con "pide rebaja o un valor fuera del tarifario". Las dos acciones legislan sobre la rebaja y no coinciden: una dice "nunca presentes el neto como descuento, si necesitas gancho usa los reales", la otra dice "ofrece el extremo bajo del rango como gesto". Una contesta sola y la otra escala al dueño. El aviso está señalando un disparador mal puesto — justo para lo que sirve. |
| 55 % | `precio-exacto-neto` ↔ `cotizar-kit-completo` | **Duplicado real** (trío) | Mismo kit, misma orden: valor exacto del tarifario, sin recordar ni estimar. |
| 50 % | `ubicación-especial` ↔ `fuera-de-cobertura` | **Legítimo — el hallazgo más valioso** | La misma condición escrita dos veces ("La comuna no está en ninguna zona del tarifario" / "no aparece en las zonas del tarifario") con salidas **opuestas**: uno agradece y cierra con puente ("nunca cotices"), el otro promete que el equipo confirma el valor hoy y pide la dirección. Nadie declaró prioridad entre los dos: hoy gana el que caiga primero en la selección. |
| 50 % | `sin-eco-un-mensaje` ↔ `calificar-kit-mínimo` | **Falso positivo** | Los dos se activan cuando falta el kit, cierto, pero `sin-eco` es del grupo **estilo** ("cómo conversa"): dice CÓMO escribir (un mensaje, sin repetir lo que el cliente acaba de mandar) y `calificar` dice QUÉ preguntar (ubicación → tiempo → cantidad). Una capa acompañando a un camino de contenido es el diseño, no un defecto. |
| 50 % | `precio-kit-completo` ↔ `precio-exacto-neto` | **Duplicado real** (trío) | Cierra el clique del trío. |

**Tasa de falsos positivos: 2 de 9 = 22 %.** La lectura previa acertó en el trío (duplicado
real, predicho antes de medir) y en `sin-eco ↔ calificar-kit-mínimo` (ruido); se equivocó en
`neto-iva ↔ gesto-buen-cliente`, que es un choque de verdad, y se le pasó un duplicado
(`precio-exacto-neto ↔ neto-iva-factura`) y el falso positivo que sí existía
(`neto-iva ↔ consulta-sobre-cotización-enviada`).

## Lo que se probó ANTES de tocar la fórmula

La sospecha era la fórmula, y pesar las palabras por lo raras que son (IDF). **Se midió y es
peor.** Con IDF sobre estos 30 caminos:

| Fórmula | Pares | ¿Ve el trío? | ¿Calla el ruido? |
|---|---|---|---|
| Dice (la actual) | 9 | Sí, los 3 pares | No |
| Dice × rareza (IDF), corte 0,50 | 5 | **No** — pierde 2 de los 3 pares | No: los 2 falsos positivos sobreviven |
| Dice × rareza, corte 0,45 | 7 | A medias (un par cae a 47,6 %) | No |
| Dice × rareza, corte 0,55 | 4 | **No** | Parcial, por accidente |

El motivo es entendible leyendo el corpus: los duplicados de verdad comparten justo las
palabras **más frecuentes** del rubro (comuna, cantidad, tiempo — en 9, 8 y 5 caminos), y los
falsos positivos comparten una palabra **rara** del andamiaje ("incluye", en 2 caminos). En
un corpus de un solo negocio, la rareza apunta al revés. **La fórmula de los disparadores
quedó igual.**

## El arreglo: el detector ahora mira los PASOS, no solo los disparadores

Un solape puede ser dos cosas muy distintas y el aviso tiene que decir cuál:

- **duplicado** — arrancan igual **y mandan lo mismo** → júntalos en uno.
- **choque** — arrancan igual **pero terminan distinto** → no los juntes; decide cuál gana.

Se distingue por dos vías, las dos leídas del propio camino:

1. **El texto de la acción** (contención: cuánto del más corto cabe en el más largo — Dice
   castigaría a la misma orden escrita larga y corta). Contra los 30 reales parte en dos
   limpio: duplicados de 29 % para arriba, choques de 23 % para abajo. La acción de un par
   cualquiera se parece 14 % (mediana de los 435 pares); el corte quedó en 26 %, que es el
   10 % de arriba.
2. **La pausa al dueño** — si uno para a preguntarle a Alejandro y el otro le contesta solo
   al cliente, no son el mismo camino digan las palabras que digan. No se mide: se lee del
   paso (`tipo: 'pausa-dueno'`).

Y dos guardias nuevas contra el ruido, además de las dos que ya había (polaridad y mínimo de
palabras en común):

- **Capas transversales** — un camino de grupo `estilo` acompaña a todos por diseño; solo se
  compara contra otra capa. Mata el falso positivo `sin-eco ↔ calificar-kit-mínimo`.
- **Mismo dominio** — a dos dominios distintos los atiende un agente distinto. **Con una
  excepción que se respetó a propósito:** `general` y `soporte` son dominios GLOBALES
  (`ConfigCaminos.dominiosGlobales`), o sea que se cargan en TODOS los turnos y sí compiten
  con cualquiera. Por eso esta guardia **no** tapa el falso positivo del IVA contra el de
  soporte: taparlo habría exigido apoyarse en una razón falsa.

### Resultado, medido

| | Antes | Ahora |
|---|---|---|
| Pares | 9 | **8** |
| Avisos | 18 | **16** |
| Caminos marcados | 11 | **9** |
| Falsos positivos | 2 (22 %) | **1 (12,5 %)** |
| Avisos con el consejo equivocado | 9 de 9 | **0** |
| Fusión propuesta | el trío | **el trío** (sin cambios) |

Los 8 quedan en 4 duplicados (el trío + el del IVA) y 4 choques. El falso positivo que
sobrevive (`neto-iva ↔ consulta-sobre-cotización-enviada`) ya no miente: sale como choque y
el aviso dice "terminan distinto, uno para a preguntarte a ti y el otro le contesta solo al
cliente, así que NO los juntes" — se descarta de una mirada.

Y la fusión ahora **solo junta duplicados** (`solo_duplicados`, encendida por defecto): aunque
alguien baje el umbral, jamás va a proponer fusionar `fuera-de-cobertura` con
`ubicación-especial`.

### Sigue siendo administrable

Todo desde la config del clon (`caminos.solape_disparadores` y `caminos.fusion`), sin tocar
código: `umbral`, `umbral_accion`, `min_palabras_comunes`, `distinguir_negacion`,
`distinguir_pausa_dueno`, `solo_mismo_dominio`, `dominios_globales`, `grupos_transversales`,
`max_por_camino`, `activo` — y en la fusión `umbral`, `min_caminos` y `solo_duplicados`.

### Lo que hay que hacer con los 4 choques (no lo arregla el detector)

Ninguno de los 30 caminos declara una sola relación, así que hoy, cuando dos chocan, gana el
que caiga primero. Los cuatro pares de choque necesitan que alguien escriba quién manda —
sobre todo `fuera-de-cobertura` vs `ubicación-especial`, que es el que le puede cambiar la
respuesta a un cliente real.

## Dónde quedó

- Detector y clasificación: `/Users/alejandroriveracarrasco/SaSS/DIXDY/dixdybot/src/core/caminos-motor.ts`
- Candado de la fusión: `/Users/alejandroriveracarrasco/SaSS/DIXDY/dixdybot/src/modulos/caminos/fusion.ts`
- Regresiones de esta auditoría: `/Users/alejandroriveracarrasco/SaSS/DIXDY/dixdybot/src/core/solape.test.ts`
  y el fixture `/Users/alejandroriveracarrasco/SaSS/DIXDY/dixdybot/src/modulos/caminos/solape.fixture.ts`
  (marcado "no molde")

`tsc` limpio y **579 tests verdes en 37 archivos**.

> **Ojo:** el panel que corre en `127.0.0.1:8793` sigue sirviendo el código anterior (9 pares)
> hasta que alguien lo reinicie — no se reinició por instrucción.
