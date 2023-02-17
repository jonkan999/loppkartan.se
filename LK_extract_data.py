import requests
from bs4 import BeautifulSoup
import json
import config
import get_lat_long_goog
import re

access_token = config.GOOGLE_GEOCODING_API_KEY


months_se = ["Mars", "April", "Maj", "June", "Juli", "Augusti", "September", "Oktober", "November", "December"]
months_dict = {'Mars': '03', 'April': '04', 'Maj': '05', 'Juni': '06', 'Juli': '07', 'Augusti': '08', 'September': '09', 'Oktober': '10', 'November': '11', 'December': '12'}
months_list = list(months_dict.keys())

# make a GET request to the website
response = requests.get("http://loparkalendern.se/")

# parse the response with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# find all elements with class "fusion-builder-row"
rows = soup.find_all("div", class_="fusion-builder-row")

# list to store the events
events = []

# iterate over each row
for row in rows:
    # find the title heading
    title_heading = row.find("h1", class_="title-heading-left")
    
    # if the title heading contains one of the months
    if title_heading and any(month in title_heading.text for month in months_se):
        # find all elements with class "fusion-text"
        fusion_texts = row.find_all("div", class_="fusion-text")

        # iterate over each fusion text
        for fusion_text in fusion_texts:
          # extract the text
          if fusion_text.find("p"):
            for p in fusion_text.find_all("p"):
              print(p.text)
              try:
                if p and p.text[0].isdigit():
                  
                  text = p.text
                  day, rest = text.split(". ", 1)
                  try:
                    #Extracts just the first number if in the form 22-23
                    print(day)
                    result = re.search("(\d+)", day)
                    print(result.group(1))
                    first_day = result.group(1)
                  except:
                    first_day = day
                  
                  name, rest = rest.split(", ", 1)
                  try:
                    place = rest
                  except:
                    place = "N/A"
                  # extract the href
                  link = p.find("a")["href"]
                  # store the event information

                  #Find type, if #ff0000 ski (ignore) if #339966 trail, keep, else we assume road
                  try:
                    type_color = text.find('a').find('span')
                    if type_color.startswith('color: #ff0000'):
                      break
                    elif type_color.startswith('color: #339966'):
                      type_surface = "Terräng"
                    else:
                      type_surface = "Väg"
                  except:
                    type_surface = "Väg"
                    print("no color style found, choose road")
                  #VERY CLUMPSY MONTH OPERATION
                  for month in months_list:
                    if month in title_heading.text:
                      date_string = months_dict[month]
                      final_date = "2023" + date_string + first_day.strip().zfill(2)
                      break

                  #Fetching geocoordinates
                  # Use the place as a search string
                  # Perform the geocoding request
                  print("kom hit")
                  if place != "N/A":
                    print("geo?")
                    [latitude, longitude] = get_lat_long_goog.get_lat_long_goog(place, access_token)
                    print("geo success")
                  else:
                    latitude = 0;
                    longitude = 0;
                  print("kom hit2")
                  event = {
                    "date": final_date,
                    "day": first_day.strip(),
                    "month": month,
                    "name": name.strip(),
                    "type": type_surface,
                    "place": place.strip(),
                    "website": link,
                    "latitude": latitude,
                    "longitude": longitude
                  }
                  print(event)
                  # add the event to the list of events
                  events.append(event)



              except:
                print("Error: not enough values to unpack")

# write the events to a json file
with open("LK_events.json", "w", encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False)