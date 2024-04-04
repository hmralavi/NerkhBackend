from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import bonbast.main
import requests
from bs4 import BeautifulSoup
from typing import Union, List


class PriceData(BaseModel):
    code: str
    name: str
    price: Union[str, int, float]


def get_bonbast_prices():
    collections = bonbast.main.get_prices()
    prices = []
    for collection in collections:
        for model in collection:
            try:
                prices.append(PriceData(code=model.code, name=model.name, price=model.buy))
            except AttributeError:
                prices.append(PriceData(code=model.code, name=model.name, price=model.price))
    return prices


def get_tgju_prices():
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
                prices.append(PriceData(code=name, name=name, price=price))
            except:
                pass
    else:
        print(f"Failed to retrieve webpage: {response.status_code}")
    return prices


app = FastAPI()


@app.get("/get_prices")
def get_prices(asset_code: str = None) -> List[PriceData]:
    return get_bonbast_prices()
