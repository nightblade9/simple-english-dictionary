#!/bin/python3
# Filters possibly objectionable content based on keywords; probably over-filters.
import json, os

merged_json = {}
filter_out_words = []

with open(os.path.join("data", "filter_words.txt"), "r") as input_file:
    filter_out_words = [x.strip().lower() for x in input_file.readlines()]

with open(os.path.join("processed", "merged.json"), "r") as input_file:
    contents = input_file.read()
    merged_json = json.loads(contents)

to_delete = []

for word in merged_json.keys():
    for filtered_word in filter_out_words:
        if filtered_word.lower() in word.lower():
            to_delete.append(word)
            break

    data = merged_json[word]

    meanings = data["MEANINGS"]
    filtered_meanings = []

    for i in range(len(meanings)):
        meaning_data = meanings[i]
        description = meaning_data[1].lower()
        
        filter_out = False
        for filter_word in filter_out_words:
            if filter_word in description:
                filter_out = True
                break
        
        if not filter_out:
            filtered_meanings.append(meaning_data)

    data["MEANINGS"] = filtered_meanings

    synonyms = []
    for synonym in data["SYNONYMS"]:
        if not synonym.lower() in filter_out_words:
            synonyms.append(synonym)
    
    data["SYNONYMS"] = synonyms

    antonyms = []
    for antonym in data["ANTONYMS"]:
        if not antonym.lower() in filter_out_words:
            antonyms.append(antonym)

    data["ANTONYMS"] = antonyms

for delete_me in to_delete:
    del merged_json[delete_me]

output_file = open(os.path.join("processed", "filtered.json"), "w")
output_file.write(json.dumps(merged_json))

print("Wrote out processed/filtered.json")