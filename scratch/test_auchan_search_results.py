import requests
from bs4 import BeautifulSoup
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

url = "https://www.auchan.pt/pt/pesquisa?q=amendoas"
try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Final URL: {r.url}")
    print(f"Length: {len(r.text)}")
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Check for product tiles. Since it's Demandware (Salesforce), it might use div.product-tile or similar classes.
    tiles = soup.select('div.product-tile') or soup.select('div.product') or soup.select('div[class*="product-grid"]')
    print(f"Found {len(tiles)} product-related elements")
    
    # Let's search for divs with class containing product-tile
    p_tiles = soup.select('div.product-tile')
    print(f"Found {len(p_tiles)} 'div.product-tile'")
    
    # Find any image with src containing dw/image or products or check-icon
    images = soup.find_all('img')
    print(f"Found {len(images)} images total")
    count = 0
    for img in images:
        src = img.get('src') or img.get('data-src')
        alt = img.get('alt', '')
        if src and ('dw/image' in src or 'produtos' in src or 'auc-master' in src):
            print(f"  Img: alt={alt} | src={src}")
            count += 1
            if count > 5:
                break
                
    # Find any link with /produto/ or /pd/ or /p/
    links = soup.find_all('a')
    print(f"Found {len(links)} links total")
    count = 0
    for a in links:
        href = a.get('href')
        text = a.get_text(strip=True)
        if href and ('/produto/' in href or '/p/' in href or '-p-' in href):
            print(f"  Link: href={href} | text={text[:40]}")
            count += 1
            if count > 5:
                break
except Exception as e:
    print(f"Error: {e}")
