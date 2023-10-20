from PIL import Image, ImageDraw
import pickle

matrix_size = 27  # 27x27 matrix
tussenruimte = 30
directory = "/home/willem/Pictures/Camouflage/ColorCard/converted/"

origineel = directory + "colorCard_zonder_tekst.jpg"
tshirt = directory + "tshirt_zon_20230930_105940_000046A-8.0_E-1600_I-400_D7500.jpg"
lexmark = directory + "Lexmark_20230922_094924_000717A-8.0_E-50_I-400_D7500.jpg"

def haal_kleuren_per_vakje(pad, matrix_size, tussenruimte):
    im = Image.open(pad)
    b, h = im.size
    dot_size = b / matrix_size - tussenruimte
    im_draw = ImageDraw.Draw(im)
    averageColors = []
    for y in range(matrix_size):
        for x in range(matrix_size):
            x_pixel_start = x * (dot_size + tussenruimte) + tussenruimte / 2
            x_pixel_eind = x_pixel_start + dot_size
            y_pixel_start = y * (dot_size + tussenruimte) + tussenruimte / 2
            y_pixel_eind = y_pixel_start + dot_size
            region = im.crop((x_pixel_start, y_pixel_start, x_pixel_eind, y_pixel_eind))
            average_color = tuple(map(int, region.resize((1, 1), Image.Resampling.LANCZOS).getpixel((0, 0))))
            im_draw.rectangle([x_pixel_start, y_pixel_start, x_pixel_start + dot_size, y_pixel_start + dot_size], fill=average_color)
            averageColors.append(average_color)
    im.show()
    return averageColors

origineel_kleuren = haal_kleuren_per_vakje(origineel, matrix_size, tussenruimte)
tshirt_kleuren = haal_kleuren_per_vakje(tshirt, matrix_size, tussenruimte)
lexmark_kleuren = haal_kleuren_per_vakje(lexmark, matrix_size, tussenruimte)

with open('origineel_kleuren.pkl', 'wb') as file:
    pickle.dump(origineel_kleuren, file)
with open('tshirt_kleuren.pkl', 'wb') as file:
    pickle.dump(tshirt_kleuren, file)
with open('lexmark_kleuren.pkl', 'wb') as file:
    pickle.dump(lexmark_kleuren, file)
