import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

url = "https://www.amazon.es/s?k=airpods"
try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Length: {len(r.text)}")
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        # Check if we got the page or a captcha (e.g. title contains "Robot" or "Captcha")
        title = soup.title.string if soup.title else "No Title"
        print(f"Title: {title}")
        # Search for product image URLs or links
        # Amazon search results usually have class "s-image" for images
        images = soup.select("img.s-image")
        print(f"Found {len(images)} s-image elements")
        for idx, img in enumerate(images[:2]):
            print(f"  {idx}: {img.get('alt')} -> {img.get('src')}")
except Exception as e:
    print(f"Error: {e}")
