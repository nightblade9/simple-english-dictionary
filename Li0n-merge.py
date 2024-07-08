#!/bin/python3
### Claude ai fork of the merge.py file  JSON l10n
### creates pot , tmx , jsonl10n as well.
### useful for Bilingual or multilingual dictionary builds
import glob
import json
import os
from translate.storage.tmx import tmxfile
from translate.storage.jsonl10n import JsonFile
from translate.storage.po import pofile

def flatten_meaning(meaning):
    if isinstance(meaning, str):
        return meaning
    elif isinstance(meaning, list):
        return ' '.join(flatten_meaning(item) for item in meaning)
    else:
        return str(meaning)

# Reads all the files in /data and merges them into "processed/merged.json"
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

# Create i18n-compatible JSON and TMX file
i18n_json = {"en": {}}
tmx = tmxfile()

for key, value in combined_json.items():
    # Get the first meaning or an empty string if no meanings
    first_meaning = value["MEANINGS"][0] if value["MEANINGS"] else ""
    
    # Flatten the meaning
    flattened_meaning = flatten_meaning(first_meaning)
    
    # Add to i18n_json
    i18n_json["en"][key] = flattened_meaning
    
    # Add to TMX
    tmx.addtranslation(key, "en", flattened_meaning, "en")

# Write outputs
os.makedirs("processed", exist_ok=True)

with open(os.path.join("processed", "merged.json"), "w") as output_file:
    json.dump(combined_json, output_file, indent=2)

with open(os.path.join("processed", "i18n.json"), "w") as i18n_file:
    json.dump(i18n_json, i18n_file, indent=2)

# Write TMX file
with open(os.path.join("processed", "export.tmx"), "wb") as tmx_file:
    tmx.serialize(tmx_file)

# Create JSON l10n file
jsonl10n = JsonFile()
jsonl10n.settargetlanguage('en')
for key, value in i18n_json["en"].items():
    jsonl10n.addunit(jsonl10n.UnitClass(source=key, target=value))

with open(os.path.join("processed", "l10n.json"), "wb") as l10n_file:
    jsonl10n.serialize(l10n_file)

# Create PO file
po = pofile()
po.settargetlanguage('en')
for key, value in i18n_json["en"].items():
    unit = po.UnitClass(source=key, target=value)
    po.addunit(unit)

with open(os.path.join("processed", "messages.po"), "wb") as po_file:
    po.serialize(po_file)
