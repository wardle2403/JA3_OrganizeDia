import csv
import os
import shutil
import re

# Step 1: Read the CSV file and create a dictionary mapping file names to actor names
csv_file_path = 'Game.csv'
output_directory = os.path.dirname(os.path.abspath(__file__))

with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

# Find the indices of the columns with actor names and file names
file_name_column = 'ID'  # Change this to the actual column name for file names
actor_column = 'Voice Actor'  # Change this to the actual column name for actor names
header_row = rows[0]

file_name_column_index = header_row.index(file_name_column)
actor_column_index = header_row.index(actor_column)

# Create a dictionary mapping file names to actor names
file_to_actor = {row[file_name_column_index]: row[actor_column_index] for row in rows}

# Step 2: Create directories for each actor
for actor in set(file_to_actor.values()):
    actor_directory = os.path.join(output_directory, actor)
    os.makedirs(actor_directory, exist_ok=True)

# Step 3: Move files to their respective actor's directory
for file_name, actor in file_to_actor.items():
    source_file_path = os.path.join(output_directory, file_name + '.opus')
    destination_directory = os.path.join(output_directory, actor)
    destination_file_path = os.path.join(destination_directory, file_name + '.opus')

    if os.path.exists(source_file_path):
        shutil.move(source_file_path, destination_file_path)
        print(f"Moved {file_name}.opus to {actor}'s directory.")

# Step 4: Read the variations.lua file
variations_lua_path = 'variations.lua'  # Change this to the actual path of your variations.lua file

variations = []
with open(variations_lua_path, 'r') as lua_file:
    lua_content = lua_file.read()
    keys = re.findall(r'\["(.+?)"\] = {', lua_content)

# Step 5: Move variations to their corresponding actor folders
variations_moved = 0  # Count of moved variations
for key in keys:
    if key in file_to_actor:  # Only process if the key (file name) exists in the CSV data
        actor = file_to_actor[key]
        actor_directory = os.path.join(output_directory, actor)
        variation_file_name = key + '-1'
        
        source_variation_path = os.path.join(output_directory, variation_file_name + '.opus')
        destination_variation_directory = os.path.join(actor_directory, 'variations')
        destination_variation_path = os.path.join(destination_variation_directory, variation_file_name + '.opus')

        if os.path.exists(source_variation_path):
            os.makedirs(destination_variation_directory, exist_ok=True)
            shutil.move(source_variation_path, destination_variation_path)
            print(f"Moved variation {variation_file_name}.opus to {destination_variation_directory}")
            variations_moved += 1

unique_actors = len(set(file_to_actor.values()))
print(f"Files and variations moved successfully! Variations moved: {variations_moved}. Unique actors found: {unique_actors}")
