#%%
import pandas as pd
import numpy as np
from projectClasses.CanvasGenerator import CanvasGeneratator
from projectClasses.TopoGenerator import TopoGenerator
from projectClasses.Camo_picture import CamoPicture
from datetime import datetime

kleuren_filenaam = 'blauw_en_veel_wit.jpgkleurSchaduwMedian20230708 150749.csv'

root_dir = '/home/willem/Pictures/Camouflage/camoBuilder/'
plaatjes_dir = root_dir + 'camoOutput/'
kleurenPad = './kleurParameters/' + kleuren_filenaam

kleurInfo = pd.read_csv(kleurenPad, index_col=0)

# 2023-06-10 15:22:05.587923.jpg	bruin_groen_contrast_230518e.jpgkleurSchaduwMedian20230608 111525.csv	breedte	260	hoogte	300	contrast	1	saturation	0.8	belichting	0.9	start_volgorde	hoofdKleur	kleurmanipulatie	oplopend

canvasGenerator = CanvasGeneratator(
    breedte=300,
    hoogte=300,
    kleur_verhoudingen=kleurInfo,
    naam_basis=kleuren_filenaam,
    contrast= 1,
    saturation = 0.99,
    belichting=0.99,
    start_volgorde="hoofdKleur",#hoofdKleur, grijsGroep
    kleur_manipulatie="oplopend") #licht_donker_licht, oplopend

topoGenerator = TopoGenerator(versie=9,
                              breedte=canvasGenerator.breedte,
                              hoogte=canvasGenerator.hoogte)

# Id	Glob1	noise	simplex	o	4	per	0.8	lan	4	scaleX	100	scaleY	30	versie	1	macht	1	bereik	1

x = []
topografieGlobaal = topoGenerator.genereer_1(
    Id = "Glob1",
    noise_type="simplex",
    octaves=4,
    persistence=0.8,
    lacunarity=4,
    scaleX=100,
    scaleY=30,
    macht=1,
    bereik=1
)

# Id	Glob2	noise	simplex	o	4	per	0.8	lan	4	scaleX	200	scaleY	70	versie	2	macht	3	bereik	100
topografieGlobaal += topoGenerator.genereer_1(
    Id = "Glob2",
    noise_type="simplex",
    octaves=4,
    persistence=0.8,
    lacunarity=4,
    scaleX=200,
    scaleY=70,
    macht=3,
    bereik=1
)

# x = topoGenerator.binair_1(
#     Id="GlobInverse",
#     noise_type="simplex",
#     octaves=1,
#     persistence=0,
#     lacunarity=1,
#     scaleX=800,
#     scaleY=800,
#     ondergrens=-0.3,
#     bovengrens=0.3
# )
# print(np.linalg.norm(x))
# topografieGlobaal *= x

# Id	Lok1	noise	simplex	o	3	per	0.8	lan	4	scaleX	70	scaleY	30	versie	3	macht	3	bereik	3
topografieLokaal = topoGenerator.genereer_N(
    N = canvasGenerator.aantal_globale_kleurgroepen,
    Id = "Lok1",
    noise_type="simplex",
    octaves=3,
    persistence=0.8,
    lacunarity=4,
    scaleX=70,
    scaleY=30,
    macht=3,
    bereik=1
)


# Id	Lok2	noise	simplex	o	4	per	0.8	lan	2	scaleX	20	scaleY	70	versie	6	macht	3	bereik	3	vor_sx	40	vor_sy	40	_rx	3	_ry	3
topografieLokaal += topoGenerator.genereer_N(
    N=canvasGenerator.aantal_globale_kleurgroepen,
    Id = "Lok2",
    noise_type = "simplex",
    octaves = 4,
    persistence = 0.8,
    lacunarity = 2,
    scaleX = 20,
    scaleY = 70,
    macht = 3,
    bereik = 1
)

# topografieLokaal *= topoGenerator.binair_1_n(
#     N=canvasGenerator.aantal_globale_kleurgroepen,
#     Id="DetInverse",
#     noise_type="perlin",
#     octaves=1,
#     persistence=0,
#     lacunarity=1,
#     scaleX=100,
#     scaleY=100,
#     ondergrens=0,
#     bovengrens=1000
# )


canvasGenerator.maakGlobaalCanvas(topografieGlobaal)
canvasGenerator.generate_locale_topo(topografieLokaal)

fileNaam = str(datetime.now()) + ".jpg"


picture = CamoPicture(canvasGenerator.canvas_detail, canvasGenerator.verdeling_in_N_naar_kleur)
# picture.create_bolletjes()
picture.create_vonoroi(schaal_X=40, schaal_Y=40, randomfactor_X=3, randomfactor_Y=3)
#
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
