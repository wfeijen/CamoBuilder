import pickle
from sklearn.linear_model import LinearRegression, Lasso
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
def scatterPlotColors(a, b, alpha, verplaatsing = 5):
    plt.scatter(a[:,0], b[:,0], color='r', alpha=alpha)
    plt.scatter(a[:,1] + verplaatsing , b[:,1], color='g', alpha=alpha)
    plt.scatter(a[:,2] + verplaatsing * 2, b[:,2], color='b', alpha=alpha)
    plt.show()

def scatterPlotColor(a, b, alpha, verplaatsing = 5):
    plt.scatter(a[:,0], b, color='r', alpha=alpha)
    plt.scatter(a[:,1] + verplaatsing , b, color='g', alpha=alpha)
    plt.scatter(a[:,2] + verplaatsing * 2, b, color='b', alpha=alpha)
    plt.show()


def kleurenlijst_naar_int(kleurenlijst):
    kleurenlijst = kleurenlijst.astype(np.intc)
    np.clip(kleurenlijst, 0, 255)
    return kleurenlijst


def vergelijk_plaatje_met_kleuren_range(pad, np_kleuren_float, matrix_size, 
                                        tussenruimte, titel=None):
    im = Image.open(pad)
    np_kleuren = kleurenlijst_naar_int(np_kleuren_float)
    b, h = im.size
    tussenruimte = 2 * tussenruimte
    dot_size = b / matrix_size - tussenruimte
    im_draw = ImageDraw.Draw(im)
    kleur_index = 0
    font = ImageFont.truetype("/home/willem/anaconda3/envs/CamoBuilder/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/cmb10.ttf", 30)
    for y in range(matrix_size):
        for x in range(matrix_size):
            x_pixel_start = x * (dot_size + tussenruimte) + tussenruimte / 2
            x_pixel_eind = x_pixel_start + dot_size
            y_pixel_start = y * (dot_size + tussenruimte) + tussenruimte / 2
            y_pixel_eind = y_pixel_start + dot_size
            kleur = tuple(np_kleuren[kleur_index])
            im_draw.rectangle([x_pixel_start, y_pixel_start, x_pixel_eind, y_pixel_eind], fill=kleur)
            kleur_index += 1
    im.show(title=titel)

def relatief_kleurverschil(a, b):
    verschil = abs(a - b)
    return verschil * 100 // 255


def vergelijk_2_kleurenranges(np_kleuren_float_1, np_kleuren_float_2, 
                              aantal_hokjes, grootte_hokje, tussenruimte, 
                              titel=None):
    np_kleuren_1 = kleurenlijst_naar_int(np_kleuren_float_1)
    np_kleuren_2 = kleurenlijst_naar_int(np_kleuren_float_2)
    im = Image.new(mode="RGB", size=(aantal_hokjes * grootte_hokje, aantal_hokjes * grootte_hokje))
    dot_size = grootte_hokje - tussenruimte
    im_draw = ImageDraw.Draw(im)
    kleur_index = 0
    font = ImageFont.truetype("/home/willem/anaconda3/envs/CamoBuilder/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/cmb10.ttf", grootte_hokje // 4)
    for y in range(aantal_hokjes):
        for x in range(aantal_hokjes):
            x_pixel_start = x * grootte_hokje + tussenruimte / 2
            x_pixel_eind = x_pixel_start + dot_size
            y_pixel_start = y * grootte_hokje + tussenruimte / 2
            y_pixel_eind = y_pixel_start + dot_size
            kleur1 = tuple(np_kleuren_1[kleur_index])
            kleur2 = tuple(np_kleuren_2[kleur_index])
            im_draw.rectangle([x * grootte_hokje, y * grootte_hokje, (x + 1) * grootte_hokje, (y + 1) * grootte_hokje], fill=kleur1)
            im_draw.rectangle([x_pixel_start, y_pixel_start, x_pixel_eind, y_pixel_eind], fill=kleur2)
            im_draw.text((x * grootte_hokje, y * grootte_hokje), str(relatief_kleurverschil(np_kleuren_1[kleur_index][0], np_kleuren_2[kleur_index][0])), font = font)
            im_draw.text((x * grootte_hokje, y * grootte_hokje + grootte_hokje//3), str(relatief_kleurverschil(np_kleuren_1[kleur_index][1], np_kleuren_2[kleur_index][1])), font=font)
            im_draw.text((x * grootte_hokje, y * grootte_hokje + 2 * grootte_hokje//3), str(relatief_kleurverschil(np_kleuren_1[kleur_index][2], np_kleuren_2[kleur_index][2])), font=font)
            kleur_index += 1
    im.show(title=titel)


def vergelijk_3_kleurenranges(np_kleuren_float_1, np_kleuren_float_2, 
                              np_kleuren_float_3, aantal_hokjes, 
                              grootte_hokje, tussenruimte, 
                              titel=None):
    np_kleuren_1 = kleurenlijst_naar_int(np_kleuren_float_1)
    np_kleuren_2 = kleurenlijst_naar_int(np_kleuren_float_2)
    np_kleuren_3 = kleurenlijst_naar_int(np_kleuren_float_3)
    im = Image.new(mode="RGB", size=(aantal_hokjes * grootte_hokje, aantal_hokjes * grootte_hokje))
    dot_size = grootte_hokje - tussenruimte
    im_draw = ImageDraw.Draw(im)
    kleur_index = 0
    font = ImageFont.truetype("/home/willem/anaconda3/envs/CamoBuilder/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/cmb10.ttf", grootte_hokje // 4)
    for y in range(aantal_hokjes):
        for x in range(aantal_hokjes):
            kleur1 = tuple(np_kleuren_1[kleur_index])
            kleur2 = tuple(np_kleuren_2[kleur_index])
            kleur3 = tuple(np_kleuren_3[kleur_index])
            im_draw.rectangle([x * grootte_hokje, y * grootte_hokje, (x + 1) * grootte_hokje, (y + 1) * grootte_hokje], fill=kleur1)
            im_draw.rectangle([x * grootte_hokje + tussenruimte / 2, y * grootte_hokje + tussenruimte / 2, (x + 1) * grootte_hokje + tussenruimte / 2 + dot_size, (y + 1) * grootte_hokje + tussenruimte / 2 + dot_size], fill=kleur2)
            im_draw.rectangle([x * grootte_hokje + tussenruimte, y * grootte_hokje + tussenruimte, (x + 1) * grootte_hokje - tussenruimte + dot_size, (y + 1) * grootte_hokje - tussenruimte + dot_size], fill=kleur3)
            im_draw.text((x * grootte_hokje, y * grootte_hokje), str(relatief_kleurverschil(np_kleuren_1[kleur_index][0], np_kleuren_2[kleur_index][0])), font = font)
            im_draw.text((x * grootte_hokje, y * grootte_hokje + grootte_hokje//3), str(relatief_kleurverschil(np_kleuren_1[kleur_index][1], np_kleuren_2[kleur_index][1])), font=font)
            im_draw.text((x * grootte_hokje, y * grootte_hokje + 2 * grootte_hokje//3), str(relatief_kleurverschil(np_kleuren_1[kleur_index][2], np_kleuren_2[kleur_index][2])), font=font)
            kleur_index += 1
    im.show(title=titel)