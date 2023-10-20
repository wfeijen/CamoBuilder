#%%
import pickle
from sklearn.linear_model import LinearRegression, Lasso
import numpy as np
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



tshirt_plat = tshirt.reshape(27 * 27, 3)
origineel_plat = origineel.reshape(27 * 27, 3)
#%%

tree = KDTree(tshirt_plat)
P1 = [(0,0,0), (100, 100, 100), (150, 150, 150)]
punten = len(P1)
K = 10
# For finding K neighbors of P1 with shape (1, 3)
distances, indices = tree.query(P1, K)

x = tshirt_plat[indices]
distances_expanded = np.repeat(distances.reshape(punten,K,1), 3, axis=2)

y = x / distances_expanded * distances.mean()

z = y.mean(axis = 1)
# %%
