import urllib.request
import urllib.parse
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Paths
BASE_DIR = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project"
PRODUCTS_JS = os.path.join(BASE_DIR, "dashboard", "src", "data", "storeProducts.js")
PUBLIC_IMG_DIR = os.path.join(BASE_DIR, "dashboard", "public", "product_images")

# Whitelist domains of official retail stores and CDNs
WHITELIST_DOMAINS = [
    'continente.pt', 'produtos.continente.pt', 'auchan.pt', 'pingo-doce.pt', 
    'elcorteingles.pt', 'elcorteingles.es', 'auchan.fr', 'intermarche.pt',
    'openfoodfacts.org', 'wikimedia.org', 'wikipedia.org',
    'amazon.com', 'media-amazon.com', 'images-amazon.com', 'ssl-images-amazon.com',
    'walmart.com', 'walmartimages.com', 'target.com', 'scene7.com',
    'steamstatic.com', 'nintendo.com', 'playstation.com', 'xbox.com'
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

def is_whitelisted(url):
    url_lower = url.lower()
    return any(domain in url_lower for domain in WHITELIST_DOMAINS)

def download_file(url, filepath):
    if not is_whitelisted(url):
        return 0
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.continente.pt/'
            }
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            data = response.read()
            if len(data) > 1500:
                with open(filepath, 'wb') as f:
                    f.write(data)
                return len(data)
    except Exception as e:
        pass
    return 0

def fetch_bing_candidate_urls(name, category):
    urls = []
    
    # Constructing queries that force supermarket/retailer context
    queries = []
    
    pt_name = PORTUGUESE_KEYWORDS.get(name.lower(), name.lower())
    
    if category in ['Vegetais', 'Fruta', 'Padaria & Laticínios', 'Carne & Peixe', 'Despensa', 'Bebidas', 'Cereais & Snacks']:
        # Force Portuguese retail search terms
        queries.append(f"site:continente.pt {pt_name}")
        queries.append(f"site:produtos.continente.pt {pt_name}")
        queries.append(f"site:elcorteingles.pt {pt_name}")
        queries.append(f"site:openfoodfacts.org {name}")
        queries.append(f"{pt_name} produto continente")
        queries.append(f"{name} amazon product pack")
    elif category == 'Gaming':
        # Force game covers
        queries.append(f"site:steamstatic.com {name} header")
        queries.append(f"site:nintendo.com {name} box art")
        queries.append(f"site:amazon.com {name} game cover")
        queries.append(f"site:en.wikipedia.org {name} game")
    elif category == 'Electrónica':
        queries.append(f"site:target.com {name} product")
        queries.append(f"site:amazon.com {name} official")
        queries.append(f"site:en.wikipedia.org {name}")
    else:
        queries.append(f"{name} site:continente.pt")
        queries.append(f"{name} site:amazon.com")
        
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
                
            for img_url in matches[:25]:
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
    
    print(f"[RETAIL-SCRAPE-START] Processing: '{name}' ({category})...")
    
    candidate_urls = fetch_bing_candidate_urls(name, category)
    
    # Scan through matched URLs. ONLY download if they are whitelisted.
    for img_url in candidate_urls:
        if is_whitelisted(img_url):
            ext = get_extension(img_url)
            filename = f"product_{cleaned}{ext}"
            filepath = os.path.join(PUBLIC_IMG_DIR, filename)
            
            bytes_saved = download_file(img_url, filepath)
            if bytes_saved > 0:
                print(f"[RETAIL-SUCCESS] '{name}' ({category}) -> {filename} ({bytes_saved} bytes) from {img_url}")
                return prod_id, filename
                
    # If no whitelisted URL was found/downloaded
    print(f"[RETAIL-FAILED] No official whitelisted retail image for '{name}'. Using Vite category default.")
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
        
    print("Updated storeProducts.js with official whitelisted retail image paths.")

def main():
    os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
    products = parse_products()
    
    print(f"Scraping official retail product photos for {len(products)} products...")
    downloaded_map = {}
    
    # 8 workers for fast parallel processing
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_product, p): p for p in products}
        for future in as_completed(futures):
            prod_id, filename = future.result()
            if filename:
                downloaded_map[prod_id] = filename
                
    print(f"Scraped {len(downloaded_map)} of {len(products)} official retail images.")
    update_products_js(downloaded_map)

if __name__ == "__main__":
    main()
