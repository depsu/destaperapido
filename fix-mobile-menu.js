const fs = require('fs');
const path = require('path');

const indexContent = fs.readFileSync('public/index.html', 'utf8');

// 1. Obtener el panel del menú móvil
const mobileMenuRegex = /<div id="mobile-menu-overlay"[\s\S]*?<\/div>\s*<\/div>/;
const mobileMenuMatch = indexContent.match(mobileMenuRegex);
if (!mobileMenuMatch) { console.error("Error: No se encontró mobile-menu-overlay en index.html"); process.exit(1); }
const mobileMenuPanelHtml = mobileMenuMatch[0];

// 2. Obtener el botón de toggle móvil
// Buscamos el bloque específico en index.html
const toggleBtnRegex = /<!-- Mobile Toggle -->[\s\S]*?<\/div>/;
const toggleBtnMatch = indexContent.match(toggleBtnRegex);
let toggleBtnHtml = '';
if (toggleBtnMatch) {
    toggleBtnHtml = toggleBtnMatch[0];
} else {
    // Fallback manual si no se encuentra el comentario
    toggleBtnHtml = `
                <div class="flex items-center gap-4 lg:hidden">
                    <a href="tel:+56936470112"
                        class="flex items-center justify-center w-10 h-10 rounded-full bg-slate-100 text-slate-900 active:scale-95 transition">
                        <i class="fa-solid fa-phone"></i>
                    </a>
                    <button onclick="openMenu()" aria-label="Abrir menú de navegación"
                        class="p-2.5 rounded-lg text-slate-900 hover:bg-slate-100 focus:outline-none transition active:scale-95">
                        <i class="fa-solid fa-bars text-2xl"></i>
                    </button>
                </div>`;
}

// 3. Obtener el script del menú
// Buscamos la función openMenu en index.html y extraemos el bloque script
const scriptRegex = /<script>[\s\S]*?function openMenu\(\)[\s\S]*?<\/script>/;
const scriptMatch = indexContent.match(scriptRegex);
let scriptHtml = '';
if (scriptMatch) {
    scriptHtml = scriptMatch[0];
} else {
    // Fallback manual
    scriptHtml = `
    <script>
        const overlay = document.getElementById('mobile-menu-overlay');
        const panel = document.getElementById('mobile-menu-panel');

        function openMenu() {
            if (overlay && panel) {
                overlay.classList.remove('invisible', 'opacity-0');
                panel.classList.remove('translate-x-full');
                document.body.style.overflow = 'hidden';
            }
        }

        function closeMenu() {
            if (overlay && panel) {
                panel.classList.add('translate-x-full');
                overlay.classList.add('invisible', 'opacity-0');
                document.body.style.overflow = '';
            }
        }

        function toggleSubmenu(id, btn) {
            const submenu = document.getElementById(id);
            const icon = btn.querySelector('.fa-chevron-down');
            if (submenu) {
                if (submenu.classList.contains('hidden')) {
                    submenu.classList.remove('hidden');
                    if (icon) icon.style.transform = 'rotate(180deg)';
                } else {
                    submenu.classList.add('hidden');
                    if (icon) icon.style.transform = 'rotate(0deg)';
                }
            }
        }
    </script>`;
}

function getAllHtmlFiles(dirPath, arrayOfFiles) {
    const files = fs.readdirSync(dirPath);
    arrayOfFiles = arrayOfFiles || [];
    files.forEach(function (file) {
        if (fs.statSync(dirPath + "/" + file).isDirectory()) {
            arrayOfFiles = getAllHtmlFiles(dirPath + "/" + file, arrayOfFiles);
        } else {
            if (file.endsWith('.html') && !file.endsWith('index.html')) {
                arrayOfFiles.push(path.join(dirPath, "/", file));
            }
            // Incluir index.html de subdirectorios
            if (file === 'index.html' && dirPath !== 'public') {
                arrayOfFiles.push(path.join(dirPath, "/", file));
            }
        }
    });
    return arrayOfFiles;
}

const files = getAllHtmlFiles('public');
let updatedCount = 0;

files.forEach(file => {
    // Saltar el index.html raíz
    if (path.resolve(file) === path.resolve('public/index.html')) return;

    let content = fs.readFileSync(file, 'utf8');
    let originalContent = content;
    let modified = false;

    // 1. Actualizar o Insertar Panel del Menú
    if (content.includes('id="mobile-menu-overlay"')) {
        // Ya existe, reemplazarlo
        content = content.replace(mobileMenuRegex, mobileMenuPanelHtml);
        modified = true;
    } else {
        // No existe, insertar antes del cierre del body
        if (content.includes('</body>')) {
            content = content.replace('</body>', `${mobileMenuPanelHtml}\n</body>`);
            modified = true;
        }
    }

    // 2. Insertar Botón Toggle si no existe
    if (!content.includes('onclick="openMenu()"')) {
        // Buscar el cierre del div que contiene los botones de desktop en el nav
        // En vitacura.html es: <div class="flex items-center gap-4"> ... </div>
        // Intentamos encontrar el cierre de ese div y poner el botón después

        // Estrategia: Buscar el último </div> antes de </nav> y pegarlo antes de eso.
        // El nav suele cerrar con </div></div></nav>
        const navEndRegex = /(<\/div>\s*<\/div>\s*<\/nav>)/;
        if (navEndRegex.test(content)) {
            // Insertar antes del cierre de los contenedores del nav
            // Pero necesitamos que esté dentro del contenedor flex principal del nav
            // El contenedor flex es: <div class="flex justify-between items-center h-17">

            // Vamos a intentar insertar justo después del último div que sea hijo directo del flex container.
            // Esto es difícil con regex.

            // Alternativa: Buscar el botón de teléfono desktop y añadirlo después de su cierre de div padre.
            // Patrón común: <div class="flex items-center gap-4"> ... </div>
            const desktopBtnContainerRegex = /(<div class="[^"]*flex items-center gap-4[^"]*">[\s\S]*?<\/div>)/;

            if (desktopBtnContainerRegex.test(content)) {
                content = content.replace(desktopBtnContainerRegex, `$1\n${toggleBtnHtml}`);
                modified = true;
            } else {
                console.warn(`No se pudo encontrar lugar para insertar botón toggle en ${file}`);
            }
        }
    }

    // 3. Insertar Script si no existe
    if (!content.includes('function openMenu()')) {
        if (content.includes('</body>')) {
            content = content.replace('</body>', `${scriptHtml}\n</body>`);
            modified = true;
        }
    }

    if (modified) {
        fs.writeFileSync(file, content, 'utf8');
        console.log(`Corregido menú móvil en: ${file}`);
        updatedCount++;
    }
});

console.log(`Total de archivos corregidos: ${updatedCount}`);
