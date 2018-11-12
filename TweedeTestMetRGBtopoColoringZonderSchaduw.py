from PIL import Image, ImageCms
from array import array
import random
import math
import csv
import cProfile
import numpy
import datetime

# w, h = 500, 500
w, h = 5000, 3000
N = 10000
minSize = 20
maxSize = 200
startRandom = 400


class ColorPair:
    def __init__(self, value):
        self.valueIn = value
        self.valueOut = value

def locXY(x, y):
    return x + (y * w)

def changePoint(topo, loc, afstand, verdeling, size, factor, lenVerdeling):
    if afstand < size:
        topo[loc] = topo[loc] + verdeling[afstand * lenVerdeling // size] * factor

def liftSingle(topo, size, centerX, centerY, verdeling, lenVerdeling):
    if centerX - size < 0:
        startX = 0
    else:
        startX = centerX - size
    if centerX + size > w:
        endX = w
    else:
        endX = centerX + size
    if centerY - size < 0:
        startY = 0
    else:
        startY = centerY - size
    if centerY + size > h:
        endY = h
    else:
        endY = centerY + size
    #print('size:' + str(size)  + " x:" + str(centerX) + " y:" + str(centerY))
    if topo[locXY(centerX, centerY)] < startRandom:
        factor = -1
    else:
        factor = 1
    for ix in range(startX, endX):
        for iy in range(startY, endY):
            afstand = int(math.hypot((centerX - ix) ,(centerY - iy))) #math.sqrt 60.234
            changePoint(topo, locXY(ix,iy), afstand, verdeling, size, factor, lenVerdeling)



# len en random veel tijd

def makeTopoForColor(width, height, N, minSize, maxSize, verdeling):
    topo = array('i', numpy.random.choice(2 * startRandom, height * width))
    for i in range(N):
        print(str(i))
        cx = numpy.random.random_integers (0, width - 1)
        cy = numpy.random.random_integers (0, height - 1)
        size = numpy.random.random_integers (minSize, maxSize)
        liftSingle(topo, size, cx, cy, verdeling, len(verdeling))
    return topo

def createPicture(name, R, gewichtR, G, gewichtG, B, gewichtB, T, transparantieWaarde):
    now = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
    img = Image.new('RGB', (w, h), (255, 255, 255))
    pix = img.load()

    for ix in range(w):
        for iy in range(h):
            loc = locXY(ix, iy)
            red = ColorPair(R[loc] + gewichtR)
            green = ColorPair(G[loc] + gewichtG)
            blue = ColorPair(B[loc] + gewichtB)
            colors = [red, blue, green]
            colors.sort(key=lambda x: x.valueIn, reverse=True)
            if T[loc] > transparantieWaarde:
                firstColor = colors[0].valueIn - colors[2].valueIn
                secondColor = colors[1].valueIn - colors[2].valueIn
                tot = firstColor + secondColor + 1  # we willen geen nul krijgen
                colors[0].valueOut = (firstColor * 255) // tot
                colors[1].valueOut = (secondColor * 255) // tot
                colors[2].valueOut = 0
            else:
                colors[0].valueOut = 255
                colors[1].valueOut = 0
                colors[2].valueOut = 0
            pix[ix, iy] = (red.valueOut, green.valueOut, blue.valueOut)
    img.save(name + now + ".JPG")

def main():
    with open('normaalVerdeling1000stappen1000naar1.csv', 'r') as f:
        reader = csv.reader(f)
        dummy = list(reader)
        normaalVerdeling = []
        for s in dummy: normaalVerdeling.append(int(float((s[0]))))
    print("R")
    R = makeTopoForColor(w, h, N, minSize, maxSize, normaalVerdeling)
    print("G")
    G = makeTopoForColor(w, h, N, minSize, maxSize // 2, normaalVerdeling)
    print("B")
    B = makeTopoForColor(w, h, N, minSize, maxSize, normaalVerdeling)
    print("T")
    T = makeTopoForColor(w, h, N, minSize, maxSize, normaalVerdeling)
    createPicture("RGB trans 123 Waarde", R, 0, G, 100, B, 300, T, startRandom)
    createPicture("RGB trans 123 volledig ",  R, 0, G, 100, B, 300, T, -10000)
    createPicture("RGB trans 111 Waarde", R, 0, G, 0, B, 0, T, startRandom)
    createPicture("RGB trans 111 volledig ",  R, 0, G, 0, B, 0, T, -10000)

def profile():
    #cProfile.run('main()','stats')
    #Tweede test met RGB topo coloring zonder schaduw.py
    from cProfile import Profile
    from pyprof2calltree import convert, visualize
    profiler = Profile()
    profiler.runctx('main()',locals(),globals())
    visualize(profiler.getstats())
    #convert(profiler.getstats(), 'profiling_results.kgrind')

main()
#profile()