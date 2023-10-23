#%%
import pickle
import numpy as np
import pandas as pd
from functies_voor_onderzoek import vergelijk_plaatje_met_kleuren_range, vergelijk_2_kleurenranges
from sklearn.neighbors import KDTree

#unset GTK_PATH
hokjes_per_rij = 27  # 27x27 matrix
grootte_hokje = 100
tussenruimte = 25


def corrigeer_kleuren(van_schema_filenaam, naar_schema_filenaam, kleurinfo_in, alfa = 0.001, K = 10):
    kleuren_in = kleurinfo_in[['R', 'G', 'B']].to_numpy()
    with open(van_schema_filenaam, 'rb') as file:
        van_schema = pickle.load(file)
    with open(naar_schema_filenaam, 'rb') as file:
        naar_schema = pickle.load(file)
    aantal_kleuren_in_schema = len(van_schema)    
    if len(naar_schema) !=aantal_kleuren_in_schema:
        raise Exception('kleurenschemas zijn niet even lang')
    van_schema = np.array(van_schema).reshape(aantal_kleuren_in_schema, 3)
    naar_schema = np.array(naar_schema).reshape(aantal_kleuren_in_schema, 3)
    tree = KDTree(van_schema)
    afstanden, indices = tree.query(kleuren_in , K)
    relevante_rgb = naar_schema[indices]
    afstanden_per_rgb = np.repeat(afstanden.reshape(aantal_kleuren_in_schema,K,1), 3, axis=2) + alfa
    kleurwaarde_div_afstand = (relevante_rgb / afstanden_per_rgb)
    som_kleurwaarde_div_afstand = np.sum(kleurwaarde_div_afstand, axis = 1)
    div_afstand = (1 / afstanden_per_rgb)
    som_div_afstand = np.sum(div_afstand, axis = 1)
    kleurwaarden_gecorrigeerd = (som_kleurwaarde_div_afstand / som_div_afstand).astype(int)
    kleurInfo_gecorrigeerd = kleurinfo_in.copy(deep=True)    
    kleurInfo_gecorrigeerd[['R', 'G', 'B']] = kleurwaarden_gecorrigeerd
    return kleurwaarden_gecorrigeerd

# y = x / afstanden_per_rgb * afstanden.mean()

# z = y.mean(axis = 1)
# %%
from functies_voor_onderzoek import vergelijk_plaatje_met_kleuren_range

# unset GTK_PATH

directory = "/home/willem/Pictures/Camouflage/ColorCard/converted/"
origineel_pad = directory + "colorCard_zonder_tekst.jpg"


with open('origineel_kleuren.pkl', 'rb') as file:
    origineel_kleuren = pickle.load(file)
with open('tshirt_kleuren.pkl', 'rb') as file:
    tshirt_kleuren = pickle.load(file)
with open('lexmark_kleuren.pkl', 'rb') as file:
    lexmark_kleuren = pickle.load(file)

tshirtNp = np.array(tshirt_kleuren)
origineelNp = np.array(origineel_kleuren)
lexmarkNp = np.array(lexmark_kleuren)

tshirtPd = pd.DataFrame(tshirt_kleuren, columns = ['R','G','B'])
origineelPd = pd.DataFrame(origineel_kleuren, columns = ['R','G','B'])
lexmarkPd = pd.DataFrame(lexmark_kleuren, columns = ['R','G','B'])
#testwaarden = np.array([[20,20,20], [128, 128, 128], [200, 200, 200]])
x = np.sort(tshirtPd, axis=0)
testwaarden = np.concatenate(([x[0]], [np.median(x, axis=0)], [x[-1]]), axis=0)

# Support Vector Machines
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

pred_origineel = corrigeer_kleuren(van_schema_filenaam='tshirt_kleuren.pkl',
                                naar_schema_filenaam='origineel_kleuren.pkl',
                                kleurinfo_in=tshirtPd)

# vergelijk_2_kleurenranges(origineelNp, pred_origineel,
#                           aantal_hokjes = hokjes_per_rij, grootte_hokje=grootte_hokje, tussenruimte=tussenruimte)

pred_origineel = corrigeer_kleuren(van_schema_filenaam='lexmark_kleuren.pkl',
                                naar_schema_filenaam='origineel_kleuren.pkl',
                                kleurinfo_in=lexmarkPd)

vergelijk_2_kleurenranges(origineelNp, pred_origineel,
                          aantal_hokjes = hokjes_per_rij, grootte_hokje=grootte_hokje, tussenruimte=tussenruimte)
