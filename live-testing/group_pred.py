from utils.collect import next_game_pred
from utils.combine_prop_pred import combine_props_pred_files
from utils.evaluate import get_player_log_df, get_player_logs_on_date, append_game_result, count_success, add_to_analysis

# DATES = ["2024-03-27", "2024-03-28", "2024-03-29", "2024-03-30", "2024-03-31", "2024-04-01", "2024-04-02", "2024-04-03", "2024-04-04", "2024-04-05", "2024-04-06"]
DATES = []
PREDICTIONS = "predictions.csv"
PROPS_FILE = "odd.csv"
COMBINED_FILE = "combined.csv"
PLAYER_INFO_FILE = "player_info.csv"
RESULTS_FILE = "prediction_results.csv"
ANALYSIS_FILE = "overall_results_grouped.csv"
COMBINED_FILE = "combined.csv"
PLAYER_LOGS = "player_logs.csv"


if __name__ == "__main__":
    
    if len(DATES) != 0:
        print("collecting season data")
        df = get_player_log_df()

    for DATE in DATES:
        print(f"\n\nworking on {DATE}")

        prediction_dir = f"prediction-{DATE}"

        dir_player_log = f"{prediction_dir}/{PLAYER_LOGS}"
        dir_pred_file = f"{prediction_dir}/{PREDICTIONS}"
        dir_props_file = f"{prediction_dir}/{PROPS_FILE}"
        dir_combined_file = f"{prediction_dir}/{COMBINED_FILE}"

        next_game_pred(dir_player_log, dir_pred_file)

        print("next game predicted")

        combine_props_pred_files(dir_props_file, dir_pred_file, dir_combined_file)

        print("props and predictions combined")


        dir_results_file = f"{prediction_dir}/{RESULTS_FILE}"

        print("data collected, getting logs by date")
        get_player_logs_on_date(f"{prediction_dir}/{COMBINED_FILE}", df, DATE).to_csv(dir_results_file, index=False)


        print("logs collected, calculating results")

        append_game_result(dir_results_file).to_csv(dir_results_file, index=False)

        print("results calculated, calculating success")

        res = count_success(dir_results_file, DATE)

        print(res)

        add_to_analysis(ANALYSIS_FILE, res)

        print(f"success rate added to {ANALYSIS_FILE}")

