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

    # Add the AQI target
    aqi = pd.read_csv(f"data/raw/epa_aqi_{year}.csv", parse_dates=["Date"])
    aqi = aqi.set_index("Date")["AQI"].rename("aqi")
    daily = daily.join(aqi)

    daily = daily.asfreq("D")
    daily["aqi_tomorrow"] = daily["aqi"].shift(-1)
    return daily


if __name__ == "__main__":
    year = 2024
    daily = build_daily(year)
    out = Path("data/processed")
    out.mkdir(parents=True, exist_ok=True)
    daily.to_csv(out / f"daily_{year}.csv", index_label="date")
    print(daily.isna().sum())
    print("saved", len(daily), "rows")