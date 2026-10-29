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
    path = RAW / f"epa_aqi_{year}.csv"
    if path.exists():
        return  # already downloaded
    df = fetch(f"daily_aqi_by_county_{year}")
    boston = df[(df["State Name"] == "Massachusetts")
                & (df["county Name"] == "Suffolk")]
    boston.to_csv(path, index=False)
    print(year, len(boston), "rows")

if __name__ == "__main__":
    for year in range(2018, 2026):
        try:
            download_aqi(year)
        except requests.HTTPError as e:
            print(year, "failed:", e)