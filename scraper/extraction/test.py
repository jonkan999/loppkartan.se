import requests
from bs4 import BeautifulSoup

def main():

    subdomain = "jogg"
    url = "https://www.jogg.se/Kalender/Tavlingar.aspx?aar=2024&mon=13&fdist=0&tdist=1000&type=0&country=1&region=0&tlopp=False&relay=False&surface=&tridist=0&title=1"
    
    
    response = requests.get(url)



    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        calendar_items = soup.find_all("div", class_="calendaritem")
        for item in calendar_items:
            if "notOnMarathon" not in item["class"] and "weeknumber" not in item["class"]:
                name_div = item.find("div", class_="name")
                name = name_div.text.strip()
                website = "https://www.jogg.se/"+name_div.find("a").get("href")
                date_div = item.find("div", class_="dateInfo")
                date_text = date_div.text.strip()

                day = date_text.split(" ")[1].zfill(2)
                month_name = date_text.split(" ")[2]
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
                proper_date = f"2024{month_num}{day}"
                distance_div = item.find("div", class_="distanceInfo")
                distance_str = distance_div.text.strip()
                distance_m = 0
                if distance_str.endswith("km"):
                    try:
                        distance_part=distance_str.split(" ")[0]
                        distance_km = float(distance_part.split(",")[0])
                        distance_m = int(distance_km * 1000)
                    except ValueError:
                        pass
                #mappig out backyard ultras
                print(name)
                print(name.find("ackyard"))
                if name.find("ackyard") != -1:
                    distance_m = "backyard"
                    race_type = "backyard"

                place_div = item.find("div", class_="city")
                place = place_div.text.strip()
                organizer = ""
                website_ai_fallback = name + " " + place + " " + distance_str
                print(race_type)

    else:
        print("Error: Could not retrieve source URL:" + url )

    race_collection.append_or_create_source_json(subdomain)
    race_collection.append_or_create_source_json()
    print("Finished crawling " + url)

if __name__ == "__main__":
    main()

