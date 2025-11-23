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

    return nav_block, mobile_menu_block, footer_block

def update_files():
    nav_block, mobile_menu_block, footer_block = get_golden_blocks()
    
    # Walk through all files
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # Skip index.html (source of truth) but we might want to update it if we modify the blocks in code?
                # No, we use index.html as source.
                if file == 'index.html' and root == ROOT_DIR:
                    continue
                
                print(f"Updating {file_path}...")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Update Body Class
                # Add pb-30 md:pb-0 if not present
                if 'pb-30' not in content:
                    content = re.sub(r'<body\s+class="([^"]*)"', r'<body class="\1 pb-30 md:pb-0"', content)
                
                # 2. Replace Nav
                # Find existing nav
                content = re.sub(r'<nav\s+class="fixed w-full z-50.*?<\/nav>', nav_block, content, flags=re.DOTALL)
                
                # 3. Replace Mobile Menu Overlay
                # Find existing mobile menu. It might vary in other files.
                # We look for <div id="mobile-menu-overlay" ...
                # And replace until the next major tag.
                # To be safe, we can try to match the ID.
                if 'id="mobile-menu-overlay"' in content:
                     # Regex to replace from <div id="mobile-menu-overlay" to the closing div of the panel?
                     # This is risky with regex.
                     # Alternative: Identify the block by start string and end string?
                     # In most files, it's before <header> or <section>.
                     # Let's try to replace the whole block if we can identify it.
                     # If the file has the exact same structure, regex works.
                     # If not, we might need to be careful.
                     # Given the project structure, it's likely consistent.
                     content = re.sub(r'<div id="mobile-menu-overlay".*?<\/div>\s*<\/div>', mobile_menu_block, content, flags=re.DOTALL)
                else:
                    # If not found, insert it after nav?
                    # Usually it's after nav.
                    content = content.replace('</nav>', '</nav>\n\n' + mobile_menu_block)

                # 4. Replace Footer
                content = re.sub(r'<footer class="bg-slate-50.*?<\/footer>', footer_block, content, flags=re.DOTALL)
                
                # 5. Accessibility Fix for mantencion-preventiva.html
                if 'mantencion-preventiva.html' in file_path:
                    # Fix the invisible button text
                    # Look for text-prev-900 and replace with text-brand-600
                    content = content.replace('text-prev-900', 'text-brand-600')
                    # Also check for text-prev-700 just in case
                    content = content.replace('text-prev-700', 'text-brand-600')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

if __name__ == "__main__":
    update_files()
