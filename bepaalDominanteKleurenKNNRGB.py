# Doel:
#   Bepalen dominante kleuren
#   bepalen welke kleuren daar onder vallen
#   bepalen schaduw licht verdeling
#   wegschrijven verdeling
#   wegschrijven foto in nieuwe kleuren

import numpy
from PIL import Image, ImageCms
from math import hypot
import datetime
from os import listdir
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import random
import os

# Parameters
dir = "bepaalDominanteKleuren"
aantalKleuren = 6


def bepaalWaardenEnPasAan(dir, name):
    # Inlezen file
    imOrig = Image.open(dir + "/" + name)
    if imOrig.mode != "RGB":
        imOrig = imOrig.convert("RGB")

    w, h = imOrig.size
    kleuren = imOrig.getcolors(w * h)
    npImageOrig = np.array(imOrig)
    npImageOrigReduced = npImageOrig.reshape(w * h, 3, order="C")
    pdImageOrig = pd.DataFrame(npImageOrigReduced, columns=['R', 'G', 'B'])
    kmeans = KMeans(n_clusters=aantalKleuren)
    kmeans.fit(pdImageOrig)
    y_kmeans = kmeans.predict(pdImageOrig)
    npCenters = kmeans.cluster_centers_.astype(int)

    pdImageTransform = pdImageOrig.copy(deep=True)
    pdImageTransform['groep'] = y_kmeans
    groepen = list(range(0, aantalKleuren))
    pdCenters = pd.DataFrame(npCenters, columns=['Rn', 'Gn', 'Bn'])
    pdCenters['groep'] = groepen
    pdImageTransform = pdImageTransform.join(pdCenters.set_index('groep'), on='groep')
    pdImageNieuw = pdImageTransform.copy(deep=True)
    pdImageNieuw = pdImageNieuw.iloc[:, 4:7]
    npImageNieuwReduced = pdImageNieuw.to_numpy()
    npImageNieuw = npImageNieuwReduced.reshape(h, w, 3, order="C")
    imageNieuw = Image.fromarray(numpy.uint8(npImageNieuw),  # ,numpy.uint8(npImageOrig)
                                 mode='RGB')
    now = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
    imageNieuw.save(dir + "/" + name + now + " vervangenVolgensMapC.JPG")

    # selectie = random.sample(list(range(0, pdImage['R'].size)), 1000)
    # R = pdImage.iloc[selectie, 0]
    # G = pdImage.iloc[selectie, 1]
    # B = pdImage.iloc[selectie, 2]
    # C = y_kmeans[selectie]
    #
    # fig, ax = plt.subplots()
    # ax.scatter(R, G, c=C, s=50, cmap='viridis')
    # ax.set_xlabel('R')
    # ax.set_ylabel('G')
    # ax.scatter(npCenters[:, 0], npCenters[:, 1], c='black', s=200, alpha=0.5)
    # plt.show()
    #
    # fig, ax = plt.subplots()
    # ax.scatter(R, B, c=C, s=50, cmap='viridis')
    # ax.set_xlabel('R')
    # ax.set_ylabel('B')
    # ax.scatter(npCenters[:, 0], npCenters[:, 2], c='black', s=200, alpha=0.5)
    # plt.show()
    #
    # fig, ax = plt.subplots()
    # ax.scatter(G, B, c=C, s=50, cmap='viridis')
    # ax.set_xlabel('G')
    # ax.set_ylabel('B')
    # ax.scatter(npCenters[:, 1], npCenters[:, 2], c='black', s=200, alpha=0.5)
    # plt.show()


files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
for name in files:
    if name[-4:] != ".JPG":
        print(name[-4:])
        bepaalWaardenEnPasAan(dir, name)
