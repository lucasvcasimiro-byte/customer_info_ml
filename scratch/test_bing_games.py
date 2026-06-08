import urllib.request
import urllib.parse
import re

def test_bing_games(name):
    try:
        # Search steamgriddb or steampowered or igdb
        query = f"site:steamgriddb.com {name} grid"
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        if not matches:
            matches = re.findall(r'"murl"\s*:\s*"([^"]+)"', html)
            
        print(f"Games matches for '{name}':")
        for m in matches[:5]:
            print("  ", m)
        return matches
    except Exception as e:
        print("Error searching Bing games:", e)
    return None

if __name__ == "__main__":
    test_bing_games("Portal 2")
    test_bing_games("Half-Life 2")
    test_bing_games("Metroid Fusion")
