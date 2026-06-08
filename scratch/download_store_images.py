import urllib.request
import urllib.parse
import re
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Paths
BASE_DIR = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project"
PRODUCTS_JS = os.path.join(BASE_DIR, "dashboard", "src", "data", "storeProducts.js")
PUBLIC_IMG_DIR = os.path.join(BASE_DIR, "dashboard", "public", "product_images")

# Category search hints to get clean, professional product images
CATEGORY_HINTS = {
    'Vegetais': 'fresh vegetable',
    'Fruta': 'fresh fruit',
    'Padaria & Laticínios': 'dairy bread food product',
    'Carne & Peixe': 'raw meat fish grocery',
    'Bebidas': 'beverage drink bottle',
    'Cereais & Snacks': 'snack package box food',
    'Animais & Bebé': 'pet food baby food product',
    'Despensa': 'grocery product package brand',
    'Higiene': 'hygiene shampoo body product packaging',
    'Electrónica': 'electronic gadget device product white background',
    'Gaming': 'game box art cover'
}

def clean_id(prod_id):
    # replace spaces, hyphens, colons, ampersands, slashes with underscores
    cleaned = prod_id.lower()
    cleaned = re.sub(r'[\s\-:&/]+', '_', cleaned)
    cleaned = re.sub(r'_+', '_', cleaned)
    return cleaned.strip('_')

def get_extension(url):
    url_lower = url.lower().split('?')[0]
    for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg']:
        if url_lower.endswith(ext):
            return ext
    # Check if it contains the extension somewhere in path
    for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg']:
        if ext in url_lower:
            return ext
    return '.jpg'

def download_product_image(product):
    prod_id = product['id']
    name = product['name']
    category = product['category']
    cleaned = clean_id(prod_id)
    
    # Custom query construction
    hint = CATEGORY_HINTS.get(category, 'product')
    query = f"{name} {hint} product"
    if category == 'Gaming':
        query = f"{name} game cover art"
    
    print(f"[START] Searching image for: '{name}' (query: '{query}')...")
    
    try:
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8')
            
        matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        if not matches:
            matches = re.findall(r'"murl"\s*:\s*"([^"]+)"', html)
            
        if not matches:
            print(f"[WARN] No image matches found for '{name}'")
            return prod_id, None
            
        # Try downloading one of the first few matches
        for img_url in matches[:6]:
            # Avoid svg from bing tracker or strange domains
            if 'bing.com' in img_url or 'favicon' in img_url:
                continue
                
            ext = get_extension(img_url)
            filename = f"product_{cleaned}{ext}"
            filepath = os.path.join(PUBLIC_IMG_DIR, filename)
            
            try:
                # Add headers to avoid bot blocks
                img_req = urllib.request.Request(
                    img_url,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                with urllib.request.urlopen(img_req, timeout=5) as img_resp:
                    data = img_resp.read()
                    if len(data) > 1500: # Ensure it's not a tiny tracking pixel or redirect
                        with open(filepath, 'wb') as f:
                            f.write(data)
                        print(f"[SUCCESS] Downloaded '{name}' to {filename} ({len(data)} bytes)")
                        return prod_id, filename
            except Exception as e:
                # Silently try next URL
                pass
                
        print(f"[ERROR] All download attempts failed for '{name}'")
    except Exception as e:
        print(f"[ERROR] Exception searching for '{name}': {e}")
        
    return prod_id, None

def parse_products():
    products = []
    with open(PRODUCTS_JS, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Match the patterns: { id: '...', name: '...', category: '...', ... }
    pattern = r"\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*category:\s*'([^']+)'"
    matches = re.findall(pattern, content)
    for match in matches:
        products.append({
            'id': match[0],
            'name': match[1],
            'category': match[2]
        })
        
    print(f"Parsed {len(products)} products from storeProducts.js.")
    return products

def update_products_js(downloaded_map):
    with open(PRODUCTS_JS, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    updated_count = 0
    
    for line in lines:
        # Check if line contains a product definition
        match = re.search(r"id:\s*'([^']+)'", line)
        if match:
            prod_id = match.group(1)
            # If we successfully downloaded an image, append it
            filename = downloaded_map.get(prod_id)
            if filename:
                # Check if image field already exists
                if "image:" not in line:
                    # Insert image field before price or after price. Let's insert before price
                    # Replace: price:
                    # with:   image: '/product_images/...', price:
                    line = re.sub(
                        r"(price:\s*[\d.]+)",
                        f"image: '/product_images/{filename}', \\1",
                        line
                    )
                    updated_count += 1
            else:
                # Fallback to category default image if not downloaded
                if "image:" not in line:
                    line = re.sub(
                        r"(price:\s*[\d.]+)",
                        "image: null, \\1",
                        line
                    )
        new_lines.append(line)
        
    with open(PRODUCTS_JS, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print(f"Updated storeProducts.js with {updated_count} image paths.")

def main():
    os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
    
    products = parse_products()
    if not products:
        print("No products found to download. Exiting.")
        return
        
    print("Starting download pool...")
    downloaded_map = {}
    
    # Using 8 workers to not get rate-limited but download quickly
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_product_image, p): p for p in products}
        for future in as_completed(futures):
            prod_id, filename = future.result()
            if filename:
                downloaded_map[prod_id] = filename
                
    print(f"Downloaded {len(downloaded_map)} of {len(products)} product images.")
    
    # Update storeProducts.js with image filenames
    update_products_js(downloaded_map)

if __name__ == "__main__":
    main()
