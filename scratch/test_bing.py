import urllib.request
import urllib.parse
import re

def get_bing_image(query):
    try:
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # Bing images are in murl (media url) in the html
        # Format is often: murl&quot;:&quot;https://...&quot; or similar
        matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        if not matches:
            # Try raw search for img urls
            matches = re.findall(r'"murl"\s*:\s*"([^"]+)"', html)
            
        if matches:
            return matches[0]
    except Exception as e:
        print(f"Error scraping Bing for '{query}':", e)
    return None

if __name__ == "__main__":
    url = get_bing_image("asparagus fruit veg")
    print("Found Bing image URL:", url)
