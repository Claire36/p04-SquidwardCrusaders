from flask import Flask, render_template, url_for, request, redirect
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

@app.route('/test')
def test():
    return "<h1>Test</h1>"

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

if __name__ == "__main__":
	app.run(host='0.0.0.0')

