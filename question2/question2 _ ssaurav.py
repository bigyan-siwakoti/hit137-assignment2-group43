import pandas as pd
import os
from glob import glob
import os
from glob import glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# 🕵️ Print current working directory
print("Current working dir:", os.getcwd())

# 🧭 Show all files inside /temperatures folder
print("Files inside 'temperatures' folder:")
folder_path = os.path.join("temperatures")
if os.path.exists(folder_path):
    print(os.listdir(folder_path))
else:
    print("❌ 'temperatures' folder NOT FOUND")

# 🔍 Try globbing .csv files
csv_files = glob(os.path.join("temperatures", "*.csv"))

print("CSV files found:", csv_files)


# 🔍 Folder where the CSV files are located
csv_files = glob(os.path.join("temperatures", "stations_group_*.csv"))

# 📥 Combine all CSV files
df_list = [pd.read_csv(file) for file in csv_files]
df = pd.concat(df_list, ignore_index=True)

# 🔄 Define seasons
seasons = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

# 📊 Calculate seasonal averages
season_averages = {}
for season, months in seasons.items():
    season_averages[season] = df[months].mean().mean()

# 🔥 Find station with largest temperature range
df['MaxTemp'] = df.loc[:, "January":"December"].max(axis=1)
df['MinTemp'] = df.loc[:, "January":"December"].min(axis=1)
df['TempRange'] = df['MaxTemp'] - df['MinTemp']
max_range = df['TempRange'].max()
largest_range_stations = df[df['TempRange'] == max_range][['STATION_NAME', 'TempRange']]

# 🌡️ Find warmest and coolest stations
df['YearlyAvg'] = df.loc[:, "January":"December"].mean(axis=1)
max_avg = df['YearlyAvg'].max()
min_avg = df['YearlyAvg'].min()
warmest = df[df['YearlyAvg'] == max_avg][['STATION_NAME', 'YearlyAvg']]
coolest = df[df['YearlyAvg'] == min_avg][['STATION_NAME', 'YearlyAvg']]

# 📄 Save output to text files
with open("average_temp.txt", "w") as f:
    f.write("Average Temperature per Season:\n")
    for s, avg in season_averages.items():
        f.write(f"{s}: {round(avg, 2)}°C\n")

with open("largest_temp_range_station.txt", "w") as f:
    f.write("Station(s) with Largest Temperature Range:\n")
    f.write(largest_range_stations.to_string(index=False))

with open("warmest_and_coolest_station.txt", "w") as f:
    f.write("Warmest Station(s):\n")
    f.write(warmest.to_string(index=False) + "\n\n")
    f.write("Coolest Station(s):\n")
    f.write(coolest.to_string(index=False))
