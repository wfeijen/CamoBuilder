import math
import numpy as np
import pandas as pd
import random

xs = random.sample(list(range(0, 5)), 2)

o = np.array(list(range(0, 81)))
reshape1 = o.reshape(9, 3, 3, order='C')
reshape2 = reshape1.reshape(27, 3, order='C')
reshape3 = reshape1.reshape(9, 3, 3, order='C')

print(round(53, -1))
