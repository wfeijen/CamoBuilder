import matplotlib.pyplot as plt
import pandas as pd

KleurenPad = 'kleurParameters/graslandZomer3.jpg20210815 172940.csv'
kleurInfo = pd.read_csv(KleurenPad, index_col=0)

def rgb_to_hex(rgb):
    hexkleur = '%02x%02x%02x' % rgb
    return '#' + hexkleur
KleurGewichten = kleurInfo.iloc[:, [3]].squeeze().values.tolist()
kleuren = kleurInfo.iloc[:, [0, 1, 2]]
hex_kleuren = kleuren.values.tolist()
for kleur in kleuren.values:
    print(tuple(kleur))
hex_kleuren2 = [rgb_to_hex(tuple(kleur)) for kleur in kleuren.values]




# Plot
plt.pie(x = KleurGewichten,  colors=hex_kleuren2,
autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.show()