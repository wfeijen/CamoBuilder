class PerlinTopoGeneratator:
    def __init__(self,
                 w,
                 h,
                 n,
                 minSize,
                 maxSize,
                 startRandom,
                 afplatting,
                 versie):
        self.h = h
        self.w = w
        self.n = n
        self.minSize = minSize
        self.maxSize = maxSize
        self.startRandom = startRandom
        self.afplatting = afplatting
        self.versie = versie
        print(self.naam())

    def naam(self):
        return "_N" + str(self.n) + \
               "_MinSize" + str(self.minSize) + \
               "_MaxSize" + str(self.maxSize) + \
               "_StartRandom" + str(self.startRandom) + \
               "_afplatting" + str(self.afplatting) +\
               "_v" + str(self.versie)


    def afmetingen(self):
        return "_W" + str(self.w) + \
               "_H" + str(self.h)

    def perlin_topo_generator():
        topo = np.zeros((w, h))
        for i in range(shape[0]):
            for j in range(shape[1]):
                topo[i][j] = noise.pnoise2(i / scale,
                                           j / scale,
                                           octaves=octaves,
                                           persistence=persistence,
                                           lacunarity=lacunarity,
                                           repeatx=1024,
                                           repeaty=1024,
                                           base=0)

        min = np.amin(topo)
        factor = 255 / (np.amax(topo) - min)
        Image.fromarray(np.uint8((topo - min) * factor)).show()
        factor = 1000 / (np.amax(topo) - min)
        return np.uint8((topo - min) * factor)