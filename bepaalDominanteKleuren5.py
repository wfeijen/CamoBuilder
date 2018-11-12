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
from array import array

#Parameters
dir = "C:/Users\wfeij/PycharmProjects/Camo builder/bepaalDominanteKleuren"
mountainProfileLength = 1000

def bepaalWaardenEnPasAan(dir, name):
    #Inlezen file
    startImage = Image.open(dir + "/" + name)
    if startImage.mode != "RGB":
      startImage = startImage.convert("RGB")
    srgb_profile = ImageCms.createProfile("sRGB")
    lab_profile  = ImageCms.createProfile("LAB")
    lab2rgb_transform = ImageCms.buildTransformFromOpenProfiles(lab_profile, srgb_profile, "LAB", "RGB")
    rgb2lab_transform = ImageCms.buildTransformFromOpenProfiles(srgb_profile, lab_profile, "RGB", "LAB")
    labReducedToneImage = ImageCms.applyTransform(startImage, rgb2lab_transform)
    labOriginalToneImage = ImageCms.applyTransform(startImage, rgb2lab_transform)
    labReducedTonePix = labReducedToneImage.load()
    labOriginalTonePix = labOriginalToneImage.load()
    w, h = labReducedToneImage.size

    for x in range(w):
        for y in range(h):
            L, A, B = labReducedTonePix[x,y]
            labReducedTonePix[x,y] = (128, A, B)
    rgbReducedToneImage = ImageCms.applyTransform(labReducedToneImage, lab2rgb_transform)
    rgbReducedColorImage = rgbReducedToneImage.convert('P', palette=Image.ADAPTIVE, colors=5).convert('RGB')
    now = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
    rgbReducedColorImage.save(dir + "/" + name + now + " vervangenVolgensMap.JPG")
    labReducedColorImage = ImageCms.applyTransform(rgbReducedColorImage, rgb2lab_transform)
    labReducedColorPix = labReducedColorImage.load()

    labReducedColorsMap = labReducedColorImage.getcolors(w * h)
    labReducedColorsWithTonesDict = {}
    for number, (L, A, B) in labReducedColorsMap:
        labReducedColorsWithTonesDict[(A,B)] = [number,L,[0] * 256]
    for x in range(w):
        for y in range(h):
            Lor,Aor,Bor = labOriginalTonePix[x,y]
            Lr, Ar, Br = labReducedColorPix[x,y]
            labReducedColorsWithTonesDict[Ar,Br][2][Lor] = labReducedColorsWithTonesDict[Ar,Br][2][Lor] +1
    # omzetten van tellingen per lichtsterkte naar relatieve breedte per lichtsterkte
    for tint, lichtsterkten in labReducedColorsWithTonesDict.items():
        increase = lichtsterkten[0] / mountainProfileLength
        lArray = lichtsterkten[2]
        mountainProfile = array('i')
        mpi = 0
        drempel = increase / 2  # measure in the middle
        for i in range(mountainProfileLength):
            if lArray[mpi] >= drempel:
                drempel += increase
                mpi += 1
            mountainProfile[i] = lArray[mpi]




    for aantal, (L, A, B) in labReducedColorsMap:
        print(str(aantal) + " " + str(L) + " " + str(A) + " " + str(B))
    #rgbReducedToneImage = ImageCms.applyTransform(labReducedToneImage, lab2rgb_transform)
    #rgbReducedToneImage.save(dir + "/" + name + now + " vervangenVolgensMap.JPG")

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