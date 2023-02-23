import json

# Read in the all_races.json file with UTF-8 encoding
with open("backend/all_races.json", "r", encoding="utf-8") as f:
    all_races = json.load(f)

# Read in the URL_Summary.json file with UTF-8 encoding
with open("backend/URL_Summary_Formatted.json", "r", encoding="utf-8") as f:
    url_summary = json.load(f)

# Create a dictionary of the URLs and summaries
url_dict = {d['url']: d['summary'] for d in url_summary}

# Create a new list to store the joined data
all_races_w_formatted_summary = []

# Loop through each row in all_races
for race in all_races:
    # Extract the URL from the row
    race_url = race['website']
    
    # Check if the URL has a corresponding summary
    if race_url in url_dict:
        race['summary'] = url_dict[race_url]
    else:
        # If the URL doesn't have a summary, add a blank value
        race['summary'] = ""
    
    # Add the row to the new list
    all_races_w_formatted_summary.append(race)

# Save the joined data to a new file with UTF-8 encoding
with open("all_races_w_formatted_summary.json", "w", encoding="utf-8") as f:
    json.dump(all_races_w_formatted_summary, f, indent=4, ensure_ascii=False)
