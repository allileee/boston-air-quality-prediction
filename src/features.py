from pathlib import Path

import numpy as np
import pandas as pd

BAD_THRESHOLD = 50 

def add_features(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

def add_features(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    # flag missing ozone
    df["ozone_missing"] = df["ozone"].isna().astype(int)

    # fill in short gaps
    for col in ["ozone", "no2", "co"]:
        df[col] = df[col].ffill(limit=2)

    # lagged values
    for lag in [1, 3, 7]:
        df[f"aqi_lag{lag}"] = df["aqi"].shift(lag)
    for col in ["pm25", "ozone", "no2"]:
        df[f"{col}_lag1"] = df[col].shift(1)

    # rolling averages
    for col in ["aqi", "pm25", "ozone"]:
        df[f"{col}_roll7"] = df[col].rolling(7, min_periods=3).mean()

    # calendar
    df["month"] = df.index.month
    df["day_of_week"] = df.index.dayofweek
    doy = df.index.dayofyear
    df["doy_sin"] = np.sin(2 * np.pi * doy / 365.25)
    df["doy_cos"] = np.cos(2 * np.pi * doy / 365.25)

    # wind direction
    rad = np.deg2rad(df["wind_direction_10m_dominant"])
    df["wind_sin"] = np.sin(rad)
    df["wind_cos"] = np.cos(rad)

    # temperature
    df["temp_range"] = df["temperature_2m_max"] - df["temperature_2m_min"]

    # targets
    df["bad_tomorrow"] = (df["aqi_tomorrow"] > BAD_THRESHOLD).astype(int)
    df = df.dropna(subset=["aqi_tomorrow"])  # last row has no tomorrow

    return df


FEATURES = [
    "pm25", "ozone", "no2", "co", "aqi", "ozone_missing",
    "aqi_lag1", "aqi_lag3", "aqi_lag7",
    "pm25_lag1", "ozone_lag1", "no2_lag1",
    "aqi_roll7", "pm25_roll7", "ozone_roll7",
    "temperature_2m_max", "temperature_2m_min", "temp_range",
    "precipitation_sum", "wind_speed_10m_max", "wind_sin", "wind_cos",
    "relative_humidity_2m_mean", "surface_pressure_mean",
    "month", "day_of_week", "doy_sin", "doy_cos",
]


def split_by_year(df: pd.DataFrame):
    train = df.loc[:"2022"]
    val = df.loc["2023"]
    test = df.loc["2024":]
    return train, val, test


if __name__ == "__main__":
    data = pd.read_csv("data/processed/dataset.csv", parse_dates=["date"], index_col="date")
    df = add_features(data)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df.to_csv("data/processed/features.csv", index_label="date")

    train, val, test = split_by_year(df)
    print("shape:", df.shape)
    for name, part in [("train", train), ("val", val), ("test", test)]:
        print(name, len(part), "rows, share bad:", round(part["bad_tomorrow"].mean(), 3))
    print(df[FEATURES].isna().sum()[lambda s: s > 0])