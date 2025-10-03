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
        topografie = np.zeros((self.breedte, self.hoogte))
        if bereik > 0:
            noiseMachine = NoiseFactory(noise_type)        
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
    
    def modulo_1_canvas(self,
               Id,
               topo_in,
               grens):
        self.info = f'{self.info},moduloId,{Id},grens,{grens}'
        topo = np.mod(topo_in, grens)
        return topo
    
    def modulo_N_canvas(self,
            Id,
            topos_in,
            grens):
        self.info = f'{self.info},moduloNId,{Id},grens,{grens}'
        topos = [np.mod(topo, grens) for topo in topos_in]
        return topos
    
    def tilt_1_canvas(self,
                      Id,
                      topo_in,
                      tilt_x,
                      tilt_y):
        tilt_x_canvas = np.full(topo_in.shape, tilt_x)
        tilt_x_canvas = np.cumsum(tilt_x_canvas, 1)
        tilt_y_canvas = np.full(topo_in.shape, tilt_y)
        tilt_y_canvas = np.cumsum(tilt_y_canvas, 1)
        return topo_in + tilt_x_canvas + tilt_y_canvas
    
    def tilt_N_canvas(self,
                      Id,
                      topos_in,
                      tilt_x,
                      tilt_y):
        tilt_x_canvas = np.full(topos_in[0].shape, tilt_x)
        tilt_x_canvas = np.cumsum(tilt_x_canvas, 1)
        tilt_y_canvas = np.full(topos_in[0].shape, tilt_y)
        tilt_y_canvas = np.cumsum(tilt_y_canvas, 1)
        return [topo_in + tilt_x_canvas + tilt_y_canvas for topo_in in topos_in]
        


