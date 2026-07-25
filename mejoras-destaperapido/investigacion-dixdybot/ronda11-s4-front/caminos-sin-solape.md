# Que los caminos no se pisen — tareas #11 y #12

Fecha: 2026-07-25 · Molde: `~/SaSS/DIXDY/dixdybot` · Instancia: `~/SaSS/destaperapido/dixdybot-data`
Estado: **tsc limpio, `vitest run` entero verde (36 archivos, 554 tests)**.
Respaldo del archivo de la instancia antes de tocarlo:
`scratchpad/caminos-propuestos.RESPALDO-s4caminos.json` (md5 `90a5652…` idéntico al original)
más el `.bak-2026-07-25065117` que la propia migración deja al lado.

---

## Los números, medidos (no supuestos)

| | Antes | Después |
|---|---:|---:|
| Cajones para los 30 caminos | **17** | **10** (de una lista de 12 disponibles) |
| Caminos movidos de cajón | — | **12** |
| Caminos que ningún cajón reconoció | — | **0** |
| Pares de caminos marcados por pisarse | **0** (el candado no podía verlo) | **9** |
| Caminos con aviso de solape | 0 | **11 de 30** |
| Fusiones propuestas | 0 | **1** (junta 3 caminos) |
| Veredicto del lote | 24 ✅ · 6 ⚠️ · 0 ❌ | 17 ✅ · 13 ⚠️ · 0 ❌ |
| Costo del candado sobre los 30 | 1,4 ms | 22 ms |

El reparto nuevo de los 30: `cotizacion` 9 · `estilo` 4 · `seguimiento` 3 · `cierre` 3 ·
`excepciones` 3 · `upsell` 3 · `calificacion` 2 · `objeciones` 1 · `cobertura` 1 · `confianza` 1.

Ningún camino se borró, ninguno cambió de texto, las 52 pruebas doradas siguen ahí. Verificado
comparando el archivo migrado contra su respaldo: mismos ids, mismos disparadores, mismas pruebas.

---

## Problema #11 — 17 cajones para 30 caminos

### Lo que había
El destilador inventaba el nombre del grupo camino por camino. Salieron 17 cajones, con pares
que son el mismo cajón escrito distinto (`precio`/`precios`, `cotizacion`/`cotizacion-formal`,
`estilo`/`estilo_conversacion`/`conversacion`, `atencion`, `kit_minimo`) y once de ellos con un
solo camino adentro. Revisar 30 reglas repartidas en 17 carpetas es imposible.

### Lo que hice

**1. Lista de cajones CERRADA y administrable** — `src/modulos/caminos/grupos.ts`, nueva.
Vive en la config del clon (`ConfigCaminos.grupos`, Zod), no en el código. Los 12 que trae el
molde son el embudo de **cualquier** negocio de servicios — cero palabras del rubro de los
baños: `apertura`, `calificacion`, `cotizacion`, `objeciones`, `upsell`, `cierre`,
`excepciones`, `cobertura`, `confianza`, `seguimiento`, `estilo`, `otros`. Cada uno con
`nombre` (lo que se lee en el panel), `descripcion` y `sinonimos` (las otras formas de
nombrarlo). Un clon de otro rubro los reemplaza enteros desde el panel, sin tocar código.

**2. El destilador está obligado a elegir de esa lista** — `destilar.ts`.
El prompt le muestra los cajones permitidos y le prohíbe inventar. Si de verdad cree que falta
uno, no lo crea: lo **pide** (`grupo_nuevo: {id, nombre, porque}`) y el camino queda mientras
tanto en el cajón de sobra. Los pedidos salen en `revisarPropuestas().gruposPedidos` para que
Alejandro decida agregarlos a su lista. Si el modelo igual inventa un nombre, el resolutor lo
aterriza (id exacto → sinónimo → palabra en común → cajón de sobra) y lo deja **contado**.

**3. Migración de una sola vez, con informe** — `cli/normalizar-grupos.ts`, nueva.
```
node cli/normalizar-grupos.ts --datos <instancia> [--salida informe.md] [--aplicar]
```
Sin `--aplicar` **no toca nada**: solo escribe el informe (ensayo). Con `--aplicar` deja un
`.bak-<fecha>` al lado de cada archivo **antes** de escribirlo. El informe dice camino por
camino de dónde a dónde y por qué, marca aparte los que ningún cajón reconoció, y lista además
los caminos que se pisan y las fusiones propuestas (sin aplicar ninguna).

Corrida real sobre la instancia (informe en `dixdybot-data/caminos-grupos.md`): 18 → 11 cajones
contando los 3 caminos de ejemplo del molde; **17 → 10 mirando solo los 30 borradores reales**.

**4. La cascada del panel** ahora agrupa por el **nombre** del cajón y en el **orden de la
lista** (que es el embudo del negocio), no alfabético. Un grupo que ya no está en la lista se
muestra igual, al final y marcado "fuera de tu lista" — nada se esconde.

---

## Problema #11 bis — tres caminos que son la misma regla

Los tres decían lo mismo y los tres disparaban con "ya están comuna, cantidad y tiempo":
`cam-cotizar-kit-completo`, `cam-precio-exacto-neto`, `cam-precio-kit-completo`. Importa porque
el bot carga solo 3-5 caminos por turno: tres cupos gastados en la misma instrucción desplazan
reglas que sí hacían falta.

**Lo que hice** — `src/modulos/caminos/fusion.ts`, nueva. Propone (no aplica) juntar grupos de
caminos donde **cada par** supera el umbral. La propuesta trae:

- el camino que queda (base elegido con regla determinista: más pruebas → más disparadores →
  acción más larga → id), con los **disparadores unidos** y las **pruebas doradas SUMADAS**;
- el porqué en castellano y los pares medidos que lo sostienen;
- **la acción textual de cada uno de los absorbidos**, para que nada se pierda de vista.

La propuesta real: se queda `cam-precio-kit-completo` y absorbe a los otros dos → **8
disparadores y 6 pruebas doradas** (las 6 de los tres, ninguna descartada).

**Visible y reversible, nunca silenciosa:** aparece en la revisión de borradores del panel con
qué se junta con qué; se aplica solo si Alejandro aprieta el botón (`POST /api/caminos/fusionar`);
los absorbidos quedan **retirados, no borrados**, y se deshace volviéndolos a borrador desde su
ficha. Verificado en proceso contra una copia de la instancia real: 30 → 28 borradores al
aplicar, el que queda con 8 disparadores y 6 pruebas, y 28 → 29 al deshacer uno.

Por qué exige TRES y no dos (`fusion.min_caminos`, configurable): midiendo los 30 reales, los
pares sueltos por encima del umbral resultaron ser caminos que comparten UN disparador pero
hacen cosas distintas (el "¿incluye IVA?" aparece en el camino del precio y en el del IVA).
Que tres se parezcan **todos contra todos** ya no es casualidad. Quien quiera fusiones de a dos
baja el número desde el panel.

---

## Problema #12 — el candado no podía ver el solape

### Lo verificado del código viejo
El detector de conflictos de `caminos-motor.ts` solo conocía relaciones que el propio camino
**declara** (`prioridad_sobre`, `depende_de`, `implica`, `desambiguar`, `reevaluar`). Medido:
**0 de los 30 caminos declara ninguna**. El "0 rechazados" del informe estaba garantizado antes
de correr porque no había nada que mirar.

### Lo que hice
`detectarSolapes()` en `src/core/caminos-motor.ts`: el motor lo calcula **solo**, mirando las
palabras de los disparadores. Sale por el veredicto que ya existía (`veredicto.ts` →
`conflictoEnSimple`) y se ve en la cascada del panel. **No inventé otra vía.**

- **Es AVISO ámbar, jamás rechazo.** El test lo fija: los dos caminos siguen activos y los dos
  quedan anotados como aplicados; el aviso solo los señala.
- **El umbral es config** (`ConfigCaminos.solape_disparadores`, Zod): `activo`, `umbral`,
  `min_palabras_comunes`, `distinguir_negacion`, `max_por_camino`.
- **No se disfraza de "si apruebas todo el lote junto"**: dos caminos que arrancan con la misma
  frase se pisan igual, se apruebe lo que se apruebe.
- **El turno del bot no lo paga**: el orquestador no pasa la config, así que en cada mensaje el
  detector ni corre. Lo enciende quien REVISA (el candado y el panel).

### El umbral por defecto: 0,50, justificado con los datos reales
La medida es el parecido (Dice sobre palabras significativas) del **par de disparadores más
parecido** entre dos caminos. Contra los 30 reales:

| Umbral | Pares marcados |
|---:|---:|
| 0,40 | 25 (ruido: coincidencias del tipo "el cliente pide el valor") |
| **0,50** | **9** |
| 0,55 | 5 — deja fuera a uno de los tres gemelos (0,50) |
| 0,60 | 4 |

En 0,50 entran los tres gemelos (0,89 / 0,55 / 0,50) y lo siguiente ya baja a 0,44. Es el corte
natural del conjunto real.

> **Discrepancia con el enunciado, dicha derecho:** el brief hablaba de "13 pares por encima del
> 45 % y el más alto 56 %". Con mi métrica no reproduzco esos números exactos: da 15 pares ≥45 %
> sin la guardia de negación (y 9 con ella), y el par `cam-cotizar-kit-completo` ↔
> `cam-precio-exacto-neto` marca **54,5 %**, no 56 %. Es la misma familia de medida con otro
> tokenizador. Los números de este informe son los que produce el código que quedó.

### La guardia contra el falso positivo del enunciado
`cam-calificar-kit-minimo` ("…y **falta** comuna, cantidad o tiempo") comparte casi todas las
palabras con los gemelos ("**ya están** comuna, cantidad y tiempo") y es lo **contrario**: es la
excepción del otro, no un duplicado. Sin guardia, ese par marcaba 54,5 %.

La guardia de **polaridad** compara si los dos disparadores hablan de una ausencia (`no`, `sin`,
`falta`, `nunca`, `ningún`, `salvo`, `excepto`…) y no cruza uno que niega con uno que afirma.
Lo que mató, medido: `calificar-kit-mínimo`↔`cotizar-kit-completo` (54,5 % → fuera),
`calificar-kit-mínimo`↔`precio-kit-completo` (50 % → fuera), `precio-kit-completo`↔
`ubicacion-especial` (54,5 % → fuera, "el plazo **existe**" vs "el plazo **no existe**"),
`cotizacion-pendiente`↔`consulta-sobre-cotizacion-enviada` (50 % → 36 %, "**no** la ha recibido"
vs "la **recibió**"). Y hay test de regresión: kit-mínimo ↔ cantidad-en-rango **no se marca**.

### Los 9 pares que marca, ordenados
| Parecido | Un camino | El otro | En qué se pisan |
|---:|---|---|---|
| 89 % | cam-cotizar-kit-completo | cam-precio-kit-completo | "Ya están comuna, cantidad y tiempo" ≈ "…en la conversación" |
| 75 % | cam-precio-exacto-neto | cam-neto-iva-factura | "¿el valor está con IVA incluido?" ≈ "¿el valor incluye IVA?" |
| 60 % | cam-neto-iva-factura | cam-consulta-sobre-cotizacion-enviada | "¿el valor incluye IVA?" ≈ "¿el valor incluye traslados…?" |
| 60 % | cam-precio-kit-completo | cam-extra-sin-tarifa | "¿cuánto sale / cuánto vale?" ≈ "¿cuánto sale agregar una limpieza?" |
| 57 % | cam-gesto-buen-cliente | cam-neto-iva-factura | "pide rebaja o un valor fuera del tarifario" ≈ "pide rebaja" |
| 55 % | cam-cotizar-kit-completo | cam-precio-exacto-neto | "Ya están comuna, cantidad y tiempo" ≈ "Ya tienes… y toca dar el valor" |
| 50 % | cam-calificar-kit-minimo | cam-sin-eco-un-mensaje | "falta comuna, cantidad o tiempo" ≈ "Falta un dato del kit mínimo" |
| 50 % | cam-fuera-de-cobertura | cam-ubicacion-especial | "la comuna no está en ninguna zona" ≈ "la comuna no aparece en las zonas" |
| 50 % | cam-precio-exacto-neto | cam-precio-kit-completo | "Ya tienes comuna, cantidad y tiempo" ≈ "Ya están… en la conversación" |

Los 9 son avisos legítimos: cada uno es un par que de verdad arranca con la misma frase.

### El aviso, en castellano de persona
> se pisa con 'cam-precio-kit-completo': los dos arrancan casi con lo mismo (89% parecido) —
> el tuyo dice "Ya están comuna, cantidad y tiempo" y el otro "Ya están comuna, cantidad y
> tiempo en la conversación"

Hay test que prohíbe la jerga (jaccard, coeficiente, token, umbral) en ese texto.

---

## Efecto colateral que Alejandro tiene que saber

Con el detector encendido, **13 de los 30 borradores pasan de ✅ a ⚠️** (antes 24 ✅ / 6 ⚠️,
ahora 17 ✅ / 13 ⚠️). Ninguno queda rechazado: se pueden aprobar igual. Pero como la
preselección viene en `solo_pasa`, el panel **premarca 17 en vez de 24**. Si prefiere que el
ámbar también venga marcado, es un ajuste: `caminos.veredicto.preseleccion = 'pasa_y_avisos'`.

El candado sobre los 30 pasó de 1,4 ms a 22 ms (compara todos los disparadores contra todos).
Sigue sin caché — el número viaja en `resumen.ms` y se ve en el panel.

---

## Administrabilidad (misión #1) — todo con test

| Ajuste | Qué cambia | Test |
|---|---|---|
| `caminos.grupos` | la lista de cajones entera (otro rubro → otro reparto) | `grupos.test.ts`, `destilar.test.ts`, `api-caminos.test.ts`, `normalizar-grupos.test.ts` |
| `caminos.grupo_por_defecto` | dónde cae lo que no calza | `grupos.test.ts` |
| `caminos.grupos_cerrados` | volver al nombre libre de antes | `destilar.test.ts` |
| `solape_disparadores.umbral` | cuántos pares se marcan (0,5→9 · 0,6→2 · 0,8→1) | `solape.test.ts`, `api-caminos.test.ts` |
| `solape_disparadores.activo` | apagar el detector | `solape.test.ts`, `api-caminos.test.ts` |
| `solape_disparadores.distinguir_negacion` | la guardia contra el falso positivo | `solape.test.ts` |
| `solape_disparadores.min_palabras_comunes` | piso de palabras en común | `solape.test.ts` |
| `solape_disparadores.max_por_camino` | cuántos avisos por camino | `solape.test.ts` |
| `fusion.min_caminos` | fusiones de a dos o solo de a tres | `fusion.test.ts`, `api-caminos.test.ts` |
| `fusion.umbral` / `fusion.activo` | qué se propone juntar, o nada | `fusion.test.ts`, `api-caminos.test.ts` |

Todo es Zod dentro de `ConfigCaminos`, así que el panel ya lo dibuja y lo edita sin código nuevo.

---

## Bug de paso que apareció y quedó arreglado

`recolectarBorradores` (`consultas.ts`) no respetaba un camino **retirado**: si el retiro venía
de la base y el archivo del destilador aún lo tenía como borrador, volvía a aparecer en la lista
en la recarga. Sin eso, la fusión no se sostenía. Ahora `retirado` manda sobre el archivo.

---

## Archivos

**Nuevos**
- `src/modulos/caminos/grupos.ts` — la lista cerrada, el resolutor y la migración pura
- `src/modulos/caminos/fusion.ts` — la propuesta de fusión
- `src/modulos/caminos/solape.fixture.ts` — fixture de regresión, marcado **no molde**
- `cli/normalizar-grupos.ts` — la migración de una sola vez, con informe
- `src/core/solape.test.ts`, `src/modulos/caminos/grupos.test.ts`,
  `src/modulos/caminos/fusion.test.ts`, `tests/normalizar-grupos.test.ts`

**Tocados**
- `src/core/caminos-motor.ts` — `ConfigSolape`, `detectarSolapes`, `medirSolape`,
  `solapeEnCastellano`, nuevo tipo `solape-disparadores` en el resolver
- `src/core/duda-motor.ts` — `verificarParaActivar` recibe la config de solape
- `src/modulos/caminos/modulo.ts` — `grupos`, `grupo_por_defecto`, `grupos_cerrados`,
  `solape_disparadores`, `fusion`; ejemplos del molde con cajones de la lista
- `src/modulos/caminos/veredicto.ts` — traduce el solape, no le pone prefijo de lote, devuelve
  las fusiones
- `src/modulos/caminos/destilar.ts` — elige de la lista, pide permiso por un cajón nuevo
- `src/modulos/caminos/consultas.ts` — el retiro se sostiene
- `src/panel/api-caminos.ts` — cascada con nombres y orden, fusiones en `/borradores`,
  `POST /api/caminos/fusionar`
- `cli/revisar-caminos.ts` — el informe usa el mismo detector que el panel
- `panel/pwa/app.js` — nombres/descripción de cajón en la cascada, bloque de fusiones en la
  revisión. **Solo clases que ya existen en `tokens.css`** (`grupo-c`, `chip draft`, `meta-f`,
  `seccion`, `info-fila`, `pto esp`, `crece`, `btn s`, `cuerpo-n`); ni un `<style>` nuevo.

**Instancia**
- `dixdybot-data/caminos-propuestos.json` — migrado (30 caminos, 52 pruebas intactos)
- `dixdybot-data/caminos-propuestos.json.bak-2026-07-25065117` — el respaldo automático
- `dixdybot-data/caminos-grupos.md` — el informe de la migración, para que él lo lea

---

## Lo que queda para Alejandro

1. **Mirar `caminos-grupos.md`** y, si algún camino quedó en un cajón que no le gusta, moverlo
   (o cambiar la lista de cajones: es suya).
2. **Decidir la fusión** de los tres del precio en el panel. Al aplicarla conviene revisar la
   acción del que queda contra las dos textuales que trae la propuesta: puede haber un matiz
   (el "(neto) pegado al número", el "IVA solo si es empresa que factura") que valga la pena
   copiar antes de aprobar.
3. **Los otros 6 pares en ámbar** no son error. Los dos que más vale la pena mirar:
   `cam-fuera-de-cobertura` ↔ `cam-ubicacion-especial` (dicen literalmente lo mismo sobre la
   comuna fuera del tarifario) y `cam-gesto-buen-cliente` ↔ `cam-neto-iva-factura` ("el cliente
   pide rebaja" está escrito en los dos).
4. Si prefiere que el panel le premarque también los de ámbar:
   `caminos.veredicto.preseleccion = 'pasa_y_avisos'`.
