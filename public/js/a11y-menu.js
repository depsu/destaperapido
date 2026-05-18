/**
 * a11y-menu.js
 * Mejora la accesibilidad del menú móvil en todas las páginas:
 *  - Sincroniza aria-expanded en el botón hamburguesa con la apertura del overlay.
 *  - Cierra el menú con la tecla Escape y devuelve el foco al botón hamburguesa.
 *  - Garantiza que la primera opción del panel reciba foco al abrir.
 *
 * Funciona aunque las funciones globales openMenu()/closeMenu() varíen entre páginas.
 */
(function () {
    'use strict';

    function ready(fn) {
        if (document.readyState !== 'loading') fn();
        else document.addEventListener('DOMContentLoaded', fn);
    }

    ready(function () {
        var overlay = document.getElementById('mobile-menu-overlay');
        var panel = document.getElementById('mobile-menu-panel');
        var openBtns = document.querySelectorAll('[onclick="openMenu()"], [data-menu-open]');
        var closeBtns = document.querySelectorAll('[onclick="closeMenu()"], [data-menu-close]');
        if (!overlay || !panel) return;

        var lastOpenBtn = null;

        function setExpanded(state) {
            openBtns.forEach(function (b) {
                b.setAttribute('aria-expanded', state ? 'true' : 'false');
            });
        }

        // Observa cambios de clase en el overlay para mantener aria-expanded en sync
        var observer = new MutationObserver(function () {
            var hidden = overlay.classList.contains('invisible') || overlay.classList.contains('opacity-0');
            setExpanded(!hidden);
            if (!hidden) {
                // foco al primer link del panel (mejor UX accesible)
                var first = panel.querySelector('a, button');
                if (first) {
                    setTimeout(function () { first.focus(); }, 60);
                }
            }
        });
        observer.observe(overlay, { attributes: true, attributeFilter: ['class'] });

        // Estado inicial
        setExpanded(false);

        openBtns.forEach(function (b) {
            b.addEventListener('click', function () {
                lastOpenBtn = b;
            });
        });

        closeBtns.forEach(function (b) {
            b.addEventListener('click', function () {
                if (lastOpenBtn) {
                    setTimeout(function () { lastOpenBtn.focus(); }, 80);
                }
            });
        });

        // Cierra con Escape
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' || e.keyCode === 27) {
                var hidden = overlay.classList.contains('invisible');
                if (!hidden && typeof window.closeMenu === 'function') {
                    window.closeMenu();
                    if (lastOpenBtn) lastOpenBtn.focus();
                }
            }
        });
    });
})();
