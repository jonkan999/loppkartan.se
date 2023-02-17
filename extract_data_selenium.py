import json
import config
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Use the access token
access_token = config.GOOGLE_GEOCODING_API_KEY

url = "https://friidrott.euwest01.umbraco.io/tavling-landslag/tavling/tavlingskalender/tavlingar-i-sverige/langlopp/"



# Set the options to run the browser in headless mode
options = Options()
""" options.add_argument("--headless")
options.add_argument("--disable-gpu") """
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--disable-remote-fonts')
options.add_argument('--disable-geolocation')
options.add_argument('--disable-infobars')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-logging')
options.add_argument('--disable-web-security')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-cookie-encryption')
options.add_argument('--incognito')
options.add_argument('--disable-plugins-discovery')
options.add_argument('--disable-plugins')
options.add_argument('--disable-sync')

# Initialize the Chrome driver and load the page
driver = webdriver.Chrome(options=options)
# assuming driver is your Selenium webdriver instance
driver.execute_script("window.cookietractor = null;")
driver.get(url)

months_dict = {'MARS': '03', 'APRIL': '04', 'MAJ': '05', 'JUNI': '06', 'JULI': '07', 'AUGUSTI': '08', 'SEPTEMBER': '09', 'OKTOBER': '10', 'NOVEMBER': '11', 'DECEMBER': '12'}
months_list = list(months_dict.keys())

data = []

time.sleep(1)

# Click show filters
driver.find_element(By.XPATH, "//button[@aria-label='Visa eller dölj filters för tävlingskalendern']").click()
time.sleep(1)
# Click välj gren
filters = driver.find_elements(By.XPATH, "//button[@id='categoryFilterBtn']")
filters[3].click()
time.sleep(1)

dropdown = driver.find_element(By.XPATH, "//div[@data-filter-group='gren']")

selector_list = dropdown.find_elements(By.XPATH, ".//button")

print(selector_list[0].find_element(By.XPATH, ".//span[@class='label']").text)
print(selector_list[1].get_attribute("innerHTML"))


for item in selector_list:
    try:
        distance_elem = item.find_element(By.XPATH, ".//span[@class='label']")
        print(distance_elem.text)
        if distance_elem.text == "Visa alla":
            continue
        # Simulate a click on the filter item
        item.click()
        try:
            print("clicked")
            print(item.get_attribute("innerHTML"))
            time.sleep(2)
            distance = distance_elem.text.strip()
            distance_regex = re.compile(r"(\d+(?:[,.]\d+)?)\s*(km|m|Marathon|Halvmarathon)")
            matches = distance_regex.search(distance)
            if matches:
                distance_value, distance_unit = matches.groups()
                print(distance_unit)
                if "/" in distance_value:
                    distance_value = distance_value.split("/")[0]
                if distance_unit == "km":
                    distance_value = int(float(distance_value.replace(",", ".")) * 1000)
                elif distance_unit == "m":
                    distance_value = int(distance_value.replace(",", "."))
                elif distance_unit == "Marathon":
                    distance_value = 42195
                elif distance_unit == "Halvmarathon":
                    distance_value = 21098
                else:
                    distance_value = None
            else:
                distance_value = None
            for container in driver.find_elements(By.XPATH, "//div[@class='calendar__container']"):
                try:
                    month_name = container.find_element(By.XPATH, ".//h2[@class='heading']").text.strip()
                except:
                    continue

                print(month_name)
                if month_name in months_dict:
                    month_num = months_dict[month_name]
                    print(month_num)
                    events = container.find_elements(By.XPATH, ".//li[@class='calendar-item' and not(@style='display: none')]")
                    print("found events")
                    print(events[0].get_attribute("innerHTML"))
                    for event in events:
                        print(event.text)
                        date_text = event.find_element(By.XPATH, ".//time[@class='calendar-item__date']")
                        print(date_text.text)
                        day = date_text.text.split("-")[0]
                        proper_date = '2023' + month_num + day.zfill(2)
                        # Type mapping
                        mapping = {
                            "Trail": "trail",
                            "Väg": "road",
                            "Terräng": "terrain",
                            "Stafett": "relay"
                        }
                        type = event.find_element(By.XPATH, ".//p[@class='calendar-item__type']").text.strip()
                        translated_type = mapping.get(type, type)
                        print("here")
                        texts = event.find_elements(By.XPATH, ".//p[@class='calendar-item__text']")
                        name = texts[1].text.strip()
                        print(name)
                        place = texts[2].text.strip()
                        print(place)
                        organizer = texts[3].text.strip()
                        print(texts[1].get_attribute('innerHTML'))
                        element = texts[1].find_element(By.XPATH, ".//a")
                        print(element.get_attribute('href'))
                        website = element.get_attribute('href')
                        #Fetching geocoordinates
                        # Use the place as a search string
                        # Perform the geocoding request
                        #[latitude, longitude] = [0,0]#get_lat_long_goog.get_lat_long_goog(place, access_token)
                        latitude = 0
                        longitude = 0
                        event_data = {"date": proper_date, "month": month_name, "day": day, "type": translated_type, "name": name, "distance": distance,"distance_m": distance_value, "place": place,"latitude": latitude, "longitude": longitude, "organizer": organizer, "website": website}
                        data.append(event_data)
                        print(element.get_attribute('href'))
        except:
            #efore closing we click out the filter we clicked in
            item.click()
            time.sleep(2)
    except:
        print("something went wrong before the click ")

with open("events.json", "w", encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)