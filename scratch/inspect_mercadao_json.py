import requests
from bs4 import BeautifulSoup
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

url = "https://mercadao.pt/search?q=abacate"
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print(f"Status: {r.status_code}")
print(f"Final URL: {r.url}")

# Find script tags containing NEXT_DATA or state
scripts = soup.find_all('script')
print(f"Found {len(scripts)} script tags")

for idx, script in enumerate(scripts):
    content = script.string or ''
    # check for next data
    if script.get('id') == '__NEXT_DATA__':
        print(f"Found __NEXT_DATA__ script in script {idx}!")
        print(f"Length of __NEXT_DATA__: {len(content)}")
        print(content[:500])
        with open("scratch/next_data.json", "w", encoding="utf-8") as f:
            f.write(content)
        print("Saved __NEXT_DATA__ to scratch/next_data.json")
        
    # check for other large JSON/JS state variables
    elif 'window.' in content or 'initialState' in content or 'state =' in content:
        print(f"Found potential state script in script {idx} (length {len(content)}):")
        print(content[:300])
