class TestClass:
    data = bytearray(1)
    integers = list()

a = TestClass()
a.data[0] = 1
a.integers.append(1)
b = TestClass()
b.data[0] = 2
b.integers.append(2)
print( a.data[0] , a.integers[0])
print( b.data[0] , a.integers[0])
print( TestClass.data[0] )