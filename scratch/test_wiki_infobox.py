import urllib.request
import urllib.parse
import re

def test_wiki_infobox(title):
    try:
        # Wikipedia article URL
        title_clean = title.replace(" ", "_")
        url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title_clean)}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'NOVAIMSGroceryStoreSimulator/1.0 (afonso@novaims.unl.pt)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # Find the infobox table: <table class="infobox ..."> ... </table>
        # Look for the first image inside it
        infobox_match = re.search(r'<table class="infobox[^">]*">(.*?)</table>', html, re.DOTALL)
        if infobox_match:
            infobox_html = infobox_match.group(1)
            # Find image tags: src="//upload.wikimedia.org/..."
            img_matches = re.findall(r'src="([^"]+)"', infobox_html)
            if img_matches:
                img_url = img_matches[0]
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                print(f"Infobox image for '{title}' -> {img_url}")
                return img_url
        print(f"No infobox image found for '{title}'")
    except Exception as e:
        print(f"Error fetching infobox for '{title}':", e)
    return None

if __name__ == "__main__":
    test_wiki_infobox("Portal 2")
    test_wiki_infobox("Minecraft")
    test_wiki_infobox("Metroid Fusion")
    test_wiki_infobox("AirPods")
