from pydantic import BaseModel
from typing import List
from datetime import datetime
import numpy as np


MAIN_CODES = {
    # Currencies
    "USD-TMN": "US Dollar - IR Toman",  # code: name(description)
    "EUR-TMN": "EURO - IR Toman",
    "GBP-TMN": "British Pound - IR Toman",
    "CHF-TMN": "Swiss Franc - IR Toman",
    "CAD-TMN": "Canadian Dollar - IR Toman",
    "AUD-TMN": "Australian Dollar - IR Toman",
    "SEK-TMN": "Swedish Krona - IR Toman",
    "NOK-TMN": "Norwegian Krone - IR Toman",
    "RUB-TMN": "Russian Ruble - IR Toman",
    "THB-TMN": "Thai Baht - IR Toman",
    "SGD-TMN": "Singapore Dollar - IR Toman",
    "HKD-TMN": "Hong Kong Dollar - IR Toman",
    "AZN-TMN": "Azerbaijani Manat - IR Toman",
    "AMD-TMN": "10Armenian Dram - IR Toman",
    "DKK-TMN": "Danish Krone - IR Toman",
    "AED-TMN": "UAE Dirham - IR Toman",
    "JPY-TMN": "10Japanese Yen - IR Toman",
    "TRY-TMN": "Turkish Lira - IR Toman",
    "CNY-TMN": "Chinese Yuan - IR Toman",
    "SAR-TMN": "KSA Riyal - IR Toman",
    "INR-TMN": "Indian Rupee - IR Toman",
    "MYR-TMN": "Ringgit - IR Toman",
    "AFN-TMN": "Afghan Afghani - IR Toman",
    "KWD-TMN": "Kuwaiti Dinar - IR Toman",
    "IQD-TMN": "100Iraqi Dinar - IR Toman",
    "BHD-TMN": "Bahraini Dinar - IR Toman",
    "OMR-TMN": "Omani Rial - IR Toman",
    "QAR-TMN": "Qatari Riyal - IR Toman",
    # Assets
    "SEKKE-EMAMI-TMN": "Sekke Emami Tamam - IR Toman",
    "SEKKE-GERAMI-TMN": "Sekke 1Gerami - IR Toman",
    "SEKKE-AZADI-TMN": "Sekke Azadi Tamam - IR Toman",
    "SEKKE-NIM-TMN": "Sekke Azadi Nim - IR Toman",
    "SEKKE-ROB-TMN": "Sekke Azadi Rob - IR Toman",
    "TALA-MESGHAL-TMN": "Tala18 Mesghal - IR Toman",
    "TALA-GERAM-TMN": "Tala18 Gerami - IR Toman",
    "OUNCE-USD": "Ounce Jahani - US Dollar",
    "BITCOIN-USD": "Bitcoin - US Dollar",
    # Cars
    "CAR-PEUGEOT-PARS": " Peugeot Pars - IR Toman",
}

bonbast_translate_dict = {
    "USD": "USD-TMN",
    "EUR": "EUR-TMN",
    "GBP": "GBP-TMN",
    "CHF": "CHF-TMN",
    "CAD": "CAD-TMN",
    "AUD": "AUD-TMN",
    "SEK": "SEK-TMN",
    "NOK": "NOK-TMN",
    "RUB": "RUB-TMN",
    "THB": "THB-TMN",
    "SGD": "SGD-TMN",
    "HKD": "HKD-TMN",
    "AZN": "AZN-TMN",
    "AMD": "AMD-TMN",
    "DKK": "DKK-TMN",
    "AED": "AED-TMN",
    "JPY": "JPY-TMN",
    "TRY": "TRY-TMN",
    "CNY": "CNY-TMN",
    "SAR": "SAR-TMN",
    "INR": "INR-TMN",
    "MYR": "MYR-TMN",
    "AFN": "AFN-TMN",
    "KWD": "KWD-TMN",
    "IQD": "IQD-TMN",
    "BHD": "BHD-TMN",
    "OMR": "OMR-TMN",
    "QAR": "QAR-TMN",
    "emami1": "SEKKE-EMAMI-TMN",
    "azadi1g": "SEKKE-GERAMI-TMN",
    "azadi1": "SEKKE-AZADI-TMN",
    "azadi1_2": "SEKKE-NIM-TMN",
    "azadi1_4": "SEKKE-ROB-TMN",
    "mithqal": "TALA-MESGHAL-TMN",
    "gol18": "TALA-GERAM-TMN",
    "ounce": "OUNCE-USD",
    "bitcoin": "BITCOIN-USD",
}

iranjib_transtale_dict = {
    "پژو پارس": "CAR-PEUGEOT-PARS",
}


class PriceData(BaseModel):
    code: str = ""
    name: str = ""
    source: str = ""
    price_sell: float = 0
    price_buy: float = 0
    price_sell_change: float = 0
    price_buy_change: float = 0
    time: str = ""  # datetime.isoformat: "yyyy-mm-ddThh:mm:ss.ms", for example: "2024-04-17T15:34:27.559598"


def translate_prices(prices: List[PriceData], prune: bool = True) -> List[PriceData]:
    """
    translate PriceData.code and PriceData.name according to the translation dicts.

    Args:
        prices (List[PriceData]): list of price data.
        prune (bool, optional): eliminate the prices whose codes/source does not exist in our dictionaries. Defaults to True.

    Returns:
        List[PriceData]: translated list of the price data.
    """
    source_dict = {
        "bonbast": bonbast_translate_dict,
        "iranjib": iranjib_transtale_dict,
    }
    translated_prices = []
    for price in prices:
        p = price.model_copy()
        if p.source in source_dict.keys():
            if p.code in source_dict[p.source].keys():
                p.code = source_dict[p.source][p.code]
                p.name = MAIN_CODES[p.code]
                translated_prices.append(p)
            else:
                if not prune:
                    translated_prices.append(p)
        else:
            if not prune:
                translated_prices.append(p)
    return translated_prices


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
