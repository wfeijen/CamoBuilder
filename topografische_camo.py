#%%
import pandas as pd
import numpy as np
from projectClasses.CanvasGenerator import CanvasGeneratator
from projectClasses.TopoGenerator import TopoGenerator
from projectClasses.Camo_picture import CamoPicture
from projectClasses.Utilities import corrigeer_kleuren
from datetime import datetime

kleuren_filenaam = 'genuanceerd_groen_bruin6.jpgkleurSchaduwMedian20231029 162405.csv'

root_dir = '/home/willem/Pictures/Camouflage/camoBuilder/'
plaatjes_dir = root_dir + 'camoOutput/'
kleurenPad = './kleurParameters/' + kleuren_filenaam

kleurInfo = pd.read_csv(kleurenPad, index_col=0)


kleurInfo[['R', 'G', 'B']] = corrigeer_kleuren(van_schema_filenaam='lexmark_kleuren.pkl',
                                naar_schema_filenaam='origineel_kleuren.pkl',
                                kleurinfo_in=kleurInfo)

# 22023-10-27 20:04:10.992090.jpg	bruin_groen_contrast_230518e.jpgkleurSchaduwMedian20230608 111525.csv	breedte	300	hoogte	300	contrast	1	saturation	0.8	belichting	0.9	start_volgorde	hoofdKleur	kleurmanipulatie	oplopend	Id	

canvasGenerator = CanvasGeneratator(
    breedte=300,
    hoogte=300,
    kleur_verhoudingen=kleurInfo,
    naam_basis=kleuren_filenaam,
    contrast= 0.7,
    saturation = 0.8,
    belichting=0.9,
    start_volgorde="hoofdKleur",#hoofdKleur, grijsGroep
    kleur_manipulatie="oplopend") #licht_donker_licht, oplopend

topoGenerator = TopoGenerator(versie=1,
                              breedte=canvasGenerator.breedte,
                              hoogte=canvasGenerator.hoogte,
                              N= canvasGenerator.aantal_globale_kleurgroepen
                            )


# PX	noise	simplex	o	3	per	2	lan	3	scaleX	100	scaleY	35	versie	1	bereik	5	Id	
punt_randomisatie_X = topoGenerator.genereer_1_noise(
    Id = "PX",
    noise_type="simplex",
    octaves=3,
    persistence=2,
    lacunarity=3,
    scaleX=100,
    scaleY=35,
    bereik=5
)
# PY	noise	simplex	o	3	per	2	lan	3	scaleX	100	scaleY	35	versie	2	bereik	5	
punt_randomisatie_Y = topoGenerator.genereer_1_noise(
    Id = "PY",
    noise_type="simplex",
    octaves=3,
    persistence=2,
    lacunarity=3,
    scaleX=100,
    scaleY=35,
    bereik=5
)

pointsDelta = np.vstack(([punt_randomisatie_X.T], [punt_randomisatie_Y.T])).T

# Id	Glob1	noise	simplex	o	4	per	1.2	lan	4	scaleX	100	scaleY	30	versie	3	bereik	1	
topografieGlobaal = topoGenerator.genereer_1_noise(
    Id = "Glob1",
    noise_type="simplex",
    octaves=4,
    persistence=1.2,
    lacunarity=4,
    scaleX=100,
    scaleY=30,
    bereik=1
)

# Id	Lok1	noise	simplex	o	8	per	0.1	lan	2	scaleX	70	scaleY	30	versie	4	bereik	1	
topografieLokaal = topoGenerator.genereer_N_noise(
    Id = "Lok1",
    noise_type="simplex",
    octaves=8,
    persistence=0.1,
    lacunarity=2,
    scaleX=70,
    scaleY=30,
    bereik=1
)

# MachtId	Lok1	macht	3	bereik	3	
topografieLokaal = topoGenerator.verhef_tot_macht(Id = "Lok1",
                                                  topo_in=topografieLokaal, 
                                                  macht=3, 
                                                  bereik=3)

#Id	Lok2	noise	simplex	o	4	per	0.8	lan	2	scaleX	20	scaleY	70	versie	7	bereik	1	
topografieLokaal2 = topoGenerator.genereer_N_noise(
    Id = "Lok2",
    noise_type = "simplex",
    octaves = 4,
    persistence = 0.8,
    lacunarity = 2,
    scaleX = 20,
    scaleY = 70,
    bereik = 1
)

# MachtId	Lok2	macht	3	bereik	3	
topografieLokaal2 = topoGenerator.verhef_tot_macht(Id = "Lok2",
                                                  topo_in=topografieLokaal2, 
                                                  macht=3, 
                                                  bereik=3)

topografieLokaal += topografieLokaal2

canvasGenerator.maakGlobaalCanvas(topografieGlobaal)
canvasGenerator.generate_locale_topo(topografieLokaal)

fileNaam = str(datetime.now()) + ".jpg"


picture = CamoPicture(canvasGenerator.canvas_detail, pointsDelta, canvasGenerator.verdeling_in_N_naar_kleur)
#vor_sy	40	_rx	0	_ry	0
picture.create_vonoroi(schaal_X=40, schaal_Y=40, randomfactor_X=3, randomfactor_Y=3)

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
