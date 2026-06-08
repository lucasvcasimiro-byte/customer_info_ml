import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

url = "https://www.auchan.pt/pt/pesquisa?q=amendoas"
try:
    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    tiles = soup.select('div.product-tile')
    if tiles:
        for idx, tile in enumerate(tiles[:2]):
            print(f"\n--- Tile {idx} Images ---")
            imgs = tile.find_all('img')
            for img_idx, img in enumerate(imgs):
                print(f"  Image {img_idx}: src={img.get('src')} | data-src={img.get('data-src')} | class={img.get('class')} | alt={img.get('alt')}")
except Exception as e:
    print(f"Error: {e}")
