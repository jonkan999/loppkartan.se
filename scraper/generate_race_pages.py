import os
import base64
from jinja2 import Environment, FileSystemLoader
from PIL import Image
import io
import json
from datetime import datetime

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set up Jinja2 environment
template_path = os.path.join(script_dir, "race_page_template.html")
env = Environment(loader=FileSystemLoader(searchpath=script_dir))
# Register the filter function with the Jinja2 environment
template = env.get_template("race_page_template.html")

current_date = datetime.now().strftime("%Y%m%d")

def read_all_races():
    try:
        with open('approved_races_raw.json', 'r', encoding='utf-8') as races_file:
            races_data = json.load(races_file)
            # Filter races with 'long_summary' key
            date_filtered_races = [race for race in races_data if race.get("date", "") >= current_date]
            races_with_long_summary = [race for race in date_filtered_races if 'long_summary' in race]
            return races_with_long_summary
    except FileNotFoundError:
        print("File 'approved_races_raw.json' not found.")
        return []

def read_all_images():
    try:
        with open('images.json', 'r', encoding='utf-8') as images_file:
            images_data = json.load(images_file)
            return images_data
    except FileNotFoundError:
        print("File 'images.json' not found.")
        return []

def join_images_and_races(races, images):
    joined_data = []

    for race in races:
        race_id = race["id"]

        for image in images:
            if type(image) == str:
                continue
            image_id = image["id"]
            
            # Check if race_id is equal to image_id
            if race_id == image_id:
                joined_data.append({**race, 'images': image['images']})
                break  # No need to continue checking once a match is found
    return joined_data

def save_webp_image(base64_data, output_path):
    # Decode the base64 data
    decoded_data = base64.b64decode(base64_data)

    # Open the image from the decoded data
    img = Image.open(io.BytesIO(decoded_data))

    # Save the image as a WebP file
    img.save(output_path, "WEBP", quality=100)

def clean_filename(name):
    name = name.replace('-', ' ').replace('/', '').replace('å', 'a').replace('ä', 'a').replace('ö', 'o').lower()
    return '-'.join(name.split()).lower()

def save_images(images, output_folder, filename_prefix):
    image_paths = []
    index_of_first_image = 1
    for i, image_data in enumerate(images):
        if image_data is not None:
            image_filename = f"{filename_prefix}_{index_of_first_image}.webp"
            image_path = os.path.join(output_folder, image_filename)
            # Check if the image file already exists
            if not os.path.exists(image_path):
                save_webp_image(image_data, image_path)
            else:
                print(f"Skipped saving image '{image_filename}' as it already exists.")
            image_paths.append(image_filename)
            index_of_first_image += 1

    return image_paths

def main():
    races = read_all_races()
    images = read_all_images()
    print(images[0]["id"])
    print(len(races))
    races_w_images = join_images_and_races(races, images)

    # Read all_races_w_formatted_summary.json
    try:
        with open('../all_races_w_formatted_summary.json', 'r', encoding='utf-8') as all_races_file:
            unfiltered_races = json.load(all_races_file)
            all_races_data = [race for race in unfiltered_races if race.get("date", "") >= current_date]
    except FileNotFoundError:
        print("File '../all_races_w_formatted_summary.json' not found.")
        all_races_data = []
    
    for race in races_w_images:
        print("Generates:" + race["name"] + ".html")
        cleaned_name = clean_filename(race['name'])

        # Save images associated with the race
        # Define the relative path from the root directory to your images folder
        relative_path = "../race-pages/img"

        # Combine the root directory and the relative path to create the full path
        images_folder = os.path.join(script_dir, relative_path)

        # Create the directory if it doesn't exist
        os.makedirs(images_folder, exist_ok=True)
        print("Images saved to: " + images_folder + "with name: " + cleaned_name)
        image_paths = save_images(race['images'], images_folder, cleaned_name)
        context = {
            'race': race,
            'image_paths': image_paths  # Pass the filename prefix here
        }

        # Render the Jinja2 template with the data
        html_content = template.render(context=context)

        # Create a new HTML file
        relative_path = "../race-pages"

        # Combine the root directory and the relative path to create the full path
        os_relative_path = os.path.join(script_dir, relative_path)
        output_path = os.path.join(os_relative_path, f"{cleaned_name}.html")

        if not os.path.exists(output_path):
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(html_content)
            print(f"HTML file '{output_path}' created.")
        else:
            print(f"Skipped creating HTML file '{output_path}' as it already exists.")

        # If race already in active races, update "website" keys in all_races_data
        new_race=True
        for i, all_race in enumerate(all_races_data):
            if all_race["id"] == race["id"]:
                all_races_data[i]["website_organizer"] = race["website"]
                all_races_data[i]["website"] = f'/race-pages/{cleaned_name}.html'
                new_race = False
                break
            #Else append the race to all_races_data
        if new_race:
            #Update website
            race["website_organizer"] = race["website"]
            race["website"] = f'/race-pages/{cleaned_name}.html'
            # Keep only specific keys from the race dictionary
            keys_to_keep = [
                "date", "type", "name", "distance", "distance_m",
                "place", "latitude", "longitude", "organizer",
                "website", "src_url", "county",
                 "id", "summary", "website_organizer"
            ]

            # Create a new dictionary with only the specified keys
            selected_race = {key: race[key] for key in keys_to_keep}
            selected_race["new_version"] = True

            all_races_data.append(selected_race)


    #Sort races
    # Save the modified all_races_data
    try:
        all_races_data = sorted(all_races_data, key=lambda x: (x["date"], x["longitude"], x["latitude"]))
        with open('../all_races_w_formatted_summary.json', 'w', encoding='utf-8') as all_races_file:
            json.dump(all_races_data, all_races_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("File '../all_races_w_formatted_summary.json' not found.")

    print("HTML files generated successfully.")

    # Update sitemap.xml

    new_urls = []
    for i, race in enumerate(races):
        # Extract the race name from the website URL
        race_name = race["website"].split("/")[-1].replace(".html", "")
        sitemap_url = f"https://loppkartan.se/race-pages/{clean_filename(race['name'])}.html"
        sitemap_url = sitemap_url.replace('&', '&amp;') #escaping ampersand
        new_urls.append(f'<url>\n  <loc>{sitemap_url}</loc>\n  <lastmod>{datetime.now().isoformat()}+00:00</lastmod>\n  <priority>0.8</priority>\n</url>')

    # Append new URLs to sitemap_top.xml
    try:
        with open('../sitemap_top.xml', 'r', encoding='utf-8') as sitemap_top_file:
            sitemap_top_content = sitemap_top_file.read()

        # Find the closing </urlset> tag in sitemap_top.xml
        index = sitemap_top_content.rfind('</urlset>')
        if index == -1:
            print("Invalid sitemap_top.xml file format. Could not find </urlset> tag.")
        else:
            # Create the new <url> entries
            new_entries = '\n'.join(new_urls)

            # Insert the new entries before the closing </urlset> tag
            updated_sitemap_top_content = sitemap_top_content[:index] + new_entries + sitemap_top_content[index:]

            # Write the updated content back to sitemap_top.xml
            with open('../sitemap.xml', 'w', encoding='utf-8') as sitemap_file:
                sitemap_file.write(updated_sitemap_top_content)
    except FileNotFoundError:
        print("File 'sitemap_top.xml' not found.")
    except Exception as e:
        print(f"An error occurred while updating 'sitemap_top.xml': {e}")



if __name__ == "__main__":
    main()