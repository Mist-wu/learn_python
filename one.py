import time
def timer(func):
    def wrapper(*args, **kwargs):
        time1 = time.time()
        func(*args, **kwargs)
        time2 = time.time()
        print(f"Function {func.__name__} took {time2 - time1:.2f} seconds to execute.")
    return wrapper

@timer
def compute_squares(n):
    return [i * i for i in range(n)]

print(timer.__closure__)  

compute_squares(1000000)