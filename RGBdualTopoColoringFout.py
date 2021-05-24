import csv
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
import pickle
from os.path import exists
from projectClasses.TopoGeneratieDefinities import TopoGeneratieDefinities
from projectClasses.Topografie import Topografie
from projectClasses.PictureCreator import PictureCreator

GlobaleTopoDefinities = TopoGeneratieDefinities(w=50,
                                                h=60,
                                                n=30,
                                                minSize=20,
                                                maxSize=300,
                                                startRandom=300,
                                                invloedGewichten=700)

# GlobaleTopoDefinities = TopoGeneratieDefinities(w=5000,
#                                                 h=6000,
#                                                 n=300,
#                                                 minSize=20,
#                                                 maxSize=300,
#                                                 startRandom=300,
#                                                 invloedGewichten=700)

# GlobaleTopoDefinities = TopoGeneratieDefinities(w=50,
#                                                 h=60,
#                                                 n=3,
#                                                 minSize=250,
#                                                 maxSize=1000,
#                                                 startRandom=1,
#                                                 invloedGewichten=700)
Kleurendir = 'kleurParameters/'
# Kleurenbestand = '2KleurenVoorOnderzoekGroveTekenig.csv'
Kleurenbestand = 'lenteAlmer.jpg20210522 121425.csv'

NaamFilePrefix = "camoOutput/" + GlobaleTopoDefinities.naam() + "kleurBest" + Kleurenbestand[:-4]

kleurInfo = pd.read_csv(Kleurendir + Kleurenbestand, index_col=0)
kleurCodes = kleurInfo.iloc[:, 0:3].to_numpy()
kleurGewichten = kleurInfo.iloc[:, 3]
kleurGewichten = (kleurGewichten * GlobaleTopoDefinities.invloedGewichten) // kleurGewichten.max()
kleurGewichten = kleurGewichten.to_numpy()

with open('normaalVerdeling1000stappen1000naar1.csv', 'r') as f:
    reader = csv.reader(f)
    dummy = list(reader)
    normaalVerdeling = []
    for s in dummy: normaalVerdeling.append(int(float((s[0]))))

aantalKleuren = len(kleurCodes)

pickleNaam = "cacheFiles/" + GlobaleTopoDefinities.naam() + str(aantalKleuren) + ".pkl"
if exists(pickleNaam):
    print("van cache")
    filehandler = open(pickleNaam, 'rb')
    topografien = pickle.load(filehandler)
else:
    topografien = [Topografie(GlobaleTopoDefinities) for i in range(aantalKleuren + 1)]
    Parallel(n_jobs=min(7, aantalKleuren + 1), verbose=10)(
        delayed(topografie.genereer)(normaalVerdeling) for topografie in topografien)
    # for topografie in topografien:
    #     topografie.genereer(verdeling=normaalVerdeling)
    print('klaar met topos')
    filehandler = open(pickleNaam, 'wb')
    pickle.dump(topografien, filehandler)

# Parallel(n_jobs=7, verbose=10)(
#     delayed(createPicture)(NaamFilePrefix, kleurCodes, topografien, np.append(kleurGewichten, transparantie))
#     for transparantie in [-10000, -8000, -6000, -4000, -2000, 0])
pictureCreator = PictureCreator(GlobaleTopoDefinities)
for transparantie in [100000]:
    pictureCreator.createPicture(NaamFilePrefix, kleurCodes, topografien, np.append(kleurGewichten, transparantie))
    print('klaar met plaatje')

print('klaar met plaatjes')
