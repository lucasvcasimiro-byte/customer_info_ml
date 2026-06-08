import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

url = "https://html.duckduckgo.com/html/?q=site:continente.pt+almonds"
try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Response length: {len(r.text)}")
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a', class_='result__snippet')
    print(f"Found {len(links)} snippet links")
    # Let's print the actual search result links
    res_links = soup.find_all('a', class_='result__url')
    for a in res_links[:5]:
        print(f"URL: {a.get_text(strip=True)} -> Href: {a.get('href')}")
except Exception as e:
    print(f"Error: {e}")
