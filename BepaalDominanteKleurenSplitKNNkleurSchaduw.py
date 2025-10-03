#%%
from PIL import Image
import datetime
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# Parameters
kleuren_filenaam = 'nfp_groen_en_tan_50_50.jpg'
gewicht_factor = 1


root_dir = '/home/willem/Pictures/Camouflage/'
plaatjes_dir = root_dir + 'camoBuilder/camoOutput/'
broncompilaties_dir = root_dir + 'broncompilaties/'
kleurParametersDir = './kleurParameters/'

sampleSizeTest = 1000
sampleSize = 1000000
aantal_hoofdlkeuren = 4
aantal_grijswaarden = 12
kleurboost = 0.06
aantal_kleuren = aantal_hoofdlkeuren * aantal_grijswaarden

# Inlezen en naar data omzetten
im = Image.open(broncompilaties_dir + kleuren_filenaam)
if im.mode != "RGB":
    im = im.convert("RGB")

w, h = im.size
npImageOrig = np.array(im)
npImage = npImageOrig.reshape(w * h, 3)
pdImage = pd.DataFrame(npImage, columns=['R', 'G', 'B'])



#%%
df = pdImage.copy(deep=True)

if sampleSize<df.size:
    df = df.sample(sampleSize)

# Toevoegen schakering en hoofdkleur
df['grijswaarde'] = (0.2989 * df['R']) + (0.5870 * df['G']) + (0.1140 * df['B'])
#%%
df['Rr'] = df['R'] / df['grijswaarde'].replace(0, 0.001)
df['Gr'] = df['G'] / df['grijswaarde'].replace(0, 0.001)
df['Br'] = df['B'] / df['grijswaarde'].replace(0, 0.001)
df['Rp'] = ((df['Rr'] > df['Gr']) & (df['Rr'] > df['Br'])).astype('Int8') * kleurboost + df['Rr']
df['Gp'] = ((df['Gr'] > df['Rr']) & (df['Gr'] > df['Br'])).astype('Int8') * kleurboost + df['Gr']
df['Bp'] = ((df['Br'] > df['Gr']) & (df['Br'] > df['Rr'])).astype('Int8') * kleurboost + df['Br']

#%%
df['gewicht_kleur'] = (df[['R', 'G', 'B']] - df[['grijswaarde', 'grijswaarde', 'grijswaarde']].to_numpy()).pow(2).sum(axis=1) * gewicht_factor + 1
#%%
gemiddelde_grijswaarde = df[['grijswaarde']].mean()
#%%
df['gewicht_grijs'] = (df[['grijswaarde']] - gemiddelde_grijswaarde.to_numpy()).pow(2) * gewicht_factor + 1
#%%
# Eerste opdeling in hoofdkleuren
kmeans = KMeans(n_clusters= aantal_hoofdlkeuren)
kmeans.fit(df[['Rp', 'Gp', 'Bp']], sample_weight=df['gewicht_kleur'])
df['hoofdKleur'] = kmeans.labels_

#%%
# Nu per hoofdkleur in grijsgroepen
def k_means_per_grijsgroep(df_grijsgroep, aant_groepen):
    clustering=KMeans(n_clusters=aant_groepen)
    model = clustering.fit(df_grijsgroep[['R', 'G', 'B']])
    df_grijsgroep['grijsGroep'] = model.labels_
    centers = pd.DataFrame(clustering.cluster_centers_, columns=['cR', 'cG', 'cB'])
    df_grijsgroep = df_grijsgroep.join(centers, on=('grijsGroep'))
    return df_grijsgroep

#%%
df = df.sort_values(by = ['hoofdKleur', 'grijswaarde'])
#%%
df = df.groupby('hoofdKleur', group_keys=False).apply(k_means_per_grijsgroep, aantal_grijswaarden)

#%%
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

#%%
centroids = df.groupby(['hoofdKleur', 'grijsGroep'])[['cR', 'cG', 'cB', 'grijswaarde']].mean().astype({'cR':'int', 'cG':'int', 'cB':'int'}).rename(columns={'cR':'R', 'cG':'G', 'cB':'B'})
#%%
centroids['aantal'] = df.groupby(['hoofdKleur', 'grijsGroep']).size()
centroids = centroids.sort_values(['grijswaarde']).reset_index()
centroids['grijsGroep'] = centroids.groupby(['hoofdKleur']).cumcount()
centroids['hex'] = centroids.loc[:,['R', 'G', 'B']].apply(lambda r: rgb_to_hex(*r), axis=1)
centroids = centroids.sort_values(['hoofdKleur', 'grijsGroep']).reset_index()
#%%
verschil = medians.copy(deep=True)
verschil['R'] = (centroids['R'] - medians['R']).abs()
verschil['G'] = (centroids['G'] - medians['G']).abs()
verschil['B'] = (centroids['B'] - medians['B']).abs()
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
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
ax1.pie(medians["aantal"], labels = medians["hoofdKleur"], colors=medians['hex'])
ax1.set_xlabel('medianen')
ax2.pie(means["aantal"], labels = means["hoofdKleur"], colors=means['hex'])
ax2.set_xlabel('means')
ax3.pie(centroids["aantal"], labels = centroids["hoofdKleur"], colors=centroids['hex'])
ax3.set_xlabel('centroids')
ax4.pie(verschil["aantal"], labels = verschil["hoofdKleur"], colors=verschil['hex'])
ax4.set_xlabel(f'verschil is maximaal {maximaal_verschil}')

#%%
# Aanpassen aan ontvangend programma met andere naamgeving
# ,R,G,B,RG,grijswaarde,groep,hex,counts
# ,R,G,B,aantal,verdeling_in_N,verdeling_in_M
# Wegschrijven
extra_info = f"{datetime.datetime.now().strftime('%Y%m%d %H%M%S')}_{str(aantal_hoofdlkeuren)}x{str(aantal_grijswaarden)}"

print(kleurParametersDir + kleuren_filenaam + "kleurSchaduwMedian" + extra_info + '.csv')
medians.to_csv(kleurParametersDir + kleuren_filenaam + "kleurSchaduwMedian" + extra_info + '.csv')
print(kleurParametersDir + kleuren_filenaam + "kleurSchaduwCentroid:" + str(gewicht_factor) + "_"  + extra_info + '.csv')
centroids.to_csv(kleurParametersDir + kleuren_filenaam + "kleurSchaduwCentroid:" + str(gewicht_factor) + "_" + extra_info + '.csv')
plt.savefig(broncompilaties_dir + kleuren_filenaam + "kleurSchaduwMedian" + extra_info + '.jpg', dpi = 300)
plt.show()
# if not ontwikkel:
#     print(name + "kleurSchaduwMean" + now + '.csv')
#     means.to_csv(kleurParametersDir + name + "kleurSchaduwMean" + now + '.csv')





# %%
