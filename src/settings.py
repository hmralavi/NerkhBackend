from dotenv import load_dotenv
import os

load_dotenv()


def get_redis_index():
    branch = os.environ["CURRENT_BRANCH"]
    if branch == "main":
        return 0
    elif branch == "development":
        return 1
    return 2


REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
REDIS_INDEX = get_redis_index()
