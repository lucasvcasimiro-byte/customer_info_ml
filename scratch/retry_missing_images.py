import urllib.request
import urllib.parse
import re
import os
import sys

# Paths
BASE_DIR = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project"
PRODUCTS_JS = os.path.join(BASE_DIR, "dashboard", "src", "data", "storeProducts.js")
PUBLIC_IMG_DIR = os.path.join(BASE_DIR, "dashboard", "public", "product_images")

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

def download_image_retry(prod_id, name, category):
    cleaned = clean_id(prod_id)
    
    # Try different query options
    queries = [
        f"{name} photo",
        f"{name} product",
        f"{name} {category}",
        name
    ]
    if category == 'Gaming':
        queries = [
            f"{name} game cover",
            f"{name} box art",
            f"{name} game"
        ]
        
    for query in queries:
        print(f"  Trying query: '{query}'")
        try:
            url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
                
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            if not matches:
                matches = re.findall(r'"murl"\s*:\s*"([^"]+)"', html)
                
            if not matches:
                continue
                
            # Try up to 10 URLs
            for img_url in matches[:10]:
                if 'bing.com' in img_url or 'favicon' in img_url:
                    continue
                    
                ext = get_extension(img_url)
                filename = f"product_{cleaned}{ext}"
                filepath = os.path.join(PUBLIC_IMG_DIR, filename)
                
                try:
                    img_req = urllib.request.Request(
                        img_url,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    )
                    with urllib.request.urlopen(img_req, timeout=8) as img_resp:
                        data = img_resp.read()
                        if len(data) > 1000:
                            with open(filepath, 'wb') as f:
                                f.write(data)
                            print(f"  [SUCCESS] Downloaded '{name}' to {filename} ({len(data)} bytes) from {img_url}")
                            return filename
                except Exception as e:
                    # try next url
                    pass
        except Exception as e:
            print(f"  Error searching for '{query}': {e}")
            
    print(f"  [FAILED] Could not download image for '{name}'")
    return None

def check_missing_and_retry():
    with open(PRODUCTS_JS, 'r', encoding='utf-8') as f:
        content = f.read()
        
    missing = []
    lines = content.split('\n')
    for line in lines:
        if 'id:' in line:
            id_match = re.search(r"id:\s*'([^']+)'", line)
            name_match = re.search(r"name:\s*'([^']+)'", line)
            cat_match = re.search(r"category:\s*'([^']+)'", line)
            img_match = re.search(r"image:\s*(null|'[^']+')", line)
            
            if id_match and name_match and cat_match:
                prod_id = id_match.group(1)
                name = name_match.group(1)
                cat = cat_match.group(1)
                img = img_match.group(1) if img_match else None
                
                if not img or img == 'null':
                    missing.append({'id': prod_id, 'name': name, 'category': cat})
                    
    print(f"Found {len(missing)} missing images. Retrying now...")
    
    downloaded_map = {}
    for m in missing:
        print(f"Retrying: {m['name']} ({m['id']})...")
        filename = download_image_retry(m['id'], m['name'], m['category'])
        if filename:
            downloaded_map[m['id']] = filename
            
    if downloaded_map:
        # Read lines and replace
        with open(PRODUCTS_JS, 'r', encoding='utf-8') as f:
            js_lines = f.readlines()
            
        new_lines = []
        updated_count = 0
        
        for line in js_lines:
            match = re.search(r"id:\s*'([^']+)'", line)
            if match:
                prod_id = match.group(1)
                filename = downloaded_map.get(prod_id)
                if filename:
                    # replace the image field (or price if image field was null)
                    if "image: null" in line:
                        line = line.replace("image: null", f"image: '/product_images/{filename}'")
                        updated_count += 1
                    elif "image:" not in line:
                        line = re.sub(
                            r"(price:\s*[\d.]+)",
                            f"image: '/product_images/{filename}', \\1",
                            line
                        )
                        updated_count += 1
            new_lines.append(line)
            
        with open(PRODUCTS_JS, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
        print(f"Updated storeProducts.js with {updated_count} retried images.")
    else:
        print("No new images were downloaded.")

if __name__ == "__main__":
    check_missing_and_retry()
