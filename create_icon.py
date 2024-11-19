from PIL import Image, ImageDraw, ImageFont
import os

def create_dmv_icon():
    # Create directory if it doesn't exist
    os.makedirs('src/assets', exist_ok=True)
    
    # Create a new image with a white background
    size = (256, 256)
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a blue circle
    circle_bbox = [20, 20, 236, 236]
    draw.ellipse(circle_bbox, fill='#1E88E5')
    
    # Add text
    text = "DMV"
    # Try to use Arial, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()
    
    # Get text size
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate center position
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text in white
    draw.text((x, y), text, font=font, fill='white')
    
    # Save as ICO
    image.save('src/assets/app_icon.ico', format='ICO', sizes=[(256, 256)])

if __name__ == '__main__':
    create_dmv_icon()
