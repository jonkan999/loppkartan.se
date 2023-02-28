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

# Example usage: find the county for a latitude and longitude
lat = 59.8332794
lon = 17.658447
county = find_county(lat, lon)
print(county)