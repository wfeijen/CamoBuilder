import numpy as np
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plot


range = np.random.RandomState(1)
X = np.sort(5 * range.rand(80, 1), axis=0)
Y = np.sin(X).ravel()
Y[::5] += 3 * (0.5 - range.rand(16))


regression_1 = DecisionTreeRegressor(max_depth=4)
regression_2 = DecisionTreeRegressor(max_depth=7)
regression_1.fit(X, Y)
regression_2.fit(X, Y)


X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
Y1 = regression_1.predict(X_test)
Y2 = regression_2.predict(X_test)


plot.figure()
plot.scatter(X, Y, s=20, edgecolor="black", c="pink", label="data")
plot.plot(X_test, Y1, color="blue", label="max_depth=4", linewidth=2)
plot.plot(X_test, Y2, color="green", label="max_depth=7", linewidth=2)
plot.xlabel("data")
plot.ylabel("target")
plot.title("Decision Tree Regression")
plot.legend()
plot.show()