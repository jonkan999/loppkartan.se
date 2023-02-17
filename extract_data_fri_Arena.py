import requests
from bs4 import BeautifulSoup
import json
import get_lat_long_goog
import re

url = "https://friidrott.euwest01.umbraco.io/tavling-landslag/tavling/tavlingskalender/tavlingar-i-sverige/arenatavlingar/"

response = requests.get(url)

months_dict = {'MARS': '03', 'APRIL': '04', 'MAJ': '05', 'JUNI': '06', 'JULI': '07', 'AUGUSTI': '08', 'SEPTEMBER': '09', 'OKTOBER': '10', 'NOVEMBER': '11', 'DECEMBER': '12'}
months_list = list(months_dict.keys())

data = []

# Parse the filtered event data and geocode the location
event_soup = BeautifulSoup(response.content, "html.parser")

for container in event_soup.find_all("div", class_="calendar__container"):
    month_header = container.find("header", class_="calendar__header")
    if month_header is None:
        continue
    month_name = month_header.h2.text.strip()
    if month_name in months_dict:
        month_num = months_dict[month_name]
        events = container.find_all("li", class_="calendar-item")
        for event in events:
            day = event.find("time", class_="calendar-item__date").find("span").text.strip()

            proper_date = '2023' + month_num + day.zfill(2)
            translated_type = "track"
            texts = event.find_all("p", class_="calendar-item__text")
            name = texts[1].text.strip()
            place = texts[2].text.strip()
            organizer = texts[3].text.strip()
            website = ""
            try:
                website = event.find("a").get("href")
            except:
                website = ""
            distance_str = event.get("data-event")
            #if no 1500-10k race then pass
            event_distances = ["event-1500-m", "event-3000-m", "event-5000-m", "event-10000-m"]

            if (not any(event_distance in distance_str.split(" ") for event_distance in event_distances)):
                continue

            distances = []
            for distance_item in distance_str.split(" "):
                km_index = distance_item.find("-km")
                if "event-marathon" == distance_item:
                    distances.append(42195)
                elif "event-halvmarathon" == distance_item:
                    distances.append(21098)
                elif "event-5000-m" == distance_item:
                    distances.append(5000)
                elif "event-10-000-m" == distance_item:
                    distances.append(10000)
                elif "event-3000-m" == distance_item:
                    distances.append(3000)
                elif "event-1500-m" == distance_item:
                    distances.append(1500)
                elif distance_item.startswith("event-") and distance_item.endswith("-km"):
                    value_str = distance_item[6:-3]
                    try:
                        value = float(value_str)
                        distances.append(int(value * 1000))
                    except ValueError:
                        pass

            #Fetching geocoordinates
            # Use the place as a search string
            # Perform the geocoding request
            #[latitude, longitude] = get_lat_long_goog.get_lat_long_goog(place, access_token)
            latitude = 0
            longitude = 0
            event_data = {"date": proper_date, "month": month_name, "day": day, "type": translated_type, "name": name, "distance": distance_str,"distance_m": distances, "place": place,"latitude": latitude, "longitude": longitude, "organizer": organizer, "website": website}
            data.append(event_data)


with open("events_fri_Arena.json", "w", encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)