import urllib.request
import urllib.parse
import json
import re
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Paths
BASE_DIR = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project"
PRODUCTS_JS = os.path.join(BASE_DIR, "dashboard", "src", "data", "storeProducts.js")
PUBLIC_IMG_DIR = os.path.join(BASE_DIR, "dashboard", "public", "product_images")

# Category-specific search queries for Wikimedia Commons
WIKI_SEARCH_HINTS = {
    'Vegetais': ['{name} vegetable', '{name} plant', '{name}'],
    'Fruta': ['{name} fruit', '{name} berry', '{name}'],
    'Padaria & Laticínios': ['{name} cheese', '{name} bread', '{name} dairy', '{name}'],
    'Carne & Peixe': ['{name} meat', '{name} fish', '{name} raw', '{name}'],
    'Bebidas': ['{name} bottle', '{name} drink', '{name} beverage', '{name}'],
    'Cereais & Snacks': ['{name} box', '{name} snack', '{name} package', '{name}'],
    'Animais & Bebé': ['{name} pet food', '{name} baby food', '{name}'],
    'Despensa': ['{name} food', '{name} package', '{name}'],
    'Higiene': ['{name} shampoo', '{name} soap', '{name} product', '{name}'],
    'Electrónica': ['{name} product', '{name} device', '{name}'],
    'Gaming': ['{name} game cover', '{name} box art', '{name} game']
}

# Bing fallback queries if Wikimedia fails
BING_QUERIES = {
    'Gaming': ['{name} game cover art', '{name} box art', '{name} switch game cover'],
    'Electrónica': ['{name} product white background', '{name} official product photo'],
    'Higiene': ['{name} packaging product', '{name} item photo'],
    'Bebidas': ['{name} bottle product photo', '{name} can product'],
    'Cereais & Snacks': ['{name} package product', '{name} box'],
    'Animais & Bebé': ['{name} package product', '{name} food brand'],
    'Despensa': ['{name} package grocery', '{name} bottle product'],
    'Carne & Peixe': ['{name} raw meat grocery', '{name} food photo'],
    'Padaria & Laticínios': ['{name} product food', '{name} loaf'],
    'Fruta': ['{name} fresh fruit', '{name} raw fruit'],
    'Vegetais': ['{name} vegetable raw', '{name} fresh vegetable']
}

def clean_id(prod_id):
    cleaned = prod_id.lower()
    cleaned = re.sub(r'[\s\-:&/]+', '_', cleaned)
    cleaned = re.sub(r'_+', '_', cleaned)
    return cleaned.strip('_')

def get_extension(url):
    url_lower = url.lower().split('?')[0]
    for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg']:
        if url_lower.endswith(ext):
            return ext
    for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg']:
        if ext in url_lower:
            return ext
    return '.jpg'

def download_file(url, filepath):
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = response.read()
            if len(data) > 1500: # avoid tiny pixel trackers
                with open(filepath, 'wb') as f:
                    f.write(data)
                return len(data)
    except Exception as e:
        pass
    return 0

def try_wikimedia(name, category):
    hints = WIKI_SEARCH_HINTS.get(category, ['{name}'])
    for hint in hints:
        query = hint.replace('{name}', name)
        try:
            query_encoded = urllib.parse.quote(query)
            api_url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrsearch={query_encoded}&gsrnamespace=6&gsrlimit=8&prop=imageinfo&iiprop=url"
            
            req = urllib.request.Request(
                api_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) NOVAIMSGroceryStore/1.0'}
            )
            with urllib.request.urlopen(req, timeout=6) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_info in pages.items():
                imageinfo = page_info.get('imageinfo', [])
                if imageinfo:
                    img_url = imageinfo[0].get('url')
                    # Filter out diagrams, maps, icons, coats of arms, flags unless the item is a diagram
                    img_url_lower = img_url.lower()
                    if any(term in img_url_lower for term in ['diagram', 'map', 'coat_of_arms', 'flag', 'logo', 'anatomy', 'uterus', 'vagina', 'cartoon', 'illustration']):
                        # Skip unless category is Gaming or Electrónica where logos/illustrations are okay
                        if category not in ['Gaming', 'Electrónica']:
                            continue
                    return img_url
        except Exception as e:
            pass
    return None

def try_bing(name, category):
    hints = BING_QUERIES.get(category, ['{name} product'])
    for hint in hints:
        query = hint.replace('{name}', name)
        try:
            url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            )
            with urllib.request.urlopen(req, timeout=6) as response:
                html = response.read().decode('utf-8')
                
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            if not matches:
                matches = re.findall(r'"murl"\s*:\s*"([^"]+)"', html)
                
            for img_url in matches[:10]:
                if 'bing.com' in img_url or 'favicon' in img_url:
                    continue
                # Filter out obvious anatomical or diagram domains if food item
                img_url_lower = img_url.lower()
                if category not in ['Gaming', 'Electrónica']:
                    if any(term in img_url_lower for term in ['diagram', 'anatomy', 'medical', 'illustration', 'clipart', 'vector']):
                        continue
                return img_url
        except Exception as e:
            pass
    return None

def download_product_image(product):
    prod_id = product['id']
    name = product['name']
    category = product['category']
    cleaned = clean_id(prod_id)
    
    # Standard output target
    # We will try Wikimedia Commons first, then fallback to Bing Images
    print(f"[START] Processing: '{name}' ({category})...")
    
    img_url = None
    # For Gaming, go straight to Bing because box arts are rarely on Wikimedia Commons
    if category == 'Gaming':
        img_url = try_bing(name, category)
        if not img_url:
            img_url = try_wikimedia(name, category)
    else:
        img_url = try_wikimedia(name, category)
        if not img_url:
            img_url = try_bing(name, category)
            
    if img_url:
        ext = get_extension(img_url)
        filename = f"product_{cleaned}{ext}"
        filepath = os.path.join(PUBLIC_IMG_DIR, filename)
        
        bytes_saved = download_file(img_url, filepath)
        if bytes_saved > 0:
            print(f"[SUCCESS] '{name}' -> {filename} ({bytes_saved} bytes) from {img_url}")
            return prod_id, filename
        else:
            # Try second option in case download failed
            fallback_url = try_bing(name, category) if category != 'Gaming' else try_wikimedia(name, category)
            if fallback_url and fallback_url != img_url:
                ext = get_extension(fallback_url)
                filename = f"product_{cleaned}{ext}"
                filepath = os.path.join(PUBLIC_IMG_DIR, filename)
                bytes_saved = download_file(fallback_url, filepath)
                if bytes_saved > 0:
                    print(f"[SUCCESS-FALLBACK] '{name}' -> {filename} ({bytes_saved} bytes) from {fallback_url}")
                    return prod_id, filename
                    
    print(f"[FAILED] Could not download image for '{name}'")
    return prod_id, None

def parse_products():
    products = []
    with open(PRODUCTS_JS, 'r', encoding='utf-8') as f:
        content = f.read()
        
    pattern = r"\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*category:\s*'([^']+)'"
    matches = re.findall(pattern, content)
    for match in matches:
        products.append({
            'id': match[0],
            'name': match[1],
            'category': match[2]
        })
    return products

def update_products_js(downloaded_map):
    with open(PRODUCTS_JS, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We want to clear out any old image paths and write new ones
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        match = re.search(r"id:\s*'([^']+)'", line)
        if match:
            prod_id = match.group(1)
            filename = downloaded_map.get(prod_id)
            
            # Remove existing image field if present
            line = re.sub(r"image:\s*(null|'[^']+'|`[^`]+`),?\s*", "", line)
            
            if filename:
                # Insert clean image path before price
                line = re.sub(
                    r"(price:\s*[\d.]+)",
                    f"image: '/product_images/{filename}', \\1",
                    line
                )
            else:
                line = re.sub(
                    r"(price:\s*[\d.]+)",
                    "image: null, \\1",
                    line
                )
        new_lines.append(line)
        
    with open(PRODUCTS_JS, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
    print("Updated storeProducts.js with clean image paths.")

def main():
    os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
    products = parse_products()
    
    print(f"Starting clean download for {len(products)} products...")
    downloaded_map = {}
    
    # 10 workers for rapid concurrent processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(download_product_image, p): p for p in products}
        for future in as_completed(futures):
            prod_id, filename = future.result()
            if filename:
                downloaded_map[prod_id] = filename
                
    print(f"Clean download summary: {len(downloaded_map)} of {len(products)} images downloaded.")
    update_products_js(downloaded_map)

if __name__ == "__main__":
    main()
