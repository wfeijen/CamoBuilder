from PIL import Image
from projectClasses.ColorPair import ColorPair


class PictureCreator:
    def __init__(self, definities):
        self.definities = definities

    def createPicture(self, name, colorCodes, detailTopos, globaleTopos, transparantieTopo,
                      transparantie, colorWeights, kleurNaarHoofdkleurVerwijzing,
                      sterkteSecundairPatroon):
        img = Image.new('RGB', (self.definities.w, self.definities.h), (255, 255, 255))
        pix = img.load()

        # kleurInformatie = list(zip(detailTopos, colorWeights))

        for ix in range(self.definities.w):
            for iy in range(self.definities.h):
                kleurGewichten_kleurCodes = [
                    (detailTopos[kleur].topografie[ix, iy] +
                     colorWeights[kleur] +
                     int(globaleTopos[kleurNaarHoofdkleurVerwijzing[kleur]].topografie[
                             ix, iy] * sterkteSecundairPatroon),
                     colorCodes[kleur]) for
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
                else:  # We nemen alleen de dominante kleur
                    pixel = (kleurGewichten_kleurCodes[0][1][0],
                             kleurGewichten_kleurCodes[0][1][1],
                             kleurGewichten_kleurCodes[0][1][2])
                    pix[ix, iy] = pixel
        img.save(name + '_transp' + str(transparantie) + "_sterkteSecPatr" + str(sterkteSecundairPatroon) + ".JPG")
