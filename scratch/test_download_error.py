import urllib.request
import urllib.parse
import re

def test():
    url = "https://upload.wikimedia.org/wikipedia/en/thumb/b/be/Minecraft_game_logo_2023.png/250px-Minecraft_game_logo_2023.png"
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            print("Successfully downloaded! Size:", len(data))
    except Exception as e:
        print("Error downloading:", e)

if __name__ == "__main__":
    test()
