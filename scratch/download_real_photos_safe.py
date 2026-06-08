import urllib.request
import urllib.parse
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Paths
BASE_DIR = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project"
PRODUCTS_JS = os.path.join(BASE_DIR, "dashboard", "src", "data", "storeProducts.js")
PUBLIC_IMG_DIR = os.path.join(BASE_DIR, "dashboard", "public", "product_images")

# Blacklist of domains to block adult content, stock watermarks, and diagrams
BLACKLIST_DOMAINS = [
    'eporner.com', 'met-art.com', 'pixhost.to', 'erome.com', 'babehub.com', 
    'playboy.com', 'hawtcelebs.com', 'livemaster.ru', 'livemaster.co.uk',
    'tumblr.com', 'deviantart.com', 'fanpop.com', 'pinterest.com', 'pinimg.com',
    'shutterstock.com', 'dreamstime.com', 'istockphoto.com', 'gettyimages.com',
    'depositphotos.com', '123rf.com', 'alamy.com', 'alamy.es', 'vectorstock.com',
    'hoodamath.com', 'unblockedgames', 'datosnutricional.com', 'wikihow.com',
    'healthline.com', 'webmd.com', 'medicalnewstoday.com', 'anatomy', 'uterus', 'vagina'
]

# Blacklist keywords in URL to avoid diagrams, drawings, etc.
BLACKLIST_KEYWORDS = [
    'diagram', 'anatomy', 'medical', 'map', 'flag', 'cartoon', 'illustration', 
    'clipart', 'vector', 'drawing', 'sketch', 'logo', 'icon', 'silhouette',
    'coloring', 'raskrasil', 'coloring-page', 'obstructive-sleep-apnoea', 'spider-bites'
]

# Simple mapping of product names to Portuguese keywords for Continente/supermarket searches
PORTUGUESE_KEYWORDS = {
    'asparagus': 'espargos',
    'spinach': 'espinafres',
    'tomatoes': 'tomate',
    'carrots': 'cenoura',
    'green beans': 'feijao verde',
    'salad': 'salada',
    'zucchini': 'curgete',
    'eggplant': 'berinjela',
    'pepper': 'pimento',
    'cauliflower': 'couve flor',
    'corn': 'milho doce',
    'shallot': 'chalota',
    'yams': 'inhame',
    'mint': 'hortela',
    'strawberries': 'morangos',
    'blueberries': 'mirtilos',
    'bramble': 'amoras',
    'melons': 'melao',
    'green grapes': 'uvas verdes',
    'chicken': 'frango',
    'ground beef': 'carne picada',
    'salmon': 'salmao',
    'seabass': 'robalo',
    'shrimp': 'camarao',
    'catfish': 'peixe gato',
    'trout': 'truta',
    'turkey': 'peru',
    'bacon': 'bacon fatias',
    'ham': 'fiambre',
    'meatballs': 'almondegas',
    'escalope': 'escalope',
    'fresh tuna': 'atum fresco',
    'burgers': 'hamburguer',
    'hot dogs': 'salsichas hot dog',
    'cider': 'sidra',
    'energy drink': 'bebida energetica',
    'gums': 'gomas',
    'tomato sauce': 'polpa tomate',
    'ketchup': 'ketchup',
    'pickles': 'pickles jar',
    'soup': 'sopa legumes',
    'mashed potato': 'pure batata',
    'french fries': 'batatas fritas conheladas',
    'toilet paper': 'papel higienico',
    'napkins': 'guardanapos',
    'cologne': 'agua de colonia',
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

def is_safe_url(url):
    url_lower = url.lower()
    # Check blacklist domains
    if any(domain in url_lower for domain in BLACKLIST_DOMAINS):
        return False
    # Check blacklist keywords
    if any(kw in url_lower for kw in BLACKLIST_KEYWORDS):
        return False
    return True

def download_file(url, filepath):
    if not is_safe_url(url):
        return 0
    try:
        # Standard browser headers with NO referrer to avoid cross-origin block
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            if len(data) > 2000:  # Must be larger than 2KB to ensure it's a real photo
                with open(filepath, 'wb') as f:
                    f.write(data)
                return len(data)
    except Exception as e:
        pass
    return 0

def fetch_bing_candidate_urls(name, category):
    urls = []
    
    # Category search term refinement
    queries = []
    pt_name = PORTUGUESE_KEYWORDS.get(name.lower(), name.lower())
    
    if category in ['Vegetais', 'Fruta', 'Padaria & Laticínios', 'Carne & Peixe', 'Despensa', 'Bebidas', 'Cereais & Snacks']:
        # Prefer Continente search or general supermarket product photos
        queries.append(f"{pt_name} continente")
        queries.append(f"{pt_name} supermercado produto")
        queries.append(f"{name} supermarket product packaging")
    elif category == 'Gaming':
        queries.append(f"{name} game cover art")
        queries.append(f"{name} switch game cover")
    elif category == 'Electrónica':
        queries.append(f"{name} official product photo white background")
        queries.append(f"{name} amazon product")
    else:
        queries.append(f"{name} product packaging")
        
    for query in queries:
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
                
            for img_url in matches[:30]:
                if 'bing.com' in img_url or 'favicon' in img_url:
                    continue
                urls.append(img_url)
        except Exception as e:
            pass
            
    return urls

def process_product(product):
    prod_id = product['id']
    name = product['name']
    category = product['category']
    cleaned = clean_id(prod_id)
    
    print(f"[SAFE-SCRAPE-START] Processing: '{name}' ({category})...")
    
    candidate_urls = fetch_bing_candidate_urls(name, category)
    
    # Iterate and download first safe matching URL
    for img_url in candidate_urls:
        if is_safe_url(img_url):
            ext = get_extension(img_url)
            filename = f"product_{cleaned}{ext}"
            filepath = os.path.join(PUBLIC_IMG_DIR, filename)
            
            bytes_saved = download_file(img_url, filepath)
            if bytes_saved > 0:
                print(f"[SAFE-SUCCESS] '{name}' -> {filename} ({bytes_saved} bytes) from {img_url}")
                return prod_id, filename
                
    print(f"[SAFE-FAILED] Could not download any safe photo for '{name}'. Using Vite category default.")
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
        
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        match = re.search(r"id:\s*'([^']+)'", line)
        if match:
            prod_id = match.group(1)
            filename = downloaded_map.get(prod_id)
            
            # Reset existing image attribute
            line = re.sub(r"image:\s*(null|'[^']+'|`[^`]+`),?\s*", "", line)
            
            if filename:
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
        
    print("Updated storeProducts.js with safe web scraped image paths.")

def main():
    os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
    products = parse_products()
    
    print(f"Scraping safe real product photos for {len(products)} products...")
    downloaded_map = {}
    
    # 8 workers for parallel downloads
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_product, p): p for p in products}
        for future in as_completed(futures):
            prod_id, filename = future.result()
            if filename:
                downloaded_map[prod_id] = filename
                
    print(f"Safe scraping completed. {len(downloaded_map)} of {len(products)} images downloaded.")
    update_products_js(downloaded_map)

if __name__ == "__main__":
    main()
