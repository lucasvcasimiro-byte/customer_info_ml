import sys
import requests
from bs4 import BeautifulSoup
import re

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

# Let's search for almonds
url = "https://www.continente.pt/pesquisa/?q=almonds"
r = requests.get(url, headers=headers)
html_content = r.text

print(f"Status Code: {r.status_code}")
print(f"Total HTML length: {len(html_content)}")

# Check if the search term "almond" or similar exists in the text
occurrences_almonds = len(re.findall(r'almonds', html_content, re.IGNORECASE))
occurrences_amendoas = len(re.findall(r'amendoa', html_content, re.IGNORECASE))
print(f"Occurrences of 'almonds': {occurrences_almonds}")
print(f"Occurrences of 'amendoa': {occurrences_amendoas}")

# Let's write the first 50000 characters to see if there's any JSON config or script containing product list
with open("scratch/continente_head.html", "w", encoding="utf-8") as f:
    f.write(html_content[:150000])

print("Wrote first 150k characters of HTML to scratch/continente_head.html")
