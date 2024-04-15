import sys
import requests
from dotenv import load_dotenv
import os
import subprocess
from typing import List

sys.path.append("src")

from data import PriceData, convert_crawler_results
from crawlers import get_bonbast_prices, get_tgju_prices


load_dotenv()

NERKH_TOKEN = os.environ["NERKH_TOKEN"]


def get_current_branch():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # Handle the case where Git is not available or the command fails
        return None


# Function to post a list of PriceData to a URL
def post_data(url: str, data: List[PriceData]):
    json_data = [item.model_dump() for item in data]
    response = requests.post(url, headers={"token": NERKH_TOKEN}, json=json_data)
    return response


def main():
    current_branch = get_current_branch()

    url = None

    if current_branch == "main":
        url = "https://nerkh-api.liara.run/submit_prices"
    elif current_branch == "development":
        url = "https://nerkh-api-dev.liara.run/submit_prices"
        # url = "http://localhost:8000/submit_prices"
        # url = "http://0.0.0.0:10000/submit_prices"

    if url:
        # bonbast_prices = get_bonbast_prices()
        bonbast_prices = get_tgju_prices()
        converted_prices = convert_crawler_results(bonbast_prices)
        # Post the data to the URL
        response = post_data(url, converted_prices)

        # Check the response
        if response.status_code == 200:
            print(f"Data posted successfully! response: {response.text}")
        else:
            print(f"Failed to post data. Status code: {response.status_code}, Error: {response.text}")


if __name__ == "__main__":
    main()
