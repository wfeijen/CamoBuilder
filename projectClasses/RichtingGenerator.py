import random


class RichtingGenerator:
    def __init__(self, richtingKansen, overall_max):
        self.cum_richting_kansen = cumSum(richtingKansen)
        self.max_kans = max(self.cum_richting_kansen) - 1
        self.overall_max = overall_max

    def geef_richting(self, max_afstand):
        dobbelsteen_gooi = random.randint(0, self.max_kans)
        if dobbelsteen_gooi < self.cum_richting_kansen[0]: richting = (-1, -1)
        elif dobbelsteen_gooi < self.cum_richting_kansen[1]: richting = (-1, 0)
        elif dobbelsteen_gooi < self.cum_richting_kansen[2]: richting = (-1, 1)
        elif dobbelsteen_gooi < self.cum_richting_kansen[3]: richting = (0, -1)
        elif dobbelsteen_gooi < self.cum_richting_kansen[4]: richting = (0, 1)
        elif dobbelsteen_gooi < self.cum_richting_kansen[5]: richting = (1, -1)
        elif dobbelsteen_gooi < self.cum_richting_kansen[6]: richting = (1, 0)
        else: richting = (1, 1)
        afstand = max(0, (min(int(max_afstand), self.overall_max)))
        richting = tuple(random.randint(0, afstand) * x for x in richting)

        return richting


def cumSum(s):
    sm = 0
    cum_list = []
    for i in s:
        sm = sm + i
        cum_list.append(sm)
    return cum_list
