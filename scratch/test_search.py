import urllib.request
import urllib.parse
import re
import json

def ddg_search(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = 'https://html.duckduckgo.com/html/?' + urllib.parse.urlencode({'q': query})
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        return str(e)

print("Testing DuckDuckGo search...")
html = ddg_search("site:worten.pt airpods")
print("HTML length:", len(html))
if "worten.pt" in html:
    print("Found worten.pt in HTML!")
else:
    print("Worten not found or blocked.")
