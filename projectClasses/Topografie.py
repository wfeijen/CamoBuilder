import math
import numpy as np
from projectClasses.TweeDimentionalClass import TweeDimentionalClass


class Topografie:
    def __init__(self, definities):
        self.definities = definities
        self.minSizeSqrt = math.isqrt(self.definities.minSize)
        self.maxSizeSqrt = int(math.ceil(math.sqrt(self.definities.maxSize)))
        if definities.startRandom == 0:
            initieleVulling = [0] * (definities.w * definities.h)
        else:
            initieleVulling = np.random.choice(2 * definities.startRandom, definities.w * definities.h)
        self.topografie = TweeDimentionalClass(soortVulling='i',
                                               breedte=definities.w,
                                               hoogte=definities.h,
                                               vulling=initieleVulling )

    def liftSingle(self, size, centerX, centerY, verdeling, lenVerdeling):
        startX = max(centerX - size, 0)
        endX = min(centerX + size, self.definities.w)
        startY = max(centerY - size, 0)
        endY = min(centerY + size, self.definities.h)
        if self.topografie.getPunt(centerX, centerY) > self.definities.startRandom:
            factor = -1
        else:
            factor = 1
        for ix in range(startX, endX):
            for iy in range(startY, endY):
                afstand = int(math.hypot((centerX - ix), (centerY - iy)))
                if afstand < size:
                    self.topografie.setPunt(ix, iy,
                                            waarde=self.topografie.getPunt(ix, iy) + verdeling[
                                                afstand * lenVerdeling // size] * factor)

    def genereer(self, verdeling):
        for i in range(self.definities.n):
            # print(str(i))
            cx = np.random.randint(0, self.definities.w - 1)
            cy = np.random.randint(0, self.definities.h - 1)
            size = np.random.randint(self.minSizeSqrt, self.maxSizeSqrt)
            size = size * size
            self.liftSingle(size, cx, cy, verdeling, len(verdeling))
        return self
