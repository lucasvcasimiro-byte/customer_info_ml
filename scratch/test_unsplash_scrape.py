import urllib.request
import re

def test_unsplash(query):
    try:
        url = f"https://unsplash.com/s/photos/{urllib.parse.quote(query)}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # Unsplash image URLs typically look like: https://images.unsplash.com/photo-...
        # We want the ones that look like source images, e.g. with auto=format&fit=crop&w=...
        # Let's search for matches
        matches = re.findall(r'(https://images.unsplash.com/photo-[^?"]+)', html)
        print(f"Found {len(matches)} matches on Unsplash for query '{query}':")
        for m in matches[:5]:
            print("  ", m)
        return matches
    except Exception as e:
        print("Error scraping Unsplash:", e)
    return None

import urllib.parse
if __name__ == "__main__":
    test_unsplash("strawberries")
