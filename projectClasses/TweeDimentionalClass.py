import warnings
from array import array

class TweeDimentionalClass:
    def __init__(self, soortVulling, breedte, hoogte, vulling):
        self.breedte = breedte
        self.lengte = breedte * hoogte
        self.lineaireArray = array(soortVulling, vulling)
        if len(self.lineaireArray) != self.lengte:
            warnings.warn("let op. Tweedimentional object gevuld met verkeerde lengte input. Verwacht: " +
                          self.lengte + " gekregen: " + len(self.lineaireArray))


    def getPunt(self, x, y):
        return self.lineaireArray[x + (y * self.breedte)]

    def setPunt(self, x, y, waarde):
        self.lineaireArray[x + (y * self.breedte)] = waarde
