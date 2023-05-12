import random
from math import sqrt
import numpy as np
import pandas as pd
from projectClasses.TopoGenerator import TopoGenerator
from projectClasses.Utilities import replace_with_dict
import re

kleuren_naam = 'graslandZomer.jpg20230322 095001.csv'
root_dir = '/media/willem/KleindSSD/machineLearningPictures/camoBuilder/'
plaatjes_dir = root_dir + 'camoOutput/'
kleurenPad = './kleurParameters/' + kleuren_naam

kleurInfo = pd.read_csv(kleurenPad, index_col=0)


breedte = 200
hoogte = 200
aantal = 200
max_waarde_stopconditie = 400
octaves = 8
persistence = 0.4
lacunarity = 4
scaleX = 300
scaleY = 600
percentage_max_px = 0.60
versie = 1

kleurInfo = kleurInfo.rename(columns={'aantal': 'wenselijk_aantal'})
aantal_kleurmetingen = kleurInfo['wenselijk_aantal'].sum()
kleurInfo['verhouding'] = kleurInfo['wenselijk_aantal'] / aantal_kleurmetingen
kleurgroepen_globaal = kleurInfo.groupby(['verdeling_in_M'])[
    'verhouding'].sum().reset_index()

kleurgroepen_globaal['wenselijk_aantal'] = (kleurgroepen_globaal['verhouding'] * breedte * hoogte).astype(int)



blotter = TopoGenerator(persistence, lacunarity, octaves, scaleX, scaleY, versie, 0)
blot = blotter.genereer(blot_sizeX=breedte, blot_sizeY=hoogte)
hist = np.histogram(blot, bins = 1000)
hist = pd.DataFrame({'aantal': hist[0], 'bin_grens': hist[1][0:1000]})
hist['aantal_cumulatief'] = np.cumsum(hist['aantal'])
kleurgroepen_globaal['wenselijk_aantal_cum']=np.cumsum(kleurgroepen_globaal['wenselijk_aantal'])
grenswaarden = [hist.iloc[(hist['aantal_cumulatief']-x).abs().argsort()[:1]]['bin_grens'].iloc[0] for x in kleurgroepen_globaal['wenselijk_aantal_cum']]

print(grenswaarden)

