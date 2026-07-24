# Estado 2025–2026 de las formas de conectar un bot a WhatsApp

Investigación web verificada el 23-jul-2026 para el rediseño "dixdybot" (destaperapido.cl).
Todas las cifras de repos vienen de la API de GitHub y del registry de npm consultados hoy;
el pricing viene de la documentación oficial de Meta y de rate cards secundarias de 2026.

---

## (a) Baileys hoy

### Repo canónico y salud del proyecto

- **El canónico es `WhiskeySockets/Baileys`** (github.com/WhiskeySockets/Baileys). El repo
  original del autor (`adiwajshing/Baileys`) fue retirado por su autor; la comunidad
  WhiskeySockets continuó el desarrollo y es el único repo oficial hoy.
- Cifras exactas (GitHub API, 23-jul-2026): **10.233 estrellas, 3.216 forks, 334 issues
  abiertos, licencia MIT, NO archivado, último push 2026-07-22** — es decir, activo al día.
- En npm el paquete vigente es **`baileys`** (versión **7.0.0-rc13**) con **~817.000
  descargas/semana**, y el paquete viejo `@whiskeysockets/baileys` aún suma **~778.000
  descargas/semana** (npm API, semana 15–21 jul 2026). Combinados ~1,6 M/semana: es, por
  lejos, la librería no oficial más usada del mundo.
- **Pero lleva más de un año en "release candidate"**: la rama 7.0.0 va por rc13
  (2026-05-21) sin versión estable; hubo un hueco de releases de ~5 meses (rc.9 nov-2025 →
  rc10 may-2026). rc12 (2026-05-20) parchó una falla de seguridad (GHSA-qvv5-jq5g-4cgg);
  rc10 trajo fixes de memoria, mapeos LID y framework de testing. La rama legacy 6.7.x
  sigue recibiendo parches (6.7.23). Traducción: mantenido, sí; estable y predecible, no.

### Los males conocidos, con issues reales

- **Stream errors / desconexiones (los códigos que ya conoces):**
  - **440 = connectionReplaced** ("otro dispositivo tomó la sesión"): issues #502 ("Stream
    Errored Out Status code 440") y **#1933** ("Connection Closed | 440") con usuarios en
    loops de reconexión cada pocos segundos. Coincide con la memoria del proyecto: el 440
    tras vincular es "asentamiento", no hay que reiniciar.
  - **515 = restartRequired**: issues #141, #313 y **#1218** (el 515 corta la conexión
    justo durante el pairing). Es esperado por protocolo, pero Baileys delega en el
    usuario TODA la lógica de reconexión — cada app la reinventa.
  - **428 = connectionClosed**: cierre "normal", también hay que manejarlo a mano.
  - La búsqueda de issues del repo arroja **54 issues** que mencionan "stream errored".
- **"Bad MAC" (sesión Signal corrupta):** **36 issues** en el repo mencionan "Bad MAC".
  Destacan **#2234** ("Session error: Bad MAC" aleatorio), #635 (mensajes no visibles en
  el dispositivo), #1725 ("Failed to decrypt message with any known session") y #2110
  (reconexión que el teléfono rechaza y fuerza logout). Causas raíz documentadas: (1) la
  **migración a LID (Linked Identity)** de WhatsApp — si la sesión de cifrado se creó bajo
  una identidad y el mensaje llega bajo la otra, el descifrado falla (es el bug nº1
  reportado; v7/rc10 agrega mapeos LID justamente por esto); (2) archivos de sesión
  corruptos por apagones a mitad de escritura; (3) sesiones múltiples. La "auto-sanación"
  que ya tiene el bot de destaperapido (borrar sesión + reenviar) es exactamente el
  workaround que la comunidad aplica.
- **Mensajes duplicados / fantasma:** #568 (eventos duplicados en
  group-participants.update), **#1963** ("Baileys reporta enviado con éxito aunque el
  mensaje NO se entregó" — sin forma programática de detectarlo), #1643 ("Waiting for
  message" — el candado pegado en un check que destaperapido ya sufrió), #1692 (mensajes a
  un remoteJid incorrecto/aleatorio). Esto valida el diseño `envios.jsonl` anti-duplicados.
- **Riesgo de ban:** el issue **#1869 "High number of bans on WhatsApp!"** (abierto
  5-oct-2025, cerrado como "Stale" sin solución) reporta un usuario con **5 bots baneados
  en una semana, dos de ellos con 3+ años funcionando sin problemas**, en v6.7.19 y
  v7.0.0-rc.5 por igual. No hay patrón predecible: meses sin problema o ban en una semana.
  Análisis de terceros (2025-2026) apuntan a que los modelos de Meta pesan: **ratio de
  respuesta** (<10% de respuestas = alto riesgo), distancia en el grafo de contactos
  (escribir a desconocidos) y timing robótico. Un bot **solo-respondedor** como el de
  destaperapido está en el perfil de MENOR riesgo, pero el riesgo nunca es cero: usar
  Baileys viola los ToS y el ban puede ser permanente y sin aviso.
- **Riesgo extra de ecosistema:** hay reportes (no verificados de primera mano en esta
  investigación) de paquetes npm "anti-ban" maliciosos que exfiltran credenciales de
  sesión. Regla práctica: cero dependencias de terceros alrededor de Baileys que toquen
  la carpeta `auth/`.

---

## (b) Alternativas no oficiales

Todas van sobre uno de dos caminos: (1) el **mismo protocolo websocket reverse-engineered**
que Baileys (o su equivalente en Go, `whatsmeow`), o (2) **Puppeteer sobre WhatsApp Web**.
Ninguna elimina el riesgo de ban ni la fragilidad de la sesión local; cambia el empaque.

| Proyecto | Stars | Issues abiertos | Último push | Licencia | Base técnica |
|---|---|---|---|---|---|
| whatsapp-web.js (pedroslopez) | 22.248 | 81 | 2026-07-19 | Apache-2.0 | Puppeteer (navegador) |
| Evolution API (EvolutionAPI) | 9.028 | 150 | 2026-07-14 | Apache-2.0 + cláusulas de marca | Baileys por debajo; también Cloud API oficial |
| WAHA (devlikeapro) | 7.073 | 447 | 2026-07-22 | Apache-2.0 | 3 motores: WEBJS (navegador), NOWEB (websocket Node), GOWS (whatsmeow/Go) |
| WPPConnect (wppconnect-team) | 3.364 | 38 | 2026-07-23 | Propia ("Other") | WhatsApp Web exportado a Node |

(Cifras exactas de la API de GitHub, 23-jul-2026.)

- **whatsapp-web.js:** el más popular y mantenido, pero al ir por navegador es pesado
  (Chrome headless por sesión) y se rompe cuando WhatsApp Web cambia. Sufre bans igual:
  issues #532 ("account banned (frequently)"), #2052 (usar listas/botones = ban), #2701,
  #3250 (cuentas bloqueadas por spam con solo 7 mensajes/hora; usuarios que perdieron 10+
  cuentas). Su propia guía admite que WhatsApp no permite clientes no oficiales.
- **Evolution API:** el estándar de facto en Brasil para montar "WhatsApp como API REST".
  Dato clave: **por debajo usa Baileys** (hereda TODOS sus males — de hecho parchean
  eventos fallidos de Baileys en PRs como #1660) **pero también soporta la Cloud API
  oficial de Meta como segundo conector**. Eso lo vuelve un puente interesante: misma API
  REST propia, motor conmutable no-oficial ↔ oficial. Trae integraciones (Chatwoot,
  Typebot, OpenAI, colas). Costo: gratis, self-hosted.
- **WAHA:** REST API con motor a elección; GOWS usa whatsmeow (Go), más liviano que
  Puppeteer. Cambio de modelo reciente: desde la versión **2026.6.1 las features "Plus"
  pasaron al Core gratuito** (antes Plus ~US$19/mes); queda un tier "Community" de US$5/mes
  como donación. Ojo: 447 issues abiertos, la cifra más alta de la tabla en proporción.
- **WPPConnect:** comunidad brasileña activa (push de hoy), pero la más chica de las
  cuatro y con licencia propia.

**Conclusión (b):** migrar de Baileys a otra librería no oficial NO resuelve nada de fondo:
mismo protocolo, misma sesión Signal local corruptible, mismo ban posible. La única
alternativa cualitativamente distinta es la vía oficial. Evolution API es el único "híbrido"
que permite tener ambas detrás de una misma API.

---

## (c) La vía oficial: WhatsApp Business Cloud API (Meta)

### Modelo de cobro 2025–2026 (verificado en docs oficiales de Meta)

- Desde el **1-jul-2025** Meta cobra **por mensaje de plantilla ENTREGADO**, no por
  conversación ("You are only charged when a template message is delivered").
- **Gratis, textual de la doc de Meta:**
  1. **"All non-template messages are free"** dentro de la **ventana de servicio de 24 h**
     (se abre cada vez que el cliente te escribe). O sea: **responder al cliente dentro de
     24 h es gratis e ilimitado** — el flujo completo de cotización del bot saldría US$0.
  2. **"Utility templates delivered within an open customer service window are free"** —
     confirmaciones/avisos con plantilla utility dentro de la ventana: también gratis.
  3. **Free entry point de 72 h**: si el cliente llega por anuncio click-to-WhatsApp o
     botón de página de Facebook, TODO es gratis por 72 h.
- **Lo que se paga:** plantillas fuera de ventana, por categoría y país del destinatario.
  Chile no tiene fila propia en el rate card: cae en **"Rest of Latin America"**:
  - **Marketing: US$0,074/mensaje** (~**CLP $69** al cambio 935,86 CLP/USD del 22-jul-2026)
  - **Utility: US$0,0113/mensaje** (~**CLP $11**)
  - **Authentication: US$0,0113/mensaje** (~**CLP $11**)
  - Desde 2025 Meta factura en **CLP** (moneda local agregada al sistema de billing).
- Meta **no cobra fee de plataforma** por usar la Cloud API directo (se paga solo lo
  anterior). Los BSP (Twilio, 360dialog, Wati, etc.) agregan cargos propios por mensaje o
  mensualidad — para un negocio chico con equipo técnico, ir **directo a Meta** es lo
  barato.

### Números aterrizados a destaperapido

El bot es respondedor puro: el cliente escribe primero → ventana de 24 h → cotización,
fotos, PDF, todo **gratis**. Costos reales serían solo:
- Aviso al repartidor por entrega (plantilla utility fuera de ventana): ~CLP $11 c/u →
  200 entregas/mes ≈ **CLP $2.100/mes**.
- Recordatorios 💤 post-24 h ("¿sigues interesado?"): Meta los clasificaría marketing →
  ~CLP $69 c/u → 100/mes ≈ **CLP $6.900/mes**.
Orden de magnitud total: **menos de CLP $10.000/mes**.

### La ventana de 24 horas (regla de oro)

- Cliente escribe → tienes 24 h para responder **lo que quieras, en texto libre, gratis**.
- Pasadas las 24 h sin mensaje nuevo del cliente, SOLO puedes iniciar con **plantilla
  pre-aprobada** (aprobación de Meta, minutos-horas) y pagas la tarifa por categoría.
- Cada mensaje nuevo del cliente reabre la ventana.

### Requisitos

- Cuenta en **Meta Business Manager** (business.facebook.com) con datos reales.
- **Número dedicado** que pueda recibir SMS/llamada de verificación. Novedad importante:
  desde **mayo-2025 existe "Coexistence"** (ya disponible globalmente): el MISMO número
  puede estar en la app WhatsApp Business del teléfono **y** en la Cloud API a la vez, con
  espejo bidireccional por webhooks — ya no hay que borrar la cuenta de la app para migrar.
- **Sin verificación de empresa**: partes limitado a **250 conversaciones iniciadas por la
  empresa cada 24 h** (las RESPUESTAS a clientes no tienen ese límite). Con verificación de
  empresa + buena calidad, escala automático 1.000 → 10.000 → 100.000 → ilimitado.
- Display name aprobado por Meta.

### Qué gana en estabilidad (y qué pierde)

Gana:
- **Cero ban por ToS**: es la única vía permitida; el riesgo de amanecer con el número
  muerto desaparece.
- **Cero "ciego"**: webhooks HTTPS con entrega confirmada y reintentos de Meta; no hay
  sesión Signal local, no hay `auth/` corruptible, no hay Bad MAC, no hay 440/428/515, no
  hay QR ni pairing, no hay "Esperando el mensaje", no hay reportar-enviado-sin-entregar.
- Estados de mensaje confiables (sent/delivered/read/failed) por webhook.
- **Instagram DM por la misma casa**: la Instagram Messaging API es de la misma familia
  Graph API/webhooks de Meta — el plan multi-canal de dixdybot calza natural.
Pierde:
- Texto libre solo dentro de la ventana de 24 h (fuera: plantillas pagadas).
- **Grupos**: la Groups API existe desde oct-2025 pero solo para cuentas con **Official
  Business Account (OBA)** — en la práctica, fuera del alcance de un negocio chico. Si un
  flujo depende de grupos, eso hoy solo lo da la vía no oficial.
- Requiere un endpoint HTTPS público para webhooks (el Mac necesitaría un túnel tipo
  Cloudflare Tunnel/Tailscale Funnel, o un Worker intermedio — encaja con la doctrina
  DIXDY de reutilizar los workers de Cloudflare existentes).

---

## (d) Recomendación honesta por etapas (negocio chico que hoy usa Baileys)

**Etapa 0 — ya mismo, sin plata:** quedarse en Baileys PERO endurecer lo que ya existe:
fijar versión (rama 6.7.x o un rc concreto de v7 con mapeos LID por el tema Bad MAC),
respaldo periódico de `auth/` con escritura atómica, dedup persistente (ya está:
`envios.jsonl`), gating anti-ban (ya está), y mantener el perfil de bajo riesgo: SOLO
responder, nunca iniciar en frío a desconocidos. Asumir por escrito que el número puede
morir cualquier día y tener plan B (número de respaldo + aviso en la web).

**Etapa 1 — este trimestre, costo ~US$0:** abrir la cuenta Cloud API en paralelo SIN tocar
el bot vivo: Meta Business Manager + verificación de empresa (destaperapido tiene giro
real: trivial), número secundario o Coexistence sobre el actual, webhook de prueba en un
Worker de Cloudflare (infra que DIXDY ya opera), 2-3 plantillas utility aprobadas. Esto
compra la opción de migrar en horas, no semanas, el día que Baileys falle o llegue un ban.

**Etapa 2 — al rediseñar dixdybot:** diseñar el core **agnóstico del canal** (los "caminos"
y el cerebro no deben saber si el mensaje entró por Baileys, Cloud API o Instagram). Un
adaptador por canal. Mover el flujo de cotización inbound al oficial (gratis, estable) y
dejar Baileys solo para lo que el oficial no cubre (grupos, si se usan). Evolution API es
el ejemplo a estudiar de esa arquitectura dual, aunque para DIXDY conviene el adaptador
propio y liviano antes que adoptar otra plataforma completa (doctrina: no reinventar, pero
tampoco adoptar infraestructura ajena pesada).

**Etapa 3 — multi-canal:** con el core agnóstico, Instagram DM entra por la misma Graph
API de Meta con otro adaptador. El "pausar chat y pedir la regla al humano" funciona igual
en ambos canales porque vive en el core, no en el transporte.

**Lo que NO haría:** migrar de Baileys a whatsapp-web.js/WPPConnect/WAHA esperando
estabilidad — es el mismo riesgo con otro empaque; y contratar un BSP con mensualidad
(Wati, etc.) teniendo capacidad técnica para ir directo a Meta.

---

## Fuentes

- https://github.com/WhiskeySockets/Baileys y https://api.github.com/repos/WhiskeySockets/Baileys (stats exactas)
- https://api.github.com/repos/WhiskeySockets/Baileys/releases (rc13 21-may-2026, rc12 seguridad, rc10 LID)
- npm registry: registry.npmjs.org/baileys/latest (7.0.0-rc13) y api.npmjs.org (descargas semanales)
- Issues Baileys: #1869 (bans masivos oct-2025), #2234/#635/#1725/#2110 (Bad MAC), #502/#1933 (440), #141/#313/#1218 (515), #568 (duplicados), #1963 (enviado-sin-entregar), #1643 (Waiting for message), #1692 (JID incorrecto)
- Búsqueda GitHub: 36 issues "Bad MAC", 54 issues "stream errored" en el repo
- https://baileys.wiki/docs/api/enumerations/DisconnectReason/ (significado 440/428/515)
- https://api.github.com/repos/pedroslopez/whatsapp-web.js · /wppconnect-team/wppconnect · /EvolutionAPI/evolution-api · /devlikeapro/waha
- Issues whatsapp-web.js: #532, #2052, #2701, #3250 (bans)
- https://github.com/evolution-foundation/evolution-api (dual Baileys + Cloud API, licencia)
- https://github.com/devlikeapro/waha y releases (Plus→Core gratis en 2026.6.1)
- https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing (per-message jul-2025, gratis en ventana 24h, utility gratis en ventana, 72h entry point)
- https://flowcall.co/blog/whatsapp-business-api-pricing-2026 (rate card: Rest of Latin America 0.074 / 0.0113 / 0.0113 USD)
- https://www.authgear.com/post/whatsapp-api-pricing/ (confirma servicio gratis en ventana)
- https://sleekflow.io/blog/whatsapp-business-price (facturación en CLP disponible)
- https://developers.facebook.com/documentation/business-messaging/whatsapp/groups (Groups API, solo OBA)
- https://support.wati.io/en/articles/11822402-introducing-whatsapp-coexistence y https://clientify.com/en/blog/communication/whatsapp-coexistence (Coexistence may-2025, global)
- https://ayuda.clientify.com/es/articles/8791508 y https://ghostlock.com/whatsapp-cloud-api-guia/ (límite 250/día sin verificar, escalado 1k/10k/100k)
- https://wise.com/us/currency-converter/usd-to-clp-rate/history (935,86 CLP/USD al 22-jul-2026)
