from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with a blue background
img = Image.new('RGB', (32, 32), color='#4F46E5')
d = ImageDraw.Draw(img)

# Add text
try:
    font = ImageFont.truetype("arial.ttf", 16)
except:
    font = ImageFont.load_default()

# Draw "AI" text in white
text = "AI"
text_bbox = d.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
x = (32 - text_width) / 2
y = (32 - text_height) / 2
d.text((x, y), text, font=font, fill='white')

# Save the image
img.save('favicon.png') 