import requests
from bs4 import BeautifulSoup
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

url = "https://www.pingodoce.pt/pesquisa/?q=abacate"
try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Length: {len(r.text)}")
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Let's search for product tiles
    tiles = soup.select('div.product-tile')
    print(f"Found {len(tiles)} product tiles")
    
    for idx, tile in enumerate(tiles[:5]):
        impression_str = tile.get('data-product-tile-impression')
        product_data = {}
        if impression_str:
            try:
                product_data = json.loads(impression_str)
            except Exception:
                pass
        
        # Link and image
        link_el = tile.select_one('a.image-link') or tile.select_one('a[href*="/produtos/"]') or tile.select_one('a[href*="/produto/"]')
        product_url = ""
        if link_el:
            product_url = link_el.get('href')
            if product_url and product_url.startswith('/'):
                product_url = "https://www.pingodoce.pt" + product_url

        # Check for image element
        img_el = tile.select_one('img')
        image_url = ""
        if img_el:
            image_url = img_el.get('data-src') or img_el.get('src')
            if image_url and image_url.startswith('/'):
                image_url = "https://www.pingodoce.pt" + image_url
                
        print(f"Product {idx}:")
        print(f"  Name: {product_data.get('name') or tile.get_text(strip=True)[:50]}")
        print(f"  URL: {product_url}")
        print(f"  Image: {image_url}")
except Exception as e:
    print(f"Error: {e}")
