import requests
from bs4 import BeautifulSoup
import json
import time
import sys
import re
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

# 1. Product list and their Portuguese translations
products_to_scrape = [
    {"en": "airpods", "pt": "airpods"},
    {"en": "almonds", "pt": "amendoa"},
    {"en": "antioxydant juice", "pt": "sumo antioxidante"},
    {"en": "asparagus", "pt": "espargos"},
    {"en": "avocado", "pt": "abacate"},
    {"en": "babies food", "pt": "comida bebe"},
    {"en": "bacon", "pt": "bacon"},
    {"en": "barbecue sauce", "pt": "molho barbecue"},
    {"en": "beer", "pt": "cerveja"},
    {"en": "black beer", "pt": "cerveja preta"},
    {"en": "black tea", "pt": "cha preto"},
    {"en": "blueberries", "pt": "mirtilos"},
    {"en": "bluetooth headphones", "pt": "auscultadores bluetooth"},
    {"en": "body spray", "pt": "body spray"},
    {"en": "bramble", "pt": "amoras"},
    {"en": "brownies", "pt": "brownie"},
    {"en": "burger sauce", "pt": "molho burger"},
    {"en": "burgers", "pt": "hamburguer"},
    {"en": "butter", "pt": "manteiga"},
    {"en": "cake", "pt": "bolo"},
    {"en": "candy bars", "pt": "barras de chocolate"},
    {"en": "canned_tuna", "pt": "atum em lata"},
    {"en": "carrots", "pt": "cenoura"},
    {"en": "cat food", "pt": "comida gato"},
    {"en": "catfish", "pt": "peixe gato"},
    {"en": "cauliflower", "pt": "couve flor"},
    {"en": "cotton buds", "pt": "cotonetes"},
    {"en": "cream", "pt": "natas"},
    {"en": "deodorant", "pt": "desodorizante"},
    {"en": "dessert wine", "pt": "vinho porto"},
    {"en": "dog food", "pt": "comida cao"},
    {"en": "eggplant", "pt": "beringela"},
    {"en": "eggs", "pt": "ovos"},
    {"en": "energy bar", "pt": "barra energetica"},
    {"en": "energy drink", "pt": "bebida energetica"},
    {"en": "escalope", "pt": "escalopes"},
    {"en": "extra dark chocolate", "pt": "chocolate negro extra"},
    {"en": "final fantasy xix", "pt": "final fantasy"},
    {"en": "final fantasy xx", "pt": "final fantasy"},
    {"en": "final fantasy xxii", "pt": "final fantasy"},
    {"en": "flax seed", "pt": "sementes de linhaça"},
    {"en": "french fries", "pt": "batatas fritas"},
    {"en": "fresh bread", "pt": "pao fresco"},
    {"en": "fresh tuna", "pt": "atum fresco"},
    {"en": "fromage blanc", "pt": "queijo fresco batido"},
    {"en": "frozen smoothie", "pt": "smoothie"},
    {"en": "frozen vegetables", "pt": "legumes congelados"},
    {"en": "gadget for tiktok streaming", "pt": "tripé anel de luz"},
    {"en": "gluten free bar", "pt": "barra sem gluten"},
    {"en": "grated cheese", "pt": "queijo ralado"},
    {"en": "green beans", "pt": "feijao verde"},
    {"en": "green grapes", "pt": "uva verde"},
    {"en": "green tea", "pt": "cha verde"},
    {"en": "ground beef", "pt": "carne picada novilho"},
    {"en": "gums", "pt": "gomas"},
    {"en": "half-life 2", "pt": "half-life"},
    {"en": "half-life: alyx", "pt": "half-life"},
    {"en": "ham", "pt": "fiambre"},
    {"en": "hand protein bar", "pt": "barra proteina"},
    {"en": "herb & pepper", "pt": "ervas e pimenta"},
    {"en": "honey", "pt": "mel"},
    {"en": "hot dogs", "pt": "salsichas hot dog"},
    {"en": "imac", "pt": "imac"},
    {"en": "ipad", "pt": "ipad"},
    {"en": "iphone 10", "pt": "iphone"},
    {"en": "ketchup", "pt": "ketchup"},
    {"en": "laptop", "pt": "computador portatil"},
    {"en": "light cream", "pt": "natas light"},
    {"en": "light mayo", "pt": "maionese light"},
    {"en": "low fat yogurt", "pt": "iogurte magro"},
    {"en": "mashed potato", "pt": "pure batata"},
    {"en": "mayonnaise", "pt": "maionese"},
    {"en": "meatballs", "pt": "almondegas"},
    {"en": "megaman zero", "pt": "megaman"},
    {"en": "megaman zero 2", "pt": "megaman"},
    {"en": "megaman zero 3", "pt": "megaman"},
    {"en": "megaman zero 4", "pt": "megaman"},
    {"en": "melons", "pt": "melao"},
    {"en": "metroid fusion", "pt": "metroid"},
    {"en": "metroid prime", "pt": "metroid"},
    {"en": "milk", "pt": "leite"},
    {"en": "minecraft", "pt": "minecraft"},
    {"en": "mineral water", "pt": "agua mineral"},
    {"en": "mint", "pt": "hortela"},
    {"en": "mint green tea", "pt": "cha verde menta"},
    {"en": "muffins", "pt": "muffins"},
    {"en": "mushroom cream sauce", "pt": "molho cogumelos"},
    {"en": "napkins", "pt": "guardanapos"},
    {"en": "nonfat milk", "pt": "leite magro"},
    {"en": "oatmeal", "pt": "aveia"},
    {"en": "oil", "pt": "oleo alimentar"},
    {"en": "olive oil", "pt": "azeite"},
    {"en": "pancakes", "pt": "panquecas"},
    {"en": "parmesan cheese", "pt": "queijo parmesao"},
    {"en": "pasta", "pt": "massa"},
    {"en": "pepper", "pt": "pimenta"},
    {"en": "pet food", "pt": "comida animais"},
    {"en": "phone car charger", "pt": "carregador isqueiro carro"},
    {"en": "phone charger", "pt": "carregador telemovel"},
    {"en": "pickles", "pt": "pickles"},
    {"en": "pokemon scarlet", "pt": "pokemon scarlet"},
    {"en": "pokemon shield", "pt": "pokemon shield"},
    {"en": "pokemon sword", "pt": "pokemon sword"},
    {"en": "pokemon violet", "pt": "pokemon violet"},
    {"en": "portal", "pt": "portal"},
    {"en": "portal 2", "pt": "portal 2"},
    {"en": "protein bar", "pt": "barra proteica"},
    {"en": "ratchet & clank", "pt": "ratchet clank"},
    {"en": "ratchet & clank 2", "pt": "ratchet clank"},
    {"en": "ratchet & clank 3", "pt": "ratchet clank"},
    {"en": "razor", "pt": "gillette"},
    {"en": "red wine", "pt": "vinho tinto"},
    {"en": "rice", "pt": "arroz"},
    {"en": "ring light", "pt": "ring light"},
    {"en": "salad", "pt": "salada"},
    {"en": "salmon", "pt": "salmao"},
    {"en": "salt", "pt": "sal"},
    {"en": "samsung galaxy 10", "pt": "samsung galaxy"},
    {"en": "sandwich", "pt": "sandes"},
    {"en": "seabass", "pt": "robalo"},
    {"en": "shallot", "pt": "chalotas"},
    {"en": "shampoo", "pt": "shampoo"},
    {"en": "shower gel", "pt": "gel banho"},
    {"en": "shrimp", "pt": "camarao"},
    {"en": "soda", "pt": "refrigerante"},
    {"en": "soup", "pt": "sopa"},
    {"en": "spaghetti", "pt": "esparguete"},
    {"en": "sparkling water", "pt": "agua com gas"},
    {"en": "spinach", "pt": "espinafres"},
    {"en": "strawberries", "pt": "morango"},
    {"en": "strong cheese", "pt": "queijo curado forte"},
    {"en": "tea", "pt": "cha"},
    {"en": "toilet paper", "pt": "papel higienico"},
    {"en": "tomato juice", "pt": "sumo de tomate"},
    {"en": "tomato sauce", "pt": "molho de tomate"},
    {"en": "tomatoes", "pt": "tomate"},
    {"en": "tooth brush", "pt": "escova de dentes"},
    {"en": "toothpaste", "pt": "pasta de dentes"},
    {"en": "trout", "pt": "truta"},
    {"en": "turkey", "pt": "peru"},
    {"en": "vacuum cleaner", "pt": "aspirador"},
    {"en": "vegetables mix", "pt": "mistura de legumes"},
    {"en": "water spray", "pt": "agua termal"},
    {"en": "white wine", "pt": "vinho branco"},
    {"en": "whole weat flour", "pt": "farinha integral"},
    {"en": "whole wheat pasta", "pt": "massa integral"},
    {"en": "whole wheat rice", "pt": "arroz integral"},
    {"en": "yams", "pt": "inhame"},
    {"en": "yogurt cake", "pt": "bolo de iogurte"},
    {"en": "zucchini", "pt": "curgete"}
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

def clean_text(text):
    if not text:
        return ""
    # Remove accents
    nfkd_form = unicodedata.normalize('NFKD', text)
    only_ascii = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    # Lowercase and keep alphanumeric only
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', only_ascii).lower()
    return clean

def score_match(product_name, target_en, target_pt):
    # Standard scoring based on matching words
    p_clean = clean_text(product_name)
    en_words = set(clean_text(target_en).split())
    pt_words = set(clean_text(target_pt).split())
    p_words = set(p_clean.split())
    
    # Calculate word overlap
    en_overlap = len(en_words.intersection(p_words))
    pt_overlap = len(pt_words.intersection(p_words))
    max_overlap = max(en_overlap, pt_overlap)
    
    # Heuristic penalty for title length (prefer shorter, precise matches)
    length_penalty = len(p_words) * 0.05
    score = max_overlap - length_penalty
    return score

def scrape_continente(query, target_en, target_pt):
    url = f"https://www.continente.pt/pesquisa/?q={query}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        tiles = soup.select('div.product-tile')
        best_match = None
        best_score = -999.0
        
        for tile in tiles:
            impression_str = tile.get('data-product-tile-impression')
            if not impression_str:
                continue
            try:
                prod_data = json.loads(impression_str)
            except Exception:
                continue
            name = prod_data.get('name')
            if not name:
                continue
            
            # Extract link
            link_el = tile.select_one('a.image-link') or tile.select_one('a[href*="/produto/"]')
            product_url = ""
            if link_el:
                product_url = link_el.get('href')
                if product_url and product_url.startswith('/'):
                    product_url = "https://www.continente.pt" + product_url
            
            # Extract image
            img_el = tile.select_one('img.ct-tile-image') or tile.select_one('img[src*="/images/col/"]')
            image_url = ""
            if img_el:
                image_url = img_el.get('data-src') or img_el.get('src')
                if image_url and image_url.startswith('/'):
                    image_url = "https://www.continente.pt" + image_url
            
            if not product_url or not image_url:
                continue
                
            score = score_match(name, target_en, target_pt)
            if score > best_score:
                best_score = score
                best_match = {
                    "search_source": "continente.pt",
                    "product_page": product_url,
                    "image_url": image_url,
                    "name": name,
                    "score": score
                }
        return best_match
    except Exception as e:
        print(f"Continente error for {query}: {e}")
        return None

def scrape_auchan(query, target_en, target_pt):
    url = f"https://www.auchan.pt/pt/pesquisa?q={query}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        tiles = soup.select('div.product-tile')
        best_match = None
        best_score = -999.0
        
        for tile in tiles:
            # Extract name and URLs
            gtm_str = tile.get('data-gtm') or tile.get('data-gtm-new')
            name = ""
            if gtm_str:
                try:
                    gtm_data = json.loads(gtm_str)
                    name = gtm_data.get('name') or gtm_data.get('item_name')
                except Exception:
                    pass
            
            # Fallback name from image alt
            img_el = tile.select_one('img.tile-image')
            if not name and img_el:
                name = img_el.get('alt')
            
            if not name:
                continue
                
            urls_str = tile.get('data-urls')
            product_url = ""
            if urls_str:
                try:
                    urls_data = json.loads(urls_str)
                    product_url = urls_data.get('absoluteProductUrl') or urls_data.get('productUrl')
                    if product_url and product_url.startswith('/'):
                        product_url = "https://www.auchan.pt" + product_url
                except Exception:
                    pass
            
            image_url = ""
            if img_el:
                image_url = img_el.get('data-src') or img_el.get('src')
                
            if not product_url or not image_url:
                continue
                
            score = score_match(name, target_en, target_pt)
            if score > best_score:
                best_score = score
                best_match = {
                    "search_source": "auchan.pt",
                    "product_page": product_url,
                    "image_url": image_url,
                    "name": name,
                    "score": score
                }
        return best_match
    except Exception as e:
        print(f"Auchan error for {query}: {e}")
        return None

# Loop and scrape
results = []
missing = []

print(f"Starting scraping for {len(products_to_scrape)} items...")

for idx, p in enumerate(products_to_scrape):
    en_name = p["en"]
    pt_name = p["pt"]
    print(f"[{idx+1}/{len(products_to_scrape)}] Searching: {en_name} ({pt_name})...")
    
    # 1. Search Continente using Portuguese name
    match = scrape_continente(pt_name, en_name, pt_name)
    
    # 2. If not found, search Continente using English name
    if not match and en_name != pt_name:
        match = scrape_continente(en_name, en_name, pt_name)
        
    # 3. If not found, search Auchan using Portuguese name
    if not match:
        match = scrape_auchan(pt_name, en_name, pt_name)
        
    # 4. If not found, search Auchan using English name
    if not match and en_name != pt_name:
        match = scrape_auchan(en_name, en_name, pt_name)
        
    if match:
        results.append({
            "product_name": en_name,
            "search_source": match["search_source"],
            "product_page": match["product_page"],
            "image_url": match["image_url"],
            "matched_name": match["name"]
        })
        print(f"  Found on {match['search_source']}: {match['name']}")
    else:
        missing.append(p)
        print("  Not found!")
        
    time.sleep(1.0) # Respect rate limits

# Save initial results
output_data = {
    "found": results,
    "missing": missing
}

with open("scratch/scraping_results_v1.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("\n=== SCRAPING PHASE 1 COMPLETE ===")
print(f"Found: {len(results)}")
print(f"Missing: {len(missing)}")
print(f"Saved results to scratch/scraping_results_v1.json")
