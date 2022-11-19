import pandas as pd
from projectClasses.PerlinTopoGenerator import PerlinTopoGeneratator
from projectClasses.Camo_picture import CamoPicture
from projectClasses.RichtingGenerator import RichtingGenerator
from datetime import datetime

kleuren_naam = 'Almere nazomer1.jpg20221118 134755.csv'
# kleuren_naam = 'graslandZomer3.jpg20220108 134624.csv'

root_dir = '/media/willem/KleineSSD/machineLearningPictures/camoBuilder/camoOutput/'
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
                        overall_max = 0),
    kleur_samentrekking=1)

ptg.generate_globale_topo(
    Id = "Glob1",
    aantal=50,
    blot_grootte_factor=0.8,
    min_blotgrootte= 1000,
    max_blotgrootte= 10000,
    afplatting= 2,
    persistence=0.5,
    lacunarity=6.0,
    octaves=4,
    scaleX=100,
    scaleY=100,
    grenswaarde=0.4
)


ptg.generate_globale_topo(
    Id="Glob2",
    aantal=100,
    blot_grootte_factor=0.8,
    min_blotgrootte= 400,
    max_blotgrootte= 2000,
    afplatting=0.5,
    persistence=0.5,
    lacunarity=6.0,
    octaves=4,
    scaleX=100,
    scaleY=100,
    grenswaarde=0.4)
#

ptg.richtingGenerator.overall_max = 5

ptg.generate_globale_topo(
    Id="Glob3",
    aantal=150,
    blot_grootte_factor=0.8,
    min_blotgrootte= 200,
    max_blotgrootte= 2000,
    afplatting=2,
    persistence=0.6,
    lacunarity=16.0,
    octaves=2,
    scaleX=200,
    scaleY=200,
    grenswaarde=0.5)

ptg.richtingGenerator.overall_max = 10
#
ptg.generate_globale_topo(
    Id="Glob4",
    aantal=200,
    blot_grootte_factor=0.8,
    min_blotgrootte= 10,
    max_blotgrootte= 2000,
    afplatting=2,
    persistence=0.6,
    lacunarity=16.0,
    octaves=2,
    scaleX=200,
    scaleY=200,
    grenswaarde=0.5)

ptg.bereid_lokale_topos_voor()

ptg.generate_locale_topo(
    Id="Det1",
    aantal=6000,
    blot_grootte_factor=0.9,
    min_blotgrootte= 10,
    max_blotgrootte= 200,
    octaves=8,
    persistence=0.3,
    lacunarity=5.0,
    scaleX=50,
    scaleY=200,
    afplatting=1.5,
    grenswaarde=0.5)

fileNaam = str(datetime.now()) + ".jpg"
print(ptg.naam)

f=open(root_dir + "/boekhouding.csv", "a")
f.write(fileNaam +  ","  + ptg.naam + "\n")
f.close()
picture = CamoPicture(ptg.canvas_detail, ptg.verdeling_in_N_naar_kleur)
# picture.show()
picture.save(root_dir, fileNaam)

i = 1

# ptg.generate_globale_topo(
#     aantal = 150,
#     persistence=0.2,
#     lacunarity=2.0,
#     octaves=8,
#     scaleX=50,
#     scaleY=100,
#     grenswaarde=0.5)

# ptg.generate_globale_topo(
#     aantal = 150,
#     persistence=0.3,
#     lacunarity=4.0,
#     octaves=4,
#     scaleX=300,
#     scaleY=300,
#     grenswaarde=0.5)

# ptg = PerlinTopoGeneratator(
#     breedte=1500,
#     hoogte=2000,
#     aantal_globaal=100,
#     aantal_detail=3,
#     kleur_verhoudingen=kleurInfo,
#     persistence=0.3,
#     lacunarity=8.0,
#     octaves=8,
#     scaleX=200,
#     scaleY=200,
#     grenswaarde=0.3,
#     versie = 1)

# ptg = PerlinTopoGeneratator(
#     breedte=1500,
#     hoogte=2000,
#     aantal_globaal=100,
#     aantal_detail=3,
#     kleur_verhoudingen=kleurInfo,
#     octaves=8,
#     persistence=0.2,
#     lacunarity=2.0,
#     scaleX=100,
#     scaleY=200,
#     grenswaarde=0.3,
#     versie = 1)

# def show_general_canvas(canvas):
#     max = np.amax(canvas)
#     print(max)
#     print(np.amax(canvas))
#     canvas_grens = np.uint8(canvas * 255 / max)
#     Image.fromarray(canvas_grens).show()
#     img = Image.new('RGB', canvas.shape, (255, 255, 255))
#     pix = img.load()
#     maxX, maxY = canvas.shape
#     for x in range(maxX):
#         for y in range(maxY):
#             pix[x, y] = (canvas_grens[x, y], 0, 0)
#     img.show()
