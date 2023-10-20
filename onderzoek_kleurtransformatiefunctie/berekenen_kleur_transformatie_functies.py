import pickle
from sklearn.linear_model import LinearRegression, Lasso
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.model_selection import train_test_split


with open('origineel_kleuren.pkl', 'rb') as file:
    origineel_kleuren = pickle.load(file)
with open('tshirt_kleuren.pkl', 'rb') as file:
    tshirt_kleuren = pickle.load(file)
with open('lexmark_kleuren.pkl', 'rb') as file:
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

# scatterPlotColors(origineel, tshirt, alpha)
# scatterPlotColors(origineel, lexmark, alpha)


tshirt_naar_origineel_lineair = LinearRegression().fit(tshirt, origineel)
tshirt_naar_origineel_lineair_r_sq = tshirt_naar_origineel_lineair.score(tshirt, origineel)
print(f"coefficient of determination: {tshirt_naar_origineel_lineair_r_sq}")
print(f"predicted response:\n{tshirt_naar_origineel_lineair.predict(testwaarden)}")
print(tshirt_naar_origineel_lineair.coef_)
print(tshirt_naar_origineel_lineair.intercept_)
pred_tshirt = tshirt_naar_origineel_lineair.predict(tshirt)
# scatterPlotColors(tshirt, pred_tshirt, alpha, 0)

# nu gaan we polinomiaal proberen
polynoom = 2
tshirt_ = PolynomialFeatures(degree=polynoom, include_bias=False).fit_transform(tshirt)
tshirt_naar_origineel_polynoom = LinearRegression().fit(tshirt_, origineel)
tshirt_naar_origineel_polynoom_r_sq = tshirt_naar_origineel_polynoom.score(tshirt_, origineel)
print(f"coefficient of determination polynoom 2: {tshirt_naar_origineel_polynoom_r_sq}")
print(f"predicted response:\n{tshirt_naar_origineel_polynoom.predict(PolynomialFeatures(degree=polynoom, include_bias=False).fit_transform(testwaarden))}")
print(tshirt_naar_origineel_polynoom.coef_)
print(tshirt_naar_origineel_polynoom.intercept_)

pred_tshirt = tshirt_naar_origineel_polynoom.predict(tshirt_)
# scatterPlotColors(tshirt, pred_tshirt, alpha, 0)
# de verbetering is niet echt zodanig dat we het model op deze manier ingewikkeld moeten maken

import numpy as np
from sklearn.linear_model import RidgeCV
reg = RidgeCV(alphas=np.logspace(-6, 6, 13)).fit(tshirt, origineel)
print(reg.alpha_)
print(reg.coef_)
print(reg.intercept_)


# Lasso regressie
tshirt_naar_origineel_lasso = Lasso().fit(tshirt, origineel)
tshirt_naar_origineel_lasso_r_sq = tshirt_naar_origineel_lasso.score(tshirt, origineel)
print(f"coefficient of determination lasso: {tshirt_naar_origineel_lasso_r_sq}")
print(f"predicted response lasso:\n{tshirt_naar_origineel_lasso.predict(testwaarden)}")
print(tshirt_naar_origineel_lasso.coef_)
print(tshirt_naar_origineel_lasso.intercept_)
pred_tshirt = tshirt_naar_origineel_lasso.predict(tshirt)
# scatterPlotColors(tshirt, pred_tshirt, alpha, 0)

# Support Vector Machines
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

tshirt_naar_origineel_svn = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
tshirt_naar_origineel_svn.fit(tshirt, origineel[:,0])
pred_tshirt_R = tshirt_naar_origineel_svn.predict(tshirt)

scatterPlotColor(tshirt, pred_tshirt_R, alpha, 0)
x=1