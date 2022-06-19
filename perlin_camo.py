import pandas as pd
from projectClasses.PerlinTopoGenerator import PerlinTopoGeneratator
from projectClasses.Camo_picture import CamoPicture

kleuren_naam = '8000x8000.jpgRGB20220613 191417'
# kleuren_naam = 'lenteOostvaardersplassen_1.2.jpgRGB20220613 091203'

root_dir = '/mnt/GroteSchijf/machineLearningPictures/camoBuilder/camoOutput/'
kleurenPad = '../kleurParameters/' + kleuren_naam + '.csv'

kleurInfo = pd.read_csv(kleurenPad, index_col=0)

ptg = PerlinTopoGeneratator(
    breedte=1500,
    hoogte=1500,
    kleur_verhoudingen=kleurInfo,
    percentage_donker_licht=0.05,
    versie=4,
    naam_basis=kleuren_naam)

ptg.generate_globale_topo(
    aantal=400,
    blot_grootte_factor=0.8,
    afplatting=5,
    octaves=8,
    persistence=0.4,
    lacunarity=3.0,
    scaleX=80,
    scaleY=80,
    grenswaarde=0.5,
    richting_kans_verdeling_lb_ro=(1, 1, 1,
                                   1, 1,
                                   1, 0, 1))

ptg.generate_locale_topo(
    aantal=3000,
    blot_grootte_factor=1,
    afplatting=8,
    octaves=8,
    persistence=0.3,
    lacunarity=4.0,
    scaleX=50,
    scaleY=50,
    grenswaarde=0.5)

print(ptg.naam)
picture = CamoPicture(ptg.canvas_detail, ptg.dict_kleurnummer_kleur)
# picture.show()
picture.save(root_dir, ptg.naam)

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
