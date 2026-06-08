import urllib.request
import urllib.parse
import re
import os

def download_image(query, filepath):
    try:
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            
        matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        if not matches:
            matches = re.findall(r'"murl"\s*:\s*"([^"]+)"', html)
            
        if not matches:
            print("No matches for query:", query)
            return False
            
        # Try downloading one by one until one succeeds
        for img_url in matches[:5]:
            try:
                print(f"Trying download from {img_url} for query: {query}")
                req_img = urllib.request.Request(
                    img_url,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
                )
                with urllib.request.urlopen(req_img, timeout=4) as img_resp:
                    # check content length or type if possible, or just write it
                    data = img_resp.read()
                    if len(data) > 1000: # not empty or error page
                        with open(filepath, 'wb') as f:
                            f.write(data)
                        print(f"Successfully downloaded to {filepath} ({len(data)} bytes)")
                        return True
            except Exception as e:
                print(f"Failed to download from {img_url}: {e}")
    except Exception as e:
        print(f"Error scraping Bing for '{query}': {e}")
    return False

if __name__ == "__main__":
    os.makedirs("scratch/test_imgs", exist_ok=True)
    download_image("asparagus fruit veg product", "scratch/test_imgs/asparagus.jpg")
