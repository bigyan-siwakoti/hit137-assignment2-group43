# q2_temperature.py
import os
import pandas as pd
import numpy as np

# Folder containing ALL the CSV files (you already uploaded them here):
DATA_FOLDER = "temperatures"

# Output files (will be created/overwritten in the same folder as this script)
AVG_OUT = "average_temp.txt"
RANGE_OUT = "largest_temp_range_station.txt"
STABILITY_OUT = "temperature_stability_stations.txt"

# Month and season defs (Australian seasons)
MONTHS = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]
SEASON_OF_MONTH = {
    "December": "Summer", "January": "Summer", "February": "Summer",
    "March": "Autumn", "April": "Autumn", "May": "Autumn",
    "June": "Winter", "July": "Winter", "August": "Winter",
    "September": "Spring", "October": "Spring", "November": "Spring",
}

def _read_single_csv(fp: str) -> pd.DataFrame:
    """
    Read ONE csv like stations_group_1986.csv and return a long-form DataFrame:
    columns: ['STATION_NAME','Month','Temperature'].
    We ignore non-month columns and NaNs.
    """
    df = pd.read_csv(fp)

    # Normalise column names: strip spaces; title-case known months
    df.columns = [c.strip() for c in df.columns]

    # Identify month columns present in this file (some files may include extras like 'Annual')
    month_cols = [m for m in MONTHS if m in df.columns]
    if not month_cols:
        raise ValueError(f"No month columns found in {os.path.basename(fp)}")

    # Ensure the station name column exists (common names seen)
    station_col = None
    for candidate in ["STATION_NAME", "Station", "Station_Name", "station_name"]:
        if candidate in df.columns:
            station_col = candidate
            break
    if station_col is None:
        # Fallback: if a column looks like 'NAME' use it
        for c in df.columns:
            if c.lower() in ("name", "stationname"):
                station_col = c
                break
    if station_col is None:
        raise ValueError(f"Could not find station name column in {os.path.basename(fp)}")

    # Melt to long format: one row per station-month with temperature value
    long_df = df.melt(
        id_vars=[station_col],
        value_vars=month_cols,
        var_name="Month",
        value_name="Temperature"
    ).rename(columns={station_col: "STATION_NAME"})

    # Keep numeric temps only; ignore NaNs per assignment
    long_df["Temperature"] = pd.to_numeric(long_df["Temperature"], errors="coerce")
    long_df = long_df.dropna(subset=["Temperature"])

    # Add season
    long_df["Season"] = long_df["Month"].map(SEASON_OF_MONTH)

    # Some files might have unexpected month labels; drop those if any
    long_df = long_df.dropna(subset=["Season"])

    return long_df[["STATION_NAME", "Month", "Season", "Temperature"]]


def load_all_data() -> pd.DataFrame:
    """
    Load and combine ALL .csv files from the 'temperatures' folder
    into a single long-form DataFrame with columns:
    ['STATION_NAME','Month','Season','Temperature'].
    """
    if not os.path.exists(DATA_FOLDER):
        raise FileNotFoundError(f"Folder '{DATA_FOLDER}' not found (expected next to this script).")

    csv_paths = [
        os.path.join(DATA_FOLDER, f)
        for f in os.listdir(DATA_FOLDER)
        if f.lower().endswith(".csv")
    ]
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in '{DATA_FOLDER}'.")

    frames = []
    for fp in sorted(csv_paths):
        frames.append(_read_single_csv(fp))
    return pd.concat(frames, ignore_index=True)


def seasonal_average(df: pd.DataFrame) -> None:
    """
    Calculate the average temperature for each Australian season
    across ALL stations and ALL years. Save to 'average_temp.txt' with:
    Summer: 28.5°C
    """
    order = ["Summer", "Autumn", "Winter", "Spring"]
    avg = (
        df.groupby("Season", as_index=False)["Temperature"]
          .mean(numeric_only=True)
    )
    # Ensure order
    avg["Season"] = pd.Categorical(avg["Season"], categories=order, ordered=True)
    avg = avg.sort_values("Season")

    lines = [f"{row.Season}: {row.Temperature:.1f}°C" for _, row in avg.iterrows()]
    with open(AVG_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def temperature_range(df: pd.DataFrame) -> None:
    """
    Find station(s) with the largest temperature range (max - min)
    across ALL months and ALL years. Save to 'largest_temp_range_station.txt'.
    If multiple tie, list all.
    """
    agg = df.groupby("STATION_NAME")["Temperature"]
    stats = pd.DataFrame({
        "Min": agg.min(),
        "Max": agg.max()
    })
    stats["Range"] = stats["Max"] - stats["Min"]

    # Max range value
    max_range = stats["Range"].max()
    winners = stats[stats["Range"] == max_range].reset_index()

    lines = []
    for _, r in winners.iterrows():
        lines.append(
            f"{r['STATION_NAME']}: Range {r['Range']:.1f}°C (Max: {r['Max']:.1f}°C, Min: {r['Min']:.1f}°C)"
        )
    with open(RANGE_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def temperature_stability(df: pd.DataFrame) -> None:
    """
    Compute standard deviation of temperatures per station.
    Output MOST STABLE (lowest std) and MOST VARIABLE (highest std)
    to 'temperature_stability_stations.txt'. If ties, list all.
    """
    stds = (
        df.groupby("STATION_NAME")["Temperature"]
          .std(ddof=0)  # population std; ddof=1 (sample) would also be OK
          .rename("StdDev")
          .to_frame()
    ).dropna()

    min_std = stds["StdDev"].min()
    max_std = stds["StdDev"].max()

    most_stable = stds[stds["StdDev"] == min_std].reset_index()
    most_variable = stds[stds["StdDev"] == max_std].reset_index()

    lines = []
    for _, r in most_stable.iterrows():
        lines.append(f"Most Stable: {r['STATION_NAME']}: StdDev {r['StdDev']:.1f}°C")
    for _, r in most_variable.iterrows():
        lines.append(f"Most Variable: {r['STATION_NAME']}: StdDev {r['StdDev']:.1f}°C")

    with open(STABILITY_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    df = load_all_data()
    # Run all three required tasks
    seasonal_average(df)
    temperature_range(df)
    temperature_stability(df)
    # Small confirmation in console (when running locally/Codespaces)
    print(f"Wrote: {AVG_OUT}, {RANGE_OUT}, {STABILITY_OUT}")

if __name__ == "__main__":
    main()
