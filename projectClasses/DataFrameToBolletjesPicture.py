from PIL import Image

class DataFrameToBolletjesPicture:
    def __init__(self, breedte, hoogte, rootDir):
        self.breedte = breedte
        self.hoogte = hoogte
        self.rootDir = rootDir

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

    def genereer(self, dataFrame, naamBasis):
        img = Image.new('RGB', (self.breedte * 4 + 2, self.hoogte * 3 + 1), (255, 255, 255))
        pix = img.load()
        for ix in range(self.breedte):
            for iy in range(self.hoogte):
                self.vul_bolletje(pix, dataFrame[ix, iy], ix, iy)
        img.save(self.rootDir + naamBasis + ".JPG")
