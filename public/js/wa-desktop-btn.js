/**
 * wa-desktop-btn.js
 * Inyecta el botón flotante de WhatsApp en desktop (md+) para páginas que
 * no tienen uno propio. Idempotente: si ya existe un .wa-floating-btn o
 * #wa-btn en el DOM, no hace nada.
 *
 * Cargar con: <script src="/js/wa-desktop-btn.js" defer></script>
 */
(function () {
  "use strict";
  if (window.__waDesktopBtnLoaded) return;
  window.__waDesktopBtnLoaded = true;

  function pickPhone() {
    var path = (location.pathname || "").toLowerCase();
    if (path.indexOf("/servicios/banos-quimicos") === 0 ||
        path.indexOf("/banos-quimicos") === 0) {
      return "56936470112";
    }
    return "56997946463";
  }

  function alreadyHasWaBtn() {
    return !!(document.querySelector('.wa-floating-btn') ||
              document.getElementById('wa-btn'));
  }

  function injectStyles() {
    if (document.getElementById('wa-desktop-btn-styles')) return;
    var s = document.createElement('style');
    s.id = 'wa-desktop-btn-styles';
    s.textContent = [
      ':root{--wa-green:#25D366;}',
      '.wa-desktop-fab{position:fixed;bottom:20px;left:20px;width:60px;height:60px;',
      'background-color:var(--wa-green);color:#fff;border-radius:50%;',
      'display:none;align-items:center;justify-content:center;',
      'box-shadow:0 4px 10px rgba(0,0,0,.3);cursor:pointer;z-index:1000;',
      'transition:all .3s ease;animation:wa-pulse 2s infinite;text-decoration:none;}',
      '@media(min-width:768px){.wa-desktop-fab{display:flex;}}',
      '.wa-desktop-fab:hover{transform:scale(1.1);}',
      '.wa-desktop-fab svg{width:35px;height:35px;fill:#fff;}',
      '@keyframes wa-pulse{0%{box-shadow:0 0 0 0 rgba(37,211,102,.7);}',
      '70%{box-shadow:0 0 0 15px rgba(37,211,102,0);}',
      '100%{box-shadow:0 0 0 0 rgba(37,211,102,0);}}'
    ].join('');
    document.head.appendChild(s);
  }

  function buildBtn() {
    var phone = pickPhone();
    var a = document.createElement('a');
    a.href = 'https://wa.me/' + phone;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.className = 'wa-desktop-fab';
    a.setAttribute('aria-label', 'Enviar mensaje por WhatsApp');
    a.innerHTML = '<svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.008-.57-.008-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>';
    return a;
  }

  function init() {
    if (alreadyHasWaBtn()) return;
    injectStyles();
    document.body.appendChild(buildBtn());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
