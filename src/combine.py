from pathlib import Path

import pandas as pd


def build_dataset(years=range(2018, 2026)):
    frames = [
        pd.read_csv(f"data/processed/daily_{y}.csv", parse_dates=["date"], index_col="date")
        for y in years
    ]
    daily = pd.concat(frames).sort_index()
    daily = daily.drop(columns=["aqi_tomorrow"], errors="ignore")

    weather = pd.read_csv("data/raw/weather.csv", parse_dates=["date"], index_col="date")

    data = daily.join(weather, how="left").asfreq("D")
    data["aqi_tomorrow"] = data["aqi"].shift(-1)
    return data


if __name__ == "__main__":
    data = build_dataset()
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    data.to_csv("data/processed/dataset.csv", index_label="date")
    print(data.shape)
    print(data.isna().sum())