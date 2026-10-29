from pathlib import Path

import pandas as pd
import requests

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

def download_weather(start="2018-01-01", end="2025-12-31"):
    params = {
        "latitude": 42.36,
        "longitude": -71.06,
        "start_date": start,
        "end_date": end,
        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max",
            "wind_direction_10m_dominant",
            "relative_humidity_2m_mean",
            "surface_pressure_mean",
        ]),
        "timezone": "America/New_York",
    }
    r = requests.get("https://archive-api.open-meteo.com/v1/archive",
                     params=params, timeout=120)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["daily"]).rename(columns={"time": "date"})
    df.to_csv(RAW / "weather.csv", index=False)
    print(len(df), "days", df["date"].min(), "to", df["date"].max())
    print(df.isna().sum())

if __name__ == "__main__":
    download_weather()