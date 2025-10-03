#%%
# 
import pandas as pd
import matplotlib.pyplot as plt


base_dir = '/home/willem/Pictures/Camouflage/camoBuilder'
boekhouding_file = base_dir + '/camovergelijking_resultaten.csv'

resultaten = pd.read_csv(boekhouding_file, index_col=False)
resultaten['tijd1'] = pd.to_datetime(resultaten['tijd1'])
resultaten['tijd2'] = pd.to_datetime(resultaten['tijd2'])


resultaten['winnaar'] = (resultaten['tijd2'] - resultaten['tijd1']).dt.total_seconds()

resultatenLong1 = resultaten.loc[:, ['scenes', 'camo1', 'winnaar']]
resultatenLong1['winnaar'] = -resultatenLong1['winnaar']
resultatenLong1.rename(columns = {'camo1' : 'camo'}, inplace = True)
resultatenLong2 = resultaten.loc[:, ['scenes', 'camo2', 'winnaar']] 
resultatenLong2.rename(columns = {'camo2' : 'camo'}, inplace = True)
resultatenLong = pd.concat([resultatenLong1, resultatenLong2])

def drieWaardenLogica(num):
    if num > 0: return 1
    if num < 0: return -1
    return 0

resultatenLong['winnaar_ongenuanceerd'] = resultatenLong.apply(lambda row: drieWaardenLogica(row['winnaar']), axis = 1)
resultatenLong['camo'] = resultatenLong['camo'].replace(to_replace='.*/', value='', regex = True)
resultatenLong['scenes'] = resultatenLong['scenes'].replace(to_replace='.*/', value='', regex = True)


rangorde = resultatenLong.groupby(['camo', 'scenes']).mean()
rangorde = rangorde.sort_values(by = 'winnaar_ongenuanceerd', ascending = 0)
pd.options.display.max_colwidth = 255

print("Sorting rows by Science:\n \n", rangorde)

#%%
# Heatmap maken
rangoredePerSchene = pd.crosstab(index=resultatenLong['scenes'],
                                 columns=resultatenLong['camo'],
                                 values=resultatenLong['winnaar_ongenuanceerd'],
                                 aggfunc='mean',
                                 dropna=True)  #resultatenLong.groupby(['camo', 'scenes']).mean()

# Calculate the mean of each column
column_means = rangoredePerSchene.mean()

# Sort the columns by their mean values
sorted_columns = column_means.sort_values().index

# Reorder the DataFrame columns based on the sorted order
rangoredePerSchene_sorted = rangoredePerSchene[sorted_columns]

print(rangoredePerSchene_sorted)
rangoredePerSchene_sorted.style.background_gradient(cmap ='viridis').set_properties(**{'font-size': '20px'})
plt.imshow(rangoredePerSchene_sorted, cmap ="RdYlBu")
plt.colorbar()
plt.xticks(range(len(rangoredePerSchene_sorted.columns)), rangoredePerSchene_sorted.columns)
plt.yticks(range(len(rangoredePerSchene_sorted)), rangoredePerSchene_sorted.index)
plt.xticks(rotation = 'vertical', fontsize=6)
# plt.tick_params(length= 200)
plt.show()
i = 1
# %%
