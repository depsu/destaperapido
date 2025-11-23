document.addEventListener('DOMContentLoaded', () => {
    // CONFIGURATION
    const CONFIG = {
        DROP_TO_2_MIN: 30000, // 30 seconds
        DROP_TO_2_MAX: 60000, // 60 seconds
        DROP_TO_1_MIN: 300000, // 5 minutes
        DROP_TO_1_MAX: 600000, // 10 minutes
        RESET_HOURS: 2,
        STORAGE_KEY: 'alc_pro_units_state_v3' // Unified key
    };

    const getRandomTime = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);

    const calculateState = () => {
        const now = Date.now();
        const savedState = localStorage.getItem(CONFIG.STORAGE_KEY);
        const resetTimeMs = CONFIG.RESET_HOURS * 60 * 60 * 1000;

        if (!savedState) return createNewState(now);

        let data = JSON.parse(savedState);

        if (!data.timestamp || (now - data.timestamp > resetTimeMs)) {
            return createNewState(now);
        }

        data.timestamp = now;

        if (data.count <= 1) {
            localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(data));
            return data;
        }

        if (now > data.nextChange) {
            data.count--;
            if (data.count === 2) {
                data.nextChange = now + getRandomTime(CONFIG.DROP_TO_1_MIN, CONFIG.DROP_TO_1_MAX);
            } else {
                data.nextChange = null;
            }
            localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(data));
            triggerFlashEffect();
        } else {
            localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(data));
        }
        return data;
    };

    const createNewState = (now) => {
        const newState = {
            count: 3, // Start with 3
            nextChange: now + getRandomTime(CONFIG.DROP_TO_2_MIN, CONFIG.DROP_TO_2_MAX),
            timestamp: now
        };
        localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(newState));
        return newState;
    };

    const renderUI = (count) => {
        const badges = document.querySelectorAll('.availability-badge');
        badges.forEach(badge => {
            const countSpan = badge.querySelector('.unit-count');
            const textSpan = badge.querySelector('.unit-text');
            const pingDot = badge.querySelector('.ping-dot');
            const staticDot = badge.querySelector('.static-dot');

            // --- TEXT & COLOR LOGIC ---

            const isDark = badge.getAttribute('data-theme') === 'dark';

            if (count <= 1) {
                // CASE 1: URGENCY (Orange)
                if (countSpan) countSpan.innerText = "Queda 1 camión";
                // Note: The structure in HTML might be <span><span class="unit-count">3</span> <span class="unit-text">Camiones...</span></span>
                // If we replace innerText of countSpan, we might lose the space if not careful, but usually it's fine.
                // Let's stick to the user's request: "Queda 1 camión disponible Región Metropolitana"

                // However, the HTML structure is often:
                // <span>
                //    <span class="unit-count">3</span>
                //    <span class="unit-text">Camiones disponibles</span>
                // </span>

                // If we set countSpan to "Queda 1 camión", and textSpan to "disponible Región Metropolitana", it reads correctly.

                if (textSpan) textSpan.innerText = "disponible Región Metropolitana";

                if (isDark) {
                    // Dark Mode Urgency
                    badge.classList.remove('bg-white/10', 'border-white/20', 'text-slate-300', 'text-white');
                    badge.classList.add('bg-orange-900/40', 'border-orange-500/50', 'text-orange-100');
                } else {
                    // Light Mode Urgency
                    badge.classList.remove('bg-green-50', 'text-green-800', 'border-green-200', 'text-green-700', 'border-green-100'); // Remove all green variations
                    badge.classList.add('bg-orange-50', 'text-orange-800', 'border-orange-200');
                }

                if (pingDot) {
                    pingDot.classList.remove('bg-green-400');
                    pingDot.classList.add('bg-orange-400');
                }
                if (staticDot) {
                    staticDot.classList.remove('bg-green-500');
                    staticDot.classList.add('bg-orange-500');
                }
            } else {
                // CASE 2: NORMAL (Green)
                if (countSpan) countSpan.innerText = count;
                if (textSpan) textSpan.innerText = "Camiones disponibles RM";

                if (isDark) {
                    // Dark Mode Normal
                    badge.classList.add('bg-white/10', 'border-white/20', 'text-slate-300');
                    badge.classList.remove('bg-orange-900/40', 'border-orange-500/50', 'text-orange-100');
                } else {
                    // Ensure Green colors
                    badge.classList.add('bg-green-50', 'text-green-800', 'border-green-200');
                    badge.classList.remove('bg-orange-50', 'text-orange-800', 'border-orange-200');
                }

                if (pingDot) {
                    pingDot.classList.add('bg-green-400');
                    pingDot.classList.remove('bg-orange-400');
                }
                if (staticDot) {
                    staticDot.classList.add('bg-green-500');
                    staticDot.classList.remove('bg-orange-500');
                }
            }

            // Show badge smoothly
            setTimeout(() => {
                badge.classList.remove('opacity-0');
            }, 500);
        });
    };

    const triggerFlashEffect = () => {
        const badges = document.querySelectorAll('.availability-badge');
        badges.forEach(b => {
            b.style.transform = 'scale(1.05)';
            setTimeout(() => { b.style.transform = 'scale(1)'; }, 300);
        });
    }

    // Initialize Badge
    let currentState = calculateState();
    renderUI(currentState.count);

    // Timer
    setInterval(() => {
        const now = Date.now();
        if (currentState.count > 1 && currentState.nextChange && now >= currentState.nextChange) {
            currentState = calculateState();
            renderUI(currentState.count);
        }
    }, 1000);
});
