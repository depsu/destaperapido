document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('casos-grid');
    const filterButtons = document.querySelectorAll('.filter-btn');

    if (!container) return; // Exit if container doesn't exist on this page

    // Fetch data
    fetch('/data/casos.json')
        .then(response => response.json())
        .then(data => {
            renderCards(data);
            setupFilters(data);
        })
        .catch(error => console.error('Error loading blog cases:', error));

    function renderCards(cases) {
        container.innerHTML = cases.map(caso => `
            <article class="bg-white rounded-3xl overflow-hidden shadow-lg border border-slate-100 hover:shadow-2xl transition-all duration-300 group fade-in" data-category="${caso.category}">
                <div class="grid md:grid-cols-2 h-full">
                    <div class="relative h-64 md:h-full overflow-hidden">
                        <img src="${caso.image}" alt="${caso.title}" loading="lazy"
                            class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
                        <div class="absolute top-4 left-4 ${caso.badgeColor} text-white text-xs font-bold px-3 py-1 rounded-full">
                            ${caso.badgeText}
                        </div>
                    </div>
                    <div class="p-8 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-3">
                                <i class="fa-solid fa-location-dot"></i> ${caso.location}
                            </div>
                            <h3 class="text-xl font-extrabold text-slate-900 mb-4">${caso.title}</h3>

                            <div class="space-y-4">
                                <div>
                                    <h4 class="text-sm font-bold text-red-500 mb-1 flex items-center gap-2">
                                        <i class="fa-solid fa-circle-xmark"></i> El Problema
                                    </h4>
                                    <p class="text-sm text-slate-600">${caso.problem}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-bold text-green-600 mb-1 flex items-center gap-2">
                                        <i class="fa-solid fa-circle-check"></i> La Solución
                                    </h4>
                                    <p class="text-sm text-slate-600">${caso.solution}</p>
                                </div>
                            </div>
                        </div>

                        <div class="mt-8 pt-6 border-t border-slate-100 flex justify-between items-center">
                            <span class="text-xs font-bold text-slate-400">${caso.meta}</span>
                            <a href="${caso.link}" class="text-brand-600 font-bold text-sm hover:underline">
                                Tengo este problema &rarr;
                            </a>
                        </div>
                    </div>
                </div>
            </article>
        `).join('');
    }

    function setupFilters(allCases) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active state
                filterButtons.forEach(b => {
                    b.classList.remove('bg-brand-600', 'text-white', 'border-transparent');
                    b.classList.add('bg-white', 'text-slate-600', 'border-slate-200');
                });
                btn.classList.remove('bg-white', 'text-slate-600', 'border-slate-200');
                btn.classList.add('bg-brand-600', 'text-white', 'border-transparent');

                const filter = btn.dataset.filter;

                if (filter === 'all') {
                    renderCards(allCases);
                } else {
                    const filtered = allCases.filter(c => c.category === filter);
                    renderCards(filtered);
                }
            });
        });
    }
});
