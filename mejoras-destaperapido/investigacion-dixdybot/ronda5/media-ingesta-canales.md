# Media entrante/saliente por canal: Cloud API de Meta, Instagram, Baileys y correo — y el contrato de ingesta unificado

Investigación para dixdybot (E-plan mediano plazo: interfaz Canal multi-canal).
Fecha de verificación de TODOS los datos web: **2026-07-23** (fetch directo a docs de Meta y Cloudflare).
Datos locales verificados el 2026-07-23 leyendo el código vivo del bot y del correo-worker.

---

## (a) WhatsApp Cloud API — media ENTRANTE

### Cómo llega (webhook)

- El webhook `messages` trae un objeto por tipo (`image`, `audio`, `video`, `document`, `sticker`) con:
  `id` (media ID), `mime_type`, `sha256`, y según tipo `caption` (image/video/document), `filename` (document), `voice` (audio).
- **Cambio 2026 (clave):** desde el **12-nov-2025** (rollout gradual "over several weeks") el webhook incluye **también un campo `url` directo** (`https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=...`): "You can query this URL directly with your access token to download the media asset". Documentado en las páginas nuevas `developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/{image,audio,document}` (verificado 2026-07-23). El diseño NO debe asumir que el `url` siempre viene (rollout gradual): el camino canónico sigue siendo el media ID.
- Ejemplo real de audio (doc oficial, 2026-07-23): `"audio": {"mime_type": "audio/ogg; codecs=opus", "sha256": "...", "id": "1908647269898587", "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=133...", "voice": true}`.
  → **Las notas de voz llegan como `audio/ogg; codecs=opus` con `voice: true`** (audio "normal" reenviado trae `voice: false`/ausente).

### Cómo se descarga (camino por media ID)

1. `GET https://graph.facebook.com/<VER>/<MEDIA_ID>?phone_number_id=<PHONE_NUMBER_ID>` con header `Authorization: Bearer <token>` → responde `{messaging_product, url, mime_type, sha256, file_size, id}`.
2. `GET <url>` con el MISMO header `Authorization: Bearer` → binario ya **descifrado** (Meta descifra server-side). "If you omit your token, the request will fail."

### Caducidades (todas verificadas 2026-07-23 en `docs/whatsapp/cloud-api/reference/media`)

| Cosa | Vigencia |
|---|---|
| URL devuelta por GET /{media-id} (y la del webhook) | **5 minutos** ("Media URLs expire after 5 minutes"); se vuelve a pedir otra |
| Media ID que llega EN EL WEBHOOK | **7 días** ("Media IDs in webhooks expire after 7 days") |
| Media ID devuelto al SUBIR media (POST /media) | **30 días** |
| El archivo en servidores de Meta | "All media files sent through this API are encrypted and persist for **30 days**, unless they are deleted earlier" |

→ Regla de diseño: **descargar dentro de los 7 días** (en la práctica: al recibir el webhook), y tratar la URL como efímera de 5 min que se puede re-emitir pidiendo de nuevo el media ID.

### Límites de tamaño y formatos (Cloud API, verificado 2026-07-23)

| Tipo | Formatos | Máx |
|---|---|---|
| Imagen | JPEG, PNG (8-bit, RGB/RGBA) | **5 MB** |
| Audio | AAC, AMR, MP3, M4A, OGG ("OPUS codecs only; base audio/ogg not supported; **mono input only**") | **16 MB** |
| Video | MP4, 3GPP (solo H.264 + AAC) | **16 MB** |
| Documento | TXT, XLS(X), DOC(X), PPT(X), PDF | **100 MB** |
| Sticker | WebP | **100 KB** estático / **500 KB** animado |

## (b) WhatsApp Cloud API — media SALIENTE

- Dos vías en el objeto media del mensaje: `id` (subido antes con `POST /<PHONE_NUMBER_ID>/media`, multipart: `file`, `type`, `messaging_product=whatsapp`; el ID dura 30 días y es **reutilizable**) o `link` (URL en "your public server"). Doc oficial (image-messages, 2026-07-23): "For better performance, we recommend using `id`" → **upload-primero es lo recomendado**; el link lo descarga Meta y debe ser público.
- `caption` opcional en image/video/document (máx **1024 caracteres**); `filename` en document. Audio y sticker no llevan caption.
- Mismos límites de tamaño/formato de la tabla anterior (aplican en ambas direcciones).
- **Plantillas con header multimedia** (fuera de la ventana de 24 h): la plantilla se CREA con `{"type":"HEADER","format":"IMAGE|VIDEO|DOCUMENT|GIF","example":{"header_handle":["4::YX..."]}}` donde el handle sale de subir el ejemplo por la **Resumable Upload API** ("You must upload all media with the Resumable Upload API"); al ENVIARLA, el componente header lleva un MediaObject normal (`image`/`video`/`document` con `id` o `link`). Verificado 2026-07-23 en business-management-api/message-templates/components y reference/messages (HeaderObject).

## (c) Instagram Messaging API

- **Entrante:** webhook `messages` con array `attachments`; cada uno `{"type": "...", "payload": {"url": "<CDN>"}}` — **URL directa, sin indirection de media ID** (a diferencia de WhatsApp). Tipos documentados para IG: `image` (incluye gif), `video`, **`audio` (sí hay mensajes de voz en IG DM)**, `file`, `share`, `story_mention`, `reel`/`ig_reel` (con `reel_video_id` y `title`), `ig_post`, `sticker` (`sticker_id`). Verificado 2026-07-23 en messenger-platform/reference/webhook-events/messages y messenger-platform/instagram/features/webhook. **La doc NO publica cuánto dura la URL del CDN** (lookaside firmada) → tratarla como efímera y descargar al tiro. "Disappearing media (view once, allow replay) is not supported on Instagram media webhooks".
- **Saliente** (messenger-platform/instagram/features/send-message, 2026-07-23): attachment con `payload.url` o `payload.attachment_id` (se pueden mezclar ambos métodos). Tipos y topes: **imagen (png, jpeg) 8 MB; audio (aac, m4a, wav, mp4) 25 MB; video (mp4, ogg, avi, mov, webm) 25 MB; archivo (pdf) 25 MB; sticker `like_heart`**. GIF no aparece como tipo de envío propio. Texto máx 1000 caracteres/1000 bytes UTF-8. Nota de acceso: "Apps with Standard Access can only send messages to people that have a role on the app" (App Review para producción).

## (d) Cómo maneja media el bot ACTUAL (Baileys 6.7.23, instancia viva en `SaSS/destaperapido/whatsapp-bot`)

- **Entrante: HOY NO SE DESCARGA NADA.** `src/index.js:71-75` solo etiqueta: `imageMessage`→"📷 Foto", `videoMessage`→"🎥 Video", `documentMessage`→"📎 <fileName>", `audioMessage.ptt`→"🎤 Mensaje de voz", `stickerMessage`→"🙂 Sticker". El cerebro ve la etiqueta, no el contenido. (`ptt` de Baileys ≙ `voice` de Cloud API.)
- **Saliente:** PDFs de cotización como Buffer local: `{document: readFileSync(pdf), mimetype: "application/pdf", fileName}` (`src/outbox.js:76-80`, `src/integracion.js:617-621`) y la ficha como `{image: readFileSync(config.fichaImg)}` (`src/index.js:618`, `media/ficha-bano.jpeg`). Baileys cifra y sube el binario al CDN de WhatsApp por su cuenta.
- **Si mañana se quiere leer media entrante con Baileys:** `downloadContentFromMessage({mediaKey, directPath, url}, tipo)` (verificado en `node_modules/@whiskeysockets/baileys/lib/Utils/messages-media.js:388`): baja el **ciphertext** del CDN de WhatsApp (sin token) y lo **descifra localmente**: HKDF-expande el `mediaKey` del mensaje E2E a 112 bytes con info `"WhatsApp <Tipo> Keys"` → AES-CBC + verificación HMAC. Si el CDN ya expiró el archivo, existe re-upload request al emisor (`sock.updateMediaMessage`).
- **Diferencia clave vs Cloud API:** en Baileys el descifrado E2E es NUESTRO problema (mediaKey viaja en el mensaje; el CDN sirve ciphertext sin auth); en Cloud API **Meta ya entrega el binario descifrado** tras un GET autenticado con Bearer token. Y en Baileys no hay caducidad documentada de 7 días/5 min — hay expiración informal del CDN con re-upload.

## (e) Correo (correo-worker de Cloudflare)

- **Entrante:** Email Routing → handler `email()` → `PostalMime.parse(message.raw)` (`src/index.js:250`). **Los adjuntos entrantes HOY SE DESCARTAN**: a D1 solo van texto (cap 50 KB) y HTML (cap 100 KB); el correo original completo (con adjuntos) se reenvía al buzón humano con `message.forward(env.FORWARD_TO)`. PostalMime sí parsea adjuntos (buffer + mime + filename): capturarlos es agregar lectura de `parsed.attachments`, no infra nueva.
- **Saliente:** PDF de cotización guardado como base64 en D1 (`adjunto_b64`), servido por `/api/adjunto` y enviado vía **Resend** con `attachments: [{filename, content: <base64>}]` (`src/index.js:596-620`).
- **Límites que mandan (verificados 2026-07-23 en docs de Cloudflare):** Email Routing rechaza mensajes entrantes > **25 MiB**; Worker: **128 MB** de memoria por isolate, CPU 10 ms free / hasta 5 min paid ("complex handlers may exceed these limits" en free → EXCEEDED_CPU); **D1: fila/string/BLOB máx 2 MB** → un adjunto en `adjunto_b64` no puede pasar de ~**1.4 MB reales** (base64 infla +33 %). Adjuntos grandes → R2, no D1.

## Contrato de ingesta unificado — lo que la interfaz Canal debe exponer

Un solo shape para que el pipeline (cerebro, CRM, panel) no sepa de qué canal vino:

```js
// MediaEntrante — lo emite cada adaptador de Canal junto al mensaje
{
  tipo: "imagen" | "voz" | "audio" | "video" | "documento" | "sticker" | "otro",
  // "voz" ≠ "audio": WA lo marca (voice/ptt); en IG audio DM se asume "voz".
  mime: "audio/ogg; codecs=opus" | "image/jpeg" | ...,   // como lo declaró el canal
  tamanoBytes: 123456 | null,      // Cloud API lo da (file_size); Baileys (fileLength); IG no siempre
  nombreArchivo: "recibo.pdf" | null,  // solo documentos
  caption: "..." | null,
  sha256: "..." | null,            // Cloud API y Baileys lo traen; sirve de dedup
  caducaEn: epochMs | null,        // WA Cloud: ahora+7d (media ID webhook); IG/Baileys: null = "descarga ya"
  obtenerBinario(): Promise<Buffer>  // LAZY, bajo demanda; el adaptador resuelve el cómo
}
```

- `obtenerBinario()` encapsula la diferencia real entre canales: **Baileys** = bajar ciphertext + descifrar con mediaKey (y re-upload si expiró); **Cloud API** = GET /{media-id} → URL de 5 min → GET con Bearer (re-pedir URL si venció; usar el `url` del webhook como fast-path si vino); **IG** = GET directo al `payload.url` sin auth; **correo** = `parsed.attachments[i].content` ya en memoria. Errores tipados: `MediaCaducado` (re-pedible o no) y `MediaMuyGrande`.
- **Política de persistencia del pipeline (no del canal):** descargar y guardar en disco/R2 apenas interese (WA borra a 30 días y el ID webhook a 7; IG no documenta vigencia de URL), y guardar `sha256` para no bajar dos veces.
- **Saliente espejo (`enviarMedia`)**: `{tipo, mime, nombreArchivo, caption, origen: Buffer|urlPublica}` + tabla de topes por canal (WA: 5/16/16/100 MB, caption 1024; IG: 8/25/25/25 MB, texto 1000; correo: adjunto D1 ≤ ~1.4 MB o R2). El adaptador decide upload-primero (WA recomienda `id`; el media ID subido dura 30 días y es cacheable por cliente — la ficha/PDF frecuentes se suben UNA vez) vs link vs buffer (Baileys). Plantillas WA con header multimedia quedan como capacidad exclusiva del adaptador Cloud API (Resumable Upload API), invisible para el pipeline.

## Fuentes

- https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media (GET media, expiraciones, tabla de tipos/tamaños; 2026-07-23)
- https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/audio (voice:true, ogg opus, url en webhook; 2026-07-23)
- https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/image y .../document (url rollout 12-nov-2025; 2026-07-23)
- https://developers.facebook.com/docs/whatsapp/cloud-api/messages/image-messages (id vs link, caption 1024; 2026-07-23)
- https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages (MediaObject id|link, HeaderObject; 2026-07-23)
- https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates/components (header_handle, Resumable Upload API; 2026-07-23)
- https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/messages/ (attachments IG/Messenger; 2026-07-23)
- https://developers.facebook.com/docs/messenger-platform/instagram/features/send-message (topes IG; 2026-07-23)
- https://developers.facebook.com/docs/messenger-platform/instagram/features/webhook (attachments IG, view-once no soportado; 2026-07-23)
- https://developers.cloudflare.com/email-routing/limits/ · https://developers.cloudflare.com/workers/platform/limits/ · https://developers.cloudflare.com/d1/platform/limits/ (2026-07-23)
- Código local: `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/src/{index.js,outbox.js,integracion.js}`, `node_modules/@whiskeysockets/baileys/lib/Utils/messages-media.js` (v6.7.23), `/Users/alejandroriveracarrasco/SaSS/DIXDY/correo-worker/src/index.js`
