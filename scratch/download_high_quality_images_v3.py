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
    
    # Fresh foods / produce
    'asparagus': 'Asparagus',
    'spinach': 'Spinach',
    'tomatoes': 'Tomato',
    'carrots': 'Carrots',
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
    # Padaria & Laticínios
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
    
    # Bebidas
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
    
    # Cereais & Snacks
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
    
    # Despensa
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
    
    # Higiene
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
    
    # Animais & Bebé
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
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
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
    try:
        query = f"{name} product packaging"
        if category == 'Gaming':
            query = f"{name} game cover box art"
        elif category == 'Electrónica':
            query = f"{name} official product photo"
            
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
            img_url_lower = img_url.lower()
            if category not in ['Gaming', 'Electrónica']:
                if any(t in img_url_lower for t in ['diagram', 'uterus', 'anatomy', 'medical', 'map', 'flag', 'cartoon', 'illustration']):
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
    
    print(f"[RETRY-V3-START] Processing: '{name}' ({category})...")
    
    candidate_urls = []
    
    # 1. Wikipedia mapping
    if prod_id in WIKI_TITLE_MAPPING:
        wiki_title = WIKI_TITLE_MAPPING[prod_id]
        candidate_urls.extend(fetch_wikipedia_infobox_urls(wiki_title))
            
    # 2. Open Food Facts
    if prod_id in OFF_SEARCH_ITEMS:
        off_term = OFF_SEARCH_ITEMS[prod_id]
        candidate_urls.extend(fetch_openfoodfacts_urls(off_term))
            
    # 3. Direct Wikipedia Infobox
    candidate_urls.extend(fetch_wikipedia_infobox_urls(name))
            
    # 4. Bing Fallback
    candidate_urls.extend(fetch_bing_urls(name, category))
    
    # Try downloading candidates sequentially until one succeeds
    for img_url in candidate_urls:
        ext = get_extension(img_url)
        filename = f"product_{cleaned}{ext}"
        filepath = os.path.join(PUBLIC_IMG_DIR, filename)
        
        bytes_saved = download_file(img_url, filepath)
        if bytes_saved > 0:
            print(f"[RETRY-V3-SUCCESS] '{name}' ({category}) -> {filename} ({bytes_saved} bytes) from {img_url}")
            return prod_id, filename
            
    print(f"[RETRY-V3-FAILED] Could not download image for '{name}'")
    return prod_id, None

def get_missing_products(all_products):
    with open(PRODUCTS_JS, 'r', encoding='utf-8') as f:
        content = f.read()
        
    missing_ids = set()
    lines = content.split('\n')
    for line in lines:
        if 'id:' in line:
            id_match = re.search(r"id:\s*'([^']+)'", line)
            img_match = re.search(r"image:\s*(null|'[^']+')", line)
            if id_match:
                prod_id = id_match.group(1)
                img = img_match.group(1) if img_match else None
                if not img or img == 'null':
                    missing_ids.add(prod_id)
                    
    return [p for p in all_products if p['id'] in missing_ids]

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
        new_lines.append(line)
        
    with open(PRODUCTS_JS, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
    print("Updated storeProducts.js with retried image paths.")

def main():
    os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
    all_products = parse_all_products()
    missing_products = get_missing_products(all_products)
    
    if not missing_products:
        print("No missing products to retry. All images exist!")
        return
        
    print(f"Retrying download for {len(missing_products)} missing products using list-based fallback...")
    downloaded_map = {}
    
    # 8 workers for safe parallel downloads
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_product, p): p for p in missing_products}
        for future in as_completed(futures):
            prod_id, filename = future.result()
            if filename:
                downloaded_map[prod_id] = filename
                
    print(f"Retry summary: {len(downloaded_map)} of {len(missing_products)} images downloaded.")
    update_products_js(downloaded_map)

if __name__ == "__main__":
    main()
