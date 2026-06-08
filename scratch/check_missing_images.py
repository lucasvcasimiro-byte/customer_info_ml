import os
import re

PRODUCTS_JS = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project\dashboard\src\data\storeProducts.js"

def check_missing():
    with open(PRODUCTS_JS, 'r', encoding='utf-8') as f:
        content = f.read()
        
    pattern = r"id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*category:\s*'([^']+)'.*?image:\s*(null|'[^']+')"
    # Wait, let's match line by line
    missing = []
    lines = content.split('\n')
    for line in lines:
        if 'id:' in line:
            id_match = re.search(r"id:\s*'([^']+)'", line)
            name_match = re.search(r"name:\s*'([^']+)'", line)
            cat_match = re.search(r"category:\s*'([^']+)'", line)
            img_match = re.search(r"image:\s*(null|'[^']+')", line)
            
            if id_match and name_match and cat_match:
                prod_id = id_match.group(1)
                name = name_match.group(1)
                cat = cat_match.group(1)
                img = img_match.group(1) if img_match else None
                
                if not img or img == 'null':
                    missing.append({'id': prod_id, 'name': name, 'category': cat})
                    
    print(f"Total missing: {len(missing)}")
    for m in missing:
        print(f"Missing: {m['name']} (ID: {m['id']}, Category: {m['category']})")
    return missing

if __name__ == "__main__":
    check_missing()
