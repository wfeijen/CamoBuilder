from PIL import Image
from projectClasses.ColorPair import ColorPair

class PictureCreator:
    def __init__(self, definities):
        self.definities = definities

    def createPicture(self, name, colorCodes, topos, colorWeights):
        img = Image.new('RGB', (self.definities.w, self.definities.h), (255, 255, 255))
        pix = img.load()

        kleurInformatie = list(zip(topos, colorWeights))
        transparency = kleurInformatie[-1]
        kleurInformatie = kleurInformatie[:-1]

        for ix in range(self.definities.w):
            for iy in range(self.definities.h):
                kleurenParen = [
                    ColorPair(kleurInformatie[kleur][0].topografie.getPunt(ix, iy) + kleurInformatie[kleur][1],
                              colorCodes[kleur]) for
                    kleur in range(0, len(kleurInformatie))]
                kleurenParen.sort(key=lambda x: x.valueIn, reverse=True)
                if transparency[0].topografie.getPunt(ix, iy) > transparency[1]:  # We combineren kleuren
                    firstColor = kleurenParen[0].valueIn  # - kleurenParen[2].valueIn
                    secondColor = kleurenParen[1].valueIn  # - kleurenParen[2].valueIn
                    tot = max(firstColor + secondColor, 1)  # we willen geen nul krijgen
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
        img.save(name + '_transp_' + str(colorWeights[-1]).zfill(6) + ".JPG")


