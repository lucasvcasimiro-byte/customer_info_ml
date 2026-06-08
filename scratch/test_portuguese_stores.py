import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

stores = {
    "FNAC": "https://www.fnac.pt/SearchResult/SearchResult.aspx?Search=minecraft",
    "Worten": "https://www.worten.pt/pesquisa?query=minecraft",
    "PCDIGA": "https://www.pcdiga.com/search?query=minecraft",
    "KuantoKusta": "https://www.kuantokusta.pt/search?q=minecraft"
}

for name, url in stores.items():
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"{name}: Status = {r.status_code}, Length = {len(r.text)}, Final URL = {r.url}")
    except Exception as e:
        print(f"{name} failed: {e}")
