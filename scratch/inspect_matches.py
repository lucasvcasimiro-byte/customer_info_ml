import json

with open("scratch/scraping_results_v1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total found: {len(data['found'])}")
print(f"Total missing: {len(data['missing'])}")

if data['missing']:
    print("\nMissing items:")
    for p in data['missing']:
        print(f"  - {p['en']}")

print("\nAll matches:")
for idx, item in enumerate(data['found']):
    print(f"{idx+1:3d}. Target: {item['product_name']:28s} | Match: {item['matched_name']:45s} | Source: {item['search_source']}")
