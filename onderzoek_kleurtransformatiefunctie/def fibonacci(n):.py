def fibonacci(n):
 a, b = 0, 1
 for _ in range(n):
    yield a
    a, b = b, a + b

f = fibonacci(10000)

print(str(next(f)))
print(str(next(f)))
print(str(next(f)))
print(str(next(f)))
print(str(next(f)))
print(str(next(f)))