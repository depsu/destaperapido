
import os
import re

def process_content(content):
    # Regex to find href attributes that are NOT absolute URLs (http/https) and end with .html
    # We look for href=" or href='
    # Capture group 1: quote style (" or ')
    # Capture group 2: the path
    # Negative lookahead for http: or https:
    
    pattern = r'href=(["\'])(?!https?:|#|mailto:)([^"\'>]+)\.html\1'
    
    def replacer(match):
        quote = match.group(1)
        path = match.group(2) # e.g. /servicios/destape-alcantarillado or index
        
        # Handle index.html cases
        if path.endswith('/index'):
            new_path = path[:-5] # remove 'index', leave trailing slash: /servicios/
        elif path == 'index':
            new_path = './' # relative home? or just '.'
        else:
            new_path = path
            
        return f'href={quote}{new_path}{quote}'

    return re.sub(pattern, replacer, content)

def main():
    base_dir = '/Users/alejandroriveracarrasco/proyectos-personales/destaperapido/public'
    modified_count = 0
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                new_content = process_content(original_content)
                
                if new_content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {filepath}")
                    modified_count += 1
    
    print(f"Total files updated: {modified_count}")

if __name__ == '__main__':
    main()
