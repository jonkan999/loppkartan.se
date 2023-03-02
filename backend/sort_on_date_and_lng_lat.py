import json

# Read data from the file
with open("backend/new_races_w_formatted_summary.json", "r", encoding="utf-8") as f:
    races = json.load(f)

# Sort the data by date, longitude, and latitude
races_sorted = sorted(races, key=lambda r: (r["date"], r["longitude"], r["latitude"]))

# Write the sorted data back to the file
with open("backend/new_races_w_formatted_summary.json", "w", encoding="utf-8") as f:
    json.dump(races_sorted, f, ensure_ascii=False, indent=2)
