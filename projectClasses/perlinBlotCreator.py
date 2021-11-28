import random
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
        grenswaarde = self.grenswaarde * (np.amax(canvas) - np.amin(canvas)) - np.amin(canvas)
        canvas = np.where(canvas > grenswaarde, 1, 0)
        self.base = self.base + 1
        return canvas



def show_blot(world):
    min = np.amin(world)
    print(min)
    print(np.amax(world))
    world_grens = world * 255
    Image.fromarray(np.uint8(world_grens)).show()

pb = PerlinBlotter(persistence=0.4,
                   lacunarity=4.0,
                   octaves=9,
                   scaleX=200,
                   scaleY=400,
                   startBase=0,
                   grenswaarde=0.5)

for i in range(0, 5):
    show_blot(pb.blot(blot_sizeX=300,
                   blot_sizeY=300))