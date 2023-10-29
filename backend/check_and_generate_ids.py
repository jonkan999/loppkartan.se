import random
import hashlib
import json
import uuid

def generate_unique_id():
    # Generate a unique hash here (replace this with your hash generation logic)
    unique_id = str(uuid.uuid4())
    return unique_id

def check_unique_ids(json_data):
    id_list = []
    modified_ids = {}
    unique = True

    for index, entity in enumerate(json_data):
        entity_id = entity.get('id')  # Assuming 'id' is the key for the hash ID field
        if entity_id in id_list:
            print(f"Non-unique ID found: {entity_id}")
            unique = False
            new_id = generate_unique_id()  # Generate a new unique hash ID
            while new_id in id_list:
                new_id = generate_unique_id()  # Ensure the new ID is unique
            entity['id'] = new_id  # Update the ID in the JSON data
            modified_ids[index] = new_id  # Keep track of modified IDs
            id_list.append(new_id)
        else:
            id_list.append(entity_id)

    if unique:
        print("All IDs are unique!")
    else:
        print("Duplicate IDs found. Modified IDs:")
        for index, new_id in modified_ids.items():
            print(f"Index {index}: New ID - {new_id}")


#retrieve races from production
with open('../all_races_w_formatted_summary.json', encoding='utf-8') as f:
    already_crawled_races = json.load(f)

check_unique_ids(already_crawled_races)

# Write the merged data to a new file, using UTF-8 encoding
with open('all_races_w_formatted_summary_unique_id.json', 'w', encoding='utf-8') as f:
    json.dump(already_crawled_races, f, ensure_ascii=False)
