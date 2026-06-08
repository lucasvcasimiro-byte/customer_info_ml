import urllib.request
import urllib.parse
import re

def test_bing_unsplash(query):
    try:
        full_query = f"site:unsplash.com {query}"
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(full_query)}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        if not matches:
            matches = re.findall(r'"murl"\s*:\s*"([^"]+)"', html)
            
        print(f"Found {len(matches)} matches on Bing Unsplash for query '{query}':")
        for m in matches[:5]:
            print("  ", m)
        return matches
    except Exception as e:
        print("Error searching Bing Unsplash:", e)
    return None

if __name__ == "__main__":
    test_bing_unsplash("strawberries")
