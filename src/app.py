from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from typing import List
from data import PriceData
from crawlers import get_bonbast_prices, get_tgju_prices
import redis
from settings import DATABASE_HOST, DATABASE_PORT, DATABASE_INDEX


@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect to redis db
    try:
        r = redis.Redis(host=DATABASE_HOST, port=DATABASE_PORT, db=DATABASE_INDEX)
        r.ping()  # Test if the connection is working by sending a PING command
    except redis.ConnectionError:
        raise redis.ConnectionError("Failed to connect to Redis database")
    app.state.redis = r
    yield
    # disconnect from redis db
    app.state.redis.close()


app = FastAPI(lifespan=None)


@app.get("/")
async def index() -> str:
    return "Nerkh API. see /docs for details."


@app.get("/get_prices")
async def get_prices(asset_code: str = None) -> List[PriceData]:
    bonbast_prices = await get_bonbast_prices()
    tgju_prices = await get_tgju_prices()
    return [*bonbast_prices, *tgju_prices]


if __name__ == "__main__":
    pass
