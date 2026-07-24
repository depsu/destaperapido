# El papeleo de Meta, paso a paso, y cuánto puede automatizar la IA

Investigación web del 23-jul-2026 para dixdybot (DIXDY / destaperapido.cl).
Complementa `mejoras-destaperapido/investigacion-dixdybot/canales-whatsapp-2026.md` y
`multicanal-instagram-plataformas.md` (ambos del 23-jul-2026). Cada dato lleva la fecha
de su fuente. Lo que NO pude verificar está marcado como tal.

**Respuesta corta al dueño:** sí, se puede agilizar mucho. El papeleo de Meta para un
negocio chico chileno son ~30–60 minutos de clicks humanos repartidos en 1–3 días de
esperas, y la IA puede dejar precargado o ejecutar por API el ~70% del trabajo. La vía
más sólida es abrir la Cloud API **en paralelo** (sin tocar el bot vivo), con
**Coexistence** sobre el mismo número cuando toque migrar. Baileys sigue siendo el
arranque en el día para clientes nuevos: el patrón dual es viable y Evolution API lo
practica a escala.

---

## (a) Checklist EXACTO 2026: negocio chico chileno → WhatsApp Cloud API

Flujo "directo a Meta" (sin BSP), verificado contra la doc oficial de Meta
(developers.facebook.com "Get Started", consultada jul-2026) y guías 2026.

| # | Paso | Tiempo real | ¿Quién? |
|---|------|-------------|---------|
| 1 | **Meta Business Manager / portafolio** en business.facebook.com (exige cuenta personal de Facebook del dueño o de Alejandro; datos legales reales: razón social, dirección, web, correo del dominio) | 10–15 min | 🧑 Humano sí-o-sí (login FB + 2FA). 🤖 IA precarga: textos exactos a pegar, coherencia web↔razón social |
| 2 | **App de Meta** en developers.facebook.com con caso de uso "WhatsApp", conectada al portafolio | 10–15 min | 🧑 Clicks de creación y aceptar términos. 🤖 IA guía pantalla a pantalla |
| 3 | **Número de prueba + token temporal**: Meta regala un número de test y un token de 24 h; primer mensaje de prueba | 5–10 min | 🤖 IA casi todo (llamadas a Graph API); 🧑 solo copiar el token |
| 4 | **Número real**: (A) número nuevo/secundario → verificación por SMS o llamada, minutos; (B) **el MISMO número actual vía Coexistence** → ver flujo abajo | A: 10 min · B: 15–30 min | 🧑 Recibir el SMS/OTP o escanear el QR. 🤖 IA registra el número por API una vez verificado |
| 5 | **Display name**: se propone al registrar el número; Meta lo revisa | Aprobación típica: minutos–48 h (guías chilenas 2026 hablan de 1–2 días hábiles tras verificación) | 🤖 IA lo deja escrito según las reglas de nombres; 🧑 nada extra |
| 6 | **Webhook**: endpoint HTTPS con verify token + suscripción al campo `messages` | 15–30 min | 🤖 IA al 100% (Worker de Cloudflare, patrón correo-worker de DIXDY, y la suscripción va por API/UI) |
| 7 | **Token permanente**: crear System User en Business Settings → generar token con `whatsapp_business_messaging`, `whatsapp_business_management`, `business_management` | 10 min | 🧑 Clicks en Business Settings (UI). 🤖 IA dicta exactamente qué marcar y guarda el token en `.env.local` |
| 8 | **Verificación del negocio** (opcional para partir, ver abajo): Security Centre → subir documentos | Chile: 12–72 h hábiles típico; hasta 5–14 días si los papeles vienen mal (fuentes 2026) | 🧑 Subir PDF y responder el contacto de Meta. 🤖 IA arma el PDF único con constitución + RUT resaltados (formato que recomiendan las guías chilenas) |
| 9 | **Plantillas utility** (aviso a repartidor, recordatorio): crear 2–3 | Creación por API: minutos; revisión de Meta: hasta 24 h (doc oficial, jul-2026), típicamente minutos–horas | 🤖 IA redacta y crea por API; 🧑 nada |
| 10 | **Medio de pago** (tarjeta) en el WABA — solo hace falta para plantillas pagadas fuera de ventana; responder dentro de 24 h es gratis | 5 min | 🧑 Humano sí-o-sí (plata → regla Guardián: OK de Alejandro/dueño) |

**Total realista:** 1 sesión humana de ~45 min + esperas (display name hasta 48 h,
verificación 1–3 días, plantillas hasta 24 h). **Operativo respondiendo gratis el mismo
día** si se parte con número de prueba o Coexistence; "fino" (nombre aprobado +
plantillas) en 2–3 días.

### ¿La verificación del negocio es obligatoria?

**No para partir.** Reglas 2026 (Meta messaging limits + ActiveCampaign/Chatarmin,
consultadas jul-2026):

- **Responder a clientes que escriben primero: sin límite y gratis** dentro de la
  ventana de 24 h. El bot respondedor de destaperapido funciona entero SIN verificación.
- Sin verificar: máx **250 conversaciones INICIADAS por la empresa** cada 24 h (con
  display name aprobado). Con verificación: escala 1.000 → 10.000 → 100.000 → ilimitado.
- La verificación exige (guías chilenas 2026, Cognitiva/AsistChat): documento legal de
  registro (constitución / Registro de Empresas y Sociedades), **RUT de la empresa**
  coherente con el admin del Business Manager, web con la razón social visible y correo
  del dominio. Demora reportada en Chile: **12–72 h hábiles** (otras fuentes: 1–5 días
  hábiles, hasta 14 si hay que reintentar).

### El flujo Coexistence (mismo número, app + API a la vez) — detalle exacto

Fuentes: docs 360dialog (consultadas jul-2026), TimelinesAI (actualizado mar-2026),
chakrahq (2026). Existe desde may-2025; **desde may-2026 disponible en casi todo el
mundo** (exclusiones confirmadas a inicios de 2026: Nigeria y Sudáfrica; Chile OK).

Elegibilidad:
- Número registrado en la **app WhatsApp Business** (no la personal) con **≥7 días de
  uso activo** (recomiendan 1–2 meses; destaperapido lleva meses: califica).
- App versión ≥2.24.17 (en la práctica: "la última"), teléfono con cámara.
- Un Business Manager con datos legales completos. **OJO: el Business Manager elegido
  queda fijo para siempre** para ese número (no se puede cambiar después).

Flujo (vía Embedded Signup de un partner, o el flujo directo de Meta):
1. En el signup elegir "conectar mi app WhatsApp Business existente" y confirmar el número.
2. Llega un mensaje de WhatsApp al teléfono → tocar → **escanear QR** (o código).
3. Consentir la sincronización de historial/contactos (opcional).
4. Confirmar datos del WABA → el número queda vivo en app + API. Minutos.

Qué sincroniza: **hasta 6 meses de chats 1:1** y contactos (la sync toma minutos).
NO sincroniza: grupos ni listas de difusión.

Limitaciones permanentes de una cuenta Coexistence (360dialog, jul-2026):
- **Hay que abrir la app en el teléfono al menos cada 13–14 días** o se cae la conexión API.
- Desinstalar la app = desconexión. El teléfono sigue siendo pieza viva (¡igual que hoy!).
- **Sin verificación estándar del negocio** y **sin Official Business Account** (check
  azul) — es decir, Coexistence ≠ camino para escalar marketing masivo. Para un bot
  respondedor, irrelevante.
- Tope 20 msg/segundo; sin migración del número entre WABAs; sin editar/borrar mensajes,
  sin "ver una vez", sin ubicación en vivo en chats 1:1.
- Al onboardear se **desvinculan todos los dispositivos acompañantes** (esto mataría la
  sesión Baileys en ese momento); después solo se pueden re-vincular WhatsApp Web y Mac
  (Windows y WearOS no). Mensajes enviados desde dispositivos no soportados no generan
  webhook.

---

## (b) Embedded Signup y ser "Tech Provider": ¿le sirve a DIXDY?

Qué es (Meta docs + whautomate, abr-2026): **Embedded Signup** es el popup oficial de
Meta (Facebook Login for Business) que un partner incrusta en SU web para que un cliente
haga TODO el papeleo en un solo flujo: login FB → portafolio → crear WABA → número + OTP
→ permisos. **5–15 minutos por cliente** con los datos a mano. Es exactamente "onboardear
clientes de DIXDY en minutos".

Cambios 2025–2026 (importante, con fechas):
- Meta exigió que todo ISV que ofrece WhatsApp a terceros se enrole como **Tech Provider
  antes del 31-dic-2025** (docs de Infobip, consultadas jul-2026; una fuente menciona un
  hito previo el 30-jun-2025).
- Desde **abril-2026** Embedded Signup es la vía por defecto para altas nuevas en la
  plataforma (whautomate, actualizado abr-2026).

Requisitos para que DIXDY sea Tech Provider (doc oficial de Meta, consultada jul-2026):
1. Portafolio de Meta Business propio de DIXDY con datos exactos + **verificación del
   negocio de DIXDY** (2FA activada).
2. App con caso de uso WhatsApp.
3. **App Review con Advanced Access** para `whatsapp_business_messaging` y
   `whatsapp_business_management`: hay que presentar videos demo (enviar mensaje, crear
   plantilla) y documentación. Tiempo de App Review: Meta no publica plazo; la referencia
   de App Reviews similares es ~5–10 días hábiles (informe IG del 23-jul-2026); **no
   verifiqué un plazo específico de WhatsApp**.
4. Implementar Embedded Signup (SDK JS) + webhooks. Los clientes onboardeados agregan SU
   tarjeta a SU WABA (cada cliente paga sus mensajes a Meta, no DIXDY).

**Veredicto para DIXDY:** con 1–4 clientes NO hace falta. Regla clave verificada
(jul-2026): **Standard Access basta cuando la app accede a WABAs del MISMO negocio**
(o donde el admin tiene rol); Advanced Access + App Review se exige solo para WABAs de
terceros. O sea, el camino artesanal hoy es: crear la app DENTRO del Business Manager de
cada cliente (o con DIXDY como partner/admin del BM del cliente) → cero App Review, cero
programa Tech Provider. El enrolamiento como Tech Provider es la jugada de la etapa E6
(producto multi-cliente con onboarding self-service): vale la pena empezar la
verificación del negocio DIXDY con antelación porque es el paso lento.

---

## (c) ¿Directo a Meta o vía BSP? (costos 2026)

- **Directo a Meta: US$0 de plataforma.** Solo pagas plantillas entregadas fuera de
  ventana (Chile = "Rest of Latin America": marketing US$0,074, utility/auth US$0,0113;
  vigente desde el cambio a cobro por mensaje del 1-jul-2025; verificado jul-2026).
  Responder dentro de 24 h: gratis. A cambio pones tú el webhook y la operación —
  infraestructura que DIXDY ya tiene (Workers de Cloudflare).
- **360dialog:** €49/mes por número con paso-through de tarifas Meta "sin markup" (su
  pricing, jul-2026); una comparativa 2026 le atribuye además ~US$0,005/msg — las fuentes
  discrepan, verificar al contratar. Aporta: onboarding con Embedded Signup ya aprobado,
  soporte, Partner-led Business Verification (la vía "rápida y confiable" de verificar,
  según sus docs jul-2026).
- **Twilio:** sin mensualidad, ~US$0,005/msg (entrante y saliente) sobre la tarifa Meta
  (jul-2026). Cómodo si ya usas Twilio; para volumen de respuestas (que en directo son
  gratis) ese fee convierte lo gratis en pagado.
- **Gupshup y "capas gratis" de otros BSP:** no verifiqué precios 2026 concretos; no los
  afirmo. Las comparativas 2026 (SetSmart, whapi.cloud) advierten que el costo real con
  BSP termina 2–5× el de Meta directo por markups y mensualidades.

**Veredicto:** para DIXDY, **directo a Meta** — es gratis en el caso de uso respondedor,
y DIXDY tiene la capacidad técnica que un BSP le vendería a quien no la tiene. Un BSP
solo se justificaría por (1) prisa extrema con Embedded Signup ya montado, o (2)
Partner-led Business Verification si la verificación estándar se atasca.

---

## (d) El patrón DUAL en la práctica (Baileys hoy → Cloud API al validar)

**¿Alguien lo hace así? Sí.** Evolution API (9.028★, jul-2026) es exactamente eso a
escala: cada conexión es una "instancia" aislada que corre sobre **Baileys O sobre la
Cloud API oficial**, conmutables detrás de la misma API REST; el ecosistema brasileño la
usa como "PoC/arranque barato en Baileys → migrar a oficial al validar" manteniendo la
capa de abstracción (docs Evolution + guías de arquitectura 2026). Valida el diseño E4
de dixdybot (adaptador por canal); DIXDY no necesita adoptar Evolution, solo copiar el
patrón.

**Qué pasa con el número al migrar (dos rutas):**

1. **Ruta Coexistence (la buena para nosotros):** el número de un bot Baileys vive en la
   app WhatsApp Business del teléfono (Baileys es solo un "dispositivo vinculado"). Ese
   número casi siempre ya cumple los 7+ días de uso → Coexistence directo: se conserva la
   app en el teléfono, se sincronizan hasta 6 meses de chats 1:1 a la API, y el corte es
   de minutos. **Lo que se pierde:** la sesión Baileys (los dispositivos acompañantes se
   desvinculan en el onboarding), la posibilidad de OBA/verificación estándar, grupos por
   API, y aparece la obligación de abrir la app cada 13–14 días. **Lo que se gana:** cero
   riesgo de ban por ToS, webhooks confiables, adiós Bad MAC/440/QR.
   *Correr Baileys + Cloud API a la vez en el mismo número tras Coexistence es terreno
   pantanoso:* en teoría WhatsApp Web es "re-vinculable" y Baileys se hace pasar por Web;
   hay gente intentándolo (issue whatsmeow #916, 2025–2026) — **no diseñar nada que
   dependa de eso**.
2. **Ruta clásica (número dedicado a la API):** exige **borrar la cuenta de la app** en
   el teléfono; el historial en la app se pierde (respaldar antes), el número queda
   inutilizable en la app, hay hasta ~3 min para que el número se libere y Meta puede
   retener mensajes entrantes durante la transición (fuentes citan hasta 1 mes de "hold"
   en casos malos; BotSailor/Meta docs, consultadas jul-2026). Solo tiene sentido para
   números nuevos que nacen 100% API.

**El patrón operativo recomendado para DIXDY (cliente nuevo):** día 1 = chip nuevo + app
WhatsApp Business + Baileys (cero papeleo, bot vivo en horas) **y esa misma semana** la IA
deja el expediente Meta precargado (paso a paso de (a)). El requisito de 7 días de uso de
la app corre solo. Cuando el cliente valida (paga, hay volumen), Coexistence en una
tarde. Si el número Baileys muere antes (ban), el expediente precargado convierte la
emergencia en horas, no semanas.

---

## (e) Instagram DM para una cuenta que DIXDY administra

Base verificada el 23-jul-2026 contra docs de Meta (informe
`multicanal-instagram-plataformas.md`); tiempos estimados del flujo (sin fuente de
"minutos exactos", pero ningún paso tiene revisión de Meta en este escenario):

1. **Cuenta profesional** de Instagram (Business/Creator): toggle en la app, minutos. 🧑
2. En la **misma app de Meta** del cliente, agregar el producto Instagram ("Instagram API
   with Instagram Login", vía vigente desde jul-2024; ya NO exige página de Facebook).
   10–15 min. 🧑 clicks / 🤖 IA guía.
3. **Login de Instagram** del dueño de la cuenta → token con
   `instagram_business_basic` + `instagram_business_manage_messages` (scopes vigentes
   desde ene-2025). Minutos. 🧑 (credenciales).
4. En la app de Instagram: permitir acceso a mensajes para herramientas conectadas
   (ajuste de mensajería). Minutos. 🧑
5. **Webhook** a `messages` (+ postbacks, reactions, seen…): mismo Worker de Cloudflare,
   otro endpoint. 🤖 IA al 100%.
6. **Sin App Review**: con **Standard Access** alcanza mientras la app atienda cuentas
   propias o que DIXDY administra (verificado jul-2026 en docs de Meta). Advanced Access
   (review de 5–10 días hábiles + verificación) recién si dixdybot se vende como SaaS
   donde terceros conectan sus cuentas — misma frontera que en WhatsApp.

**Total: una tarde**, sin esperas de Meta. Reglas de operación: solo responder, ventana
de 24 h, divulgar que es un bot; `HUMAN_AGENT` (7 días) prohibido para el bot. Y para
IG jamás vía no oficial: la cuenta del cliente es irremplazable (suspensiones 15–30%/año
en herramientas no oficiales vs <0,5% oficial; datos 2025–2026 del informe previo).

---

## Síntesis para la decisión del dueño

| | Baileys (hoy) | Cloud API directo | Coexistence |
|---|---|---|---|
| Alta | Horas, cero papeleo | 1–3 días (45 min humanos) | Minutos (si el número ya tiene 7+ días de app) |
| Costo | $0 | ~$0 respondiendo; plantillas CLP ~$11–69 | Igual que Cloud API |
| Riesgo | Ban posible, sesión frágil | Cero ban ToS | Cero ban ToS; app cada 13–14 días |
| Escalar marketing | No aplica | Sí (con verificación) | **No** (sin verificación estándar/OBA) |

La jugada: mantener Baileys como rampa de entrada (velocidad), precargar el expediente
Meta de cada cliente apenas parte (la IA hace el ~70%), migrar por Coexistence al
validar, e Instagram entra por la misma app en una tarde. Tech Provider: solo al llegar
a E6, empezando por la verificación del negocio DIXDY porque es el paso lento.

## Fuentes

- https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started (pasos oficiales, system user/token permanente; consultado jul-2026)
- https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-tech-providers (requisitos Tech Provider; consultado jul-2026)
- https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates (revisión de plantillas hasta 24 h; consultado jul-2026)
- https://developers.facebook.com/docs/whatsapp/messaging-limits/ (límites de mensajería; consultado jul-2026)
- https://developers.facebook.com/docs/whatsapp/cloud-api/get-started/migrate-existing-whatsapp-number-to-a-business-account/ (migración clásica; consultado jul-2026)
- https://docs.360dialog.com/partner/onboarding/whatsapp-coexistence y https://docs.360dialog.com/partner/onboarding/whatsapp-coexistence/coexistence-onboarding (flujo QR, límites, 13 días; consultado jul-2026)
- https://docs.360dialog.com/docs/resources/phone-numbers/coexistence (limitaciones COEX; consultado jul-2026)
- https://docs.360dialog.com/docs/resources/meta-business-verification (documentos, Partner-led verification; consultado jul-2026)
- https://timelines.ai/whatsapp-coexistence-account-setup-guide (elegibilidad 7 días, 6 meses de historial, 20 msg/s; actualizado mar-2026)
- https://chakrahq.com/article/whatsapp-coexistence-live-eu-uk-europe-whatsapp-business-for-api-live/ (disponibilidad global may-2026, exclusiones Nigeria/Sudáfrica)
- https://whautomate.com/whatsapp-embedded-signup (Embedded Signup 5–15 min, mandato abr-2026)
- https://www.infobip.com/docs/whatsapp/tech-provider-program (deadline ISV→Tech Provider 31-dic-2025; consultado jul-2026)
- https://www.twilio.com/docs/whatsapp/isv/tech-provider-program/integration-guide (programa Tech Provider en BSPs; consultado jul-2026)
- https://cognitiva.la/verificacion-cuenta-meta-business-suite/ y https://www.asistchat.com/blog/como-verificar-negocio-meta-business-paso-a-paso (Chile: 12–72 h hábiles, RUT + constitución en un PDF; 2026)
- https://help.activecampaign.com/hc/en-us/articles/21826249568540 y https://chatarmin.com/en/blog/whats-app-messaging-limits (250/24 h sin verificar, escalado 1k→ilimitado; 2026)
- https://360dialog.com/pricing (€49/mes; consultado jul-2026) · https://ezcontact.ai/en/blog/whatsapp-api-pricing-comparison-meta-twilio-360dialog-ezcontact/ y https://setsmart.io/blog/whatsapp-business-api-pricing (markups BSP 2026)
- https://github.com/evolution-foundation/evolution-api y https://deepwiki.com/EvolutionAPI/evolution-api (instancias duales Baileys/Cloud API; jul-2026)
- https://botsailor.com/blog/how-to-migrate-your-existing-whatsapp-account-to-whatsapp-cloud-api (borrar cuenta, historial, hold de mensajes; consultado jul-2026)
- https://github.com/tulir/whatsmeow/issues/916 (intentos de cliente Web no oficial sobre cuenta Coexistence; 2025–2026)
- https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api/ y https://developers.facebook.com/docs/instagram-platform/overview/ (IG: scopes, Standard vs Advanced Access; verificado 23-jul-2026)
