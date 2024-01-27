import os
from dotenv import load_dotenv
import requests
import json
import re

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE = "https://api.the-odds-api.com/v4"


class Collector:

    sports_titles = []
    sports_keys = []

    def __init__(self) -> None:
        pass

    @staticmethod
    def getSports():
        url = f'{BASE}/sports/?apiKey={API_KEY}'

        response = requests.request("GET", url, headers={}, data={})

        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error Collecting Sports Data. Status code: {response.status_code}")
            data = None

        if data is not None:
            with open("sports.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
    
    
    @staticmethod
    def setSportTitles():
        with open("sports.json", "r") as json_file:
            data = json.load(json_file)
            Collector.sports_titles = [sport["title"] for sport in data]

    @staticmethod
    def setSportKeys():
        with open("sports.json", "r") as json_file:
            data = json.load(json_file)
            Collector.sports_keys = [sport["key"] for sport in data]

    @staticmethod
    def getOdds(sport, region, market, out_file):

        if Collector.validateRegion(region) is False:
            print(f"Invalid region: {region}")
        elif Collector.validateMarket(market) is False:
            url = f'{BASE}/sports/{sport}/odds/?apiKey={API_KEY}&regions={region}'
        else:
            url = f'{BASE}/sports/{sport}/odds/?apiKey={API_KEY}&regions={region}&markets={market}'

        print(url)

        response = requests.request("GET", url, headers={}, data={})

        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error Collecting Odds Data. Status code: {response.status_code}")
            data = None

        if data is not None:
            with open(out_file, "w") as json_file:
                json.dump(data, json_file, indent=4)


        
    @staticmethod
    def validateRegion(reg):
        regex_pattern = r'^(us|us2|uk|au|eu)(,(us|us2|uk|au|eu))*$'
        return bool(re.match(regex_pattern, reg))

    @staticmethod
    def validateMarket(market):
        regex_pattern = r'^(h2h|spreads|totals|outrights|h2h_lay|outrights_lay)(,(h2h|spreads|totals|outrights|h2h_lay|outrights_lay))*$'
        return bool(re.match(regex_pattern, market))
    


if __name__ == "__main__":
    # Collector.getOdds("basketball_nba", "us", "h2h", "basketball-us-odds.json")
    # print(Collector.sports_keys)

    print("nothing running...")
