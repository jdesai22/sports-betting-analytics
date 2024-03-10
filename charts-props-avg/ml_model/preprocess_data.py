import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import torch
from torch.utils.data import DataLoader, TensorDataset

# Load your data
data = pd.read_csv("filtered_player_data_2.csv")

# Define your features and target variables here
features = data[['Tm', 'Opp', 'Place', 'Points_Running_Avg', 'Rebounds_Running_Avg', 'Assists_Running_Avg']]
targets = data[['PTS', 'TRB', 'AST']]

# Adjusted preprocessing steps
preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), ['Points_Running_Avg', 'Rebounds_Running_Avg', 'Assists_Running_Avg']),
    ('cat', OneHotEncoder(), ['Tm', 'Opp', 'Place'])
])


X_processed = preprocessor.fit_transform(features)
y = targets.values

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Convert to PyTorch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

# Create DataLoader for training
train_data = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)