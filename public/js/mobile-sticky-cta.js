/**
 * mobile-sticky-cta.js
 * Inyecta dinámicamente un sticky CTA dual (Llamar + WhatsApp) en la zona del
 * pulgar para móvil, en cualquier página que aún no lo tenga. Idempotente:
 * si ya existe un sticky en el DOM, no hace nada.
 *
 * Cargar con: <script src="/js/mobile-sticky-cta.js" defer></script>
 */
(function () {
  "use strict";
  if (window.__mobileStickyCtaLoaded) return;
  window.__mobileStickyCtaLoaded = true;

  // Número principal vs línea de baños químicos
  function pickPhone() {
    var path = (location.pathname || "").toLowerCase();
    if (path.indexOf("/servicios/banos-quimicos") === 0 ||
        path.indexOf("/banos-quimicos") === 0) {
      return "56936470112";
    }
    return "56928461485";
  }

  function alreadyHasSticky() {
    // Heurísticas: comentario marcador, clase típica del bloque actual
    if (document.querySelector('.mobile-sticky-cta')) return true;
    var bottoms = document.querySelectorAll('.fixed.bottom-0');
    for (var i = 0; i < bottoms.length; i++) {
      var el = bottoms[i];
      if (el.querySelector('a[href^="tel:"]') && el.querySelector('a[href*="wa.me/"]')) {
        return true;
      }
    }
    return false;
  }

  // Inyecta padding-bottom global en móvil siempre (defensivo: aplica
  // tanto si este script monta el sticky como si la página ya trae el suyo).
  function injectGlobalPadding() {
    if (document.getElementById('mobile-sticky-pad-styles')) return;
    var s = document.createElement('style');
    s.id = 'mobile-sticky-pad-styles';
    s.textContent = '@media (max-width: 767px){body{padding-bottom:calc(96px + env(safe-area-inset-bottom));}body.has-bottom-pad-extra{padding-bottom:calc(120px + env(safe-area-inset-bottom));}.wa-floating-btn{display:none !important;}}';
    document.head.appendChild(s);
  }

  function injectStyles() {
    if (document.getElementById('mobile-sticky-cta-styles')) return;
    var s = document.createElement('style');
    s.id = 'mobile-sticky-cta-styles';
    s.textContent = [
      '.mobile-sticky-cta{position:fixed;left:0;right:0;bottom:0;z-index:50;display:none;background:#fff;box-shadow:0 -4px 20px rgba(0,0,0,.15);padding-bottom:env(safe-area-inset-bottom);}',
      '@media (max-width: 767px){.mobile-sticky-cta{display:flex;flex-direction:column;}}',
      '.mobile-sticky-cta .msc-row{display:flex;gap:.75rem;padding:.75rem;border-top:1px solid #f1f5f9;}',
      '.mobile-sticky-cta a{flex:1;display:flex;align-items:center;justify-content:center;gap:.5rem;font-weight:700;border-radius:.75rem;padding:.85rem .5rem;font-size:.95rem;text-decoration:none;transition:transform .1s ease;}',
      '.mobile-sticky-cta a:active{transform:scale(.97);}',
      '.mobile-sticky-cta .msc-call{background:#1e293b;color:#fff;box-shadow:0 6px 14px rgba(15,23,42,.2);}',
      '.mobile-sticky-cta .msc-wa{background:#15803d;color:#fff;box-shadow:0 6px 14px rgba(21,128,61,.25);}',
      '.mobile-sticky-cta .msc-icon{display:inline-block;width:1.1rem;height:1.1rem;}'
    ].join('');
    document.head.appendChild(s);
  }

  function buildSticky() {
    var phone = pickPhone();
    var wrap = document.createElement('div');
    wrap.className = 'mobile-sticky-cta';
    wrap.setAttribute('role', 'region');
    wrap.setAttribute('aria-label', 'Acciones rápidas: llamar o WhatsApp');
    wrap.innerHTML = [
      '<div class="msc-row">',
        '<a class="msc-call" href="tel:+', phone, '" aria-label="Llamar ahora">',
          '<svg class="msc-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.05 15.05 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25c1.12.37 2.33.57 3.6.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.27.2 2.48.57 3.6a1 1 0 0 1-.25 1l-2.22 2.2z"/></svg>',
          ' Llamar',
        '</a>',
        '<a class="msc-wa" href="https://wa.me/', phone, '" aria-label="Enviar mensaje por WhatsApp">',
          '<svg class="msc-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.5-.2-.7.1-.2.3-.8.9-1 1.1-.2.2-.4.2-.7.1-.3-.2-1.2-.5-2.4-1.5-.9-.8-1.5-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.4.3-.5.1-.2 0-.4-.1-.5l-1-2.2c-.2-.5-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5 0 1.5 1 2.9 1.2 3.1.2.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.4M12 22h-.1c-1.8 0-3.6-.5-5.1-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.9 9.9 0 0 1 2 12c0-5.5 4.5-10 10-10s10 4.5 10 10-4.5 10-10 10m8.4-18.3A11.8 11.8 0 0 0 12 0C5.4 0 .1 5.3.1 11.9c0 2.1.5 4.1 1.6 5.9L0 24l6.3-1.7c1.7 1 3.7 1.5 5.7 1.5h.1C18.6 23.8 24 18.5 24 11.9a11.8 11.8 0 0 0-3.6-8.2"/></svg>',
          ' WhatsApp',
        '</a>',
      '</div>'
    ].join('');
    return wrap;
  }

  function init() {
    // Aplicar padding global siempre, así no se tapa contenido aunque la
    // página tenga su propio sticky en HTML.
    injectGlobalPadding();
    if (alreadyHasSticky()) return;
    injectStyles();
    var node = buildSticky();
    document.body.appendChild(node);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
