class ColorPair:
    def __init__(self, value, kleurCode):
        self.valueIn = value
        self.valueOut = value
        self.kleurCode = kleurCode

    def afgewogen_kleurcode(self, i):
        antwoord = int(self.valueOut * self.kleurCode[i])
        return antwoord