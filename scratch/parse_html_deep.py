import sys
from bs4 import BeautifulSoup
import re

sys.stdout.reconfigure(encoding='utf-8')

# Read from saved HTML or refetch
import requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}
url = "https://www.continente.pt/pesquisa/?q=almonds"
r = requests.get(url, headers=headers)
html_content = r.text

soup = BeautifulSoup(html_content, 'html.parser')

print("=== CHECKING FOR IMAGES ===")
images = soup.find_all('img')
count = 0
for img in images:
    src = img.get('src') or img.get('data-src') or img.get('data-original') or img.get('data-src-retina')
    alt = img.get('alt', '')
    # Check if this looks like a product image
    if src and any(term in src for term in ['cdn.continente.pt', 'produtos', 'images', 'jpg', 'png']):
        # Ignore small icons, logos, etc.
        if 'logo' in src or 'icon' in src or 'svg' in src or 'brand' in src:
            continue
        print(f"Image: src={src}, alt={alt}, class={img.get('class')}")
        count += 1
        if count > 20:
            break

print("\n=== CHECKING FOR PRODUCT LINKS ===")
links = soup.find_all('a')
count = 0
for a in links:
    href = a.get('href')
    # Product links on Continente often have /p/ in the path
    if href and ('/p/' in href or '/produto/' in href):
        print(f"Link: href={href}, text={a.get_text(strip=True)[:50]}, class={a.get('class')}")
        count += 1
        if count > 20:
            break

print("\n=== SEARCHING FOR ALMOND CONTENT ===")
# Find elements that contain "almond" in their text
elements = soup.find_all(text=re.compile(r'almond', re.IGNORECASE))
print(f"Found {len(elements)} text nodes containing 'almond'")
for idx, el in enumerate(elements[:10]):
    parent = el.parent
    print(f"Text: {el.strip()[:60]} | Parent tag: {parent.name} | Parent class: {parent.get('class')}")
