from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error

from features import split_by_year

df = pd.read_csv("data/processed/features.csv", parse_dates=["date"], index_col="date")
train, val, test = split_by_year(df)

rows = []
for name, part in [("train", train), ("val", val), ("test", test)]:
    y_true = part["bad_tomorrow"]
    y_pred = (part["aqi"] > 50).astype(int)
    rows.append({
        "split": name,
        "days": len(part),
        "share_bad": round(y_true.mean(), 3),
        "accuracy": round(accuracy_score(y_true, y_pred), 3),
        "f1": round(f1_score(y_true, y_pred), 3),
        "mae": round(mean_absolute_error(part["aqi_tomorrow"], part["aqi"]), 2),
    })

results = pd.DataFrame(rows)
print(results.to_string(index=False))
Path("results").mkdir(exist_ok=True)
results.to_csv("results/baseline.csv", index=False)