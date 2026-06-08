import json

with open("scratch/scraping_results_v1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("First 70 matches:")
for idx, item in enumerate(data['found'][:70]):
    print(f"{idx+1:3d}. Target: {item['product_name']:28s} | Match: {item['matched_name']:45s} | Source: {item['search_source']}")
