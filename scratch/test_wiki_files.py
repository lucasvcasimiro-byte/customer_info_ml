import urllib.request
import urllib.parse
import json

def test_wiki_titles(names):
    # Construct title strings
    titles = "|".join([f"File:{n}.jpg" for n in names])
    titles_encoded = urllib.parse.quote(titles)
    
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={titles_encoded}&prop=imageinfo&iiprop=url&format=json"
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'NOVAIMSGroceryStoreSimulator/1.0 (afonso@novaims.unl.pt)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        pages = data.get('query', {}).get('pages', {})
        print("Wikimedia exact titles results:")
        for page_id, page_info in pages.items():
            title = page_info.get('title')
            imageinfo = page_info.get('imageinfo', [])
            if imageinfo:
                print(f"  {title} -> {imageinfo[0].get('url')}")
            else:
                print(f"  {title} -> NOT FOUND")
    except Exception as e:
        print("Error fetching exact titles:", e)

if __name__ == "__main__":
    test_wiki_titles(["Asparagus", "Spinach", "Carrots", "Avocado", "Blueberries", "Tomato", "Melon"])
