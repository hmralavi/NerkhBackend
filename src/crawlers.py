"""
TODO: use httpx.AsyncClient (pip install httpx) instead of requests.get
"""

import bonbast.main
import bonbast.models
import requests
from bs4 import BeautifulSoup
from data_tools import PriceData, translate_prices
from datetime import datetime, timezone, timedelta

# Define the offset for Tehran timezone (UTC+3:30)
tehran_offset = timedelta(hours=3, minutes=30)

# Create a timezone object for Tehran
tehran_tz = timezone(tehran_offset)


def get_bonbast_prices(check_website_is_available_first: bool = False) -> list[PriceData]:
    if check_website_is_available_first:
        try:
            requests.get("https://bonbast.com", timeout=20)
        except requests.exceptions.ConnectTimeout as e:
            return [PriceData(code="ERROR", description=str(e))]
    collections = bonbast.main.get_prices()
    prices = []
    for collection in collections:
        for model in collection:
            if isinstance(model, bonbast.models.Currency) or isinstance(model, bonbast.models.Coin):
                prices.append(
                    PriceData(
                        code=model.code,
                        source="bonbast",
                        price1=model.sell,
                        price2=model.buy,
                        time=datetime.now(tz=tehran_tz).isoformat(),
                    )
                )
            elif isinstance(model, bonbast.models.Gold):
                prices.append(
                    PriceData(
                        code=model.code,
                        source="bonbast",
                        price1=float(model.price),
                        time=datetime.now(tz=tehran_tz).isoformat(),
                    )
                )
    prices = translate_prices(prices)
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
                        source="tgju",
                        price1=float(price.replace(",", "")),
                        price2=float(price.replace(",", "")),
                        time=datetime.now(tz=tehran_tz).isoformat(),
                    )
                )
            except Exception as e:
                pass
    else:
        print(f"Failed to retrieve webpage: {response.status_code}")
    prices = translate_prices(prices)
    return prices


def get_car_prices():
    url = "https://www.iranjib.ir/showgroup/45/%D9%82%DB%8C%D9%85%D8%AA-%D8%AE%D9%88%D8%AF%D8%B1%D9%88-%D8%AA%D9%88%D9%84%DB%8C%D8%AF-%D8%AF%D8%A7%D8%AE%D9%84/"
    response = requests.get(url)
    prices = []

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        for tr in soup.find_all("tr"):
            try:
                code = tr.find("td", class_="entryrtl").a.text
                pr = [float(p.text.replace(",", "")) for p in tr.find_all("span", class_="lastprice")]
            except AttributeError:
                continue
            try:
                prices.append(
                    PriceData(
                        code=code,
                        source="iranjib",
                        price1=pr[0],
                        price2=pr[1],
                        time=datetime.now(tz=tehran_tz).isoformat(),
                    )
                )
            except Exception as e:
                pass
    else:
        print(f"Failed to retrieve webpage: {response.status_code}")
    prices = translate_prices(prices)
    return prices


# prices = get_car_prices()
# prices = get_bonbast_prices()
# print(prices)
