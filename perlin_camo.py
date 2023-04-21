import itertools

import pandas as pd
from projectClasses.PerlinTopoGenerator import PerlinTopoGeneratator
from projectClasses.Camo_picture import CamoPicture
from datetime import datetime
import numpy as np

kleuren_naam = 'c1_1.jpgkleurSchaduwMedian20230416 175421.csv'
# kleuren_naam = 'graslandZomer.jpg20230322 095001.csv'
# kleuren_naam = 'graslandZomer.jpg20230103 081900.csv'
# kleuren_naam = 'nazomerWinter2.jpg20230320 105239.csv'
# kleuren_naam = 'graslandZomer3.jpg20220108 134624.csv'

root_dir = '/media/willem/KleindSSD/machineLearningPictures/camoBuilder/'
plaatjes_dir = root_dir + 'camoOutput/'
kleurenPad = './kleurParameters/' + kleuren_naam

kleurInfo = pd.read_csv(kleurenPad, index_col=0)

ptg = PerlinTopoGeneratator(
    breedte=400,
    hoogte=400,
    kleur_verhoudingen=kleurInfo,
    versie=1,
    naam_basis=kleuren_naam,
    contrast=0.9,
    belichting=0.8,
    start_volgorde="grijsGroep") #hoofdKleur, grijsGroep

ptg.generate_globale_topo_canvas_hoogtelijnen(
    Id = "Glob1",
    noise_type = "simplex",
    octaves = 6,
    persistence = 0.4,
    lacunarity = 2,
    scaleX = 20,
    scaleY = 40
)

ptg.bereid_lokale_topos_voor()

ptg.generate_locale_topo_canvas_hoogtelijnen(
    Id = "Lok1",
    noise_type = "simplex",
    octaves = 4,
    persistence = 0,
    lacunarity = 0,
    scaleX = 20,
    scaleY = 20
)

fileNaam = str(datetime.now()) + ".jpg"


picture = CamoPicture(ptg.canvas_detail, ptg.verdeling_in_N_naar_kleur)
# picture.create_bolletjes()
picture.create_vonoroi(schaal_X=30, schaal_Y=30, randomfactor_X=0, randomfactor_Y=0)
#
# picture.show()
picture.save(plaatjes_dir, fileNaam)

info = ptg.info + picture.info
print(info)
f = open(root_dir + "boekhouding.csv", "a")
f.write(fileNaam + "," + info + "\n")
f.close()

i = 1
