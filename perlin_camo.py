import pandas as pd
from projectClasses.PerlinTopoGenerator import PerlinTopoGeneratator
from projectClasses.Camo_picture import CamoPicture

kleuren_naam = 'graslandZomer3.jpg20220224 134905'
# kleuren_naam = 'graslandZomer3.jpg20220108 134624.csv'

root_dir = '/mnt/GroteSchijf/machineLearningPictures/camoBuilder/camoOutput/'
kleurenPad = '../kleurParameters/' + kleuren_naam + '.csv'
kleurenpad_donker_licht = '../kleurParameters/' + kleuren_naam + 'lichtDonker.csv'

kleurInfo = pd.read_csv(kleurenPad, index_col=0)
donker_licht_info = pd.read_csv(kleurenpad_donker_licht, index_col=0)

ptg = PerlinTopoGeneratator(
    breedte=1500,
    hoogte=1500,
    kleur_verhoudingen=kleurInfo,
    ondergrens_donker_licht=0.02,
    versie=2,
    naam_basis=kleuren_naam)

ptg.generate_globale_topo(
    aantal=300,
    blot_grootte_factor=0.3,
    octaves=8,
    persistence=0.4,
    lacunarity=4.0,
    scaleX=100,
    scaleY=100,
    grenswaarde=0.5,
    afplatting=3,
    richting_kans_verdeling_lb_ro=(3, 5, 3,
                                   1, 1,
                                   1, 0, 1))

ptg.generate_locale_topo(
    aantal=6000,
    blot_grootte_factor=1,
    octaves=8,
    persistence=0.3,
    lacunarity=4.0,
    scaleX=50,
    scaleY=50,
    grenswaarde=0.5,
    afplatting=10)

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
