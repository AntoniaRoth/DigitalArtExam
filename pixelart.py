from PIL import Image, ImageDraw

# Set the canvas size
canvas_width = 300
canvas_height = 100

# Create a new image with a white background
img = Image.new('RGB', (canvas_width, canvas_height), color='white')
draw = ImageDraw.Draw(img)

# Define pixel colors
black = (0, 0, 0)
red = (255, 0, 0)
gray = (128, 128, 128)

# Draw the car body
draw.rectangle([30, 40, 200, 80], fill=red)
draw.rectangle([70, 20, 130, 40], fill=red)
draw.rectangle([85, 5, 115, 20], fill=black)

# Draw the wheels
draw.ellipse([50, 80, 80, 110], fill=black)
draw.ellipse([150, 80, 180, 110], fill=black)

# Add some details
draw.rectangle([170, 30, 180, 40], fill=gray)
draw.rectangle([165, 40, 185, 45], fill=gray)

# Save the Formula 1 car pixel art
img.save('formula1_car.png')

# Show the pixel art
img.show()
