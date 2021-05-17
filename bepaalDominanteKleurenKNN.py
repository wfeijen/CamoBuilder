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
from tensorboard.notebook import display

dir = "bepaalDominanteKleuren"
aantalKleuren = 6


def bepaalWaardenEnPasAan(dir, name):
    # Inlezen file
    im = Image.open(dir + "/" + name)
    if im.mode != "RGB":
        im = im.convert("RGB")

    srgb_profile = ImageCms.createProfile("sRGB")
    lab_profile = ImageCms.createProfile("LAB")

    rgb2lab_transform = ImageCms.buildTransformFromOpenProfiles(srgb_profile, lab_profile, "RGB", "LAB")
    lab_im = ImageCms.applyTransform(im, rgb2lab_transform)
    w, h = lab_im.size
    labColors = lab_im.getcolors(w * h)
    npImageOrig = np.array(lab_im)
    npImage = npImageOrig.reshape(w * h, 3, order="C")
    pdImage = pd.DataFrame(npImage, columns=['L', 'A', 'B'])
    # print(pdImage.head())
    # *************************************************
    # npOrig2 =  pdImage.to_numpy()
    # npOrig2 =  npOrig2.reshape(h, w, 3, order="C")
    # **************************************************
    kmeans = KMeans(n_clusters=aantalKleuren)
    kmeans.fit(pdImage)
    y_kmeans = kmeans.predict(pdImage)
    npCenters = kmeans.cluster_centers_.astype(int)

    selectie = random.sample(list(range(0, pdImage['L'].size)), 1000)
    L = pdImage.iloc[selectie, 0]
    A = pdImage.iloc[selectie, 1]
    B = pdImage.iloc[selectie, 2]
    C = y_kmeans[selectie]

    fig, ax = plt.subplots()
    ax.scatter(L, A, c=C, s=50, cmap='viridis')
    ax.set_xlabel('L')
    ax.set_ylabel('A')
    ax.scatter(npCenters[:, 0], npCenters[:, 1], c='black', s=200, alpha=0.5)
    plt.show()

    fig, ax = plt.subplots()
    ax.scatter(L, B, c=C, s=50, cmap='viridis')
    ax.set_xlabel('L')
    ax.set_ylabel('B')
    ax.scatter(npCenters[:, 0], npCenters[:, 2], c='black', s=200, alpha=0.5)
    plt.show()

    fig, ax = plt.subplots()
    ax.scatter(A, B, c=C, s=50, cmap='viridis')
    ax.set_xlabel('A')
    ax.set_ylabel('B')
    ax.scatter(npCenters[:, 1], npCenters[:, 2], c='black', s=200, alpha=0.5)
    plt.show()

    pdImage['groep'] = y_kmeans
    groepen = list(range(0, aantalKleuren))
    pdCenters = pd.DataFrame(npCenters, columns=['Ln', 'An', 'Bn'])
    pdCenters['groep'] = groepen
    pdImageTransform = pdImage.join(pdCenters.set_index('groep'), on='groep')
    pdImageNieuw = pdImageTransform.iloc[:, 4:7]
    # Exporteren van tellingen
    now = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
    export = pdImageNieuw.groupby(['Ln', 'An', 'Bn'])['Bn'].count()
    print(export)
    export.to_csv(name + now + '.csv')

    npImageNieuw = pdImageNieuw.to_numpy()
    npImageNieuw = npImageNieuw.reshape(h, w, 3, order="C")
    imageNiew = Image.fromarray(numpy.uint8(npImageNieuw),
                                mode='LAB')
    lab2rgb_transform = ImageCms.buildTransformFromOpenProfiles(lab_profile, srgb_profile, "LAB", "RGB")
    imgRGB = ImageCms.applyTransform(imageNiew, lab2rgb_transform)
    imgRGB.save(dir + "/" + name + now + " vervangenVolgensMapC.JPG")


files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
for name in files:
    if name[-4:] != ".JPG":
        print(name[-4:])
        bepaalWaardenEnPasAan(dir, name)
