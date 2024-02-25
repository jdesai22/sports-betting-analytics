import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

# Load the dataset
data = pd.read_csv('filtered_player_data.csv')

# Function to plot data for a selected player
def plot_player_data(player_name):
    # Filter data for the selected player
    player_data = data[data['Player'] == player_name]
    
    # Convert Date to datetime for plotting
    player_data['Date'] = pd.to_datetime(player_data['Date'])
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    line1, = ax.plot(player_data['Date'], player_data['PTS'], label='PTS', marker='o')
    line2, = ax.plot(player_data['Date'], player_data['Points_Running_Avg'], label='Points_Running_Avg', marker='o')
    line3, = ax.plot(player_data['Date'], player_data['player_points_line'], label='player_points_line', marker='o')
    
    # Formatting the plot
    plt.title(f'Data for {player_name}')
    plt.xlabel('Date')
    plt.ylabel('Points')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Adding interactive cursors
    mplcursors.cursor([line1, line2, line3], hover=True)
    
    # Display the plot
    plt.show()

# Example usage
player_name = input("Enter a player's name: ")
plot_player_data(player_name)
