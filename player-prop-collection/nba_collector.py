import os
# from dotenv import load_dotenv
import requests
import json
import re
from datetime import datetime, date
import csv
import pytz
# load_dotenv()

# API_KEY = os.getenv('API_KEY')
# HISTORICAL_API_KEY = os.getenv('HISTORICAL_API_KEY')
API_KEY = "bc7791c727dae92fcf26b6e1338575e9"
HISTORICAL_API_KEY = "668b5200589eb79da855b2f68cd0749a"
BASE = "https://api.the-odds-api.com/v4"


class Collector:

    sports_titles = []
    sports_keys = []

    @staticmethod
    def getAPIKey():
        print("testing")

    @staticmethod
    def convertISOtoEST(iso_time):
        # Split the ISO 8601 string to extract date and time components
        date_part, time_part = iso_time.split('T')

        # Extract hour, minute, and second components from the time part
        hour, minute, second = map(int, time_part[:-1].split(':'))  # Remove the 'Z' at the end

        # Adjust the hour to EST timezone (UTC-5)
        hour -= 5

        # If the adjusted hour is negative, roll back to the previous day
        if hour < 0:
            hour += 24
            # Adjust the date part accordingly
            year, month, day = map(int, date_part.split('-'))
            previous_day = (year, month, day - 1)
            date_part = '-'.join(map(str, previous_day))

        # Construct the EST time string
        est_time = f"{date_part}"

        return est_time

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

        orig_date = date
        date += "T10:00:00Z"  # auto collect at 10 AM

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
            with open(f"basketball-events/{sport}-event-{orig_date}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)


    @staticmethod
    def getPropByEventFiles(dir, sport, markets, regions):
        # gets all props for every single event in basketball-events
        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file)) and file.endswith('.json'):
                with open(os.path.join(dir, file), "r") as f:
                    data = json.load(f)

                timestamp = data["timestamp"]

                for event in data["data"]:
                    eventId = event["id"]
                    Collector.getHistoricalNbaPropsByEventId(sport, eventId, markets, regions, timestamp, True)
        
    @staticmethod
    def convertPropFilesToSingularCSV(dir):
        csv_player_data = []

        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file)) and file.endswith('.json'):
                with open(os.path.join(dir, file), "r") as f:
                    data = json.load(f)

                filename = os.path.join(dir, file)
                date = filename.split("props-")[1].replace(".json", "")


                data = data["data"]

                player_data = {}

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
                    

                for player, lines in player_data.items():
                    row = {'Player': player, 'Date': date}
                    for prop_type, values in lines.items():
                        for prop_info, value in values.items():
                            row[f"{prop_type}_{prop_info}"] = value
                    csv_player_data.append(row)


        headers = set()
        for row in csv_player_data:
            headers.update(row.keys())

        # Write CSV data to file
        with open('odds_output.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(headers))
            writer.writeheader()
            writer.writerows(csv_player_data)


    @staticmethod
    def getHistoricalNBAPropsByEventId(sport, eventId, markets, regions, date, testing):
        if (testing == True):
            with open("basketball-player-props/da359da99aa27e97d38f2df709343998-props-2023-11-29T10:00:00Z.json", "r") as file:
                d = json.loads(file)
                return d

        # ISO format: 2021-10-18T12:00:00Z
        # yyyy mm dd

        if not Collector.validateDate(date):
            print(f"Invalid date: {date}")
            return
        
        orig_date = date
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

            return None


        if data is not None:
            with open(f"basketball-player-props/{eventId}-props-{orig_date}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
            
        return data


    
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
    def exploreHistoricalPropData(filename):
        date = filename.split("props-")[1].replace(".json", "")

        with open(filename) as f:
            data = json.load(f)

        data = data["data"]

        player_data = {}

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
            row = {'Player': player, 'Date': date}
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

    #Collector.getPropByEventFiles("basketball-events")

    #Collector.getHistoricalEvents("basketball_nba", "2023-03-30")

    #Collector.getHistoricalNBAPropsByEventId("basketball_nba", "da359da99aa27e97d38f2df709343998", ["player_points"], ["us"], "2023-11-29")

    #Collector.exploreHistoricalPropData("basketball-player-props/da359da99aa27e97d38f2df709343998-props-2023-11-29.json")

    #Collector.convertPropFilesToSingularCSV("basketball-player-props")

    iso_time = "2023-12-21T00:10:00Z"  # Example ISO 8601 time
    est_time = Collector.convertISOtoEST(iso_time)
    print("ISO 8601 time:", iso_time)
    print("EST time:", est_time)

    print("nothing running...")


