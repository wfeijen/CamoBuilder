import csv
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
import pickle
from os.path import exists
from projectClasses.TopoGeneratieDefinities import TopoGeneratieDefinities
from projectClasses.Topografie import Topografie, genereerToposEnCache
from projectClasses.PictureCreator import PictureCreator

breedte = 5000
hoogte = 6000
sterkteSecundairPatroon = 1.0 # schaal is 0,0 (niet) tot en met 2.0 Secundair patroon maximaal
transparantie = 1000 # schaal is 0 (niet tot 2000, volledig transparant)

DetailTopoDefinities = TopoGeneratieDefinities(w=breedte,
                                               h=hoogte,
                                               n=max(5, hoogte) ,
                                               minSize=max(1, hoogte // 300),
                                               maxSize=max(1, hoogte // 20),
                                               startRandom=10,
                                               invloedGewichten=700,
                                               afplatting=2)

GlobaleTopoDefinities = TopoGeneratieDefinities(w=breedte,
                                                h=hoogte,
                                                n=max(1, hoogte // 20),
                                                minSize=max(1, hoogte // 12),
                                                maxSize=max(1, hoogte // 4),
                                                startRandom=0,
                                                invloedGewichten=700,
                                                afplatting=3)
Kleurendir = 'kleurParameters/'
# Kleurenbestand = '2KleurenVoorOnderzoekGroveTekenig.csv'
Kleurenbestand = 'lenteAlmer.jpg20210522 121425.csv'

NaamFilePrefix = "camoOutput/kleurBest-" + Kleurenbestand[:-4] + GlobaleTopoDefinities.afmetingen() + \
                 "_GLOB" + GlobaleTopoDefinities.naam() + "_DET" + DetailTopoDefinities.naam()

kleurInfo = pd.read_csv(Kleurendir + Kleurenbestand, index_col=0)
DetailKleurCodes = kleurInfo.iloc[:, 0:3].to_numpy()
KleurGewichten = kleurInfo.iloc[:, [3]]
KleurGewichten = (KleurGewichten * GlobaleTopoDefinities.invloedGewichten) // KleurGewichten.max()
KleurGewichten = KleurGewichten.to_numpy().flatten()
KleurNaarHoofdkleurVerwijzing = kleurInfo.iloc[:, [5]].to_numpy().flatten()

with open('normaalVerdeling1000stappen1000naar1.csv', 'r') as f:
    reader = csv.reader(f)
    dummy = list(reader)
    normaalVerdeling = []
    for s in dummy: normaalVerdeling.append(int(float((s[0]))))

aantalKleuren = len(DetailKleurCodes)

GlobaleTopografien = genereerToposEnCache(topoDefinities=GlobaleTopoDefinities,
                                          aantalTopos=2,
                                          verdeling=normaalVerdeling)

DetailTopografien = genereerToposEnCache(topoDefinities=DetailTopoDefinities,
                                         aantalTopos=aantalKleuren,
                                         verdeling=normaalVerdeling)

TranspariantieTopografie = genereerToposEnCache(topoDefinities=DetailTopoDefinities,
                                                aantalTopos=1,
                                                verdeling=normaalVerdeling)[0]

# Parallel(n_jobs=7, verbose=10)(
#     delayed(createPicture)(NaamFilePrefix, kleurCodes, topografien, np.append(kleurGewichten, transparantie))
#     for transparantie in [-10000, -8000, -6000, -4000, -2000, 0])
pictureCreator = PictureCreator(GlobaleTopoDefinities)

pictureCreator.createPicture(name=NaamFilePrefix,
                             colorCodes=DetailKleurCodes,
                             detailTopos=DetailTopografien,
                             globaleTopos=GlobaleTopografien,
                             transparantieTopo=TranspariantieTopografie,
                             transparantie=transparantie,
                             colorWeights=KleurGewichten,
                             kleurNaarHoofdkleurVerwijzing=KleurNaarHoofdkleurVerwijzing,
                             sterkteSecundairPatroon=sterkteSecundairPatroon)
print('klaar met plaatje')
