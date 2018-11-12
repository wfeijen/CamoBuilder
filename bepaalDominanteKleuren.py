#Doel:
#   Bepalen dominante kleuren
#   bepalen welke kleuren daar onder vallen
#   bepalen schaduw licht verdeling
#   wegschrijven verdeling
#   wegschrijven foto in nieuwe kleuren

import numpy
from PIL import Image, ImageCms
from math import hypot
import datetime
from os import listdir

#Parameters
dir = "C:/Users\wfeij/PycharmProjects/Camo builder/bepaalDominanteKleuren"

class ColorParameters:
    def __init__(self, a, b, origineel):
        self.a = a
        self.b = b
        self.waardeOrigineel = origineel
        self.waardeGecorrigeerd = 0
        self.vervangenDoor = self
        self.vervangt = []

def bepaalWaardenEnPasAan(dir, name):
    #Inlezen file
    im = Image.open(dir + "/" + name)
    if im.mode != "RGB":
      im = im.convert("RGB")


    srgb_profile = ImageCms.createProfile("sRGB")
    lab_profile  = ImageCms.createProfile("LAB")

    rgb2lab_transform = ImageCms.buildTransformFromOpenProfiles(srgb_profile, lab_profile, "RGB", "LAB")
    lab_im = ImageCms.applyTransform(im, rgb2lab_transform)
    w, h = lab_im.size
    labColors = lab_im.getcolors(w*h)

    labColorsGeenLD = {}
    for color in labColors:
        col = (color[1][1],color[1][2])
        aant = color[0]
        if col in labColorsGeenLD:
            labColorsGeenLD[col] = labColorsGeenLD[col] + aant
        else:
            labColorsGeenLD[col] = aant
    print(str(len(labColorsGeenLD)))

    colorParametersList = []
    for  (a,b) , aant in labColorsGeenLD.items():
        colorParametersList.append(ColorParameters(a,b,aant))



    for eigen in colorParametersList:
        for buur in colorParametersList:
            afstand = int(hypot((eigen.a - buur.a), (eigen.b - buur.b))) # math.sqrt 60.234
            if afstand > 0:
                eigen.waardeGecorrigeerd = eigen.waardeGecorrigeerd + buur.waardeOrigineel // afstand
            else:
                eigen.waardeGecorrigeerd = eigen.waardeGecorrigeerd + buur.waardeOrigineel

    wegstreeplijst = sorted(colorParametersList, key=lambda x: x.waardeGecorrigeerd, reverse=True)


    #belangrijkste kleuren
    hoofdkleurenLijst = []
    while len(wegstreeplijst) > 0:
        hoofdKleur = wegstreeplijst[0]
        wegstreeplijst.remove(hoofdKleur)
        for kleur in wegstreeplijst:
            afstand = int(hypot((hoofdKleur.a - kleur.a), (hoofdKleur.b - kleur.b)))
            kleur.waardeGecorrigeerd = kleur.waardeGecorrigeerd - hoofdKleur.waardeGecorrigeerd * 2 // afstand
            if kleur.waardeGecorrigeerd <= 0:
                kleur.vervangenDoor = hoofdKleur
                hoofdKleur.vervangt.append(kleur)
                wegstreeplijst.remove(kleur)
        hoofdkleurenLijst.append(hoofdKleur)
        wegstreeplijst.sort(key=lambda x: x.waardeGecorrigeerd, reverse=True)
    print(len(wegstreeplijst))
    print(len(hoofdkleurenLijst))
    i = 1

    #foto aanpassen op basis van de lijst
    pixOud = lab_im.load()
    lab2rgb_transform = ImageCms.buildTransformFromOpenProfiles(lab_profile, srgb_profile, "LAB", "RGB")

    vervangDict = {}
    for color in colorParametersList:
        vervangDict[(color.a, color.b)] = color.vervangenDoor


    now = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
    imgNew = Image.new('LAB', (w, h), (255, 255, 255))
    pixNew = imgNew.load()
    for x in range(w):
        for y in range(h):
            L,A,B = pixOud[x,y]
            vervangColor = vervangDict[(A,B)]
            pixNew[x,y] = (L, vervangColor.a, vervangColor.b)

    imgRGB = ImageCms.applyTransform(imgNew, lab2rgb_transform)
    imgRGB.save(dir + "/" + name + now + " vervangenVolgensMap.JPG")


files = listdir(dir)
for name in files:
    if name[-4] != ".JPG":
        bepaalWaardenEnPasAan(dir, name)