import pandas as pd

for code in [88101, 44201, 42602, 42101]:
    df = pd.read_csv(f"data/raw/epa_{code}_2018.csv")
    print(f"\n=== {code} ===")
    print("unique days:", df["Date Local"].nunique())
    print("per site:\n", df.groupby("Site Num")["Date Local"].nunique())
    for col in ["POC", "Pollutant Standard", "Sample Duration"]:
        if col in df.columns:
            print(col, df[col].unique())
    print("date range:", df["Date Local"].min(), "to", df["Date Local"].max())