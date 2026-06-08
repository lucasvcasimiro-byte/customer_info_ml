import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

url = "https://www.elcorteingles.pt/supermercado/pesquisa/?term=abacate"
try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"El Corte Inglés: Status = {r.status_code}, Length = {len(r.text)}, Final URL = {r.url}")
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        tiles = soup.select('div.product_tile') or soup.select('div[class*="product"]')
        print(f"Found {len(tiles)} product-related elements")
except Exception as e:
    print(f"El Corte Inglés failed: {e}")
