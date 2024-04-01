from nba_api.stats.endpoints import playergamelogs
import pandas as pd
import datetime

def get_player_log_df():
    gl = playergamelogs.PlayerGameLogs(    
        # player_id_nullable=pid,
        season_nullable="2023-24",
        #last_n_games_nullable='82'
    )

    df = gl.get_data_frames()[0]

    return df

def get_player_logs_on_date(predictions_file, df, date):
    date_param = f"{date}T00:00:00"

    df_selected = df[df['GAME_DATE'] == date_param]

    df_selected = df_selected[['PLAYER_ID', 'PLAYER_NAME', 'GAME_DATE', 'PTS', 'REB', 'AST']]

    # Read the predictions file to filter players
    predictions_file = pd.read_csv(predictions_file)
    predictions_file.rename(columns={'Player': 'PLAYER_NAME'}, inplace=True)

    df_selected = pd.merge(df_selected, predictions_file, on='PLAYER_NAME', how='inner')

    
    return df_selected

def append_game_result(results_file):
    res = pd.read_csv(results_file)

    # Check if PTS_np is over res.apply(lambda row: 'over' if row['PTS_np'] == 'over' else 'under', axis=1)
    res['RES'] = "NA"

    # Check if PTS is greater than player_points_over_line or player_points_under_line
    res.loc[(res['PTS_np'] == 'over') & (res['PTS'] > res['player_points_over_line']), 'RES'] = 'over'
    res.loc[(res['PTS_np'] == 'over') & (res['PTS'] <= res['player_points_over_line']), 'RES'] = 'under'
    res.loc[(res['PTS_np'] == 'under') & (res['PTS'] > res['player_points_under_line']), 'RES'] = 'over'
    res.loc[(res['PTS_np'] == 'under') & (res['PTS'] <= res['player_points_under_line']), 'RES'] = 'under'

    return res

def count_success(results_file, date):
    res = pd.read_csv(results_file)

    count_over_correct = len(res[(res['PTS_np'] == 'over') & (res['RES'] == 'over')])
    count_over_predicted = len(res[res['PTS_np'] == 'over'])

    count_under_correct = len(res[(res['PTS_np'] == 'under') & (res['RES'] == 'under')])
    count_under_predicted = len(res[res['PTS_np'] == 'under'])

    count_total_rows = len(res)

    return (
        {
            f"{date}" : {
                "over_correct" : count_over_correct,
                "over_predicted" : count_over_predicted,
                "under_correct" : count_under_correct,
                "under_predicted" : count_under_predicted,
                "total_predicted" : count_total_rows
            }
        }
    )

def add_to_analysis(analysis_file, res):
    res_df = pd.DataFrame(res).transpose()
    res_df.to_csv(analysis_file, mode='a', header=False, index_label='date')

    df = pd.read_csv(analysis_file)
    df.drop_duplicates(inplace=True)
    df = df[['date', 'over_correct', 'over_predicted', 'under_correct', 'under_predicted', 'total_predicted']]
    df.to_csv(analysis_file, index=False)


def testing():
    # DATE = "2024-03-29"
    # RESULTS_FILE = "testing.csv"
    # TESTING_EVAL_FILE = "testingpt2.csv"
    # analysis_file = "results.csv"

    # df = get_player_log_df()

    # get_player_logs_on_date(f"prediction-{DATE}/combined.csv", df, DATE).to_csv(RESULTS_FILE, index=False)
    
    # append_game_result(RESULTS_FILE).to_csv(TESTING_EVAL_FILE, index=False)

    # res = count_success(TESTING_EVAL_FILE, DATE)

    # add_to_analysis(analysis_file, res)

    # print(res)

    print("place holder")
