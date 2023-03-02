import json

with open('backend/all_races.json', encoding='utf-8') as f:
    all_races = json.load(f)

# Sort the list based on the date value in ascending order
all_races = sorted(all_races, key=lambda x: x['date'])

# Write the sorted data to a new file, using UTF-8 encoding
with open('backend/all_races.json', 'w', encoding='utf-8') as f:
    json.dump(all_races, f, ensure_ascii=False)