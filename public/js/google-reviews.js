/**
 * Widget de reseñas reales de Google.
 *
 * Uso:
 *   <div data-google-reviews
 *        data-limit="6"
 *        data-min-stars="4"></div>
 *
 * Hace fetch a /api/google-reviews y renderiza un slider/grilla simple.
 */

(function () {
  'use strict';

  const ENDPOINT = '/api/google-reviews';

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
    })[c]);
  }

  function starsHtml(rating) {
    const full = Math.round(rating);
    let html = '';
    for (let i = 1; i <= 5; i++) {
      html += `<i class="fa-solid fa-star ${i <= full ? 'text-yellow-400' : 'text-slate-200'}"></i>`;
    }
    return html;
  }

  function initialOf(name) {
    if (!name) return 'G';
    const parts = name.trim().split(/\s+/);
    return (parts[0][0] + (parts[1] ? parts[1][0] : '')).toUpperCase();
  }

  function reviewCard(r) {
    const initials = initialOf(r.author);
    const photo = r.photo
      ? `<img src="${escapeHtml(r.photo)}" alt="${escapeHtml(r.author)}" loading="lazy" class="w-10 h-10 rounded-full object-cover" referrerpolicy="no-referrer">`
      : `<div class="w-10 h-10 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-sm">${initials}</div>`;
    return `
      <article class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm flex flex-col h-full">
        <header class="flex items-center gap-3 mb-3">
          ${photo}
          <div class="flex-1 min-w-0">
            <p class="font-semibold text-slate-800 truncate">${escapeHtml(r.author)}</p>
            <p class="text-xs text-slate-500">${escapeHtml(r.relativeTime || '')}</p>
          </div>
          <i class="fa-brands fa-google text-slate-400" aria-label="Reseña en Google"></i>
        </header>
        <div class="text-sm mb-2" aria-label="${r.rating} de 5 estrellas">${starsHtml(r.rating)}</div>
        <p class="text-slate-700 text-sm leading-relaxed line-clamp-5">${escapeHtml(r.text || '')}</p>
      </article>`;
  }

  function summaryBlock(d) {
    if (!d.rating) return '';
    return `
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white rounded-2xl border border-slate-200 p-5 mb-6">
        <div class="flex items-center gap-4">
          <div class="text-4xl font-extrabold text-slate-900">${d.rating.toFixed(1)}</div>
          <div>
            <div class="text-yellow-500 text-lg">${starsHtml(d.rating)}</div>
            <p class="text-xs text-slate-500">Basado en ${d.total} reseñas reales en Google</p>
          </div>
        </div>
        ${d.mapsUrl ? `<a href="${escapeHtml(d.mapsUrl)}" target="_blank" rel="noopener" class="text-sm font-semibold text-blue-600 hover:underline">Ver todas en Google &rarr;</a>` : ''}
      </div>`;
  }

  function render(container, data) {
    const limit = parseInt(container.dataset.limit || '6', 10);
    const minStars = parseInt(container.dataset.minStars || '0', 10);
    const reviews = (data.reviews || [])
      .filter((r) => r.rating >= minStars && r.text)
      .slice(0, limit);

    if (!reviews.length && !data.rating) {
      container.innerHTML = '<p class="text-sm text-slate-500 text-center">Aún no hay reseñas para mostrar.</p>';
      return;
    }

    container.innerHTML = `
      ${summaryBlock(data)}
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        ${reviews.map(reviewCard).join('')}
      </div>
      <p class="mt-6 text-xs text-slate-500 text-center">
        Reseñas obtenidas en vivo desde Google Business · actualizadas cada 6 h.
      </p>
    `;
  }

  function loadInto(container) {
    container.setAttribute('aria-busy', 'true');
    fetch(ENDPOINT, { headers: { Accept: 'application/json' } })
      .then((r) => {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then((data) => render(container, data))
      .catch((err) => {
        console.warn('google-reviews: no se pudieron cargar reseñas:', err);
        container.innerHTML = '<p class="text-sm text-slate-500 text-center">No se pudieron cargar las reseñas en este momento.</p>';
      })
      .finally(() => container.removeAttribute('aria-busy'));
  }

  function init() {
    const containers = document.querySelectorAll('[data-google-reviews]');
    containers.forEach(loadInto);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
