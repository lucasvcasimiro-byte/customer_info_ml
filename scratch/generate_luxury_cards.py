import os
import re
import shutil
from PIL import Image, ImageDraw, ImageFont

# Paths
BASE_DIR = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project"
PRODUCTS_JS = os.path.join(BASE_DIR, "dashboard", "src", "data", "storeProducts.js")
PUBLIC_IMG_DIR = os.path.join(BASE_DIR, "dashboard", "public", "product_images")

# Categories and their corresponding luxury gradients (RGB)
CATEGORY_THEMES = {
    'Vegetais': {
        'grad_start': (12, 74, 52),     # Deep Emerald
        'grad_end': (40, 140, 95),      # Light Green
        'accent': (232, 245, 233),      # Soft mint
        'label': 'V E G E T A I S'
    },
    'Fruta': {
        'grad_start': (114, 28, 36),    # Cherry Red
        'grad_end': (219, 68, 85),      # Sweet Coral
        'accent': (255, 235, 238),      # Soft Rose
        'label': 'F R U T A'
    },
    'Padaria & Laticínios': {
        'grad_start': (122, 68, 12),    # Warm Cinnamon
        'grad_end': (220, 150, 60),     # Baked Golden
        'accent': (255, 248, 225),      # Cream
        'label': 'P A D A R I A  &  L A T I C Í N I O S'
    },
    'Carne & Peixe': {
        'grad_start': (100, 15, 15),    # Maroon
        'grad_end': (180, 50, 30),      # Crimson
        'accent': (255, 235, 230),      # Pale Pink
        'label': 'C A R N E  &  P E I X E'
    },
    'Bebidas': {
        'grad_start': (10, 40, 80),     # Deep Navy
        'grad_end': (30, 110, 180),     # Ocean Blue
        'accent': (224, 247, 250),      # Cool Cyan
        'label': 'B E B I D A S'
    },
    'Cereais & Snacks': {
        'grad_start': (140, 50, 10),    # Toasted Orange
        'grad_end': (230, 100, 30),     # Bright Apricot
        'accent': (255, 243, 224),      # Light Peach
        'label': 'C E R E A I S  &  S N A C K S'
    },
    'Animais & Bebé': {
        'grad_start': (74, 20, 110),    # Dark Indigo
        'grad_end': (142, 68, 173),     # Soft Violet
        'accent': (243, 229, 245),      # Lavender
        'label': 'A N I M A I S  &  B E B É'
    },
    'Despensa': {
        'grad_start': (45, 45, 45),     # Charcoal
        'grad_end': (90, 85, 80),       # Slate/Clay
        'accent': (245, 245, 245),      # Light Grey
        'label': 'D E S P E N S A'
    },
    'Higiene': {
        'grad_start': (10, 80, 80),     # Deep Teal
        'grad_end': (35, 150, 120),     # Clean Sage
        'accent': (224, 242, 241),      # Water Mint
        'label': 'H I G I E N E'
    },
    'Electrónica': {
        'grad_start': (15, 17, 26),     # Cyber Obsidian
        'grad_end': (40, 45, 75),       # Matte Navy
        'accent': (230, 242, 255),      # Light Slate
        'label': 'E L E C T R Ó N I C A'
    },
    'Gaming': {
        'grad_start': (30, 15, 60),     # Dark Purple
        'grad_end': (110, 30, 135),     # Violet Neon
        'accent': (235, 200, 255),      # Bright Violet
        'label': 'G A M I N G'
    }
}

def clean_id(prod_id):
    cleaned = prod_id.lower()
    cleaned = re.sub(r'[\s\-:&/]+', '_', cleaned)
    cleaned = re.sub(r'_+', '_', cleaned)
    return cleaned.strip('_')

def generate_luxury_card(product):
    name = product['name'].upper()
    category = product['category']
    prod_id = product['id']
    
    # Get theme
    theme = CATEGORY_THEMES.get(category, {
        'grad_start': (20, 20, 20),
        'grad_end': (60, 60, 60),
        'accent': (255, 255, 255),
        'label': category.upper()
    })
    
    width, height = 400, 300
    # Create RGBA image
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw linear gradient from top-left to bottom-right
    color1 = theme['grad_start']
    color2 = theme['grad_end']
    for y in range(height):
        # Interpolation factor
        factor = y / height
        r = int(color1[0] + (color2[0] - color1[0]) * factor)
        g = int(color1[1] + (color2[1] - color1[1]) * factor)
        b = int(color1[2] + (color2[2] - color1[2]) * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
    # Draw premium card borders
    draw.rectangle([12, 12, width-12, height-12], outline=(255, 255, 255, 35), width=1)
    draw.rectangle([16, 16, width-16, height-16], outline=(255, 255, 255, 20), width=1)
    
    # Load fonts
    try:
        font_serif = "C:\\Windows\\Fonts\\georgiab.ttf"
        font_serif_italic = "C:\\Windows\\Fonts\\georgiai.ttf"
        font_sans = "C:\\Windows\\Fonts\\calibrib.ttf"
        font_sans_reg = "C:\\Windows\\Fonts\\calibri.ttf"
        
        # Adaptive font sizing for long product names
        if len(name) > 20:
            name_size = 22
        elif len(name) > 14:
            name_size = 26
        else:
            name_size = 32
            
        font_name = ImageFont.truetype(font_serif, name_size)
        font_bg_initial = ImageFont.truetype(font_serif_italic, 85)
        font_label = ImageFont.truetype(font_sans, 10)
        font_badge = ImageFont.truetype(font_sans_reg, 9)
    except IOError:
        font_name = ImageFont.load_default()
        font_bg_initial = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        
    # Draw a big elegant ghost initial letter in the background
    initial = name[0] if name else "?"
    draw.text((width/2, height/2 - 38), initial, font=font_bg_initial, fill=(255, 255, 255, 18), anchor="mm")
    
    # Draw product category label at the top
    draw.text((width/2, 40), theme['label'], font=font_label, fill=theme['accent'] + (180,), anchor="mm")
    
    # Draw product name centered
    draw.text((width/2, height/2 + 25), name, font=font_name, fill=(255, 255, 255, 255), anchor="mm")
    
    # Draw a divider line
    draw.line([(width/2 - 40, height/2 + 65), (width/2 + 40, height/2 + 65)], fill=(255, 255, 255, 45), width=1)
    
    # Draw premium seal/subtext at the bottom
    draw.text((width/2, height/2 + 88), "NOVAIMS PREMIUM SELECTION", font=font_badge, fill=(255, 255, 255, 130), anchor="mm")
    
    # Save the card
    cleaned = clean_id(prod_id)
    filename = f"product_{cleaned}.png"
    filepath = os.path.join(PUBLIC_IMG_DIR, filename)
    image.save(filepath, "PNG")
    return prod_id, filename

def parse_products():
    products = []
    with open(PRODUCTS_JS, 'r', encoding='utf-8') as f:
        content = f.read()
        
    pattern = r"\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*category:\s*'([^']+)'"
    matches = re.findall(pattern, content)
    for match in matches:
        products.append({
            'id': match[0],
            'name': match[1],
            'category': match[2]
        })
    return products

def update_products_js(downloaded_map):
    with open(PRODUCTS_JS, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        match = re.search(r"id:\s*'([^']+)'", line)
        if match:
            prod_id = match.group(1)
            filename = downloaded_map.get(prod_id)
            
            # Clear any old image mapping completely
            line = re.sub(r"image:\s*(null|'[^']+'|`[^`]+`),?\s*", "", line)
            
            if filename:
                line = re.sub(
                    r"(price:\s*[\d.]+)",
                    f"image: '/product_images/{filename}', \\1",
                    line
                )
            else:
                line = re.sub(
                    r"(price:\s*[\d.]+)",
                    "image: null, \\1",
                    line
                )
        new_lines.append(line)
        
    with open(PRODUCTS_JS, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
    print("Updated storeProducts.js with generated card paths.")

def main():
    os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
    products = parse_products()
    
    print(f"Generating premium card assets for {len(products)} products...")
    downloaded_map = {}
    
    for p in products:
        prod_id, filename = generate_luxury_card(p)
        downloaded_map[prod_id] = filename
        
    print(f"Successfully generated {len(downloaded_map)} premium cards.")
    update_products_js(downloaded_map)

if __name__ == "__main__":
    main()
