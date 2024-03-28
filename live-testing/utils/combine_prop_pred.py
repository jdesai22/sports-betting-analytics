import pandas as pd


def combine_props_pred_files(odds_file, pred_file, combined_file):
    # Read the first file
    odds = pd.read_csv(odds_file)

    # Read the second file
    preds = pd.read_csv(pred_file)


    # Perform the join operation
    merged_data = pd.merge(odds, preds, left_on='Player', right_on='PLAYER_NAME')

    # Rename the GAME_DATE column to LAST_GAME
    merged_data.rename(columns={'GAME_DATE': 'LAST_GAME'}, inplace=True)
    merged_data.rename(columns={'Date': 'PROPS_DATE'}, inplace=True)

    # Remove the Player column
    merged_data.drop('PLAYER_NAME', axis=1, inplace=True)

    merged_data = merged_data[['Player', 'TEAM_ABBREVIATION', 'PTS_np', 'player_points_over_book', 'player_points_over_line', 'player_points_over', 'player_points_under_book', 'player_points_under_line', 'player_points_under', 'PROPS_DATE', 'LAST_GAME']]


    merged_data.to_csv(combined_file, index=False)