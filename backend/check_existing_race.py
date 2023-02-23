import json

def check_existing_race(date, name, distance, src_url):
    with open('backend/all_races.json', encoding='utf-8') as f:
        all_races = json.load(f)

    #adjusted_races = [race for race in all_races if race.get('adjusted') == 1]
    
    for race in all_races:
        if race.get('date') == date and race.get('name') == name and race.get('distance') == distance and race.get('src_url') == src_url:
            return True
    return False