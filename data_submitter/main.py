import sys
import requests
from dotenv import load_dotenv
import os
import subprocess
from typing import List
import time

sys.path.append("src")

from data_tools import PriceData, translate_prices
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
    nerkh_server_urls = [
        "https://nerkh-api.liara.run/submit_prices",
        "https://nerkh-api-dev.liara.run/submit_prices",
        # "http://localhost:8000/submit_prices",
    ]
    attempts = 1
    while attempts < 1001:
        try:
            print(f"attempt {attempts} to get bonbast data.")
            bonbast_prices = get_bonbast_prices()
            print("bonbast data received successfully.")
            break
        except requests.HTTPError as e:
            print(f"attempt {attempts} failed. error: {e}")
            time.sleep(1)
            attempts += 1
    translate_prices(bonbast_prices)
    for url in nerkh_server_urls:
        # Post the data to the URL
        response = post_data(url, bonbast_prices)
        # Check the response
        if response.status_code == 200:
            print(f"Data posted successfully to {url}. Status code: {response.status_code}, response: {response.text}")
        else:
            print(f"Failed to post data to {url}. Status code: {response.status_code}, response: {response.text}")


if __name__ == "__main__":
    main()
