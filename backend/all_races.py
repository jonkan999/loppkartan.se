import json
import uuid
import config
import get_lat_long_goog
import re

access_token = config.GOOGLE_GEOCODING_API_KEY

#retrieve manually adjusted races
with open('old_races.json', encoding='utf-8') as f:
    already_crawled_races = json.load(f)


# Load the data from the two input files
with open('events_fri_Arena.json', encoding='utf-8') as f:
    events_fri_Arena = json.load(f)

with open('events_fri_Indoor_2023.json', encoding='utf-8') as f:
    events_fri_Arena = json.load(f)

with open('events_fri_Indoor_2024.json', encoding='utf-8') as f:
    events_fri_Arena = json.load(f)

with open('events_fri_LL.json', encoding='utf-8') as f:
    events_fri_LL = json.load(f)

with open('events_fri_jogg_trail.json', encoding='utf-8') as f:
    events_fri_jogg_trail = json.load(f)

with open('events_fri_jogg_road.json', encoding='utf-8') as f:
    events_fri_jogg_road = json.load(f)

with open('events_trailkalendern.json', encoding='utf-8') as f:
    events_trailkalendern = json.load(f)



# Merge all the new dictionaries for geolocating
all_races = events_fri_Arena + events_fri_LL + events_fri_jogg_trail + events_fri_jogg_road + events_trailkalendern

# geolocate place and add a unique ID to each row
for i in range(len(all_races)):
    [latitude, longitude] = get_lat_long_goog.get_lat_long_goog(all_races[i]["place"], access_token)
    #If unsuccessfull on place, we try name
    if latitude == 0:
        [latitude, longitude] = get_lat_long_goog.get_lat_long_goog(all_races[i]["name"], access_token)
    all_races[i]["latitude"] = latitude
    all_races[i]["longitude"] = longitude
    all_races[i]["id"] = str(uuid.uuid4())

# Merge the all dictionaries into one
old_races = all_races + already_crawled_races

# Write the merged data to a new file, using UTF-8 encoding
with open('all_races.json', 'w', encoding='utf-8') as f:
    json.dump(all_races, f, ensure_ascii=False)

with open('old_races.json', 'w', encoding='utf-8') as f:
    json.dump(old_races, f, ensure_ascii=False)