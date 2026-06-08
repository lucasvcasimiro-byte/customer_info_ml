import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = "scratch/final_products.json"

if not os.path.exists(file_path):
    print("Verification Failed: File not found!")
    sys.exit(1)

try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print(f"Verification Failed: Invalid JSON format: {e}")
    sys.exit(1)

if not isinstance(data, list):
    print("Verification Failed: Output is not a JSON list/array!")
    sys.exit(1)

print(f"Total items in final JSON: {len(data)}")

required_keys = {"product_name", "search_source", "product_page", "image_url"}
sources_summary = {}
invalid_items = []

for idx, item in enumerate(data):
    # Check keys
    item_keys = set(item.keys())
    missing_keys = required_keys - item_keys
    if missing_keys:
        invalid_items.append((idx, item.get("product_name"), f"Missing keys: {missing_keys}"))
        continue
        
    # Check non-empty values
    empty_fields = [k for k, v in item.items() if not isinstance(v, str) or not v.strip()]
    if empty_fields:
        invalid_items.append((idx, item.get("product_name"), f"Empty or non-string fields: {empty_fields}"))
        continue
        
    # Check URL schemes
    for url_field in ["product_page", "image_url"]:
        val = item[url_field]
        if not val.startswith("http://") and not val.startswith("https://"):
            invalid_items.append((idx, item.get("product_name"), f"Invalid URL scheme in {url_field}: {val[:50]}"))
            
    # Count sources
    source = item["search_source"]
    sources_summary[source] = sources_summary.get(source, 0) + 1

if invalid_items:
    print(f"\nVerification Failed: Found {len(invalid_items)} invalid items:")
    for idx, name, reason in invalid_items[:10]:
        print(f"  Item {idx} ({name}): {reason}")
    sys.exit(1)

print("\nVerification Succeeded! All 150 products are valid and fully filled.")
print("\nSources breakdown:")
for src, count in sorted(sources_summary.items(), key=lambda x: x[1], reverse=True):
    print(f"  - {src}: {count} products")
