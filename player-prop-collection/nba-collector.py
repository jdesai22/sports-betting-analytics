import os
from dotenv import load_dotenv
import requests
import json
import re
from datetime import date
import csv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE = "https://api.the-odds-api.com/v4"


class Collector:

    sports_titles = []
    sports_keys = []

    def __init__(self) -> None:
        pass

    @staticmethod
    def getEvents(sport):
        url = f'{BASE}/sports/{sport}/events?apiKey={API_KEY}'
        
        response = requests.request("GET", url, headers={}, data={})

        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error Collecting Events Data. Status code: {response.status_code}")
            data = None

        if data is not None:
            with open(f"{sport}-event-{date.today()}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
    
    @staticmethod
    def getNBAPropsByEventId(sport, eventId, markets, regions):
        url = f'{BASE}/sports/{sport}/events/{eventId}/odds?markets={",".join(markets)}&regions={",".join(regions)}&apiKey={API_KEY}'

        response = requests.request("GET", url, headers={}, data={})

        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error Collecting Player Props Data for {eventId}. Status code: {response.status_code}")
            data = None

        if data is not None:
            with open(f"{eventId}-props-{date.today()}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

    
    @staticmethod
    def explorePropData(filename):
        with open(filename) as f:
            data = json.load(f)


        player_data = {}

        # for book in data["bookmakers"]:
        #     markets = book["markets"]
        #     for market in markets:
        #         key = market["key"]
        #         for odds in market["outcomes"]:

        for market in data["bookmakers"][0]["markets"]:
            key = market["key"]

            for odds in market["outcomes"]:
                player = odds["description"]
                if player not in player_data:
                    player_data[player] = {}

                if key not in player_data[player]:
                    player_data[player][key] = {}

                player_data[player][key]["line"] = odds["point"]
                player_data[player][key][odds["name"].lower()] = odds["price"]
            

        csv_player_data = []
        for player, lines in player_data.items():
            row = {'Player': player}
            for prop_type, values in lines.items():
                for prop_info, value in values.items():
                    row[f"{prop_type}_{prop_info}"] = value
            csv_player_data.append(row)


        headers = set()
        for row in csv_player_data:
            headers.update(row.keys())

        # Write CSV data to file
        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(headers))
            writer.writeheader()
            writer.writerows(csv_player_data)

                    
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

    #Collector.getEvents("basketball_nba")
    #Collector.getNBAPropsByEventId("basketball_nba", "04a4ea52daa7aa07eb08e449ed7f3e92", ["player_points", "player_rebounds", "player_assists", "player_blocks", "player_steals"], ["us"])
   
    #print(Collector.sports_keys)

    #Collector.explorePropData("04a4ea52daa7aa07eb08e449ed7f3e92-props-2024-02-11.json")

    print("nothing running...")
