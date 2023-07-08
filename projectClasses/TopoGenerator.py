from projectClasses.NoiseFactory import NoiseFactory
from sklearn.preprocessing import normalize
import numpy as np


def schaalNaarMin1Tot1(arr):
    min = np.min(arr)
    return ((arr - min) * 2 / (np.max(arr) - min)) - 1


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
                 persistence,
                 lacunarity,
                 octaves,
                 scaleX,
                 scaleY,
                 noise_type,
                 macht,
                 bereik,
                 ):
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
        # topografie = normalize(topografie)
        topografie = schaalNaarMin1Tot1(topografie)
        if macht != 1:
            topografie = np.power(topografie, macht)
        if bereik != 1:
            topografie = topografie * bereik
        return topografie

    def genereer_1(self,
                   Id,
                   persistence,
                   lacunarity,
                   octaves,
                   scaleX,
                   scaleY,
                   noise_type,
                   macht=1,
                   bereik=1
                   ):
        self.info = f'{self.info},Id,{Id},noise,{noise_type},o,{str(octaves)},per,{str(persistence)},lan,{str(lacunarity)},scaleX,{str(scaleX)},scaleY,{str(scaleY)},versie,{str(self.versie)},macht,{str(macht)},bereik,{bereik}'
        return self.genereer(persistence,
                             lacunarity,
                             octaves,
                             scaleX,
                             scaleY,
                             noise_type,
                             macht,
                             bereik
                             )

    def genereer_N(self,
                   N,
                   Id,
                   persistence,
                   lacunarity,
                   octaves,
                   scaleX,
                   scaleY,
                   noise_type,
                   macht=1,
                   bereik=1
                   ):
        self.info = f'{self.info},Id,{Id},noise,{noise_type},o,{str(octaves)},per,{str(persistence)},lan,{str(lacunarity)},scaleX,{str(scaleX)},scaleY,{str(scaleY)},versie,{str(self.versie)},macht,{str(macht)},bereik,{bereik}'

        antwoord = []
        for i in range(N):
            antwoord.append(self.genereer(persistence,
                                          lacunarity,
                                          octaves,
                                          scaleX,
                                          scaleY,
                                          noise_type,
                                          macht,
                                          bereik))

        return np.stack(antwoord)

    def binair_1(self,
                 Id,
                 persistence,
                 lacunarity,
                 octaves,
                 scaleX,
                 scaleY,
                 noise_type,
                 bovengrens,
                 ondergrens
                 ):
        self.info = f'{self.info},InverseId,{Id},bovengrens,{bovengrens},ondergrens,{ondergrens}'
        topo = self.genereer_1(
            Id,
            persistence,
            lacunarity,
            octaves,
            scaleX,
            scaleY,
            noise_type
        )
        topo = np.where(topo < bovengrens, 1, -1) * np.where(topo > ondergrens, 1, -1)
        return topo

    # Maakt 1 binaire topo -1 en 1 die over alle N kanalen herhaald wordt. De bedoeling is namelijk om hier inversies mee te maken in licht en donker
    def binair_1_n(self,
                   N,
                   Id,
                   persistence,
                   lacunarity,
                   octaves,
                   scaleX,
                   scaleY,
                   noise_type,
                   bovengrens,
                   ondergrens
                   ):
        self.info = f'{self.info},InverseId,{Id},bovengrens,{bovengrens},ondergrens,{ondergrens}'
        topo = self.genereer_1(
            Id,
            persistence,
            lacunarity,
            octaves,
            scaleX,
            scaleY,
            noise_type
        )
        topo = np.where(topo < bovengrens, 1, -1) * np.where(topo > ondergrens, 1, -1)
        antwoord = []
        for i in range(N):
            antwoord.append(topo)
        return np.stack(antwoord)

