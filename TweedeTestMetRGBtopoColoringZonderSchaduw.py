from PIL import Image, ImageCms
from array import array
import random
import math
import csv
import cProfile
import numpy

# w, h = 500, 500
w, h = 1920, 1200
N = 100
minSize = 50
maxSize = 500

def changePoint(topo, x, y, afstand, verdeling, size, factor, lenVerdeling):
    if afstand < size:
        topo[x][y] = topo[x][y] + verdeling[afstand * lenVerdeling // size] * factor

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
    print('size:' + str(size)  + " x:" + str(centerX) + " y:" + str(centerY))
    if topo[centerX][centerY] < 100:
        factor = -1
    else:
        factor = 1
    for ix in range(startX, endX):
        for iy in range(startY, endY):
            afstand = int(math.hypot((centerX - ix) ,(centerY - iy))) #math.sqrt 60.234
            changePoint(topo, ix, iy, afstand, verdeling, size, factor, lenVerdeling)



# len en random veel tijd

def makeTopoForColor(width, height, N, minSize, maxSize, verdeling):
    #topo = [array('f', [item % 200 - 100 for item in random.sample(range(0, height), height)]) for x in range(width)]
    topo = [array('f', numpy.random.choice(200,height)) for x in range(width)]
    for i in range(N):
        print(str(i))
        cx = numpy.random.random_integers (0, width - 1)
        cy = numpy.random.random_integers (0, height - 1)
        size = numpy.random.random_integers (minSize, maxSize)
        liftSingle(topo, size, cx, cy, verdeling, len(verdeling))
    return topo


def main():
    with open('normaalVerdeling1000stappen1000naar1.csv', 'r') as f:
        reader = csv.reader(f)
        dummy = list(reader)
        normaalVerdeling = []
        for s in dummy: normaalVerdeling.append(float(s[0]))
    print("R")
    R = makeTopoForColor(w, h, N, minSize, maxSize, normaalVerdeling)
    print("G")
    G = makeTopoForColor(w, h, N, minSize, maxSize, normaalVerdeling)
    print("B")
    B = makeTopoForColor(w, h, N, minSize, maxSize, normaalVerdeling)

    img = Image.new('RGB', (w, h), (255, 255, 255))
    pix = img.load()

    for ix in range(w):
        for iy in range(h):
            if R[ix][iy] > G[ix][iy]:
                if R[ix][iy] > B[ix][iy]:
                    pix[ix, iy] = (255, 0, 0)
                else:
                    pix[ix, iy] = (0, 0, 255)
            else:
                if G[ix][iy] > B[ix][iy]:
                    pix[ix, iy] = (0, 255, 0)
                else:
                    pix[ix, iy] = (0, 0, 255)

    img.save("RGB Topo 3.JPG")

main()
#cProfile.run('main()','stats')

#Tweede test met RGB topo coloring zonder schaduw.py
from cProfile import Profile
from pyprof2calltree import convert, visualize
profiler = Profile()
profiler.runctx('main()',locals(),globals())
visualize(profiler.getstats())
#convert(profiler.getstats(), 'profiling_results.kgrind')