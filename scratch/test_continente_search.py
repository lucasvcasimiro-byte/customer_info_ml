import requests
from bs4 import BeautifulSoup
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

def search_continente(query):
    url = f"https://www.continente.pt/pesquisa/?q={query}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        tiles = soup.select('div.product-tile')
        results = []
        for tile in tiles:
            impression_str = tile.get('data-product-tile-impression')
            product_data = {}
            if impression_str:
                try:
                    product_data = json.loads(impression_str)
                except Exception:
                    pass
            
            link_el = tile.select_one('a.image-link') or tile.select_one('a[href*="/produto/"]')
            product_url = ""
            if link_el:
                product_url = link_el.get('href')
                if product_url and product_url.startswith('/'):
                    product_url = "https://www.continente.pt" + product_url

            img_el = tile.select_one('img.ct-tile-image') or tile.select_one('img[src*="/images/col/"]')
            image_url = ""
            if img_el:
                image_url = img_el.get('data-src') or img_el.get('src')
                if image_url and image_url.startswith('/'):
                    image_url = "https://www.continente.pt" + image_url
            
            if product_data.get('name'):
                results.append({
                    'name': product_data.get('name'),
                    'url': product_url,
                    'image': image_url
                })
        return r.status_code, len(results), results
    except Exception as e:
        return 0, 0, str(e)

test_queries = ["airpods", "abacate", "amendoas", "bacon", "minecraft"]
for q in test_queries:
    status, count, res = search_continente(q)
    print(f"Query: {q} | Status: {status} | Products Found: {count}")
    for idx, p in enumerate(res[:2]):
        print(f"  {idx}: {p['name']} | URL: {p['url']} | Image: {p['image']}")
