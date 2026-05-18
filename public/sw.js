/**
 * Service Worker — destaperapido.cl
 *
 * Estrategia:
 *  - Assets estáticos (CSS, JS, fonts, imágenes): cache-first con expiración.
 *  - HTML: network-first con fallback a caché (no servir contenido viejo si
 *    hay red). Permite navegación offline para páginas ya visitadas.
 *  - Solo cachea same-origin (GET).
 *
 * Versión: subir CACHE_VERSION para invalidar todo el caché tras un release.
 */
const CACHE_VERSION = "v2026-05-08-1";
const STATIC_CACHE = `static-${CACHE_VERSION}`;
const HTML_CACHE = `html-${CACHE_VERSION}`;

// Assets que precachear en install — los críticos del LCP móvil.
const PRECACHE = [
  "/output.css",
  "/fonts/fontawesome/all.min.css",
  "/fonts/webfonts/fa-solid-900.woff2",
  "/fonts/webfonts/fa-brands-400.woff2",
  "/logo-nav.webp",
  "/js/conversion.js",
  "/js/mobile-sticky-cta.js",
  "/js/availability-badge.js",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) =>
      cache.addAll(PRECACHE).catch(() => {
        // No bloquear el install si algún asset falla
      })
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k !== STATIC_CACHE && k !== HTML_CACHE)
          .map((k) => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

function isStaticAsset(url) {
  return /\.(css|js|woff2?|ttf|otf|eot|svg|png|jpe?g|webp|gif|ico)$/i.test(url.pathname);
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // HTML → network-first
  if (req.headers.get("accept")?.includes("text/html")) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(HTML_CACHE).then((c) => c.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then((cached) => cached || caches.match("/")))
    );
    return;
  }

  // Assets estáticos → cache-first
  if (isStaticAsset(url)) {
    event.respondWith(
      caches.match(req).then(
        (cached) =>
          cached ||
          fetch(req).then((res) => {
            if (res.ok) {
              const copy = res.clone();
              caches.open(STATIC_CACHE).then((c) => c.put(req, copy));
            }
            return res;
          })
      )
    );
    return;
  }
});
