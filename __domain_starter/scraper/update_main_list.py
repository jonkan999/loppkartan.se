from jinja2 import Environment, FileSystemLoader
import os
import base64
import json
import yaml

def map_distance(distance, race_type, distance_mapping, distance_units):
    if isinstance(distance, str):
        return distance_mapping.get(distance, distance) # If distance is not in the mapping, return the original value
    elif isinstance(distance, list):
        return [map_distance(d, race_type, distance_mapping, distance_units) for d in distance] # Recursively map each distance in the list
    elif isinstance(distance, (int, float)):
        if race_type == 'track':
            for unit in distance_units:
                if unit['range'][0] <= distance <= unit['range'][1]:
                    return f"{int(distance)} {unit['label']}"
            return f"{int(distance)} meter"
        else:
            distance = distance / 1000
            for unit in distance_units:
                if unit['range'][0] <= distance <= unit['range'][1]:
                    return f"{unit['label']}"
            return f"{int(distance)} km"

# Load the Jinja2 template
# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Move up one folder to the parent directory
parent_dir = os.path.join(script_dir, '..')

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(searchpath=parent_dir))
# Print the template loader's search path
print(f"Template search path: {env.loader.searchpath}")
# Register the filter function with the Jinja2 environment
template = env.get_template("lopplistan_template.html")

if __name__ == "__main__":
    with open("../all_races_w_formatted_summary.json", 'r', encoding='utf-8') as all_races_file:
        events_data = json.load(all_races_file)

    with open("../collection_configuration/general_config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) 

    # Group races by month
    events_by_month = {}
    for event in events_data:
        day_num = event['date'][6:8]
        month_num = event['date'][4:6]
        # Map month using the month mapping from config
        month_mapping = config['month_mapping']
        month = month_mapping[month_num]
        year = event['date'][0:4]
        month_year = f"{month} {year}"

        # necessary html mapping
        month_mapping_short = config['month_mapping_short']
        month = month_mapping_short[month_num]
        event['display_date'] = f"{day_num.lstrip('0')} {month}"
        event['display_distances'] = map_distance(sorted(event['distance_m']),event['type'],config['distance_mapping'],config['distance_units'])
        event['display_distances'] = ', '.join(map(str, event['display_distances']))
        events_by_month.setdefault(month_year, []).append(event) # Set default value to empty list if key doesn't exist, appends races to the list for each month

    #print(events_by_month["Januari 2024"])
    print(events_by_month.keys())
    data = {
    'config': config,
    'events_by_month': events_by_month
    }
    html = template.render(data=data)

    page_path = f"../output.html"
    print(f"Saving page to {page_path}")
    # Save the generated HTML page
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(html)