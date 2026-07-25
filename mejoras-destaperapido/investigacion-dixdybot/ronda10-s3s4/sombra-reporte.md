# Modo Sombra — motor nuevo (dixdybot) vs bot vivo

- **Fecha:** 2026-07-24
- **Motor nuevo:** puerta única · motor cli (claude -p)
- **Fuente real:** /Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/data/conversaciones.jsonl
- **Muestra:** 12 pares cliente→bot · umbral de coincidencia 0.6

## Resumen

| Clase | Qué significa | Casos | % |
|---|---|---:|---:|
| 🟢 coincide | el nuevo dice esencialmente lo mismo que el vivo | 10 | 83% |
| 🔵 mejora | el nuevo pide el dato faltante donde el vivo cotizó a ciegas | 0 | 0% |
| 🔴 empeora | el nuevo soltó una cifra sin datos donde el vivo pidió el dato | 0 | 0% |
| ⚪ distinto | difieren sin señal clara de mejor/peor | 2 | 17% |
| | **similitud media** | | **0.22** |

> Clasificación de PRIMERA PASADA automática: `coincide`/`distinto` por similitud de
> tokens; `mejora`/`empeora` por señales de calidad (pedir el dato vs. soltar cifra sin
> datos). No es un juicio final — el juez (`juez.ts`) puede refinar los `distinto`.

## Detalle

### 🟢 coincide · `89219489886306@lid` · sim 0.21

- **Cliente:** Hola, quiero saber precios de arriendo de baños químicos
- **Vivo:** Buenas noches Jandy, claro. Me dice en qué comuna está y por cuánto tiempo lo necesitaría? así le paso el valor de una
- **Nuevo:** Hola, para pasarle el valor exacto necesito saber en qué comuna sería y por cuánto tiempo lo necesita
- **Motivo:** misma intención: ambos piden el dato faltante antes de cotizar, ninguno inventa cifra

### 🟢 coincide · `179362246701142@lid` · sim 0.25

- **Cliente:** Hola, quiero cotizar baños químicos (1–2 baños) para un evento o fiesta. ¿Me pueden dar un precio?
- **Vivo:** Buenas noches Katy, un gusto. Claro que sí, en qué comuna sería el evento? así le paso el valor de una
- **Nuevo:** Hola, para pasarle el valor exacto necesito saber dónde sería el evento, en qué comuna
- **Motivo:** misma intención: ambos piden el dato faltante antes de cotizar, ninguno inventa cifra

### 🟢 coincide · `227152381366460@lid` · sim 0.35

- **Cliente:** Hola, quiero cotizar baños químicos (1–2 baños) para una obra de construcción. ¿Me pueden dar un precio? por dia
- **Vivo:** Buenos días Mary, un gusto. En qué comuna está la obra y por cuánto tiempo lo necesitarían? así le paso el valor exacto
- **Nuevo:** Perfecto, para obra manejamos tarifa según los días que lo necesite /// ¿En qué comuna está la obra y por cuántos días sería? así le paso el valor exacto
- **Motivo:** misma intención: ambos piden el dato faltante antes de cotizar, ninguno inventa cifra

### 🟢 coincide · `225094941044748@lid` · sim 0.29

- **Cliente:** Hola, quiero cotizar baños químicos (1 baños) para una obra de construcción. ¿Me pueden dar un precio?
- **Vivo:** Buenos días, dónde está ubicado y por cuánto tiempo lo necesitaría? así le paso el valor
- **Nuevo:** Hola, para pasarle el valor exacto, en qué comuna está la obra y por cuánto tiempo lo necesitaría
- **Motivo:** misma intención: ambos piden el dato faltante antes de cotizar, ninguno inventa cifra

### 🟢 coincide · `263926294020327@lid` · sim 0.19

- **Cliente:** Hola, quiero cotizar baños químicos para una obra de construcción. ¿Me pueden dar un precio?
- **Vivo:** Buenos días Pintando, claro que sí. En qué comuna está la obra? así le paso el valor
- **Nuevo:** Hola, para pasarle el valor exacto dígame en qué comuna está la obra y cuántos baños necesitaría
- **Motivo:** misma intención: ambos piden el dato faltante antes de cotizar, ninguno inventa cifra

### ⚪ distinto · `242335275348156@lid` · sim 0.14

- **Cliente:** Por favor
- **Vivo:** Entendido Sebastian, le aviso de inmediato al equipo para que pasen a hacer el aseo de ese baño en Av Golf Lomas de la Dehesa 11480 hoy mismo lo coordinan y le confirman la hora por acá
- **Nuevo:** Ya le aviso al equipo para que le coordinen el aseo lo antes posible
- **Motivo:** similitud léxica 0.14 < umbral 0.6, sin señal de intención clara

### 🟢 coincide · `gym-1784863505701@entrenamiento` · sim 0.43

- **Cliente:** hola
- **Vivo:** Buenas noches, en qué comuna necesitaría el baño
- **Nuevo:** Hola, buenas, en qué comuna necesita el baño
- **Motivo:** misma intención: ambos piden el dato faltante antes de cotizar, ninguno inventa cifra

### 🟢 coincide · `275659607830626@lid` · sim 0.31

- **Cliente:** Hola, quiero cotizar baños químicos (1–2 baños) para un evento o fiesta. ¿Me pueden dar un precio?
- **Vivo:** Hola Ale, un gusto, dónde sería el evento, así le paso el valor
- **Nuevo:** Hola, para pasarle el valor exacto necesito saber en qué comuna sería el evento
- **Motivo:** misma intención: ambos piden el dato faltante antes de cotizar, ninguno inventa cifra

### 🟢 coincide · `222543780819019@lid` · sim 0.23

- **Cliente:** por dia
- **Vivo:** Buenos días, dónde estaría ubicado, así le paso el valor
- **Nuevo:** Perfecto, en qué comuna sería y cuántos baños necesita, así le paso el valor
- **Motivo:** misma intención: ambos piden el dato faltante antes de cotizar, ninguno inventa cifra

### 🟢 coincide · `161336570953769@lid` · sim 0.08

- **Cliente:** Hola, quiero cotizar baños químicos (1–2 baños) para un evento o fiesta. ¿Me pueden dar un precio?
- **Vivo:** Buenos días, ¿y dónde está ubicado el evento?
- **Nuevo:** Hola, para pasarle el valor exacto necesito saber dónde sería el evento, en qué comuna
- **Motivo:** misma intención: ambos piden el dato faltante antes de cotizar, ninguno inventa cifra

### ⚪ distinto · `25250381181159@lid` · sim 0.00

- **Cliente:** Le envio detalle para cotización según lo conversado telefónicamente
- **Vivo:** Perfecto, lo reviso apenas me llegue el detalle
- **Nuevo:** [[SILENCIO]]
- **Motivo:** el nuevo calló (le faltaba contexto); el vivo respondió apoyado en la conversación previa

### 🟢 coincide · `159158653419586@lid` · sim 0.21

- **Cliente:** Hola, quiero cotizar baños químicos para usar en alto del maipo. 3 baños por un total de 3 días, ¿Me pueden dar un precio?
- **Vivo:** Buenas tardes Marcelo, en qué sector del Cajón exactamente sería, así le confirmo el valor con todo incluido
- **Nuevo:** Alto del Maipo lo cubrimos sin problema, ¿en qué sector exactamente está la faena o el evento? así le confirmo el total de los 3 baños
- **Motivo:** misma intención: ambos piden el dato faltante antes de cotizar, ninguno inventa cifra

