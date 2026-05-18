/**
 * Registra el service worker después del load para no competir con el LCP.
 * Si el navegador no soporta SW (Safari iOS antiguos), simplemente no hace nada.
 */
(function () {
  if (!("serviceWorker" in navigator)) return;
  if (location.hostname === "localhost" && location.search.includes("nosw")) return;

  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("/sw.js", { scope: "/" })
      .catch(function () {
        // silencioso — no es crítico
      });
  });
})();
