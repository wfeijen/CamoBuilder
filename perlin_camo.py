import random

import pandas as pd
from projectClasses.PerlinTopoGenerator import PerlinTopoGeneratator
from projectClasses.Camo_picture import CamoPicture
from datetime import datetime
import numpy as np

kleuren_naam = 'graslandZomer.jpg20230322 095001.csv'
# kleuren_naam = 'graslandZomer.jpg20230103 081900.csv'
# kleuren_naam = 'nazomerWinter2.jpg20230320 105239.csv'
# kleuren_naam = 'graslandZomer3.jpg20220108 134624.csv'

root_dir = '/media/willem/KleindSSD/machineLearningPictures/camoBuilder/'
plaatjes_dir = root_dir + 'camoOutput/'
kleurenPad = './kleurParameters/' + kleuren_naam

kleurInfo = pd.read_csv(kleurenPad, index_col=0)

ptg = PerlinTopoGeneratator(
    breedte=200,
    hoogte=200,
    kleur_verhoudingen=kleurInfo,
    versie=1,
    naam_basis=kleuren_naam,
    contrast=0.9,
    belichting=0.8)

ptg.generate_globale_topo_ringen_canvas(
    Id="Glob1",
    aantal=200,
    max_waarde_stopconditie=400,
    octaves=8,
    persistence=0.4,
    lacunarity=4,
    scaleX=300,
    scaleY=600,
    percentage_max_px=0.60
)

ptg.generate_globale_topo_blots(
    Id="Glob2",
    aantal=400,
    blot_grootte_factor=0.5,
    min_blotgrootte=0,
    max_blotgrootte=200,
    afplattingen=[*np.arange(1., 3., 0.3), .5],
    octaves=8,
    persistence=0.4,
    lacunarity=4.0,
    scaleX=150,
    scaleY=300,
    grenswaarde=0.60
)

ptg.generate_globale_topo_blots(
    Id="Glob3",
    aantal=400,
    max_waarde_stopconditie=25,
    blot_grootte_factor=0.5,
    min_blotgrootte=0,
    max_blotgrootte=200,
    afplattingen=[*np.arange(1., 3., 0.3), .5],
    octaves=8,
    persistence=0.4,
    lacunarity=4.0,
    scaleX=150,
    scaleY=300,
    grenswaarde=0.60
)

ptg.bereid_lokale_topos_voor()

ptg.generate_locale_topo(
    Id="Det1",
    aantal=800,
    blot_grootte_factor=0.7,
    min_blotgrootte=100,
    max_blotgrootte=200,
    # max_waarde_stopconditie = 200,
    afplattingen=[*np.arange(1., 2., 0.3), .5],
    octaves=8,
    persistence=0.3,
    lacunarity=5.0,
    scaleX=25,
    scaleY=100,
    grenswaarde=0.5)

ptg.generate_locale_topo(
    Id="Det2",
    aantal=400,
    blot_grootte_factor=0.6,
    min_blotgrootte=5,
    max_blotgrootte=500,
    max_waarde_stopconditie=5,
    afplattingen=[*np.arange(1., 2., 0.3), .5],
    octaves=8,
    persistence=0.3,
    lacunarity=5.0,
    scaleX=25,
    scaleY=100,
    grenswaarde=0.5)

fileNaam = str(datetime.now()) + ".jpg"


picture = CamoPicture(ptg.canvas_detail, ptg.verdeling_in_N_naar_kleur)
# picture.create_bolletjes()
picture.create_vonoroi(schaal_X=30, schaal_Y=30, randomfactor_X=3, randomfactor_Y=3)
#
# picture.show()
picture.save(plaatjes_dir, fileNaam)

info = ptg.info + picture.info
print(info)
f = open(root_dir + "boekhouding.csv", "a")
f.write(fileNaam + "," + info + "\n")
f.close()

i = 1
