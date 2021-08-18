class TopoGeneratieDefinities:
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
