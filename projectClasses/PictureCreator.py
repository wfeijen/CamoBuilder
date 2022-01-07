import random

from PIL import Image
from projectClasses.ColorPair import ColorPair
from random import shuffle


class PictureCreator:
    def __init__(self, definities):
        self.definities = definities

    def createPicture(self, name, colorCodes, detailTopos, globaleTopos, transparantieTopo,
                      transparantie, colorWeights, kleurNaarHoofdkleurVerwijzing,
                      sterkteSecundairPatroon):
        img = Image.new('RGB', (self.definities.w, self.definities.h), (255, 255, 255))
        pix = img.load()

        # kleurInformatie = list(zip(detailTopos, colorWeights))
        # We willen kleuren in dezelfde verhouding hebben. Dat doen we door langzaam de bias te verhogen
        # We bekijken dus het verschil in voorkomen in dit nieuwe plaatje in vergelijking met de oorspronkelijke verdeling
        colorBias = list(colorWeights)
        pixelsPerKleur = [0] * len(colorBias)
        pixelsGedaan = 1 # We initaliseren op 0 om niet door 0 te delen

        for ix in range(self.definities.w):
            for iy in range(self.definities.h):
                kleurGewichten_kleurCodes = [
                    (detailTopos[kleur].topografie[ix, iy] +
                     (colorBias[kleur] - (1000 * pixelsPerKleur[kleur]) // pixelsGedaan) +
                     int(globaleTopos[kleurNaarHoofdkleurVerwijzing[kleur]].topografie[
                             ix, iy] * sterkteSecundairPatroon),
                     colorCodes[kleur],
                     kleur) for
                    kleur in range(0, len(colorWeights))]
                kleurGewichten_kleurCodes.sort(key=lambda x: x[0], reverse=True)
                if transparantie > 0 and transparantieTopo.topografie[ix, iy] <= transparantie:  # We combineren kleuren
                    if len(kleurGewichten_kleurCodes) > 2:
                        thirdColor = kleurGewichten_kleurCodes[2][0]
                        firstColor = max(1, kleurGewichten_kleurCodes[0][0] - thirdColor)  # - kleurGewichten_kleurCodes[2].valueIn
                        secondColor = max(1, kleurGewichten_kleurCodes[1][0] - thirdColor)  # - kleurGewichten_kleurCodes[2].valueIn

                    else:
                        firstColor = kleurGewichten_kleurCodes[0][0]
                        secondColor = kleurGewichten_kleurCodes[1][0]
                    tot = firstColor + secondColor
                    aandeelEersteKleur = firstColor / tot
                    aandeelTweedeKleur = secondColor / tot
                    # Nu kunnen we de kleuren combineren
                    pixel = (
                    int(kleurGewichten_kleurCodes[0][1][0] * aandeelEersteKleur + kleurGewichten_kleurCodes[1][1][0] * aandeelTweedeKleur),
                    int(kleurGewichten_kleurCodes[0][1][1] * aandeelEersteKleur + kleurGewichten_kleurCodes[1][1][1] * aandeelTweedeKleur),
                    int(kleurGewichten_kleurCodes[0][1][2] * aandeelEersteKleur + kleurGewichten_kleurCodes[1][1][2] * aandeelTweedeKleur))
                    pix[ix, iy] = pixel
                    # Bijwerken telling
                    pixelsPerKleur[kleurGewichten_kleurCodes[0][2]] = pixelsPerKleur[kleurGewichten_kleurCodes[0][2]] + aandeelEersteKleur
                    pixelsPerKleur[kleurGewichten_kleurCodes[1][2]] = pixelsPerKleur[kleurGewichten_kleurCodes[1][2]] + aandeelTweedeKleur
                else:  # We nemen alleen de dominante kleur
                    pixel = (kleurGewichten_kleurCodes[0][1][0],
                             kleurGewichten_kleurCodes[0][1][1],
                             kleurGewichten_kleurCodes[0][1][2])
                    pix[ix, iy] = pixel
                    # Bijwerken telling
                    pixelsPerKleur[kleurGewichten_kleurCodes[0][2]] = pixelsPerKleur[kleurGewichten_kleurCodes[0][2]] + 1
                pixelsGedaan = pixelsGedaan + 1
        img.save(name + '_transp' + str(transparantie) + "_sterkteSecPatr" + str(sterkteSecundairPatroon) + ".JPG")


    def vul_bolletje(self, img, pixel, x, y):
        ybase = y * 3
        xbase = x * 4
        if (y % 2) == 0:
            xbase = xbase + 2

        img[xbase, ybase + 1] = pixel
        img[xbase, ybase + 2] = pixel
        img[xbase + 1, ybase] = pixel
        img[xbase + 1, ybase + 1] = pixel
        img[xbase + 1, ybase + 2] = pixel
        img[xbase + 1, ybase + 3] = pixel
        img[xbase + 2, ybase] = pixel
        img[xbase + 2, ybase + 1] = pixel
        img[xbase + 2, ybase + 2] = pixel
        img[xbase + 2, ybase + 3] = pixel
        img[xbase + 3, ybase + 1] = pixel
        img[xbase + 3, ybase + 2] = pixel


    def createBolletjesPicture(self, name, colorCodes, detailTopos, globaleTopos, transparantieTopo,
                      transparantie, colorWeights, kleurNaarHoofdkleurVerwijzing,
                      sterkteSecundairPatroon,
                               rootDir):
        img = Image.new('RGB', (self.definities.w * 4 + 2, self.definities.h * 3 + 1), (255, 255, 255))
        pix = img.load()

        # kleurInformatie = list(zip(detailTopos, colorWeights))
        # We willen kleuren in dezelfde verhouding hebben. Dat doen we door langzaam de bias te verhogen
        # We bekijken dus het verschil in voorkomen in dit nieuwe plaatje in vergelijking met de oorspronkelijke verdeling
        colorBias = list(colorWeights)
        pixelsPerKleur = [0] * len(colorBias)
        pixelsGedaan = 1 # We initaliseren op 0 om niet door 0 te delen

        coordinatenLijst = []
        for ix in range(self.definities.w):
            for iy in range(self.definities.h):
                coordinatenLijst.append((ix, iy))
        random.shuffle(coordinatenLijst)

        for ix, iy in coordinatenLijst:
            kleurGewichten_kleurCodes = [
                (detailTopos[kleur].topografie[ix, iy] +
                 (colorBias[kleur] - (pixelsPerKleur[kleur] // pixelsGedaan)) +
                 int(globaleTopos[kleurNaarHoofdkleurVerwijzing[kleur]].topografie[
                         ix, iy] * sterkteSecundairPatroon),
                 colorCodes[kleur],
                 kleur) for
                kleur in range(0, len(colorWeights))]
            kleurGewichten_kleurCodes.sort(key=lambda x: x[0], reverse=True)
            if transparantie > 0 and transparantieTopo.topografie[ix, iy] <= transparantie:  # We combineren kleuren
                if len(kleurGewichten_kleurCodes) > 2:
                    thirdColor = kleurGewichten_kleurCodes[2][0]
                    firstColor = max(1, kleurGewichten_kleurCodes[0][0] - thirdColor)  # - kleurGewichten_kleurCodes[2].valueIn
                    secondColor = max(1, kleurGewichten_kleurCodes[1][0] - thirdColor)  # - kleurGewichten_kleurCodes[2].valueIn
                else:
                    firstColor = kleurGewichten_kleurCodes[0][0]
                    secondColor = kleurGewichten_kleurCodes[1][0]
                tot = firstColor + secondColor
                aandeelEersteKleur = firstColor / tot
                aandeelTweedeKleur = secondColor / tot
                # Nu kunnen we de kleuren combineren
                pixel = (
                int(kleurGewichten_kleurCodes[0][1][0] * aandeelEersteKleur + kleurGewichten_kleurCodes[1][1][0] * aandeelTweedeKleur),
                int(kleurGewichten_kleurCodes[0][1][1] * aandeelEersteKleur + kleurGewichten_kleurCodes[1][1][1] * aandeelTweedeKleur),
                int(kleurGewichten_kleurCodes[0][1][2] * aandeelEersteKleur + kleurGewichten_kleurCodes[1][1][2] * aandeelTweedeKleur))
                self.vul_bolletje(pix, pixel, ix, iy)
                # Bijwerken telling
                pixelsPerKleur[kleurGewichten_kleurCodes[0][2]] = pixelsPerKleur[kleurGewichten_kleurCodes[0][2]] + aandeelEersteKleur
                pixelsPerKleur[kleurGewichten_kleurCodes[1][2]] = pixelsPerKleur[kleurGewichten_kleurCodes[1][2]] + aandeelTweedeKleur
            else:  # We nemen alleen de dominante kleur
                pixel = (kleurGewichten_kleurCodes[0][1][0],
                         kleurGewichten_kleurCodes[0][1][1],
                         kleurGewichten_kleurCodes[0][1][2])
                self.vul_bolletje(pix, pixel, ix, iy)
                # Bijwerken telling
                pixelsPerKleur[kleurGewichten_kleurCodes[0][2]] = pixelsPerKleur[kleurGewichten_kleurCodes[0][2]] + 1
            pixelsGedaan = pixelsGedaan + 1
        img.save(rootDir + name + '_tr' + str(transparantie) + "_secPatr" + str(sterkteSecundairPatroon) + ".JPG")


