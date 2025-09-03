import os
import pandas as pd
import numpy as np

# Folder containing ALL the CSV files you'll receive later
DATA_FOLDER = "temperatures"

def load_all_data():
    """
    Load and combine ALL .csv files from the 'temperatures' folder.
    Assumes each CSV has at least: Station, Date, Temperature columns.
    We'll adjust column names after we see the real files.
    """
    files = []
    if not os.path.exists(DATA_FOLDER):
        raise FileNotFoundError(f"Folder '{DATA_FOLDER}' not found. Create it and add CSV files.")
    for name in os.listdir(DATA_FOLDER):
        if name.lower().endswith(".csv"):
            files.append(os.path.join(DATA_FOLDER, name))
    if not files:
        raise FileNotFoundError(f"No CSV files found in '{DATA_FOLDER}'.")
    frames = [pd.read_csv(fp) for fp in files]
    df = pd.concat(frames, ignore_index=True)
    return df

def seasonal_average(df):
    """TODO: Calculate seasonal averages and save to average_temp.txt"""
    pass

def temperature_range(df):
    """TODO: Find station(s) with largest range and save to largest_temp_range_station.txt"""
    pass

def temperature_stability(df):
    """TODO: Find most stable/variable stations and save to temperature_stability_stations.txt"""
    pass

def main():
    df = load_all_data()
    print("Data preview:")
    print(df.head())
    
    seasonal_average(df)
    temperature_range(df)
    temperature_stability(df)

if __name__ == "__main__":
    main()
