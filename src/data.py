from pydantic import BaseModel
from typing import List, Union

MainNames = ["USD-TMN", "EUR-TMN", "AED-TMN", "GBP-TMN", "TRY-TMN"]


class PriceData(BaseModel):
    code: str
    name: str
    source: str
    price: Union[str, int, float]
