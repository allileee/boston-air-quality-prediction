import pandas as pd

for year in [2021, 2022, 2023]:
    df = pd.read_csv(f"data/processed/daily_{year}.csv", parse_dates=["date"], index_col="date")
    missing = df[df["ozone"].isna()]
    print(year, "missing ozone days:", len(missing))
    print(missing.index.month.value_counts().sort_index())