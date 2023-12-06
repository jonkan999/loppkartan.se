# File: C:\Users\Joel\loppkartan.se\scraper\run_all_scripts.py
import sys
from extraction import (
    extract_data_fri_Indoor_2024,
    extract_data_jogg_road,
    extract_data_jogg_trail,
    extract_data_trailkalendern,
)
from scraper_package.race_classes import Race, RaceCollection
from transform_race import transform_and_store_race

def run_all_scraper_scripts():
    extract_data_fri_Indoor_2024.main()
    extract_data_jogg_road.main()
    extract_data_jogg_trail.main()
    extract_data_trailkalendern.main()

if __name__ == "__main__":
    try:
        run_all_scraper_scripts()
    except Exception as e:
        print(e)
        sys.exit()

    #load all not transformed from source
    untransformed_races = RaceCollection()
    untransformed_races.load_not_transformed_from_source_json()
    costometer=0
    #transform all untransformed
    print(untransformed_races.races)
    for i, race in enumerate(untransformed_races.races):
        print(f"""
        TRANSFORMING----------------------
        ----------------------------------
        {race["name"]}
        RACES TRANSFORMED: {i} / {len(untransformed_races.races)}
        ----------------------------------
          """)
        transform_and_store_race(race.data,costometer,openai=True)
    print(f"""
    DONE TRANSFORMING----------------------
    ----------------------------------
    RACES TRANSFORMED: {i+1} / {len(untransformed_races.races)}
    ----------------------------------
    """)


    
