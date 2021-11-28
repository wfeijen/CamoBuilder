import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

KleurenPad = 'kleurParameters/graslandZomer3.jpg20211018 190113.csv'
kleurInfo = pd.read_csv(KleurenPad, index_col=0)

def rgb_to_hex(rgb):
    hexkleur = '%02x%02x%02x' % rgb
    return '#' + hexkleur
KleurGewichten = kleurInfo.iloc[:, [3]].squeeze().values.tolist()
kleuren = kleurInfo.iloc[:, [0, 1, 2]]
hex_kleuren = kleuren.values.tolist()
for kleur in kleuren.values:
    print(tuple(kleur))
hex_kleuren1 = [rgb_to_hex(tuple(kleur)) for kleur in kleuren.values]

# Plot1
plt.pie(x = KleurGewichten,  colors=hex_kleuren1, radius=1,
autopct='%1.1f%%', shadow=False, startangle=0)

# Plot2
kleurenM = np.uint8(kleurInfo.iloc[:, [5, 5, 5]]) * 30 + 120
hex_kleuren2 = [rgb_to_hex(tuple(kleur)) for kleur in kleurenM]
plt.pie(x = KleurGewichten,  colors=hex_kleuren2, radius=0.7,
 shadow=False, startangle=0)

plt.axis('equal')
plt.show()