(function () {
  'use strict';

  const ENDPOINT = '/data/google-reviews.json';

  function esc(str) {
    return String(str).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    })[c]);
  }

  const starPath = 'M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z';

  const googleSvg = `<svg class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>`;

  function heroStars(rating) {
    const full = Math.round(rating);
    const uid = 'gr-' + Math.random().toString(36).slice(2, 8);
    let html = '';
    for (let i = 1; i <= 5; i++) {
      const delay = (i - 1) * 80;
      const isMid = i === 3;
      const size = isMid ? 'h-14 w-14 md:h-16 md:w-16' : 'h-10 w-10 md:h-12 md:w-12';
      const shadow = isMid ? 'drop-shadow-lg' : 'drop-shadow';

      if (i <= full && isMid) {
        html += `
          <svg class="${size} gr-star opacity-0 scale-0 ${shadow}" viewBox="0 0 24 24" data-delay="${delay}">
            <defs>
              <clipPath id="${uid}-tl"><rect x="0" y="0" width="12" height="12"/></clipPath>
              <clipPath id="${uid}-tr"><rect x="12" y="0" width="12" height="12"/></clipPath>
              <clipPath id="${uid}-br"><rect x="12" y="12" width="12" height="12"/></clipPath>
              <clipPath id="${uid}-bl"><rect x="0" y="12" width="12" height="12"/></clipPath>
            </defs>
            <path clip-path="url(#${uid}-tl)" fill="#EA4335" d="${starPath}"/>
            <path clip-path="url(#${uid}-tr)" fill="#4285F4" d="${starPath}"/>
            <path clip-path="url(#${uid}-br)" fill="#34A853" d="${starPath}"/>
            <path clip-path="url(#${uid}-bl)" fill="#FBBC05" d="${starPath}"/>
          </svg>`;
      } else {
        const fill = i <= full ? 'fill-yellow-400' : 'fill-slate-200';
        html += `
          <svg class="${size} gr-star opacity-0 scale-0 ${fill} ${shadow}" viewBox="0 0 24 24" data-delay="${delay}">
            <path d="${starPath}"/>
          </svg>`;
      }
    }
    return html;
  }

  function smallStars(rating) {
    const full = Math.round(rating);
    let h = '';
    for (let i = 1; i <= 5; i++) {
      h += `<i class="fa-solid fa-star ${i <= full ? 'text-yellow-400' : 'text-slate-200'} text-sm"></i>`;
    }
    return h;
  }

  function initials(name) {
    if (!name) return 'G';
    const p = name.trim().split(/\s+/);
    return (p[0][0] + (p[1] ? p[1][0] : '')).toUpperCase();
  }

  function card(r, idx) {
    const avatar = r.photo
      ? `<img src="${esc(r.photo)}" alt="${esc(r.author)}" loading="lazy" class="w-11 h-11 rounded-full object-cover" referrerpolicy="no-referrer">`
      : `<div class="w-11 h-11 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-sm">${initials(r.author)}</div>`;
    return `
      <article class="gr-card opacity-0 translate-y-6 bg-white rounded-2xl p-6 shadow-md shadow-slate-200/60 border border-slate-100 flex flex-col h-full hover:shadow-xl hover:-translate-y-1 transition-all duration-300" data-delay="${idx * 100}">
        <header class="flex items-center gap-3 mb-4">
          ${avatar}
          <div class="flex-1 min-w-0">
            <p class="font-bold text-slate-900 truncate">${esc(r.author)}</p>
            <div class="flex items-center gap-2">
              <span class="flex gap-0.5">${smallStars(r.rating)}</span>
              <span class="text-xs text-slate-400">${esc(r.relativeTime || '')}</span>
            </div>
          </div>
          ${googleSvg}
        </header>
        <p class="text-slate-600 text-[15px] leading-relaxed line-clamp-4 flex-1">${esc(r.text || '')}</p>
      </article>`;
  }

  function hero(d) {
    if (!d.rating) return '';
    const reviewUrl = 'https://xn--resealo-7za.cl/destape-rapido';
    const link = `<a href="${reviewUrl}" target="_blank" rel="noopener"
          class="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 font-semibold text-sm transition-colors">
          Deja tu rese&ntilde;a <i class="fa-solid fa-arrow-right text-xs"></i>
        </a>`;
    return `
      <div class="flex flex-col items-center text-center mb-14">
        <div class="flex items-center justify-center gap-2 md:gap-3 mb-6" aria-hidden="true">
          ${heroStars(d.rating)}
        </div>
        <div class="flex items-end justify-center gap-2 mb-3">
          <span class="gr-rating text-7xl md:text-8xl font-black text-slate-900 leading-none tabular-nums" data-target="${d.rating.toFixed(1)}">0.0</span>
          <span class="text-slate-300 text-2xl font-medium mb-3">/ 5</span>
        </div>
        <div class="inline-flex items-center gap-2.5 bg-white border border-slate-200 rounded-full px-4 py-2 shadow-sm mb-4">
          ${googleSvg}
          <span class="text-sm font-semibold text-slate-700">Rese&ntilde;as verificadas en Google</span>
        </div>
        <p class="text-slate-500 text-base max-w-md mb-3">
          Basado en <strong class="text-slate-700">${d.total} rese&ntilde;as reales</strong> de clientes que contrataron nuestros servicios.
        </p>
        ${link}
      </div>`;
  }

  function animate(container) {
    if (typeof IntersectionObserver === 'undefined') {
      container.querySelectorAll('.gr-star, .gr-card').forEach((el) => {
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
      const num = container.querySelector('.gr-rating');
      if (num) num.textContent = num.dataset.target;
      return;
    }

    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);

        container.querySelectorAll('.gr-star').forEach((star) => {
          const delay = parseInt(star.dataset.delay || '0', 10);
          setTimeout(() => {
            star.style.transition = 'opacity 0.4s ease, transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
            star.style.opacity = '1';
            star.style.transform = 'scale(1)';
          }, delay);
        });

        const num = container.querySelector('.gr-rating');
        if (num) {
          const target = parseFloat(num.dataset.target);
          const duration = 800;
          const start = performance.now();
          function tick(now) {
            const t = Math.min((now - start) / duration, 1);
            const ease = 1 - Math.pow(1 - t, 3);
            num.textContent = (target * ease).toFixed(1);
            if (t < 1) requestAnimationFrame(tick);
          }
          setTimeout(() => requestAnimationFrame(tick), 350);
        }

        container.querySelectorAll('.gr-card').forEach((c) => {
          const delay = parseInt(c.dataset.delay || '0', 10);
          setTimeout(() => {
            c.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            c.style.opacity = '1';
            c.style.transform = 'translateY(0)';
          }, 500 + delay);
        });
      });
    }, { threshold: 0.15 });

    io.observe(container);
  }

  function compactCard(r) {
    const avatar = r.photo
      ? `<img src="${esc(r.photo)}" alt="${esc(r.author)}" loading="lazy" class="w-9 h-9 rounded-full object-cover" referrerpolicy="no-referrer">`
      : `<div class="w-9 h-9 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-xs">${initials(r.author)}</div>`;
    return `
      <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-100 flex-1 min-w-0">
        <p class="text-slate-600 text-sm leading-relaxed line-clamp-3 mb-3">"${esc(r.text || '')}"</p>
        <div class="flex items-center gap-2">
          ${avatar}
          <div class="min-w-0">
            <p class="font-semibold text-slate-800 text-sm truncate">${esc(r.author)}</p>
            <span class="flex gap-0.5">${smallStars(r.rating)}</span>
          </div>
        </div>
      </div>`;
  }

  function renderCompact(container, data) {
    const reviews = filterReviews(data.reviews || [], container).slice(0, 2);

    if (!data.rating) {
      container.innerHTML = '';
      return;
    }

    const reviewUrl = 'https://xn--resealo-7za.cl/destape-rapido';
    container.innerHTML = `
      <div class="flex flex-col sm:flex-row items-center gap-6">
        <div class="flex flex-col items-center gap-1 flex-shrink-0">
          <div class="flex gap-1">${smallStars(data.rating).replace(/text-sm/g, 'text-lg')}</div>
          <p class="text-2xl font-black text-slate-900">${data.rating.toFixed(1)}<span class="text-slate-300 text-base font-medium"> / 5</span></p>
          <div class="inline-flex items-center gap-1.5 mt-1">
            ${googleSvg}
            <span class="text-xs font-semibold text-slate-500">${data.total} rese&ntilde;as</span>
          </div>
          <a href="${reviewUrl}" target="_blank" rel="noopener" class="text-xs text-blue-600 hover:text-blue-800 font-semibold mt-1">Deja tu rese&ntilde;a &rarr;</a>
        </div>
        <div class="flex flex-col sm:flex-row gap-3 flex-1 min-w-0">
          ${reviews.map(compactCard).join('')}
        </div>
      </div>
    `;
  }

  function filterReviews(reviews, container) {
    const minStars = parseInt(container.dataset.minStars || '0', 10);
    const limit = parseInt(container.dataset.limit || '6', 10);
    const deprioritize = (container.dataset.exclude || '').toLowerCase().split(',').map((s) => s.trim()).filter(Boolean);

    const valid = reviews.filter((r) => r.rating >= minStars && r.text);

    if (!deprioritize.length) return valid.slice(0, limit);

    const preferred = valid.filter((r) => !deprioritize.some((kw) => (r.text || '').toLowerCase().includes(kw)));
    const rest = valid.filter((r) => deprioritize.some((kw) => (r.text || '').toLowerCase().includes(kw)));

    return [...preferred, ...rest].slice(0, limit);
  }

  function render(container, data) {
    if (container.hasAttribute('data-compact')) {
      return renderCompact(container, data);
    }

    const reviews = filterReviews(data.reviews || [], container);

    if (!reviews.length && !data.rating) {
      container.innerHTML = '<p class="text-sm text-slate-500 text-center">A&uacute;n no hay rese&ntilde;as para mostrar.</p>';
      return;
    }

    container.innerHTML = `
      ${hero(data)}
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
        ${reviews.map(card).join('')}
      </div>
    `;

    animate(container);
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
        console.warn('google-reviews:', err);
        container.innerHTML = '<p class="text-sm text-slate-500 text-center">No se pudieron cargar las rese&ntilde;as.</p>';
      })
      .finally(() => container.removeAttribute('aria-busy'));
  }

  function init() {
    document.querySelectorAll('[data-google-reviews]').forEach(loadInto);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
