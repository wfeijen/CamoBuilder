from projectClasses.NoiseFactory import NoiseFactory
import numpy
import numpy as np


class TopoGenerator:
    def __init__(self,
                 versie,
                 breedte,
                 hoogte):
        self.versie = versie
        self.breedte = breedte
        self.hoogte = hoogte
        self.info = ""

    def genereer(self,
                 Id,
                 persistence,
                 lacunarity,
                 octaves,
                 scaleX,
                 scaleY,
                 noise_type
                 ):
        self.info = f'{self.info},Id,{Id},noise,{noise_type},o,{str(octaves)},per,{str(persistence)},lan,{str(lacunarity)},scaleX,{str(scaleX)},scaleY,{str(scaleY)},versie,{str(self.versie)}'
        noiseMachine = NoiseFactory(noise_type)
        topografie = np.zeros((self.breedte, self.hoogte))
        for x in range(0, self.breedte):
            for y in range(0, self.hoogte):
                topografie[x, y] = noiseMachine.waarde(x / scaleX,
                                                   y / scaleY,
                                                   octaves=octaves,
                                                   persistence=persistence,
                                                   lacunarity=lacunarity,
                                                   repeatx=self.breedte / scaleX,
                                                   repeaty=self.hoogte / scaleY,
                                                   base=self.versie)
        self.versie += 1
        return topografie
