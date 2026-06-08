import sys
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

url = "https://www.continente.pt/pesquisa/?q=almonds"
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

# Find product tiles. Let's look for divs with classes like product-grid, product-tile, ct-product-tile, etc.
# In our previous run, we saw:
# Image class: ['ct-tile-image', 'lazyload', 'hidden']
# Description class: ['pwc-tile--description']
# Link class: ['image-link', 'pb-1']

tiles = soup.find_all('div', class_=lambda x: x and ('product' in x or 'tile' in x))
print(f"Found {len(tiles)} product tiles/divs")

# Let's find divs containing the class 'ct-product-tile' or similar
pwc_tiles = soup.find_all('div', class_=lambda x: x and any(term in x for term in ['product-tile', 'pwc-tile']))
print(f"Found {len(pwc_tiles)} specific pwc/product tiles")

for idx, tile in enumerate(pwc_tiles[:3]):
    print(f"\n--- TILE {idx} ---")
    print(tile.prettify()[:1000])
