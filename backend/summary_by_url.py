import json
import requests
import config

access_token = config.MEANINGCLOUD_SUMMARY_API
url = "https://api.meaningcloud.com/summarization-1.0"

# Open the all_races.json file and load its contents into a Python object
with open('all_races.json', encoding='utf-8') as f:
    races = json.load(f)

url_summary = {}

# Loop through each row in the races object
for race in races:
    # Extract the URL from the row
    race_url = race['website']
    
    # Check if the URL has already been processed
    if race_url in url_summary:
        continue
    
    # Call the MeaningCloud API to generate a summary for the URL
    payload = {
        'key': access_token,
        'url': race_url,
        'sentences': 3  # Change the number of sentences to suit your needs
    }
    response = requests.post(url, data=payload)
    
    # Extract the summary from the response
    print(response.json())
    try:
      summary = response.json()['summary']
    except KeyError:
        summary = "Error: Could not generate summary"
        print("Error: Could not generate summary for URL: ", race_url)
    
    # Add the URL and summary to the url_summary dictionary
    url_summary[race_url] = summary


# Save the url_summary dictionary as a JSON file
with open("URL_Summary.json", "w", encoding='utf-8') as f:
    json.dump(url_summary, f, ensure_ascii=False)


