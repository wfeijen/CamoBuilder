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
        self.buren = []
        self.verdeeldNu = origineel * 1000
        self.verdeeldStraks = 0

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

    wegstreeplijst = sorted(colorParametersList, key=lambda x: x.waardeGecorrigeerd, reverse=True)

    for eigen in wegstreeplijst:
        eigen.verdeeldNu = float(eigen.waardeOrigineel)
        for buur in colorParametersList:
            afstand = int(hypot((eigen.a - buur.a), (eigen.b - buur.b))) # math.sqrt 60.234
            if afstand < 5:
                eigen.buren.append(buur)
    teller = 1
    while len(wegstreeplijst) > 1:
        print("iteratie " + str(teller))
        teller = teller + 1
        for eigen in wegstreeplijst:
            if len(eigen.buren) == 0 or eigen.verdeeldNu < 50:
                for buur in eigen.buren:
                    buur.buren.remove(eigen)
                wegstreeplijst.remove(eigen)
            else:
                vraag = 0
                for buur in eigen.buren:
                    vraag = vraag + buur.verdeeldNu
                bijdrage = eigen.verdeeldNu // (vraag * 2)
                for buur in eigen.buren:
                    buur.verdeeldStraks = buur.verdeeldStraks + buur.verdeeldNu * bijdrage
        for eigen in wegstreeplijst:
            eigen.verdeeldNu = eigen.verdeeldStraks
            eigen.verdeeldStraks = eigen.verdeeldStraks // 2


    #toekennen nevenkleuren aan hoofdkleur
    wegstreeplijst = sorted(colorParametersList, key=lambda x: x.verdeeldStraks, reverse=True)
    hoofdkleurenLijst = wegstreeplijst[:7]
    wegstreeplijst = wegstreeplijst[7:]
    for eigen in wegstreeplijst:
        minAfstand =10000000
        for hoofdKleur in hoofdkleurenLijst:
            if minAfstand > int(hypot((eigen.a - hoofdKleur.a), (eigen.b - hoofdKleur.b))):
                minAfstand = int(hypot((eigen.a - hoofdKleur.a), (eigen.b - hoofdKleur.b)))
                eigen.vervangenDoor = hoofdKleur
                hoofdKleur.vervangt.append(eigen)

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

def main():
    files = listdir(dir)
    for name in files:
        if name[-4:] != ".JPG":
            print(name[-4:])
            bepaalWaardenEnPasAan(dir, name)

def profile():
    #cProfile.run('main()','stats')
    #Tweede test met RGB topo coloring zonder schaduw.py
    from cProfile import Profile
    from pyprof2calltree import convert, visualize
    profiler = Profile()
    profiler.runctx('main()',locals(),globals())
    visualize(profiler.getstats())
    #convert(profiler.getstats(), 'profiling_results.kgrind')

#main()
profile()