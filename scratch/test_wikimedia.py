import urllib.request
import urllib.parse
import json

def test_wikimedia(query):
    try:
        query_encoded = urllib.parse.quote(query)
        url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrsearch={query_encoded}&gsrnamespace=6&gsrlimit=3&prop=imageinfo&iiprop=url"
        
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) NOVAIMSGroceryStore/1.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        pages = data.get('query', {}).get('pages', {})
        results = []
        for page_id, page_info in pages.items():
            imageinfo = page_info.get('imageinfo', [])
            if imageinfo:
                img_url = imageinfo[0].get('url')
                results.append(img_url)
        
        print(f"Wikimedia matches for '{query}':")
        for r in results:
            print("  ", r)
        return results
    except Exception as e:
        print("Error searching Wikimedia:", e)
    return None

if __name__ == "__main__":
    queries = [
        "mint leaf",
        "green grapes",
        "melon fruit",
        "avocado fruit",
        "flax seed",
        "fresh bread loaf",
        "bramble fruit",
        "blueberries fruit"
    ]
    for q in queries:
        test_wikimedia(q)
        print("-" * 40)
