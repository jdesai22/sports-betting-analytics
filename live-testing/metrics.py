import pandas as pd

ANALYSIS_FILE = "overall_results.csv"
SUCCESS_RATES_FILE = "success_rates.csv"

if __name__ == "__main__":
    df = pd.read_csv(ANALYSIS_FILE)

    
    # Calculate the sum of each column (excluding the 'Date' column)
    totals = df.drop(columns='date').sum()

    # Create a new row with the date value as 'TOTAL'
    totals_row = pd.DataFrame({'date': ['TOTAL']})
    totals_row = pd.concat([totals_row, totals.to_frame().T], axis=1)

    # Concatenate the totals row with the original DataFrame
    df = pd.concat([df, totals_row], ignore_index=True)



    df["over_success"] = (df["over_correct"] / df["over_predicted"]) * 100
    df["under_success"] = (df["under_correct"] / df["under_predicted"]) * 100
    df["overall_success"] = ((df["over_correct"] + df["under_correct"]) / (df["over_predicted"] + df["under_predicted"])) * 100
    df = df.round(decimals=2)
    df = df[['date', 'over_success', 'under_success', 'overall_success']]    

    df.to_csv(SUCCESS_RATES_FILE, index=False)

    print("success rates calculated")
    