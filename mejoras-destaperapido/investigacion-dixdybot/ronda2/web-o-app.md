# ¿Web o aplicación? — Informe para dixdybot (destaperapido)

**Fecha:** 23 de julio de 2026
**Pregunta del dueño:** "¿Afectaría si lo hacemos web o creamos una aplicación? ¿Podríamos sacarle más provecho?"
**Respuesta corta:** No conviene hacer una app nativa hoy. La web instalable (PWA) en iOS 2026 ya da el 95% de la experiencia "de app" que este negocio necesita, con costo ~cero y sin frenar la velocidad de iteración con IA. La app nativa se reconsidera solo si dixdybot escala a muchos clientes que pidan app de marca o si se necesita algo que la web no puede dar (widgets, tracking en segundo plano).

---

## 0. Punto de partida: lo que YA existe en la casa

- **Panel del dueño:** web local en el Mac (`:8789`), accesible desde el iPhone vía Tailscale (`http://100.72.55.61:8789`), ya responsive.
- **Panel del repartidor:** web simple de solo lectura sobre Supabase.
- **Push al bolsillo:** `avisos-worker` (Cloudflare, gratis) **ya es una PWA con web push funcionando en el iPhone de Alejandro** — aes128gcm + VAPID ES256, con poda automática de suscripciones muertas (404/410). O sea: el patrón "notificación push sin App Store" ya está probado en producción en este mismo sistema.

Esto importa porque la doctrina DIXDY manda no reinventar: cualquier mejora "de app" debe sumarse a estas piezas, no construirse al lado.

---

## (a) PWA instalable en iOS hoy (2025-2026): ¿experiencia "de app" sin App Store?

**Sí, para este caso de uso.** Estado real, con fechas:

| Capacidad | Estado en iOS | Desde cuándo |
|---|---|---|
| Ícono en pantalla de inicio, pantalla completa (sin barra de Safari) | ✅ | Siempre; **iOS 26 (sept 2025)** además abre por defecto como web app TODO sitio añadido a inicio |
| Notificaciones push (Web Push) | ✅ solo si la web está instalada en pantalla de inicio | iOS 16.4 (marzo 2023) |
| Push "declarativo" (más confiable, sin service worker; el sistema muestra la notificación aunque el JS falle) | ✅ | Safari/iOS 18.4 (marzo-abril 2025); reforzado en WWDC 2025 |
| Badge (numerito rojo en el ícono) | ✅ con permiso de notificaciones | iOS 16.4 |
| Offline (cache + service worker) | ✅ con matices | — |
| Datos persistentes | ✅ las web apps **instaladas** están exentas del borrado a los 7 días de ITP (WebKit lo documenta oficialmente, política 2023); el límite de 7 días aplica a Safari normal | 2023 |
| Background Sync / trabajo en segundo plano | ❌ no existe en iOS | — |
| Widgets, Live Activities, Siri, NFC, Bluetooth | ❌ solo nativa | — |

**Los "peros" honestos (información de 2025-2026):**

1. **Instalar tiene fricción:** iOS no muestra prompt de instalación; hay que enseñar el gesto Compartir → "Añadir a pantalla de inicio". Para 2 usuarios internos (dueño + repartidor) esto es un tutorial de 1 minuto, irrelevante. Para clientes futuros, es una página de onboarding con capturas. iOS 26 lo suavizó: ahora todo lo añadido a inicio abre como app por defecto (MacRumors/iDownloadBlog, junio-sept 2025).
2. **Suscripciones push que se pierden:** hay reportes reales (foros XenForo, Apple Developer, 2023-2026) de suscripciones revocadas en iOS. La causa dominante está documentada por Progressier: si el service worker no muestra una notificación por cada push (falta `event.waitUntil`), Safari revoca la suscripción. El **Declarative Web Push de iOS 18.4 elimina esta clase de fallo de raíz** (el sistema muestra la notificación él mismo). Además `avisos-worker` ya poda y re-suscribir es apretar un botón. Con 2 usuarios internos, riesgo manejable; con cientos de usuarios finales sería un dolor — pero ese no es el caso.
3. **UE, no Chile:** en 2024 Apple amenazó con matar las web apps en la UE por la DMA (iOS 17.4) y se retractó en marzo 2024; algunos artículos aún arrastran confusión. **Chile no está afectado en ningún escenario.**
4. Ojo técnico local: para que el push llegue, el panel debe servirse por **HTTPS** — el `:8789` por Tailscale es HTTP. Solución sin construir nada: el push del panel del dueño sigue saliendo por `avisos-worker` (ya HTTPS, ya funciona), y el panel solo necesita manifest + ícono para instalarse. Tailscale ofrece `tailscale serve` con HTTPS si algún día se quiere push directo del panel.

**Veredicto (a):** una PWA le da al dueño y al repartidor ícono, pantalla completa, push y badge — la experiencia que la gente llama "app" — sin Apple, sin costo y sin esperar revisiones.

---

## (b) App nativa (Swift / React Native / Expo): ¿qué ganaría DE VERDAD?

Lo único que una nativa da y la PWA no (estado 2026):

- Widgets en pantalla de inicio y **Live Activities** (ej.: "entrega en camino" fijada en la pantalla bloqueada).
- Trabajo en segundo plano real: **tracking GPS continuo del repartidor en ruta**, sincronización con la app cerrada.
- Siri/Shortcuts profundos, NFC, Bluetooth, Face ID nativo.
- Presencia en App Store (marketing/confianza para un producto B2C masivo — no es el caso de un panel interno).

Lo que costaría (datos 2025-2026):

- **US$99/año** Apple Developer Program (obligatorio incluso para distribuir por TestFlight).
- **Revisión de Apple:** 90-94% en <24h, promedio 24-72h, pero con casos de 7-10 días — cada actualización pasa por ahí. Esto **mata el loop de iteración con IA**: hoy un cambio del panel es editar un archivo y recargar; con app nativa es build (EAS: gratis solo 15 builds iOS/mes, luego US$19+/mes) + firma + TestFlight/revisión.
- **Riesgo Guideline 4.2 ("minimum functionality"):** Apple rechaza activamente en 2025 las apps que son "una web envuelta" — que es exactamente lo que sería empaquetar estos paneles. Habría que añadir features nativas solo para justificar la app.
- **TestFlight caduca a los 90 días** por build → una "app interna" por TestFlight obliga a re-publicar cada 3 meses aunque no cambie nada. La distribución interna sin App Store (Apple Business/Enterprise) exige ser empresa de 100+ empleados.
- Mantenimiento típico de nativa: 15-25% del costo de desarrollo al año; una PWA cuesta 40-60% menos de entrada y ~la mitad de mantención (comparativas 2025-2026).

**Veredicto (b):** para un panel de dueño + un panel de repartidor + paneles de clientes futuros, la nativa no aporta nada que se use hoy y cobra caro en plata, fricción y velocidad. El único gatillo futuro real es **Live Activities / GPS en segundo plano del repartidor** — si algún día eso se vuelve prioridad, el camino es Expo/React Native (es lo que usa Chatwoot para su app), no Swift puro.

---

## (c) ¿App de escritorio / menubar en el Mac (Electron / Tauri)?

**No aporta aquí.** El Mac mini es el **servidor** del sistema, no un puesto de trabajo: el dueño opera desde el iPhone y el dashboard local ya es web en localhost. Una app de menubar (Tauri sería la opción liviana: ~12 MB vs ~180 MB de Electron, datos 2025-2026) solo duplicaría lo que ya muestran el Kanban y los avisos push, y agregaría una pieza más que mantener — justo lo que la doctrina DIXDY prohíbe. Si algún día se quiere "semáforo de salud del bot" en la barra del Mac, existen atajos nativos (SwiftBar/xbar leyendo un JSON local) que no requieren construir una app. **Descartado.**

---

## (d) Multi-cliente: ¿qué hace la competencia si dixdybot se vende?

Revisado el mercado de plataformas de conversación/WhatsApp (respond.io, Wati, SleekFlow, Trengo, Zoko, ManyChat, Chatwoot — fuentes 2025-2026):

- **El estándar universal es panel web con login.** Nadie obliga a instalar una app: la app móvil es un **complemento** del inbox (respond.io la vende como "también tenemos app"), nunca la puerta principal.
- **Chatwoot** (el open source de referencia) tiene su app móvil en React Native + Expo, con iOS distribuido por TestFlight — y aun así su producto ES el dashboard web. Confirma que web-first es la arquitectura, y la app llega tarde y como extra.
- Para dixdybot multi-cliente: **panel web con login + instalable como PWA** es exactamente lo que el mercado espera. Opciones de login en el stack que DIXDY ya usa:
  - **Cloudflare Access (Zero Trust): gratis hasta 50 usuarios** (plan permanente, verificado 2025-2026; US$7/usuario/mes después). Perfecto para los primeros clientes: cero código de auth, login con Google/email por cliente delante del worker.
  - **Workers + D1 con sesión propia** (API key/magic link por cliente) cuando se quiera marca blanca total — el `panel-cliente/` del maestro ya apunta en esa dirección (E6 de la investigación previa contempla API key por cliente).

**Veredicto (d):** vender dixdybot NO requiere app. Requiere un buen panel web con login — que además es lo único compatible con iterar rápido con IA para muchos clientes a la vez (un deploy actualiza a todos; una app serían binarios + revisión de Apple por cada mejora).

---

## (e) RECOMENDACIÓN — costo/beneficio

**Hacer (barato, reutiliza lo que existe):**

1. **Dueño:** convertir el panel `:8789` en instalable (manifest + íconos + service worker mínimo) para que viva como ícono a pantalla completa en su iPhone. Push sigue llegando por `avisos-worker` (ya probado). Costo: horas de trabajo, $0.
2. **Repartidor:** mismo tratamiento al panel Supabase + push "nueva entrega / actualización" reutilizando el `webpush.js` que ya existe (correo-worker/avisos-worker). Usar **Declarative Web Push** (iOS 18.4+) como formato preferido por su confiabilidad. Costo: horas, $0. (El aviso por WhatsApp que hoy recibe se mantiene como respaldo.)
3. **Badge + offline básico** en ambos: numerito de pendientes en el ícono y cache de la última vista para túneles/mala señal. Todo es API web soportada en iOS 16.4+.
4. **Clientes futuros (dixdybot E6):** panel web con login — Cloudflare Access gratis (≤50 usuarios) al principio, sesiones propias en Workers+D1 al crecer — e instalable como PWA con la marca del cliente. Es el estándar de todos los competidores.

**NO construir:**

- ❌ App nativa iOS hoy (US$99/año + revisión 24-72h por cada cambio + riesgo de rechazo 4.2 por "web envuelta" + TestFlight caduca a 90 días + rompe la velocidad de iteración con IA).
- ❌ App de escritorio/menubar Electron o Tauri (el Mac es servidor; duplicaría los avisos).
- ❌ Adoptar una plataforma con app propia (Chatwoot etc.) solo por su app — ya se decidió gateway propio y la evidencia confirma que la app no es lo que vende.

**Cuándo reabrir la puerta a la nativa (gatillos concretos):** (1) clientes de dixdybot pagando que exijan app de marca en App Store; (2) necesidad real de Live Activities o GPS del repartidor en segundo plano; (3) decenas de repartidores/usuarios donde la pérdida ocasional de suscripciones push se vuelva costosa. En ese momento: **Expo/React Native** (una base para iOS+Android, camino Chatwoot), nunca Swift puro para un equipo de una persona + IA.

**Respuesta a "¿le sacaríamos más provecho con una app?":** No — hoy le sacan más provecho a la web instalable, porque cada mejora llega al teléfono al instante sin pasar por Apple, y las dos únicas cosas que una app regalaría de verdad (widgets/tracking en segundo plano) no están en el plan E0-E6. La plata y las horas rinden más en el bot mismo (E1-E3) que en empaquetar paneles.

---

## Fuentes (consultadas 23-jul-2026)

- WebKit (Apple) — Meet Declarative Web Push (mar 2025): https://webkit.org/blog/16535/meet-declarative-web-push/
- WebKit — Features in Safari 18.4 (mar 2025): https://webkit.org/blog/16574/webkit-features-in-safari-18-4/
- WebKit — Updates to Storage Policy (exención de web apps instaladas, 2023): https://webkit.org/blog/14403/updates-to-storage-policy/
- Apple WWDC25 — Learn more about Declarative Web Push (jun 2025): https://developer.apple.com/videos/play/wwdc2025/235/
- MagicBell — PWA iOS Limitations and Safari Support (2026): https://www.magicbell.com/blog/pwa-ios-limitations-safari-support-complete-guide
- MobiLoud — Do PWAs Work on iOS? (2026): https://www.mobiloud.com/blog/progressive-web-apps-ios
- iDownloadBlog — iOS 26: Safari abre como web app todo lo añadido a inicio (jun 2025): https://www.idownloadblog.com/2025/06/17/apple-ios-26-safari-web-apps-home-screen-bookmarks/
- MacRumors — iOS 26: Add Web App to Home Screen (2025): https://www.macrumors.com/how-to/save-safari-bookmark-web-app-iphone-home-screen/
- Progressier — Fix iOS push subscriptions terminated (causa raíz de suscripciones perdidas): https://dev.to/progressier/how-to-fix-ios-push-subscriptions-being-terminated-after-3-notifications-39a7
- XenForo community — "Lost" push subscriptions for iOS PWA (reportes reales): https://xenforo.com/community/threads/lost-push-subscriptions-for-ios-pwa.215833/
- Aimtell — State of Declarative Web Push (2026): https://aimtell.com/blog/state-of-declarative-web-push-2026
- Foresight Mobile — iOS Distribution Guide: TestFlight, App Store & Enterprise (2026): https://foresightmobile.com/blog/ios-app-distribution-guide-2026
- Apple — TestFlight (builds válidos 90 días): https://developer.apple.com/testflight/
- MobiLoud — App Store Review Guidelines: Webview/Wrapper (guideline 4.2, 2025): https://www.mobiloud.com/blog/app-store-review-guidelines-webview-wrapper
- Metacto — The True Cost of Expo App Development / EAS pricing (2026): https://www.metacto.com/blogs/the-true-cost-of-expo-app-development-a-comprehensive-guide
- respond.io — Best conversation platforms WITH a mobile app (la app como complemento, 2025-2026): https://respond.io/blog/best-customer-conversation-management-platforms-with-a-mobile-app
- GitHub — Chatwoot mobile app (React Native + Expo, iOS por TestFlight): https://github.com/chatwoot/chatwoot-mobile-app
- Cloudflare — Zero Trust / Access (gratis ≤50 usuarios): https://www.cloudflare.com/sase/products/access/ y https://costbench.com/software/business-vpn/cloudflare-zero-trust/free-plan/
- Tech-Insider — Tauri vs Electron (2026): https://tech-insider.org/tauri-vs-electron-2026/
- Instinctools — PWA vs Native App: Pros and Cons (2026): https://www.instinctools.com/blog/pwa-vs-native-app/
