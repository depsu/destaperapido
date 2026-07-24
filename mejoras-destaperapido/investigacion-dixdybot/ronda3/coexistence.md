# Arbitraje: Coexistence (WhatsApp Business App + Cloud API) — ¿ruta por defecto o trampa?

Fecha de verificación: 2026-07-23. Todas las fuentes consultadas hoy vía fetch directo.
Nota metodológica: el buscador de la sesión estaba agotado; se trabajó con fetch directo a
URLs primarias + DuckDuckGo HTML como índice. Ninguna afirmación descansa en una sola página
salvo donde se indica explícitamente.

## (a) Lo que documenta META (fuente primaria)

Doc principal: "Onboard WhatsApp Business app users" —
https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users/
(consultada 2026-07-23; también accesible por la ruta vieja /docs/whatsapp/embedded-signup/custom-flows/onboarding-business-app-users):

- **Throughput fijo 20 mps**: "business phone numbers that are in use with both the WhatsApp
  Business app and Cloud API have a fixed throughput of 20 mps".
- **Cloud API normal: 80 mps por defecto, hasta 1.000 por upgrade automático** — doc de
  Throughput (developers.facebook.com/documentation/business-messaging/whatsapp/throughput/,
  2026-07-23): "up to 80 messages per second (mps) by default, and up to 1,000 mps by
  automatic upgrade".
- **Features que se apagan en la app** (chats 1:1): mensajes temporales (disappearing),
  view once, ubicación en vivo, listas de difusión ("Existing Broadcast lists will become
  read-only"). **OJO: "Message Edit/Revoke is now supported"** — editar/eliminar mensajes YA
  se soporta según la doc vigente de Meta.
- **Historial**: sincroniza hasta **180 días** hacia atrás; el partner tiene **24 horas** para
  completar la sincronización o hay que des-onboardear; la sincronización de historial y
  contactos es **una sola vez** ("You can only perform this step once").
- **Actividad del teléfono**: desconexión por "PRIMARY_INACTIVITY (primary device inactive
  for approximately 14 days)" y "COMPANION_INACTIVITY (~30 days)". De ahí la regla práctica
  "abrir la app cada 14 días".
- **Requisitos**: app Business ≥ 2.24.17, ser Solution Partner o **Tech Provider**, Embedded
  Signup con session logging, webhook que digiera `history`, `smb_app_state_sync`,
  `smb_message_echoes`. No se puede usar el Deregister API estando en coexistence.
- **Países**: anuncio oficial (developers.facebook.com/blog/post/2025/03/19/introducing-api-
  solutions-for-whatsapp-business-users-launched/, 2025-03-19): rollout global **excluyendo**
  India, UK, EEA, Turquía, Japón, Nigeria, Australia, Filipinas, Corea del Sur, Sudáfrica y
  Rusia. **Chile SÍ está cubierto.**

## (b) Verificación de las fuentes de ChatGPT

- **Wati** — EXISTE: support.wati.io/en/articles/14818473 "Understanding WhatsApp Coexistence
  (CoEx) Limitations" (actualizado 2026-04-29). Documenta problemas reales de sync: "Existing
  chats not syncing immediately", "Chats syncing initially but not updating later", "Missing
  conversations due to sync issues". NO dice literalmente ">24h". Hallazgo extra (solo esta
  fuente): CoEx y la verificación pagada (Meta Verified) serían mutuamente excluyentes.
- **Seven** — EXISTE: help.seven.io/en/whatsapp/whatsapp-coexistence (sin fecha). Confirma
  20 MPS, "app must be opened at least once every 14 days", y lista features deshabilitadas
  incluyendo "Message editing" y "Message revoke" — **desactualizado frente a Meta**, que hoy
  dice que Edit/Revoke ya se soporta.
- **Spur** — EXISTE: help.spurnow.com/en/articles/15840061 "Coexistence? Should you go for
  it?" (actualizado ~jul 2026). Cita textual: "Simple answer: No. There are very few cases
  where you should be using Coexistence." Lista 16 contras (sin fuente de datos duros).
  **Matiz decisivo**: sus casos donde SÍ lo recomienda son "migrating gradually from the app
  to the API", "need occasional manual phone conversations", "very small teams" — es
  EXACTAMENTE el perfil de este cliente.
- **Manychat** — EXISTE: manychat.com/blog/whatsapp-coexistence-grow-and-keep-your-number/
  (marketing pro-coexistence, sin datos duros nuevos).
- **Primer mensaje de click-to-WhatsApp** — CONFIRMADO en dos vendors independientes (no en
  Meta): respond.io/help/whatsapp/whatsapp-coexistence ("the initial message may not be
  delivered through the webhook and will appear as unsupported") y
  engagelab.com/docs/whatsapp/quick-access/whatsapp-business-app-coexistence ("a brief
  message anomaly may occur"). Ambas consultadas 2026-07-23.

## (c) Los claims de Gemini

- **"40-50% de webhooks perdidos con tráfico alto"**: búsqueda con comillas y variantes →
  **cero resultados**. Ninguna doc de Meta, ningún vendor, ningún foro. Sin fuente primaria
  ni secundaria: tratarlo como **inventado** (no citable).
- **"Bucles de sincronización que duplican contactos"**: no existe ninguna fuente que
  describa eso en coexistence. Lo único que aparece son duplicados genéricos de contactos en
  WhatsApp (Reddit/StackExchange) sin relación con CoEx. **No verificable**; probablemente
  extrapolación sin base.

## (d) Las tres rutas para ESTE cliente (dueño atiende a diario desde la app)

1. **Coexistence**: es la ÚNICA ruta oficial que le conserva la app. El bot va por Cloud API
   y `smb_message_echoes` deja que el CRM vea lo que el dueño escribe desde la app (mejora el
   Kanban actual). Costos reales documentados: pierde listas de difusión / view-once /
   ubicación en vivo / mensajes temporales; 20 mps (irrelevante: el negocio mueve decenas de
   mensajes al día, no 20 por segundo); regla de 14 días (la cumple de sobra, usa la app a
   diario); sync imperfecto (Wati) y rareza del primer mensaje CTWA (afecta ads de Meta, no
   el flujo Google Ads → link de WhatsApp que usa hoy). Requiere onboardear vía un BSP/Tech
   Provider que soporte CoEx (respond.io, Wati, 360dialog…): implica costo mensual de BSP o
   hacerse Tech Provider.
2. **Migración completa a Cloud API**: Meta exige borrar la cuenta de la app — "To use an
   existing WhatsApp Business app phone number with Cloud API, you must either delete your
   account, or onboard... using a partner who supports business app number onboarding"
   (developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/
   migrate-existing-whatsapp-number-to-a-business-account/, 2026-07-23). El dueño quedaría
   SIN app: atendería solo por un inbox web (del BSP o extendiendo el panel propio). Para
   este dueño es la ruta disruptiva: le cambia el hábito diario por un beneficio (80 mps)
   que no necesita. **Esta es la trampa aquí, no coexistence.**
3. **Seguir en Baileys**: gratis y con el CRM actual funcionando, pero no-oficial: el propio
   repo (github.com/WhiskeySockets/Baileys, 2026-07-23) declara no-afiliación y que no avala
   usos contra los ToS de WhatsApp; el riesgo de baneo del número principal es real y sin
   recurso. Viable como statu quo SOLO con expediente de salida listo (ya existe:
   conversaciones.jsonl, envios.jsonl, tarifario en código).

## (e) Veredicto

**Coexistence es la ruta correcta para este cliente — no es trampa — pero como decisión con
piloto, no como salto ciego al 30-sep.** Los números catastróficos (40-50% webhooks,
bucles de duplicación) no tienen fuente; los costos reales documentados por Meta son menores
a esta escala. Salvaguardas obligatorias:

1. Tratar el 30-sep como **fecha de decisión con piloto**, no de corte: probar CoEx primero
   en un número secundario con el BSP elegido antes de tocar el principal.
2. **No depender del history sync** (es una sola vez y con ventana de 24h): el historial
   maestro ya vive en el CRM propio (conversaciones.jsonl). Hacer el onboarding en ventana
   de bajo tráfico.
3. Mantener **Baileys como fallback caliente** 30-60 días post-migración antes de apagarlo.
4. Disciplina anti-duplicados en el CRM (el contrato envios.jsonl ya existe): el API pasa a
   ser fuente de verdad de envíos del bot; la app, del dueño.
5. Verificar ANTES con el BSP: soporte real de CoEx en Chile, costo mensual, y el posible
   conflicto CoEx ↔ Meta Verified pagado (claim de Wati, una sola fuente — confirmar).
6. Confirmar que el dueño no usa listas de difusión / view-once / ubicación en vivo desde la
   app; si usa difusión, avisarle que quedan de solo lectura.
7. Si algún día corren ads click-to-WhatsApp de Meta, probar el primer mensaje (puede llegar
   como "unsupported" al webhook — respond.io/EngageLab).

## Fuentes (todas consultadas 2026-07-23)

- Meta, Onboard WhatsApp Business app users: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users/
- Meta, Throughput: https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput/
- Meta, blog anuncio CoEx (2025-03-19): https://developers.facebook.com/blog/post/2025/03/19/introducing-api-solutions-for-whatsapp-business-users-launched/
- Meta, migrar número existente: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/migrate-existing-whatsapp-number-to-a-business-account/
- Wati (2026-04-29): https://support.wati.io/en/articles/14818473-understanding-whatsapp-coexistence-coex-limitations
- Seven (s/f): https://help.seven.io/en/whatsapp/whatsapp-coexistence
- Spur (~jul 2026): https://help.spurnow.com/en/articles/15840061-coexistence-should-you-go-for-it
- Manychat: https://manychat.com/blog/whatsapp-coexistence-grow-and-keep-your-number/
- Respond.io: https://respond.io/help/whatsapp/whatsapp-coexistence
- EngageLab: https://www.engagelab.com/docs/whatsapp/quick-access/whatsapp-business-app-coexistence
- Baileys: https://github.com/WhiskeySockets/Baileys
