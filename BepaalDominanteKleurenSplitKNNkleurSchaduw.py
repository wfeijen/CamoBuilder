#%%
from PIL import Image
import datetime
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import random


# Parameters
bepaalDominanteKleurenDir = '/home/willem/Pictures/Camouflage/broncompilaties/'
kleurParametersDir = '/home/willem/PycharmProjects/CamoBuilder/kleurParameters/'
name = 'blauw_en_veel_wit.jpg'
sampleSizeTest = 1000
sampleSize = 1000000
aantal_hoofdlkeuren = 3
aantal_grijswaarden = 17
kleurboost = 0.06
aantal_kleuren = aantal_hoofdlkeuren * aantal_grijswaarden
ontwikkel = False

# Inlezen en naar data omzetten
im = Image.open(bepaalDominanteKleurenDir + name)
if im.mode != "RGB":
    im = im.convert("RGB")

w, h = im.size
npImageOrig = np.array(im)
npImage = npImageOrig.reshape(w * h, 3)
pdImage = pd.DataFrame(npImage, columns=['R', 'G', 'B'])
df = pdImage.copy(deep=True)

if ontwikkel:
    sampleSize = sampleSizeTest

df = df.sample(sampleSize)
# Toevoegen schakering en hoofdkleur
df['grijswaarde'] = df[['R', 'G', 'B']].sum(axis=1).replace(0, 1)
df['Rr'] = df['R'] / df['grijswaarde']
df['Gr'] = df['G'] / df['grijswaarde']
df['Br'] = df['B'] / df['grijswaarde']
df['Rp'] = ((df['Rr'] > df['Gr']) & (df['Rr'] > df['Br'])).astype('Int8') * kleurboost + df['Rr']
df['Gp'] = ((df['Gr'] > df['Rr']) & (df['Gr'] > df['Br'])).astype('Int8') * kleurboost + df['Gr']
df['Bp'] = ((df['Br'] > df['Gr']) & (df['Br'] > df['Rr'])).astype('Int8') * kleurboost + df['Br']


# Eerste opdeling in hoofdkleuren
kmeans = KMeans(n_clusters= aantal_hoofdlkeuren)
kmeans.fit(df[['Rp', 'Gp', 'Bp']])
df['hoofdKleur'] = kmeans.labels_

# Nu per hoofdkleur in grijsgroepen
def k_means(row, aant_groepen):
    clustering=KMeans(n_clusters=aant_groepen)
    model = clustering.fit(row[['R', 'G', 'B']])
    row['grijsGroep'] = model.labels_
    return row

df = df.sort_values(by = ['hoofdKleur', 'grijswaarde'])
df = df.groupby('hoofdKleur').apply(k_means, aantal_grijswaarden)


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)
# Nu kunnen we mean of mediaan berekenen per groep
df.reset_index(drop = True, inplace = True)
medians = df.groupby(['hoofdKleur', 'grijsGroep'])[['R', 'G', 'B', 'grijswaarde']].median().astype({'R':'int', 'G':'int', 'B':'int'})
medians['aantal'] = df.groupby(['hoofdKleur', 'grijsGroep']).size()
medians = medians.sort_values(['grijswaarde']).reset_index()
medians['grijsGroep'] = medians.groupby(['hoofdKleur']).cumcount()
medians['hex'] = medians.loc[:,['R', 'G', 'B']].apply(lambda r: rgb_to_hex(*r), axis=1)
medians = medians.sort_values(['hoofdKleur', 'grijsGroep']).reset_index()


means = df.groupby(['hoofdKleur', 'grijsGroep'])[['R', 'G', 'B', 'grijswaarde']].mean().astype({'R':'int', 'G':'int', 'B':'int'})
means['aantal'] = df.groupby(['hoofdKleur', 'grijsGroep']).size()
means = means.sort_values(['grijswaarde']).reset_index()
means['grijsGroep'] = means.groupby(['hoofdKleur']).cumcount()
means['hex'] = means.loc[:,['R', 'G', 'B']].apply(lambda r: rgb_to_hex(*r), axis=1)
means = means.sort_values(['hoofdKleur', 'grijsGroep']).reset_index()

verschil = medians.copy(deep=True)
verschil['R'] = (means['R'] - medians['R']).abs()
verschil['G'] = (means['G'] - medians['G']).abs()
verschil['B'] = (means['B'] - medians['B']).abs()
maximaal_verschil = verschil[['R', 'G', 'B']].max().max()
verschil['R'] = (verschil['R'] * 255 / maximaal_verschil).astype('int')
verschil['G'] = (verschil['G'] * 255 / maximaal_verschil).astype('int')
verschil['B'] = (verschil['B'] * 255 / maximaal_verschil).astype('int')
verschil['hex'] = verschil.loc[:,['R', 'G', 'B']].apply(lambda r: rgb_to_hex(*r), axis=1)



# if sampleSizeTest > df['R'].size:
#     sampleSizeTest = pdImage['R'].size
# selectie = random.sample(list(range(0, df['R'].size)), sampleSizeTest)
# R = df.iloc[selectie, 0]
# G = df.iloc[selectie, 1]
# B = df.iloc[selectie, 2]
# C = df.iloc[selectie, 5]
# fig, ax = plt.subplots()
# ax.scatter(R, G, c=C, s=50, cmap='viridis')
# ax.set_xlabel('R')
# ax.set_ylabel('G')
# ax.scatter(medians.loc[:, 'R'], medians.loc[:, 'G'], c=medians.loc[:, 'hex'], s=200, alpha=1)
# plt.show()
#
# fig, ax = plt.subplots()
# ax.scatter(R, B, c=C, s=50, cmap='viridis')
# ax.set_xlabel('R')
# ax.set_ylabel('B')
# ax.scatter(medians.loc[:, 'R'], medians.loc[:, 'B'], c=medians.loc[:, 'hex'], s=200, alpha=1)
# plt.show()
#
# fig, ax = plt.subplots()
# ax.scatter(G, B, c=C, s=50, cmap='viridis')
# ax.set_xlabel('G')
# ax.set_ylabel('B')
# ax.scatter(medians.loc[:, 'G'], medians.loc[:, 'B'], c=medians.loc[:, 'hex'], s=200, alpha=1)
# plt.show()
#%%
# Pie charts
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.pie(medians["aantal"], labels = medians["hoofdKleur"], colors=medians['hex'])
ax1.set_xlabel('medianen')
ax2.pie(means["aantal"], labels = means["hoofdKleur"], colors=medians['hex'])
ax2.set_xlabel('means')
ax3.pie(verschil["aantal"], labels = verschil["hoofdKleur"], colors=verschil['hex'])
ax3.set_xlabel(f'verschil is maximaal {maximaal_verschil}')

#%%
# Aanpassen aan ontvangend programma met andere naamgeving
# ,R,G,B,RG,grijswaarde,groep,hex,counts
# ,R,G,B,aantal,verdeling_in_N,verdeling_in_M
# Wegschrijven
now = datetime.datetime.now().strftime('%Y%m%d %H%M%S')

if not ontwikkel:
    print(kleurParametersDir + name + "kleurSchaduwMedian" + now + '.csv')
    medians.to_csv(kleurParametersDir + name + "kleurSchaduwMedian" + now + '.csv')
    plt.savefig(bepaalDominanteKleurenDir + name + "kleurSchaduwMedian" + now + '.jpg')
plt.show()
# if not ontwikkel:
#     print(kleurParametersDir + name + "kleurSchaduwMean" + now + '.csv')
#     means.to_csv(kleurParametersDir + name + "kleurSchaduwMean" + now + '.csv')





# %%
