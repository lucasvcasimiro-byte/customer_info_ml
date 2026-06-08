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

# Whitelist of domain substrings to filter official product photos
WHITELIST_DOMAINS = [
    'continente.pt', 'produtos.continente.pt', 'auchan.pt', 'pingo-doce.pt', 
    'elcorteingles.pt', 'elcorteingles.es', 'mendozaselect.pt', 'auchan.fr',
    'openfoodfacts.org', 'wikimedia.org', 'wikipedia.org',
    'amazon.com', 'media-amazon.com', 'images-amazon.com', 'ssl-images-amazon.com',
    'walmart.com', 'walmartimages.com', 'target.com', 'scene7.com',
    'steamstatic.com', 'nintendo.com', 'playstation.com', 'xbox.com'
]

# Explicit mapping for games and electronics to exact English Wikipedia article titles
WIKI_TITLE_MAPPING = {
    # Gaming
    'minecraft': 'Minecraft',
    'portal': 'Portal (video game)',
    'portal 2': 'Portal 2',
    'half-life 2': 'Half-Life 2',
    'half-life: alyx': 'Half-Life: Alyx',
    'pokemon scarlet': 'Pokémon Scarlet and Violet',
    'pokemon violet': 'Pokémon Scarlet and Violet',
    'pokemon sword': 'Pokémon Sword and Shield',
    'pokemon shield': 'Pokémon Sword and Shield',
    'final fantasy xix': 'Final Fantasy VII Remake',
    'final fantasy xx': 'Final Fantasy XV',
    'final fantasy xxii': 'Final Fantasy XVI',
    'megaman zero': 'Mega Man Zero (video game)',
    'megaman zero 2': 'Mega Man Zero 2',
    'megaman zero 3': 'Mega Man Zero 3',
    'megaman zero 4': 'Mega Man Zero 4',
    'metroid fusion': 'Metroid Fusion',
    'metroid prime': 'Metroid Prime',
    'ratchet & clank': 'Ratchet & Clank (2002 video game)',
    'ratchet & clank 2': 'Ratchet & Clank: Going Commando',
    'ratchet & clank 3': 'Ratchet & Clank: Up Your Arsenal',
    
    # Electronics
    'airpods': 'AirPods',
    'bluetooth headphones': 'Headphones',
    'ring light': 'Ring light',
    'laptop': 'Laptop',
    'iphone 10': 'iPhone X',
    'ipad': 'IPad',
    'imac': 'IMac',
    'samsung galaxy 10': 'Samsung Galaxy S10',
    'phone charger': 'Battery charger',
    'phone car charger': 'Car charger',
    'vacuum cleaner': 'Vacuum cleaner',
    'gadget for tiktok streaming': 'Webcam',
}

# Open Food Facts mapping for packaged items
OFF_SEARCH_ITEMS = {
    'fresh bread': 'bread loaf',
    'chocolate bread': 'pain au chocolat',
    'pancakes': 'pancakes',
    'cake': 'cake',
    'muffins': 'muffins',
    'yogurt cake': 'yogurt cake',
    'milk': 'milk 1l',
    'nonfat milk': 'nonfat milk 1l',
    'butter': 'butter',
    'cream': 'cream',
    'light cream': 'light cream',
    'eggs': 'eggs',
    'honey': 'honey',
    'low fat yogurt': 'low fat yogurt',
    'cottage cheese': 'cottage cheese',
    'fromage blanc': 'fromage blanc',
    'grated cheese': 'grated cheese',
    'parmesan cheese': 'parmesan cheese',
    'strong cheese': 'cheddar cheese',
    'frozen smoothie': 'frozen smoothie',
    'mayonnaise': 'mayonnaise',
    'light mayo': 'light mayonnaise',
    'canned_tuna': 'canned tuna',
    'mineral water': 'mineral water bottle',
    'sparkling water': 'sparkling water',
    'soda': 'soda bottle',
    'beer': 'beer can',
    'black beer': 'stout beer',
    'red wine': 'red wine bottle',
    'white wine': 'white wine bottle',
    'french wine': 'bordeaux wine',
    'champagne': 'champagne bottle',
    'cider': 'cider bottle',
    'dessert wine': 'port wine',
    'energy drink': 'energy drink can',
    'antioxydant juice': 'juice bottle',
    'tomato juice': 'tomato juice',
    'green tea': 'green tea pack',
    'black tea': 'black tea pack',
    'mint green tea': 'mint tea',
    'tea': 'tea bags',
    'cereals': 'cereal box',
    'oatmeal': 'oatmeal',
    'protein bar': 'protein bar',
    'energy bar': 'energy bar',
    'gluten free bar': 'gluten free bar',
    'hand protein bar': 'protein bar',
    'brownies': 'brownies',
    'cookies': 'cookies box',
    'candy bars': 'chocolate candy bar',
    'chocolate': 'milk chocolate bar',
    'extra dark chocolate': 'dark chocolate bar',
    'almonds': 'almonds bag',
    'gums': 'gummy candy bag',
    'rice': 'white rice bag',
    'whole wheat rice': 'brown rice bag',
    'pasta': 'pasta pack',
    'spaghetti': 'spaghetti pack',
    'whole wheat pasta': 'whole wheat pasta pack',
    'whole weat flour': 'whole wheat flour',
    'cooking oil': 'sunflower oil',
    'olive oil': 'olive oil bottle',
    'oil': 'cooking oil',
    'salt': 'table salt',
    'tomato sauce': 'tomato sauce jar',
    'ketchup': 'ketchup bottle',
    'barbecue sauce': 'barbecue sauce',
    'burger sauce': 'burger sauce',
    'mushroom cream sauce': 'mushroom soup',
    'chutney': 'chutney',
    'pickles': 'pickles jar',
    'chili': 'chili powder',
    'soup': 'soup can',
    'mashed potato': 'mashed potato pack',
    'french fries': 'frozen french fries',
    'sandwich': 'sandwich',
    'toilet paper': 'toilet paper rolls',
    'napkins': 'paper napkins',
    'shampoo': 'shampoo bottle',
    'shower gel': 'shower gel',
    'deodorant': 'deodorant spray',
    'body spray': 'body spray',
    'toothpaste': 'toothpaste tube',
    'tooth brush': 'toothbrush pack',
    'cotton buds': 'cotton buds pack',
    'razor': 'shaver razor',
    'cologne': 'perfume cologne',
    'water spray': 'water spray bottle',
    'dog food': 'dog food pedigree',
    'cat food': 'cat food whiskas',
    'pet food': 'purina pet food',
    'babies food': 'nestle baby food',
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

def fetch_wikipedia_infobox_urls(title):
    urls = []
    try:
        title_clean = title.replace(" ", "_")
        url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title_clean)}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8')
            
        infobox_match = re.search(r'<table class="infobox[^">]*">(.*?)</table>', html, re.DOTALL)
        if infobox_match:
            infobox_html = infobox_match.group(1)
            img_matches = re.findall(r'src="([^"]+)"', infobox_html)
            for img_url in img_matches:
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                urls.append(img_url)
    except Exception as e:
        pass
    return urls

def fetch_openfoodfacts_urls(search_term):
    urls = []
    try:
        query_encoded = urllib.parse.quote(search_term)
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query_encoded}&search_simple=1&action=process&json=1&page_size=5"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        products = data.get('products', [])
        for p in products:
            img = p.get('image_front_url') or p.get('image_url')
            if img:
                urls.append(img)
    except Exception as e:
        pass
    return urls

def fetch_bing_urls(name, category):
    urls = []
    
    # Constructing queries that force supermarket/retailer context
    queries = []
    if category in ['Vegetais', 'Fruta', 'Padaria & Laticínios', 'Carne & Peixe', 'Despensa', 'Bebidas', 'Cereais & Snacks']:
        # Try Portuguese supermarket search terms
        pt_name = name.lower()
        if pt_name == 'spinach': pt_name = 'espinafres'
        elif pt_name == 'tomatoes': pt_name = 'tomate'
        elif pt_name == 'carrots': pt_name = 'cenoura'
        elif pt_name == 'green beans': pt_name = 'feijao verde'
        elif pt_name == 'salad': pt_name = 'salada'
        elif pt_name == 'zucchini': pt_name = 'curgete'
        elif pt_name == 'eggplant': pt_name = 'berinjela'
        elif pt_name == 'pepper': pt_name = 'pimento'
        elif pt_name == 'cauliflower': pt_name = 'couve flor'
        elif pt_name == 'corn': pt_name = 'milho doce'
        elif pt_name == 'shallot': pt_name = 'chalota'
        elif pt_name == 'yams': pt_name = 'inhame'
        elif pt_name == 'mint': pt_name = 'hortela'
        elif pt_name == 'strawberries': pt_name = 'morangos'
        elif pt_name == 'blueberries': pt_name = 'mirtilos'
        elif pt_name == 'bramble': pt_name = 'amoras'
        elif pt_name == 'melons': pt_name = 'melao'
        elif pt_name == 'green grapes': pt_name = 'uvas verdes'
        elif pt_name == 'chicken': pt_name = 'frango'
        elif pt_name == 'ground beef': pt_name = 'carne picada'
        elif pt_name == 'salmon': pt_name = 'salmao'
        elif pt_name == 'seabass': pt_name = 'robalo'
        elif pt_name == 'shrimp': pt_name = 'camarao'
        elif pt_name == 'catfish': pt_name = 'peixe gato'
        elif pt_name == 'trout': pt_name = 'truta'
        elif pt_name == 'turkey': pt_name = 'peru'
        elif pt_name == 'bacon': pt_name = 'bacon continente'
        elif pt_name == 'ham': pt_name = 'fiambre'
        elif pt_name == 'meatballs': pt_name = 'almondegas'
        elif pt_name == 'escalope': pt_name = 'bife escalope'
        elif pt_name == 'fresh tuna': pt_name = 'atum fresco'
        elif pt_name == 'burgers': pt_name = 'hamburguer'
        elif pt_name == 'hot dogs': pt_name = 'salsichas hot dog'
        elif pt_name == 'cider': pt_name = 'sidra'
        elif pt_name == 'energy drink': pt_name = 'bebida energetica'
        elif pt_name == 'gums': pt_name = 'gomas'
        elif pt_name == 'tomato sauce': pt_name = 'polpa tomate'
        elif pt_name == 'ketchup': pt_name = 'ketchup'
        elif pt_name == 'pickles': pt_name = 'pepinos pickles'
        elif pt_name == 'soup': pt_name = 'sopa continente'
        
        queries.append(f"{pt_name} continente")
        queries.append(f"{pt_name} site:continente.pt")
        queries.append(f"{name} supermarket product")
    elif category == 'Gaming':
        queries.append(f"{name} game cover art")
        queries.append(f"{name} switch game cover")
    elif category == 'Electrónica':
        queries.append(f"{name} official product photo")
        queries.append(f"{name} target product")
    else:
        queries.append(f"{name} product packaging")
        queries.append(f"{name} site:continente.pt")
        
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
    
    print(f"[SCRAPE-PHOTO-START] Processing: '{name}' ({category})...")
    
    candidate_urls = []
    
    # 1. Wikipedia explicit mapping
    if prod_id in WIKI_TITLE_MAPPING:
        wiki_title = WIKI_TITLE_MAPPING[prod_id]
        candidate_urls.extend(fetch_wikipedia_infobox_urls(wiki_title))
            
    # 2. Open Food Facts
    if prod_id in OFF_SEARCH_ITEMS:
        off_term = OFF_SEARCH_ITEMS[prod_id]
        candidate_urls.extend(fetch_openfoodfacts_urls(off_term))
            
    # 3. Direct Wikipedia infobox by name
    candidate_urls.extend(fetch_wikipedia_infobox_urls(name))
            
    # 4. Bing Search with Retailer context
    candidate_urls.extend(fetch_bing_urls(name, category))
    
    # Step A: First pass - download ONLY if URL is in WHITELIST_DOMAINS
    for img_url in candidate_urls:
        img_url_lower = img_url.lower()
        # Check if URL contains any whitelisted domains
        is_whitelisted = any(domain in img_url_lower for domain in WHITELIST_DOMAINS)
        
        if is_whitelisted:
            ext = get_extension(img_url)
            filename = f"product_{cleaned}{ext}"
            filepath = os.path.join(PUBLIC_IMG_DIR, filename)
            
            bytes_saved = download_file(img_url, filepath)
            if bytes_saved > 0:
                print(f"[WHITELIST-SUCCESS] '{name}' -> {filename} ({bytes_saved} bytes) from {img_url}")
                return prod_id, filename
                
    # Step B: Second pass - download from ANY domain but apply strict negative filters to avoid spam/diagrams
    # (Only if whitelist pass failed)
    for img_url in candidate_urls:
        img_url_lower = img_url.lower()
        
        # Negative filter terms
        bad_terms = ['diagram', 'uterus', 'anatomy', 'medical', 'map', 'flag', 'cartoon', 'illustration', 'clipart', 'vector', 'drawing']
        is_bad = any(term in img_url_lower for term in bad_terms)
        
        if not is_bad:
            ext = get_extension(img_url)
            filename = f"product_{cleaned}{ext}"
            filepath = os.path.join(PUBLIC_IMG_DIR, filename)
            
            bytes_saved = download_file(img_url, filepath)
            if bytes_saved > 0:
                print(f"[ANY-DOMAIN-SUCCESS] '{name}' -> {filename} ({bytes_saved} bytes) from {img_url}")
                return prod_id, filename
                
    print(f"[SCRAPE-PHOTO-FAILED] Could not find any clean image for '{name}'")
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
            
            if filename:
                line = re.sub(r"image:\s*(null|'[^']+'|`[^`]+`),?\s*", "", line)
                line = re.sub(
                    r"(price:\s*[\d.]+)",
                    f"image: '/product_images/{filename}', \\1",
                    line
                )
        new_lines.append(line)
        
    with open(PRODUCTS_JS, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
    print("Updated storeProducts.js with clean web scraped image paths.")

def main():
    # Keep folder, just let files be overwritten
    os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
    products = parse_products()
    
    print(f"Scraping real product photos for {len(products)} products...")
    downloaded_map = {}
    
    # 8 workers to avoid rate limiting
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_product, p): p for p in products}
        for future in as_completed(futures):
            prod_id, filename = future.result()
            if filename:
                downloaded_map[prod_id] = filename
                
    print(f"Scraped {len(downloaded_map)} of {len(products)} real product photos.")
    update_products_js(downloaded_map)

if __name__ == "__main__":
    main()
