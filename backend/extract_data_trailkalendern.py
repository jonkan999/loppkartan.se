import requests
from bs4 import BeautifulSoup
import json
import check_existing_race
import re

url = "https://trailrunningsweden.se/trailkalendern/"
response = requests.get(url, 
            headers={'User-Agent': 'Mozilla/5.0'}
            )

data = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    events = soup.find_all("div", class_="event")
    for event in events:
        if "past_event" not in event["class"]:
            date_span = event.find("span", class_="evoet_dayblock evcal_cblock")
            month_name = date_span.get("data-smon")
            months_dict = {
                "januari": "01",
                "februari": "02",
                "mars": "03",
                "april": "04",
                "maj": "05",
                "juni": "06",
                "juli": "07",
                "augusti": "08",
                "september": "09",
                "oktober": "10",
                "november": "11",
                "december": "12"
            }
            month_num = months_dict.get(month_name.lower(), "00")
            day = event.find("em", class_="date").text.strip().zfill(2)
            proper_date = f"2023{month_num}{day}"
            name_span = event.find("span", class_="evoet_title evcal_desc2 evcal_event_title")
            name = name_span.text.strip()
            distance_str = ""
            distances = []
            try:
                distance_span = event.find("span", class_="evcal_event_subtitle")
                distance_str = distance_span.text.strip()
                for distance_item in distance_str.split(", "):
                    if "KM" in distance_str:
                        if "," in distance_item:
                            distance_item = distance_item.split(",")[0] #get first digit if fraction
                            distances.append(int(distance_item)*1000)
                        else:
                            try:
                                distances.append(int(distance_item[:-2])*1000)
                            except:
                                pass
                    elif "km" in distance_str:
                        if "," in distance_item:
                            distance_item = distance_item.split(",")[0] #get first digit if fraction
                            distances.append(int(distance_item)*1000)
                        else:
                            try:
                                distances.append(int(distance_item[:-2])*1000)
                            except:
                                pass
                    elif "MILES" in distance_str:
                        try:
                            for match in re.findall(r"(\d+)\s*KM", distance_str):
                                distances.append(int(match)*1609)
                        except:
                            pass
            except: 
                pass

            website_a = event.find("a", class_="evcal_evdata_row evo_clik_row")
            website = website_a.get("href") if website_a else ""
            place = ""
            organizer = ""
            latitude = 0
            longitude = 0
            event_data = {"date": proper_date, "month": month_name, "day": day, "type": "trail", "name": name, "distance": distance_str,"distance_m": distances, "place": place,"latitude": latitude, "longitude": longitude, "organizer": organizer, "website": website, "src_url": url}
            #Checks if race is already crawled
            if check_existing_race.check_existing_race(event_data['date'], event_data['name'], event_data['distance'], event_data['src_url']):
                print("already crawled: " + proper_date + ", " + name + ", " +  distance_str + ", " + url)
            else:
                #Else we crawl
                data.append(event_data)
else:
    print("Error: Could not retrieve page")

with open("backend/events_trailkalendern.json", "w", encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)