class TopoGeneratieDefinities:
    def __init__(self,
                 w,
                 h,
                 n,
                 minSize,
                 maxSize,
                 startRandom,
                 invloedGewichten,
                 afplatting):
        self.h = h
        self.w = w
        self.n = n
        self.minSize = minSize
        self.maxSize = maxSize
        self.startRandom = startRandom
        self.invloedGewichten = invloedGewichten
        self.afplatting = afplatting
        print(self.naam())

    def naam(self):
        return "_N" + str(self.n) + \
               "_MinSize" + str(self.minSize) + \
               "_MaxSize" + str(self.maxSize) + \
               "_StartRandom" + str(self.startRandom) + \
               "_InvloedGew" + str(self.invloedGewichten) +\
               "_afplatting" + str(self.afplatting)

    def afmetingen(self):
        return "_W" + str(self.w) + \
               "_H" + str(self.h)
