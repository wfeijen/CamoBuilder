import pandas as pd
from projectClasses.PerlinTopoGenerator import PerlinTopoGeneratator
from projectClasses.Camo_picture import CamoPicture
from projectClasses.RichtingGenerator import RichtingGenerator
from datetime import datetime

kleuren_naam = 'Almere nazomer1.jpg20221127 182223.csv'
# kleuren_naam = 'graslandZomer3.jpg20220108 134624.csv'

root_dir = '/media/willem/KleindSSD/machineLearningPictures/camoBuilder/camoOutput/'
kleurenPad = '../kleurParameters/' + kleuren_naam

kleurInfo = pd.read_csv(kleurenPad, index_col=0)


ptg = PerlinTopoGeneratator(
    breedte=1500,
    hoogte=1500,
    kleur_verhoudingen=kleurInfo,
    versie=3,
    naam_basis=kleuren_naam,
    richtingGenerator = RichtingGenerator([1,2,1,
                                           0,  0,
                                           1, 2, 1],
                        overall_max = 1),
    contrast=1,
    belichting=0.9)

ptg.generate_globale_topo(
    Id = "Glob1",
    aantal=600,
    blot_grootte_factor=0.6,
    min_blotgrootte= 0,
    max_blotgrootte= 10000,
    afplatting= 2,
    octaves=8,
    persistence=0.4,
    lacunarity=3.0,
    scaleX=81,
    scaleY=81,
    grenswaarde=0.60
)
ptg.bereid_lokale_topos_voor()

ptg.generate_locale_topo(
    Id="Det1",
    aantal=3000,
    blot_grootte_factor=0.7,
    min_blotgrootte= 10,
    max_blotgrootte= 2000,
    afplatting=1.5,
    octaves=8,
    persistence=0.3,
    lacunarity=5.0,
    scaleX=50,
    scaleY=200,
    grenswaarde=0.5)

ptg.generate_locale_topo(
    Id="Det2",
    aantal=3000,
    blot_grootte_factor=0.5,
    min_blotgrootte= 10,
    max_blotgrootte= 200,
    afplatting=1.5,
    max_waarde_stopconditie=200,
    octaves=8,
    persistence=0.3,
    lacunarity=5.0,
    scaleX=50,
    scaleY=200,
    grenswaarde=0.5)

fileNaam = str(datetime.now()) + ".jpg"
print(ptg.naam)

f=open(root_dir + "boekhouding.csv", "a")
f.write(fileNaam +  ","  + ptg.naam + "\n")
f.close()
picture = CamoPicture(ptg.canvas_detail, ptg.verdeling_in_N_naar_kleur)
# picture.show()
picture.save(root_dir, fileNaam)

i = 1

# ptg = PerlinTopoGeneratator(
#     breedte=1500,
#     hoogte=1500,
#     kleur_verhoudingen=kleurInfo,
#     versie=3,
#     naam_basis=kleuren_naam,
#     richtingGenerator = RichtingGenerator([1,2,1,
#                                            0,  0,
#                                            1, 2, 1],
#                         overall_max = 1),
#     contrast=1,
#     belichting=0.9)
#
# ptg.generate_globale_topo(
#     Id = "Glob1",
#     aantal=50,
#     blot_grootte_factor=0.6,
#     min_blotgrootte= 1000,
#     max_blotgrootte= 10000,
#     afplatting= 2,
#     octaves=4,
#     persistence=0.5,
#     lacunarity=6.0,
#     scaleX=101,
#     scaleY=101,
#     grenswaarde=0.40
# )
#
#
# ptg.generate_globale_topo(
#     Id="Glob2",
#     aantal=25,
#     blot_grootte_factor=0.6,
#     min_blotgrootte= 400,
#     max_blotgrootte= 2000,
#     afplatting=0.5,
#     octaves=4,
#     persistence=0.5,
#     lacunarity=6.0,
#     scaleX=101,
#     scaleY=101,
#     grenswaarde=0.40
# )
#
# ptg.richtingGenerator.overall_max = 10
#
# ptg.generate_globale_topo(
#     Id="Glob3",
#     aantal=50,
#     blot_grootte_factor=0.6,
#     min_blotgrootte= 400,
#     max_blotgrootte= 2000,
#     afplatting=2,
#     max_waarde_stopconditie=-100000,
#     octaves=4,
#     persistence=0.5,
#     lacunarity=6.0,
#     scaleX=101,
#     scaleY=101,
#     grenswaarde=0.40
# )
# # #
# #
# ptg.generate_globale_topo(
#     Id="Glob4",
#     aantal=150,
#     blot_grootte_factor=0.6,
#     min_blotgrootte= 200,
#     max_blotgrootte= 2000,
#     afplatting=3,
#     octaves=2,
#     persistence=0.6,
#     lacunarity=16.0,
#     scaleX=200,
#     scaleY=200,
#     grenswaarde=0.5)
#
# ptg.richtingGenerator.overall_max = 20
#
# ptg.generate_globale_topo(
#     Id="Glob5",
#     aantal=200,
#     blot_grootte_factor=0.4,
#     min_blotgrootte= 10,
#     max_blotgrootte= 2000,
#     afplatting=3,
#     max_waarde_stopconditie=200,
#     octaves=2,
#     persistence=0.4,
#     lacunarity=4.0,
#     scaleX=200,
#     scaleY=200,
#     grenswaarde=0.5)
#
# ptg.bereid_lokale_topos_voor()
#
# ptg.generate_locale_topo(
#     Id="Det1",
#     aantal=3000,
#     blot_grootte_factor=0.7,
#     min_blotgrootte= 10,
#     max_blotgrootte= 2000,
#     afplatting=1.5,
#     octaves=8,
#     persistence=0.3,
#     lacunarity=5.0,
#     scaleX=50,
#     scaleY=200,
#     grenswaarde=0.5)
#
# ptg.generate_locale_topo(
#     Id="Det2",
#     aantal=3000,
#     blot_grootte_factor=0.5,
#     min_blotgrootte= 10,
#     max_blotgrootte= 200,
#     afplatting=1.5,
#     max_waarde_stopconditie=200,
#     octaves=8,
#     persistence=0.3,
#     lacunarity=5.0,
#     scaleX=50,
#     scaleY=200,
#     grenswaarde=0.5)