import pandas as pd

rows = []
for year in range(2018, 2026):
    for code in [88101, 44201, 42602, 42101]:
        df = pd.read_csv(f"data/raw/epa_{code}_{year}.csv")
        rows.append({
            "year": year,
            "code": code,
            "sites": sorted(df["Site Num"].unique()),
            "days": df["Date Local"].nunique(),
        })
print(pd.DataFrame(rows).to_string())