import random
from math import sqrt
import numpy as np
import pandas as pd
from PIL import Image, ImageShow
from projectClasses.PerlinBlotter import PerlinBlotter
from projectClasses.Utilities import replace_with_dict

class PerlinTopoGeneratator:
    def __init__(self,
                 breedte,
                 hoogte,
                 kleur_verhoudingen,
                 versie,
                 naam_basis):
        self.h = hoogte
        self.w = breedte
        self.kleur_verhoudingen = kleur_verhoudingen.rename(columns={'aantal': 'wenselijk_aantal'})
        aantal_kleurmetingen = self.kleur_verhoudingen['wenselijk_aantal'].sum()
        self.kleur_verhoudingen['verhouding'] = self.kleur_verhoudingen['wenselijk_aantal'] / aantal_kleurmetingen
        self.versie = versie
        self.lichte_kleur = self.kleur_verhoudingen.tail(1)
        self.donkere_kleur = self.kleur_verhoudingen.head(1)
        self.kleur_verhoudingen.drop(self.lichte_kleur.index, inplace=True)
        self.kleur_verhoudingen.drop(self.donkere_kleur.index, inplace=True)
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
        self.naam = naam_basis + "b" + str(breedte) + "h" + str(hoogte)
        self.verdeling_in_N_naar_kleur = dict(zip(self.kleur_verhoudingen.verdeling_in_N, zip(self.kleur_verhoudingen.R,
                                                                                              self.kleur_verhoudingen.G,
                                                                                              self.kleur_verhoudingen.B)))

    def afmetingen(self):
        return "_W" + str(self.w) + \
               "_H" + str(self.h)

    def generate_globale_topo(self,
                              aantal,
                              blot_grootte_factor,
                              octaves,
                              persistence,
                              lacunarity,
                              scaleX,
                              scaleY,
                              grenswaarde):
        blotter = PerlinBlotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, grenswaarde)
        self.naam = self.naam + "_glob_a" + str(aantal) + "bg" + str(blot_grootte_factor) + blotter.naam
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
            #blotDiameter = int(max(sqrt(max_delta) * 2, (sqrt(aantal) * 10) // (i + 1)))
            blotDiameter = int(sqrt(max_delta + aantal - i) * blot_grootte_factor)
            blotDiameter = random.randint(blotDiameter // 2, blotDiameter)
            blot = blotter.blot(blotDiameter, blotDiameter)
            print("blotdiameter", blotDiameter)
            # plaatsen van de blot op canvas
            # we werken vanaf linksboven
            # We doen dit 3 keer. Eerst licht met negatieve extra vershuiving. Dan donker met extra verschuiving. Dan kleur zonder extra verschuiving.
            x_verschuiving = np.random.randint(blotDiameter + self.w) - blotDiameter
            y_verschuiving = np.random.randint(blotDiameter + self.h) - blotDiameter
            xEind = min(x_verschuiving + blotDiameter, self.w)
            yEind = min(y_verschuiving + blotDiameter, self.h)
            xStart = max(0, x_verschuiving)
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
        # In gereedheid brengen voor locale topo
        aantal_per_M = self.kleurgroepen_globaal[['verdeling_in_M', 'aantal']]
        self.kleurgroepen_detail = self.kleurgroepen_globaal.drop(
            columns=['verhouding', 'wenselijk_aantal', 'delta_aantal'])
        self.kleurgroepen_detail = self.kleur_verhoudingen.\
            join(self.kleurgroepen_detail.set_index('verdeling_in_M'), on='verdeling_in_M').\
            sort_values(by='verdeling_in_N')

        # Per globaal kleurnumme het hoogste lokale kleurnummer vinden
        minKleurAantallen = self.kleurgroepen_detail.groupby(['verdeling_in_M'])['wenselijk_aantal'] \
            .min() \
            .to_list()
        # We zetten nu de regels zonder minKleurAantallen op 0
        min_kleur_nummers_lokaal = self.kleurgroepen_detail[self.kleurgroepen_detail['aantal'] != 0][
            'verdeling_in_M'].min()
        self.kleurgroepen_detail.loc[
            ~self.kleurgroepen_detail['wenselijk_aantal'].isin(minKleurAantallen), 'aantal'] = 0
        self.kleurgroepen_detail['wenselijk_aantal'] = self.kleurgroepen_detail['verhouding'] * self.w * self.h
        self.kleurgroepen_detail['delta_aantal'] = self.kleurgroepen_detail['wenselijk_aantal'] - \
                                                   self.kleurgroepen_detail['aantal']
        # Nu invullen canvaslocaal met echte kleurnummers
        temp_kleurgroepen = self.kleurgroepen_detail[self.kleurgroepen_detail['aantal'] > 0]
        vertaalTabel = dict(zip(temp_kleurgroepen.verdeling_in_M, temp_kleurgroepen.verdeling_in_N))
        self.canvas_detail = replace_with_dict(self.canvas_globaal, vertaalTabel)
        i = 1

    def generate_locale_topo(self,
                             aantal,
                             blot_grootte_factor,
                             octaves,
                             persistence,
                             lacunarity,
                             scaleX,
                             scaleY,
                             grenswaarde):
        blotter = PerlinBlotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, grenswaarde)
        self.naam = self.naam + "_det_a" + str("{:02d}".format(aantal)) + "_bg" + str("{:02d}".format(blot_grootte_factor)) + blotter.naam + "v" + str("{:02d}".format(self.versie))

        # Eerst van hoofdkl
        for i in range(aantal):
            # Boekhouding op orde
            for j in self.kleurgroepen_detail['verdeling_in_N']:
                self.canvas_detail[0, j] = j
            kleurnummer, aantallen_per_detailkleur = np.unique(self.canvas_detail,
                                                              return_counts=True)
            self.kleurgroepen_detail['aantal'] = aantallen_per_detailkleur
            self.kleurgroepen_detail['delta_aantal'] = self.kleurgroepen_detail['wenselijk_aantal'] - \
                                                       self.kleurgroepen_detail['aantal']

            max_deltas = self.kleurgroepen_detail.groupby(['verdeling_in_M'])['delta_aantal'].max()
            # transities per groep bepalen
            dummy = self.kleurgroepen_detail[self.kleurgroepen_detail['delta_aantal'].\
                isin(max_deltas)].\
                groupby(['verdeling_in_M'])[['verdeling_in_M', 'verdeling_in_N']].\
                max().\
                rename(columns= {'verdeling_in_N':'doel'}).\
                join(self.kleurgroepen_detail.set_index('verdeling_in_M'), rsuffix ='_r')

            doel_kleurnummers = dict(zip(dummy.verdeling_in_N, dummy.doel))
            # We maken een blot met oppervlakte gelijk aan delta wenselijk aantal en werkelijk aantal
            # eerst vierkant later kan dat mooier gemaakt
            #blotDiameter = int(max(sqrt(max_deltas.max()) * blot_grootte_factor, (sqrt(aantal) * 10) // (i + 1)))
            blotDiameter = int(sqrt(max_deltas.max() + aantal - i) * blot_grootte_factor )
            blotDiameter = random.randint(blotDiameter // 2, blotDiameter)
            blot = blotter.blot(blotDiameter, blotDiameter)
            # plaatsen van de blot op canvas
            # we werken vanaf linksboven
            x_verschuiving = np.random.randint(blotDiameter + self.w) - blotDiameter
            xEind = min(x_verschuiving + blotDiameter, self.w)
            xStart = max(0, x_verschuiving)
            y_verschuiving = np.random.randint(blotDiameter + self.h) - blotDiameter
            yEind = min(y_verschuiving + blotDiameter, self.h)
            yStart = max(0, y_verschuiving)

            print('i', i)
            print(self.kleurgroepen_detail)
            print(doel_kleurnummers)
            print('x ', xStart, '-', xEind, 'displacementX', x_verschuiving)
            print('y ', yStart, '-', yEind, 'displacementY', y_verschuiving)
            print("blotdiameter", blotDiameter)
            print("")

            if blotDiameter <= 10:
                break

            for x in range(xStart, xEind):
                for y in range(yStart, yEind):
                    if blot[x - x_verschuiving, y - y_verschuiving] == 1:
                        self.canvas_detail[x, y] = doel_kleurnummers.get(self.canvas_detail[x, y])


