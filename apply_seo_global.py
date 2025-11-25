import os
import re

ROOT_DIR = '/Users/alejandroriveracarrasco/proyectos-personales/destape-rapido/destaperapido/public'
BASE_URL = 'https://www.destaperapido.cl'
PHONE_DISPLAY = '+56 9 3647 0112'
PHONE_HREF = '+56936470112'

def get_canonical_url(file_path):
    rel_path = os.path.relpath(file_path, ROOT_DIR)
    if rel_path == 'index.html':
        return BASE_URL + '/'
    
    # Remove .html
    url_path = rel_path.replace('.html', '')
    # Remove index if it's a directory index
    if url_path.endswith('/index'):
        url_path = url_path[:-6] # remove /index
    elif url_path == 'index':
        url_path = ''
        
    return f"{BASE_URL}/{url_path}"

def apply_seo(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Canonical Tag
    canonical_url = get_canonical_url(file_path)
    canonical_tag = f'<link rel="canonical" href="{canonical_url}">'
    
    if '<link rel="canonical"' not in content:
        # Insert after <head> or before </head>
        # Let's put it after <meta charset> or viewport to be safe, or just before </head>
        # User suggested: <link rel="canonical" ...>
        # I'll put it before <link rel="stylesheet" href="/output.css"> which seems common
        if '<link rel="stylesheet" href="/output.css">' in content:
             content = content.replace('<link rel="stylesheet" href="/output.css">', f'{canonical_tag}\n    <link rel="stylesheet" href="/output.css">')
        else:
             content = content.replace('</head>', f'    {canonical_tag}\n</head>')
    
    # 2. Phone Number Standardization
    # Replace dummy numbers
    content = content.replace('+56 9 1234 5678', PHONE_DISPLAY)
    content = content.replace('+56 9 6588 9226', PHONE_DISPLAY)
    # Ensure hrefs are correct
    # This regex finds tel: links and updates the number
    content = re.sub(r'href="tel:\+56\s?9\s?\d{4}\s?\d{4}"', f'href="tel:{PHONE_HREF}"', content)
    
    # 3. Ñuñoa Fix in Links
    content = content.replace('ñuñoa.html', 'nunoa.html')
    content = content.replace('n%CC%83un%CC%83oa.html', 'nunoa.html')
    content = content.replace('/zonas/urbano/nunoa.html', '/zonas/urbano/nunoa.html')
    
    # 4. Alt Text for Carbon Fibre
    content = re.sub(r'(src="[^"]*carbon-fibre\.png")(?![^>]*alt=)', r'\1 alt=""', content)
    
    # 5. Brand in Title
    # If "Alcantarillados Pro" is in title, replace with "Destape Rápido"
    content = content.replace('<title>Alcantarillados Pro', '<title>Destape Rápido')
    
    # If title doesn't have "Destape Rápido", append it
    # We need to be careful not to double it
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        title_text = title_match.group(1)
        if 'Destape Rápido' not in title_text:
            new_title = f"{title_text} | Destape Rápido"
            content = content.replace(f'<title>{title_text}</title>', f'<title>{new_title}</title>')

    # 6. Open Graph Tags (Generic Fallback)
    # Only add if not present
    if '<meta property="og:title"' not in content:
        # Generate generic OG based on title/desc
        title_match = re.search(r'<title>(.*?)</title>', content)
        desc_match = re.search(r'<meta name="description"\s+content="(.*?)">', content)
        
        og_title = title_match.group(1) if title_match else "Destape Rápido"
        og_desc = desc_match.group(1) if desc_match else "Servicio de destape de alcantarillado y limpieza de fosas."
        
        og_tags = f'''
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_desc}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:image" content="{BASE_URL}/images/hero_home.webp">
    <meta name="twitter:card" content="summary_large_image">'''
        
        content = content.replace('</head>', f'{og_tags}\n</head>')

    if content != original_content:
        print(f"Updating {file_path}...")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith('.html'):
                apply_seo(os.path.join(root, file))

if __name__ == '__main__':
    main()
