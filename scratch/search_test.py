import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

url = "https://www.continente.pt/pesquisa/?q=almonds"
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print(f"HTML Title: {soup.title.string if soup.title else 'No Title'}")

# Print first few image src and tags
print("\n--- FIRST 20 IMG TAGS ---")
img_tags = soup.find_all('img')
for i, img in enumerate(img_tags[:20]):
    print(f"{i}: src={img.get('src')}, class={img.get('class')}, alt={img.get('alt')}")

# Print first few links
print("\n--- FIRST 20 LINKS ---")
links = soup.find_all('a')
for i, a in enumerate(links[:20]):
    print(f"{i}: href={a.get('href')}, class={a.get('class')}, text={a.get_text(strip=True)[:40]}")
