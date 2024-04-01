from utils.collect import calculate_player_log_file

from utils.prop_collector import Collector

from utils.combine_prop_pred import combine_props_pred_files

from utils.cleanup import move_files, move_file
import datetime
import os

EVENT_DIR = "events"
PROP_DIR = "props"
PLAYER_LOGS = "player_logs.csv"
PREDICTIONS = "predictions.csv"
PROPS_FILE = "odd.csv"
COMBINED_FILE = "combined.csv"
PLAYER_INFO_FILE = "player_info.csv"

if __name__ == "__main__":
    calculate_player_log_file(PLAYER_LOGS, PREDICTIONS, PLAYER_INFO_FILE)
    print("player logs calculated")


    Collector.collectAllPropDataToCSV(EVENT_DIR, PROP_DIR, PROPS_FILE)
    print("props found")


    combine_props_pred_files(PROPS_FILE, PREDICTIONS, COMBINED_FILE)
    print("combined odds and predictions")

    #Create directory for predictions archive
    prediction_dir = os.path.join(os.getcwd(), f"prediction-{datetime.date.today()}")
    os.makedirs(prediction_dir, exist_ok=True)

    today = datetime.date.today()
    archive_event = f"{prediction_dir}/events"
    archive_props = f"{prediction_dir}/props"

    move_files(EVENT_DIR, archive_event)
    move_files(PROP_DIR, archive_props)

    move_file(PLAYER_LOGS, prediction_dir)
    move_file(PROPS_FILE, prediction_dir)
    move_file(COMBINED_FILE, prediction_dir)
    move_file(PREDICTIONS, prediction_dir)

    print("placeholder")
