import json
from scraper_package import transform_module
from config import GOOGLE_GEOCODING_API_KEY as goog_access_token
from config import OPENAI_KEY as openai_access_token
from scraper_package.race_classes import Race, RaceCollection

def transform_and_store_race(race, costometer, openai=True):
    try:
        print(f"""
              TRANSFORMING----------------------
              ----------------------------------
              {race["name"]}
              ----------------------------------
                """)

        # Get website if not allowed or missing
        print("getting website")
        race["website"] = transform_module.check_allowed_url_get_goog(race["website"], race["website_ai_fallback"])
        print("done getting website")

        # Get website contents
        print("getting website content")
        contents = transform_module.get_website_contents(race["website"])
        race["contents"] = contents
        print("done getting website content")

        # Getting images
        image_search_query = f'"{race["name"]} {transform_module.process_url(race["website"])}"'
        image_url_list = transform_module.get_images_selenium(image_search_query)
        print("got images:")
        print(image_url_list)
        images = [transform_module.convert_and_compress_image(img, max_size_kb=200) for img in image_url_list]
        transform_module.add_or_update_object(race["name"], race["id"], images, "images.json")
        print("done with images")

        # Extract specific fields
        title = race['contents']['title']
        description = race['contents']['description']
        h1 = race['contents']['h1']
        paragraphs = race['contents']['p'] if race['contents']['p'] else ""
        h2 = race['contents']['h2'][0] if race['contents']['h2'] else ""

        # Map distances
        race["race_categories"] = transform_module.race_category_mapping(race["distance_m"], race["type"])
        print(race["race_categories"])

        if openai:
          # Generate summary prompt
          summary_prompt = f"Given this:\n\nTitle: {title}\nDescription: {description}\nH1: {h1}\nH2: {h2}\n\n Make a summary of the race in Swedish. Pretend that you are a running race director. Write a description in a couple of paragraphs that describes a race like that, you are allowed to freestyle a bit. Don't use HTML elements like Title:, H1:, or H2: in the text. Also emphasize that the race includes the following race categories/distances: {race['race_categories']} . And of this type: {race['type']}"
          race["long_summary"], costometer = transform_module.get_completion(prompt=summary_prompt, costometer=costometer, openai_key=openai_access_token)

          if race['long_summary']:
              short_summary_prompt = f"Given this:{race['long_summary']} Pretend that you are a running race director and write a shorter summary in Swedish of no more than 500 characters. Also emphasize that the race includes the following race categories/distances: {race['race_categories']} . And of this type: {race['type']}"
              race["summary"], costometer = transform_module.get_completion(prompt=short_summary_prompt, costometer=costometer, openai_key=openai_access_token)
          else:
              race["summary"] = None

          name_prompt = f"Given this:\n\nTitle: {title}\nDescription: {description}\nH1: {h1}\nH2: {h2}\n\n Pretend that you are the race director for this running race and give it a name in Swedish and using no more than 3 words"
          race["ai_name_guess"], costometer = transform_module.get_completion(prompt=name_prompt, costometer=costometer, openai_key=openai_access_token)
        else:
            race["ai_name_guess"] = None
        # Get lat and long from google geocoding API using search strings in order of preference
        search_strings = [
            race["place"],
            race["name"],
            race["website"],
            race["website_ai_fallback"],
            race["contents"]["title"],
            race["contents"]["h1"],
            race["ai_name_guess"]
        ]

        # Get coordinates for the first successful search string
        latitude, longitude = transform_module.get_lat_long_goog(goog_access_token, *search_strings)
        print("done geocoding")
        race["latitude"] = latitude
        race["longitude"] = longitude

        # Get counties for found coordinates
        if latitude != 0:
            race["county"] = transform_module.find_county(latitude, longitude)
        else:
            race["county"] = None

        #get id from races in staged_for_aproval
        staging_path="staged_for_approval.json"
        print("getting id from staged_for_approval")
        if race["id"] not in transform_module.get_all_ids_from_json(staging_path):
            print("appending to staged_for_approval")
            in_race = Race(**race)
            race_collection = RaceCollection()
            race_collection.races.append(in_race)
            print("appending to staged_for_approval")
            race_collection.append_or_create_json(staging_path)
            #updating race id in source json
            in_race.set_is_transformed(in_bool = True, update_source_json = True)

        return race

    except Exception as e:
        print(f"Error transforming race: {e}")
        return None
    
if __name__ == "__main__":
    # Hardcoded test race
    test_race = {
        "date": "20241019",
        "type": "trail",
        "name": "Night Trail Run 30 km",
        "distance": "30 km",
        "distance_m": [30000],
        "place": "Night Trail Run 30 km",
        "organizer": "",
        "website": "https://www.nighttrailrun.se/",
        "website_ai_fallback": "Night Trail Run 30 km 30 km",
        "src_url": "https://www.trailrunningsweden.se/trailkalendern/",
        "created_date": "2023-11-25 14:14:30",
        "updated_date": "2023-11-25 14:14:30",
        "id": "night-trail-run-30-km_20241019_httpswwwtrailrunningswedensetrailkalendern",
        "extract_id": "17ae8970-06cc-4719-9b92-7c50bc273045"
    }

    # Run transformation on the test race
    transformed_test_race = transform_and_store_race(test_race,costometer=0, openai=False)

    if transformed_test_race:
        print("Transformed Test Race:")
        print(transformed_test_race)
    else:
        print("Error transforming test race.")