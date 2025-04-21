from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'SquidwardT'

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/map')
def map():
    return render_template('line.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, password_hash) VALUES (? ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? and password_hash = ?", (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect('/')
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/map/<pollutant>')
def map_view(pollutant):
    return render_template('map.html', pollutant=pollutant)

@app.route('/data/<pollutant>')
def data_api(pollutant):
    conn = get_db_connection()
    data = conn.execute(
        "SELECT year, state, value FROM airQuality WHERE pollutant = ? ORDER BY year",
        (pollutant,)
    ).fetchall()
    conn.close()
    return {'data': [dict(row) for row in data]}

@app.route('/congestion_data')
def congestion_api():
    conn = get_db_connection()
    data = conn.execute("SELECT year, state, congestion_index FROM congestion ORDER BY year").fetchall()
    conn.close()
    return {'data': [dict(row) for row in data]}

if __name__ == "__main__":
	app.run(host='0.0.0.0')
