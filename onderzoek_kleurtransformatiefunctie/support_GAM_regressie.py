import pickle
from sklearn.linear_model import LinearRegression, Lasso
import numpy as np
from functies_voor_onderzoek import vergelijk_kleuren_per_vakje, scatterPlotColors, scatterPlotColor

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

# Support Vector Machines
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

tshirt_naar_origineel_svn = make_pipeline(StandardScaler(), SVR(C=100.0, epsilon=0.5))
tshirt_naar_origineel_svn.fit(tshirt, origineel[:,0])
pred_tshirt_R = np.atleast_2d(tshirt_naar_origineel_svn.predict(tshirt)).T
tshirt_naar_origineel_svn.fit(tshirt, origineel[:,1])
pred_tshirt_G = np.atleast_2d(tshirt_naar_origineel_svn.predict(tshirt)).T
tshirt_naar_origineel_svn.fit(tshirt, origineel[:,2])
pred_tshirt_B = np.atleast_2d(tshirt_naar_origineel_svn.predict(tshirt)).T
# scatterPlotColors(tshirt, pred_tshirt, alpha, 0)
pred_tshirt = np.hstack((pred_tshirt_R, pred_tshirt_G, pred_tshirt_B))

vergelijk_kleuren_per_vakje(origineel_pad, pred_tshirt, matrix_size, tussenruimte)
x=1