import math
import numpy as np
import pandas as pd
import random
def x(centerX, size):
    if centerX - size < 0:
        startX = 0
    else:
        startX = centerX - size
    return startX


for c in range(-2, 2):
    for s in range(-2, 2):
        print(c, "_", s, x(c ,s), max(c-s, 0))

