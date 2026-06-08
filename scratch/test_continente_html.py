import urllib.request
import urllib.parse
import re

def test_continente_search(query):
    query_encoded = urllib.parse.quote(query)
    url = f"https://www.continente.pt/pesquisa/?q={query_encoded}"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8'
            }
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            html = response.read().decode('utf-8')
            
        # Let's search for image tags in the HTML
        # Continente image URLs typically contain something like /productimages/ or resemble product images
        # Let's find matches for: src="https://www.continente.pt/...jpg" or similar
        # Let's look for src="..." in img tags
        img_urls = re.findall(r'src="([^"]+continente\.pt/[^"]+)"', html)
        if not img_urls:
            img_urls = re.findall(r'data-src="([^"]+continente\.pt/[^"]+)"', html)
        if not img_urls:
            # General image match
            img_urls = re.findall(r'src="([^"]+\.(?:jpg|png|jpeg)[^"]*)"', html)
            
        print(f"Continente search HTML results for '{query}':")
        for img in img_urls[:10]:
            print("  ", img)
        return img_urls
    except Exception as e:
        print("Error scraping Continente search:", e)
    return []

if __name__ == "__main__":
    test_continente_search("maionese")
