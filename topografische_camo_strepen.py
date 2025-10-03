#%%
import pandas as pd
import numpy as np
from projectClasses.CanvasGenerator import CanvasGeneratator
from projectClasses.TopoGenerator import TopoGenerator
from projectClasses.Camo_picture import CamoPicture
from projectClasses.kleurbeheer import maak_color_card_op_basis_van_lijst_met_kleuren, corrigeer_kleuren, pas_kleuren_aan_met_parameters
from datetime import datetime
from PIL import ImageCms

kleuren_filenaam = 'genuanceerd_groen_bruin6.jpgkleurSchaduwCentroid:1_20240405 143510.csv'
#'genuanceerd_groen_bruin6.jpgkleurSchaduwCentroid:1_20240407 231414_4x12.csv'

root_dir = '/home/willem/Pictures/Camouflage/camoBuilder/'
plaatjes_dir = root_dir + 'camoOutput/'
kleurenPad = './kleurParameters/' + kleuren_filenaam

kleuren = pd.read_csv(kleurenPad, index_col=0)
#%%
kleuren, info_voor_boekhouding = pas_kleuren_aan_met_parameters(
    kleuren_in=kleuren,
    contrast= 1.5,
    saturation = 0.8,
    belichting=1,
    gewicht_extremen=10,
    macht_kleur= 2)

versie = 3

kleuren_kleurenkaart = kleuren.copy(deep=True)


# kleuren[['R', 'G', 'B']] = corrigeer_kleuren(van_schema_filenaam='lexmark_kleuren.pkl',
#                                 naar_schema_filenaam='origineel_kleuren.pkl',
#                                 kleurinfo_in=kleuren)
 #%%

# kleuren[['R', 'G', 'B']] = corrigeer_kleuren(naar_schema_filenaam='tshirt_kleuren_verzamel.pkl',
#                                 van_schema_filenaam='origineel_kleuren_verzamel.pkl',
#                                 kleurinfo_in=kleuren)
# kleuren_kleurenkaart = pd.concat([kleuren_kleurenkaart, kleuren])
kleurenkaart = maak_color_card_op_basis_van_lijst_met_kleuren(kleuren_kleurenkaart, square_size=100)

# 22023-10-27 20:04:10.992090.jpg	bruin_groen_contrast_230518e.jpgkleurSchaduwMedian20230608 111525.csv	breedte	300	hoogte	300	contrast	1	saturation	0.8	belichting	0.9	start_volgorde	hoofdKleur	kleurmanipulatie	oplopend	Id	

canvasGenerator = CanvasGeneratator(
    breedte=650,
    hoogte=650,
    kleur_verhoudingen=kleuren,
    naam_basis=kleuren_filenaam,
    kleur_info_voor_boekhouding=info_voor_boekhouding,
    start_volgorde="hoofdKleur",#hoofdKleur, grijsGroep
    kleur_manipulatie="oplopend") #licht_donker_licht, oplopend

topoGenerator = TopoGenerator(versie=versie,
                              breedte=canvasGenerator.breedte,
                              hoogte=canvasGenerator.hoogte,
                              N= canvasGenerator.aantal_globale_kleurgroepen
                            )





# Id	Glob1	noise	simplex	o	4	per	1.2	lan	4	scaleX	100	scaleY	30	versie	3	bereik	1	
topografieGlobaal = topoGenerator.genereer_1_noise(
    Id = "Glob1",
    noise_type="simplex",
    octaves=4,
    persistence=1.2,
    lacunarity=4,
    scaleX=200,
    scaleY=60,
    bereik=5
)



# Id	Lok1	noise	simplex	o	8	per	0.1	lan	2	scaleX	70	scaleY	30	versie	4	bereik	1	
topografieLokaal = topoGenerator.genereer_N_noise(
    Id = "Lok1",
    noise_type="simplex",
    octaves=8,
    persistence=0.1,
    lacunarity=2,
    scaleX=140,
    scaleY=60,
    bereik=10
)

# # MachtId	Lok1	macht	3	bereik	3	
# topografieLokaal = topoGenerator.verhef_tot_macht(Id = "Lok1",
#                                                   topo_in=topografieLokaal, 
#                                                   macht=3, 
#                                                   bereik=3)

#Id	Lok2	noise	simplex	o	4	per	0.8	lan	2	scaleX	20	scaleY	70	versie	7	bereik	1	
topografieLokaal2 = topoGenerator.genereer_N_noise(
    Id = "Lok2",
    noise_type = "simplex",
    octaves = 4,
    persistence = 0.8,
    lacunarity = 2,
    scaleX = 40,
    scaleY = 140,
    bereik = 0.7
)


topografieLokaal += topografieLokaal2

#%%
ribbels_x = topoGenerator.tilt_N_canvas(Id="Tilt1", 
                                        topos_in=topografieLokaal, 
                                        tilt_x=0.2, 
                                        tilt_y=0)

#%%
topografieLokaal = topografieLokaal + ribbels_x
#%%
topografieLokaal = topoGenerator.modulo_N_canvas(Id="Mod1", 
                                          topos_in=topografieLokaal, 
                                          grens=10)

#%%
canvasGenerator.maakGlobaalCanvas(topografieGlobaal)
#%%
canvasGenerator.generate_locale_topo(topografieLokaal)

fileNaam = str(datetime.now())
x, y = topografieGlobaal.shape
puntdelta = np.zeros((x, y, 2))

picture = CamoPicture(canvasGenerator.canvas_detail, puntdelta, canvasGenerator.verdeling_in_N_naar_kleur)
#vor_sy	40	_rx	0	_ry	0
picture.create_vonoroi(schaal_X=5, schaal_Y=5, randomfactor_X=10, randomfactor_Y=10)

# picture.show()
picture.save(plaatjes_dir, fileNaam)


info = canvasGenerator.info + topoGenerator.info + picture.info
print(info)
f = open(root_dir + "boekhouding.csv", "a")
f.write(fileNaam + ".jpg," + info + "\n")
f.close()
print(fileNaam)
i = 1

fileNaam = str(datetime.now()) + "_xpalet"

profile = ImageCms.createProfile("sRGB")
kleurenkaart.save(plaatjes_dir + fileNaam + ".jpg", icc_profile=ImageCms.ImageCmsProfile(profile).tobytes())



# %%
