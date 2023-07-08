import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

np.random.seed(123)
arr = np.random.rand(100) * 3 -1
def schaalNaarMin1Tot1(arr):
    min = np.min(arr)
    return ((arr - min) * 2 / (np.max(arr) - min)) - 1

geschaalde_vector = schaalNaarMin1Tot1(arr)
print(geschaalde_vector)
plt.hist(x=geschaalde_vector, bins='auto', color='#0504aa',  alpha=0.7, rwidth=0.85)
plt.show()
print(arr)
print(normalize([arr]))
plt.hist(x=arr, bins='auto', color='#0504aa',  alpha=0.7, rwidth=0.85)
plt.show()


normalized_vector = arr / np.linalg.norm(arr)
print(normalized_vector)
plt.hist(x=normalized_vector, bins='auto', color='#0504aa',  alpha=0.7, rwidth=0.85)
plt.show()

# tussen -1 en 1



