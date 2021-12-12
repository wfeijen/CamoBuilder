from math import sqrt
import numpy as np
import pandas as pd
from PIL import Image
from projectClasses.perlinBlotCreator import PerlinBlotter

class PerlinTopoGeneratator:
    def __init__(self,
                 breedte,
                 hoogte,
                 aantal_globaal,
                 aantal_detail,
                 kleur_verhoudingen,
                 octaves,
                 persistence,
                 lacunarity,
                 scaleX,
                 scaleY,
                 grenswaarde,
                 versie):
        self.h = hoogte
        self.w = breedte
        self.n = aantal_globaal
        self.m = aantal_detail
        self.kleur_verhoudingen = kleur_verhoudingen
        aantal_kleurmetingen = self.kleur_verhoudingen['aantal'].sum()
        self.kleur_verhoudingen['verhouding'] = self.kleur_verhoudingen['aantal'] / aantal_kleurmetingen
        self.versie = versie
        self.blotter = PerlinBlotter(persistence, lacunarity, octaves,scaleX, scaleY, versie, grenswaarde)
        # print(self.naam())

    # def naam(self):
    #     return "_N" + str(self.n) + \
    #            "_o" + str(self.octaves) + \
    #            "_p" + str(self.persistence) + \
    #            "_l" + str(self.lacunarity) + \
    #            "_sx" + str(self.scalex) + \
    #            "_sy" + str(self.scaley) + \
    #            "_v" + str(self.versie)


    def afmetingen(self):
        return "_W" + str(self.w) + \
               "_H" + str(self.h)


    def generate_globale_topo(self):
        # We gaan nu eerst de tellingen per kleurgroep op orde maken en topo uitvullen met het meest voorkomende kleurgroep nummer
        kleurgroepen = self.kleur_verhoudingen.groupby(['verdeling_in_M'])['verhouding'].sum().reset_index()
        aantal_pixels = self.w * self.h
        kleurgroepen['wenselijk_aantal'] = kleurgroepen['verhouding'] * aantal_pixels
        kleurgroepen['aantal'] = np.where(kleurgroepen['verhouding'] == kleurgroepen['verhouding'].max(), aantal_pixels, 0)
        max_kleur_nummer = kleurgroepen[kleurgroepen['aantal'] != 0]['verdeling_in_M'].max()
        topo = np.full((self.w, self.h), max_kleur_nummer)
        # Nu kunnen we met blotten de andere kleuren toe gaan voegen
        for i in range(self.n):
            # We maken een blot met oppervlakte gelijk aan delta wenselijk aantal en werkelijk aantal
            # eerst vierkant later kan dat mooier gemaakt
            kleurgroepen['delta_aantal'] = kleurgroepen['wenselijk_aantal'] - kleurgroepen['aantal']
            max_delta = kleurgroepen['delta_aantal'].max()
            max_delta_kleurgroep = kleurgroepen[kleurgroepen['delta_aantal'] == max_delta]['verdeling_in_M'].max()
            blotDiameter = int(sqrt(max_delta)) * 2
            blot = self.blotter.blot(blotDiameter, blotDiameter)
            # plaatsen van de blot op canvas
            # we werken vanaf linksboven
            x_verschuiving = np.random.randint(blotDiameter + self.w) - blotDiameter
            xEind = min(x_verschuiving + blotDiameter, self.w)
            xStart = max(0, x_verschuiving)
            y_verschuiving = np.random.randint(blotDiameter + self.h) - blotDiameter
            yEind = min(y_verschuiving + blotDiameter, self.h)
            yStart = max(0, y_verschuiving)

            print("")
            print(kleurgroepen)
            print('kleur', max_delta_kleurgroep)
            print('blotDiam', blotDiameter)
            print('x ', xStart, '-', xEind, ' y ', yStart, '-', yEind)

            if blotDiameter <= 10:
                break

            for x in range(xStart, xEind):
                for y in range(yStart, yEind):
                    if blot[x - x_verschuiving, y - y_verschuiving] == 1:
                        # boekhouding bijwerken
                        huidige_kleurgroep = topo[x, y]
                        kleurgroepen.at[huidige_kleurgroep, 'aantal'] -= 1
                        kleurgroepen.at[max_delta_kleurgroep, 'aantal'] += 1
                        topo[x,y] = max_delta_kleurgroep
        return topo

def show_general_canvas(canvas):
    max = np.amax(canvas)
    print(max)
    print(np.amax(canvas))
    canvas_grens = canvas * 255 / max
    Image.fromarray(np.uint8(canvas_grens)).show()


kleurenPad = '../kleurParameters/graslandZomer3.jpg20210815 172940.csv'

kleurInfo = pd.read_csv(kleurenPad, index_col=0)

ptg = PerlinTopoGeneratator(
    breedte=400,
    hoogte=300,
    aantal_globaal=100,
    aantal_detail=3,
    kleur_verhoudingen=kleurInfo,
    persistence=0.4,
    lacunarity=4.0,
    octaves=9,
    scaleX=200,
    scaleY=400,
    grenswaarde=0.5,
    versie = 1)

topo = ptg.generate_globale_topo()

show_general_canvas(topo)