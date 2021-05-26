import math
import numpy as np
import pickle
from joblib import Parallel, delayed
from os.path import exists


class Topografie:
    def __init__(self, definities):
        self.definities = definities
        self.minSizeSqrt = math.isqrt(self.definities.minSize)
        self.maxSizeSqrt = int(math.ceil(math.sqrt(self.definities.maxSize)))
        self.topografie = np.zeros((definities.w, definities.h))

    def liftSingle(self, size, centerX, centerY, verdeling):
        lenVerdeling = len(verdeling)
        startX = int(max(centerX - (size * self.definities.afplatting), 0))
        endX = int(min(centerX + (size * self.definities.afplatting), self.definities.w))
        startY = max(centerY - size, 0)
        endY = min(centerY + size, self.definities.h)
        if self.topografie[centerX, centerY] > self.definities.startRandom:
            factor = -1
        else:
            factor = 1
        for ix in range(startX, endX):
            for iy in range(startY, endY):
                afstand = int(math.hypot((centerX - ix) // self.definities.afplatting,
                                         centerY - iy))
                if afstand < size:
                    waarde = self.topografie[ix, iy] + \
                             verdeling[afstand * lenVerdeling // size] * factor
                    self.topografie[ix, iy] = waarde

    def genereer(self, verdeling):
        # hier pas echt topgrafie object maken omdat het anders door parallelle processing imutable is.
        if self.definities.startRandom == 0:
            self.topografie = np.zeros((self.definities.w, self.definities.h))
        else:
            initieleVulling = np.random.choice(2 * self.definities.startRandom - self.definities.startRandom,
                                               self.definities.w * self.definities.h)
            self.topografie = initieleVulling.reshape(self.definities.w, self.definities.h)

        for i in range(self.definities.n):
            # print(str(i))
            cx = np.random.randint(0, self.definities.w - 1)
            cy = np.random.randint(0, self.definities.h - 1)
            size = np.random.randint(self.minSizeSqrt, self.maxSizeSqrt)
            size = size * size
            self.liftSingle(size, cx, cy, verdeling)
        self.topografie = np.absolute(self.topografie) + 1
        return self


def genereerToposEnCache(topoDefinities, aantalTopos, verdeling):
    pickleNaam = "cacheFiles/" + topoDefinities.afmetingen() + topoDefinities.naam() + "_aantal" + str(
        aantalTopos) + ".pkl"
    if exists(pickleNaam):
        print("van cache")
        filehandler = open(pickleNaam, 'rb')
        topografien = pickle.load(filehandler)
    else:
        topografien = [Topografie(topoDefinities) for i in range(aantalTopos)]
        topografien = Parallel(n_jobs=min(7, aantalTopos), verbose=10)(
            delayed(topografie.genereer)(verdeling) for topografie in topografien)
        # for topografie in topografien:
        #     topografie.genereer(verdeling=verdeling)
        #     print("topgrafie klaar")
        print('klaar met topos')
        filehandler = open(pickleNaam, 'wb')
        pickle.dump(topografien, filehandler)
    return topografien
