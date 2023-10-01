import json
import subprocess
import os

# Assuming your script is located in 'C:\Users\Joel\loppkartan.se\backend'
script_directory = os.path.abspath(os.path.dirname(__file__))
venv_activate_command = os.path.join(script_directory, 'backend', 'venv', 'Scripts', 'activate.bat')

# Activate the virtual environment
subprocess.run([venv_activate_command], shell=True)


# crawl pages
subprocess.run(["python", "extract_data_fri_Arena.py"])
subprocess.run(["python", "extract_data_fri_LL.py"])
subprocess.run(["python", "extract_data_jogg_road.py"])
subprocess.run(["python", "extract_data_jogg_trail.py"])
subprocess.run(["python", "extract_data_trailkalendern.py"])

# check existing races
# This is done implicitly in each site crawl

# crawl only new races
subprocess.run(["python", "check_existing_race.py"])

# combine all races
subprocess.run(["python", "all_races.py"])

# get geolocation coordinates
subprocess.run(["python", "get_lat_long_goog.py"])

# sort races by date
subprocess.run(["python", "all_races_sort.py"])

# summarize race URLs
subprocess.run(["python", "summary_by_url.py"])

# format URL summaries
subprocess.run(["python", "format_URL_Summary.py"])

# combine race data with URL summaries
subprocess.run(["python", "all_races_w_summary.py"])

# find county for each race
subprocess.run(["python", "findCounty.py"])

# sort races by date and geolocation
subprocess.run(["python", "sort_on_date_and_lng_lat.py"])