#%%
from PIL import Image, ImageDraw
import pickle

matrix_size = 11  # 27x27 matrix
tussenruimte = 30
directory = "/home/willem/Pictures/Camouflage/ColorCard/converted/"

origineel = directory + "kleuren_computer_2.jpg"
tshirt = directory + "kleuren_shirt_2.jpg"

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

#%%
with open('computer_kleuren_2.pkl', 'wb') as file:
    pickle.dump(origineel_kleuren, file)
with open('tshirt_kleuren_2.pkl', 'wb') as file:
    pickle.dump(tshirt_kleuren, file)

#%% Toevoegen aan totaal file
with open('origineel_kleuren_verzamel.pkl', 'rb') as f:
    origineel_kleuren_verzamel = pickle.load(f)
with open('tshirt_kleuren_verzamel.pkl', 'rb') as f:
    tshirt_kleuren_verzamel = pickle.load(f)
#%%
origineel_kleuren_verzamel_nieuw = origineel_kleuren_verzamel + tshirt_kleuren
tshirt_kleuren_verzamel_nieuw = tshirt_kleuren_verzamel + tshirt_kleuren

# %%
with open('origineel_kleuren_verzamel.pkl', 'wb') as file:
    pickle.dump(origineel_kleuren_verzamel_nieuw, file)
with open('tshirt_kleuren_verzamel.pkl', 'wb') as file:
    pickle.dump(tshirt_kleuren_verzamel_nieuw, file)
# %%
