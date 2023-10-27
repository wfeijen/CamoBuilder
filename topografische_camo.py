#%%
import pandas as pd
import numpy as np
from projectClasses.CanvasGenerator import CanvasGeneratator
from projectClasses.TopoGenerator import TopoGenerator
from projectClasses.Camo_picture import CamoPicture
from projectClasses.Utilities import corrigeer_kleuren
from datetime import datetime

kleuren_filenaam = 'bruin_groen_contrast_230518e.jpgkleurSchaduwMedian20230608 111525.csv'

root_dir = '/home/willem/Pictures/Camouflage/camoBuilder/'
plaatjes_dir = root_dir + 'camoOutput/'
kleurenPad = './kleurParameters/' + kleuren_filenaam

kleurInfo = pd.read_csv(kleurenPad, index_col=0)

canvasGenerator = CanvasGeneratator(
    breedte=300,
    hoogte=300,
    kleur_verhoudingen=kleurInfo,
    naam_basis=kleuren_filenaam,
    contrast= 1,
    saturation = 0.8,
    belichting=0.9,
    start_volgorde="hoofdKleur",#hoofdKleur, grijsGroep
    kleur_manipulatie="oplopend") #licht_donker_licht, oplopend

topoGenerator = TopoGenerator(versie=1,
                              breedte=canvasGenerator.breedte,
                              hoogte=canvasGenerator.hoogte)


punt_randomisatie_X = topoGenerator.genereer_1_noise(
    Id = "PX",
    noise_type="simplex",
    octaves=3,
    persistence=0.4,
    lacunarity=2,
    scaleX=100,
    scaleY=35,
    bereik=5
)

punt_randomisatie_Y = topoGenerator.genereer_1_noise(
    Id = "PY",
    noise_type="simplex",
    octaves=3,
    persistence=0.4,
    lacunarity=2,
    scaleX=100,
    scaleY=35,
    bereik=5
)

pointsDelta = np.vstack(([punt_randomisatie_X.T], [punt_randomisatie_Y.T])).T

x = []
topografieGlobaal = topoGenerator.genereer_1_noise(
    Id = "Glob1",
    noise_type="simplex",
    octaves=4,
    persistence=0.8,
    lacunarity=4,
    scaleX=100,
    scaleY=30,
    bereik=1
)

topografieGlobaal += topoGenerator.genereer_1_noise(
    Id = "Glob2",
    noise_type="simplex",
    octaves=4,
    persistence=0.8,
    lacunarity=4,
    scaleX=200,
    scaleY=70,
    bereik=100
)

topografieGlobaal = topoGenerator.verhef_tot_macht(Id = "Lok1",
                                                  topo_in=topografieGlobaal, 
                                                  macht=3, 
                                                  bereik=1)

topografieLokaal = topoGenerator.genereer_N_noise(
    N = canvasGenerator.aantal_globale_kleurgroepen,
    Id = "Lok1",
    noise_type="simplex",
    octaves=2,
    persistence=0.6,
    lacunarity=3,
    scaleX=70,
    scaleY=30,
    bereik=1
)

topografieLokaal = topoGenerator.verhef_tot_macht(Id = "Lok1",
                                                  topo_in=topografieLokaal, 
                                                  macht=3, 
                                                  bereik=3)

topografieLokaal = topoGenerator.vouw_over_grens_en_schaal(
    Id = "Lok1",
    topo_in=topografieLokaal,
    grens=0,
    bereik=1
)

topografieLokaal2 = topoGenerator.genereer_N_noise(
    N=canvasGenerator.aantal_globale_kleurgroepen,
    Id = "Lok2",
    noise_type = "simplex",
    octaves = 4,
    persistence = 0.8,
    lacunarity = 2,
    scaleX = 20,
    scaleY = 70,
    bereik = 3
)

topografieLokaal2 = topoGenerator.verhef_tot_macht(Id = "Lok2",
                                                  topo_in=topografieLokaal2, 
                                                  macht=3, 
                                                  bereik=1)

topografieLokaal += topografieLokaal2

canvasGenerator.maakGlobaalCanvas(topografieGlobaal)
canvasGenerator.generate_locale_topo(topografieLokaal)

fileNaam = str(datetime.now()) + ".jpg"


picture = CamoPicture(canvasGenerator.canvas_detail, pointsDelta, canvasGenerator.verdeling_in_N_naar_kleur)

picture.create_vonoroi(schaal_X=40, schaal_Y=40, randomfactor_X=1, randomfactor_Y=1)

# picture.show()
picture.save(plaatjes_dir, fileNaam)

info = canvasGenerator.info + topoGenerator.info + picture.info
print(info)
f = open(root_dir + "boekhouding.csv", "a")
f.write(fileNaam + "," + info + "\n")
f.close()
print(fileNaam)
i = 1

# %%
