import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

# Load the dataset
data = pd.read_csv("filtered_player_data_2.csv")

# Prepare features and target variables
features = data[
    [
        "Tm",
        "Opp",
        "Place",
        "Points_Running_Avg",
        "Rebounds_Running_Avg",
        "Assists_Running_Avg",
    ]
].fillna("Unknown")
targets = data[["PTS", "TRB", "AST"]]

# OneHotEncoder for categorical variables
encoder = OneHotEncoder(sparse=False)
encoded_features = encoder.fit_transform(features[["Tm", "Opp", "Place"]])

# Combine encoded categorical features with numerical features
numerical_features = features[
    ["Points_Running_Avg", "Rebounds_Running_Avg", "Assists_Running_Avg"]
].to_numpy()
X = np.hstack([numerical_features, encoded_features])

# Split the data into training and testing sets
X_train, X_test, y_train_pts, y_test_pts = train_test_split(
    X, targets["PTS"], test_size=0.2, random_state=42
)
_, _, y_train_trb, y_test_trb = train_test_split(
    X, targets["TRB"], test_size=0.2, random_state=42
)
_, _, y_train_ast, y_test_ast = train_test_split(
    X, targets["AST"], test_size=0.2, random_state=42
)

# Train LinearRegression models
model_points = LinearRegression().fit(X_train, y_train_pts)
model_rebounds = LinearRegression().fit(X_train, y_train_trb)
model_assists = LinearRegression().fit(X_train, y_train_ast)


# Prediction function
def predict_player_performance_auto(player_name, team, opponent, place):
    # Use the last observed running averages for simplicity
    player_data = data[data["Player"] == player_name]
    if player_data.empty:
        return "Player data not available"

    points_running_avg = player_data.iloc[-1]["Points_Running_Avg"]
    rebounds_running_avg = player_data.iloc[-1]["Rebounds_Running_Avg"]
    assists_running_avg = player_data.iloc[-1]["Assists_Running_Avg"]

    # Prepare input data
    input_features_df = pd.DataFrame(
        {
            "Tm": [team],
            "Opp": [opponent],
            "Place": [place],
            "Points_Running_Avg": [points_running_avg],
            "Rebounds_Running_Avg": [rebounds_running_avg],
            "Assists_Running_Avg": [assists_running_avg],
        }
    )

    # Transform input data using fitted encoder
    encoded_input = encoder.transform(input_features_df[["Tm", "Opp", "Place"]])
    numerical_input = input_features_df[
        ["Points_Running_Avg", "Rebounds_Running_Avg", "Assists_Running_Avg"]
    ].to_numpy()
    X_input = np.hstack([numerical_input, encoded_input])

    # Make predictions
    predicted_points = model_points.predict(X_input)[0]
    predicted_rebounds = model_rebounds.predict(X_input)[0]
    predicted_assists = model_assists.predict(X_input)[0]

    return {
        "Player": player_name,
        "Predicted Points": predicted_points,
        "Predicted Rebounds": predicted_rebounds,
        "Predicted Assists": predicted_assists,
    }


def predict_performance_from_input():
    player_name = input("Enter player name: ")
    team = input("Enter player's team: ")
    opponent = input("Enter opponent team: ")
    place = input("Enter game location (Home/Away): ")
    
    prediction = predict_player_performance_auto(player_name, team, opponent, place)
    print(prediction)

# Call the function to prompt user input and predict performance
predict_performance_from_input()
