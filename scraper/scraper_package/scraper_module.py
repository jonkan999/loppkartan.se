import json
import os
from difflib import SequenceMatcher
import uuid

def generate_unique_id():
    # Generate a unique hash here (replace this with your hash generation logic)
    unique_id = str(uuid.uuid4())
    return unique_id

def add_id(id_prefix, data):
    for i in range(len(data)):
        data[i][f'{id_prefix}_id'] = generate_unique_id()
        
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def create_json(filename, data):
    # write the file
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


def append_or_create_json(filename, data):
    # Check if the file exists
    if os.path.exists(filename):
        # If file exists, load the existing data and append to it
        with open(filename, "r", encoding='utf-8') as file:
            existing_data = json.load(file)
        
        existing_data.extend(data)
        
        # Write the combined data back to the file
        with open(filename, "w", encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False)
    else:
        # If file doesn't exist, create a new file with the provided data
        with open(filename, "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

def update_source(in_dict, file_path,join_col,key, value):
    with open(file_path, encoding='utf-8') as f:
        source = json.load(f)
    for item in in_dict:
        for obj in source:
            if join_col in item and item[join_col] == obj.get(join_col):
                print("Found match")
                obj[key] = value
    create_json(file_path, source)


def check_existing_race(event_data):
    date, name, distance, src_url = event_data['date'], event_data['name'], event_data['distance'], event_data['src_url']
    with open('scraped_data/old_races.json', encoding='utf-8') as f:
        old_races = json.load(f)
    #Appends with already scraped races if exists
    if os.path.exists('sourced_races.json'):
        with open('sourced_races.json', encoding='utf-8') as file:
            old_races.extend(json.load(file))
    for race in old_races:
        if race.get('date') == date and race.get('name') == name and race.get('distance') == distance and race.get('src_url') == src_url:
            print(race.get('name') + " already crawled ")
            return True
        elif race.get('date') == date and (similar(race.get('name'),name) > 0.5):
            print(race.get('name') + " and " + name+ " too similar ")
            return True
    return False

def extract_subdomain(url):
    try:
        subdomain = url.split('www.')[1].split('.')[0]
        return subdomain
    except IndexError:
        # Handle the case where there is no "www." or the URL structure is different
        return None
    






