import os
import shutil
import json
import subprocess
import time
import subprocess

def copy_missing_files(file_paths, target_folder):
    for file_path in file_paths:
        target_path = os.path.join(target_folder, os.path.basename(file_path))
        shutil.copy(file_path, target_path)
        print(f"File copied: {target_path}")

def copy_missing_folders(folders_to_check, is_initial=False):
  parent_folder = os.path.dirname(os.getcwd())

  for folder in folders_to_check:
    folder_path = os.path.join(parent_folder, folder)
    if is_initial:
      shutil.rmtree(folder_path)
      shutil.copytree(folder, folder_path)
    if not os.path.exists(folder_path):
      shutil.copytree(folder, folder_path)

  gitignore_path = os.path.join(parent_folder, ".gitignore")
  if not os.path.exists(gitignore_path):
    shutil.copy(".gitignore", gitignore_path)

def copy_empty_json():
  parent_folder = os.path.dirname(os.getcwd())
  json_file = "all_races_w_formatted_summary.json"
  json_path = os.path.join(parent_folder, json_file)
  
  current_date = time.strftime("%Y%m%d")
  future_date = (time.time() + (4 * 7 * 24 * 60 * 60))  # 4 weeks from now
  future_date_str = time.strftime("%Y%m%d", time.localtime(future_date))
  
  race_data = [{
    "date": future_date_str,
    "type": "trail",
    "name": "Night Trail Farsta",
    "distance": "Night Trail Farsta",
    "distance_m": [
      6000,
      11000
    ],
    "place": "Night Trail Farsta",
    "latitude": 59.2444552,
    "longitude": 18.0902987,
    "organizer": "",
    "website": "/race-pages/night-trail-farsta.html",
    "src_url": "https://www.trailrunningsweden.se/trailkalendern/",
    "id": "night-trail-farsta_" + future_date_str + "_httpswwwtrailrunningswedensetrailkalendern",
    "summary": "I lördags arrangerade vi vår årliga terränglöpning med distanserna 6 km och 11 km. Deltagarna kom i alla åldrar och löparnivåer, och det var fantastiskt att se så många människor njuta av den vackra naturen. Vi är glada att främja hälsosam livsstil och ser fram emot att fortsätta arrangera dessa evenemang i framtiden! Tack till alla deltagare, volontärer och supportrar!",
    "county": "Stockholms",
    "website_organizer": "https://trailrunningsweden.se/events/farsta-night-trail-2022/"
  }]
  
  if not os.path.exists(json_path):
    with open(json_path, 'w') as f:
      json.dump(race_data, f)

if __name__ == "__main__":
  subprocess.run(["python", "-m", "venv", "venv"])  # Replace "myenv" with the desired name for your virtual environment
  #need to figure this out, run manual for now
  #venv\\Scripts\\Activate.ps1
  #pip install jinja2 pyyaml
  #subprocess.run(["venv\\Scripts\\Activate.ps1"], shell=True)  # Activate the virtual environment
  #subprocess.run(["pip", "install", "jinja2", "pyyaml"])  # Install Jinja2 and PyYAML
  is_initial=False
  folders_to_check = ['css', 'img', 'js', 'netlify', 'scraper', 'svg', 'collection_configuration']
  copy_missing_folders(folders_to_check, is_initial)
  # List of files to copy during initialization
  files_to_copy = ['lopplistan_template.html', 'index_template.html']

  copy_empty_json()
  #if is_initial: RUN THESE TWO MANUALLY FOR NOW
  #  copy_missing_files(files_to_copy, os.path.dirname(os.getcwd()))
  #  subprocess.run(["python", "initiate_main_list.py"])
  #  subprocess.run(["python", "initiate_main_map.py"])
  #  subprocess.run(["python", "initiate_add_auxilliary_pages.py"])
  #  print("Initial setup complete.")

  
