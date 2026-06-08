import urllib.request

def test():
    try:
        url = "https://source.unsplash.com/featured/?asparagus"
        # We need a User-Agent to avoid being blocked
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        response = urllib.request.urlopen(req, timeout=10)
        print("Connected, final URL after redirects:", response.geturl())
        print("Content-type:", response.info().get_content_type())
    except Exception as e:
        print("Error connecting to Unsplash source:", e)

if __name__ == "__main__":
    test()
