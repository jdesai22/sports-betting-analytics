import pandas as pd
from fpdf import FPDF


# DATES = ["2024-03-27", "2024-03-28", "2024-03-29", "2024-03-30", "2024-03-31", "2024-04-01", "2024-04-02", "2024-04-03", "2024-04-04", "2024-04-05", "2024-04-06"]
DATES = ["2024-03-27"]
PREDICTIONS = "predictions.csv"
PROPS_FILE = "odd.csv"
COMBINED_FILE = "combined.csv"
PLAYER_INFO_FILE = "player_info.csv"
RESULTS_FILE = "prediction_results.csv"
ANALYSIS_FILE = "overall_results_grouped.csv"
COMBINED_FILE = "combined.csv"
PLAYER_LOGS = "player_logs.csv"



class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Player Stats", 0, 1, "C")
        self.ln(8)

    def footer(self):
        # Set up the footer
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        # Set up the chapter title
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(10)

    # Define a class for PDF generation
    def chapter_body(self, df):
        # Set up the chapter body
        self.set_font("Arial", "", 10)
        # Add table headers
        headers = ["Player", "Team", "Points", "Prediction Type", "Prediction", "Result"]
        col_width = self.w / len(headers)  # Calculate column width based on number of headers
        for header in headers:
            self.cell(col_width, 10, header, 1, 0, "C")
        self.ln()
        # Add table rows
        for index, row in df.iterrows():
            self.cell(col_width, 10, str(row['PLAYER_NAME']), 1, 0, "C")
            self.cell(col_width, 10, str(row['TEAM_ABBREVIATION']), 1, 0, "C")
            self.cell(col_width, 10, str(row['PTS']), 1, 0, "C")
            self.cell(col_width, 10, str(row['pred_type']), 1, 0, "C")
            self.cell(col_width, 10, str(row['PTS_np']), 1, 0, "C")
            self.cell(col_width, 10, str(row['RES']), 1, 0, "C")
            self.ln()
        self.ln(10)


if __name__ == "__main__":

    for DATE in DATES:
        print(f"\n\nworking on {DATE}")

        prediction_dir = f"prediction-{DATE}"

        res_file = f"{prediction_dir}/{RESULTS_FILE}"

        # Open CSV file as DataFrame
        df = pd.read_csv(res_file)
        
        df = df[["PLAYER_NAME", "TEAM_ABBREVIATION", "PTS", "pred_type", "PTS_np", "RES"]]

        # Generate PDF
            # Create a PDF object
        pdf = PDF()
        pdf.add_page()

        # Add the chapter title
        pdf.chapter_title("Player Stats")

        # Add the chapter body with the DataFrame
        pdf.chapter_body(df)

        # Save the PDF file
        pdf.output(f"{prediction_dir}/summary.pdf")

