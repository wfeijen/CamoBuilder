import random
from math import sqrt
import numpy as np
import pandas as pd

from projectClasses.PerlinBlotter import PerlinBlotter
from projectClasses.Utilities import replace_with_dict
from projectClasses.RichtingGenerator import RichtingGenerator

MIN_BLOT_DIAMETER = 5
LICHT_DONKER_VERSCHUIVINGSFACTOR = 0.5
LICHT_DONKER_MINIMALE_VERSCHUIVING = 3
LICHT_DONKER_MAXIMALE_VERSCHUIVING = 10
AFKAP_MAX_MIN_DELTA_AANTAL_FACTOR = 0.1
AFKAP_MAX_MIN_DELTA_AANTAL_FACTOR_DETAIL = 0.3


class PerlinTopoGeneratator:
    def __init__(self,
                 breedte,
                 hoogte,
                 kleur_verhoudingen,
                 ondergrens_donker_licht,
                 versie,
                 naam_basis):
        kleurInfo, donker_licht_info, donker_licht_percentage = splits_hoogste_en_laagste_lichtheid_af(kleur_verhoudingen, ondergrens_donker_licht)
        self.h = hoogte
        self.w = breedte
        self.afkap_max_min_delta_aantal = int(sqrt(hoogte * breedte) * AFKAP_MAX_MIN_DELTA_AANTAL_FACTOR)
        self.kleur_verhoudingen = kleurInfo.rename(columns={'aantal': 'wenselijk_aantal'})
        self.versie = versie
        # Licht en donker aantallen berekenen
        self.aantal_pixels = self.w * self.h
        self.totaal_percentage_donker_licht = sum(donker_licht_percentage) / 100
        totaal_absoluut_donker_licht = self.totaal_percentage_donker_licht * self.aantal_pixels
        # aanpassen wenselijke aantal omdat we een deel aan licht en donker hebben vergeven
        self.donker_licht_verdeling = donker_licht_info  # pd.DataFrame({'R':[0, 255], 'G':[0, 0], 'B':[0,0]})#
        self.donker_licht_verdeling['wenselijk_aantal'] = [
            p / self.totaal_percentage_donker_licht / 100 * totaal_absoluut_donker_licht
            for p in donker_licht_percentage]
        self.donker_licht_verdeling['verhouding'] = [x / 100 for x in donker_licht_percentage]

        # We gaan nu eerst de tellingen per kleurgroep op orde maken en canvas uitvullen met het meest voorkomende kleurgroep nummer
        aantal_kleurmetingen = self.kleur_verhoudingen['wenselijk_aantal'].sum()
        self.kleur_verhoudingen['verhouding'] = self.kleur_verhoudingen['wenselijk_aantal'] / aantal_kleurmetingen
        self.kleurgroepen_globaal = self.kleur_verhoudingen.groupby(['verdeling_in_M'])[
            'verhouding'].sum().reset_index()
        self.kleurgroepen_globaal['wenselijk_aantal'] = self.kleurgroepen_globaal['verhouding'] * self.aantal_pixels * (
                1 - self.totaal_percentage_donker_licht)
        self.kleurgroepen_globaal['wenselijk_aantal'] = self.kleurgroepen_globaal['wenselijk_aantal']
        self.kleurgroepen_globaal['aantal'] = np. \
            where(self.kleurgroepen_globaal['verhouding'] == self.kleurgroepen_globaal['verhouding'].min(),
                  self.aantal_pixels, 0)
        min_kleur_nummer = self.kleurgroepen_globaal[self.kleurgroepen_globaal['aantal'] != 0]['verdeling_in_M'].min()
        self.canvas_globaal = np.full((self.w, self.h), min_kleur_nummer)
        self.naam = naam_basis + "b" + str(breedte) + "h" + str(hoogte) + "odl" + str(ondergrens_donker_licht)

    def generate_globale_topo(self,
                              aantal,
                              blot_grootte_factor,
                              octaves,
                              persistence,
                              lacunarity,
                              scaleX,
                              scaleY,
                              grenswaarde,
                              afplatting,
                              richting_kans_verdeling_lb_ro):
        richting_generator = RichtingGenerator(richting_kans_verdeling_lb_ro)
        blotter = PerlinBlotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, grenswaarde)
        self.naam = self.naam + "_glob_a" + str(aantal) + "bg" + str(blot_grootte_factor) + "af" + str(afplatting) + blotter.naam
        for i in range(aantal):
            # Boekhouding op orde
            min_delta_kleurgroepen, max_delta_kleurgroepen, max_delta_kleurgroep, min_delta_donker_licht, max_delta_donker_licht = self.doe_boekhouding_hoofdkleuren()

            # We maken een blot met oppervlakte gelijk aan delta wenselijk aantal en werkelijk aantal
            # eerst vierkant later kan dat mooier gemaakt
            # blotDiameter = int(max(sqrt(max_delta_kleurgroepen) * 2, (sqrt(aantal) * 10) // (i + 1)))
            blotDiameter_t = int(
                sqrt(max(max_delta_kleurgroepen, max_delta_donker_licht) + aantal - i) * blot_grootte_factor)
            blotDiameter_t = random.randint(blotDiameter_t // 2, blotDiameter_t)
            if blotDiameter_t < MIN_BLOT_DIAMETER:
                blotDiameter_t = MIN_BLOT_DIAMETER
            blot_diameter_x = blotDiameter_t
            blot_diameter_y = int(blotDiameter_t * afplatting)

            print("blotdiameter", blot_diameter_x, " _ ", blot_diameter_y)

            # positioneren van de blot op canvas
            # we werken vanaf linksboven
            x_verschuiving = np.random.randint(blot_diameter_x + self.w) - blot_diameter_x
            y_verschuiving = np.random.randint(blot_diameter_y + self.h) - blot_diameter_y
            donker_delta, licht_delta = [x * blotDiameter_t for x in
                                         self.donker_licht_verdeling.delta_percentage.tolist()]
            richting = richting_generator.geef_richting()
            print("")
            print('i', i)
            print(self.kleurgroepen_globaal[['wenselijk_aantal', 'aantal', 'delta_aantal']])
            # We plaatsen eerst de lichte kleur met een kleine extra verplaatsing
            print("licht_donker ")
            print(self.donker_licht_verdeling[['wenselijk_aantal', 'aantal', 'delta_aantal']])
            if max(-min_delta_kleurgroepen, max_delta_kleurgroepen, -min_delta_donker_licht,
                   max_delta_donker_licht) <= self.afkap_max_min_delta_aantal:
                break
            # Maken blotsjabloon
            blot = blotter.blot(blot_diameter_x, blot_diameter_y)
            # Strepen.

            # Eigenlijke vlek
            if max_delta_kleurgroepen > 0:
                self.plaats_blot_op_canvas(blot=blot,
                                           blot_diameter_x=blot_diameter_x,
                                           blot_diameter_y=blot_diameter_y,
                                           kleurcode=max_delta_kleurgroep,
                                           x_verschuiving=x_verschuiving,
                                           y_verschuiving=y_verschuiving)
            else:  # Er word geen kleurvlek geplaatst
                print('############################# geen vlek #####################################')

            # Lichte streep eerst als het de grootste (positieve) delta heeft
            if licht_delta > 0:
                licht_verplaatsing_x, licht_verplaatsing_y = [
                    x * min(LICHT_DONKER_MAXIMALE_VERSCHUIVING,
                            max(int(licht_delta * LICHT_DONKER_VERSCHUIVINGSFACTOR),
                                LICHT_DONKER_MINIMALE_VERSCHUIVING)) for
                    x
                    in richting]
                self.plaats_ring_blot_op_canvas(blot=blot,
                                                blot_diameter_x=blot_diameter_x,
                                                blot_diameter_y=blot_diameter_y,
                                                kleurcode=-1,
                                                x_verschuiving=x_verschuiving,
                                                y_verschuiving=y_verschuiving,
                                                licht_verplaatsing_x=licht_verplaatsing_x,
                                                licht_verplaatsing_y=licht_verplaatsing_y)
            # Donkere streep op canvas
            if donker_delta > 0:
                donker_verplaatsing_x, donker_verplaatsing_y = [
                    x * min(LICHT_DONKER_MAXIMALE_VERSCHUIVING,
                            -1 * max(int(donker_delta * LICHT_DONKER_VERSCHUIVINGSFACTOR),
                                     LICHT_DONKER_MINIMALE_VERSCHUIVING)) for
                    x in richting]
                self.plaats_ring_blot_op_canvas(blot=blot,
                                                blot_diameter_x=blot_diameter_x,
                                                blot_diameter_y=blot_diameter_y,
                                                kleurcode=-2,
                                                x_verschuiving=x_verschuiving,
                                                y_verschuiving=y_verschuiving,
                                                licht_verplaatsing_x=donker_verplaatsing_x,
                                                licht_verplaatsing_y=donker_verplaatsing_y)

        # In gereedheid brengen voor locale topo
        # Boekhouding op orde
        self.doe_boekhouding_hoofdkleuren()
        self.kleurgroepen_detail = self.kleurgroepen_globaal.drop(
            columns=['verhouding', 'wenselijk_aantal', 'delta_aantal'])
        self.kleurgroepen_detail = self.kleur_verhoudingen. \
            join(self.kleurgroepen_detail.set_index('verdeling_in_M'), on='verdeling_in_M'). \
            sort_values(by='verdeling_in_N')

        # Per globaal kleurnumme het hoogste lokale kleurnummer vinden
        minKleurAantallen = self.kleurgroepen_detail.groupby(['verdeling_in_M'])['wenselijk_aantal'] \
            .min() \
            .to_list()
        # We zetten nu de regels zonder minKleurAantallen op 0
        self.kleurgroepen_detail.loc[
            ~self.kleurgroepen_detail['wenselijk_aantal'].isin(minKleurAantallen), 'aantal'] = 0
        self.kleurgroepen_detail['wenselijk_aantal'] = self.kleurgroepen_detail['verhouding'] * self.aantal_pixels * (
                1 - self.totaal_percentage_donker_licht)
        self.kleurgroepen_detail['delta_aantal'] = self.kleurgroepen_detail['wenselijk_aantal'] - \
                                                   self.kleurgroepen_detail['aantal']
        # We moeten nu zorgen dat eventuele pixels die licht en donker te veel of te weinig genomen hebben geen probleem op gaan leveren
        # in het bepalen van de detail verdeling. We verdelen naar verhouding
        donker_licht_delta = self.donker_licht_verdeling.delta_aantal.sum()
        self.kleurgroepen_detail[
            'wenselijk_aantal'] = self.kleurgroepen_detail.wenselijk_aantal + self.kleurgroepen_detail.verhouding * donker_licht_delta
        # Nu gaan we licht en donker er in faken
        self.donker_licht_verdeling['verdeling_in_N'] = [-2, -1]
        self.donker_licht_verdeling['verdeling_in_M'] = [-2, -1]
        # We zetten het gewensta aantal op aantal omdat de rol van licht en donker eigenlijk uitgespeeld is
        self.donker_licht_verdeling['wenselijk_aantal'] = self.donker_licht_verdeling['aantal']
        self.donker_licht_verdeling['delta_aantal'] = [0.0, 0.0]
        donker_licht_verdeling = self.donker_licht_verdeling.drop(
            columns=['delta_percentage'])

        self.kleurgroepen_detail = donker_licht_verdeling.append(self.kleurgroepen_detail, ignore_index=True, )
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
                             grenswaarde,
                             afplatting):
        blotter = PerlinBlotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, grenswaarde)
        self.naam = self.naam + "_det_a" + str("{:02d}".format(aantal)) + "_bg" + str(
            "{:02d}".format(blot_grootte_factor)) + "af" + str(afplatting) + blotter.naam + "v" + str("{:02d}".format(self.versie))

        # Eerst van hoofdkl
        for i in range(aantal):
            # Boekhouding op orde
            for j in self.kleurgroepen_detail['verdeling_in_N']:
                self.canvas_detail[0, j] = j
            self.canvas_globaal[0, -1] = -1
            self.canvas_globaal[0, -2] = -2
            kleurnummer, aantallen_per_detailkleur = np.unique(self.canvas_detail,
                                                               return_counts=True)
            self.kleurgroepen_detail['aantal'] = aantallen_per_detailkleur
            self.kleurgroepen_detail['delta_aantal'] = self.kleurgroepen_detail['wenselijk_aantal'] - \
                                                       self.kleurgroepen_detail['aantal']

            max_deltas = self.kleurgroepen_detail.groupby(['verdeling_in_M'])['delta_aantal'].max()
            # transities per groep bepalen
            dummy = self.kleurgroepen_detail[self.kleurgroepen_detail['delta_aantal']. \
                isin(max_deltas)]. \
                groupby(['verdeling_in_M'])[['verdeling_in_M', 'verdeling_in_N']]. \
                max(). \
                rename(columns={'verdeling_in_N': 'doel'}). \
                join(self.kleurgroepen_detail.set_index('verdeling_in_M'), rsuffix='_r')

            doel_kleurnummers = dict(zip(dummy.verdeling_in_N, dummy.doel))
            # We maken een blot met oppervlakte gelijk aan delta wenselijk aantal en werkelijk aantal
            # eerst vierkant later kan dat mooier gemaakt
            # blotDiameter = int(max(sqrt(max_deltas.max()) * blot_grootte_factor, (sqrt(aantal) * 10) // (i + 1)))
            blotDiameter_t = int(sqrt(max_deltas.max() + aantal - i) * blot_grootte_factor)
            blotDiameter_t = random.randint(blotDiameter_t // 2, blotDiameter_t)
            blot_diameter_x = blotDiameter_t
            blot_diameter_y = int(blotDiameter_t * afplatting)

            blot = blotter.blot(blot_diameter_x, blot_diameter_y)
            # plaatsen van de blot op canvas
            # we werken vanaf linksboven
            x_verschuiving = np.random.randint(blot_diameter_x + self.w) - blot_diameter_x
            xEind = min(x_verschuiving + blot_diameter_x, self.w)
            xStart = max(0, x_verschuiving)
            y_verschuiving = np.random.randint(blot_diameter_y + self.h) - blot_diameter_y
            yEind = min(y_verschuiving + blot_diameter_y, self.h)
            yStart = max(0, y_verschuiving)

            print('i', i)
            print(self.kleurgroepen_detail[['verdeling_in_N', 'wenselijk_aantal', 'aantal', 'delta_aantal']])
            print(doel_kleurnummers)
            print('x ', xStart, '-', xEind, 'displacementX', x_verschuiving)
            print('y ', yStart, '-', yEind, 'displacementY', y_verschuiving)
            print("blotdiameter", blot_diameter_x, " _ ", blot_diameter_y)
            print("")

            minDelta = self.kleurgroepen_detail['delta_aantal'].min()
            maxkDelta = self.kleurgroepen_detail['delta_aantal'].max()
            if max(-minDelta, maxkDelta) <= self.afkap_max_min_delta_aantal * AFKAP_MAX_MIN_DELTA_AANTAL_FACTOR_DETAIL:
                break

            for x in range(xStart, xEind):
                for y in range(yStart, yEind):
                    if blot[x - x_verschuiving, y - y_verschuiving] == 1:
                        self.canvas_detail[x, y] = doel_kleurnummers.get(self.canvas_detail[x, y])

        i = 1
        self.dict_kleurnummer_kleur = dict(zip(self.kleurgroepen_detail.verdeling_in_N, zip(self.kleurgroepen_detail.R,
                                                                                            self.kleurgroepen_detail.G,
                                                                                            self.kleurgroepen_detail.B)))

    def afmetingen(self):
        return "_W" + str(self.w) + \
               "_H" + str(self.h)

    def plaats_blot_op_canvas(self, blot, blot_diameter_x, blot_diameter_y, kleurcode, x_verschuiving, y_verschuiving):
        xEind = min(x_verschuiving + blot_diameter_x, self.w)
        xStart = max(0, x_verschuiving)
        yEind = min(y_verschuiving + blot_diameter_y, self.h)
        yStart = max(0, y_verschuiving)

        print("")
        print('kleur', kleurcode)
        print('blotDiam', blot_diameter_x, " - _ ", blot_diameter_y)
        # print('x ', xStart, '-', xEind, 'displacementX', x_verschuiving)
        # print('y ', yStart, '-', yEind, 'displacementY', y_verschuiving)
        for x in range(xStart, xEind):
            for y in range(yStart, yEind):
                if blot[x - x_verschuiving, y - y_verschuiving] == 1:
                    self.canvas_globaal[x, y] = kleurcode

    def plaats_ring_blot_op_canvas(self, blot, blot_diameter_x, blot_diameter_y, kleurcode, x_verschuiving, y_verschuiving,
                                   licht_verplaatsing_x, licht_verplaatsing_y):
        xEind = min(x_verschuiving + blot_diameter_x + licht_verplaatsing_x, self.w)
        xStart = max(0, x_verschuiving + licht_verplaatsing_x)
        yEind = min(y_verschuiving + blot_diameter_y + licht_verplaatsing_y, self.h)
        yStart = max(0, y_verschuiving + licht_verplaatsing_y)

        print("")
        print("ring")
        print('kleur', kleurcode)
        print('blotDiam', blot_diameter_x, " - _ ", blot_diameter_y)
        # print('x ', xStart, '-', xEind, 'displacementX', x_verschuiving)
        # print('y ', yStart, '-', yEind, 'displacementY', y_verschuiving)
        print('licht verpl ', str(licht_verplaatsing_x), ', ', str(licht_verplaatsing_y))
        max_index_x = blot_diameter_x - 1
        max_index_y = blot_diameter_y - 1
        for x in range(xStart, xEind):
            for y in range(yStart, yEind):
                # we maken gebruik van het feit dat bij de randen toch geen inkt zit
                # met min en max voorkomen we zo complexe if the else constructies
                if blot[min(x - x_verschuiving, max_index_x),
                        min(y - y_verschuiving, max_index_y)] == 0:  # Alleen als er geen vlek overheen hoort
                    if blot[
                        x - x_verschuiving - licht_verplaatsing_x, y - y_verschuiving - licht_verplaatsing_y]:  # En we wel een randje zien
                        self.canvas_globaal[x, y] = kleurcode

    def doe_boekhouding_hoofdkleuren(self):
        for j in self.kleurgroepen_globaal['verdeling_in_M']:
            self.canvas_globaal[0, j] = j
        self.canvas_globaal[0, -1] = -1
        self.canvas_globaal[0, -2] = -2
        kleurnummer, aantallen_per_hoofdkleur = np.unique(self.canvas_globaal,
                                                          return_counts=True)
        self.kleurgroepen_globaal['aantal'] = aantallen_per_hoofdkleur[2:]
        self.kleurgroepen_globaal['delta_aantal'] = self.kleurgroepen_globaal['wenselijk_aantal'] - \
                                                    self.kleurgroepen_globaal['aantal']
        min_delta_kleurgroepen = self.kleurgroepen_globaal['delta_aantal'].min()
        max_delta_kleurgroepen = self.kleurgroepen_globaal['delta_aantal'].max()
        max_delta_kleurgroep = self.kleurgroepen_globaal[self.kleurgroepen_globaal['delta_aantal'] ==
                                                         max_delta_kleurgroepen]['verdeling_in_M'].max()
        self.donker_licht_verdeling['aantal'] = aantallen_per_hoofdkleur[0:2]
        self.donker_licht_verdeling['delta_aantal'] = self.donker_licht_verdeling['wenselijk_aantal'] - \
                                                      self.donker_licht_verdeling['aantal']
        self.donker_licht_verdeling['delta_percentage'] = self.donker_licht_verdeling[
                                                              'delta_aantal'] / self.aantal_pixels
        min_delta_donker_licht = self.donker_licht_verdeling.delta_aantal.min()
        max_delta_donker_licht = self.donker_licht_verdeling.delta_aantal.max()
        return min_delta_kleurgroepen, max_delta_kleurgroepen, max_delta_kleurgroep, min_delta_donker_licht, max_delta_donker_licht


def splits_hoogste_en_laagste_lichtheid_af(df_kleuren, grens_factor):
    kleuren_sorted = df_kleuren.copy()
    kleuren_sorted['lichtheid'] = kleuren_sorted.R + kleuren_sorted.G + kleuren_sorted.B
    kleuren_sorted = kleuren_sorted.sort_values(by='lichtheid')
    totaal_aantal = kleuren_sorted.aantal.sum()
    grens = totaal_aantal * grens_factor
    kleuren_sorted = kleuren_sorted[kleuren_sorted.aantal > grens]
    kleuren_antwoord = kleuren_sorted.iloc[1:-1]
    kleuren_sorted = kleuren_sorted.iloc[[0, -1]]
    licht_donker_antwoord = kleuren_sorted.loc[:, ['R', 'G', 'B']]
    # kleuren_antwoord = pd.merge(df_kleuren, kleuren_sorted.verdeling_in_N, how='outer', left_on='verdeling_in_N',
    #                             right_on='verdeling_in_N', indicator=True)
    # kleuren_antwoord = kleuren_antwoord.loc[kleuren_antwoord['_merge'] == 'left_only']
    percentage_donker_licht = tuple((kleuren_sorted.aantal.tolist() / totaal_aantal) * 100)
    # kleuren_antwoord = kleuren_antwoord.drop(['_merge'], axis=1)
    return kleuren_antwoord, licht_donker_antwoord, percentage_donker_licht
