/**
 * conversion.js
 * Pre-llena dinámicamente los links wa.me/56997946463 sin ?text= con un
 * mensaje contextual a la página actual. Mejora UX y la calidad del lead.
 *
 * Cargar con: <script src="/js/conversion.js" defer></script>
 */
(function () {
  "use strict";
  if (window.__conversionLoaded) return;
  window.__conversionLoaded = true;

  function capitalize(s) {
    return s ? s.charAt(0).toUpperCase() + s.slice(1) : "";
  }

  function buildWhatsappText() {
    var path = (location.pathname || "").toLowerCase();
    var seg = path.replace(/\/+$/, "").split("/").filter(Boolean);
    var last = seg[seg.length - 1] || "";
    var pretty = last.replace(/[-_]/g, " ").trim();

    if (path === "/" || path === "" || path === "/index.html") {
      return "Hola, necesito información sobre destape o limpieza de fosa.";
    }
    if (path.indexOf("/zonas/rural/") === 0) {
      return "Hola, necesito limpieza de fosa séptica en " + capitalize(pretty) + ".";
    }
    if (path.indexOf("/zonas/urbano/") === 0) {
      return "Hola, necesito un destape urgente en " + capitalize(pretty) + ".";
    }
    if (path.indexOf("/servicios/limpieza-fosas") === 0) return "Hola, necesito cotizar limpieza de fosa séptica.";
    if (path.indexOf("/servicios/destape-wc") === 0) return "Hola, necesito destape de WC / baño.";
    if (path.indexOf("/servicios/destape-desagues") === 0) return "Hola, necesito destape de cañería de cocina o trampa de grasa.";
    if (path.indexOf("/servicios/destape-alcantarillado") === 0) return "Hola, necesito destape de alcantarillado.";
    if (path.indexOf("/servicios/destape-edificios") === 0 || path.indexOf("/landing/destape-edificios") === 0) {
      return "Hola, soy administrador y necesito cotizar destape para edificio/condominio.";
    }
    if (path.indexOf("/servicios/inspeccion-camara") === 0) return "Hola, necesito inspección con cámara CCTV de alcantarillado.";
    if (path.indexOf("/servicios/camion-alta-presion") === 0 || path.indexOf("/servicios/hidrojet") !== -1) {
      return "Hola, necesito servicio de camión hidrojet alta presión.";
    }
    if (path.indexOf("/servicios/banos-quimicos") === 0) return "Hola, necesito cotizar arriendo de baños químicos.";
    if (path.indexOf("/servicios/mantencion") === 0 || path.indexOf("/landing/mantencion") === 0) {
      return "Hola, quiero información sobre planes de mantención preventiva.";
    }
    if (path.indexOf("/servicios/contratos") === 0) return "Hola, necesito cotizar contrato de servicios para empresa/condominio.";
    if (path.indexOf("/landing/destape-urgente") === 0 || path.indexOf("/urgencias") === 0) {
      return "Hola, tengo una urgencia y necesito atención ahora.";
    }
    if (path.indexOf("/landing/limpieza-fosas-parcelas") === 0) return "Hola, necesito limpieza de fosa para mi parcela.";
    if (path.indexOf("/blog/") === 0) return "Hola, vengo del blog y necesito ayuda con un destape o fosa.";
    if (path.indexOf("/precios") === 0) return "Hola, quiero confirmar precio para mi caso.";
    if (pretty) return "Hola, necesito información sobre " + capitalize(pretty) + ".";
    return "Hola, necesito ayuda con un destape o fosa séptica.";
  }

  function ensureText(href) {
    if (!href) return href;
    if (href.indexOf("wa.me/") === -1) return href;
    if (href.indexOf("text=") !== -1) return href;
    var sep = href.indexOf("?") === -1 ? "?" : "&";
    return href + sep + "text=" + encodeURIComponent(buildWhatsappText());
  }

  // Listener delegado: cualquier click en un link wa.me sin ?text= se enriquece
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest && e.target.closest('a[href*="wa.me/"]');
    if (!a) return;
    var href = a.getAttribute("href") || "";
    var enriched = ensureText(href);
    if (enriched !== href) a.setAttribute("href", enriched);
  }, true);
})();
