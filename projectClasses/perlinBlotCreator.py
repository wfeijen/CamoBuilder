import noise
import numpy as np
from PIL import Image

class PerlinBlotter:
    def __init__(self,
                 persistence,
                 lacunarity,
                 octaves,
                 scaleX,
                 scaleY,
                 startBase,
                 grenswaarde):
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.base = startBase
        self.grenswaarde = grenswaarde

    def name(self):
        return "_o" + str(self.octaves) + \
            "_p" + str(self.persistence) + \
               "_l" + str(self.lacunarity) + \
               "_X" + str(self.scaleX) + \
               "_Y" + str(self.scaleY) + \
               "_b" + str(self.base) + \
               "_g" + str(self.grenswaarde)

    def blot(self, blot_sizeX, blot_sizeY):
        centerX = blot_sizeX // 2
        centerY = blot_sizeY // 2
        middenKwadraat = min(centerX ** 2, centerY ** 2)
        canvas = np.zeros((blot_sizeX, blot_sizeY))
        for x in range(0, blot_sizeX):
            for y in range(0, blot_sizeY):
                noiseWaarde = noise.pnoise2( x / self.scaleX,
                                             y / self.scaleY,
                                             octaves=self.octaves,
                                             persistence=self.persistence,
                                             lacunarity=self.lacunarity,
                                             repeatx=blot_sizeX / self.scaleX + 1,
                                             repeaty=blot_sizeY / self.scaleY + 1,
                                             base=self.base)
                canvas[x, y] = noiseWaarde
        canvas = (canvas - np.amin(canvas)) / (np.amax(canvas) - np.amin(canvas))
        for x in range(0, blot_sizeX):
            for y in range(0, blot_sizeY):
                afstand_kwadraad = ((x - centerX) ** 2 + (y - centerY) ** 2)
                vermenigvuldinging = max(0,
                                         1 - (afstand_kwadraad / (middenKwadraat)))
                canvas[x, y] = canvas[x, y] * vermenigvuldinging
        # in plaats van opnieuw normaliseren passen we de grenswaarde aan die uitgaat
        # van range 0-1
        canvas = (canvas - np.amin(canvas)) / (np.amax(canvas) - np.amin(canvas))
        canvas = np.where(canvas > self.grenswaarde, 1, 0)
        self.base = self.base + np.random.randint(1, 2)
        return canvas

if __name__ == "__main__":
    def show_blot(canvas):
        min = np.amin(canvas)
        print(min)
        print(np.amax(canvas))
        world_grens = canvas * 255
        Image.fromarray(np.uint8(world_grens)).show()


    pb = PerlinBlotter(persistence=0.2,
                       lacunarity=2.0,
                       octaves=8,
                       scaleX=50,
                       scaleY=100,
                       startBase=0,
                       grenswaarde=0.3)

    for i in range(0, 5):
        show_blot(pb.blot(blot_sizeX=750, blot_sizeY=750))

