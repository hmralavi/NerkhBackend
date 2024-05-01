import time
import requests
import subprocess


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Time elapsed for {func.__name__}: {end_time - start_time} seconds")
        return result

    return wrapper


def get_public_ip():
    try:
        response = requests.get("https://httpbin.org/ip")
        data = response.json()
        return data["origin"]
    except Exception as e:
        print("Error:", e)
        return None


def get_current_branch():
    try:
        result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # Handle the case where Git is not available or the command fails
        return None
