from pydantic import BaseModel
from typing import List, Union
from datetime import datetime

MainNames = ["USD-TMN", "EUR-TMN", "AED-TMN", "GBP-TMN", "TRY-TMN"]


class PriceData(BaseModel):
    code: str
    name: str
    source: str
    price: Union[str, int, float]
    # price_buy: Union[str, int, float]
    # price_sell: Union[str, int, float]
    # time: datetime


def convert_crawler_results(prices: List[PriceData]) -> List[PriceData]:
    return prices
