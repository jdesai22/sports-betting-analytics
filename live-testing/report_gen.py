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
    pdf.set_fill_color(255, 255, 255)  # Default background color
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

    # Column headers and widths adjustment
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
    column_widths = [40, 20, 25, 35, 40, 25, 45, 25]
    for i, title in enumerate(column_titles):
        pdf.cell(column_widths[i], 10, title, border=1)

    pdf.ln(10)

    # Table rows with color coding for Prediction Success
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
            if column_titles[i] == "Prediction Success":
                if data == "Yes":
                    pdf.set_fill_color(144, 238, 144)  # Light green
                else:
                    pdf.set_fill_color(255, 99, 71)  # Light red
                pdf.cell(
                    column_widths[i], 10, data, border=1, ln=0, align="C", fill=True
                )
            else:
                pdf.set_fill_color(
                    255, 255, 255
                )  # Reset to default background color for other cells
                pdf.cell(
                    column_widths[i], 10, data, border=1, ln=0, align="C", fill=True
                )
        pdf.ln(10)

    # Save PDF
    pdf.output(pdf_file_path)


DATES = ["2024-03-27", "2024-03-28", "2024-03-29", "2024-03-30", "2024-03-31", "2024-04-01", "2024-04-02", "2024-04-03", "2024-04-04", "2024-04-05", "2024-04-06"]
#DATES = ["2024-03-27"]
RESULTS_FILE = "prediction_results.csv"




if __name__ == "__main__":
    
    for DATE in DATES:
        print(f"\n\nworking on {DATE}")

        prediction_dir = f"prediction-{DATE}"

        res_file = f"{prediction_dir}/{RESULTS_FILE}"


        # Example usage
        csv_file_path = (res_file)
        pdf_file_path = f"{prediction_dir}/summary-{DATE}.pdf"  # Replace with your desired PDF file path

        generate_pdf(csv_file_path, pdf_file_path)
