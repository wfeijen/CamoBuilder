from PIL import Image
from array import array
import math
import csv
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
import pickle
from os.path import exists

# W, H = 500, 500
W, H = 5000, 6000
N = 300
MinSize = 250
MaxSize = 1000
StartRandom = 1 # >0
InvloedGewichten = 700
Kleurendir = 'kleurParameters/'
Kleurenbestand = '2KleurenVoorOnderzoekGroveTekenig.csv'

NaamFilePrefix = "camoOutput/W" + str(W) + "H" + str(H) + "N" + str(N) + "MinSize" + str(MinSize) + "MaxSize" + str(
    MaxSize) + "StartRandom" + str(StartRandom) + "InvloedGew" + str(InvloedGewichten) + "kleurBest" + Kleurenbestand[:-4]


class ColorPair:
    def __init__(self, value, kleurCode):
        self.valueIn = value
        self.valueOut = value
        self.kleurCode = kleurCode

    def afgewogen_kleurcode(self, i):
        return int(self.valueOut * self.kleurCode[i])


def locXY(x, y):
    return x + (y * W)


def changePoint(topo, loc, afstand, verdeling, size, factor, lenVerdeling):
    if afstand < size:
        topo[loc] = topo[loc] + verdeling[afstand * lenVerdeling // size] * factor


def liftSingle(topo, size, centerX, centerY, verdeling, lenVerdeling):
    startX = max(centerX - size, 0)
    endX = min(centerX + size, W)
    startY = max(centerY - size, 0)
    endY = min(centerY + size, H)
    if topo[locXY(centerX, centerY)] < StartRandom:
        factor = -1
    else:
        factor = 1
    for ix in range(startX, endX):
        for iy in range(startY, endY):
            afstand = int(math.hypot((centerX - ix), (centerY - iy)))
            if afstand < size:
                loc = locXY(ix, iy)
                topo[loc] = topo[loc] + verdeling[afstand * lenVerdeling // size] * factor


def makeTopoForColor(width, height, aantalElementen, minSize, maxSize, verdeling):
    minSizeSqrt = math.isqrt(minSize)
    maxSizeSqrt = int(math.ceil(math.sqrt(maxSize)))
    topo = array('i', np.random.choice(2 * StartRandom, height * width))
    for i in range(aantalElementen):
        # print(str(i))
        cx = np.random.randint(0, width - 1)
        cy = np.random.randint(0, height - 1)
        size = np.random.randint(minSizeSqrt, maxSizeSqrt)
        size = size * size
        liftSingle(topo, size, cx, cy, verdeling, len(verdeling))
    return topo


def createPicture(name, colorCodes, topos, colorWeights):
    img = Image.new('RGB', (W, H), (255, 255, 255))
    pix = img.load()

    kleurInformatie = list(zip(topos, colorWeights))
    transparency = kleurInformatie[-1]
    kleurInformatie = kleurInformatie[:-1]

    for ix in range(W):
        for iy in range(H):
            loc = locXY(ix, iy)
            kleurenParen = [ColorPair(kleurInformatie[kleur][0][loc] + kleurInformatie[kleur][1], colorCodes[kleur]) for
                            kleur in range(0, len(kleurInformatie))]
            kleurenParen.sort(key=lambda x: x.valueIn, reverse=True)
            if transparency[0][loc] > transparency[1]:  # We combineren kleuren
                firstColor = kleurenParen[0].valueIn #- kleurenParen[2].valueIn
                secondColor = kleurenParen[1].valueIn #- kleurenParen[2].valueIn
                tot = max(firstColor + secondColor , 1)# we willen geen nul krijgen
                kleurenParen[0].valueOut = firstColor / tot
                kleurenParen[1].valueOut = secondColor / tot
                # Nu kunnen we de kleuren combineren
                pix[ix, iy] = (int(kleurenParen[0].afgewogen_kleurcode(0) + kleurenParen[1].afgewogen_kleurcode(0)),
                               int(kleurenParen[0].afgewogen_kleurcode(1) + kleurenParen[1].afgewogen_kleurcode(1)),
                               int(kleurenParen[0].afgewogen_kleurcode(2) + kleurenParen[1].afgewogen_kleurcode(2)))
            else:  # We nemen alleen de dominante kleur
                pix[ix, iy] = (kleurenParen[0].kleurCode[0],
                               kleurenParen[0].kleurCode[1],
                               kleurenParen[0].kleurCode[2])
    img.save(name + '_transp_' + str(colorWeights[-1]).zfill(6) + ".JPG")


kleurInfo = pd.read_csv(Kleurendir + Kleurenbestand, index_col=0)
kleurCodes = kleurInfo.iloc[:, 0:3].to_numpy()
kleurGewichten = kleurInfo.iloc[:, 3]
kleurGewichten = (kleurGewichten * InvloedGewichten) // kleurGewichten.max()
kleurGewichten = kleurGewichten.to_numpy()

with open('normaalVerdeling1000stappen1000naar1.csv', 'r') as f:
    reader = csv.reader(f)
    dummy = list(reader)
    normaalVerdeling = []
    for s in dummy: normaalVerdeling.append(int(float((s[0]))))

aantalKleuren = len(kleurCodes)
# topografien = []
# for i in range(0, aantalKleuren + 1):# De laatste is de transparantie tussen kleuren
#     topo = makeTopoForColor(W, H, N, MinSize, MaxSize, normaalVerdeling)
#     topografien.append(topo)

pickleNaam = "cacheFiles/W" + str(W) + "H" + str(H) + "N" + str(N) + "MinSize" + str(MinSize) + "MaxSize" + str(
    MaxSize) + "StartRandom" + str(StartRandom) + str(aantalKleuren) + ".pkl"
if exists(pickleNaam):
    print("van cache")
    filehandler = open(pickleNaam, 'rb')
    topografien = pickle.load(filehandler)
else:
    topografien = Parallel(n_jobs=min(7, aantalKleuren + 1), verbose=10)(
        delayed(makeTopoForColor)(W, H, N, MinSize, MaxSize, normaalVerdeling) for i in range(aantalKleuren + 1))
    print('klaar met topos')
    filehandler = open(pickleNaam, 'wb')
    pickle.dump(topografien, filehandler)

# Parallel(n_jobs=7, verbose=10)(
#     delayed(createPicture)(NaamFilePrefix, kleurCodes, topografien, np.append(kleurGewichten, transparantie))
#     for transparantie in [-10000, -8000, -6000, -4000, -2000, 0])
for transparantie in [100000]:
    createPicture(NaamFilePrefix, kleurCodes, topografien, np.append(kleurGewichten, transparantie))
    print('klaar met plaatje')

print('klaar met plaatjes')
