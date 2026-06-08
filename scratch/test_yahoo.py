import urllib.request
import urllib.parse
import re

def get_yahoo_image(query):
    try:
        url = f"https://images.search.yahoo.com/search/images?p={urllib.parse.quote(query)}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # Yahoo images are often in a JSON-like string or in img tags
        # Let's search for "ou":"http..." or image URLs in the html
        # Let's find matches for "iurl":"(http[^"]+)"
        matches = re.findall(r'"iurl"\s*:\s*"([^"]+)"', html)
        if not matches:
            # Try finding "imgurl":"(http[^"]+)" or similar
            matches = re.findall(r'"imgurl"\s*:\s*"([^"]+)"', html)
        if not matches:
            # Let's try raw image links in img tags or data-src
            matches = re.findall(r'src="([^"]+)"', html)
            # Filter for actual image links
            matches = [m for m in matches if m.startswith('http') and not 'yimg.com' in m]
            
        if matches:
            return matches[0].replace('\\/', '/')
    except Exception as e:
        print(f"Error scraping Yahoo for '{query}':", e)
    return None

if __name__ == "__main__":
    url = get_yahoo_image("asparagus fruit veg")
    print("Found Yahoo image URL:", url)
