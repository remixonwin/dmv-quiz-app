from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    # Create directory if it doesn't exist
    os.makedirs('src/assets', exist_ok=True)
    
    # Create a new image with a white background
    size = (256, 256)
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a blue rectangle
    draw.rectangle([20, 20, 236, 236], fill='#2196F3')
    
    # Draw text
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()
    
    draw.text((128, 128), "DMV", font=font, fill='white', anchor="mm")
    
    # Save as ICO
    image.save('src/assets/app.ico', format='ICO', sizes=[(256, 256)])

if __name__ == '__main__':
    create_app_icon()
