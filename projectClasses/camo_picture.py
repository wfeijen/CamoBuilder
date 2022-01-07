from PIL import Image
import numpy as np

from projectClasses.Utilities import replace_with_dict


def vul_bolletje(canvas, kleur_waarde, x, y):
    ybase = y * 3
    xbase = x * 4
    if (y % 2) == 0:
        xbase = xbase + 2

    canvas[xbase, ybase + 1] = kleur_waarde
    canvas[xbase, ybase + 2] = kleur_waarde
    canvas[xbase + 1, ybase] = kleur_waarde
    canvas[xbase + 1, ybase + 1] = kleur_waarde
    canvas[xbase + 1, ybase + 2] = kleur_waarde
    canvas[xbase + 1, ybase + 3] = kleur_waarde
    canvas[xbase + 2, ybase] = kleur_waarde
    canvas[xbase + 2, ybase + 1] = kleur_waarde
    canvas[xbase + 2, ybase + 2] = kleur_waarde
    canvas[xbase + 2, ybase + 3] = kleur_waarde
    canvas[xbase + 3, ybase + 1] = kleur_waarde
    canvas[xbase + 3, ybase + 2] = kleur_waarde


def createCamoPicture(canvas, getal_naar_kleur):
    w, h = canvas.shape
    groot_canvas = np.zeros((w * 4 + 2, h * 3 + 1))
    for ix in range(w):
        for iy in range(h):
            vul_bolletje(canvas=groot_canvas, kleur_waarde=canvas[ix, iy], x=ix, y=iy)
    image_array = np.uint8(replace_with_dict(groot_canvas, getal_naar_kleur))
    img = Image.fromarray(image_array)
    img.show()
    return(img)