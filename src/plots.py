from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

Path("figures").mkdir(exist_ok=True)
df = pd.read_csv("data/processed/features.csv", parse_dates=["date"], index_col="date")
bad_today = df["aqi"] > 50

#AQI over time
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df.index, df["aqi"], linewidth=0.6)
ax.axhline(50, color="red", linestyle="--", label="Moderate threshold (50)")
ax.set_ylabel("Daily AQI")
ax.set_title("Boston (Suffolk County) daily AQI, 2018-2025")
ax.legend()
fig.tight_layout()
fig.savefig("figures/aqi_timeseries.png", dpi=150)
plt.close(fig)

# Share of bad days by month
fig, ax = plt.subplots(figsize=(8, 4))
bad_today.groupby(df.index.month).mean().plot.bar(ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Share of days with AQI > 50")
ax.set_title("Seasonality of Moderate-or-worse days")
fig.tight_layout()
fig.savefig("figures/bad_days_by_month.png", dpi=150)
plt.close(fig)

# Share of bad days by year
fig, ax = plt.subplots(figsize=(8, 4))
bad_today.groupby(df.index.year).mean().plot.bar(ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Share of days with AQI > 50")
ax.set_title("Moderate-or-worse days by year")
fig.tight_layout()
fig.savefig("figures/bad_days_by_year.png", dpi=150)
plt.close(fig)

# Which pollutant defines the AQI
aqi_raw = pd.concat(
    [pd.read_csv(f"data/raw/epa_aqi_{y}.csv") for y in range(2018, 2026)]
)
counts = aqi_raw["Defining Parameter"].value_counts()
counts = counts.drop("PM10", errors="ignore")

fig, ax = plt.subplots(figsize=(7, 4))
counts.plot.bar(ax=ax)
ax.set_ylabel("Number of days")
ax.set_title("Pollutant that set the daily AQI")
fig.tight_layout()
fig.savefig("figures/defining_parameter.png", dpi=150)
plt.close(fig)

# Correlation heatmap
cols = ["pm25", "ozone", "no2", "co", "aqi", "aqi_tomorrow",
        "temperature_2m_max", "precipitation_sum", "wind_speed_10m_max",
        "relative_humidity_2m_mean", "surface_pressure_mean"]
corr = df[cols].corr()
fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")
ax.set_xticks(range(len(cols)))
ax.set_xticklabels(cols, rotation=90)
ax.set_yticks(range(len(cols)))
ax.set_yticklabels(cols)
fig.colorbar(im, label="Correlation")
ax.set_title("Correlation of pollutants, weather, and AQI")
fig.tight_layout()
fig.savefig("figures/correlation_heatmap.png", dpi=150)
plt.close(fig)

print("saved 5 figures to figures/")