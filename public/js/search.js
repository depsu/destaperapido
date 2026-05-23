(function () {
  'use strict';

  var INPUT = document.getElementById('search-input');
  var RESULTS = document.getElementById('search-results');
  var EMPTY = document.getElementById('search-empty');
  var NO_RESULTS = document.getElementById('search-no-results');
  var COUNT = document.getElementById('search-count');
  var fuse = null;

  function normalize(str) {
    return typeof str === 'string' ? str.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase() : '';
  }

  fetch('/data/search-index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      fuse = new Fuse(data, {
        keys: [
          { name: 'title', weight: 0.4 },
          { name: 'description', weight: 0.25 },
          { name: 'keywords', weight: 0.25 },
          { name: 'category', weight: 0.1 }
        ],
        threshold: 0.4,
        includeScore: true,
        minMatchCharLength: 2,
        getFn: function (obj, path) {
          var value = Fuse.config.getFn(obj, path);
          if (Array.isArray(value)) return value.map(normalize);
          return normalize(value);
        }
      });

      var params = new URLSearchParams(window.location.search);
      var q = params.get('q');
      if (q) {
        INPUT.value = q;
        doSearch(q);
      }
    });

  INPUT.addEventListener('input', function () {
    doSearch(this.value.trim());
  });

  function doSearch(query) {
    if (!fuse || query.length < 2) {
      RESULTS.innerHTML = '';
      EMPTY.classList.remove('hidden');
      NO_RESULTS.classList.add('hidden');
      if (COUNT) COUNT.classList.add('hidden');
      return;
    }

    var results = fuse.search(normalize(query), { limit: 20 });
    EMPTY.classList.add('hidden');

    if (results.length === 0) {
      RESULTS.innerHTML = '';
      NO_RESULTS.classList.remove('hidden');
      if (COUNT) COUNT.classList.add('hidden');
      return;
    }

    NO_RESULTS.classList.add('hidden');
    if (COUNT) {
      COUNT.textContent = results.length + (results.length === 1 ? ' resultado' : ' resultados');
      COUNT.classList.remove('hidden');
    }
    RESULTS.innerHTML = results.map(function (r) { return renderResult(r.item); }).join('');
  }

  var LABELS = {
    paginas: 'Página',
    blog: 'Blog',
    zonas: 'Zona',
    servicios: 'Servicio',
    'casos-reales': 'Caso Real',
    landing: 'Landing'
  };

  var COLORS = {
    paginas: 'bg-slate-100 text-slate-700',
    blog: 'bg-amber-100 text-amber-800',
    zonas: 'bg-emerald-100 text-emerald-800',
    servicios: 'bg-brand-100 text-brand-800',
    'casos-reales': 'bg-purple-100 text-purple-800',
    landing: 'bg-sky-100 text-sky-800'
  };

  function renderResult(item) {
    var label = LABELS[item.category] || 'Página';
    var color = COLORS[item.category] || 'bg-slate-100 text-slate-700';
    return '<a href="' + item.url + '" class="block p-5 rounded-xl border border-slate-200 hover:border-brand-300 hover:shadow-md transition group">' +
      '<span class="inline-block text-[11px] font-bold uppercase tracking-widest px-2 py-0.5 rounded ' + color + ' mb-2">' + label + '</span>' +
      '<h3 class="font-bold text-slate-900 group-hover:text-brand-600 transition text-lg">' + item.title + '</h3>' +
      '<p class="text-sm text-slate-500 mt-1 line-clamp-2">' + item.description + '</p>' +
    '</a>';
  }
})();
