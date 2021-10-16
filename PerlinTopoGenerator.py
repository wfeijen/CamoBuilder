import noise
import numpy as np
from PIL import Image
from joblib import Parallel, delayed

class PerlinTopoGeneratator:
    def __init__(self,
                 w,
                 h,
                 n,
                 octaves,
                 persistence,
                 lacunarity,
                 scalex,
                 scaley,
                 versie):
        self.h = h
        self.w = w
        self.n = n
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.scalex = scalex
        self.scaley = scaley
        self.versie = versie
        print(self.naam())

    def naam(self):
        return "_N" + str(self.n) + \
               "_o" + str(self.octaves) + \
               "_p" + str(self.persistence) + \
               "_l" + str(self.lacunarity) + \
               "_sx" + str(self.scalex) + \
               "_sy" + str(self.scaley) + \
               "_v" + str(self.versie)


    def afmetingen(self):
        return "_W" + str(self.w) + \
               "_H" + str(self.h)


    def generate_topo(self, versieOffset):
        topo = np.zeros((self.w, self.h))
        for i in range(self.w):
            for j in range(self.h):
                topo[i][j] = noise.snoise2(x = i / (self.scaley),
                                           y = j / (self.scalex),
                                           octaves=self.octaves,
                                           persistence=self.persistence,
                                           lacunarity=self.lacunarity,
                                           repeatx=self.w / self.scalex + 1,
                                           repeaty=self.h / self.scaley + 1,
                                           base=self.versie + versieOffset * 201)
        min = np.amin(topo)
        max = np.amax(topo)
        factor = 255 / (max - min)
        # Image.fromarray(np.uint8((topo - min) * 255 / (max - min))).show()
        # normaliseren naar 0 - 1000
        topo = (topo - min) * 1000 / (max - min)
        topografie = Topo(topo)
        return topografie

    def generate_all_topos(self):
        topografien = [self.generate_topo(i) for i in range(self.n)]
        # topografien = Parallel(n_jobs=min(7, self.n), verbose=10)(
        #     delayed(self.generate_topo)(i) for i in range(self.n))

        print('klaar met topos')
        return topografien

class Topo:
    def __init__(self, topografie):
        #self.definities = definities
        #self.minSizeSqrt = math.isqrt(self.definities.shape)
        #self.maxSizeSqrt = int(math.ceil(math.sqrt(self.definities.scale)))
        self.topografie = topografie