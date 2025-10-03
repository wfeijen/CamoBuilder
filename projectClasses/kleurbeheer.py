import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
import pickle
from math import sqrt, ceil
from PIL import Image, ImageDraw, ImageFont


#%%

def maak_contrasterende_tekstkleur(color):
    r, g, b = color
    brightness = sqrt(0.299 * r**2 + 0.587 * g**2 + 0.114 * b**2)
    text_color = "#000000" if brightness > 128 else "#FFFFFF"
    return text_color

def maak_color_card_op_basis_van_lijst_met_kleuren(kleuren_in, square_size, font_size=50, tekst=False):
    kleuren = kleuren_in.copy(deep=True)
    kleuren = kleuren.loc[:, ['R', 'G', 'B']].astype(int)
    kleuren = kleuren.drop_duplicates()
    N = len(kleuren)
    rootN = int(ceil(sqrt(N)))
    count = range(rootN)

    kleuren = [tuple(r) for r in kleuren.to_numpy()]
    np.random.shuffle(kleuren)

    image = Image.new("RGB", (rootN * square_size, rootN * square_size))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("/usr/share/fonts/truetype/tlwg/TlwgTypewriter-Bold.ttf", size=font_size)
    color_index = 0
    for x in count:
        for y in count:
            if color_index == N:
                color_index = 0
                np.random.shuffle(kleuren)
            color = kleuren[color_index]
            decimal_code = "\n".join([str(c) for c in color])
            decimal_code = f"{decimal_code}"
            x1 = x * square_size
            y1 = y * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            draw.rectangle([(x1, y1), (x2, y2)], fill=color)
            color_index = color_index + 1
            if tekst:
                draw.text((x1 + 80, y1 + 50), decimal_code, fill=maak_contrasterende_tekstkleur(color), font=font, align="center")
    return image

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
    return kleurwaarden_gecorrigeerd

def pas_kleuren_aan_met_parameters(kleuren_in,
                                   contrast,
                                   saturation,
                                   belichting,
                                   gewicht_extremen,
                                   macht_kleur):
    kleureninfo = f'contrast,{str(contrast)},saturation,{str(saturation)},belichting,{str(belichting)},gewicht_extremen,{str(gewicht_extremen)},macht_kleur,{str(macht_kleur)}'
    kleuren = kleuren_in.copy(deep=True)
        # Saturatie
    totaalAantal = kleuren['aantal'].sum()
    kleuren['R'] = kleuren['R'] * saturation + kleuren['grijswaarde'] * (1 - saturation)
    kleuren['G'] = kleuren['G'] * saturation + kleuren['grijswaarde'] * (1 - saturation)
    kleuren['B'] = kleuren['B'] * saturation + kleuren['grijswaarde'] * (1 - saturation)
    # Contrast
    Rmean = (kleuren['R'] * kleuren['aantal']).sum() / totaalAantal
    Gmean = (kleuren['G'] * kleuren['aantal']).sum() / totaalAantal
    Bmean = (kleuren['B'] * kleuren['aantal']).sum() / totaalAantal
    kleuren.loc[:, ['R', 'G', 'B']] -= [Rmean, Gmean, Bmean]
    kleuren.loc[:, ['R', 'G', 'B']] = (kleuren.loc[:, ['R', 'G', 'B']] * contrast)
    kleuren.loc[:, ['R', 'G', 'B']] += [Rmean, Gmean, Bmean]
    # Belichting
    kleuren.loc[:, ['R', 'G', 'B']] = (kleuren.loc[:, ['R', 'G', 'B']] * belichting)

    # Aantallen aanpassen om minder voorkomende kleuren meer te maskeren
    kleuren['aantal'] = kleuren['aantal'].pow(macht_kleur).astype(int)
    # Aantallen aanpassen op basis van extremiteit
    kleuren.loc[:, ['R', 'G', 'B']] -= [128, 128, 128]
    kleuren['aantal_mutatie'] = ((kleuren.loc[:, ['R', 'G', 'B']].abs().sum(axis = 1) * gewicht_extremen)).astype(int)
    kleuren['aantal'] = kleuren['aantal_mutatie'] + kleuren['aantal']
    kleuren.loc[:, ['R', 'G', 'B']] += [128, 128, 128]
    # terug naar RGB-ruimte
    kleuren.loc[:, ['R', 'G', 'B']] = kleuren.loc[:, ['R', 'G', 'B']].clip(lower=0, upper=255).round().astype(pd.Int64Dtype())

    return kleuren, kleureninfo
