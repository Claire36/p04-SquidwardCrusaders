import sqlite3
import csv
from datetime import datetime

DB_FILE = "data.db"

import_pollution_data("pollution_2000_2023.csv")
import_congestion_data("table_01_71q113.csv")

def import_pollution_data(filepath):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, username TEXT, content TEXT, map TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS airQuality (id INTEGER PRIMARY KEY, pollutant TEXT, value REAL, state TEXT, year INTEGER, userID INTEGER);")
    c.execute("CREATE TABLE IF NOT EXISTS congestion (id INTEGER PRIMARY KEY, congestion_index REAL, state TEXT, userID INTEGER, year INTEGER);")

'''
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                year = datetime.strptime(row['Date'], "%Y-%m-%d").year
                state = row['State']
                pollutants = {
                    'O3 Mean': float(row['O3 Mean']),
                    'CO Mean': float(row['CO Mean']),
                    'SO2 Mean': float(row['SO2 Mean']),
                    'NO2 Mean': float(row['NO2 Mean']),
                }

                for pollutant, value in pollutants.items():
                    c.execute("""
                        INSERT INTO airQuality (pollutant, value, state, year)
                        VALUES (?, ?, ?, ?);
                    """, (pollutant, value, state, year))

            except Exception as e:
                print(f"Error processing row {row}: {e}")

    db.commit()
    db.close()

def import_congestion_data(filepath):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()

    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    data_rows = rows[5:]  # Skip metadata lines

    for row in data_rows:
        if len(row) < 30:
            continue

        city_state = row[0].strip('"')
        state = city_state.split(",")[-1].strip()

        try:
            # Years from 1982 to 2011 (with 1983–1984 missing)
            for i, val in enumerate(row[2:26]):
                year = 1982 + (i if i < 2 else i + 1)  # Skipping 1983–1984
                if val:
                    c.execute("""
                        INSERT INTO congestion (congestion_index, state, year)
                        VALUES (?, ?, ?);
                    """, (float(val), state, year))

            # Short-term (2006–2011) and long-term (1982–2011) values
            short_term_value = row[26]
            long_term_value = row[28]

            if short_term_value:
                c.execute("""
                    INSERT INTO congestion_short_term (congestion_index, state)
                    VALUES (?, ?);
                """, (int(short_term_value), state))

            if long_term_value:
                c.execute("""
                    INSERT INTO congestion_long_term (congestion_index, state)
                    VALUES (?, ?);
                """, (int(long_term_value), state))

        except Exception as e:
            print(f"Error in row {row[0]}: {e}")
'''
    db.commit()
    db.close()
