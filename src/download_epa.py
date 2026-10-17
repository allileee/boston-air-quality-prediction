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

if __name__ == "__main__":
    year = 2018
    for code in [88101, 44201, 42602, 42101]:
        df = suffolk(fetch(f"daily_{code}_{year}"))
        df.to_csv(RAW / f"epa_{code}_{year}.csv", index=False)
        print(code, len(df), df["Site Num"].nunique(), "sites")