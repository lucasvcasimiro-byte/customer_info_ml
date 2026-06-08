import urllib.request
import urllib.parse
import re
import json

def get_ddg_image(query):
    try:
        # Step 1: get vqd token
        url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # Find vqd
        vqd_match = re.search(r'vqd=[\'"]?([^\'&"]+)[\'"]?', html)
        if not vqd_match:
            # Try finding vqd in a different format
            vqd_match = re.search(r'vqd\s*=\s*["\']([^"\']+)["\']', html)
            
        if not vqd_match:
            print("Could not find vqd token for:", query)
            return None
            
        vqd = vqd_match.group(1)
        print(f"Found vqd token: {vqd} for query: {query}")
        
        # Step 2: request images JSON
        # we can use the json endpoint
        image_url = f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(query)}&vqd={vqd}&f=,,,"
        req_img = urllib.request.Request(
            image_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://duckduckgo.com/'
            }
        )
        with urllib.request.urlopen(req_img, timeout=10) as response_img:
            data = json.loads(response_img.read().decode('utf-8'))
            results = data.get('results', [])
            if results:
                # Return the URL of the first image
                return results[0].get('image')
    except Exception as e:
        print(f"Error scraping for '{query}':", e)
    return None

if __name__ == "__main__":
    url = get_ddg_image("asparagus product white background")
    print("Found image URL:", url)
