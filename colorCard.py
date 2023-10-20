#%%
from math import sqrt, ceil
from PIL import Image, ImageDraw, ImageCms, ImageFont

#%%

file_name_met_tekst = '/home/willem/Pictures/Camouflage/camoBuilder/camoOutput/colorCard_tekst.jpg'
file_name_zonder_tekst = '/home/willem/Pictures/Camouflage/camoBuilder/camoOutput/colorCard_zonder_tekst.jpg'
N = 9
square_size = 200
font_size = 28
def calculate_text_color(color):
    r, g, b = color
    brightness = sqrt(0.299 * r**2 + 0.587 * g**2 + 0.114 * b**2)
    text_color = "#000000" if brightness > 128 else "#FFFFFF"
    return text_color

def maak_color_card(N, square_size, font_size, tekst=False):
    rootN = int(ceil(sqrt(N)))
    factor = 255 / (N - 1)
    count = range(N)

    image_width = N * rootN * square_size
    image_height = N * rootN * square_size

    image = Image.new("RGB", (image_width, image_height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("/usr/share/fonts/truetype/tlwg/TlwgTypewriter-Bold.ttf", size=font_size)
    for r in count:
        for g in count:
            for b in count:
                color = (int(r*factor), int(g*factor),int(b*factor))
                hex_code = "#%02x%02x%02x" % color
                decimal_code = "\n".join([str(c) for c in color])
                decimal_code = f"{decimal_code}"
                x1 = (r + b%rootN * N) * square_size
                y1 = (g + b//rootN * N) * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                draw.rectangle([(x1, y1), (x2, y2)], fill=color)
                if tekst:
                    draw.text((x1 + 80, y1 + 50), decimal_code, fill=calculate_text_color(color), font=font, align="center")
    return image


profile = ImageCms.createProfile("sRGB")

image = maak_color_card(N=N, square_size=square_size, font_size=font_size,tekst=True)
image.show()
image.save(file_name_met_tekst, icc_profile=ImageCms.ImageCmsProfile(profile).tobytes())
image = maak_color_card(N=N, square_size=square_size, font_size=font_size,tekst=False)
image.save(file_name_zonder_tekst, icc_profile=ImageCms.ImageCmsProfile(profile).tobytes())




