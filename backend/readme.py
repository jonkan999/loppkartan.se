import json
import subprocess

# crawl pages
subprocess.run(["python", "backend/extract_data_fri_Arena.py"])
subprocess.run(["python", "backend/extract_data_fri_LL.py"])
subprocess.run(["python", "backend/extract_data_jogg_road.py"])
subprocess.run(["python", "backend/extract_data_jogg_trail.py"])
subprocess.run(["python", "backend/extract_data_trailkalendern.py"])

# check existing races
# This is done implicitly in each site crawl

# crawl only new races
subprocess.run(["python", "backend/check_existing_race.py"])

# combine all races
subprocess.run(["python", "backend/all_races.py"])

# get geolocation coordinates
subprocess.run(["python", "backend/get_lat_long_goog.py"])

# sort races by date
subprocess.run(["python", "backend/all_races_sort.py"])

# summarize race URLs
subprocess.run(["python", "backend/summary_by_url.py"])

# format URL summaries
subprocess.run(["python", "backend/format_URL_Summary.py"])

# combine race data with URL summaries
subprocess.run(["python", "backend/all_races_w_summary.py"])

# find county for each race
subprocess.run(["python", "backend/findCounty.py"])

# sort races by date and geolocation
subprocess.run(["python", "backend/sort_on_date_and_lng_lat.py"])