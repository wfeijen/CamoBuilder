import random


class RichtingGenerator:
    def __init__(self, richtingKansen):
        self.cum_richting_kansen = cumSum(richtingKansen)
        self.max_kans = max(self.cum_richting_kansen) - 1

    def geef_richting(self):
        dobbelsteen_gooi = random.randint(0, self.max_kans)
        if dobbelsteen_gooi < self.cum_richting_kansen[0]: richting = (-1, -1)
        elif dobbelsteen_gooi < self.cum_richting_kansen[1]: richting = (-1, 0)
        elif dobbelsteen_gooi < self.cum_richting_kansen[2]: richting = (-1, 1)
        elif dobbelsteen_gooi < self.cum_richting_kansen[3]: richting = (0, -1)
        elif dobbelsteen_gooi < self.cum_richting_kansen[4]: richting = (0, 1)
        elif dobbelsteen_gooi < self.cum_richting_kansen[5]: richting = (1, -1)
        elif dobbelsteen_gooi < self.cum_richting_kansen[6]: richting = (1, 0)
        else: richting = (1, 1)

        return richting


def cumSum(s):
    sm = 0
    cum_list = []
    for i in s:
        sm = sm + i
        cum_list.append(sm)
    return cum_list
