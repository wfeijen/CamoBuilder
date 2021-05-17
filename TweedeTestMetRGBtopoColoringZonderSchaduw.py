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
N = 1000
minSize = 20
maxSize = 200
startRandom = 400

naamFilePrefix = "w" + str(w) + "h" + str(h) + "N" + str(N) + "minSize" + str(minSize) + "maxSize" + str(maxSize)


class ColorPair:
    def __init__(self, value, kleurCode):
        self.valueIn = value
        self.valueOut = value
        self.kleurCode = kleurCode

    def afgewogen_kleurcode(self, i):
        return(self.valueOut * self.kleurCode[i])


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
        cx = numpy.random.randint(0, width - 1)
        cy = numpy.random.randint(0, height - 1)
        size = numpy.random.randint(minSize, maxSize)
        liftSingle(topo, size, cx, cy, verdeling, len(verdeling))
    return topo

def createPicture(name, kleurCodes, topografien, kleurGewichten):
    now = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
    img = Image.new('RGB', (w, h), (255, 255, 255))
    pix = img.load()

    kleurInformatie = list(zip(topografien, kleurGewichten))
    transparantie = kleurInformatie[-1]
    kleurInformatie = kleurInformatie[:-1]

    for ix in range(w):
        for iy in range(h):
            loc = locXY(ix, iy)
            kleurenParen = [ColorPair(kleurInformatie[kleur][0][loc] + kleurInformatie[kleur][1], kleurCodes[kleur]) for kleur in range(0, len(kleurInformatie))]
            kleurenParen.sort(key=lambda x: x.valueIn, reverse=True)
            if transparantie[0][loc] > transparantie[1]:  # We combineren kleuren
                firstColor = kleurenParen[0].valueIn - kleurenParen[2].valueIn
                secondColor = kleurenParen[1].valueIn - kleurenParen[2].valueIn
                tot = firstColor + secondColor + 1  # we willen geen nul krijgen
                kleurenParen[0].valueOut = (firstColor * 255) // tot
                kleurenParen[1].valueOut = (secondColor * 255) // tot
                # Nu kunnen we de kleuren combineren
                pix[ix, iy] = (kleurenParen[0].afgewogen_kleurcode(0) + kleurenParen[1].afgewogen_kleurcode(0),
                               kleurenParen[0].afgewogen_kleurcode(1) + kleurenParen[1].afgewogen_kleurcode(1),
                               kleurenParen[0].afgewogen_kleurcode(2) + kleurenParen[1].afgewogen_kleurcode(2))
            else:  # We nemen alleen de dominante kleur
                pix[ix, iy] = (kleurenParen[0].kleurCode[0],
                               kleurenParen[0].kleurCode[1],
                               kleurenParen[0].kleurCode[2])

    img.save(name + '_kleurCodes_' + ",".join(map(str, kleurCodes)) + '_gew_' + ",".join(map(str, kleurGewichten)) + '_' + now + ".JPG")

def main():
    with open('normaalVerdeling1000stappen1000naar1.csv', 'r') as f:
        reader = csv.reader(f)
        dummy = list(reader)
        normaalVerdeling = []
        for s in dummy: normaalVerdeling.append(int(float((s[0]))))

    kleurCodes = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 0, 0]]  # Transparantie heeft geen kleurcode
    aantalKleuren = len(kleurCodes)
    topografien = []
    for i in range(0, aantalKleuren + 1):# De laatste is de transparantie tussen kleuren
        print(i, " van ", aantalKleuren)
        topo = makeTopoForColor(w, h, N, minSize, maxSize, normaalVerdeling)
        topografien.append(topo)
    createPicture(naamFilePrefix, kleurCodes, topografien, [0, 100, 300, startRandom])
    createPicture(naamFilePrefix, kleurCodes, topografien, [0, 100, 300, -10000])
    createPicture(naamFilePrefix, kleurCodes, topografien, [0, 0, 0, startRandom])
    createPicture(naamFilePrefix, kleurCodes, topografien, [0, 0, 0, -10000])

main()
