from memory_profiler import profile

@profile
def memory_intensive_function():
    a = [i for i in range(100000)]
    b = [i*2 for i in range(100000)]
    return a, b

if __name__ == "__main__":
    memory_intensive_function()