@profile
def slow_function():
    total = 0
    for i in range(100000):
        total += i
    return total

@profile
def faster_function():
    return sum(range(100000))

if __name__ == "__main__":
    slow_function()
    faster_function()
