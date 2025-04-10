import json
import sqlite3
import csv
from flask import Flask, render_template, url_for, request, redirect, session

def build_county_lookup(geojson_path):
    with open(geojson_path, 'r') as f:
        geojson = json.load(f)

    lookup = {}
    for feature in geojson['features']:
        name = feature['properties']['NAME']
        statefp = feature['properties']['STATEFP']
        geoid = feature['properties']['GEOID']
        # Assuming you're using state abbreviations in your dataset
        state_abbr = fips_to_state_abbr[statefp]  # You’ll need a FIPS-to-abbr dict
        key = f"{name}, {state_abbr}"  # Like "San Francisco, CA"
        lookup[key] = geoid
    return lookup

def load_county_shades(csv_path, county_lookup):
    county_shades = {}
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                name_state = row[0].strip('"')  # "Akron, OH"
                value = float(row[-4])  # Second-leftmost numeric column
                geoid = county_lookup.get(name_state)
                if geoid:
                    county_shades[geoid] = value
            except (IndexError, ValueError):
                continue
    return county_shades

def normalize_shades(shades_dict):
    values = list(shades_dict.values())
    min_val = min(values)
    max_val = max(values)
    return {
        k: (v - min_val) / (max_val - min_val) if max_val != min_val else 0.5
        for k, v in shades_dict.items()
    }
