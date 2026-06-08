from duckduckgo_search import DDGS
import traceback

print("Starting simple DDGS search...")
try:
    with DDGS() as ddgs:
        # Simple search
        results = ddgs.text("python programming", max_results=3)
        print(f"Results type: {type(results)}")
        print(f"Results count: {len(results) if results else 0}")
        if results:
            for idx, r in enumerate(results):
                print(f"Result {idx}: {r}")
except Exception as e:
    print("An exception occurred:")
    traceback.print_exc()
print("Done.")
