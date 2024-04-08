import pandas as pd
from fpdf import FPDF


def calculate_units_made(row):
    if row["PTS_np"] == "over" and row["RES"] == "over":
        return row["player_points_over"] - 1
    elif row["PTS_np"] == "under" and row["RES"] == "under":
        return row["player_points_under"] - 1
    return -1


def generate_pdf(csv_file_path, pdf_file_path):
    # Load data
    data = pd.read_csv(csv_file_path)

    # Calculate additional columns
    data["Units Made"] = data.apply(calculate_units_made, axis=1)
    data["Prediction Success"] = data.apply(
        lambda x: "Yes" if x["PTS_np"] == x["RES"] else "No", axis=1
    )

    # Calculate stats
    accuracy = (data["Prediction Success"] == "Yes").mean() * 100
    units_up = data["Units Made"].sum()

    # Setup PDF
    pdf = FPDF(orientation="L")
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(
        0, 10, "NBA Player Predictions, Results, Units Made, and Points Line", 0, 1, "C"
    )
    pdf.ln(10)

    # Summary
    pdf.set_font("Arial", size=12)
    pdf.cell(
        0, 10, f"Accuracy: {accuracy:.2f}%, Total Units Up: {units_up:.2f}", 0, 1, "C"
    )
    pdf.ln(10)

    # Column headers
    column_titles = [
        "Player Name",
        "Team",
        "Prediction",
        "Actual Points",
        "Player Points Line",
        "Result",
        "Prediction Success",
        "Units Made",
    ]
    column_widths = [40, 20, 25, 25, 30, 25, 35, 25]
    for i, title in enumerate(column_titles):
        pdf.cell(column_widths[i], 10, title, border=1)

    pdf.ln(10)

    # Table rows
    for _, row in data.iterrows():
        pdf.set_font("Arial", size=10)
        row_data = [
            row["PLAYER_NAME"],
            row["TEAM_ABBREVIATION"],
            row["PTS_np"],
            str(row["PTS"]),
            str(row["player_points_over_line"]),
            row["RES"],
            row["Prediction Success"],
            f"{row['Units Made']:.2f}",
        ]
        for i, data in enumerate(row_data):
            pdf.cell(column_widths[i], 10, data, border=1)
        pdf.ln(10)

    # Save PDF
    pdf.output(pdf_file_path)


# Example usage
csv_file_path = (
    "prediction-2024-03-27/prediction_results.csv"  # Replace with your CSV file path
)
pdf_file_path = "prediction-2024-03-27/prediction_results.pdf"  # Replace with your desired PDF file path
generate_pdf(csv_file_path, pdf_file_path)
