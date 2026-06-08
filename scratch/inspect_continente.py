import urllib.request
import urllib.parse
import re

def inspect_html(query):
    query_encoded = urllib.parse.quote(query)
    url = f"https://www.continente.pt/pesquisa/?q={query_encoded}"
    
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            html = response.read().decode('utf-8')
            
        print("HTML length:", len(html))
        # Look for image URLs containing "dw" or "catalog" or "product"
        jpg_urls = re.findall(r'https://[^\s"\'()<>]+?\.(?:jpg|png|jpeg)[^\s"\'()<>]*', html)
        print(f"Total jpg/png URLs found: {len(jpg_urls)}")
        
        # print some unique ones that are likely products
        seen = set()
        count = 0
        for url in jpg_urls:
            url_clean = url.split('?')[0]
            if url_clean not in seen:
                seen.add(url_clean)
                if 'product' in url_clean.lower() or 'catalog' in url_clean.lower() or 'produtos' in url_clean.lower():
                    print("Candidate:", url)
                    count += 1
                    if count >= 30:
                        break
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    inspect_html("maionese")
