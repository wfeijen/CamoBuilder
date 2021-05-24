class TopoGeneratieDefinities:
    def __init__(self,
                                w,
                                h,
                                n,
                                minSize,
                                maxSize,
                                startRandom,
                                invloedGewichten):
        self.h = h
        self.w = w
        self.n = n
        self.minSize = minSize
        self.maxSize = maxSize
        self.startRandom = startRandom
        self.invloedGewichten = invloedGewichten

    def naam(self):
        return "W" + str(self.w) + \
               "H" + str(self.h) + \
               "N" + str(self.n) + \
               "MinSize" + str(self.minSize) + \
               "MaxSize" + str(self.maxSize) + \
               "StartRandom" + str(self.startRandom) + \
               "InvloedGew" + str(self.invloedGewichten)
