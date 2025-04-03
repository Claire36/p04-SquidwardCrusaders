import sqlite3
import csv
from datetime import datetime

DB_FILE = "pollution.db"

def setup():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS airQuality (id INTEGER PRIMARY KEY, pollutant TEXT: 'O3', 'CO', 'SO2', 'NO2', value REAL, state TEXT, year INTEGER, userID INTEGER);")
    c.execute("CREATE TABLE IF NOT EXISTS congestion (id INTEGER PRIMARY KEY, congestion_index REAL, state TEXT, userID INTEGER, year INTEGER);")
    db.commit()
    db.close()
