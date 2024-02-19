import os
from dotenv import load_dotenv
import requests
import json
import re
from datetime import date
import csv

load_dotenv()

API_KEY = os.getenv('API_KEY')
HISTORICAL_API_KEY = os.getenv('HISTORICAL_API_KEY')
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
    def getHistoricalEvents(sport, date):

        # ISO format: 2021-10-18T12:00:00Z
        # yyyy mm dd

        if not Collector.validateDate(date):
            print(f"Invalid date: {date}")
            return
        
        date += "T10:00:00Z" # auto collect at 10 AM

        url = f"{BASE}/historical/sports/{sport}/events?apiKey={HISTORICAL_API_KEY}&date={date}"

        print(url)


        response = requests.request("GET", url, headers={}, data={})

        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error Collecting Events Data. Status code: {response.status_code}")
            data = None

        print(data)

        if data is not None:
            with open(f"basketball-events/{sport}-event-{date}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)


    @staticmethod
    def getPropByEventFiles(dir, sport, markets, regions):
        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file)) and file.endswith('.json'):
                with open(os.path.join(dir, file), "r") as f:
                    data = json.load(f)

                timestamp = data["timestamp"]

                for event in data["data"]:
                    eventId = event["id"]
                    props = Collector.getHistoricalNbaPropsByEventId(sport, eventId, markets, regions, timestamp, True)

        







    @staticmethod
    def getHistoricalNBAPropsByEventId(sport, eventId, markets, regions, date, testing):
        if (testing == True):
            return "empty data"

        # ISO format: 2021-10-18T12:00:00Z
        # yyyy mm dd

        if not Collector.validateDate(date):
            print(f"Invalid date: {date}")
            return
        
        date += "T10:00:00Z" # auto collect at 10 AM


        # /v4/historical/sports/{sport}/events/{eventId}/odds?apiKey={apiKey}&regions={regions}&markets={markets}&dateFormat={dateFormat}&oddsFormat={oddsFormat}&date={date}
        url = f'{BASE}/historical/sports/{sport}/events/{eventId}/odds?apiKey={HISTORICAL_API_KEY}&regions={",".join(regions)}&markets={",".join(markets)}&date={date}'

        print(url)
        response = requests.request("GET", url, headers={}, data={})
        print(response.json())


        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error Collecting Player Props Data for {eventId}. Status code: {response.status_code}")
            data = None


        if data is not None:
            with open(f"basketball-player-props/{eventId}-props-{date}.json", "w") as json_file:
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
    
    @staticmethod
    def validateDate(date):
        regex_pattern = r'^\d{4}-\d{2}-\d{2}$'
        return bool(re.match(regex_pattern, date))
    


if __name__ == "__main__":
    # Collector.getOdds("basketball_nba", "us", "h2h", "basketball-us-odds.json")

    #Collector.getEvents("basketball_nba")
    #Collector.getNBAPropsByEventId("basketball_nba", "c691aedfb0a90fd73aaa2d55250c9f37", ["player_points", "player_rebounds", "player_assists", "player_blocks", "player_steals"], ["us"])
   
    #print(Collector.sports_keys)

    Collector.getPropByEventFiles("basketball-events")

    #Collector.getHistoricalEvents("basketball_nba", "2023-03-30")

    #Collector.getHistoricalNBAPropsByEventId("basketball_nba", "da359da99aa27e97d38f2df709343998", ["player_points"], ["us"], "2023-11-29")

    #Collector.explorePropData("e7197eceb5146bd746348f3c861f4154-props-2024-02-12.json")

    #print("nothing running...")
