import os
from PIL import Image, ImageDraw, ImageFont

def test_generate_card():
    # 400x300 image
    width, height = 400, 300
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a gradient background
    # Vegetais gradient: #134e5e to #71b280
    color1 = (19, 78, 94, 255)
    color2 = (113, 178, 128, 255)
    for y in range(height):
        # Interpolate color
        r = int(color1[0] + (color2[0] - color1[0]) * (y / height))
        g = int(color1[1] + (color2[1] - color1[1]) * (y / height))
        b = int(color1[2] + (color2[2] - color1[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
    # Draw glassmorphism overlay
    draw.rectangle([20, 20, width-20, height-20], fill=(255, 255, 255, 25), outline=(255, 255, 255, 50), width=2)
    
    # Try to load font
    try:
        # Load Windows fonts
        font_path = "C:\\Windows\\Fonts\\calibrib.ttf"
        emoji_font_path = "C:\\Windows\\Fonts\\seguiemj.ttf"
        
        font = ImageFont.truetype(font_path, 32)
        font_sub = ImageFont.truetype(font_path, 18)
        emoji_font = ImageFont.truetype(emoji_font_path, 80)
    except IOError:
        font = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        emoji_font = ImageFont.load_default()
        
    # Draw emoji icon in center
    # Asparagus emoji: 🥦 or 🥬 or 🎋
    emoji_char = "🥦"
    
    # Get text width/height
    try:
        w_emoji, h_emoji = draw.textsize(emoji_char, font=emoji_font) if hasattr(draw, 'textsize') else (80, 80)
    except:
        w_emoji, h_emoji = 80, 80
        
    draw.text((width/2, height/2 - 20), emoji_char, font=emoji_font, fill=(255, 255, 255, 255), anchor="mm")
    
    # Draw product name
    draw.text((width/2, height/2 + 60), "ASPARAGUS", font=font, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((width/2, height/2 + 95), "VEGETAIS", font=font_sub, fill=(255, 255, 255, 180), anchor="mm")
    
    os.makedirs("scratch/test_imgs", exist_ok=True)
    image.save("scratch/test_imgs/asparagus_card.png", "PNG")
    print("Test card saved to scratch/test_imgs/asparagus_card.png")

if __name__ == "__main__":
    test_generate_card()
