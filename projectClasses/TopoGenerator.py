from projectClasses.NoiseFactory import NoiseFactory
from sklearn.preprocessing import normalize
import numpy as np


def schaal_naar_bereik(arr, bereik=1):
    min = np.min(arr)
    return (((arr - min) * 2 / (np.max(arr) - min)) - 1) * bereik


class TopoGenerator:
    def __init__(self,
                 versie,
                 breedte,
                 hoogte,
                 N):
        self.versie = versie
        self.breedte = breedte
        self.hoogte = hoogte
        self.N = N
        self.info = ""

    def genereer_noise(self,
                 persistence,
                 lacunarity,
                 octaves,
                 scaleX,
                 scaleY,
                 noise_type,
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
        topografie = schaal_naar_bereik(topografie, bereik)
        return topografie

    def genereer_1_noise(self,
                   Id,
                   persistence,
                   lacunarity,
                   octaves,
                   scaleX,
                   scaleY,
                   noise_type,
                   bereik=1
                   ):
        self.info = f'{self.info},Id,{Id},noise,{noise_type},o,{octaves},per,{persistence},lan,{lacunarity},scaleX,{scaleX},scaleY,{scaleY},versie,{self.versie},bereik,{bereik}'
        return self.genereer_noise(persistence,
                             lacunarity,
                             octaves,
                             scaleX,
                             scaleY,
                             noise_type,
                             bereik
                             )

    def genereer_N_noise(self,
                   Id,
                   persistence,
                   lacunarity,
                   octaves,
                   scaleX,
                   scaleY,
                   noise_type,
                   bereik=1
                   ):
        self.info = f'{self.info},Id,{Id},noise,{noise_type},o,{octaves},per,{persistence},lan,{lacunarity},scaleX,{scaleX},scaleY,{scaleY},versie,{self.versie},bereik,{bereik}'

        antwoord = []
        for i in range(self.N):
            antwoord.append(self.genereer_noise(persistence,
                                          lacunarity,
                                          octaves,
                                          scaleX,
                                          scaleY,
                                          noise_type,
                                          bereik))

        return np.stack(antwoord)

    def binair(self,
                 Id,
                 topo_in,
                 grens,
                 bereik
                 ):
        self.info = f'{self.info},BinairId,{Id},grens,{grens},bereik.{bereik}'
        topo = np.copy(topo_in)
        topo = np.where(topo < grens, bereik, -bereik)
        return topo
    
    def vouw_over_grens_en_schaal(self,
                Id,
                topo_in,
                grens,
                bereik
                ):
        self.info = f'{self.info},VouwId,{Id},grens,{grens},bereik,{bereik}'
        topo = np.copy(topo_in)
        topo = np.where(topo < grens, topo - grens, grens - topo) 
        topo = schaal_naar_bereik(topo, bereik)
        return topo
    
    def verhef_tot_macht(self,
                Id,
                topo_in,
                macht,
                bereik
                ):
        self.info = f'{self.info},MachtId,{Id},macht,{macht},bereik,{bereik}'
        topo = np.power(topo_in, macht)
        topo = schaal_naar_bereik(topo)
        return topo
    
    def negate(self,
                Id,
                topo_in
                ):
        self.info = f'{self.info},NegateId,{Id}'
        topo = -np.copy(topo_in)
        return topo
    
    def breidt_1_uit_naar_N(self,
                Id,
                topo_in):
        self.info = f'{self.info},uitbreidingId,{Id}'
        antwoord = []
        for i in range(self.N):
            antwoord.append(topo_in)
        return antwoord


