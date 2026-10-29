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

def suffolk(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["State Code"].astype(str) == "25")
              & (df["County Code"].astype(int) == 25)]

POLLUTANTS = [88101, 44201, 42602, 42101]

def download_pollutants(year):
    for code in POLLUTANTS:
        path = RAW / f"epa_{code}_{year}.csv"
        if path.exists():
            return
        df = suffolk(fetch(f"daily_{code}_{year}"))
        df.to_csv(path, index=False)
        print(year, code, len(df), df["Site Num"].nunique(), "sites")

if __name__ == "__main__":
    for year in range(2018, 2026):
        try:
            download_pollutants(year)
        except requests.HTTPError as e:
            print(year, "failed:", e)