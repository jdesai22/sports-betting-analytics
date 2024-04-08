import pandas as pd

ANALYSIS_FILE = "overall_results_grouped.csv"
SUCCESS_RATES_FILE = "success_rates_grouped.csv"

if __name__ == "__main__":
    df = pd.read_csv(ANALYSIS_FILE)

    
    # Calculate the sum of each column (excluding the 'Date' column)
    totals = df.drop(columns='date').sum()

    # Create a new row with the date value as 'TOTAL'
    totals_row = pd.DataFrame({'date': ['TOTAL']})
    totals_row = pd.concat([totals_row, totals.to_frame().T], axis=1)

    # Concatenate the totals row with the original DataFrame
    df = pd.concat([df, totals_row], ignore_index=True)



    df["over momentum on non-star players"] = (df["correct over momentum on non-star players"] / df["predicted over momentum on non-star players"]) * 100
    df["under momentum"] = (df["correct under momentum"] / df["predicted under momentum"]) * 100
    df["fade star players"] = (df["correct fade star players"] / df["predicted fade star players"]) * 100

    df["overall_success"] = ((df["correct over momentum on non-star players"] + df["correct under momentum"] + df["correct fade star players"]) 
                             / (df["predicted over momentum on non-star players"] + df["predicted under momentum"]+ df["predicted fade star players"])) * 100
    df = df.round(decimals=2)
    df = df[['date', 'over momentum on non-star players', 'under momentum', 'fade star players', 'overall_success']]    

    df.to_csv(SUCCESS_RATES_FILE, index=False)

    print("success rates calculated")
    