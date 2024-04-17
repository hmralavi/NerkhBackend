# TODO: use httpx.AsyncClient (pip install httpx) instead of requests.get
import bonbast.main
import requests
from bs4 import BeautifulSoup
from data_tools import PriceData
from datetime import datetime, timezone, timedelta

# Define the offset for Tehran timezone (UTC+3:30)
tehran_offset = timedelta(hours=3, minutes=30)

# Create a timezone object for Tehran
tehran_tz = timezone(tehran_offset)


def get_bonbast_prices() -> list[PriceData]:
    try:
        requests.get("https://bonbast.com", timeout=20)
    except requests.exceptions.ConnectTimeout as e:
        err = PriceData(name=str(e), code="ERROR", source="", price=0)
        return [err]
    collections = bonbast.main.get_prices()
    prices = []
    for collection in collections:
        for model in collection:
            try:
                prices.append(
                    PriceData(
                        code=model.code,
                        name=model.name,
                        source="bonbast",
                        price_sell=model.sell,
                        price_buy=model.buy,
                        time=datetime.now(tz=tehran_tz).isoformat(),
                    )
                )
            except AttributeError:
                prices.append(
                    PriceData(
                        code=model.code,
                        name=model.name,
                        source="bonbast",
                        price_sell=float(model.price),
                        price_buy=float(model.price),
                        time=datetime.now(tz=tehran_tz).isoformat(),
                    )
                )
    return prices


def get_tgju_prices() -> list[PriceData]:
    url = "https://www.tgju.org/currency"
    response = requests.get(url)
    prices = []

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all links (a tags) on the page
        sections = soup.find_all("tr")

        # Extract and print the URLs of the links
        for sec in sections:
            name = sec.get("data-market-nameslug")
            price = sec.get("data-price")
            try:
                prices.append(
                    PriceData(
                        code=name,
                        name=name,
                        source="tgju",
                        price_sell=float(price.replace(",", "")),
                        price_buy=float(price.replace(",", "")),
                        time=datetime.now(tz=tehran_tz).isoformat(),
                    )
                )
            except Exception as e:
                pass
    else:
        print(f"Failed to retrieve webpage: {response.status_code}")
    return prices
