import sys
import json
import requests
from bs4 import BeautifulSoup
import re

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

url = "https://www.continente.pt/pesquisa/?q=almonds"
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

tiles = soup.select('div.product-tile')
print(f"Total product-tile divs found: {len(tiles)}")

for idx, tile in enumerate(tiles):
    # Try to parse data-product-tile-impression
    impression_str = tile.get('data-product-tile-impression')
    product_data = {}
    if impression_str:
        try:
            product_data = json.loads(impression_str)
        except Exception as e:
            pass
    
    # Try to find the link
    link_el = tile.select_one('a.image-link') or tile.select_one('a[href*="/produto/"]')
    product_url = ""
    if link_el:
        product_url = link_el.get('href')
        if product_url and product_url.startswith('/'):
            product_url = "https://www.continente.pt" + product_url

    # Try to find the image
    img_el = tile.select_one('img.ct-tile-image') or tile.select_one('img[src*="/images/col/"]')
    image_url = ""
    if img_el:
        image_url = img_el.get('data-src') or img_el.get('src')
        if image_url and image_url.startswith('/'):
            image_url = "https://www.continente.pt" + image_url
            
    print(f"Product {idx}:")
    print(f"  Name: {product_data.get('name')}")
    print(f"  Category: {product_data.get('category')}")
    print(f"  URL: {product_url}")
    print(f"  Image: {image_url}")
    if idx >= 5:
        print("...")
        break
