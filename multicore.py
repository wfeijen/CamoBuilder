from multiprocessing import Pool
import itertools
import functools

def run(x, y, z):
    # this is the function to be run
    print(x)
    # return x + y

x = itertools.product([1, 'a', 3], [2, '2', 2], [3, '3', 3])
y = list(x)

print(list(x))
pool = Pool(processes=4)  # 10 processes
results = pool.starmap(run, x)
print(results)

def f(i, n):
    return i * i + 2*n



pool = Pool(2)
ans = pool.map(functools.partial(f, n=20), range(10))
print(ans)