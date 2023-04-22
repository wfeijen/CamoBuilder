from projectClasses.NoiseFactory import NoiseFactory
import numpy
import numpy as np


class Blotter:
    def __init__(self,
                 persistence,
                 lacunarity,
                 octaves,
                 scaleX,
                 scaleY,
                 startBase,
                 grenswaarde,
                 noise_type):
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.base = startBase
        self.noiseMachine = NoiseFactory(noise_type)
        self.info = f',noise,{noise_type},o,{str(self.octaves)},per,{str(self.persistence)},lan,{str(self.lacunarity)},scaleX,{str(self.scaleX)},scaleY,{str(self.scaleY)},base,{str(self.base)}'

    def blotCanvas(self, blot_sizeX, blot_sizeY):
        noiseWaardes = np.zeros((blot_sizeX, blot_sizeY))
        for x in range(0, blot_sizeX):
            for y in range(0, blot_sizeY):
                noiseWaardes[x, y] = self.noiseMachine.waarde(x / self.scaleX,
                                                   y / self.scaleY,
                                                   octaves=self.octaves,
                                                   persistence=self.persistence,
                                                   lacunarity=self.lacunarity,
                                                   repeatx=blot_sizeX / self.scaleX,
                                                   repeaty=blot_sizeY / self.scaleY,
                                                   base=self.base)
        return noiseWaardes