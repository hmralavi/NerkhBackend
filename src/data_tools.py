from pydantic import BaseModel
from typing import List
from datetime import datetime
import numpy as np


# Supported asset categories
_CURRENCY = "currency"
_COMMODITY = "commodity"
_DIGITAL_CURRENCY = "digital_currency"
_CAR = "car"


MAIN_CODES = {
    # Currencies
    "USD-TMN": (_CURRENCY, "US Dollar - IR Toman"),  # code: (category, description)
    "EUR-TMN": (_CURRENCY, "EURO - IR Toman"),
    "GBP-TMN": (_CURRENCY, "British Pound - IR Toman"),
    "CHF-TMN": (_CURRENCY, "Swiss Franc - IR Toman"),
    "CAD-TMN": (_CURRENCY, "Canadian Dollar - IR Toman"),
    "AUD-TMN": (_CURRENCY, "Australian Dollar - IR Toman"),
    "SEK-TMN": (_CURRENCY, "Swedish Krona - IR Toman"),
    "NOK-TMN": (_CURRENCY, "Norwegian Krone - IR Toman"),
    "RUB-TMN": (_CURRENCY, "Russian Ruble - IR Toman"),
    "THB-TMN": (_CURRENCY, "Thai Baht - IR Toman"),
    "SGD-TMN": (_CURRENCY, "Singapore Dollar - IR Toman"),
    "HKD-TMN": (_CURRENCY, "Hong Kong Dollar - IR Toman"),
    "AZN-TMN": (_CURRENCY, "Azerbaijani Manat - IR Toman"),
    "AMD-TMN": (_CURRENCY, "10Armenian Dram - IR Toman"),
    "DKK-TMN": (_CURRENCY, "Danish Krone - IR Toman"),
    "AED-TMN": (_CURRENCY, "UAE Dirham - IR Toman"),
    "JPY-TMN": (_CURRENCY, "10Japanese Yen - IR Toman"),
    "TRY-TMN": (_CURRENCY, "Turkish Lira - IR Toman"),
    "CNY-TMN": (_CURRENCY, "Chinese Yuan - IR Toman"),
    "SAR-TMN": (_CURRENCY, "KSA Riyal - IR Toman"),
    "INR-TMN": (_CURRENCY, "Indian Rupee - IR Toman"),
    "MYR-TMN": (_CURRENCY, "Ringgit - IR Toman"),
    "AFN-TMN": (_CURRENCY, "Afghan Afghani - IR Toman"),
    "KWD-TMN": (_CURRENCY, "Kuwaiti Dinar - IR Toman"),
    "IQD-TMN": (_CURRENCY, "100Iraqi Dinar - IR Toman"),
    "BHD-TMN": (_CURRENCY, "Bahraini Dinar - IR Toman"),
    "OMR-TMN": (_CURRENCY, "Omani Rial - IR Toman"),
    "QAR-TMN": (_CURRENCY, "Qatari Riyal - IR Toman"),
    # Assets
    "SEKKE-EMAMI-TMN": (_COMMODITY, "Sekke Emami Tamam - IR Toman"),
    "SEKKE-GERAMI-TMN": (_COMMODITY, "Sekke 1Gerami - IR Toman"),
    "SEKKE-AZADI-TMN": (_COMMODITY, "Sekke Azadi Tamam - IR Toman"),
    "SEKKE-NIM-TMN": (_COMMODITY, "Sekke Azadi Nim - IR Toman"),
    "SEKKE-ROB-TMN": (_COMMODITY, "Sekke Azadi Rob - IR Toman"),
    "TALA-MESGHAL-TMN": (_COMMODITY, "Tala18 Mesghal - IR Toman"),
    "TALA-GERAM-TMN": (_COMMODITY, "Tala18 Gerami - IR Toman"),
    "OUNCE-USD": (_COMMODITY, "Ounce Jahani - US Dollar"),
    "BITCOIN-USD": (_DIGITAL_CURRENCY, "Bitcoin - US Dollar"),
    # Cars Irankhodro
    "CAR-ARISAN": (_CAR, "ایرانخودرو وانت آریسان (ارتقاء)"),
    "CAR-SOREN": (_CAR, "ایرانخودرو سورن پلاس موتور XU7P"),
    "CAR-DENA": (_CAR, "دنا پلاس توربو 6 سرعته (ارتقاء)"),
    "CAR-PEUGEOT-PARS": (_CAR, "پژو پارس"),
    # Cars Saipa
    "CAR-ATLAS": (_CAR, "سایپا اطلس"),
    "CAR-SAINA-S": (_CAR, "سایپا ساینا اس"),
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
    # Irankhodro
    "وانت آریسان (ارتقاء)": "CAR-ARISAN",
    "سورن پلاس موتور XU7P": "CAR-SOREN",
    "دنا پلاس توربو 6 سرعته (ارتقاء)": "CAR-DENA",
    "پژو پارس": "CAR-PEUGEOT-PARS",
    # Saipa
    "اطلس": "CAR-ATLAS",
    "ساینا S": "CAR-SAINA-S",
}


class PriceData(BaseModel):
    code: str = ""  # code of the asset, for example, "USD-TMN".
    category: str = ""  # category of the asset, currently 4 supported categories: cuurency, commodity, digital_currency, car.
    description: str = ""  # a description about the asset.
    source: str = ""  # source of the data.
    price_high: float = 0  # assets's higher price, for example, sell price for currency and market price for car.
    price_low: float = 0  # assets's lower price, for example, buy price for currency and factory price for car.
    price_high_change: float = 0  # price_high change compared to yesterday.
    price_low_change: float = 0  # price_low change compared to yesterday.
    time: str = ""  # register time of the data in the iso format: "yyyy-mm-ddThh:mm:ss.ms".


class PricesPayload(BaseModel):
    prices: List[PriceData]


class CodesPayload(BaseModel):
    codes: List[str]


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
                p.category = MAIN_CODES[p.code][0]
                p.description = MAIN_CODES[p.code][1]
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
