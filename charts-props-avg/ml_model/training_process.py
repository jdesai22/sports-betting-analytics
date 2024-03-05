import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
import joblib

# Load the dataset
data_path = "filtered_player_data_2.csv"
data = pd.read_csv(data_path)

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
X_train, _, y_train_pts, _ = train_test_split(
    X, targets["PTS"], test_size=0.2, random_state=42
)
_, _, y_train_trb, _ = train_test_split(
    X, targets["TRB"], test_size=0.2, random_state=42
)
_, _, y_train_ast, _ = train_test_split(
    X, targets["AST"], test_size=0.2, random_state=42
)

# Train LinearRegression models
model_points = LinearRegression().fit(X_train, y_train_pts)
model_rebounds = LinearRegression().fit(X_train, y_train_trb)
model_assists = LinearRegression().fit(X_train, y_train_ast)

# Save the encoder and models
joblib.dump(encoder, "encoder.joblib")
joblib.dump(model_points, "model_points.joblib")
joblib.dump(model_rebounds, "model_rebounds.joblib")
joblib.dump(model_assists, "model_assists.joblib")
