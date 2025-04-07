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
    db.commit()
    db.close()

def addCongestionOverall():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    with open('congestion.csv', 'r') as congestion:
        csv_reader = csv.reader(congestion, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i not in (range(1,4) and range(104, 124)):
                db.execute("INSERT INTO congestion_long_term(congestion_index, state) VALUES (?, ?)", (row[28], row[0]))
    db.commit()
    db.close()

def getCongestionOverall():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * FROM congestion_long_term")
    results = c.fetchall()
    db.close()
    return results
