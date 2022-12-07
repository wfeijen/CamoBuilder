import random
from math import sqrt
import numpy as np
import pandas as pd
from PIL import Image, ImageShow
from projectClasses.PerlinBlotter import PerlinBlotter
from projectClasses.Utilities import replace_with_dict
import re


class PerlinTopoGeneratator:
    def __init__(self,
                 breedte,
                 hoogte,
                 kleur_verhoudingen,
                 versie,
                 naam_basis,
                 richtingGenerator,
                 contrast,
                 belichting):
        self.h = hoogte
        self.w = breedte
        kleur_verhoudingen.iloc[:, 0:3] -= 128
        kleur_verhoudingen.iloc[:, 0:3] = (kleur_verhoudingen.iloc[:, 0:3] * contrast)
        kleur_verhoudingen.iloc[:, 0:3] += 128
        kleur_verhoudingen.iloc[:, 0:3] = (kleur_verhoudingen.iloc[:, 0:3] * belichting)
        kleur_verhoudingen.iloc[:, 0:3].clip(lower=0, upper = 255).astype(int)

        self.kleur_verhoudingen = kleur_verhoudingen.rename(columns={'aantal': 'wenselijk_aantal'})
        aantal_kleurmetingen = self.kleur_verhoudingen['wenselijk_aantal'].sum()
        self.kleur_verhoudingen['verhouding'] = self.kleur_verhoudingen['wenselijk_aantal'] / aantal_kleurmetingen
        self.versie = versie

        # We gaan nu eerst de tellingen per kleurgroep op orde maken en canvas uitvullen met het meest voorkomende kleurgroep nummer
        self.kleurgroepen_globaal = self.kleur_verhoudingen.groupby(['verdeling_in_M'])[
            'verhouding'].sum().reset_index()
        aantal_pixels = self.w * self.h
        self.kleurgroepen_globaal['wenselijk_aantal'] = (self.kleurgroepen_globaal['verhouding'] * aantal_pixels).astype(int)
        self.kleurgroepen_globaal['aantal'] = np. \
            where(self.kleurgroepen_globaal['verhouding'] == self.kleurgroepen_globaal['verhouding'].min(),
                  aantal_pixels, 0)

        # Afscheiden licht en donkere kleuren
        # min_kleur_nummer = self.kleurgroepen_globaal[self.kleurgroepen_globaal['aantal'] != 0]['verdeling_in_M'].min()
        kleurnummers_zonder_licht_en_donker = self.kleurgroepen_globaal[1: len(self.kleurgroepen_globaal.index) - 1]
        min_kleur_nummer = int(kleurnummers_zonder_licht_en_donker.loc[kleurnummers_zonder_licht_en_donker['wenselijk_aantal'].idxmin()]['verdeling_in_M'])

        self.canvas_globaal = np.full((self.w, self.h), min_kleur_nummer)
        self.naam = naam_basis + ",breedte," + str(breedte) + ",hoogte," + str(hoogte) + \
                    ",contrast," + str(contrast) + ",belichting," + str(belichting)
        self.verdeling_in_N_naar_kleur = dict(zip(self.kleur_verhoudingen.verdeling_in_N,
                                                  zip(self.kleur_verhoudingen.R,
                                                      self.kleur_verhoudingen.G,
                                                      self.kleur_verhoudingen.B)))
        self.richtingGenerator = richtingGenerator
        print(self.naam)


    def afmetingen(self):
        return "_W" + str(self.w) + \
               "_H" + str(self.h)

    def generate_globale_topo(self,
                              Id,
                              aantal,
                              blot_grootte_factor,
                              min_blotgrootte,
                              max_blotgrootte,
                              octaves,
                              persistence,
                              lacunarity,
                              scaleX,
                              scaleY,
                              afplatting,
                              grenswaarde,
                              max_waarde_stopconditie = -100000):
        blotter = PerlinBlotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, grenswaarde)
        self.naam = self.naam + ",globaal,aant," + str(aantal) + ",blotGroottefact," + str(blot_grootte_factor) + \
                    ",minBlotGrootte,"  + str(min_blotgrootte) + ",maxBlotGrootte," + str(max_blotgrootte) + ",afplatting," + str(afplatting) + \
                    ",stopconditie," + str(max_waarde_stopconditie) + blotter.naam
        print(self.naam)
        indexWit = len(self.kleurgroepen_globaal.index) - 1
        indexZwart = 0
        blot_vraag_antwoord_verhouding = 1
        for i in range(aantal):
            # Boekhouding op orde
            for j in self.kleurgroepen_globaal['verdeling_in_M']:
                self.canvas_globaal[0, j] = j
            kleurnummer, aantallen_per_hoofdkleur = np.unique(self.canvas_globaal,
                                                              return_counts=True)
            self.kleurgroepen_globaal['aantal'] = aantallen_per_hoofdkleur
            self.kleurgroepen_globaal['delta_aantal'] = self.kleurgroepen_globaal['wenselijk_aantal'] - \
                                                        self.kleurgroepen_globaal['aantal']
            max_delta = self.kleurgroepen_globaal.iloc[indexZwart+1:indexWit]['delta_aantal'].max()
            min_delta = self.kleurgroepen_globaal.iloc[indexZwart+1:indexWit]['delta_aantal'].min()

            max_delta_kleurgroep = self.kleurgroepen_globaal[self.kleurgroepen_globaal['delta_aantal'] == max_delta][
                'verdeling_in_M'].max()
            # We maken een blot met oppervlakte gelijk aan delta wenselijk aantal en werkelijk aantal
            # eerst vierkant later kan dat mooier gemaakt
            #blotDiameter = int(max(sqrt(max_delta) * 2, (sqrt(aantal) * 10) // (i + 1)))
            blotDiameter = int(sqrt(max(10, max_delta)) * blot_grootte_factor)

            if blotDiameter > max_blotgrootte: blotDiameter = (max_blotgrootte + blotDiameter) // 2
            if blotDiameter < min_blotgrootte: blotDiameter = (blotDiameter + min_blotgrootte) // 2
            # Aanpassen op het feit dat de blotter altijd een kleinere blot geeft
            blotDiameter = max(int(blotDiameter * blot_vraag_antwoord_verhouding), 10)
            blotDiameterY = max(int(blotDiameter * afplatting), 5 * blot_grootte_factor)
            blotDiameterX = max(int(blotDiameter / afplatting), 5 * blot_grootte_factor)
            blot = blotter.blot(blotDiameterX, blotDiameterY)
            blotDiameterX, blotDiameterY = blot.shape

            blot_vraag_antwoord_verhouding = max(min(((blot_vraag_antwoord_verhouding * 9) + (blotDiameter ** 2 / (blotDiameterX * blotDiameterY + 1))) / 10, 10), 0.1)

            # plaatsen van de blot op canvas. We weten nu het relevante deel van de blot
            # we werken vanaf linksboven
            # We doen dit 3 keer. Eerst licht met negatieve extra vershuiving. Dan donker met extra verschuiving. Dan kleur zonder extra verschuiving.
            x_verschuiving = np.random.randint(blotDiameterX + self.w) - blotDiameterX // 2
            y_verschuiving = np.random.randint(blotDiameterY + self.h) - blotDiameterY // 2

            # Eerst wit
            deltaX, deltaY = self.richtingGenerator.geef_richting(max_afstand=int(self.kleurgroepen_globaal.iloc[indexWit]['delta_aantal']) / blotDiameter)
            xStart = max(0, x_verschuiving + deltaX)
            yStart = max(0, y_verschuiving + deltaY)
            xEind = min(x_verschuiving + blotDiameterX + deltaX, self.w)
            yEind = min(y_verschuiving + blotDiameterY + deltaY, self.h)
            for x in range(xStart, xEind):
                for y in range(yStart, yEind):
                    # print(str(x) + " " + str(y))
                    if blot[x - x_verschuiving - deltaX, y - y_verschuiving - deltaY] == 1:
                        self.canvas_globaal[x, y] = indexWit

            # Nu zwart
            deltaX, deltaY = self.richtingGenerator.geef_richting(max_afstand=int(self.kleurgroepen_globaal.iloc[indexZwart]['delta_aantal']) / blotDiameter)
            xStart = max(0, x_verschuiving - deltaX)
            yStart = max(0, y_verschuiving - deltaY)
            xEind = min(x_verschuiving + blotDiameterX - deltaX, self.w)
            yEind = min(y_verschuiving + blotDiameterY - deltaY, self.h)
            for x in range(xStart, xEind):
                for y in range(yStart, yEind):
                    if blot[x - x_verschuiving + deltaX, y - y_verschuiving + deltaY] == 1:
                        self.canvas_globaal[x, y] = indexZwart

            # Nu de reguliere kleur
            xStart = max(0, x_verschuiving)
            yStart = max(0, y_verschuiving)
            xEind = min(x_verschuiving + blotDiameterX, self.w)
            yEind = min(y_verschuiving + blotDiameterY, self.h)
            for x in range(xStart, xEind):
                for y in range(yStart, yEind):
                    if blot[x - x_verschuiving, y - y_verschuiving] == 1:
                        self.canvas_globaal[x, y] = max_delta_kleurgroep

            print(f"{Id} {max_delta: 7d} i:{i: 4d} blotdiameter x {blotDiameterX: 4d} blotdiameter y {blotDiameterY:4d} blotsizefact:{round(blot_vraag_antwoord_verhouding, 2): 2.2f} "+
                  f"xStart:{xStart: 5d} xEind:{xEind: 5d} yStart:{yStart: 5d} yEind:{yEind: 5d} " +
                  re.sub(r"(\n)?([0-9]{1,2}) +", r"  \2:", ''.join(str(self.kleurgroepen_globaal['delta_aantal']))).replace("\nName: delta_aantal, dtype: int64", "   "))
            if max_delta < max_waarde_stopconditie:
                break

    def bereid_lokale_topos_voor(self):
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
        self.kleurgroepen_detail['wenselijk_aantal'] = (self.kleurgroepen_detail['verhouding'] * self.w * self.h).astype(int)
        self.kleurgroepen_detail['delta_aantal'] = self.kleurgroepen_detail['wenselijk_aantal'] - \
                                                   self.kleurgroepen_detail['aantal']
        # Nu invullen canvaslocaal met echte kleurnummers
        temp_kleurgroepen = self.kleurgroepen_detail[self.kleurgroepen_detail['aantal'] > 0]
        vertaalTabel = dict(zip(temp_kleurgroepen.verdeling_in_M, temp_kleurgroepen.verdeling_in_N))
        self.canvas_detail = replace_with_dict(self.canvas_globaal, vertaalTabel)
        i = 1

    def generate_locale_topo(self,
                             Id,
                             aantal,
                             blot_grootte_factor,
                             min_blotgrootte,
                             max_blotgrootte,
                             octaves,
                             persistence,
                             lacunarity,
                             scaleX,
                             scaleY,
                             afplatting,
                             grenswaarde,
                             max_waarde_stopconditie = -100000):
        blotter = PerlinBlotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, grenswaarde)
        self.naam = self.naam + ",detail,aantal," + str("{:02d}".format(aantal)) + ",blotGr," + str(blot_grootte_factor) + \
                    ",minBlotGrootte,"  + str(min_blotgrootte) + ",maxBlotGrootte," + str(max_blotgrootte) + \
                    ",afplatting," + str(afplatting) + ",stopconditie," + str(max_waarde_stopconditie) + blotter.naam
        print(self.naam)
        blot_vraag_antwoord_verhouding = 1
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
            blotDiameter = int(sqrt(max(4, max_deltas.max())) * blot_grootte_factor)

            if blotDiameter > max_blotgrootte: blotDiameter = (max_blotgrootte + blotDiameter) // 2
            elif blotDiameter < min_blotgrootte: blotDiameter = (blotDiameter + min_blotgrootte) // 2
            # Aanpassen op het feit dat de blotter altijd een kleinere blot geeft
            blotDiameter = int(blotDiameter * blot_vraag_antwoord_verhouding)
            blotDiameterY = int(blotDiameter * afplatting)
            blotDiameterX = int(blotDiameter / afplatting)
            blot = blotter.blot(blotDiameterX, blotDiameterY)
            blotDiameterX, blotDiameterY = blot.shape

            blot_vraag_antwoord_verhouding = min(((blot_vraag_antwoord_verhouding * 9) + (blotDiameter ** 2 / (blotDiameterX * blotDiameterY + 1))) / 10, 10)
            # plaatsen van de blot op canvas
            # we werken vanaf linksboven
            x_verschuiving = np.random.randint(blotDiameterX + self.w) - (blotDiameterX // 2)
            xEind = min(x_verschuiving + blotDiameterX, self.w)
            xStart = max(0, x_verschuiving)
            y_verschuiving = np.random.randint(blotDiameterY + self.h) - (blotDiameterY // 2)
            yEind = min(y_verschuiving + blotDiameterY, self.h)
            yStart = max(0, y_verschuiving)

            # print(Id + "   i:" + str(i) + " blotsizefact:" + str(round(blot_vraag_antwoord_verhouding, 2)) + "   " +
            #       " grootste:" + str(max_deltas.max()) +
            #       re.sub(r"(\n)?([0-9]{1,2}) +", r"  \2:", ''.join(str(self.kleurgroepen_detail['delta_aantal']))).replace("\nName: delta_aantal, dtype: int64", "   ") +
            #       "blotdiameter x", blotDiameterX, "blotdiameter y", blotDiameterY)

            print(f"{Id} {max_deltas.max(): 7d} i:{i: 4d} blotdiameter x {blotDiameterX: 4d} blotdiameter y {blotDiameterY:4d} blotsizefact:{round(blot_vraag_antwoord_verhouding, 2): 2.2f} "+
                  f"xStart:{xStart: 5d} xEind:{xEind: 5d} yStart:{yStart: 5d} yEind:{yEind: 5d} " +
                  re.sub(r"(\n)?([0-9]{1,2}) +", r"  \2:", ''.join(str(self.kleurgroepen_detail['delta_aantal']))).replace("\nName: delta_aantal, dtype: int64", "   "))


            for x in range(xStart, xEind):
                for y in range(yStart, yEind):
                    if blot[x - x_verschuiving, y - y_verschuiving] == 1:
                        self.canvas_detail[x, y] = doel_kleurnummers.get(self.canvas_detail[x, y])
            if max_deltas.max() < max_waarde_stopconditie:
                break


