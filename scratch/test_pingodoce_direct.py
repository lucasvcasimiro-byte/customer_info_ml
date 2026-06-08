import requests
from bs4 import BeautifulSoup
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

url = "https://www.pingodoce.pt/on/demandware.store/Sites-pingo-doce-Site/default/Default-Start?q=abacate"
try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Final URL: {r.url}")
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Check for elements containing product details
    tiles = soup.select('div.product-tile') or soup.select('div.product') or soup.select('div[class*="product"]')
    print(f"Found {len(tiles)} product-related divs")
    
    # Check if there are any divs with class product-tile
    p_tiles = soup.select('div.product-tile')
    print(f"Found {len(p_tiles)} 'div.product-tile'")
    
    # Check for image links or names containing abacate
    abacate_imgs = soup.find_all('img', alt=lambda x: x and 'abacate' in x.lower())
    print(f"Found {len(abacate_imgs)} image tags containing 'abacate' in alt attribute")
    for idx, img in enumerate(abacate_imgs[:5]):
        print(f"  Image {idx}: alt={img.get('alt')} | src={img.get('src') or img.get('data-src')}")
        
    abacate_links = soup.find_all('a', href=lambda x: x and 'abacate' in x.lower())
    print(f"Found {len(abacate_links)} links containing 'abacate' in href")
    for idx, a in enumerate(abacate_links[:5]):
        print(f"  Link {idx}: href={a.get('href')} | text={a.get_text(strip=True)[:40]}")
except Exception as e:
    print(f"Error: {e}")
