# TODO: use httpx.AsyncClient (pip install httpx) instead of requests.get
import bonbast.main
import requests
from bs4 import BeautifulSoup
from data import PriceData


async def get_bonbast_prices():
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
                prices.append(PriceData(code=model.code, name=model.name, source="bonbast", price=model.buy))
            except AttributeError:
                prices.append(PriceData(code=model.code, name=model.name, source="bonbast", price=model.price))
    return prices


async def get_tgju_prices():
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
                prices.append(PriceData(code=name, name=name, source="tgju", price=price))
            except:
                pass
    else:
        print(f"Failed to retrieve webpage: {response.status_code}")
    return prices
