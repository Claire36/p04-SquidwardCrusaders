import sqlite3
import csv
from datetime import datetime

DB_FILE = "pollution.db"

def setup():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS airQuality (id INTEGER PRIMARY KEY, pollutant TEXT, value REAL, state TEXT, year INTEGER);")
    c.execute("CREATE TABLE IF NOT EXISTS congestion (id INTEGER PRIMARY KEY, congestion_index REAL, state TEXT, year INTEGER);")
    c.execute("CREATE TABLE IF NOT EXISTS congestion_short_term(id INTEGER PRIMARY KEY, congestion_index INTEGER, state TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS congestion_long_term(id INTEGER PRIMARY KEY, congestion_index INTEGER, state TEXT);")
    with open("counties.geojson", 'r') as file:
        data = json.load(file)
    c.execute('''
        CREATE TABLE IF NOT EXISTS counties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            geoid TEXT,
            name TEXT,
            statefp TEXT,
            countyfp TEXT,
            land_area INTEGER,
            water_area INTEGER,
            geometry TEXT
        )
    ''')

    for feature in data['features']:
        props = feature['properties']
        geom = json.dumps(feature['geometry'])  # Store geometry as JSON string

        cur.execute('''
            INSERT INTO counties (geoid, name, statefp, countyfp, land_area, water_area, geometry)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            props.get('GEOID'),
            props.get('NAME'),
            props.get('STATEFP'),
            props.get('COUNTYFP'),
            props.get('ALAND'),
            props.get('AWATER'),
            geom
        ))
    db.commit()
    db.close()
