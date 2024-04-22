import sys
import requests
from dotenv import load_dotenv
import os
from typing import List
from fastapi import FastAPI

sys.path.append("src")

from data_tools import PriceData, PricesPayload
from crawlers import get_bonbast_prices, get_car_prices


load_dotenv()

NERKH_TOKEN = os.environ["NERKH_TOKEN"]


# Function to post a list of PriceData to a URL
def post_data(url: str, prices: List[PriceData]):
    json_data = PricesPayload(prices=prices).model_dump()
    response = requests.post(url, headers={"token": NERKH_TOKEN}, json=json_data)
    return response


app = FastAPI()


nerkh_server_urls = [
    # "https://nerkh-api.liara.run/submit_prices",  # for liara
    "https://nerkh-api-dev.liara.run/submit_prices",  # for liara-dev
    # "http://localhost:8000/submit_prices",  # for local machine
    # "http://0.0.0.0:10000/submit_prices", # for docker
]


def main(crawler_func) -> str:
    prices = crawler_func()
    result = ""
    for url in nerkh_server_urls:
        # Post the data to the URL
        response = post_data(url, prices)
        # Check the response
        success = "Success" if response.status_code == 200 else "Failed"
        result = (
            result + "\n" + f"{success} data post to {url}. Status code: {response.status_code}, response: {response.text}"
        )

    return result


@app.get("/update_bonbast")
def update_bonbast() -> str:
    return main(get_bonbast_prices)


@app.get("/update_car")
def update_car() -> str:
    return main(get_car_prices)


if __name__ == "__main__":
    print(update_bonbast())
    print(update_car())
