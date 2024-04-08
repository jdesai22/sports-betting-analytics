import pandas as pd


# DATES = ["2024-03-27", "2024-03-28", "2024-03-29", "2024-03-30", "2024-03-31", "2024-04-01", "2024-04-02", "2024-04-03", "2024-04-04", "2024-04-05", "2024-04-06"]
DATES = ["2024-04-05"]
PREDICTIONS = "predictions.csv"
PROPS_FILE = "odd.csv"
COMBINED_FILE = "combined.csv"
PLAYER_INFO_FILE = "player_info.csv"
RESULTS_FILE = "prediction_results.csv"
ANALYSIS_FILE = "overall_results_grouped.csv"
COMBINED_FILE = "combined.csv"
PLAYER_LOGS = "player_logs.csv"


if __name__ == "__main__":

    for DATE in DATES:
        print(f"\n\nworking on {DATE}")

        prediction_dir = f"prediction-{DATE}"

        res_file = f"{prediction_dir}/{RESULTS_FILE}"

        # Open CSV file as DataFrame
        df = pd.read_csv(res_file)
        
        # Calculate the sum of differences in PTS and points_under_line
        df_under = df[df['PTS_np'] == "under"]
        sum_diff = (df_under['PTS'] - df_under['player_points_under_line']).sum()

        df_over = df[df['PTS_np'] == "over"]
        sum_diff_over = (df_over['player_points_over_line'] - df_over['PTS']).sum()

        #df.to_csv("testing.csv", index=False)
        df_over.to_csv("testing.csv", index=False)

        # Print the sum
        print(f"Sum of under differences: {sum_diff}")
        print(f"Sum of over difference: {sum_diff_over}")
        