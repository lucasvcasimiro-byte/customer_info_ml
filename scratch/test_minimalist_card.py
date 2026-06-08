import os
from PIL import Image, ImageDraw, ImageFont

def generate_minimalist_card():
    width, height = 400, 300
    # Create base image in RGBA
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Gradient: elegant deep purple to dark blue (Gaming/Premium vibe)
    color1 = (20, 24, 42, 255)
    color2 = (30, 41, 75, 255)
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * (y / height))
        g = int(color1[1] + (color2[1] - color1[1]) * (y / height))
        b = int(color1[2] + (color2[2] - color1[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
    # Draw a thin, elegant double-border
    draw.rectangle([12, 12, width-12, height-12], outline=(255, 255, 255, 40), width=1)
    draw.rectangle([16, 16, width-16, height-16], outline=(255, 255, 255, 25), width=1)
    
    # Load fonts
    try:
        font_name = "C:\\Windows\\Fonts\\georgiab.ttf" # Bold Georgia (elegant serif)
        font_sub_name = "C:\\Windows\\Fonts\\calibri.ttf" # Calibri for sub
        
        font_large = ImageFont.truetype(font_name, 36)
        font_sub = ImageFont.truetype(font_sub_name, 14)
        font_tag = ImageFont.truetype(font_sub_name, 12)
    except IOError:
        font_large = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        
    # Draw product initials or icon placeholder
    draw.text((width/2, height/2 - 40), "S", font=ImageFont.truetype("C:\\Windows\\Fonts\\georgiai.ttf", 64), fill=(255, 255, 255, 30), anchor="mm")
    
    # Draw product name (centered, elegant white)
    draw.text((width/2, height/2 + 20), "STRAWBERRIES", font=font_large, fill=(255, 255, 255, 255), anchor="mm")
    
    # Draw category
    draw.text((width/2, height/2 + 65), "F R U T A", font=font_sub, fill=(243, 156, 18, 220), anchor="mm") # Elegant orange/gold accent
    
    # Draw a bottom decorative line
    draw.line([(width/2 - 30, height/2 + 90), (width/2 + 30, height/2 + 90)], fill=(255, 255, 255, 60), width=1)
    
    os.makedirs("scratch/test_imgs", exist_ok=True)
    image.save("scratch/test_imgs/strawberries_card.png", "PNG")
    print("Minimalist card saved!")

if __name__ == "__main__":
    generate_minimalist_card()
