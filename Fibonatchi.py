def imp_fibbonacci_of(n):
    fibonacciList = [0, 1]
    for term in range(2, n + 1):
        value = fibonacciList[term - 1] + fibonacciList[term - 2]
        fibonacciList.append(value)
    return(fibonacciList[n])

print(imp_fibbonacci_of(4))


def funct_fibonacci_of(n):
    if n in {0, 1}:  # Base case
        return n
    return funct_fibonacci_of(n - 1) + funct_fibonacci_of(n - 2)  # Recursive case

print(funct_fibonacci_of(4))

class Class_Fibonacci:
    def __init__(self):
        self.fibonacciList = [0, 1]# Base case

    def enkele_waarde(self, n):
        return self.reeks(n)[n]

    def reeks(self, n):
        for term in range(len(self.fibonacciList), n + 1):
            value = self.fibonacciList[term - 1] + self.fibonacciList[term - 2]
            self.fibonacciList.append(value)
        return self.fibonacciList[:n + 1]


fibonacci = Class_Fibonacci()
print(fibonacci.enkele_waarde(4))
print(fibonacci.reeks(4))

def test(x):
    print('hallo')

test()