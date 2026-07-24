# KIT META — el papeleo de WhatsApp oficial, paso a paso

Guía para Alejandro (sin tecnicismos). Es UNA sesión de **~45–60 minutos de clicks**,
más esperas de Meta que corren solas (1–3 días). No hace falta cuenta de nadie para
leer esto: todo está precargado y decidido; tú solo haces los clicks que Meta exige
que haga un humano.

Fuentes: investigación verificada jul-2026 (`investigacion-dixdybot/ronda2/papeleo-meta.md`
y `ronda3/coexistence.md`). El código ya está listo y probado en el molde
(`dixdybot/src/canales/wa-cloud/` — sin desplegar, no gasta nada).

---

## Reparto del trabajo, en una tabla

| Paso | Qué es | Quién | Tiempo |
|---|---|---|---|
| 0 | Juntar datos y papeles | 🧑 Tú (con mi checklist) | 10 min |
| 1 | Business Manager (la "carpeta empresa" en Meta) | 🧑 Tú | 10–15 min |
| 2 | La app de WhatsApp en Meta | 🧑 Tú | 10 min |
| 3 | Número de PRUEBA (regalo de Meta) | 🧑 2 clicks · 🤖 yo pruebo todo | 5 min |
| 4 | El número real (decisión: nuevo vs el actual) | 🧑 Decisión + OTP/QR | 10–30 min |
| 5 | Display name (el nombre que ve el cliente) | 🧑 Escribirlo (yo te lo dejo redactado) | 2 min |
| 6 | Webhook (la dirección donde Meta nos avisa) | 🧑 Pegar 2 textos que yo te doy | 5 min |
| 7 | Token permanente (la llave para que yo opere) | 🧑 Tú (clicks) → me la entregas | 10 min |
| 8 | Expediente de verificación (papeles chilenos) | 🧑 Subir 1 PDF que yo armo | 10 min |
| — | Todo lo demás (plantillas, pruebas, conexión al bot) | 🤖 Yo, con el token | 0 min tuyos |

**Regla de oro:** si una pantalla no calza con lo descrito aquí, no adivines — me
preguntas y seguimos juntos. Nada de esto puede "romper" el bot actual: el bot vivo
(Baileys) no se toca en ningún paso de esta guía.

---

## Paso 0 — Junta esto ANTES de sentarte (10 min)

- **Tu cuenta personal de Facebook** con clave y el teléfono a mano (Meta pide
  verificación en dos pasos; puede ser la del dueño del negocio o la tuya — ver el
  gotcha del paso 1).
- **Datos legales del negocio** (deben calzar entre sí y con la web):
  - Razón social exacta: `[RELLENAR — como aparece en el SII]`
  - RUT de la empresa: `[RELLENAR]`
  - Dirección comercial: `[RELLENAR]`
  - Web: `https://destaperapido.cl`
  - Correo del dominio (no Gmail): `contacto@destaperapido.cl` o el que exista.
- **Los dos papeles** para el paso 8 (pueden juntarse después, no bloquean):
  1. Constitución de la sociedad o certificado del **Registro de Empresas y
     Sociedades** ("Tu empresa en un día") con vigencia.
  2. **e-RUT / RUT de la empresa** del SII.
  Me los pasas y yo los uno en UN solo PDF con lo importante resaltado (el formato
  que recomiendan las guías chilenas — así Meta no lo rechaza por "papeles confusos").

---

## Paso 1 — Business Manager: la carpeta empresa (10–15 min) 🧑

1. Entra a **business.facebook.com** con la cuenta personal de Facebook.
2. Botón **"Crear cuenta"** (o "Crear portafolio comercial"). La pantalla pide tres
   cosas: nombre del negocio, tu nombre, y un correo del negocio.
   - Nombre del negocio: la **razón social** (no un nombre de fantasía distinto).
   - Correo: el **del dominio** (llega un mail de confirmación — confírmalo).
3. Dentro, en **Configuración del negocio → Información del negocio**, completa
   dirección y web con los datos del paso 0, idénticos a como salen en la web.

> ⚠️ **Gotcha grande (decisión para siempre):** si más adelante conectamos el
> número ACTUAL por Coexistence, el Business Manager que elijas queda **fijo para
> siempre** para ese número — no se puede cambiar después. Por eso este BM debe ser
> el del NEGOCIO con sus datos reales, no uno improvisado "para probar".

> Si el negocio YA tiene Business Manager (por anuncios de Meta, etc.): usa ese,
> no crees otro. Solo revisa que los datos legales estén completos.

## Paso 2 — La app de WhatsApp (10 min) 🧑

1. Entra a **developers.facebook.com** con la misma cuenta → botón **"Mis apps"** →
   **"Crear app"**.
2. Cuando pregunte el caso de uso, elige **"WhatsApp"** (a veces aparece como
   "Otro" → tipo "Negocios" → y luego se agrega el producto WhatsApp — cualquiera
   de los dos caminos vale).
3. Nombre de la app: `dixdybot destaperapido` (da igual, es interno). Correo: el
   del dominio. **Vincúlala al Business Manager del paso 1** cuando lo pida.
4. Acepta los términos de la plataforma de WhatsApp cuando aparezcan.

Al terminar verás el panel de la app con un menú lateral que dice **WhatsApp →
"Configuración de la API"** (API Setup). Esa pantalla es la base de los pasos 3–6.

## Paso 3 — Número de prueba y primer mensaje (5 min) 🧑→🤖

En **WhatsApp → Configuración de la API** Meta te REGALA un número de prueba y un
token temporal de 24 horas.

1. En esa pantalla, en "Para" (recipient), agrega tu número personal y confirma el
   código que te llega por WhatsApp.
2. Copia el **token temporal** (botón de copiar junto a un texto larguísimo que
   empieza con `EAA...`) y **pégamelo**.

Con eso yo hago la prueba de humo el mismo día (mensaje de ida y vuelta, webhook
sonando) SIN tocar ningún número real. Si algo del montaje está mal, lo descubrimos
aquí, gratis y sin riesgo.

## Paso 4 — El número real: la decisión (10–30 min) 🧑

Dos opciones. **No hay apuro**: los pasos 5–8 se pueden dejar listos con el número
de prueba, y esta decisión se toma con calma (fecha límite que nos pusimos: 30-sep,
con piloto antes).

**Opción A — Número NUEVO (chip dedicado a la API):**
- ✅ Simple y directo con Meta, sin intermediarios; verificas por SMS en 10 min.
- ✅ Cero riesgo para el número actual; puede ganarse la verificación completa y el escalado.
- ❌ Los clientes ya escriben al número de siempre: habría que "mudar" a la clientela.

**Opción B — Coexistence (el número ACTUAL, app y bot a la vez):**
- ✅ Se conserva el número que todos conocen Y la app en el teléfono del dueño (él
  sigue atendiendo como siempre; el bot va por la vía oficial, sin riesgo de ban).
- ❌ Letra chica permanente: abrir la app al menos cada 14 días, sin listas de
  difusión, y ese número queda amarrado a este Business Manager para siempre.
- ❌ Se conecta a través de un partner autorizado (con costo mensual o papeleo
  extra) y **el momento de conexión desconecta la sesión Baileys del bot actual** —
  se hace en ventana de bajo tráfico y con piloto en un número secundario primero.

**Mi recomendación (de la investigación):** para destaperapido, Coexistence es la
ruta correcta a futuro — pero como decisión con piloto, no como salto. HOY basta con
el número de prueba; si quieres avanzar sin esperar la decisión, la opción A con un
chip nuevo también deja todo operativo en 10 minutos.

Si eliges A: en "Configuración de la API" → **"Agregar número de teléfono"**,
completa los datos, elige verificación por **SMS**, escribe el código que llega. Listo.

## Paso 5 — Display name: el nombre que ve el cliente (2 min) 🧑

Al registrar el número, Meta pide el **nombre para mostrar**. Escribe:

> `Destape Rápido`

Reglas que ya cumplí al redactarlo: es el nombre real del negocio, coincide con la
web, sin emojis, sin MAYÚSCULAS completas, sin "ofertas" en el nombre. Meta lo
revisa: puede aprobarse en minutos o demorar hasta 48 h (en Chile suele ser 1–2 días
hábiles). No hay que hacer nada mientras tanto.

## Paso 6 — Webhook: dónde nos avisa Meta (5 min) 🧑

El "webhook" es la dirección de internet donde Meta deja los mensajes que llegan.
**Esa dirección la fabrico yo** (es un mini-servidor gratis en Cloudflare que ya
está programado y probado; lo enciendo cuando toque este paso). Yo te entregaré dos
textos:

- **URL de callback:** `https://meta-buzon-destaperapido.[cuenta].workers.dev/webhook`
  (la exacta te la paso yo al encender el servidor)
- **Token de verificación:** un texto tipo clave que yo invento y te paso.

Tú solo:
1. En la app: menú **WhatsApp → Configuración** (Configuration) → sección
   **Webhook** → botón **"Editar"**.
2. Pega la URL en "URL de devolución de llamada" y el token en "Identificador de
   verificación" → **"Verificar y guardar"**. Si el botón da error, me avisas (el
   99% de las veces es un espacio de más al pegar).
3. En la misma pantalla, en la tabla de "Campos del webhook", busca la fila
   **`messages`** y apriétale **"Suscribirse"**.

## Paso 7 — Token permanente: la llave para que yo opere (10 min) 🧑

El token del paso 3 muere a las 24 h. El definitivo se crea así (esto es lo único
"escondido" de toda la guía — sigue la ruta con calma):

1. **business.facebook.com** → **Configuración del negocio** (engranaje) →
   columna izquierda: **Usuarios → Usuarios del sistema** → **"Agregar"**.
2. Nombre: `dixdybot` · Rol: **Administrador** → crear.
3. Con el usuario `dixdybot` seleccionado: botón **"Agregar activos"** →
   pestaña **Apps** → marca la app del paso 2 → activa **"Administrar app"
   (control total)** → guardar.
   - Repite "Agregar activos" → **Cuentas de WhatsApp** → marca la cuenta de
     WhatsApp del negocio → control total → guardar. (Si esa pestaña aún no
     aparece, no importa: se hace después, avísame.)
4. Botón **"Generar token"** (o "Generar nuevo token"):
   - App: la del paso 2.
   - Caducidad: **"Nunca"** (60 días NO — queremos la permanente).
   - Permisos — marca EXACTAMENTE estos tres (los demás, no):
     - `whatsapp_business_messaging`
     - `whatsapp_business_management`
     - `business_management`
5. **"Generar token"** → aparece UNA sola vez. Cópialo entero.

**Entrega segura:** no lo mandes por correo ni WhatsApp. Pégalo directo en el
archivo privado del clon (`scripts/.env.local`, línea `META_WA_TOKEN=...`) o
tenlo copiado y me avisas en la sesión — yo te digo dónde va y queda guardado
fuera de git.

## Paso 8 — Expediente de verificación del negocio (10 min) 🧑 (+🤖 el PDF)

**No es obligatoria para partir**: responder a clientes que escriben primero es
gratis e ilimitado sin verificar. Sirve para escalar (sin verificar hay tope de 250
conversaciones INICIADAS por nosotros al día) y da robustez a la cuenta. Como en
Chile demora 12–72 h hábiles, conviene dejarla andando temprano.

1. Me pasas los dos papeles del paso 0 → yo armo **UN solo PDF**: constitución +
   e-RUT, con razón social y RUT resaltados.
2. Reviso antes que la web muestre la razón social (si falta, la agrego yo al pie
   de página del sitio — coherencia web ↔ papeles es lo que Meta revisa).
3. Tú: **business.facebook.com → Configuración del negocio → Centro de seguridad**
   → botón **"Iniciar verificación"**. Confirma los datos (deben salir idénticos a
   los papeles), sube el PDF, y elige confirmar por **correo del dominio**.
4. Si Meta pide algo más, te llega un correo — me lo reenvías y lo resolvemos.

---

## Qué hago YO después, con el token (tú: nada)

1. Despliego el buzón del webhook en Cloudflare (gratis) y te doy la URL y el token
   del paso 6.
2. Registro el número en la API y dejo el perfil del negocio completo (foto, web,
   dirección, horario).
3. Creo por API las **plantillas** de mensajes (aviso al repartidor, recordatorio,
   reapertura de conversación) y espero su aprobación (minutos–24 h).
4. Conecto el canal oficial al bot nuevo (dixdybot) y pruebo ida y vuelta con mi
   número de prueba, sin tocar el bot vivo.
5. Dejo el monitoreo puesto: si Meta rechaza algo (nombre, plantilla, verificación),
   te aviso yo — no tienes que revisar nada.

**Lo único que siempre será tuyo:** cualquier cosa con PLATA (agregar tarjeta para
plantillas pagadas — solo hacen falta para escribir NOSOTROS primero fuera de la
ventana de 24 h) y las gestiones donde Meta exige un humano (estos clicks).

## Las esperas de Meta (corren solas)

| Qué | Cuánto |
|---|---|
| Display name | minutos – 48 h (Chile: 1–2 días hábiles típico) |
| Verificación del negocio | 12–72 h hábiles (hasta 5–14 días si los papeles van mal — por eso el PDF lo armo yo) |
| Plantillas de mensajes | minutos – 24 h |

**Total realista:** operativo respondiendo gratis el mismo día (con número de prueba
o el real); "fino" (nombre aprobado + plantillas + verificación) en 2–3 días.

## Gotchas — léelos una vez, evitan el 90 % de los dolores

- **El Business Manager del paso 1 queda amarrado para siempre** al número si
  usamos Coexistence. Créalo bien a la primera (datos reales del negocio).
- **El token del paso 7 aparece UNA vez.** Si se pierde, no es drama: se genera
  otro — pero mejor pegarlo al tiro donde te indico.
- **Verificar el negocio NO es requisito para partir.** Nadie quede esperando a
  Meta para que el bot responda: responder es gratis e ilimitado desde el día uno.
- **Coherencia total de datos:** razón social del BM = papeles del SII = pie de la
  web = correo del dominio. El 90 % de los rechazos chilenos de verificación son
  por datos que no calzan.
- **Coexistence desconecta el bot actual en el instante de conexión** (desvincula
  los "dispositivos acompañantes"). Jamás se hace un viernes a las 12 del día:
  ventana de bajo tráfico, con piloto previo en un número secundario, y Baileys
  queda de respaldo caliente 30–60 días.
- **El historial se sincroniza UNA sola vez** (hasta 6 meses de chats) y con
  ventana de 24 h. No dependemos de eso: nuestro historial maestro ya vive en el
  CRM propio.
- **La app del teléfono debe abrirse al menos cada 14 días** si hay Coexistence
  (el dueño la usa a diario — cumple de sobra, pero que se sepa: vacaciones largas
  con el teléfono apagado = se cae la conexión).
