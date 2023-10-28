import json
import uuid
import config
import get_lat_long_goog
import re
import geopandas as gpd
from shapely.geometry import Point
from sweref99 import projections

# Load the Swedish county shapefile data
counties = gpd.read_file("counties/Lan_Sweref99TM_region.shp")

# Define a function to find the county for a given latitude and longitude
def find_county(lat, lon):
    # Convert the WGS 84 coordinates to SWEREF 99 using the latlon_to_rt90 function
    tm = projections.make_transverse_mercator("SWEREF_99_TM")
    northing, easting = tm.geodetic_to_grid(lat, lon)

    # Create a shapely Point object from the transformed coordinates
    point = Point(easting, northing)

    # Loop through the counties and check if the point is inside each polygon
    for i in range(len(counties)):
        if point.within(counties.iloc[i].geometry):
            return counties.iloc[i].LnNamn

    # If the point is not inside any polygon, return None
    return None

access_token = config.GOOGLE_GEOCODING_API_KEY

#retrieve manually adjusted races
with open('new_races_w_formatted_summary_MI.json', encoding='utf-8') as f:
    new_races_MI = json.load(f)

# geolocate place and add a unique ID to each row
for i in range(len(new_races_MI)):
    [latitude, longitude] = get_lat_long_goog.get_lat_long_goog(new_races_MI[i]["place"], access_token)
    #If unsuccessfull on place, we try name
    if latitude == 0:
        [latitude, longitude] = get_lat_long_goog.get_lat_long_goog(new_races_MI[i]["name"], access_token)
    new_races_MI[i]["latitude"] = latitude
    new_races_MI[i]["longitude"] = longitude
    new_races_MI[i]["id"] = str(uuid.uuid4())
    #Get county if it doesnt exist
    try:
        if new_races_MI[i]["county"] == None:
            county = find_county(latitude, longitude)
            new_races_MI[i]["county"] = county
    except KeyError:
        
        new_races_MI[i]["county"] = None  # Handle the case where "county" key is missing
        county = find_county(latitude, longitude)
        new_races_MI[i]["county"] = county
        if county != None:
            print("county added: " + county + " for: " + new_races_MI[i]["name"] )
        else:
            print("couldnt add county " + "for: " + new_races_MI[i]["name"] )
            
        

# Write the merged data to a new file, using UTF-8 encoding
with open('new_races_w_formatted_summary_MI_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(new_races_MI, f, ensure_ascii=False)