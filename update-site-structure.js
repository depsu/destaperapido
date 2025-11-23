const fs = require('fs');
const path = require('path');

const indexContent = fs.readFileSync('public/index.html', 'utf8');

// Extraer Menú Móvil
// Buscamos desde <div id="mobile-menu-panel" hasta el cierre del div antes del script o footer.
// El menú móvil termina antes de <header class="hero... o <main...
// En index.html, el menú móvil está dentro de <div id="mobile-menu-overlay">...</div>
// Mejor extraigo todo el bloque del overlay.
const mobileMenuRegex = /<div id="mobile-menu-overlay"[\s\S]*?<\/div>\s*<\/div>/;
const mobileMenuMatch = indexContent.match(mobileMenuRegex);

if (!mobileMenuMatch) {
    console.error("No se pudo encontrar el menú móvil en index.html");
    process.exit(1);
}
const newMobileMenu = mobileMenuMatch[0];

// Extraer Footer
const footerRegex = /<footer[\s\S]*?<\/footer>/;
const footerMatch = indexContent.match(footerRegex);

if (!footerMatch) {
    console.error("No se pudo encontrar el footer en index.html");
    process.exit(1);
}
const newFooter = footerMatch[0];

function getAllHtmlFiles(dirPath, arrayOfFiles) {
    const files = fs.readdirSync(dirPath);
    arrayOfFiles = arrayOfFiles || [];

    files.forEach(function (file) {
        if (fs.statSync(dirPath + "/" + file).isDirectory()) {
            arrayOfFiles = getAllHtmlFiles(dirPath + "/" + file, arrayOfFiles);
        } else {
            if (file.endsWith('.html') && !file.endsWith('index.html')) { // Excluir index.html origen
                arrayOfFiles.push(path.join(dirPath, "/", file));
            }
            // Si index.html está en subdirectorios, también actualizarlo
            if (file === 'index.html' && dirPath !== 'public') {
                // Ya se incluyó arriba si termina en .html
            }
        }
    });

    return arrayOfFiles;
}

const files = getAllHtmlFiles('public');
let updatedCount = 0;

files.forEach(file => {
    // Saltar el index.html raíz ya que es la fuente
    if (path.resolve(file) === path.resolve('public/index.html')) return;

    let content = fs.readFileSync(file, 'utf8');
    let originalContent = content;

    // Reemplazar Menú Móvil
    // Usamos regex similar para encontrar el bloque en el archivo destino
    if (mobileMenuRegex.test(content)) {
        content = content.replace(mobileMenuRegex, newMobileMenu);
    } else {
        console.warn(`Menú móvil no encontrado en ${file}`);
    }

    // Reemplazar Footer
    if (footerRegex.test(content)) {
        content = content.replace(footerRegex, newFooter);
    } else {
        console.warn(`Footer no encontrado en ${file}`);
    }

    if (content !== originalContent) {
        fs.writeFileSync(file, content, 'utf8');
        console.log(`Actualizado: ${file}`);
        updatedCount++;
    }
});

console.log(`Total de archivos actualizados: ${updatedCount}`);
