import requests
import json

def get_lat_long(search_string, access_token):
    # Perform the geocoding request
    url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + search_string + '.json?access_token=' + access_token
    response = requests.get(url)
    coords = json.loads(response.text)

    # Get the geocoordinates from the results
    latitude = coords['features'][0]['center'][1]
    longitude = coords['features'][0]['center'][0]

    return [latitude, longitude]