import pickle
from sklearn.linear_model import LinearRegression, Lasso
import numpy as np
from functies_voor_onderzoek import vergelijk_plaatje_met_kleuren_range, scatterPlotColors, scatterPlotColor

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
alpha = 0.01

tshirt_naar_origineel_lasso = Lasso().fit(tshirt, origineel)
tshirt_naar_origineel_lasso_r_sq = tshirt_naar_origineel_lasso.score(tshirt, origineel)
print(f"coefficient of determination lasso: {tshirt_naar_origineel_lasso_r_sq}")
print(f"predicted response lasso:\n{tshirt_naar_origineel_lasso.predict(testwaarden)}")
print(tshirt_naar_origineel_lasso.coef_)
print(tshirt_naar_origineel_lasso.intercept_)
pred_tshirt = tshirt_naar_origineel_lasso.predict(tshirt)
# scatterPlotColors(tshirt, pred_tshirt, alpha, 0)

vergelijk_plaatje_met_kleuren_range(origineel_pad, pred_tshirt, matrix_size, tussenruimte)
x="1lI0Oo"