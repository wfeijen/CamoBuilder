import itertools

import pandas as pd
from projectClasses.CanvasGenerator import CanvasGeneratator
from projectClasses.Camo_picture import CamoPicture
from datetime import datetime
import numpy as np
from multiprocessing import Pool

kleuren_naam = 'c1_1.jpgkleurSchaduwMedian20230421 211330.csv'

root_dir = '/media/willem/KleindSSD/machineLearningPictures/camoBuilder/'
plaatjes_dir = root_dir + 'camoOutput/'
kleurenPad = './kleurParameters/' + kleuren_naam

kleurInfoOorspr = pd.read_csv(kleurenPad, index_col=0)

glob_noise_type = ["simplex"]
glob_octaves = [2]#[2, 4, 8]
glob_persistence = [0.2]#[0.2, 0.8]
glob_lacunarity = [2]#[2,  8]
glob_scale = [40]

det_noise_type = ["simplex"]#["perlin", "simplex"]
det_octaves = [2]#[2, 4, 8]
det_persistence = [0.2]#[0.2, 0.8]
det_lacunarity = [2]#[2,  8]
det_scale = [40]

iterator = itertools.product(glob_noise_type, glob_octaves, glob_persistence, glob_lacunarity, glob_scale,det_noise_type,det_octaves ,det_persistence ,det_lacunarity , det_scale)

x = len(list(itertools.product(glob_noise_type, glob_octaves, glob_persistence, glob_lacunarity, glob_scale,det_noise_type,det_octaves ,det_persistence ,det_lacunarity , det_scale)))
print(f'aantal plaatjes: {x}')


def doeIteratie(glob_noise_type, glob_octaves, glob_persistence, glob_lacunarity, glob_scale, det_noise_type, det_octaves, det_persistence, det_lacunarity, det_scale):
    kleurInfo = kleurInfoOorspr.copy(deep=True)
    ptg = CanvasGeneratator(
        breedte=400,
        hoogte=400,
        kleur_verhoudingen=kleurInfo,
        versie=1,
        naam_basis=kleuren_naam,
        contrast=0.99,
        belichting=0.99,
        start_volgorde="grijsGroep",#hoofdKleur, grijsGroep
        kleur_manipulatie= "licht_donker_licht")

    ptg.generate_globale_topo(
        Id = "Glob1",
        noise_type = glob_noise_type,
        octaves = glob_octaves,
        persistence = glob_persistence,
        lacunarity = glob_lacunarity,
        scaleX = glob_scale,
        scaleY = glob_scale * 2
    )

    ptg.bereid_lokale_topos_voor()

    ptg.generate_locale_topo(
        Id = "Lok1",
        noise_type = det_noise_type,
        octaves = det_octaves,
        persistence = det_persistence,
        lacunarity = det_lacunarity,
        scaleX = det_scale,
        scaleY = det_scale * 2
    )

    fileNaam = str(datetime.now()) + ".jpg"

    picture = CamoPicture(ptg.canvas_detail, ptg.verdeling_in_N_naar_kleur)
    # picture.create_bolletjes()
    picture.create_vonoroi(schaal_X=3, schaal_Y=3, randomfactor_X=0, randomfactor_Y=0)
    #
    # picture.show()
    picture.save(plaatjes_dir, fileNaam)

    info = ptg.info + picture.info
    print()
    print(fileNaam)
    print(info)
    print(f'vergelijking kleurinfo gelijk: {kleurInfo.equals(kleurInfoOorspr)}')
    f = open(root_dir + "boekhouding.csv", "a")
    f.write(fileNaam + "," + info + "\n")
    f.close()
# print(list(iterator))
pool = Pool(processes=4)  # 10 processes
results = pool.starmap(doeIteratie, iterator)
print("klaar")

i = 1
