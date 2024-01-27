import json
import re

class Strategy:

    @staticmethod
    def findArbitrage(file, market, limit):
        
        if Strategy.validateSingleMarket(market) is False:
            print(f"Invalid single market: {market}")
            return

        with open(file, "r") as json_file:
            data = json.load(json_file)


        num_proc = 0

        best_odds = []

        for game in data:
            id = game["id"]
            teams = [game["home_team"], game["away_team"]]

            opt_odds = {
                "home_team": game["home_team"],
                "home_odds": 0,
                "home_book": "NA",
                "away_team": game["away_team"],
                "away_odds": 0,
                "away_book": "NA",
            }

            for book in game["bookmakers"]:
                for m in book["markets"]:
                    if m["key"] == market:
                        for out in m["outcomes"]:
                            if out["name"] == teams[0] and out["price"] > opt_odds["home_odds"]:
                                opt_odds["home_book"] = book["title"]
                                opt_odds["home_odds"] = out["price"]
                        
                            if out["name"] == teams[1] and out["price"] > opt_odds["away_odds"]:
                                opt_odds["away_book"] = book["title"]
                                opt_odds["away_odds"] = out["price"]
                        break
            
            best_odds.append(opt_odds)

            num_proc += 1

            if (num_proc >= limit):
                break
        
        arbitrage = []


        for odds in best_odds:
            market_margin = (1/odds["home_odds"]) + (1/odds["away_odds"])

            if  market_margin <= 1:
                arbitrage.append(odds)
                arbitrage[-1]["market_margin"] = market_margin
                odds["market_margin"] = market_margin
                print("arbitrage found")

        with open("arbitrage_out.json", "w") as json_file:
            json.dump(best_odds, json_file, indent=4)

        
        return arbitrage
        


    @staticmethod
    def validateSingleMarket(market):
        regex_pattern = r'^(h2h|spreads|totals|outrights|h2h_lay|outrights_lay)$'
        return bool(re.match(regex_pattern, market))


if __name__ == "__main__":
    print(Strategy.findArbitrage("basketball-us-odds.json", "h2h", 100))