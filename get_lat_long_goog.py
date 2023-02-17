import requests

def get_lat_long_goog(search_string, api_key):
    # Perform the geocoding request
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={search_string}&key={api_key}'
    try:
        response = requests.get(url)
        coords = response.json()

        # Get the geocoordinates from the results
        latitude = coords['results'][0]['geometry']['location']['lat']
        longitude = coords['results'][0]['geometry']['location']['lng']
    except:
        latitude = 0
        longitude = 0

    return [latitude, longitude]