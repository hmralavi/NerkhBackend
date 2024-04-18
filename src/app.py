from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status, Header
from typing import List
from data_tools import PriceData, MAIN_CODES, is_prices_same_day
import redis
from settings import *
from authentication_tools import validate_token
import json
from datetime import datetime


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


def authenticate_token(token: str = Header(...)) -> bool:
    """
    Function to authenticate the user with a token.

    Args:
        token (str, optional): your token

    Raises:
        HTTPException: _description_

    Returns:
        bool: successfull authorization
    """
    token_status = validate_token(token)
    if not token_status[0]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=token_status[1])
    return True


def get_price_from_db(key: str, redisdb: redis.Redis) -> PriceData:
    """
    get price data from database.

    Args:
        key (str): key to the price in the format of "code:[yesterday/current]". for example: "USD-TMN:current"
        redisdb (redis.Redis): connection to redis database.

    Returns:
        PriceData: _description_
    """

    price = PriceData(**json.loads(redisdb.get(key)))
    return price


def store_price_in_db(key: str, price: PriceData, redisdb: redis.Redis):
    """
    store price data into the database.
    this function shouldn't be used directly. it is meant to be used by `analyze_and_store_price`.

    Args:
        key (str): key to the price in the format of "code:[yesterday/current]". for example: "USD-TMN:current"
        price (PriceData): _description_
        redisdb (redis.Redis): connection to redis database.
    """
    redisdb.set(key, price.model_dump_json())


def analyze_and_store_price(newprice: PriceData, redisdb: redis.Redis):
    """
    Analyze a new price and stores it in the database.

    Args:
        newprice (PriceData): _description_
        redisdb (redis.Redis): connection to redis database.

    Raises:
        ValueError: the newprice.code must be valid.
    """
    newprice = newprice.model_copy()
    code = newprice.code
    if code not in MAIN_CODES:
        raise ValueError(f"code '{code}' not valid. valid codes: {MAIN_CODES}")

    # get current price in db
    current_price = newprice.model_copy()
    current_key = f"{code}:current"
    if redisdb.exists(current_key):
        current_price = get_price_from_db(current_key, redisdb)

    # check if the newprice is for new day, store the current_price as yesterday's price
    yesterday_key = f"{code}:yesterday"
    if not is_prices_same_day(newprice, current_price):
        if datetime.fromisoformat(newprice.time) > datetime.fromisoformat(current_price.time):
            store_price_in_db(yesterday_key, current_price, redisdb)

    # get yesterday price in db
    yesterday_price = None
    if redisdb.exists(yesterday_key):
        yesterday_price = get_price_from_db(yesterday_key, redisdb)

    # calculate price changes compared to yesterday
    if yesterday_price:
        newprice.price_buy_change = newprice.price_buy - yesterday_price.price_buy
        newprice.price_sell_change = newprice.price_sell - yesterday_price.price_sell

    # store the new price in db
    store_price_in_db(current_key, newprice, redisdb)


@app.get("/")
def index() -> str:
    """
    Home Page
    """
    return "Nerkh API. see /docs for details."


@app.post("/submit_prices")
def submit_prices(prices: List[PriceData], authenticated: bool = Depends(authenticate_token)):
    """
    Submit prices to the server. you need a token for this action.
    """
    n_success = 0
    for price in prices:
        try:
            analyze_and_store_price(price, app.state.redis)
            n_success += 1
        except:
            pass

    return f"{n_success}/{len(prices)} prices stored successfully."


@app.post("/get_prices")
def get_prices(codes: List[str] = []) -> List[PriceData]:
    """
    Gets prices from the server.

    You can get all prices by passing an empty list. for example:

    `curl -X 'POST' 'https://nerkh-api-dev.liara.run/get_prices' -H 'accept: application/json' -H 'Content-Type: application/json' -d '[]'`

    or get prices for specific assets by passing their codes. for example:

    `curl -X 'POST' 'https://nerkh-api-dev.liara.run/get_prices' -H 'accept: application/json' -H 'Content-Type: application/json' -d '["USD-TMN", "EUR-TMN"]'`

    Raises:

        HTTPException 404: if one of the input codes is invalid, you'll get this error.

    Returns:

        List[PriceData]: a json file containing a list of prices.
    """
    prices = []
    if codes:
        for c in codes:
            if c not in MAIN_CODES:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"code '{c}' is not valid. valid codes: {MAIN_CODES}."
                )
            prices.append(get_price_from_db(f"{c}:current", app.state.redis))
    else:
        prices = [get_price_from_db(f"{c}:current", app.state.redis) for c in MAIN_CODES]

    return prices


if __name__ == "__main__":
    pass
