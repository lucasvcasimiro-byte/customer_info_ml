from duckduckgo_search import DDGS
import sys

sys.stdout.reconfigure(encoding='utf-8')

queries = [
    "continente amendoas",
    "continente abacate",
    "pingo doce abacate",
    "auchan abacate",
    "continente airpods"
]

with DDGS() as ddgs:
    for q in queries:
        print(f"\nQuery: {q}")
        try:
            results = ddgs.text(q, max_results=3)
            if results:
                for idx, r in enumerate(results):
                    print(f"  {idx}: {r.get('title')} -> {r.get('href')}")
            else:
                print("  No results found.")
        except Exception as e:
            print(f"  Error for query {q}: {e}")
