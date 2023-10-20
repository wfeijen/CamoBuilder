import pickle
from pygam import LinearGAM, s, f
import numpy as np
import pandas as pd
from functies_voor_onderzoek import vergelijk_plaatje_met_kleuren_range, scatterPlotColors, scatterPlotColor, vergelijk_2_kleurenranges, vergelijk_3_kleurenranges
import matplotlib.pyplot as plt

n_spline = 10
hokjes_per_rij = 27  # 27x27 matrix
grootte_hokje = 100
tussenruimte = 25
directory = "/home/willem/Pictures/Camouflage/ColorCard/converted/"
origineel_pad = directory + "colorCard_zonder_tekst.jpg"
tshirt_pad = directory + "tshirt_zon_20230930_105940_000046A-8.0_E-1600_I-400_D7500.jpg"


with open('../origineel_kleuren.pkl', 'rb') as file:
    origineel_kleuren = pickle.load(file)
with open('../tshirt_kleuren.pkl', 'rb') as file:
    tshirt_kleuren = pickle.load(file)
with open('../lexmark_kleuren.pkl', 'rb') as file:
    lexmark_kleuren = pickle.load(file)

origineel_pd = pd.DataFrame(origineel_kleuren, columns = ("Ro", "Go", "Bo"))
tshirt_pd = pd.DataFrame(tshirt_kleuren, columns = ("Rt", "Gt", "Bt"))

dataset_pd = origineel_pd.reset_index(drop=True).join(tshirt_pd)
dataset_pd['Rd'] = dataset_pd['Ro'] - dataset_pd['Rt']
dataset_pd['Gd'] = dataset_pd['Go'] - dataset_pd['Gt']
dataset_pd['Bd'] = dataset_pd['Bo'] - dataset_pd['Bt']


tshirt = np.array(tshirt_kleuren)
origineel = np.array(origineel_kleuren)
lexmark = np.array(lexmark_kleuren)










#testwaarden = np.array([[20,20,20], [128, 128, 128], [200, 200, 200]])
vergelijk_plaatje_met_kleuren_range(tshirt_pad, tshirt, matrix_size=hokjes_per_rij, tussenruimte=tussenruimte)

gam_R = LinearGAM(s(0, constraints='monotonic_inc') + s(1, constraints='monotonic_inc') + s(2, constraints='monotonic_inc'), n_splines = n_spline).gridsearch(tshirt, origineel[:,0])
pred_tshirt_R = np.atleast_2d(gam_R.predict(tshirt)).T
gam_G = LinearGAM(s(0, constraints='monotonic_inc') + s(1, constraints='monotonic_inc') + s(2, constraints='monotonic_inc'), n_splines = n_spline).gridsearch(tshirt, origineel[:,1])
pred_tshirt_G = np.atleast_2d(gam_G.predict(tshirt)).T
gam_B = LinearGAM(s(0, constraints='monotonic_inc') + s(1, constraints='monotonic_inc') + s(2, constraints='monotonic_inc'), n_splines = n_spline).gridsearch(tshirt, origineel[:,2])
pred_tshirt_B = np.atleast_2d(gam_B.predict(tshirt)).T
pred_tshirt = np.hstack((pred_tshirt_R, pred_tshirt_G, pred_tshirt_B))



vergelijk_2_kleurenranges(origineel, pred_tshirt,
                          aantal_hokjes = hokjes_per_rij, grootte_hokje=grootte_hokje, tussenruimte=tussenruimte)

vergelijk_3_kleurenranges(origineel,pred_tshirt,tshirt,
                          aantal_hokjes = hokjes_per_rij, grootte_hokje=grootte_hokje, tussenruimte=tussenruimte)


x=1