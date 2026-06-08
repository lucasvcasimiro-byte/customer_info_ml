import os
import json
import re

# Directory paths
images_dir = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project\dashboard\public\product_images"
store_products_js = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project\dashboard\src\data\storeProducts.js"

# 1. Get all filenames in the product_images folder
files = os.listdir(images_dir)
print(f"Found {len(files)} files in product_images folder.")

# 2. Parse the PRODUCTS array in storeProducts.js
with open(store_products_js, 'r', encoding='utf-8') as f:
    js_content = f.read()

def normalize_name(s):
    # Remove whitespace, non-alphanumeric except maybe & which becomes 'and', lower case
    s = s.lower()
    s = s.replace('&', 'and')
    s = s.replace(':', '')
    s = s.replace('-', '')
    s = s.replace('_', '')  # Remove underscores too to handle canned_tuna -> cannedtuna
    s = re.sub(r'\s+', '', s)
    return s

# Map normalized names of files to their actual filename
file_map = {}
for filename in files:
    base, ext = os.path.splitext(filename)
    if base.endswith('_foto'):
        base_name = base[:-5] # remove '_foto'
    else:
        base_name = base
    
    norm = normalize_name(base_name)
    file_map[norm] = filename

# Special cases mapping product normalized IDs to image filenames
special_cases = {
    'shrimp': 'shirmp_foto.jpg',
    'shirmp': 'shirmp_foto.jpg',
    'cottagecheese': 'cottagechese_foto.jpg',
    'energybar': 'energybar_foto.png',
    'glutenfreebar': 'glutenfreebar_foto.jpg',
    'gums': 'gums_foto.jpg',
    'salad': 'salad_foto.jpg',
    'soup': 'soup_foto.jpg',
    'zucchini': 'Zucchini_foto.webp',
    'halflife2': 'hardlife2_foto.jpg',
    'halflifealyx': 'hardlifealyx_foto.jpg',
    'wholewheatflour': 'wholewheatflour_foto.jpg',
    'wholeweatflour': 'wholewheatflour_foto.jpg',
    'mixedvegetables': 'mixedvegetables_foto.webp',
    'vegetablesmix': 'mixedvegetables_foto.webp',
    'frozenvegetables': 'frozenvegetable_foto.webp',
    'frozenvegetable': 'frozenvegetable_foto.webp',
    'tiktokstreamingkit': 'tiktokstreamingkit_foto.webp',
    'gadgetfortiktokstreaming': 'tiktokstreamingkit_foto.webp',
    'bluetoothheadphones': 'BTheadphones_foto.webp',
    'btheadphones': 'BTheadphones_foto.webp',
    'candybars': 'candybar_foto.jpg',
    'candybar': 'candybar_foto.jpg',
    'extradarkchocolate': 'darkchocolate_foto.jpg',
    'darkchocolate': 'darkchocolate_foto.jpg',
    'antioxydantjuice': 'antioxidantjuice_foto.webp',
    'antioxidantjuice': 'antioxidantjuice_foto.webp',
    'mintgreentea': 'minttea_foto.jpg',
    'minttea': 'minttea_foto.jpg',
    'ratchetclank': 'ratchetclank_foto.jpg',
    'ratchetclank2': 'ratchetclank2_foto.jpg',
    'ratchetclank3': 'ratchetclank3_foto.jpg',
    'ratchetandclank': 'ratchetclank_foto.jpg',
    'ratchetandclank2': 'ratchetclank2_foto.jpg',
    'ratchetandclank3': 'ratchetclank3_foto.jpg',
    # Unmatched items
    'milk': 'milk1L_foto.jpg',
    'nonfatmilk': 'nonfatmilk1L_foto.jpg',
    'lowfatyogurt': 'lowflatyogurt_foto.jpg',
    'escalope': 'escalopes_foto.jpg',
    'cannedtuna': 'cannedtuna_foto.jpg',
    'soda': 'soda1.5L_foto.jpg',
    'beer': 'beer_foto.jpg',
    'babiesfood': 'babyfood_foto.webp',
}

# 3. Update the js_content line-by-line
lines = js_content.split('\n')
updated_lines = []
matched_count = 0
unmatched_ids = []

for line in lines:
    match = re.search(r"id:\s*['\"]([^'\"]+)['\"]", line)
    if match:
        prod_id = match.group(1)
        norm_id = normalize_name(prod_id)
        
        # Check special cases first
        filename = None
        if norm_id in special_cases:
            filename = special_cases[norm_id]
        elif norm_id in file_map:
            filename = file_map[norm_id]
        
        if filename:
            new_image_val = f"'/product_images/{filename}'"
            line_replaced = re.sub(r"image:\s*[^,\}]+", f"image: {new_image_val}", line)
            updated_lines.append(line_replaced)
            matched_count += 1
        else:
            unmatched_ids.append((prod_id, norm_id))
            updated_lines.append(line)
    else:
        updated_lines.append(line)

print(f"Updated {matched_count} products.")
if unmatched_ids:
    print(f"Unmatched product IDs ({len(unmatched_ids)}):")
    for prod_id, norm_id in unmatched_ids:
        print(f"  - {prod_id} (normalized: {norm_id})")
else:
    print("All products matched successfully!")

# Write updated file
with open(store_products_js, 'w', encoding='utf-8') as f:
    f.write('\n'.join(updated_lines))
print("File storeProducts.js has been updated.")
