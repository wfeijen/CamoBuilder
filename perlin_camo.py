import itertools

import pandas as pd
from projectClasses.PerlinTopoGenerator import PerlinTopoGeneratator
from projectClasses.Camo_picture import CamoPicture
from datetime import datetime
import numpy as np

kleuren_filenaam = 'c1_1.jpgkleurSchaduwMedian20230421 211330.csv'
# kleuren_naam = 'graslandZomer.jpg20230322 095001.csv'
# kleuren_naam = 'graslandZomer.jpg20230103 081900.csv'
# kleuren_naam = 'nazomerWinter2.jpg20230320 105239.csv'
# kleuren_naam = 'graslandZomer3.jpg20220108 134624.csv'



root_dir = '/media/willem/KleindSSD/machineLearningPictures/camoBuilder/'
plaatjes_dir = root_dir + 'camoOutput/'
kleurenPad = './kleurParameters/' + kleuren_filenaam

kleurInfo = pd.read_csv(kleurenPad, index_col=0)
# 2023-04-21 21:23:54.240054.jpg	c1_1.jpgkleurSchaduwMedian20230421 211330.csv	breedte	400	hoogte	400	contrast	0.99	belichting	0.99	kleurmanipulatie.licht_donker_licht
# 2023-04-21 21:49:18.193865.jpg	c1_1.jpgkleurSchaduwMedian20230421 211330.csv	breedte	400	hoogte	400	contrast	0.99	belichting	0.99	kleurmanipulatie.licht_donker_licht
# 2023-04-21 21:25:04.955890.jpg	c1_1.jpgkleurSchaduwMedian20230421 211330.csv	breedte	400	hoogte	400	contrast	0.99	belichting	0.99	kleurmanipulatie.licht_donker_licht
# 2023-04-21 21:36:38.829286.jpg	c1_1.jpgkleurSchaduwMedian20230421 211330.csv	breedte	400	hoogte	400	contrast	0.99	belichting	0.99	kleurmanipulatie.licht_donker_licht
# 2023-04-21 21:40:04.897846.jpg	c1_1.jpgkleurSchaduwMedian20230421 211330.csv	breedte	400	hoogte	400	contrast	0.99	belichting	0.99	kleurmanipulatie.licht_donker_licht
# 2023-04-21 21:40:38.190401.jpg	c1_1.jpgkleurSchaduwMedian20230421 211330.csv	breedte	400	hoogte	400	contrast	0.99	belichting	0.99	kleurmanipulatie.licht_donker_licht
# 2023-04-21 21:46:34.674861.jpg	c1_1.jpgkleurSchaduwMedian20230421 211330.csv	breedte	400	hoogte	400	contrast	0.99	belichting	0.99	kleurmanipulatie.licht_donker_licht
# 2023-04-21 21:50:13.491196.jpg	c1_1.jpgkleurSchaduwMedian20230421 211330.csv	breedte	400	hoogte	400	contrast	0.99	belichting	0.99	kleurmanipulatie.licht_donker_licht
# 2023-04-21 21:52:36.233683.jpg	c1_1.jpgkleurSchaduwMedian20230421 211330.csv	breedte	400	hoogte	400	contrast	0.99	belichting	0.99	kleurmanipulatie.licht_donker_licht
# 2023-04-21 21:58:32.253815.jpg	c1_1.jpgkleurSchaduwMedian20230421 211330.csv	breedte	400	hoogte	400	contrast	0.99	belichting	0.99	kleurmanipulatie.licht_donker_licht
ptg = PerlinTopoGeneratator(
    breedte=400,
    hoogte=400,
    kleur_verhoudingen=kleurInfo,
    versie=3,
    naam_basis=kleuren_filenaam,
    contrast=0.99,
    belichting=0.8,
    start_volgorde="hoofdKleur",#hoofdKleur, grijsGroep
    kleur_manipulatie="licht_donker_licht")

# globaal	noise	simplex	o	2	per	0.8	lan	8	scaleX	40	scaleY	80	base	1	grens	0
# globaal	noise	simplex	o	4	per	0.8	lan	8	scaleX	40	scaleY	80	base	1	grens	0
# globaal	noise	simplex	o	2	per	0.8	lan	8	scaleX	40	scaleY	80	base	1	grens	0
# globaal	noise	simplex	o	2	per	0.8	lan	8	scaleX	40	scaleY	80	base	1	grens	0
# globaal	noise	simplex	o	4	per	0.8	lan	2	scaleX	40	scaleY	80	base	1	grens	0
# globaal	noise	simplex	o	4	per	0.8	lan	2	scaleX	40	scaleY	80	base	1	grens	0
# globaal	noise	simplex	o	4	per	0.8	lan	2	scaleX	40	scaleY	80	base	1	grens	0
# globaal	noise	simplex	o	4	per	0.8	lan	8	scaleX	40	scaleY	80	base	1	grens	0
# globaal	noise	simplex	o	8	per	0.8	lan	2	scaleX	40	scaleY	80	base	1	grens	0
# globaal	noise	simplex	o	8	per	0.8	lan	2	scaleX	40	scaleY	80	base	1	grens	0
ptg.generate_globale_topo(
    Id = "Glob1",
    noise_type = "simplex",
    octaves = 8,
    persistence = 0.8,
    lacunarity = 2,
    scaleX = 30,
    scaleY = 60
)

ptg.bereid_lokale_topos_voor()
# lokaal		noise	simplex	o	4	per	0.8	lan	2	scaleX	40	scaleY	80	base	2	grens	0	vor_sx	3	vor_sy	3	_rx	0	_ry	0
# lokaal		noise	simplex	o	4	per	0.8	lan	8	scaleX	40	scaleY	80	base	2	grens	0	vor_sx	3	vor_sy	3	_rx	0	_ry	0
# lokaal		noise	perlin	o	2	per	0.8	lan	8	scaleX	40	scaleY	80	base	2	grens	0	vor_sx	3	vor_sy	3	_rx	0	_ry	0
# lokaal		noise	simplex	o	8	per	0.8	lan	2	scaleX	40	scaleY	80	base	2	grens	0	vor_sx	3	vor_sy	3	_rx	0	_ry	0
# lokaal		noise	simplex	o	4	per	0.8	lan	2	scaleX	40	scaleY	80	base	2	grens	0	vor_sx	3	vor_sy	3	_rx	0	_ry	0
# lokaal		noise	perlin	o	4	per	0.8	lan	2	scaleX	40	scaleY	80	base	2	grens	0	vor_sx	3	vor_sy	3	_rx	0	_ry	0
# lokaal		noise	simplex	o	2	per	0.8	lan	8	scaleX	40	scaleY	80	base	2	grens	0	vor_sx	3	vor_sy	3	_rx	0	_ry	0
# lokaal		noise	perlin / simplex	o	8	per	0.8	lan	2	scaleX	40	scaleY	80	base	2	grens	0	vor_sx	3	vor_sy	3	_rx	0	_ry	0
# lokaal		noise	simplex	o	2	per	0.8	lan	8	scaleX	40	scaleY	80	base	2	grens	0	vor_sx	3	vor_sy	3	_rx	0	_ry	0
# lokaal		noise	simplex	o	8	per	0.8	lan	2	scaleX	40	scaleY	80	base	2	grens	0	vor_sx	3	vor_sy	3	_rx	0	_ry	0
ptg.generate_locale_topo(
    Id = "Lok1",
    noise_type = "simplex",
    octaves = 8,
    persistence = 0.8,
    lacunarity = 2,
    scaleX = 20,
    scaleY = 80
)

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
