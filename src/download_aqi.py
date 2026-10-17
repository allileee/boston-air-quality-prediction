import io
import zipfile
from pathlib import Path

import pandas as pd
import requests

BASE = "https://aqs.epa.gov/aqsweb/airdata"
RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

def fetch(name: str) -> pd.DataFrame:
    url = f"{BASE}/{name}.zip"
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        return pd.read_csv(z.open(z.namelist()[0]), low_memory=False)

def download_aqi(year):
    df = fetch(f"daily_aqi_by_county_{year}")
    print(df.columns.tolist())  # check the real column names
    boston = df[(df["State Name"] == "Massachusetts")
                & (df["county Name"] == "Suffolk")]
    boston.to_csv(RAW / f"epa_aqi_{year}.csv", index=False)
    print(year, len(boston), "rows")
    print(boston["Defining Parameter"].value_counts())
    print(boston["Category"].value_counts())

if __name__ == "__main__":
    download_aqi(2018)