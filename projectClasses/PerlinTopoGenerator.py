import random
from math import sqrt
import numpy as np
import pandas as pd
from projectClasses.Blotter import Blotter
from projectClasses.Utilities import replace_with_dict
import re


class PerlinTopoGeneratator:
    def __init__(self,
                 breedte,
                 hoogte,
                 kleur_verhoudingen,
                 versie,
                 naam_basis,
                 contrast,
                 belichting,
                 start_volgorde,
                 kleur_manipulatie = "licht_donker_licht"):# licht_donker_licht, oplopend
        self.h = hoogte
        self.w = breedte
        totaalAantal = kleur_verhoudingen['aantal'].sum()
        Rmean = (kleur_verhoudingen['R'] * kleur_verhoudingen['aantal']).sum() / totaalAantal
        Gmean = (kleur_verhoudingen['G'] * kleur_verhoudingen['aantal']).sum() / totaalAantal
        Bmean = (kleur_verhoudingen['B'] * kleur_verhoudingen['aantal']).sum() / totaalAantal
        kleur_verhoudingen.loc[:, ['R', 'G', 'B']] -= [Rmean, Gmean, Bmean]
        kleur_verhoudingen.loc[:, ['R', 'G', 'B']] = (kleur_verhoudingen.loc[:, ['R', 'G', 'B']] * contrast)
        kleur_verhoudingen.loc[:, ['R', 'G', 'B']] += [Rmean, Gmean, Bmean]
        kleur_verhoudingen.loc[:, ['R', 'G', 'B']] = (kleur_verhoudingen.loc[:, ['R', 'G', 'B']] * belichting)
        kleur_verhoudingen.loc[:, ['R', 'G', 'B']].clip(lower=0, upper=255).astype(int)
        if start_volgorde=="hoofdKleur":
            kleur_verhoudingen = kleur_verhoudingen.rename(columns={'hoofdKleur': 'verdeling_in_M', 'grijsGroep': 'verdeling_in_N'})
        elif start_volgorde== "grijsGroep":
            kleur_verhoudingen = kleur_verhoudingen.rename(columns={'hoofdKleur': 'verdeling_in_N', 'grijsGroep': 'verdeling_in_M'})
        else:
            raise ValueError(f'start_volgorde mag "hoofdKleur" of "" zijn. Geen: {start_volgorde}')
        kleur_verhoudingen['verdeling_in_N'] = kleur_verhoudingen.index

        median_grijswaarde_per_M = kleur_verhoudingen.groupby(['verdeling_in_M'])[['grijswaarde']].mean().sort_values('grijswaarde').reset_index()
        if kleur_manipulatie == "licht_donker_licht":
            median_grijswaarde_per_M['volgorde'] = median_grijswaarde_per_M.index
            median_grijswaarde_per_M.loc[median_grijswaarde_per_M.index % 2 == 0, 'volgorde'] = -median_grijswaarde_per_M.loc[median_grijswaarde_per_M.index % 2 == 0].index
            median_grijswaarde_per_M = median_grijswaarde_per_M.sort_values('volgorde')

        median_grijswaarde_per_M['verdeling_in_M_nieuw'] = range(len(median_grijswaarde_per_M.index))
        kleur_verhoudingen = median_grijswaarde_per_M.merge(kleur_verhoudingen, how='inner', on='verdeling_in_M', suffixes=('_M', ''))
        kleur_verhoudingen['verdeling_in_M'] = kleur_verhoudingen['verdeling_in_M_nieuw']
        kleur_verhoudingen.drop(columns = ['verdeling_in_M_nieuw', 'index'])


        self.kleur_verhoudingen = kleur_verhoudingen.rename(columns={'aantal': 'wenselijk_aantal'})

        aantal_kleurmetingen = self.kleur_verhoudingen['wenselijk_aantal'].sum()
        self.kleur_verhoudingen['verhouding'] = self.kleur_verhoudingen['wenselijk_aantal'] / aantal_kleurmetingen
        self.versie = versie

        # We gaan nu eerst de tellingen per kleurgroep op orde maken en canvas uitvullen met het meest voorkomende kleurgroep nummer
        self.kleurgroepen_globaal = self.kleur_verhoudingen.groupby(['verdeling_in_M'])[
            'verhouding'].sum().reset_index()
        aantal_pixels = self.w * self.h
        self.kleurgroepen_globaal['wenselijk_aantal'] = (
                    self.kleurgroepen_globaal['verhouding'] * aantal_pixels).astype(int)
        self.kleurgroepen_globaal['aantal'] = np. \
            where(self.kleurgroepen_globaal['verhouding'] == self.kleurgroepen_globaal['verhouding'].min(),
                  aantal_pixels, 0)

        # Afscheiden licht en donkere kleuren
        min_kleur_nummer = int(
            self.kleurgroepen_globaal.loc[self.kleurgroepen_globaal['wenselijk_aantal'].idxmin()]['verdeling_in_M'])

        self.canvas_globaal = np.full((self.w, self.h), min_kleur_nummer)
        self.info = f'{naam_basis},breedte,{str(breedte)},hoogte,{str(hoogte)},contrast,{str(contrast)},belichting,{str(belichting)},start_volgorde,{start_volgorde},kleurmanipulatie,{str(kleur_manipulatie)}'
        self.verdeling_in_N_naar_kleur = dict(zip(self.kleur_verhoudingen.verdeling_in_N,
                                                  zip(self.kleur_verhoudingen.R.astype(int),
                                                      self.kleur_verhoudingen.G.astype(int),
                                                      self.kleur_verhoudingen.B.astype(int))))


    def afmetingen(self):
        return "_W" + str(self.w) + \
            "_H" + str(self.h)


    def globale_boekhouding_op_orde(self):
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
        return max_delta, max_delta_kleurgroep

    def generate_globale_topo(self,
                              Id,
                              noise_type,
                              octaves,
                              persistence,
                              lacunarity,
                              scaleX,
                              scaleY):
        blotter = Blotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, 0, noise_type)
        self.info = self.info + ",globaal" + blotter.info
        print(self.info)
        # bepalen grenzen
        blot = blotter.blotCanvas(blot_sizeX=self.w, blot_sizeY=self.h)
        self.versie += 1
        hist = np.histogram(blot, bins=1000)
        hist = pd.DataFrame({'aantal': hist[0], 'bin_grens': hist[1][0:1000]})
        hist['aantal_cumulatief'] = np.cumsum(hist['aantal'])
        self.kleurgroepen_globaal['wenselijk_aantal_cum'] = np.cumsum(self.kleurgroepen_globaal['wenselijk_aantal'])
        grenswaarden = [hist.iloc[(hist['aantal_cumulatief'] - x).abs().argsort()[:1]]['bin_grens'].iloc[0] for x in
                        self.kleurgroepen_globaal['wenselijk_aantal_cum']]
        aantal_te_testen_grenswaarden = len(grenswaarden) - 1
        # plaatsen van de blot op canvas.
        for x in range(0, self.w):
            for y in range(0, self.h):
                self.canvas_globaal[x, y] = aantal_te_testen_grenswaarden  # Default de laatste
                for i in range(aantal_te_testen_grenswaarden):
                    if blot[x, y] < grenswaarden[i]:
                        self.canvas_globaal[x, y] = i
                        break

        max_delta, max_delta_kleurgroep = self.globale_boekhouding_op_orde()
        aantal_puntjes = max_delta
        print(
            f"{Id} i:{i: 4d} md{max_delta: 7d} ap{aantal_puntjes: 7d} " +
            re.sub(r"(\n)?([0-9]{1,2}) +", r"  \2:", ''.join(str(self.kleurgroepen_globaal['delta_aantal']))).replace(
                "\nName: delta_aantal, dtype: int64", "   "))

    def bereid_lokale_topos_voor(self):
        # In gereedheid brengen voor locale topo
        aantal_per_M = self.kleurgroepen_globaal[['verdeling_in_M', 'aantal']]
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
        min_kleur_nummers_lokaal = self.kleurgroepen_detail[self.kleurgroepen_detail['aantal'] != 0][
            'verdeling_in_M'].min()
        self.kleurgroepen_detail.loc[
            ~self.kleurgroepen_detail['wenselijk_aantal'].isin(minKleurAantallen), 'aantal'] = 0
        self.kleurgroepen_detail['wenselijk_aantal'] = (
                    self.kleurgroepen_detail['verhouding'] * self.w * self.h).astype(int)
        self.kleurgroepen_detail['delta_aantal'] = self.kleurgroepen_detail['wenselijk_aantal'] - \
                                                   self.kleurgroepen_detail['aantal']
        # Nu invullen canvaslocaal met echte kleurnummers
        temp_kleurgroepen = self.kleurgroepen_detail[self.kleurgroepen_detail['aantal'] > 0]
        vertaalTabel = dict(zip(temp_kleurgroepen.verdeling_in_M, temp_kleurgroepen.verdeling_in_N))
        self.canvas_detail = replace_with_dict(self.canvas_globaal, vertaalTabel)
        i = 1

    def boekhouding_locale_topo(self):
        for j in self.kleurgroepen_detail['verdeling_in_N']:
            self.canvas_detail[0, j] = j
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
        return doel_kleurnummers, max_deltas.max()

    def generate_locale_topo(self,
                             Id,
                             noise_type,
                             octaves,
                             persistence,
                             lacunarity,
                             scaleX,
                             scaleY,
                             verspringende_detailtekening = True):
        blotter = Blotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, 0, noise_type)
        self.info = self.info + ",lokaal" + blotter.info
        self.kleurgroepen_detail['wenselijk_aantal_cum'] = self.kleurgroepen_detail.groupby(['verdeling_in_M'])['wenselijk_aantal'].cumsum()
        for globale_kleur in range(len(self.kleurgroepen_globaal.index)):
            blotter = Blotter(persistence, lacunarity, octaves, scaleX, scaleY, self.versie, 0, noise_type)
            self.versie += 1

            deze_kleurgroepen_detail = self.kleurgroepen_detail.loc[self.kleurgroepen_detail['verdeling_in_M'] == globale_kleur].reset_index(drop=True)

            # bepalen grenzen
            blot = blotter.blotCanvas(blot_sizeX=self.w, blot_sizeY=self.h)
            relevant = blot[globale_kleur == self.canvas_globaal]
            hist = np.histogram(relevant, bins=1000)
            hist = pd.DataFrame({'aantal': hist[0], 'bin_grens': hist[1][0:1000]})
            hist['aantal_cumulatief'] = np.cumsum(hist['aantal'])
            grenswaarden = [hist.iloc[(hist['aantal_cumulatief'] - x).abs().argsort()[:1]]['bin_grens'].iloc[0] for x in
                            deze_kleurgroepen_detail['wenselijk_aantal_cum']]
            aantal_te_testen_grenswaarden = len(grenswaarden) - 1
        # plaatsen van de blot op canvas.
            default_waarde = deze_kleurgroepen_detail.iloc[aantal_te_testen_grenswaarden]['verdeling_in_N']
            for x in range(0, self.w):
                for y in range(0, self.h):
                    if self.canvas_globaal[x, y] == globale_kleur:
                        self.canvas_detail[x, y] = default_waarde  # Default de laatste
                        for i in range(aantal_te_testen_grenswaarden):
                            if blot[x, y] < grenswaarden[i]:
                                self.canvas_detail[x, y] = deze_kleurgroepen_detail.iloc[i]['verdeling_in_N']
                                break

        doel_kleurnummers, max_delta = self.boekhouding_locale_topo()
        aantal_puntjes = max_delta
        print(
            f"{Id} i:{i: 4d} md{max_delta: 7d} ap{aantal_puntjes: 7d} " +
            re.sub(r"(\n)?([0-9]{1,2}) +", r"  \2:",
                   ''.join(str(self.kleurgroepen_detail['delta_aantal']))).replace(
                "\nName: delta_aantal, dtype: int64", "   "))


