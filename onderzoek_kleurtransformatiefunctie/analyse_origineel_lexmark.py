#%%
import pickle
from sklearn.linear_model import LinearRegression, Lasso
import numpy as np
import pandas as pd
from functies_voor_onderzoek import vergelijk_plaatje_met_kleuren_range, scatterPlotColors, scatterPlotColor

# unset GTK_PATH

matrix_size = 27  # 27x27 matrix
tussenruimte = 30
directory = "/home/willem/Pictures/Camouflage/ColorCard/converted/"
origineel_pad = directory + "colorCard_zonder_tekst.jpg"

with open('origineel_kleuren.pkl', 'rb') as file:
    origineel_kleuren = pickle.load(file)
with open('tshirt_kleuren.pkl', 'rb') as file:
    tshirt_kleuren = pickle.load(file)
with open('lexmark_kleuren.pkl', 'rb') as file:
    lexmark_kleuren = pickle.load(file)

tshirt = np.array(tshirt_kleuren)
origineel = np.array(origineel_kleuren)
lexmark = np.array(lexmark_kleuren)
delta = origineel - lexmark
#testwaarden = np.array([[20,20,20], [128, 128, 128], [200, 200, 200]])

#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import viridis

def plot_2d_array_lines(array_2d):
    num_rows, num_cols = array_2d.shape

    # Create a color map using viridis
    colors = viridis(np.linspace(0, 1, num_rows))

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot each row as a line graph with a different color
    for i in range(num_rows):
        ax.plot(array_2d[i, :], label=f'Row {i + 1}', color=colors[i])

    # Add labels and legend
    ax.set_xlabel('Column Index')
    ax.set_ylabel('Value')
    ax.legend()

    # Show the plot
    plt.show()

def van_1d_3_kleuren_naar_2d_1_kleur(eendimentionale_kleuren_array, matrix_size, kleur):
    kleur_index = 0
    array_uit = np.zeros(shape=(matrix_size, matrix_size))
    for y in range(matrix_size):
        for x in range(matrix_size):
            array_uit[x, y] = eendimentionale_kleuren_array[kleur_index, kleur]
            kleur_index += 1
    return array_uit


#%%
delta2d_rood = van_1d_3_kleuren_naar_2d_1_kleur(delta, 27, 0)
plot_2d_array_lines(delta2d_rood)

delta2d_groen = van_1d_3_kleuren_naar_2d_1_kleur(delta, 27, 1)
plot_2d_array_lines(delta2d_groen)

delta2d_blauw = van_1d_3_kleuren_naar_2d_1_kleur(delta, 27, 2)
plot_2d_array_lines(delta2d_blauw)

import plotly.express as px

heatmap_rood = px.imshow(delta2d_rood)
heatmap_rood.show()
heatmap_groen = px.imshow(delta2d_groen)
heatmap_groen.show()
heatmap_blauw = px.imshow(delta2d_blauw)
heatmap_blauw.show()

# %%
from sklearn.neighbors import KDTree
kleuren_filenaam = '../kleurParameters/groen_buin_beige_l.jpgkleurSchaduwMedian20230701 110550.csv'
kleurInfo = pd.read_csv(kleuren_filenaam, index_col=0)

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
    relevante_rgb = van_schema[indices]
    afstanden_per_rgb = np.repeat(afstanden.reshape(aantal_kleuren_in_schema,K,1), 3, axis=2) + alfa
    kleurwaarde_div_afstand = (relevante_rgb / afstanden_per_rgb)
    som_kleurwaarde_div_afstand = np.sum(kleurwaarde_div_afstand, axis = 1)
    div_afstand = (1 / afstanden_per_rgb)
    som_div_afstand = np.sum(div_afstand, axis = 1)
    kleurwaarden_gecorrigeerd = (som_kleurwaarde_div_afstand / som_div_afstand).astype(int)
    kleurInfo_gecorrigeerd = kleurinfo_in.copy(deep=True)    
    kleurInfo_gecorrigeerd[['R', 'G', 'B']] = kleurwaarden_gecorrigeerd
    return kleurwaarden_gecorrigeerd


kleurInfo_nieuw_f = corrigeer_kleuren(van_schema_filenaam='lexmark_kleuren.pkl',
                                         naar_schema_filenaam='origineel_kleuren.pkl',
                                         kleurinfo_in=kleurInfo)





# y = x / afstanden_per_rgb * afstanden.mean()

# z = y.mean(axis = 1)
# %%
