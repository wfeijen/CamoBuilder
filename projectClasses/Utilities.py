import numpy as np
from sklearn.neighbors import KDTree
import pickle

# Vertaalt waarden snel door gebruik te maken van een dictionary
def replace_with_dict(ar, dic):
    # Extract out keys and values
    k = np.array(list(dic.keys()))
    v = np.array(list(dic.values()))

    # Get argsort indices
    sidx = k.argsort()

    # Drop the magic bomb with searchsorted to get the corresponding
    # places for a in keys (using sorter since a is not necessarily sorted).
    # Then trace it back to original order with indexing into sidx
    # Finally index into values for desired output.
    return v[sidx[np.searchsorted(k,ar,sorter=sidx)]]

# Vertaalt RGB kleurwaarden met behulp van twee schema's.
# Let op dat van het schema moet zijn waar je uiteindelijk heen print en naar het originele schema moet zijn
def corrigeer_kleuren(van_schema_filenaam, naar_schema_filenaam, kleurinfo_in, alfa = 0.001, K = 10):
    kleuren_in = kleurinfo_in[['R', 'G', 'B']].to_numpy()
    aantal_kleuren_in = len(kleurinfo_in.index)
    with open(van_schema_filenaam, 'rb') as file:
        van_schema = pickle.load(file)
    with open(naar_schema_filenaam, 'rb') as file:
        naar_schema = pickle.load(file)
    aantal_kleuren_in_schema = len(van_schema)    
    if len(naar_schema) !=aantal_kleuren_in_schema:
        raise Exception('kleurenschemas zijn niet even lang')
    van_schema = np.array(van_schema).reshape(aantal_kleuren_in_schema, 3)
    naar_schema = np.array(naar_schema).reshape(aantal_kleuren_in_schema, 3)
    tree = KDTree(van_schema)
    afstanden, indices = tree.query(kleuren_in , K)
    relevante_rgb = naar_schema[indices]
    afstanden_per_rgb = np.repeat(afstanden.reshape(aantal_kleuren_in ,K , 1), 
                                  3, axis=2) + alfa
    kleurwaarde_div_afstand = (relevante_rgb / afstanden_per_rgb)
    som_kleurwaarde_div_afstand = np.sum(kleurwaarde_div_afstand, axis = 1)
    div_afstand = (1 / afstanden_per_rgb)
    som_div_afstand = np.sum(div_afstand, axis = 1)
    kleurwaarden_gecorrigeerd = (som_kleurwaarde_div_afstand / som_div_afstand).astype(int)
    kleurInfo_gecorrigeerd = kleurinfo_in.copy(deep=True)    
    kleurInfo_gecorrigeerd[['R', 'G', 'B']] = kleurwaarden_gecorrigeerd
    return kleurwaarden_gecorrigeerd