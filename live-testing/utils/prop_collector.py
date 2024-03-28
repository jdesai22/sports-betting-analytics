import os
import time

# from dotenv import load_dotenv
import requests
import json
import re
from datetime import date
import csv
import pandas as pd

from datetime import datetime
import pytz


#load_dotenv()

# need to add api keys here for code to work
BASE = "https://api.the-odds-api.com/v4"
HISTORICAL_API_KEY=""
API_KEY="bc7791c727dae92fcf26b6e1338575e9"
OUTPUT_CSV_DIR = ""
EVENT_DIR = "events"
PROPS_DIR = "props"

class Collector:

    sports_titles = []
    sports_keys = []

    @staticmethod
    def getAPIKey():
        print(HISTORICAL_API_KEY)


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
            with open(f"{EVENT_DIR}/{sport}-event-{date.today()}.json", "w") as json_file:
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
            return None

        # print(data)

        if data is not None:
            with open(f"basketball-events/{sport}-event-{orig_date}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

        return "working"

    @staticmethod
    def getPropByEventFiles(dir, sport, markets, regions):
        # gets all props for every single event in basketball-events
        files_collected = []
        events_found = 0

        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file)) and file.endswith('.json'):
                with open(os.path.join(dir, file), "r") as f:
                    data = json.load(f)

                if type(data) is not list:
                    timestamp = data["timestamp"]
                    est_file_date = Collector.convertISOtoEST(timestamp)
                    print(est_file_date)

                    files_collected.append(os.path.join(dir, file))
                    for event in data["data"]:
                        eventId = event["id"]

                        est_start_date = Collector.convertISOtoEST(event["commence_time"])

                        if est_start_date == est_file_date:
                            events_found += 1
                            d = Collector.getHistoricalNBAPropsByEventId(sport, eventId, markets, regions, timestamp, False, True)
                            print(eventId)
                            if d is None:
                                print(files_collected)
                                return
                            time.sleep(.51)
                else:
                    files_collected.append(os.path.join(dir, file))
                    #print(data)
                    for event in data:
                        eventId = event["id"]

                        events_found += 1
                        d = Collector.getNBAPropsByEventId(sport, eventId, markets, regions)
                        print(eventId)
                        if d is None:
                            print(files_collected)
                            return
                        time.sleep(.51)



        print(f"events found: {events_found}")
        print(f"files collected: {files_collected}")

    @staticmethod
    def format_date(date_str):
        parts = date_str.split('-')
        if len(parts) == 3:
            year = parts[0]
            month = parts[1].zfill(2)  # Zero-padding month
            day = parts[2].zfill(2)    # Zero-padding day
            format_date = f"{year}-{month}-{day}"

            if format_date == "2024-01-00":
                return "2023-12-31"
            elif format_date == "2023-12-00":
                return "2023-11-30"
            elif format_date == "2023-11-00":
                return "2023-10-31"
            elif format_date == "2023-10-00":
                return "2023-09-30"
            else:
                return format_date
        else:
            return None  # Invalid date format

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

        # Format the date part
        date_part = Collector.format_date(date_part)

        # Construct the EST time string
        est_time = f"{date_part}"

        return est_time

    @staticmethod
    def convertPropFilesToSingularCSV(dir, csv_out_file_name):
        csv_player_data = []

        empty_files = []

        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file)) and file.endswith('.json'):
                with open(os.path.join(dir, file), "r") as f:
                    data = json.load(f)

                filename = os.path.join(dir, file)
                date = filename.split("props-")[1].replace(".json", "")

                if "data" in data.keys():
                    data = data["data"]
                else:
                    data = data
                    date = data["commence_time"]

                player_data = {}

                if (len(data["bookmakers"]) == 0):
                    empty_files.append(filename)
                else:
                    for book in data["bookmakers"]:
                        book_name = book["title"]

                        for market in book["markets"]:
                            key = market["key"]

                            for odds in market["outcomes"]:
                                player = odds["description"]
                                if player not in player_data:
                                    player_data[player] = {}


                                odds_type = odds["name"].lower()

                                new_line = odds["point"]
                                new_price = odds["price"]

                                update = False

                                if key not in player_data[player]:
                                    player_data[player][key] = {}
                                    update = True                                    
                                else:
                                    if f"{odds_type}-book" not in player_data[player][key].keys():
                                        update = True
                                    else:
                                        curr_line = player_data[player][key][f"{odds_type}-line"]
                                        curr_price = player_data[player][key][odds_type]

                                        if odds_type == "over":
                                            if new_line < curr_line:
                                                update = True
                                            elif new_line == curr_line and new_price > curr_price:
                                                update = True
                                        else:
                                            if new_line > curr_line:
                                                update = True
                                            elif new_line == curr_line and new_price > curr_price:
                                                update = True

                                if update:
                                    player_data[player][key][f"{odds_type}_book"] = book_name
                                    player_data[player][key][f"{odds_type}_line"] = new_line
                                    player_data[player][key][odds_type] = new_price


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
        with open(csv_out_file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(headers))
            writer.writeheader()
            writer.writerows(csv_player_data)

        print(empty_files)


    @staticmethod
    def getHistoricalNBAPropsByEventId(sport, eventId, markets, regions, date, testing, timestampUsed):
        if testing:
            with open("basketball-player-props/da359da99aa27e97d38f2df709343998-props-2023-11-29.json", "r") as file:
                d = json.load(file)
                # print(d)
                return

        # ISO format: 2021-10-18T12:00:00Z
        # yyyy mm dd

        if not timestampUsed and not Collector.validateDate(date):
            print(f"Invalid date: {date}")
            return

        if not timestampUsed:
            orig_date = date
            date += "T10:00:00Z" # auto collect at 10 AM
        else:
            orig_date = date.split("T")[0]

        # /v4/historical/sports/{sport}/events/{eventId}/odds?apiKey={apiKey}&regions={regions}&markets={markets}&dateFormat={dateFormat}&oddsFormat={oddsFormat}&date={date}
        url = f'{BASE}/historical/sports/{sport}/events/{eventId}/odds?apiKey={HISTORICAL_API_KEY}&regions={",".join(regions)}&markets={",".join(markets)}&date={date}'

        # print(url)
        if not testing:
            response = requests.request("GET", url, headers={}, data={})
        #print(response.json())


        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error Collecting Player Props Data for {eventId}. Status code: {response.status_code}")
            data = None

            return None


        est_date = Collector.convertISOtoEST(date)

        if data is not None:
            with open(f"basketball-player-props/{eventId}-props-{est_date}.json", "w") as json_file:
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
            with open(f"{PROPS_DIR}/{eventId}-props-{date.today()}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

        return data


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
    

    @staticmethod
    def collectAllPropDataToCSV(evt_dir, props_dir, csv_out_file):
        Collector.getEvents("basketball_nba")
        Collector.getPropByEventFiles(evt_dir, "basketball_nba", ["player_points"], ["us"])
        Collector.convertPropFilesToSingularCSV(props_dir, csv_out_file)


if __name__ == "__main__":
    Collector.collectAllPropDataToCSV(EVENT_DIR, PROPS_DIR)
    print("placeholder")