import numpy
from PIL import Image, ImageCms
import datetime
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import random
import os

# Parameters
bepaalDominanteKleurenDir = '//media/willem/KleineSSD/machineLearningPictures/camoBuilder/bepaalDominanteKleuren/'
kleurParametersDir = '/home/willem/PycharmProjects/CamoBuilder/kleurParameters/'
name = 'lenteOostvaardersplassen_1.0/lenteOostvaardersplassen_1.3.jpg'
sampleSize = 1000
percentage_afsplitsen = 0.05
aantal_kleuren = 6
ontwikkel = True

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
    df = df.sample(sampleSize)

# Eerste opdeling. G > B [0, 255] om te zorgen dat het relevant is voor KNN
df['groen'] = np.where(df['G']>df['R'], 255, 0)
# Split moet rond de 0.5 zijn
print('verhouding groen rood is :', df['groen'].mean()/255, ' zou rond de 0.5 moeten zijn')

# Afsplitsen licht en donker
totaal_aantal = len(df.index)
aantal_afsplitsen_per_kant = int(percentage_afsplitsen * totaal_aantal / 2)
df['grijswaarde'] = df[['R', 'G', 'B']].sum(axis=1)
df = df.sort_values(by = 'grijswaarde')
donker_grenswaarde = df['grijswaarde'].loc[df.index[aantal_afsplitsen_per_kant]]
licht_grenswaarde = df['grijswaarde'].loc[df.index[totaal_aantal - aantal_afsplitsen_per_kant]]
df_donker = df.loc[df['grijswaarde'] <= donker_grenswaarde].copy(deep=True)
df_licht = df.loc[df['grijswaarde'] >= licht_grenswaarde].copy(deep=True)
df.drop(df_donker.index,inplace=True)
df.drop(df_licht.index,inplace=True)
# Kolommen toevoegen om straks samen te kunnen voegen met df
df_donker['groep'] = -2
df_licht['groep'] = -1


# Split moet rond de 0.5 zijn
print('verhouding groen rood is :', df['groen'].mean()/255, ' zou rond de 0.5 moeten zijn')

kmeans = KMeans(n_clusters=aantal_kleuren)
kmeans.fit(df[['R', 'G', 'B', 'groen']])
np_kleurenCenters = kmeans.cluster_centers_.astype(int)
kleurenCenters = pd.DataFrame(np_kleurenCenters, columns=['R', 'G', 'B', 'groen'])
kleurenCenters.loc[-1] = df_licht.mean()
kleurenCenters.loc[-2] = df_donker.mean()
kleurenCenters['grijswaarde'] = kleurenCenters['R'] + kleurenCenters['G'] + kleurenCenters['B']
kleurenCenters = kleurenCenters.sort_values(by = 'grijswaarde')
kleurenCenters['groep'] = kleurenCenters.index

# Aantallen tellen
df['groep'] = kmeans.predict(df[['R', 'G', 'B', 'groen']])
# Nu donker en licht er weer aan plakken
df = pd.concat([df_donker, df, df_licht], axis=0).copy(deep=True).sort_index()

# Joinen met kleurenCenters zodat we een vertaaltabel krijgen
df = df.merge(kleurenCenters, how='inner', on='groep', suffixes=('', '_vervangen'))

# Maken tellinen voor verhoudingen
tellingen = df.groupby('groep').size().reset_index(name='counts')
kleurenCenters = kleurenCenters.merge(tellingen, how='inner', on='groep', suffixes=('', ''))





i = 1