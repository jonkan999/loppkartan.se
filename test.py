
import config
import get_lat_long_goog

access_token = config.GOOGLE_GEOCODING_API_KEY



[latitude, longitude] = get_lat_long_goog.get_lat_long_goog("stockholm", access_token)
print([latitude, longitude]) 

""" url = f'https://maps.googleapis.com/maps/api/geocode/json?address={"stockholm"}&key={"AIzaSyDWfb8WleRGtXjeP7yuOs167lkLT_6lC0U"}'
response = requests.get(url)
coords = response.json()


latitude = coords['results'][0]['geometry']['location']['lat']
longitude = coords['results'][0]['geometry']['location']['lng']

print([latitude,longitude]) """