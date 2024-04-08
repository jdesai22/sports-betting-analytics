from utils.evaluate import *

DATES = ["2024-04-05", "2024-04-06"]
RESULTS_FILE = "prediction_results.csv"
ANALYSIS_FILE = "overall_results.csv"
COMBINED_FILE = "combined.csv"

if __name__ == "__main__":

    if len(DATES) != 0:
        print("collecting season data")
        df = get_player_log_df()

    for DATE in DATES:
        print(f"\n\nworking on {DATE}")

        prediction_dir = f"prediction-{DATE}"

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




