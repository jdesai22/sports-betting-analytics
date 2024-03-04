import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

# Load the dataset
data = pd.read_csv("filtered_player_data_2.csv")

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
        rows=3,
        cols=1,
        subplot_titles=("Points Over Time", "Rebounds Over Time", "Assists Over Time"),
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

    # Add Rebounds
    for column, name in zip(
        ["TRB", "Rebounds_Running_Avg", "player_rebounds_line"],
        ["TRB", "Rebounds Running Avg", "Player Rebounds Line"],
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
            row=2,
            col=1,
        )

    # Add Assists
    for column, name in zip(
        ["AST", "Assists_Running_Avg", "player_assists_line"],
        ["AST", "Assists Running Avg", "Player Assists Line"],
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
            row=3,
            col=1,
        )

    # Calculate the regression line
    x = player_data["Points_Running_Avg"]
    y = player_data["player_points_line"]
    slope, intercept = np.polyfit(x, y, 1)
    # line = slope * x + intercept

    x2 = player_data["Rebounds_Running_Avg"]
    y2 = player_data["player_rebounds_line"]
    slope2, intercept2 = np.polyfit(x, y, 1)

    x3 = player_data["Assists_Running_Avg"]
    y3 = player_data["player_assists_line"]
    slope3, intercept3 = np.polyfit(x, y, 1)

    # Calculate the correlation coefficient
    correlation_coefficient = np.corrcoef(
        player_data["Points_Running_Avg"], player_data["player_points_line"]
    )[0, 1]

    correlation_coefficient2 = np.corrcoef(
        player_data["Rebounds_Running_Avg"], player_data["player_rebounds_line"]
    )[0, 1]

    correlation_coefficient3 = np.corrcoef(
        player_data["Assists_Running_Avg"], player_data["player_assists_line"]
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
        opacity=1.0,
    )

    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=1,
        y=10,  # Adjust these values to position your annotation
        text=f"Correlation: {correlation_coefficient2:.2f}",
        showarrow=False,
        font=dict(size=14, color="black"),
        align="right",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        bgcolor="white",
        opacity=1.0,
    )

    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=1,
        y=20,  # Adjust these values to position your annotation
        text=f"Correlation: {correlation_coefficient3:.2f}",
        showarrow=False,
        font=dict(size=14, color="black"),
        align="right",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        bgcolor="white",
        opacity=1.0,
    )

    # Update layout for clarity
    # fig.update_layout(height=800, hovermode="closest")
    # fig.update_xaxes(
    #     title_text="Date",
    #     row=1,
    #     col=1,
    #     gridcolor="rgba(188,188,188, 1)",
    # )
    # fig.update_yaxes(
    #     title_text="Points, Running Average, Prop Line",
    #     row=1,
    #     col=1,
    #     gridcolor="rgba(188,188,188, 1)",
    # )

    fig.update_layout(height=1200, hovermode="closest", showlegend=False)
    fig.update_xaxes(title_text="Date", tickangle=-45)
    fig.update_yaxes(
        title_text="Points",
        row=1,
        col=1,
        gridcolor="rgba(188,188,188, 1)",
    )
    fig.update_yaxes(
        title_text="Rebounds",
        row=2,
        col=1,
        gridcolor="rgba(188,188,188, 1)",
    )
    fig.update_yaxes(
        title_text="Assists",
        row=3,
        col=1,
        gridcolor="rgba(188,188,188, 1)",
    )

    # Update layout for a responsive design and to match the web aesthetics
    fig.update_layout(
        autosize=True,
        plot_bgcolor="rgba(230, 230, 230, 1)",
        paper_bgcolor="rgba(230, 230, 230, 1)",
        legend_bgcolor="rgba(230, 230, 230, 1)",
        font=dict(family="Arial, sans-serif", size=12, color="#333"),
        margin=dict(l=70, r=50, b=85, t=0, pad=0),
    )

    return fig.to_html(
        full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}
    )
