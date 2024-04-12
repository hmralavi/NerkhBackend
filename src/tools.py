import time


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Time elapsed for {func.__name__}: {end_time - start_time} seconds")
        return result

    return wrapper
