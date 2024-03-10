import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
# Assuming preprocess_data.py creates a function 'get_data_loaders' that returns train_loader, X_test, and y_test
from preprocess_data import get_data_loaders

# Model definition
class PredModel(nn.Module):
    def __init__(self, in_features, hidden_size, out_features):
        super(PredModel, self).__init__()
        self.layer1 = nn.Linear(in_features, hidden_size)
        self.layer2 = nn.Linear(hidden_size, out_features)
    
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = self.layer2(x)
        return x

# Load and preprocess data
train_loader, X_test, y_test = get_data_loaders()

# Initialize model
in_features = X_test.shape[1] # Assuming X_test is a tensor
hidden_size = 64 # Example size
out_features = 3 # Predicting PTS, TRB, AST
num_epochs = 100

model = PredModel(in_features, hidden_size, out_features)

# Model training
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

for epoch in range(num_epochs):
    for X_batch, y_batch in train_loader:
        # Forward pass
        y_pred = model(X_batch)
        
        # Compute loss
        loss = criterion(y_pred, y_batch)
        
        # Backward pass and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    print(f'Epoch {epoch}, Loss: {loss.item()}')

# Model evaluation
model.eval()
with torch.no_grad():
    predictions = model(X_test)
    loss = criterion(predictions, y_test)

print(f'Test Loss: {loss.item()}')

# Print final predictions
print("Final Predictions:\n", predictions)