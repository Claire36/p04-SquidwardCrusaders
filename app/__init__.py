from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3
import hashlib
from db import *
import functools, datetime

app = Flask(__name__)
app.secret_key = 'SquidwardT'

congestion = open("static/congestion_filtered_transposed.csv", "r")
congestion = congestion.readlines()[0].strip().split(",")[1:]
conglist = []
for item in congestion:
    conglist.append(item)

pollution = open("static/pollution_CO.csv", "r")
pollution = pollution.readlines()[0].strip().split(",")[1:]
polllist = []
for x in pollution:
    polllist.append(x)

# ─────────────────────────────  helpers ──────────────────────────────
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def root():
    return render_template('home.html', user=session.get('username'))

# @app.route('/map/O3')
# def map():
#     return render_template('map.html')

@app.route('/pollution/<pollutant>', methods=['GET', 'POST'])
def pollution(pollutant):
    if 'username' not in session:
        return redirect('/login')
    if request.method == "POST":
        content = request.form['comment']
        user = session['username']
        map = pollutant
        conn = get_db_connection()
        conn.execute("INSERT INTO comments (username, content, map) VALUES (?, ?, ?)", (user, content, map))
        conn.commit()
        conn.close()
    conn = get_db_connection()
    comments = conn.execute("SELECT * FROM comments WHERE map = ?", (pollutant,)).fetchall()
    conn.close()
    return render_template('map.html', pollutant=pollutant, comments=comments, user=session.get('username'))

@app.route('/congestion')
def congestion():
    return render_template('congestion.html', user=session.get('username'))

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        city = request.form['cities']
        county = request.form['counties']
        pollutant = request.form['pollutants']
        return render_template('compare.html', city=city, county=county, pollutant=pollutant, congestions=conglist, pollutions=polllist)
    return render_template('compare.html', congestions=conglist, pollutions=polllist, user=session.get('username'))

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')
'''
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?,?)",
                (username, pw_hash),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Username taken")
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? and password_hash = ?", (username, password)).fetchone()
        conn.close()
        if user:
            session['username'] = user['username']
            return redirect('/')
    return render_template('login.html')
'''
            session["user_id"] = user["id"]
            return redirect(request.args.get("next", "/"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")
'''

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
	app.run(host='0.0.0.0')