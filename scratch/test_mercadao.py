import requests
from bs4 import BeautifulSoup
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

# Mercadão search URL
url = "https://mercadao.pt/search?q=abacate"
try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Length: {len(r.text)}")
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        # Check if there is a script containing product details, e.g. state or JSON
        print("First 1000 chars of HTML:")
        print(soup.text[:1000].strip())
        
        # Look for images and product page links
        images = soup.find_all('img')
        print(f"Found {len(images)} images")
        for idx, img in enumerate(images[:5]):
            print(f"  {idx}: src={img.get('src')} | alt={img.get('alt')}")
            
        links = soup.find_all('a')
        print(f"Found {len(links)} links")
        for idx, a in enumerate(links[:5]):
            print(f"  {idx}: href={a.get('href')} | text={a.get_text(strip=True)[:40]}")
except Exception as e:
    print(f"Error: {e}")
