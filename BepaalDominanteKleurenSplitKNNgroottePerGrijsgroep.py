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
name = 'nazomerWinter2.jpg'
sampleSizeTest = 1000
sampleSize = 1000000
groottePerGrijsGroep = [3, 3, 3, 3, 3]
aantal_kleuren = sum(groottePerGrijsGroep)
#aantal_grijsgroepen = 3
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
# Eerste opdeling. G > B [0, 255] om te zorgen dat het relevant is voor KNN
df['RG'] = np.where(df['G']>df['R'], 255, 0)

# Split moet rond de 0.5 zijn
print('verhouding RG is :', df['RG'].mean()/255, ' zou rond de 0.5 moeten zijn')
print('verhouding GB is :', np.where(df['R']>df['B'], 255, 0).mean()/255, ' zou rond de 0.5 moeten zijn om te gebruiken. Niet gebruikt')
print('verhouding GB is :', np.where(df['G']>df['B'], 255, 0).mean()/255, ' zou rond de 0.5 moeten zijn om te gebruiken. Niet gebruikt')

# Afsplitsen licht en donker
totaal_aantal = len(df.index)
df['grijswaarde'] = df[['R', 'G', 'B']].sum(axis=1)
df = df.sort_values(by = 'grijswaarde')

# Split moet rond de 0.5 zijn
print('verhouding RG rood is :', df['RG'].mean()/255, ' zou rond de 0.5 moeten zijn')

kmeans = KMeans(n_clusters= aantal_kleuren)
kmeans.fit(df[['R', 'G', 'B', 'RG']])
np_kleurenCenters = kmeans.cluster_centers_.astype(int)
kleurenCenters = pd.DataFrame(np_kleurenCenters, columns=['R', 'G', 'B', 'RG'])
kleurenCenters['grijswaarde'] = kleurenCenters['R'] + kleurenCenters['G'] + kleurenCenters['B']
kleurenCenters = kleurenCenters.sort_values(by = 'grijswaarde')
kleurenCenters['groep'] = kleurenCenters.index

# Aantallen tellen
df['groep'] = kmeans.predict(df[['R', 'G', 'B', 'RG']])

# Joinen met kleurenCenters zodat we een vertaaltabel krijgen
df = df.merge(kleurenCenters, how='inner', on='groep', suffixes=('', '_vervangen'))


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)
kleurenCenters['hex'] = kleurenCenters.loc[:,['R', 'G', 'B']].apply(lambda r: rgb_to_hex(*r), axis=1)

if sampleSizeTest > df['R'].size:
    sampleSizeTest = pdImage['R'].size
selectie = random.sample(list(range(0, df['R'].size)), sampleSizeTest)
R = df.iloc[selectie, 0]
G = df.iloc[selectie, 1]
B = df.iloc[selectie, 2]
C = df.iloc[selectie, 5]
fig, ax = plt.subplots()
ax.scatter(R, G, c=C, s=50, cmap='viridis')
ax.set_xlabel('R')
ax.set_ylabel('G')
ax.scatter(kleurenCenters.loc[:, 'R'], kleurenCenters.loc[:, 'G'], c=kleurenCenters.loc[:, 'hex'], s=200, alpha=1)
plt.show()

fig, ax = plt.subplots()
ax.scatter(R, B, c=C, s=50, cmap='viridis')
ax.set_xlabel('R')
ax.set_ylabel('B')
ax.scatter(kleurenCenters.loc[:, 'R'], kleurenCenters.loc[:, 'B'], c=kleurenCenters.loc[:, 'hex'], s=200, alpha=1)
plt.show()

fig, ax = plt.subplots()
ax.scatter(G, B, c=C, s=50, cmap='viridis')
ax.set_xlabel('G')
ax.set_ylabel('B')
ax.scatter(kleurenCenters.loc[:, 'G'], kleurenCenters.loc[:, 'B'], c=kleurenCenters.loc[:, 'hex'], s=200, alpha=1)
plt.show()

# Maken tellingen voor verhoudingen
tellingen = df.groupby('groep').size().reset_index(name='counts')
kleurenCenters = kleurenCenters.merge(tellingen, how='inner', on='groep', suffixes=('', ''))

# Toevoegen grijsgroepen
grijsgroep_nummers = []
grijsGroep = 0
for grootteGrijsGroep in groottePerGrijsGroep:
    for i in range(grootteGrijsGroep):
        grijsgroep_nummers.append(grijsGroep)
    grijsGroep += 1


kleurenCenters['grijsgroep'] = grijsgroep_nummers
kleurenPerGrijswaarde = kleurenCenters.loc[:,['R', 'G', 'B', 'grijsgroep']].groupby('grijsgroep').mean().astype(int)
kleurenPerGrijswaarde['hex'] = kleurenPerGrijswaarde.loc[:,['R', 'G', 'B']].apply(lambda r: rgb_to_hex(*r), axis=1)
aantallenPerGrijswaarde = kleurenCenters.loc[:,['counts', 'grijsgroep']].groupby('grijsgroep').sum()

# plot a Pie Chart for Registration Price column with label Car column
plt.pie(kleurenCenters["counts"], labels = kleurenCenters["grijswaarde"], colors=kleurenCenters['hex'])
plt.pie(aantallenPerGrijswaarde["counts"], radius = 0.7, colors=kleurenPerGrijswaarde['hex'])
plt.show()

# Aanpassen aan ontvangend programma met andere naamgeving
# ,R,G,B,RG,grijswaarde,groep,hex,counts
# ,R,G,B,aantal,verdeling_in_N,verdeling_in_M
kleurenCenters.rename(columns = {'groep':'verdeling_in_N', 'grijsgroep':'verdeling_in_M', 'counts':'aantal'}, inplace = True)
kleurenCenters = kleurenCenters.loc[:, ['R', 'G', 'B', 'aantal', 'verdeling_in_N', 'verdeling_in_M']]
# Wegschrijven
if not ontwikkel:
    now = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
    print(kleurParametersDir + name + now + '.csv')
    kleurenCenters.to_csv(kleurParametersDir + name + now + '.csv')



