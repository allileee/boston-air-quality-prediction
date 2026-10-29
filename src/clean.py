from pathlib import Path

import pandas as pd


def daily_pollutant(code, year, value_col, name, standard=None):
    df = pd.read_csv(f"data/raw/epa_{code}_{year}.csv", parse_dates=["Date Local"])
    if standard:
        df = df[df["Pollutant Standard"] == standard]
    per_site = df.groupby(["Date Local", "Site Num"])[value_col].mean()
    return per_site.groupby("Date Local").mean().rename(name)


def build_daily(year):
    daily = pd.concat([
        daily_pollutant(88101, year, "Arithmetic Mean", "pm25"),
        daily_pollutant(44201, year, "1st Max Value", "ozone"),
        daily_pollutant(42602, year, "1st Max Value", "no2"),
        daily_pollutant(42101, year, "1st Max Value", "co", standard="CO 8-hour 1971"),
    ], axis=1)

    aqi = pd.read_csv(f"data/raw/epa_aqi_{year}.csv", parse_dates=["Date"])
    aqi = aqi.set_index("Date")["AQI"].rename("aqi")
    return daily.join(aqi)


if __name__ == "__main__":
    out = Path("data/processed")
    out.mkdir(parents=True, exist_ok=True)
    for year in range(2018, 2026):
        daily = build_daily(year)
        daily.to_csv(out / f"daily_{year}.csv", index_label="date")
        print(year, len(daily), "rows")
        print(daily.isna().sum().to_dict())