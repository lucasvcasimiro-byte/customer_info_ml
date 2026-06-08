import urllib.request
import urllib.parse
import json
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Paths
BASE_DIR = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project"
PRODUCTS_JS = os.path.join(BASE_DIR, "dashboard", "src", "data", "storeProducts.js")
PUBLIC_IMG_DIR = os.path.join(BASE_DIR, "dashboard", "public", "product_images")

# Whitelist domains to ensure zero external spam downloads
SAFE_DOMAINS = [
    'upload.wikimedia.org',
    'images.openfoodfacts.org',
    'openfoodfacts.org',
    'wikimedia.org',
    'wikipedia.org'
]

# Explicit mapping for games, electronics, and foods to exact Wikipedia article titles
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
    
    # Fresh Produce & Fresh Foods
    'asparagus': 'Asparagus',
    'spinach': 'Spinach',
    'tomatoes': 'Tomato',
    'carrots': 'Carrot',
    'green beans': 'Green bean',
    'salad': 'Salad',
    'zucchini': 'Zucchini',
    'eggplant': 'Eggplant',
    'pepper': 'Bell pepper',
    'cauliflower': 'Cauliflower',
    'corn': 'Maize',
    'shallot': 'Shallot',
    'yams': 'Yam (vegetable)',
    'mint': 'Mentha',
    'flax seed': 'Flax',
    'avocado': 'Avocado',
    'strawberries': 'Strawberry',
    'blueberries': 'Blueberry',
    'bramble': 'Blackberry',
    'melons': 'Melon',
    'green grapes': 'Grape',
    'chicken': 'Chicken as food',
    'ground beef': 'Ground beef',
    'salmon': 'Salmon as food',
    'seabass': 'European seabass',
    'shrimp': 'Shrimp',
    'catfish': 'Catfish',
    'trout': 'Trout',
    'turkey': 'Turkey as food',
    'bacon': 'Bacon',
    'ham': 'Ham',
    'meatballs': 'Meatball',
    'escalope': 'Escalope',
    'fresh tuna': 'Tuna',
    'burgers': 'Hamburger',
    'hot dogs': 'Hot dog',
}

# Open Food Facts queries for packaged food / grocery items
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

def is_safe_url(url):
    url_lower = url.lower()
    return any(domain in url_lower for domain in SAFE_DOMAINS)

def download_file(url, filepath):
    if not is_safe_url(url):
        print(f"[REJECTED] Unsafe URL ignored: {url}")
        return 0
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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

def fetch_wikipedia_infobox_thumbnail(title):
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
            if img_matches:
                img_url = img_matches[0]
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                return img_url
    except Exception as e:
        pass
    return None

def fetch_openfoodfacts_thumbnail(search_term):
    try:
        query_encoded = urllib.parse.quote(search_term)
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query_encoded}&search_simple=1&action=process&json=1&page_size=3"
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
                return img
    except Exception as e:
        pass
    return None

def process_product(product):
    prod_id = product['id']
    name = product['name']
    category = product['category']
    cleaned = clean_id(prod_id)
    
    print(f"[SAFE-SCRAPE-START] Processing: '{name}' ({category})...")
    
    img_url = None
    source = ""
    
    # 1. Check Wikipedia explicit mapping
    if prod_id in WIKI_TITLE_MAPPING:
        wiki_title = WIKI_TITLE_MAPPING[prod_id]
        img_url = fetch_wikipedia_infobox_thumbnail(wiki_title)
        if img_url:
            source = "Wikipedia Infobox"
            
    # 2. Check Open Food Facts
    if not img_url and prod_id in OFF_SEARCH_ITEMS:
        off_term = OFF_SEARCH_ITEMS[prod_id]
        img_url = fetch_openfoodfacts_thumbnail(off_term)
        if img_url:
            source = "Open Food Facts"
            
    # 3. Direct Wikipedia Search
    if not img_url:
        img_url = fetch_wikipedia_infobox_thumbnail(name)
        if img_url:
            source = "Wikipedia Infobox (Direct)"
            
    if img_url and is_safe_url(img_url):
        ext = get_extension(img_url)
        filename = f"product_{cleaned}{ext}"
        filepath = os.path.join(PUBLIC_IMG_DIR, filename)
        
        bytes_saved = download_file(img_url, filepath)
        if bytes_saved > 0:
            print(f"[SAFE-SUCCESS] '{name}' -> {filename} ({bytes_saved} bytes) from {source}")
            return prod_id, filename
            
    print(f"[SAFE-FAILED] No safe image found for '{name}'. Using Vite category default.")
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
        
    print("Updated storeProducts.js with safe product image paths.")

def main():
    os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
    products = parse_products()
    
    print(f"Downloading 100% safe real product photos for {len(products)} products...")
    downloaded_map = {}
    
    # 10 workers for rapid concurrent processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_product, p): p for p in products}
        for future in as_completed(futures):
            prod_id, filename = future.result()
            if filename:
                downloaded_map[prod_id] = filename
                
    print(f"Safe download summary: {len(downloaded_map)} of {len(products)} images downloaded.")
    update_products_js(downloaded_map)

if __name__ == "__main__":
    main()
