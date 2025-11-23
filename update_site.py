import os
import re

# Define the root directory
ROOT_DIR = '/Users/alejandroriveracarrasco/proyectos-personales/destape-rapido/destaperapido/public'

# Define the "Golden" Nav and Mobile Menu from index.html (I'll reconstruct it based on what I saw to ensure it's perfect)
# I will read index.html first to get the exact strings to avoid typos.

def get_golden_blocks():
    with open(os.path.join(ROOT_DIR, 'index.html'), 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract Nav
    nav_match = re.search(r'(<nav\s+class="fixed w-full z-50.*?<\/nav>)', content, re.DOTALL)
    if not nav_match:
        raise Exception("Could not find <nav> in index.html")
    nav_block = nav_match.group(1)

    # Extract Mobile Menu Overlay
    # It starts with <div id="mobile-menu-overlay" and ends before the Header or next section.
    # In index.html, it's followed by <header class="hero-home...
    # I'll use a regex that matches the div and its content until the closing div.
    # Since regex for nested divs is hard, I'll look for the specific structure I saw.
    # It starts at line ~628 and ends at line ~736 in the view I saw.
    # It ends with </div> </div> (two closing divs, one for panel, one for overlay).
    
    # Let's try to capture it by ID and assume it ends before <header or <main or <section
    mobile_menu_match = re.search(r'(<div id="mobile-menu-overlay".*?<\/div>\s*<\/div>)', content, re.DOTALL)
    if not mobile_menu_match:
        # Try a broader match if the specific closing tags are hard to predict
        # It seems to be followed by <header
        mobile_menu_match = re.search(r'(<div id="mobile-menu-overlay".*?)(?=<header|<section|<main)', content, re.DOTALL)
    
    if not mobile_menu_match:
        raise Exception("Could not find mobile-menu-overlay in index.html")
    mobile_menu_block = mobile_menu_match.group(1).strip()

    # Extract Footer
    footer_match = re.search(r'(<footer class="bg-slate-50.*?<\/footer>)', content, re.DOTALL)
    if not footer_match:
        raise Exception("Could not find <footer> in index.html")
    footer_block = footer_match.group(1)

    # Extract Mobile Sticky Footer
    mobile_footer_match = re.search(r'(<!-- Mobile Sticky Footer -->.*?<!-- End Mobile Sticky Footer -->)', content, re.DOTALL)
    if not mobile_footer_match:
        # Fallback if comments are missing (shouldn't happen as I just added them)
        # Try to match by class if comments fail?
        # For now, let's assume comments are there.
        # If not, we might need to rely on the previous regex approach or skip.
        # But since I edited index.html, it should be there.
        print("Warning: Could not find Mobile Sticky Footer comments in index.html")
        mobile_footer_block = ""
    else:
        mobile_footer_block = mobile_footer_match.group(1)

    return nav_block, mobile_menu_block, footer_block, mobile_footer_block

def update_files():
    nav_block, mobile_menu_block, footer_block, mobile_footer_block = get_golden_blocks()
    
    # Walk through all files
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # Skip index.html (source of truth)
                if file == 'index.html' and root == ROOT_DIR:
                    continue
                
                print(f"Updating {file_path}...")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Update Body Class
                if 'pb-30' not in content:
                    content = re.sub(r'<body\s+class="([^"]*)"', r'<body class="\1 pb-30 md:pb-0"', content)
                
                # Check if it's a landing page
                is_landing_page = '/landing/' in file_path or '\\landing\\' in file_path

                if not is_landing_page:
                    # 2. Replace Nav
                    content = re.sub(r'<nav\s+class="fixed w-full z-50.*?<\/nav>', nav_block, content, flags=re.DOTALL)
                    
                    # 3. Replace Mobile Menu Overlay
                    if 'id="mobile-menu-overlay"' in content:
                         content = re.sub(r'<div id="mobile-menu-overlay".*?<\/div>\s*<\/div>', mobile_menu_block, content, flags=re.DOTALL)
                    else:
                        content = content.replace('</nav>', '</nav>\n\n' + mobile_menu_block)

                    # 4. Replace Footer
                    content = re.sub(r'<footer class="bg-slate-50.*?<\/footer>', footer_block, content, flags=re.DOTALL)

                    # 5. Replace/Insert Mobile Sticky Footer
                    if '<!-- Mobile Sticky Footer -->' in content:
                        content = re.sub(r'<!-- Mobile Sticky Footer -->.*?<!-- End Mobile Sticky Footer -->', mobile_footer_block, content, flags=re.DOTALL)
                    else:
                        # If not found, check if there is an old version without comments
                        # The old version starts with <div class="fixed bottom-0... and ends with </div>...
                        # It's risky to regex replace without markers.
                        # Safe bet: Insert it after </footer> if </footer> exists.
                        if '</footer>' in content:
                            content = content.replace('</footer>', '</footer>\n\n' + mobile_footer_block)
                        else:
                            # If no footer, insert before body end
                            content = content.replace('</body>', mobile_footer_block + '\n</body>')

                # 6. Accessibility Fix for mantencion-preventiva.html
                if 'mantencion-preventiva.html' in file_path:
                    content = content.replace('text-prev-900', 'text-brand-600')
                    content = content.replace('text-prev-700', 'text-brand-600')

                # 7. Performance Optimizations
                if '<link rel="preconnect" href="https://www.transparenttextures.com">' not in content:
                    content = content.replace('<head>', '<head>\n    <link rel="preconnect" href="https://www.transparenttextures.com">')
                
                if 'display=swap' not in content and 'fonts.googleapis.com' in content:
                    content = re.sub(
                        r'(<link[^>]*?href="https://fonts\.googleapis\.com/css2\?family=Plus\+Jakarta\+Sans:wght@400;500;600;700;800)(&[^"]*)?"([^>]*?)>',
                        r'<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"\3>',
                        content,
                        flags=re.IGNORECASE
                    )

                content = content.replace('src="/favicon.png"', 'src="/logo-nav.png"')

                csp_meta = '<meta http-equiv="Content-Security-Policy" content="default-src \'self\' https:; script-src \'self\' \'unsafe-inline\' https:; style-src \'self\' \'unsafe-inline\' https:; img-src \'self\' data: https:; font-src \'self\' https: data:;">'
                if 'Content-Security-Policy' not in content:
                    content = content.replace('<head>', f'<head>\n    {csp_meta}')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

if __name__ == "__main__":
    update_files()
