#!/bin/python3
# Reads all the files in /data and merges them into "processed/merged.json"
import glob, json, os

read_files = glob.glob(os.path.join("data", "*.json"))
output_list = []

for f in read_files:
    with open(f, "rb") as input_file:
        output_list.append(json.load(input_file))

combined_json = {}
all_items = {}
for json_file in output_list:
    all_items.update(json_file)

combined_json = all_items

# Process MORE: convert meanings into a list.
# Instead of "MEANINGS": { "1": ..., "2": ...}, we want: "MEANINGS": [...]
# This does not preserve the original order of meanings.
for key in combined_json:
    element = combined_json[key]
    meanings = element["MEANINGS"]
    meanings_list = list(meanings.values())
    element["MEANINGS"] = meanings_list
    
output_file = open(os.path.join("processed", "merged.json"), "w")
output_file.write(json.dumps(combined_json))