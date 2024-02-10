# File: C:\Users\Joel\loppkartan.se\scraper\run_all_scripts.py
import sys
from configuration.scraper_scripts import run_all_scraper_scripts
from scraper_package.race_classes import Race, RaceCollection
from transform_race import transform_and_store_race


def transform_untransformed_races(max_races=25):
    try:
        run_all_scraper_scripts()
    except Exception as e:
        print(e)
        sys.exit()

    #load all not transformed from source
    untransformed_races = RaceCollection()
    untransformed_races.load_not_transformed_from_source_json()
    costometer=0
    num_races = min(max_races, len(untransformed_races.races))
    #print(untransformed_races.races)
    for i, race in enumerate(untransformed_races.races[:num_races]):
        print(f"""
        TRANSFORMING----------------------
        ----------------------------------
        {race["name"]}
        RACES TRANSFORMED: {i+1} / {num_races}
        ----------------------------------
          """)
        transform_and_store_race(race.data,costometer,openai=True)
    print(f"""
    DONE TRANSFORMING----------------------
    ----------------------------------
    RACES TRANSFORMED:  {num_races} / {len(untransformed_races.races)}
    ----------------------------------
    """)
if __name__ == "__main__":
    transform_untransformed_races()  # Specify the maximum number of races to load at a time


    
