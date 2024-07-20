def fib_recursive(n):
    if n <= 1:
        return n
    else:
        return fib_recursive(n-1) + fib_recursive(n-2)

def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
    return a

def test_fib_recursive(benchmark):
    result = benchmark(fib_recursive, 20)
    assert result == 6765

def test_fib_iterative(benchmark):
    result = benchmark(fib_iterative, 20)
    assert result == 6765
