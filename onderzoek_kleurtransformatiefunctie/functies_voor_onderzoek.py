import pickle
from sklearn.linear_model import LinearRegression, Lasso
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from functies_voor_onderzoek import verg

matrix_size = 27  # 27x27 matrix
tussenruimte = 50
directory = "/home/willem/Pictures/Camouflage/ColorCard/converted/"
origineel_pad = directory + "colorCard_zonder_tekst.jpg"


with open('../origineel_kleuren.pkl', 'rb') as file:
    origineel_kleuren = pickle.load(file)
with open('../tshirt_kleuren.pkl', 'rb') as file:
    tshirt_kleuren = pickle.load(file)
with open('../lexmark_kleuren.pkl', 'rb') as file:
    lexmark_kleuren = pickle.load(file)

tshirt = np.array(tshirt_kleuren)
origineel = np.array(origineel_kleuren)
lexmark = np.array(lexmark_kleuren)
#testwaarden = np.array([[20,20,20], [128, 128, 128], [200, 200, 200]])
x = np.sort(tshirt, axis=0)
testwaarden = np.concatenate(([x[0]], [np.median(x, axis=0)], [x[-1]]), axis=0)
alpha = 0.1

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

def vergelijk_kleuren_per_vakje(pad, np_kleuren_float, matrix_size, tussenruimte):
    im = Image.open(pad)
    np_kleuren = np_kleuren_float.astype(np.intc)
    np.clip(np_kleuren, 0, 255)
    b, h = im.size
    dot_size = b / matrix_size - tussenruimte
    im_draw = ImageDraw.Draw(im)
    kleur_index = 0
    for y in range(matrix_size):
        for x in range(matrix_size):
            x_pixel_start = x * (dot_size + tussenruimte) + tussenruimte / 2
            x_pixel_eind = x_pixel_start + dot_size
            y_pixel_start = y * (dot_size + tussenruimte) + tussenruimte / 2
            y_pixel_eind = y_pixel_start + dot_size
            kleur = tuple(np_kleuren[kleur_index])
            im_draw.rectangle([x_pixel_start, y_pixel_start, x_pixel_eind, y_pixel_eind], fill=kleur)
            kleur_index += 1
    im.show()

tshirt_naar_origineel_lineair = LinearRegression().fit(tshirt, origineel)
tshirt_naar_origineel_lineair_r_sq = tshirt_naar_origineel_lineair.score(tshirt, origineel)
print(f"coefficient of determination: {tshirt_naar_origineel_lineair_r_sq}")
print(f"predicted response:\n{tshirt_naar_origineel_lineair.predict(testwaarden)}")
print(tshirt_naar_origineel_lineair.coef_)
print(tshirt_naar_origineel_lineair.intercept_)
pred_tshirt = tshirt_naar_origineel_lineair.predict(tshirt)
# scatterPlotColors(tshirt, pred_tshirt, alpha, 0)

vergelijk_kleuren_per_vakje(origineel_pad, pred_tshirt, matrix_size, tussenruimte)
x=1