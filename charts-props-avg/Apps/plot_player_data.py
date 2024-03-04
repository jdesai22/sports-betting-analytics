import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

# Load the dataset
data = pd.read_csv("filtered_player_data.csv")

# Ensure the Date column is in datetime format
data["Date"] = pd.to_datetime(data["Date"])


def plot_player_data_plotly(player_name):
    # Filter data for the selected player
    player_data = data[data["Player"] == player_name]

    # Assuming player_data already has an 'Opp' column after merging with the necessary data
    hover_text = player_data.apply(
        lambda x: (
            f"Away vs. {x['Opp']}"
            if pd.notna(x["Place"]) and "Away" in x["Place"]
            else f"Home vs. {x['Opp']}" if pd.notna(x["Opp"]) else "Info Not Available"
        ),
        axis=1,
    )

    # Create figure with secondary y-axis for the correlation plot
    fig = make_subplots(
        rows=1, cols=1, subplot_titles=(f"Game Performance Over Time for {player_name}")
    )

    # Add PTS, Points_Running_Avg, player_points_line traces
    for column, name in zip(
        ["PTS", "Points_Running_Avg", "player_points_line"],
        ["PTS", "Points Running Avg", "Player Points Line"],
    ):
        fig.add_trace(
            go.Scatter(
                x=player_data["Date"],
                y=player_data[column],
                mode="markers+lines",
                name=name,
                text=hover_text,
                hoverinfo="text+y+x",
            ),
            row=1,
            col=1,
        )

    # Calculate the regression line
    x = player_data["Points_Running_Avg"]
    y = player_data["player_points_line"]
    slope, intercept = np.polyfit(x, y, 1)
    line = slope * x + intercept

    # Calculate the correlation coefficient
    correlation_coefficient = np.corrcoef(
        player_data["Points_Running_Avg"], player_data["player_points_line"]
    )[0, 1]

    # Adding the correlation coefficient as a text annotation
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=1,
        y=1,  # Adjust these values to position your annotation
        text=f"Correlation: {correlation_coefficient:.2f}",
        showarrow=False,
        font=dict(size=14, color="black"),
        align="right",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        bgcolor="white",
        opacity=0.8,
    )

    # Update layout for clarity
    fig.update_layout(height=800, hovermode="closest")
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="Points, Running Average, Prop Line", row=1, col=1)

    return fig.to_html(full_html=False)
