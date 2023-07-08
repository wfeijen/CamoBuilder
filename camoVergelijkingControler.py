import camoVergelijkingsTestScherm as cvs
from projectClasses.fileHandling import give_list_of_images

import pandas as pd
import numpy as np
#/media/willem/KleindSSD/machineLearningPictures/camoBuilder/teVergelijkenCamos
base_dir = '/home/willem/Pictures/Camouflage/camoBuilder/'
schenes_sub_dir = 'scenesVoorTest'
camos_sub_dir = 'teVergelijkenCamos'
boekhouding_file = base_dir + '/camovergelijking_resultaten.csv'

scenes_lijst = give_list_of_images(baseDir=base_dir, subdirName=schenes_sub_dir)
camos_lijst = give_list_of_images(baseDir=base_dir, subdirName=camos_sub_dir)

# Nu maken we een lijst van de combinaties
scenes_df = pd.DataFrame(scenes_lijst, columns=['scenes'])
camos1_df = pd.DataFrame({'camo1': camos_lijst, 'key': 1})
camos2_df = pd.DataFrame({'camo2': camos_lijst, 'key': 1})
combinaties = scenes_df.assign(key=1).merge(camos1_df).merge(camos2_df).drop('key', 1)
# We hebben nu de actieve combinaties. Die vullen we aan met de benodigde colommen
# combinaties['tijd1'] = np.NaN
# combinaties['tijd2'] = np.NaN
combinaties['actief'] = True
# We lezen eerdere resultaten in en combineren die met de actieve combinaties
eerdere_resultaten = pd.read_csv(boekhouding_file, index_col=False)
totale_set = pd.merge(eerdere_resultaten, combinaties, how='outer', left_on=['scenes', 'camo1', 'camo2'],
                      right_on=['scenes', 'camo1', 'camo2'], indicator=True)
# De volgorde van de kolommen wordt verstoord dus die zetten we opnieuw
totale_set = totale_set.loc[:, ['scenes', 'camo1', 'camo2', 'tijd1', 'tijd2', 'actief', '_merge']]
# combinaties met zelfde camo verwijderen
totale_set = totale_set.query("(camo1 != camo2) and (actief == True)")
print(len(totale_set.loc[(totale_set['tijd1'].notnull()) & (totale_set['_merge'] != 'left_only')]), " van ", len(totale_set.loc[(totale_set['_merge'] != 'left_only')]))

camoVergelijkingsTestScherm = cvs.CamoVergelijkingsTestScherm(scene_en_camos=totale_set,
                                                              boekhouding_file=boekhouding_file)

