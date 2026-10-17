import pandas as pd

def daily_pollutant(code, year, value_col, name, standard=None):
    df = pd.read_csv(f"data/raw/epa_{code}_{year}.csv", parse_dates=["Date Local"])
    if standard:
        df = df[df["Pollutant Standard"] == standard]
    per_site = df.groupby(["Date Local", "Site Num"])[value_col].mean()
    return per_site.groupby("Date Local").mean().rename(name)

if __name__ == "__main__":
    year = 2024
    daily = pd.concat([
        daily_pollutant(88101, year, "Arithmetic Mean", "pm25"),
        daily_pollutant(44201, year, "1st Max Value", "ozone"),
        daily_pollutant(42602, year, "1st Max Value", "no2"),
        daily_pollutant(42101, year, "1st Max Value", "co", standard="CO 8-hour 1971"),
    ], axis=1)
    print(daily.isna().sum())
    print(daily.describe())