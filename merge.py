#!/bin/python3
# Reads all the files in /data and merges them into "processed/merged.json"
import glob, json

read_files = glob.glob("data/*.json")
output_list = []

for f in read_files:
    with open(f, "rb") as input_file:
        output_list.append(json.load(input_file))

combined_json = {}
all_items = {}
for json_file in output_list:
    all_items.update(json_file)

combined_json = str(all_items)

output_file = open('merged.json', 'w')
output_file.write(str(combined_json))