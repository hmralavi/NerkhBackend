from fastapi import FastAPI, HTTPException
from typing import List
from data import PriceData
from crawlers import get_bonbast_prices, get_tgju_prices

app = FastAPI()


@app.get("/get_prices")
def get_prices(asset_code: str = None) -> List[PriceData]:
    return [*get_bonbast_prices(), *get_tgju_prices()]


if __name__ == "__main__":
    pass
