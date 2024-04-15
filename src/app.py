from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status
from typing import List, Optional
from data import PriceData, convert_crawler_results
from crawlers import get_bonbast_prices, get_tgju_prices
import redis
from settings import *
from authentication_tools import validate_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect to redis db
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_INDEX)
        r.ping()  # Test if the connection is working by sending a PING command
    except redis.ConnectionError:
        raise redis.ConnectionError("Failed to connect to Redis database")
    app.state.redis = r
    yield
    # disconnect from redis db
    app.state.redis.close()


app = FastAPI(lifespan=lifespan)


# Function to authenticate the user with the token
def authenticate_token(token: str):
    token_status = validate_token(token)
    if not token_status[0]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=token_status[1])
    return True


@app.get("/")
def index() -> str:
    return "Nerkh API. see /docs for details."


@app.post("/store_prices")
def store_prices(prices: List[PriceData], authenticated: bool = Depends(authenticate_token)):
    # Here you can store the name in your database or perform any desired operation
    app.state.redis.set("name", prices[0].code)
    return {"message": f"Name '{prices}' stored successfully"}


@app.get("/get_prices")
def get_name():
    return app.state.redis.get("name")


if __name__ == "__main__":
    pass
