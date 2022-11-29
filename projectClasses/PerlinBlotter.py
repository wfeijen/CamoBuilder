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
        self.naam = ",o," + str(self.octaves) + \
               ",per," + str(self.persistence) + \
               ",lan," + str(self.lacunarity) + \
               ",scaleX," + str(self.scaleX) + \
               ",scaleY," + str(self.scaleY) + \
               ",base," + str(self.base) + \
               ",grens," + str(self.grenswaarde)

    def blot(self, blot_sizeX, blot_sizeY):
        blot_sizeX = max(blot_sizeX, 10)
        blot_sizeY = max(blot_sizeY, 10)
        centerX = blot_sizeX // 2
        centerY = blot_sizeY // 2
        # middenKwadraat = min(centerX ** 2, centerY ** 2)
        canvas = np.zeros((blot_sizeX, blot_sizeY))
        ondergrens_x = blot_sizeX
        ondergrens_y = blot_sizeY
        bovengrens_x = 0
        bovengrens_y = 0
        for x in range(0, blot_sizeX):
            for y in range(0, blot_sizeY):
                noiseWaarde = noise.pnoise2( x / self.scaleX,
                                             y / self.scaleY,
                                             octaves=self.octaves,
                                             persistence=self.persistence,
                                             lacunarity=self.lacunarity,
                                             repeatx=blot_sizeX / self.scaleX,
                                             repeaty=blot_sizeY / self.scaleY,
                                             base=self.base) + 1 / 2
                genormaliseerde_euclidische_afstand = (x / centerX - 1) ** 2 + (y / centerY - 1) ** 2
                vermenigvuldinging = max(0,
                                         1 - (genormaliseerde_euclidische_afstand))
                if noiseWaarde * vermenigvuldinging > self.grenswaarde:
                    resultaat = 1
                    if ondergrens_x > x:
                        ondergrens_x = x
                    elif bovengrens_x < x:
                        bovengrens_x = x
                    if ondergrens_y > y:
                        ondergrens_y = y
                    elif bovengrens_y < y:
                        bovengrens_y = y
                else:
                    resultaat = 0

                canvas[x, y] = resultaat
        canvas = canvas[ondergrens_x:bovengrens_x, ondergrens_y:bovengrens_y]
        # Image.fromarray(np.uint8(canvas * 255)).show()

        self.base = self.base + np.random.randint(1, 2)
        return canvas

    def line_blot(self, blot_sizeX, blot_sizeY, dikte, richtingGenerator):
        deltaX, deltaY = self.richtingGenerator.geef_richting(dikte)
        blot_sizeX = max(blot_sizeX, 10)
        blot_sizeY = max(blot_sizeY, 10)
        centerX = blot_sizeX // 2
        centerY = blot_sizeY // 2
        # middenKwadraat = min(centerX ** 2, centerY ** 2)
        canvas = np.zeros((blot_sizeX, blot_sizeY))
        ondergrens_x = blot_sizeX
        ondergrens_y = blot_sizeY
        bovengrens_x = 0
        bovengrens_y = 0
        for x in range(0, blot_sizeX):
            for y in range(0, blot_sizeY):
                noiseWaardePos = noise.pnoise2( x / self.scaleX,
                                             y / self.scaleY,
                                             octaves=self.octaves,
                                             persistence=self.persistence,
                                             lacunarity=self.lacunarity,
                                             repeatx=blot_sizeX / self.scaleX,
                                             repeaty=blot_sizeY / self.scaleY,
                                             base=self.base) + 1 / 2
                genormaliseerde_euclidische_afstand = (x / centerX - 1) ** 2 + (y / centerY - 1) ** 2
                noiseWaardePos = noiseWaardePos * max(0, 1 - (genormaliseerde_euclidische_afstand))
                noiseWaardeNeg = noise.pnoise2( (x + deltaX) / self.scaleX,
                                                (y + deltaY) / self.scaleY,
                                             octaves=self.octaves,
                                             persistence=self.persistence,
                                             lacunarity=self.lacunarity,
                                             repeatx=blot_sizeX / self.scaleX,
                                             repeaty=blot_sizeY / self.scaleY,
                                             base=self.base) + 1 / 2
                genormaliseerde_euclidische_afstand = (x / centerX - 1) ** 2 + (y / centerY - 1) ** 2
                noiseWaardeNeg = noiseWaardeNeg * max(0, 1 - (genormaliseerde_euclidische_afstand))
                if noiseWaardePos - noiseWaardeNeg > self.grenswaarde:
                    resultaat = 1
                    if ondergrens_x > x:
                        ondergrens_x = x
                    elif bovengrens_x < x:
                        bovengrens_x = x
                    if ondergrens_y > y:
                        ondergrens_y = y
                    elif bovengrens_y < y:
                        bovengrens_y = y
                else:
                    resultaat = 0

                canvas[x, y] = resultaat
        canvas = canvas[ondergrens_x:bovengrens_x, ondergrens_y:bovengrens_y]
        # Image.fromarray(np.uint8(canvas * 255)).show()

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
