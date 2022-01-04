import random
from math import sqrt
import numpy as np
import pandas as pd
from PIL import Image, ImageShow
from projectClasses.perlinBlotCreator import PerlinBlotter


class PerlinTopoGeneratator:
    def __init__(self,
                 breedte,
                 hoogte,
                 kleur_verhoudingen,
                 versie):
        self.h = hoogte
        self.w = breedte
        self.kleur_verhoudingen = kleur_verhoudingen.rename(columns={'aantal': 'wenselijk_aantal'})
        aantal_kleurmetingen = self.kleur_verhoudingen['wenselijk_aantal'].sum()
        self.kleur_verhoudingen['verhouding'] = self.kleur_verhoudingen['wenselijk_aantal'] / aantal_kleurmetingen
        self.versie = versie
        # We gaan nu eerst de tellingen per kleurgroep op orde maken en canvas uitvullen met het meest voorkomende kleurgroep nummer
        self.kleurgroepen_globaal = self.kleur_verhoudingen.groupby(['verdeling_in_M'])[
            'verhouding'].sum().reset_index()
        aantal_pixels = self.w * self.h
        self.kleurgroepen_globaal['wenselijk_aantal'] = self.kleurgroepen_globaal['verhouding'] * aantal_pixels
        self.kleurgroepen_globaal['aantal'] = np. \
            where(self.kleurgroepen_globaal['verhouding'] == self.kleurgroepen_globaal['verhouding'].min(),
                  aantal_pixels, 0)
        min_kleur_nummer = self.kleurgroepen_globaal[self.kleurgroepen_globaal['aantal'] != 0]['verdeling_in_M'].min()
        self.canvas_globaal = np.full((self.w, self.h), min_kleur_nummer)
        self.naam = "v" + str(self.versie)

    def afmetingen(self):
        return "_W" + str(self.w) + \
               "_H" + str(self.h)

    def generate_globale_topo(self,
                              aantal,
                              octaves,
                              persistence,
                              lacunarity,
                              scaleX,
                              scaleY,
                              grenswaarde):
        blotter = PerlinBlotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, grenswaarde)
        for i in range(aantal):
            # Boekhouding op orde
            for j in self.kleurgroepen_globaal['verdeling_in_M']:
                self.canvas_globaal[0, j] = j
            kleurnummer, aantallen_per_hoofdkleur = np.unique(self.canvas_globaal,
                                                              return_counts=True)
            self.kleurgroepen_globaal['aantal'] = aantallen_per_hoofdkleur
            self.kleurgroepen_globaal['delta_aantal'] = self.kleurgroepen_globaal['wenselijk_aantal'] - \
                                                        self.kleurgroepen_globaal['aantal']
            max_delta = self.kleurgroepen_globaal['delta_aantal'].max()
            max_delta_kleurgroep = self.kleurgroepen_globaal[self.kleurgroepen_globaal['delta_aantal'] == max_delta][
                'verdeling_in_M'].max()
            # We maken een blot met oppervlakte gelijk aan delta wenselijk aantal en werkelijk aantal
            # eerst vierkant later kan dat mooier gemaakt
            blotDiameter = int(max(sqrt(max_delta) * 2, (sqrt(aantal) * 10) // (i + 1)))
            blotDiameter = random.randint(blotDiameter // 2, blotDiameter)
            blot = blotter.blot(blotDiameter, blotDiameter)
            print("blotdiameter", blotDiameter)
            # plaatsen van de blot op canvas
            # we werken vanaf linksboven
            x_verschuiving = np.random.randint(blotDiameter + self.w) - blotDiameter
            xEind = min(x_verschuiving + blotDiameter, self.w)
            xStart = max(0, x_verschuiving)
            y_verschuiving = np.random.randint(blotDiameter + self.h) - blotDiameter
            yEind = min(y_verschuiving + blotDiameter, self.h)
            yStart = max(0, y_verschuiving)

            print("")
            print(self.kleurgroepen_globaal)
            print('i', i)
            print('kleur', max_delta_kleurgroep)
            print('blotDiam', blotDiameter)
            print('x ', xStart, '-', xEind, 'displacementX', x_verschuiving)
            print('y ', yStart, '-', yEind, 'displacementY', y_verschuiving)

            if blotDiameter <= 10:
                break

            for x in range(xStart, xEind):
                for y in range(yStart, yEind):
                    if blot[x - x_verschuiving, y - y_verschuiving] == 1:
                        self.canvas_globaal[x, y] = max_delta_kleurgroep
        self.naam = self.naam + "_glog_" + blotter.name()
        # In gereedheid brengen voor locale topo
        aantal_per_M = self.kleurgroepen_globaal[['verdeling_in_M', 'aantal']]
        self.kleurgroepen_lokaal = self.kleurgroepen_globaal.drop(
            columns=['verhouding', 'wenselijk_aantal', 'delta_aantal'])
        self.kleurgroepen_lokaal = self.kleur_verhoudingen \
            .join(self.kleurgroepen_lokaal.set_index('verdeling_in_M'), on='verdeling_in_M')

        # Per globaal kleurnumme het hoogste lokale kleurnummer vinden
        minKleurAantallen = self.kleurgroepen_lokaal.groupby(['verdeling_in_M'])['wenselijk_aantal'] \
            .min() \
            .to_list()
        # We zetten nu de regels zonder minKleurAantallen op 0
        min_kleur_nummers_lokaal = self.kleurgroepen_lokaal[self.kleurgroepen_lokaal['aantal'] != 0][
            'verdeling_in_M'].min()
        self.kleurgroepen_lokaal.loc[
            ~self.kleurgroepen_lokaal['wenselijk_aantal'].isin(minKleurAantallen), 'aantal'] = 0
        self.kleurgroepen_lokaal['wenselijk_aantal'] = self.kleurgroepen_lokaal['verhouding'] * self.w * self.h
        self.kleurgroepen_lokaal['delta_aantal'] = self.kleurgroepen_lokaal['wenselijk_aantal'] - \
                                                   self.kleurgroepen_lokaal['aantal']

    def generate_locale_topo(self,
                             aantal,
                             octaves,
                             persistence,
                             lacunarity,
                             scaleX,
                             scaleY,
                             grenswaarde):
        blotter = PerlinBlotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, grenswaarde)
        # Eerst van hoofdkl
        for i in range(aantal):
            # Boekhouding op orde
            for j in self.kleurgroepen_lokaal['verdeling_in_M']:
                self.canvas_globaal[0, j] = j
            kleurnummer, aantallen_per_hoofdkleur = np.unique(self.canvas_globaal,
                                                              return_counts=True)
            self.kleurgroepen_globaal['aantal'] = aantallen_per_hoofdkleur
            self.kleurgroepen_globaal['delta_aantal'] = self.kleurgroepen_globaal['wenselijk_aantal'] - \
                                                        self.kleurgroepen_globaal['aantal']
            max_delta = self.kleurgroepen_globaal['delta_aantal'].max()
            max_delta_kleurgroep = self.kleurgroepen_globaal[self.kleurgroepen_globaal['delta_aantal'] == max_delta][
                'verdeling_in_M'].max()
            # We maken een blot met oppervlakte gelijk aan delta wenselijk aantal en werkelijk aantal
            # eerst vierkant later kan dat mooier gemaakt
            blotDiameter = int(max(sqrt(max_delta) * 2, (sqrt(aantal) * 10) // (i + 1)))
            blotDiameter = random.randint(blotDiameter // 2, blotDiameter)
            blot = blotter.blot(blotDiameter, blotDiameter)
            print("blotdiameter", blotDiameter)
            # plaatsen van de blot op canvas
            # we werken vanaf linksboven
            x_verschuiving = np.random.randint(blotDiameter + self.w) - blotDiameter
            xEind = min(x_verschuiving + blotDiameter, self.w)
            xStart = max(0, x_verschuiving)
            y_verschuiving = np.random.randint(blotDiameter + self.h) - blotDiameter
            yEind = min(y_verschuiving + blotDiameter, self.h)
            yStart = max(0, y_verschuiving)

            print("")
            print(self.kleurgroepen_globaal)
            print('i', i)
            print('kleur', max_delta_kleurgroep)
            print('blotDiam', blotDiameter)
            print('x ', xStart, '-', xEind, 'displacementX', x_verschuiving)
            print('y ', yStart, '-', yEind, 'displacementY', y_verschuiving)

            if blotDiameter <= 10:
                break

            for x in range(xStart, xEind):
                for y in range(yStart, yEind):
                    if blot[x - x_verschuiving, y - y_verschuiving] == 1:
                        self.canvas_globaal[x, y] = max_delta_kleurgroep
        self.naam = self.naam + "_glog_" + blotter.name()
        self.kleurgroepen_lokaal = self.kleurgroepen_globaal.drop(
            columns=['verhouding', 'wenselijk_aantal', 'delta_aantal'])
        self.kleurgroepen_lokaal = self.kleur_verhoudingen. \
            join(self.kleurgroepen_lokaal.set_index('verdeling_in_M'), on='verdeling_in_M')


kleurenPad = '../kleurParameters/graslandZomer3.jpg20210815 172940.csv'

kleurInfo = pd.read_csv(kleurenPad, index_col=0)
ptg = PerlinTopoGeneratator(
    breedte=150,
    hoogte=200,
    kleur_verhoudingen=kleurInfo,
    versie=1)

ptg.generate_globale_topo(
    aantal=150,
    persistence=0.3,
    lacunarity=4.0,
    octaves=8,
    scaleX=100,
    scaleY=200,
    grenswaarde=0.5)


# ptg.generate_globale_topo(
#     aantal = 150,
#     persistence=0.2,
#     lacunarity=2.0,
#     octaves=8,
#     scaleX=50,
#     scaleY=100,
#     grenswaarde=0.5)

# ptg.generate_globale_topo(
#     aantal = 150,
#     persistence=0.3,
#     lacunarity=4.0,
#     octaves=4,
#     scaleX=300,
#     scaleY=300,
#     grenswaarde=0.5)

# ptg = PerlinTopoGeneratator(
#     breedte=1500,
#     hoogte=2000,
#     aantal_globaal=100,
#     aantal_detail=3,
#     kleur_verhoudingen=kleurInfo,
#     persistence=0.3,
#     lacunarity=8.0,
#     octaves=8,
#     scaleX=200,
#     scaleY=200,
#     grenswaarde=0.3,
#     versie = 1)

# ptg = PerlinTopoGeneratator(
#     breedte=1500,
#     hoogte=2000,
#     aantal_globaal=100,
#     aantal_detail=3,
#     kleur_verhoudingen=kleurInfo,
#     octaves=8,
#     persistence=0.2,
#     lacunarity=2.0,
#     scaleX=100,
#     scaleY=200,
#     grenswaarde=0.3,
#     versie = 1)

def show_general_canvas(canvas):
    max = np.amax(canvas)
    print(max)
    print(np.amax(canvas))
    canvas_grens = canvas * 255 / max
    Image.fromarray(np.uint8(canvas_grens)).show()


print(ptg.naam)
show_general_canvas(ptg.canvas_globaal)
