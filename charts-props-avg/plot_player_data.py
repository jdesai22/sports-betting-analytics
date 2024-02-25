import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Load the dataset
data = pd.read_csv('filtered_player_data.csv')

# Function to plot data for a selected player using Plotly
def plot_player_data_plotly(player_name):
    # Filter data for the selected player
    player_data = data[data['Player'] == player_name]
    
    # Ensure the Date column is in datetime format for plotting
    player_data['Date'] = pd.to_datetime(player_data['Date'])

    # Create a figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(go.Scatter(x=player_data['Date'], y=player_data['PTS'], name='PTS', mode='markers+lines', marker=dict(size=10)), secondary_y=False)
    fig.add_trace(go.Scatter(x=player_data['Date'], y=player_data['Points_Running_Avg'], name='Points_Running_Avg', mode='markers+lines', marker=dict(size=10)), secondary_y=False)
    fig.add_trace(go.Scatter(x=player_data['Date'], y=player_data['player_points_line'], name='player_points_line', mode='markers+lines', marker=dict(size=10)), secondary_y=False)

    # Add figure title
    fig.update_layout(title_text=f"Interactive Data for {player_name}")

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="Points", secondary_y=False)

    # Show plot
    fig.show()

# Example usage
player_name = input("Enter a player's name: ")
plot_player_data_plotly(player_name)
