import noise
from PIL import Image

# Create a new image with a size of 400x400 pixels
image = Image.new("RGB", (400, 400))

# Generate random Perlin noise patterns for the camouflage
for x in range(400):
    for y in range(400):
        n = noise.snoise2(x / 100.0, y / 100.0, base=0)
        if n < 0:
            color = (0, int(128 * (1 + n)), 0)
        else:
            color = (int(128 * (1 - n)), int(128 * (1 - n)), 0)
        image.putpixel((x, y), color)

# Save the image as a JPEG file
image.save("woodland-camouflage.jpg", "JPEG")


