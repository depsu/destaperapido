/**
 * conversion.js
 * Pre-llena dinámicamente los links wa.me con un mensaje contextual a la
 * página actual y agrega parámetros UTM para tracking. Mejora UX y la
 * calidad del lead.
 *
 * Cargar con: <script src="/js/conversion.js" defer></script>
 */
(function () {
  "use strict";
  if (window.__conversionLoaded) return;
  window.__conversionLoaded = true;

  // ---------- Helpers ----------
  function capitalize(s) {
    return s ? s.charAt(0).toUpperCase() + s.slice(1) : "";
  }

  function prettify(slug) {
    return (slug || "").replace(/[-_]/g, " ").trim();
  }

  // Detecta horario nocturno (22-06) o fin de semana — usado para reforzar
  // urgencia en mensajes y CTAs.
  function isAfterHours() {
    var d = new Date();
    var hour = d.getHours();
    var day = d.getDay(); // 0 dom, 6 sáb
    return hour >= 22 || hour < 7 || day === 0 || day === 6;
  }

  // ---------- Mensaje contextual ----------
  function buildWhatsappText() {
    var path = (location.pathname || "").toLowerCase();
    var seg = path.replace(/\/+$/, "").split("/").filter(Boolean);
    var last = seg[seg.length - 1] || "";
    if (last === "index.html") last = seg[seg.length - 2] || "";
    var pretty = prettify(last);
    var urgent = isAfterHours();
    var urgentTag = urgent ? "URGENTE — " : "";

    // Home
    if (path === "/" || path === "" || path === "/index.html") {
      return urgentTag + "Hola, necesito información sobre destape o limpieza de fosa.";
    }

    // Zonas
    if (path.indexOf("/zonas/rural/") === 0) {
      return urgentTag + "Hola, necesito limpieza de fosa séptica en " + capitalize(pretty) + ".";
    }
    if (path.indexOf("/zonas/urbano/") === 0) {
      return urgentTag + "Hola, necesito un destape en " + capitalize(pretty) + ".";
    }
    if (path.indexOf("/zonas/parcelas") !== -1) {
      return urgentTag + "Hola, necesito servicio en mi parcela / condominio cerrado.";
    }

    // Servicios
    if (path.indexOf("/servicios/limpieza-fosas") === 0) return "Hola, necesito cotizar limpieza de fosa séptica.";
    if (path.indexOf("/servicios/destape-wc") === 0) return urgentTag + "Hola, necesito destape de WC / baño.";
    if (path.indexOf("/servicios/destape-desagues") === 0) return "Hola, necesito destape de cañería de cocina o trampa de grasa.";
    if (path.indexOf("/servicios/destape-alcantarillado") === 0) return urgentTag + "Hola, necesito destape de alcantarillado.";
    if (path.indexOf("/servicios/destape-edificios") === 0 || path.indexOf("/landing/destape-edificios") === 0) {
      return "Hola, soy administrador y necesito cotizar destape para edificio/condominio.";
    }
    if (path.indexOf("/servicios/inspeccion-camara") === 0) return "Hola, necesito inspección con cámara CCTV de alcantarillado.";
    if (path.indexOf("/servicios/camion-alta-presion") === 0 || path.indexOf("/hidrojet") !== -1) {
      return "Hola, necesito servicio de camión hidrojet alta presión.";
    }
    if (path.indexOf("/servicios/banos-quimicos") === 0) return "Hola, necesito cotizar arriendo de baños químicos.";
    if (path.indexOf("/servicios/mantencion") === 0 || path.indexOf("/landing/mantencion") === 0) {
      return "Hola, quiero información sobre planes de mantención preventiva.";
    }
    if (path.indexOf("/servicios/contratos") === 0) return "Hola, necesito cotizar contrato de servicios para empresa/condominio.";

    // Urgencias / landings
    if (path.indexOf("/landing/destape-urgente") === 0 || path.indexOf("/urgencias") === 0) {
      return "EMERGENCIA — necesito atención inmediata, por favor.";
    }
    if (path.indexOf("/landing/limpieza-fosas-parcelas") === 0) return "Hola, necesito limpieza de fosa para mi parcela.";

    // Cobertura / contacto / FAQ
    if (path.indexOf("/cobertura") === 0) return "Hola, ¿tienen cobertura en mi sector? Necesito un servicio.";
    if (path.indexOf("/contacto") === 0) return "Hola, necesito ayuda con un destape o fosa.";
    if (path.indexOf("/faq") === 0) return "Hola, tengo una duda y necesito orientación.";
    if (path.indexOf("/casos-reales") === 0) return "Hola, vi sus casos y necesito cotizar un servicio.";
    if (path.indexOf("/precios") === 0) return "Hola, quiero confirmar precio para mi caso.";

    // Blog — mensaje según slug del artículo
    if (path.indexOf("/blog/") === 0) {
      if (last.indexOf("fosa") !== -1 || last.indexOf("biodigestor") !== -1 || last.indexOf("pozo") !== -1) {
        return "Hola, vengo del blog. Tengo dudas con mi fosa séptica / pozo.";
      }
      if (last.indexOf("wc") !== -1 || last.indexOf("inundacion") !== -1 || last.indexOf("bano") !== -1) {
        return urgentTag + "Hola, vengo del blog. Tengo problema con WC / baño.";
      }
      if (last.indexOf("cocina") !== -1 || last.indexOf("lavaplato") !== -1 || last.indexOf("grasa") !== -1) {
        return "Hola, vengo del blog. Necesito destape de cocina / cañería de grasa.";
      }
      if (last.indexOf("edificio") !== -1 || last.indexOf("condominio") !== -1) {
        return "Hola, vengo del blog. Soy administrador y necesito cotizar.";
      }
      if (last.indexOf("hidrojet") !== -1 || last.indexOf("camara") !== -1 || last.indexOf("cctv") !== -1) {
        return "Hola, vengo del blog. Necesito hidrojet o inspección con cámara.";
      }
      if (last.indexOf("urgenc") !== -1 || last.indexOf("rebalse") !== -1 || last.indexOf("inundacion") !== -1) {
        return urgentTag + "Hola, vengo del blog. Tengo una urgencia ahora.";
      }
      return "Hola, vengo del blog y necesito ayuda con un destape o fosa.";
    }

    if (pretty) return "Hola, necesito información sobre " + capitalize(pretty) + ".";
    return "Hola, necesito ayuda con un destape o fosa séptica.";
  }

  // ---------- Enriquecer href ----------
  function buildUtm(href) {
    var path = (location.pathname || "").toLowerCase().replace(/\/+$/, "");
    var source = "web";
    var medium = "whatsapp";
    var campaign = path.split("/").filter(Boolean).join("_") || "home";
    var url = href + (href.indexOf("?") === -1 ? "?" : "&") +
      "utm_source=" + encodeURIComponent(source) +
      "&utm_medium=" + encodeURIComponent(medium) +
      "&utm_campaign=" + encodeURIComponent(campaign);
    return url;
  }

  function ensureText(href) {
    if (!href) return href;
    if (href.indexOf("wa.me/") === -1) return href;
    var out = href;
    if (out.indexOf("text=") === -1) {
      var sep = out.indexOf("?") === -1 ? "?" : "&";
      out = out + sep + "text=" + encodeURIComponent(buildWhatsappText());
    }
    if (out.indexOf("utm_source=") === -1) {
      out = buildUtm(out);
    }
    return out;
  }

  // Si estamos en una página de zona, propagamos la comuna a los enlaces
  // hacia /calculadora-cotizacion como ?comuna=<slug>.
  function currentZoneSlug() {
    var path = (location.pathname || "").toLowerCase();
    var m = path.match(/\/zonas\/(?:rural|urbano)\/([^\/]+?)(?:\.html)?\/?$/);
    if (!m) return null;
    if (m[1] === "index") return null;
    return m[1];
  }

  function enrichCalcLinks() {
    var slug = currentZoneSlug();
    if (!slug) return;
    var links = document.querySelectorAll('a[href^="/calculadora"], a[href*="/calculadora-cotizacion"]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = a.getAttribute("href") || "";
      if (href.indexOf("comuna=") !== -1) continue;
      var sep = href.indexOf("?") === -1 ? "?" : "&";
      a.setAttribute("href", href + sep + "comuna=" + encodeURIComponent(slug));
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enrichCalcLinks);
  } else {
    enrichCalcLinks();
  }

  // Listener delegado: cualquier click en un link wa.me se enriquece
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest && e.target.closest('a[href*="wa.me/"]');
    if (!a) return;
    var href = a.getAttribute("href") || "";
    var enriched = ensureText(href);
    if (enriched !== href) a.setAttribute("href", enriched);
  }, true);

  // También enriquecer en mouseover/touchstart por si el link se abre con
  // click derecho / "abrir en nueva pestaña"
  document.addEventListener("mouseover", function (e) {
    var a = e.target && e.target.closest && e.target.closest('a[href*="wa.me/"]');
    if (!a || a.dataset.waEnriched === "1") return;
    var href = a.getAttribute("href") || "";
    var enriched = ensureText(href);
    if (enriched !== href) {
      a.setAttribute("href", enriched);
      a.dataset.waEnriched = "1";
    }
  }, true);
})();
