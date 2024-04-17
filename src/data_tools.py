from pydantic import BaseModel
from typing import List
from datetime import datetime
import numpy as np


MAIN_CODES = ["USD-TMN", "EUR-TMN", "AED-TMN", "GBP-TMN", "TRY-TMN"]


class PriceData(BaseModel):
    code: str = ""
    name: str = ""
    source: str = ""
    price_sell: float = 0
    price_buy: float = 0
    price_sell_change: float = 0
    price_buy_change: float = 0
    time: str = ""  # datetime.isoformat: "yyyy-mm-ddThh:mm:ss.ms", for example: "2024-04-17T15:34:27.559598"


def translate_prices(prices: List[PriceData]) -> List[PriceData]:
    return prices


def is_prices_same_day(price1: PriceData, price2: PriceData):
    d1 = datetime.fromisoformat(price1.time)
    d2 = datetime.fromisoformat(price2.time)
    if d1.year == d2.year and d1.month == d2.month and d1.day == d2.day:
        return True
    return False


def quantize_datetime(dt: datetime, quantize_level: float = 0.25) -> float:
    """
    Convert datetime to a float number representing hour and minute.

    Args:
        dt (datetime): Datetime object.
        quantize_level (float): quantization levels. for example 0.25 means 15 minutes, 1.50 means 1 hour and 30 minutes.

    Returns:
        float: time represented in hour and minute as a float number.
    """

    def quantize_num(num, qlist):
        # Iterate through the list to find the closest number
        for i in range(len(qlist) - 1):
            if num >= qlist[i] and num < qlist[i + 1]:
                return qlist[i]

        return qlist[-1]

    float_time = dt.hour + dt.minute / 60
    qlist = np.arange(start=0, stop=24, step=quantize_level)
    qtime = quantize_num(float_time, qlist)
    return qtime
