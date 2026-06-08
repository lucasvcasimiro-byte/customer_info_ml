import urllib.request
import urllib.parse
import json

def test_off(query):
    try:
        query_encoded = urllib.parse.quote(query)
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query_encoded}&search_simple=1&action=process&json=1&page_size=3"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'NOVAIMSGroceryStoreSimulator/1.0 (afonso@novaims.unl.pt)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        products = data.get('products', [])
        print(f"Open Food Facts matches for '{query}':")
        for p in products:
            img = p.get('image_front_url') or p.get('image_url')
            if img:
                print("  Product:", p.get('product_name'), "->", img)
    except Exception as e:
        print("Error searching Open Food Facts:", e)

if __name__ == "__main__":
    test_off("mayonnaise")
    test_off("ketchup")
    test_off("spaghetti")
