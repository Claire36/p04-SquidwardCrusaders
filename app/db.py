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
    c.execute("CREATE TABLE IF NOT EXISTS congestion_long_term(id INTEGER PRIMARY KEY, congestion_index INTEGER, state TEXT);")

    db.commit()
    db.close()

def addCongestionOverall():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    with open('congestion.csv', 'r') as congestion:
        csv_reader = csv.reader(congestion, delimeter=',')
        for row in csv_reader:
             db.execute("INSERT INTO congestion_long_term(id, congestion_index, state) VALUES (?, ?, ?, ?)", (id, csvValue[28], csvValue[0]))
    db.commit()
    db.close()

def getCongestionOverall():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * FROM " + congestion_long_term + "")
    db.commit()
    db.close()
