
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Load the dataset
data = pd.read_csv('filtered_player_data.csv')

# Ensure the Date column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

def plot_player_data_plotly(player_name):
    # Filter data for the selected player
    player_data = data[data['Player'] == player_name]
    
    # Prepare the hover text with Place and Opponent information
    hover_text = player_data.apply(lambda x: f"{x['Place']} vs. {x['Opp']}" if pd.notna(x['Place']) else 'N/A', axis=1)
    
    # Create figure with secondary y-axis for the regression plot
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Game Performance Over Time', 'Regression Analysis'))

    # Add PTS, Points_Running_Avg, player_points_line traces with hover info
    for column, name in zip(['PTS', 'Points_Running_Avg', 'player_points_line'], ['PTS', 'Points Running Avg', 'Player Points Line']):
        fig.add_trace(
            go.Scatter(x=player_data['Date'], y=player_data[column], mode='markers+lines', name=name, text=hover_text, hoverinfo='text+y+x'),
            row=1, col=1
        )
    
    # Prepare the data for regression analysis
    X = player_data['Points_Running_Avg']
    X = sm.add_constant(X) # adding a constant for intercept
    y = player_data['player_points_line']

    # Perform the regression analysis
    model = sm.OLS(y, X).fit()
    predictions = model.predict(X) # make the predictions by the model

    # Add regression line trace
    fig.add_trace(
        go.Scatter(x=player_data['Points_Running_Avg'], y=predictions, mode='lines', name='Regression Line'),
        row=2, col=1
    )

    # Add scatter trace for the actual data points
    fig.add_trace(
        go.Scatter(x=player_data['Points_Running_Avg'], y=player_data['player_points_line'], mode='markers', name='Data Points'),
        row=2, col=1
    )

    # Add R-squared and p-value to the plot as annotations
    fig.add_annotation(text=f'R-squared: {model.rsquared:.2f}', xref='paper', yref='paper', x=0.05, y=0.95, showarrow=False, row=2, col=1)
    fig.add_annotation(text=f'p-value: {model.f_pvalue:.4f}', xref='paper', yref='paper', x=0.05, y=0.90, showarrow=False, row=2, col=1)
    fig.add_annotation(text=f'Standard Error: {model.bse[1]:.4f}', xref='paper', yref='paper', x=0.05, y=0.85, showarrow=False, row=2, col=1)

    # Update layout for clarity
    fig.update_layout(height=800, hovermode='closest')
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Points Running Avg", row=2, col=1)
    fig.update_yaxes(title_text="Points", row=1, col=1)
    fig.update_yaxes(title_text="Player Points Line", row=2, col=1)

    # Show plot
    fig.show()

# Example usage
player_name = input("Enter a player's name: ")
plot_player_data_plotly(player_name)
