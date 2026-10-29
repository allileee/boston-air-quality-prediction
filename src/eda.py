import pandas as pd

df = pd.read_csv("data/processed/features.csv", parse_dates=["date"], index_col="date")
bad_today = df["aqi"] > 50

print("Date range:", df.index.min().date(), "to", df.index.max().date(), "|", len(df), "rows")

print("\nShare of bad days by year:")
print(bad_today.groupby(df.index.year).mean().round(3))

print("\nShare of bad days by month:")
print(bad_today.groupby(df.index.month).mean().round(3))

print("\nAQI summary:")
print(df["aqi"].describe().round(1))

print("\nCorrelation of tomorrow's AQI with each variable:")
cols = ["aqi", "pm25", "ozone", "no2", "co", "temperature_2m_max",
        "precipitation_sum", "wind_speed_10m_max", "relative_humidity_2m_mean"]
print(df[cols + ["aqi_tomorrow"]].corr()["aqi_tomorrow"].drop("aqi_tomorrow").round(2))

aqi_raw = pd.concat(
    [pd.read_csv(f"data/raw/epa_aqi_{y}.csv") for y in range(2018, 2026)]
)
print("\nDefining parameter share:")
print(aqi_raw["Defining Parameter"].value_counts(normalize=True).round(3))