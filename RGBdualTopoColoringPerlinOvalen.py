import csv
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
import pickle
import os
from projectClasses.TopoGeneratieDefinities import TopoGeneratieDefinities
from projectClasses.Topografie import Topografie, genereerToposEnCache
from projectClasses.PictureCreator import PictureCreator
from PerlinTopoGenerator import PerlinTopoGeneratator


breedte = 1500
hoogte = 2000
versie = 4
sterkteSecundairPatroon = 1.0
transparantie = 800#3200
invloedGewichtenPromile = 800#400

KleurenPad = 'kleurParameters/graslandZomer3.jpg20210815 172940.csv'
root_dir = '/mnt/GroteSchijf/machineLearningPictures/camoBuilder/'

kleurInfo = pd.read_csv(KleurenPad, index_col=0)

DetailTopoDefinities = TopoGeneratieDefinities(w=breedte,
                                               h=hoogte,
                                               n=max(5, hoogte * 5 // len(kleurInfo)) ,
                                               minSize=max(1, hoogte // 100),
                                               maxSize=max(1, hoogte // 15),
                                               startRandom=0,
                                               afplatting=0.7,
                                               versie=versie)



GlobaleTopoDefinities = TopoGeneratieDefinities(w=breedte,
                                                h=hoogte,
                                                n=max(1, hoogte // 40),
                                                minSize=max(1, hoogte // 15),
                                                maxSize=max(1, hoogte // 6),
                                                startRandom=0,
                                                afplatting=2,
                                                versie=versie)

Kleurenbestand = os.path.splitext(os.path.basename(KleurenPad))[0]

NaamFilePrefix = "camoOutput/kleurBest-" + Kleurenbestand[:-4] + "_InvloedKleurGewichten" + str(invloedGewichtenPromile) + GlobaleTopoDefinities.afmetingen() + \
                 "_GLOB" + GlobaleTopoDefinities.naam() + "_DET" + DetailTopoDefinities.naam()


DetailKleurCodes = kleurInfo.iloc[:, 0:3].to_numpy()
KleurGewichten = kleurInfo.iloc[:, [3]]
KleurGewichten = (KleurGewichten * invloedGewichtenPromile) // KleurGewichten.max()
KleurGewichten = tuple(KleurGewichten.to_numpy().flatten()) #tuple
KleurNaarHoofdkleurVerwijzing = tuple(kleurInfo.iloc[:, [5]].to_numpy().flatten()) #tuple

AantalKleurenSecundair = len(np.unique(KleurNaarHoofdkleurVerwijzing))

with open('normaalRingVerdeling1000stappen1000naar1.csv', 'r') as f:
    reader = csv.reader(f)
    dummy = list(reader)
    normaalVerdeling = []
    for s in dummy: normaalVerdeling.append(int(float((s[0]))))

aantalKleuren = len(DetailKleurCodes)

GlobaleTopografien = genereerToposEnCache(topoDefinities=GlobaleTopoDefinities,
                                          aantalTopos=AantalKleurenSecundair,
                                          verdeling=normaalVerdeling,
                                          rootDir=root_dir)

DetailTopografien = genereerToposEnCache(topoDefinities=DetailTopoDefinities,
                                         aantalTopos=aantalKleuren,
                                         verdeling=normaalVerdeling,
                                         rootDir=root_dir)
if transparantie > 0:
    TranspariantieTopografie = genereerToposEnCache(topoDefinities=GlobaleTopoDefinities,
                                                    aantalTopos=1,
                                                    verdeling=normaalVerdeling,
                                                    rootDir=root_dir)[0]
else:
    TranspariantieTopografie = 0
pictureCreator = PictureCreator(GlobaleTopoDefinities)

pictureCreator.createBolletjesPicture(name=NaamFilePrefix,
                             colorCodes=DetailKleurCodes,
                             detailTopos=DetailTopografien,
                             globaleTopos=GlobaleTopografien,
                             transparantieTopo=TranspariantieTopografie,
                             transparantie=transparantie,
                             colorWeights=KleurGewichten,
                             kleurNaarHoofdkleurVerwijzing=KleurNaarHoofdkleurVerwijzing,
                             sterkteSecundairPatroon=sterkteSecundairPatroon,
                             rootDir=root_dir)
print('klaar met plaatje')
