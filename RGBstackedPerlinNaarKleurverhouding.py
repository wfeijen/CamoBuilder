import numpy as np
import pandas as pd
import os
import noise

KleurenPad = 'kleurParameters/graslandZomer3.jpg20211015 144736.csv'
root_dir = '/mnt/GroteSchijf/machineLearningPictures/camoBuilder/'
breedte = 1500
hoogte = 2000
versie = 4

# Eerst gaan we de globale structuur vullen.
#
# We gebruiken op dit moment alleen het kleurnummer. Later gaan we dat omzetten naar echte kleuren.
kleurInfo = pd.read_csv(KleurenPad, index_col=0)
kleurInfo.reset_index(inplace=True)

def id_met_meeste_achterstand_en_achterstand(tellingen_hoofdgroepen):
    tellingen_per_hoofdgroep["achterstand"] = tellingen_per_hoofdgroep.aantal - tellingen_hoofdgroepen.aantalGevuld
    #tellingen_hoofdgroepen tellingen_per_hoofdgroep.aantal
    achterstand = tellingen_per_hoofdgroep.achterstand.max()
    id = tellingen_per_hoofdgroep[tellingen_per_hoofdgroep.achterstand == achterstand].id.iat[0]
    return id, achterstand

tellingen_per_hoofdgroep = kleurInfo[["verdeling_in_M", "aantal"]].groupby(by=["verdeling_in_M"]).agg(['sum', 'idxmax']).aantal
tellingen_per_hoofdgroep.rename(columns= {'idxmax' : 'id' ,  'sum' : 'aantal'}, inplace = True)
tellingen_per_hoofdgroep["aantalGevuld"] = 0
totaal = tellingen_per_hoofdgroep["aantal"].sum()

aan_te_passen_groep, in_te_lopen = id_met_meeste_achterstand_en_achterstand(tellingen_per_hoofdgroep)

for i in range(3):
    world_vlak = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            world_vlak[x][y] = noise.pnoise2(x / scalex,
                                        y / scaley,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=size / scalex + 1,
                                        repeaty=size / scaley + 1,
                                        base=base + i)

# We vullen de basis voor het plaatje met de waarde voor de hoofdgroep
i = 1
