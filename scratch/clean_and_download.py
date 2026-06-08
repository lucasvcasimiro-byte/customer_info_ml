import os
import json
import re
import urllib.request
import urllib.parse
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project"
PRODUCTS_JS = os.path.join(BASE_DIR, "dashboard", "src", "data", "storeProducts.js")
PUBLIC_IMG_DIR = os.path.join(BASE_DIR, "dashboard", "public", "product_images")
FINAL_JSON = os.path.join(BASE_DIR, "scratch", "final_products.json")

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
        # Use a safe User-Agent
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.continente.pt/'
            }
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            data = response.read()
            if len(data) > 1000:
                with open(filepath, 'wb') as f:
                    f.write(data)
                return len(data)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return 0

def parse_all_products():
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
        
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        match = re.search(r"id:\s*'([^']+)'", line)
        if match:
            prod_id = match.group(1)
            filename = downloaded_map.get(prod_id)
            
            if filename:
                # Remove existing image field if present
                line = re.sub(r"image:\s*(null|'[^']+'|`[^`]+`),?\s*", "", line)
                # Insert clean image path before price
                line = re.sub(
                    r"(price:\s*[\d.]+)",
                    f"image: '/product_images/{filename}', \\1",
                    line
                )
            else:
                # If no image was downloaded, set it to null or leave category default
                line = re.sub(r"image:\s*(null|'[^']+'|`[^`]+`),?\s*", "", line)
                line = re.sub(
                    r"(price:\s*[\d.]+)",
                    f"image: null, \\1",
                    line
                )
        new_lines.append(line)
        
    with open(PRODUCTS_JS, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
    print("Updated storeProducts.js with new image paths.")

def main():
    # 1. Clean public product_images directory completely
    print("Cleaning up old product images directory...")
    if os.path.exists(PUBLIC_IMG_DIR):
        shutil.rmtree(PUBLIC_IMG_DIR)
    os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
    
    # 2. Load verified products
    with open(FINAL_JSON, 'r', encoding='utf-8') as f:
        verified_products = json.load(f)
        
    verified_map = {item['product_name'].lower().strip(): item for item in verified_products}
    
    # 3. Parse products from storeProducts.js
    store_products = parse_all_products()
    print(f"Loaded {len(store_products)} products from storeProducts.js")
    
    # We will match store products to verified products by name or ID
    download_tasks = []
    for sp in store_products:
        sp_id = sp['id'].lower().strip()
        sp_name = sp['name'].lower().strip()
        
        # Try matching by ID first, then by name
        match = verified_map.get(sp_id) or verified_map.get(sp_name)
        
        if match:
            url = match['image_url']
            # Only download if the URL is clean (i.e. not containing any NSFW domains or suspicious ones)
            url_lower = url.lower()
            bad_domains = ['sex.com', 'xnxx.com', 'rule34', 'pictoa', 'older-mature', 'hoodamath.com']
            if any(bd in url_lower for bd in bad_domains):
                print(f"Skipping bad URL for {sp['name']}: {url}")
                continue
                
            download_tasks.append((sp['id'], url))
        else:
            print(f"No match in verified products for: {sp['name']}")
            
    # 4. Download images in parallel
    print(f"Downloading {len(download_tasks)} verified product images...")
    downloaded_map = {}
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {}
        for prod_id, url in download_tasks:
            cleaned = clean_id(prod_id)
            ext = get_extension(url)
            filename = f"product_{cleaned}{ext}"
            filepath = os.path.join(PUBLIC_IMG_DIR, filename)
            
            f = executor.submit(download_file, url, filepath)
            future_to_id[f] = (prod_id, filename)
            
        for future in as_completed(future_to_id):
            prod_id, filename = future_to_id[future]
            bytes_saved = future.result()
            if bytes_saved > 0:
                downloaded_map[prod_id] = filename
                
    print(f"Successfully downloaded {len(downloaded_map)} of {len(store_products)} images.")
    
    # 5. Update storeProducts.js
    update_products_js(downloaded_map)

if __name__ == "__main__":
    main()
