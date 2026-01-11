import os
import re

# The standard footer we want to replicate everywhere.
#Extracted from noiostros.html
STANDARD_FOOTER = """<footer class="bg-slate-50 text-slate-500 py-12 text-sm border-t border-slate-200">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-8">

                <div class="lg:col-span-2">
                    <a href="/" class="flex items-center gap-3 mb-6" aria-label="Destape Rápido - Página de Inicio">
                        <div class="w-12 h-12 md:w-[72px] md:h-[72px] flex items-center justify-center">
                            <img src="/logo-nav.webp" alt="Logo Destape Rápido, servicio de destapes en la RM"
                                width="72" height="72" class="w-full h-full object-contain">
                        </div>
                        <div>
                            <span
                                class="block font-extrabold text-slate-900 text-xl leading-none tracking-tight">DESTAPE<span
                                    class="text-brand-600">RÁPIDO</span></span>
                            <span
                                class="text-[8px] md:text-[10px] font-bold text-slate-500 uppercase tracking-widest">Región
                                Metropolitana</span>
                        </div>
                    </a>
                    <p class="mb-6 text-slate-500 max-w-xs leading-relaxed">Soluciones sanitarias profesionales para
                        hogares y empresas. Atendemos urgencias reales con equipos certificados.</p>
                    <div class="flex gap-4">
                        <a href="/" class="text-slate-500 hover:text-brand-600 transition" aria-label="Facebook">
                            <i class="fa-brands fa-facebook text-xl"></i>
                        </a>
                        <a href="/" class="text-slate-500 hover:text-brand-600 transition" aria-label="Instagram">
                            <i class="fa-brands fa-instagram text-xl"></i>
                        </a>
                        <a href="/" class="text-slate-500 hover:text-brand-600 transition" aria-label="LinkedIn">
                            <i class="fa-brands fa-linkedin text-xl"></i>
                        </a>
                    </div>
                </div>

                <div>
                    <h4 class="text-slate-900 font-bold mb-4 uppercase tracking-wider text-xs">Servicios</h4>
                    <ul class="space-y-2">
                        <li><a href="/servicios/destape-alcantarillado.html"
                                class="hover:text-brand-600 transition">Destape Alcantarillado</a></li>
                        <li><a href="/servicios/limpieza-fosas-septicas.html"
                                class="hover:text-brand-600 transition">Limpieza Fosas Sépticas</a></li>
                        <li><a href="/servicios/destape-alcantarillado.html#mantencion"
                                class="hover:text-brand-600 transition">Mantención Edificios</a></li>
                        <li><a href="/servicios/destape-alcantarillado.html"
                                class="font-medium text-brand-600 hover:underline text-xs mt-2 block">Ver todos los
                                servicios &rarr;</a></li>
                    </ul>
                </div>

                <div>
                    <h4 class="text-slate-900 font-bold mb-4 uppercase tracking-wider text-xs">Cobertura</h4>
                    <ul class="space-y-2">
                        <li><a href="/zonas/urbano/index.html" class="hover:text-brand-600 transition">Las Condes /
                                Vitacura</a></li>
                        <li><a href="/zonas/rural/chicureo.html" class="hover:text-brand-600 transition">Chicureo /
                                Colina</a></li>
                        <li><a href="/zonas/rural/pirque.html" class="hover:text-brand-600 transition">Pirque / Cajón
                                del Maipo</a></li>
                        <li><a href="/zonas/urbano/index.html"
                                class="font-medium text-brand-600 hover:underline text-xs mt-2 block">Ver
                                todas las zonas &rarr;</a></li>
                    </ul>
                </div>

                <div>
                    <h4 class="text-slate-900 font-bold mb-4 uppercase tracking-wider text-xs">Blog & Ayuda</h4>
                    <ul class="space-y-2">
                        <li><a href="/servicios/destape-alcantarillado.html#consejos"
                                class="hover:text-brand-600 transition">Consejos de Mantención</a></li>
                        <li><a href="/servicios/destape-alcantarillado.html#faq"
                                class="hover:text-brand-600 transition">Preguntas Frecuentes</a></li>
                        <li><a href="/servicios/destape-alcantarillado.html#trabaja"
                                class="hover:text-brand-600 transition">Trabaja con Nosotros</a></li>
                        <li><a href="/servicios/destape-alcantarillado.html#contacto"
                                class="hover:text-brand-600 transition">Contacto Administrativo</a></li>
                        <li><a href="/blog/index.html"
                                class="hover:text-brand-600 transition font-bold text-brand-600 mt-2 block">Blog de
                                Consejos &rarr;</a></li>
                    </ul>
                </div>

            </div>

            <div
                class="border-t border-slate-200 pt-8 text-center flex flex-col md:flex-row justify-between items-center pb-24 md:pb-0">
                <div class="flex flex-col items-center md:items-start gap-2">
                    <p>&copy; <span id="year"></span> destaperapido. Todos los derechos reservados.</p>
                    <p class="text-xs text-slate-500">Diseñado por <a href="https://www.paginasfast.cl/" target="_blank"
                            rel="noopener" class="hover:text-brand-600 transition">PaginasFast.cl</a></p>
                </div>
                <div class="flex gap-4 mt-4 md:mt-0">
                    <a href="/" class="hover:text-slate-800 transition" aria-label="Facebook"><i
                            class="fa-brands fa-facebook text-lg"></i></a>
                    <a href="/" class="hover:text-slate-800 transition" aria-label="Instagram"><i
                            class="fa-brands fa-instagram text-lg"></i></a>
                    <a href="/" class="hover:text-slate-800 transition" aria-label="LinkedIn"><i
                            class="fa-brands fa-linkedin text-lg"></i></a>
                </div>
            </div>
        </div>
    </footer>"""

def update_footers():
    root_dir = "public"
    # Regex to find footer. We assume <footer ...> ... </footer> logic.
    # Be careful with nested tags, but footer usually isn't nested inside another footer.
    # We'll use DOTALL to match across lines.
    footer_pattern = re.compile(r'<footer.*?</footer>', re.DOTALL)
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith(".html"):
                continue
                
            filepath = os.path.join(dirpath, filename)
            
            # Skip nosotros.html since it is the source (and already correct)
            # Actually, we can overwrite it too to be safe, but it has the extra section before.
            # The regex only replaces the <footer> block, not the section before.
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has a footer
            if '<footer' not in content:
                continue

            new_content = footer_pattern.sub(STANDARD_FOOTER, content)
            
            if new_content != content:
                print(f"Updating footer in {filepath}")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

if __name__ == "__main__":
    update_footers()
