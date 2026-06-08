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

# Whitelist domains to ensure 100% appropriate product photos
SAFE_DOMAINS = [
    'continente.pt', 'produtos.continente.pt', 'auchan.pt', 'pingo-doce.pt', 
    'elcorteingles.pt', 'elcorteingles.es', 'auchan.fr', 'intermarche.pt',
    'upload.wikimedia.org', 'wikimedia.org', 'wikipedia.org',
    'images.openfoodfacts.org', 'openfoodfacts.org', 'demandware.net', 'demandware.static'
]

# Explicit mapping for games, electronics, and fresh foods to exact Wikipedia article titles
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
    'fresh bread': 'pao de forma',
    'chocolate bread': 'pain au chocolat',
    'pancakes': 'panquecas',
    'cake': 'bolo',
    'muffins': 'muffins',
    'yogurt cake': 'bolo iogurte',
    'milk': 'leite meio gordo',
    'nonfat milk': 'leite magro',
    'butter': 'manteiga com sal',
    'cream': 'natas',
    'light cream': 'natas leves',
    'eggs': 'ovos classe L',
    'honey': 'mel de flores',
    'low fat yogurt': 'iogurte magro',
    'cottage cheese': 'requeijao',
    'fromage blanc': 'queijo fresco',
    'grated cheese': 'queijo ralado',
    'parmesan cheese': 'queijo parmigiano',
    'strong cheese': 'queijo cheddar',
    'frozen smoothie': 'smoothie polpa',
    'mayonnaise': 'maionese heinz',
    'light mayo': 'maionese light',
    'canned_tuna': 'atum em oleo',
    'mineral water': 'agua luso',
    'sparkling water': 'agua das pedras',
    'soda': 'coca cola 1.5l',
    'beer': 'cerveja super bock',
    'black beer': 'cerveja preta',
    'red wine': 'vinho tinto alentejo',
    'white wine': 'vinho branco verde',
    'french wine': 'vinho bordeaux',
    'champagne': 'champagne moet',
    'cider': 'sidra somersby',
    'dessert wine': 'vinho do porto',
    'energy drink': 'red bull lata',
    'antioxydant juice': 'sumo compal',
    'tomato juice': 'sumo tomate',
    'green tea': 'cha verde lipton',
    'black tea': 'cha preto',
    'mint green tea': 'cha menta',
    'tea': 'cha saquetas',
    'cereals': 'cereais nestle chocapic',
    'oatmeal': 'aveia flocos',
    'protein bar': 'barra proteica',
    'energy bar': 'barra energetica',
    'gluten free bar': 'barra sem gluten',
    'hand protein bar': 'barra proteina',
    'brownies': 'brownies chocolate',
    'cookies': 'bolachas cookies',
    'candy bars': 'barra chocolate snickers',
    'chocolate': 'tablete chocolate de leite',
    'extra dark chocolate': 'tablete chocolate preto 70',
    'almonds': 'amendoas saco',
    'gums': 'gomas saco haribo',
    'rice': 'arroz agulha 1kg',
    'whole wheat rice': 'arroz integral',
    'pasta': 'massa cotovelos',
    'spaghetti': 'massa esparguete milaneza',
    'whole wheat pasta': 'massa integral',
    'whole weat flour': 'farinha trigo integral',
    'cooking oil': 'oleo alimentao',
    'olive oil': 'azeite virgem extra',
    'oil': 'oleo fula',
    'salt': 'sal marinho fidalgo',
    'tomato sauce': 'polpa tomate compal',
    'ketchup': 'ketchup heinz',
    'barbecue sauce': 'molho barbecue',
    'burger sauce': 'molho hamburguer',
    'mushroom cream sauce': 'creme cogumelos',
    'chutney': 'chutney',
    'pickles': 'pickles frasco',
    'chili': 'chili po',
    'soup': 'sopa legumes continente',
    'mashed potato': 'pure batata maggi',
    'french fries': 'batatas fritas mccain',
    'sandwich': 'sandwich club',
    'toilet paper': 'papel higienico renova',
    'napkins': 'guardanapos papel',
    'shampoo': 'shampoo pantene',
    'shower gel': 'gel banho dove',
    'deodorant': 'desodorizante rexona',
    'body spray': 'ax body spray',
    'toothpaste': 'dentifrico colgate',
    'tooth brush': 'escova dentes oral b',
    'cotton buds': 'cotonetes caixas',
    'razor': 'gillette lamina',
    'cologne': 'agua colonia nenuco',
    'water spray': 'spray agua termal',
    'dog food': 'racao cao friskies',
    'cat food': 'racao gato whiskas',
    'pet food': 'purina pet food',
    'babies food': 'papas nestle nestum',
}

# Portuguese keywords for search queries
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
    'french fries': 'batatas fritas',
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
    return any(domain in url_lower for domain in SAFE_DOMAINS)

def download_file(url, filepath):
    if not is_safe_url(url):
        return 0
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'NOVAIMSGroceryStoreSimulator/1.0 (afonso@novaims.unl.pt)'
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
            headers={'User-Agent': 'NOVAIMSGroceryStoreSimulator/1.0 (afonso@novaims.unl.pt)'}
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
            headers={'User-Agent': 'NOVAIMSGroceryStoreSimulator/1.0 (afonso@novaims.unl.pt)'}
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

def fetch_bing_safe_supermarket_urls(name, category):
    urls = []
    
    pt_name = PORTUGUESE_KEYWORDS.get(name.lower(), name.lower())
    
    queries = []
    if category in ['Vegetais', 'Fruta', 'Padaria & Laticínios', 'Carne & Peixe', 'Despensa', 'Bebidas', 'Cereais & Snacks']:
        # Strict Continente/supermarket filters
        queries.append(f"site:continente.pt {pt_name}")
        queries.append(f"site:produtos.continente.pt {pt_name}")
        queries.append(f"site:elcorteingles.pt {pt_name}")
    elif category == 'Gaming':
        queries.append(f"site:nintendo.com {name} box art")
        queries.append(f"site:en.wikipedia.org {name} game")
    elif category == 'Electrónica':
        queries.append(f"site:en.wikipedia.org {name}")
        
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
                
            for img_url in matches[:15]:
                if is_safe_url(img_url):
                    urls.append(img_url)
        except Exception as e:
            pass
            
    return urls

def process_product(product):
    prod_id = product['id']
    name = product['name']
    category = product['category']
    cleaned = clean_id(prod_id)
    
    print(f"[SCRAPE-START] Processing: '{name}' ({category})...")
    
    candidate_urls = []
    
    # 1. Wikipedia explicit mapping
    if prod_id in WIKI_TITLE_MAPPING:
        wiki_title = WIKI_TITLE_MAPPING[prod_id]
        img_url = fetch_wikipedia_infobox_thumbnail(wiki_title)
        if img_url:
            candidate_urls.append(img_url)
            
    # 2. Open Food Facts
    if prod_id in OFF_SEARCH_ITEMS:
        off_term = OFF_SEARCH_ITEMS[prod_id]
        img_url = fetch_openfoodfacts_thumbnail(off_term)
        if img_url:
            candidate_urls.append(img_url)
            
    # 3. Direct Wikipedia infobox by name
    img_url = fetch_wikipedia_infobox_thumbnail(name)
    if img_url:
        candidate_urls.append(img_url)
        
    # 4. Bing Search strictly limited to safe domains
    candidate_urls.extend(fetch_bing_safe_supermarket_urls(name, category))
    
    # Download first successful candidate
    for img_url in candidate_urls:
        if is_safe_url(img_url):
            ext = get_extension(img_url)
            filename = f"product_{cleaned}{ext}"
            filepath = os.path.join(PUBLIC_IMG_DIR, filename)
            
            bytes_saved = download_file(img_url, filepath)
            if bytes_saved > 0:
                print(f"[SCRAPE-SUCCESS] '{name}' -> {filename} ({bytes_saved} bytes) from {img_url}")
                return prod_id, filename
                
    print(f"[SCRAPE-FAILED] No safe image for '{name}'. Fallback to default.")
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
        
    print("Updated storeProducts.js with clean image paths.")

def main():
    # Keep folder, just let files be overwritten
    os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
    products = parse_products()
    
    print(f"Scraping real product photos for {len(products)} products...")
    downloaded_map = {}
    
    # 10 workers for fast parallel processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_product, p): p for p in products}
        for future in as_completed(futures):
            prod_id, filename = future.result()
            if filename:
                downloaded_map[prod_id] = filename
                
    print(f"Scraped {len(downloaded_map)} of {len(products)} real product photos.")
    update_products_js(downloaded_map)

if __name__ == "__main__":
    main()
