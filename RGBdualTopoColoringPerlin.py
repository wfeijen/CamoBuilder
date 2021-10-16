import numpy as np
import pandas as pd
import os
from projectClasses.PictureCreator import PictureCreator
from PerlinTopoGenerator import PerlinTopoGeneratator


breedte = 1500
hoogte = 2000
versie = 4
sterkteSecundairPatroon = 0.7
transparantie = 500#3200
invloedGewichtenPromile = 25#400

KleurenPad = 'kleurParameters/graslandZomer3.jpg20211015 144736.csv'
root_dir = '/mnt/GroteSchijf/machineLearningPictures/camoBuilder/'

kleurInfo = pd.read_csv(KleurenPad, index_col=0)

DetailKleurCodes = kleurInfo.iloc[:, 0:3].to_numpy()
KleurGewichten = kleurInfo.iloc[:, [3]]
KleurGewichten = (KleurGewichten * invloedGewichtenPromile) // KleurGewichten.max()
KleurGewichten = tuple(KleurGewichten.to_numpy().flatten()) #tuple
KleurNaarHoofdkleurVerwijzing = tuple(kleurInfo.iloc[:, [5]].to_numpy().flatten()) #tuple

aantalKleurenSecundair = len(np.unique(KleurNaarHoofdkleurVerwijzing))
aantalKleuren = len(DetailKleurCodes)

# noise.pnoise3()
# noise.snoise2()

detailTopoGenerator = PerlinTopoGeneratator(w=breedte,
                                            h=hoogte,
                                            n=aantalKleuren,
                                            octaves=7,
                                            persistence=0.2,
                                            lacunarity=10.0,
                                            scalex=60,
                                            scaley=40,
                                            versie=1)

detailTopos = detailTopoGenerator.generate_all_topos()



globaleTopoGenerator = PerlinTopoGeneratator(w=breedte,
                                             h=hoogte,
                                             n=aantalKleurenSecundair,
                                             octaves=3,
                                             persistence=0.2,
                                             lacunarity=4.0,
                                             scalex=300,
                                             scaley=400,
                                             versie=7)

globaleTopos = globaleTopoGenerator.generate_all_topos()

if transparantie > 0:
    transparantieTopoGenerator = PerlinTopoGeneratator(w=breedte,
                                                       h=hoogte,
                                                       n=1,
                                                       octaves=2,
                                                       persistence=0.2,
                                                       lacunarity=4.0,
                                                       scalex=100,
                                                       scaley=100,
                                                       versie=10000)
    transpariantieTopografie = transparantieTopoGenerator.generate_topo(0)
    transNaam = transparantieTopoGenerator.naam()
else:
    transpariantieTopografie = 0
    transNaam = ""

Kleurenbestand = os.path.splitext(os.path.basename(KleurenPad))[0]

NaamFilePrefix = "camoOutput/kleurBest-" + Kleurenbestand[:-4] + "_InvloedKleurGewichten" + str(invloedGewichtenPromile) + "_bh" + str(breedte) + "x" + str(hoogte) + \
                 "_P_GLOB" + globaleTopoGenerator.naam() + "_P_DET" + detailTopoGenerator.naam() + "_P_TRA" + transNaam

aantalKleuren = len(DetailKleurCodes)



pictureCreator = PictureCreator(globaleTopoGenerator)

pictureCreator.createBolletjesPicture(name=NaamFilePrefix,
                             colorCodes=DetailKleurCodes,
                             detailTopos=detailTopos,
                             globaleTopos=globaleTopos,
                             transparantieTopo=transpariantieTopografie,
                             transparantie=transparantie,
                             colorWeights=KleurGewichten,
                             kleurNaarHoofdkleurVerwijzing=KleurNaarHoofdkleurVerwijzing,
                             sterkteSecundairPatroon=sterkteSecundairPatroon,
                             rootDir=root_dir)
print('klaar met plaatje')
