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

        kleurInformatie = list(zip(detailTopos, colorWeights))

        for ix in range(self.definities.w):
            for iy in range(self.definities.h):
                kleurenParen = [
                    ColorPair(kleurInformatie[kleur][0].topografie[ix, iy] +
                              kleurInformatie[kleur][1] +
                              int(globaleTopos[kleurNaarHoofdkleurVerwijzing[kleur]].topografie[ix, iy] * sterkteSecundairPatroon),
                              colorCodes[kleur]) for
                    kleur in range(0, len(kleurInformatie))]
                kleurenParen.sort(key=lambda x: x.valueIn, reverse=True)
                if transparantieTopo.topografie[ix, iy] <= transparantie:  # We combineren kleuren
                    firstColor = kleurenParen[0].valueIn  # - kleurenParen[2].valueIn
                    secondColor = kleurenParen[1].valueIn  # - kleurenParen[2].valueIn
                    tot = firstColor + secondColor
                    kleurenParen[0].valueOut = firstColor / tot
                    kleurenParen[1].valueOut = secondColor / tot
                    # Nu kunnen we de kleuren combineren
                    pixel = (int(kleurenParen[0].afgewogen_kleurcode(0) + kleurenParen[1].afgewogen_kleurcode(0)),
                                   int(kleurenParen[0].afgewogen_kleurcode(1) + kleurenParen[1].afgewogen_kleurcode(1)),
                                   int(kleurenParen[0].afgewogen_kleurcode(2) + kleurenParen[1].afgewogen_kleurcode(2)))
                    pix[ix, iy] = pixel
                else:  # We nemen alleen de dominante kleur
                    pixel = (kleurenParen[0].kleurCode[0],
                                   kleurenParen[0].kleurCode[1],
                                   kleurenParen[0].kleurCode[2])
                    pix[ix, iy] = pixel
        img.save(name + '_transp' + str(transparantie) + "s_terkteSecPatr" + str(sterkteSecundairPatroon) + ".JPG")


