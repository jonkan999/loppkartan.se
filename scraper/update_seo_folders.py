import os
import shutil
import yaml
from datetime import datetime

def clean_filename(name):
  name = name.replace('-', ' ').replace('/', '').replace('å', 'a').replace('ä', 'a').replace('ö', 'o').replace('Å', 'A').replace('Ä', 'A').replace('Ö', 'O').lower()
  return '-'.join(name.split()).lower()

# Read the general configuration file
with open("../collection_configuration/general_config.yaml", 'r', encoding='utf-8') as f:
  config = yaml.safe_load(f)

# Define the parent folder
parent_folder = "../"

# Create a folder called "lan"
lan_folder = os.path.join(parent_folder, "lan")
os.makedirs(lan_folder, exist_ok=True)

# Iterate over the county mapping
sitemap_string = ""

for county, county_value in config["county_mapping"].items():
  print(f"Creating folder for {county}")
  # Create a folder with the same name as the county within the "lan" folder
  folder_name = clean_filename(county)
  folder_path = os.path.join(lan_folder, folder_name)
  os.makedirs(folder_path, exist_ok=True)

  # Copy lopplistan.html to index.html in the folder
  shutil.copy2("../lopplistan.html", os.path.join(folder_path, "index.html"))

  # Replace the field containing the county selector and add "selected"
  with open(os.path.join(folder_path, "index.html"), 'r+', encoding='utf-8') as file:
    string_to_replace = f"""<option value="{county}">{county}</option>"""
    string_to_replace_with = f"""<option value="{county}" selected>{county}</option>"""
    content = file.read()
    content = content.replace(string_to_replace, string_to_replace_with)
    content = content.replace(config["title_find"], config["seo_county_title"] % county_value)
    content = content.replace(config["description"], config["seo_county_description"] % county_value)
    file.seek(0)
    file.write(content)
    file.truncate()


  # Generate sitemap string
  sitemap_string += f"<url>\n"
  sitemap_string += f"  <loc>https://loppkartan.se/lan/{folder_name}/index.html</loc>\n"
  # Get the current date
  current_date = datetime.now().date()

  # Format the date as "YYYY-MM-DD"
  formatted_date = current_date.strftime("%Y-%m-%d")

  sitemap_string += f"  <lastmod>{formatted_date}T14:19:49+00:00</lastmod>\n"
  sitemap_string += f"  <priority>0.75</priority>\n"
  sitemap_string += f"</url>\n"

print("this can be used to insert into sitemap.xml")
print(sitemap_string)
