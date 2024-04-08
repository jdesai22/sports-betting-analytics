from nba_api.stats.endpoints import playercareerstats, playergamelogs
from nba_api.stats.static import players
from replace_accents import replace_accents_characters


import pandas as pd
import time



# pandas data frames (optional: pip install pandas)

def get_player_szn_stats(pid):

    career = playercareerstats.PlayerCareerStats(pid) 

    df = career.get_data_frames()[0]


    df_selected = df[df['SEASON_ID'] == '2023-24']

    df_selected = df_selected[['PLAYER_ID', 'GP', 'PTS', 'REB', 'AST']]
    df_selected['PPG'] = df_selected['PTS'] / df_selected['GP']
    df_selected['RPG'] = df_selected['REB'] / df_selected['GP']
    df_selected['APG'] = df_selected['AST'] / df_selected['GP']

    return df_selected

def get_player_logs(player_log_file, player_info_file):
    gl = playergamelogs.PlayerGameLogs(    
        # player_id_nullable=pid,
        season_nullable="2023-24",
        #last_n_games_nullable='82'
    )

    df = gl.get_data_frames()[0]

    df_selected = df[['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'PTS', 'REB', 'AST']]

    # Read the player_info.csv file to filter players
    player_info = pd.read_csv(player_info_file)

    player_info['Player'] = player_info['Player'].apply(replace_accents_characters)

    df_selected = df_selected[df_selected['PLAYER_NAME'].isin(player_info['Player'])]


    df_selected = df_selected.sort_values(['TEAM_ABBREVIATION', 'PLAYER_NAME', 'GAME_DATE'], ascending=[True, True, True])

    df_selected.to_csv(player_log_file, index=False)

    return df_selected

#get_player_logs().to_csv("player_logs.csv", index=False)


def get_player_ids():
    # Open the csv file
    player_info = pd.read_csv('player_info.csv')
    # Keep only the desired columns
    player_info = player_info[['team', 'player_link', 'Rk', 'Player', 'Position']]

    # Iterate through each row in the dataframe
    for index, row in player_info.iterrows():
        player_name = row['Player']

        player_name = replace_accents_characters(player_name)
         
        # Find players by full name
        players_found = players.find_players_by_full_name(player_name)
        
        # Filter for active players
        active_players = [player for player in players_found if player['is_active']]
        if active_players:
            # Take the first active player
            active_player = active_players[0]

            # Get the player id
            player_id = int(active_player['id'])

            # Add the player_id to the row in player_info dataframe
            player_info.at[index, 'player_id'] = int(player_id)

    # Export the modified dataframe back to the csv file
    player_info.to_csv('player_info.csv', index=False)


def calc_running_avgs(player_log_file):
    df = pd.read_csv(player_log_file)

    # Calculate running averages for each player and round to 3 decimal places
    df['PTS_ra'] = (df.groupby('PLAYER_NAME')['PTS'].cumsum() / (df.groupby('PLAYER_NAME')['PTS'].cumcount() + 1)).round(3)
    df['REB_ra'] = (df.groupby('PLAYER_NAME')['REB'].cumsum() / (df.groupby('PLAYER_NAME')['REB'].cumcount() + 1)).round(3)
    df['AST_ra'] = (df.groupby('PLAYER_NAME')['AST'].cumsum() / (df.groupby('PLAYER_NAME')['AST'].cumcount() + 1)).round(3)

    # Calculate differences for each player and round to 3 decimal places
    df['PTS_d'] = (df['PTS'] - df['PTS_ra']).round(3)
    df['REB_d'] = (df['REB'] - df['REB_ra']).round(3)
    df['AST_d'] = (df['AST'] - df['AST_ra']).round(3)

    df.to_csv(player_log_file, index=False)

    return df


def calc_std(player_log_file):
    # Group the data by Player column

    data = pd.read_csv(player_log_file)

    grouped_data = data.groupby('PLAYER_NAME')

    # Calculate the standard deviation of Points_Running_Avg, Rebounds_Running_Avg, and Assists_Running_Avg
    std_points = round(grouped_data['PTS'].std(), 5)
    std_rebounds = round(grouped_data['REB'].std(), 5)
    std_assists = round(grouped_data['AST'].std(), 5)

    # Create new columns for the standard deviation of each
    data['PTS_std'] = data['PLAYER_NAME'].map(std_points)
    data['REB_std'] = data['PLAYER_NAME'].map(std_rebounds)
    data['AST_std'] = data['PLAYER_NAME'].map(std_assists)


    data.to_csv(player_log_file, index=False)

    return data

def calc_z_scores(player_log_file):
    # Read the stdev.csv file
    data = pd.read_csv(player_log_file)

    # Calculate the z-score for PTS
    data['PTS_z'] = round((data['PTS'] - data['PTS_ra']) / data['PTS_std'], 5)

    # Calculate the z-score for TRB
    data['REB_z'] = round((data['REB'] - data['REB_ra']) / data['REB_std'], 5)

    # Calculate the z-score for AST
    data['AST_z'] = round((data['AST'] - data['AST_ra']) / data['AST_std'], 5)


    data.to_csv(player_log_file, index=False)

    return data

def next_game_pred(player_log_file, prediction_file):
    df = pd.read_csv(player_log_file)

    z_thresh_map = {
        'over_g25_fade' : 1.7,
        'over_u25_over' : 1.4,
        'under_all' : -0.5
    }
    
    
    df = df.drop_duplicates(subset='PLAYER_NAME', keep='last')
    
    df['PTS_np'] = 'NA'
    df.loc[(df['PTS_ra'] > 25) & (df['PTS_z'] > z_thresh_map['over_g25_fade']), 'PTS_np'] = 'under'
    df.loc[(df['PTS_ra'] < 25) & (df['PTS_z'] > z_thresh_map['over_u25_over']), 'PTS_np'] = 'over'
    df.loc[df['PTS_z'] < z_thresh_map['under_all'], 'PTS_np'] = 'under'
    
    df['pred_type'] = 'NA'
    df.loc[(df['PTS_ra'] > 25) & (df['PTS_z'] > z_thresh_map['over_g25_fade']), 'pred_type'] = 'fade star players'
    df.loc[(df['PTS_ra'] < 25) & (df['PTS_z'] > z_thresh_map['over_u25_over']), 'pred_type'] = 'over momentum on non-star players'
    df.loc[df['PTS_z'] < z_thresh_map['under_all'], 'pred_type'] = 'under momentum'


    df = df[df['PTS_np'] != 'NA']
    df = df[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'PTS_np', 'pred_type', 'GAME_DATE']]

    df.to_csv(prediction_file, index=False)

    return df

def calculate_player_log_file(player_log_file_name, prediction_file, player_info_file):
    PLAYER_LOG_FILE = player_log_file_name
    PREDICTIONS = prediction_file

    print("getting player logs")
    get_player_logs(PLAYER_LOG_FILE, player_info_file)
    print("player logs updated")

    print("calculating running averages")
    calc_running_avgs(PLAYER_LOG_FILE)
    print("running avgs calculated")

    print("calculating stdevs")
    calc_std(PLAYER_LOG_FILE)
    print("stdevs calculated")

    print("calculating z-scores")
    calc_z_scores(PLAYER_LOG_FILE)
    print("z-scores calculated")

    print("making predictions")
    next_game_pred(PLAYER_LOG_FILE, PREDICTIONS)
    print("predictions made")



if __name__ == "__main__":
    calculate_player_log_file("player_logs.csv")
    print("placeholder")


