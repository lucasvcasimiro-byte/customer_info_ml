import urllib.request
import urllib.parse
import json

def test_wiki_pageimages(titles):
    titles_str = "|".join(titles)
    titles_encoded = urllib.parse.quote(titles_str)
    
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={titles_encoded}&prop=pageimages&format=json&pithumbsize=400"
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'NOVAIMSGroceryStoreSimulator/1.0 (afonso@novaims.unl.pt)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        pages = data.get('query', {}).get('pages', {})
        print("Wikipedia PageImages results:")
        for page_id, page_info in pages.items():
            title = page_info.get('title')
            thumbnail = page_info.get('thumbnail', {})
            source = thumbnail.get('source')
            print(f"  {title} -> {source}")
    except Exception as e:
        print("Error fetching pageimages:", e)

if __name__ == "__main__":
    # Test real games and electronics
    test_wiki_pageimages([
        "Minecraft", 
        "Portal 2", 
        "Half-Life 2", 
        "Metroid Fusion", 
        "AirPods", 
        "IPad", 
        "IMac"
    ])
