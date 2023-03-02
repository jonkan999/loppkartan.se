import json
import geopandas as gpd
from shapely.geometry import Point
from sweref99 import projections

# Load the Swedish county shapefile data
counties = gpd.read_file("backend/counties/Lan_Sweref99TM_region.shp")

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

# Read data from the file
with open("backend/new_races_w_formatted_summary.json", "r", encoding="utf-8") as f:
    races = json.load(f)

# Go through all races and add county to the dict
for race in races:
    lat = race["latitude"]
    lon = race["longitude"]
    county = find_county(lat, lon)
    race["county"] = county

# Write the data back to the file
with open("backend/new_races_w_formatted_summary.json", "w", encoding="utf-8") as f:
    json.dump(races, f, ensure_ascii=False, indent=2)
