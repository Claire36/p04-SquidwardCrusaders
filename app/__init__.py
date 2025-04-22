from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3
import hashlib
from db import *
setup()
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
    return render_template('home.html')

@app.route('/map/O3')
def map():
    return render_template('map.html')

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
    return render_template('map.html', pollutant=pollutant, comments=comments)

@app.route('/congestion')
def congestion():
    return render_template('congestion.html')

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        city = request.form['cities']
        county = request.form['counties']
        pollutant = request.form['pollutants']
        return render_template('compare.html', city=city, county=county, pollutant=pollutant, congestions=conglist, pollutions=polllist)
    return render_template('compare.html', congestions=conglist, pollutions=polllist)

'''
app.route("/map")
def map_landing():
    # simple landing page that links to each pollutant map
    pollutants = ["O3", "CO", "SO2", "NO2"]
    return render_template("line.html", pollutants=pollutants)


@app.route("/map/<pollutant>")
def map_view(pollutant):
    if pollutant not in {"O3", "CO", "SO2", "NO2"} and pollutant != "congestion":
        abort(404)
    return render_template("map.html", pollutant=pollutant)

@app.route('/map')
def map():
    return render_template('line.html')
'''

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
'''
# --------------------  data APIs  --------------------
@app.route("/data/<pollutant>")
=======
    return redirect('/login')

@app.route('/map/<pollutant>')
def map_view(pollutant):
    return render_template('map.html', pollutant=pollutant)

@app.route('/data/<pollutant>')
>>>>>>> 9a1236d20d633912e418bac834ce97968f05775f
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

<<<<<<< HEAD
# --------------------  like / comment APIs  --------------------
@app.route("/api/likes/<graph_slug>", methods=["GET", "POST"])
@login_required
def likes_api(graph_slug):
    conn = get_db_connection()
    if request.method == "GET":
        total = conn.execute(
            "SELECT COUNT(*) FROM likes WHERE graph_slug = ?", (graph_slug,)
        ).fetchone()[0]
        user_liked = (
            conn.execute(
                "SELECT 1 FROM likes WHERE graph_slug = ? AND user_id = ?",
                (graph_slug, session["user_id"]),
            ).fetchone()
            is not None
        )
        conn.close()
        return jsonify({"total": total, "userLiked": user_liked})

    # POST toggles like
    already = conn.execute(
        "SELECT id FROM likes WHERE graph_slug = ? AND user_id = ?",
        (graph_slug, session["user_id"]),
    ).fetchone()
    if already:
        conn.execute("DELETE FROM likes WHERE id = ?", (already["id"],))
    else:
        conn.execute(
            "INSERT INTO likes (graph_slug, user_id, created_at) VALUES (?,?,?)",
            (graph_slug, session["user_id"], datetime.datetime.utcnow()),
        )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/comments/<graph_slug>", methods=["GET", "POST", "DELETE"])
@login_required
def comments_api(graph_slug):
    conn = get_db_connection()
    if request.method == "GET":
        rows = conn.execute(
            """
            SELECT c.id, c.text, c.created_at, u.username
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.graph_slug = ?
            ORDER BY c.created_at DESC
            """,
            (graph_slug,),
        ).fetchall()
        conn.close()
        return jsonify(
            comments=[
                {
                    "id": r["id"],
                    "text": r["text"],
                    "author": r["username"],
                    "created_at": r["created_at"],
                    "mine": r["username"] == session.get("username"),
                }
                for r in rows
            ]
        )

    if request.method == "POST":
        text = request.json.get("text", "").strip()
        if not text:
            conn.close()
            return jsonify({"error": "Empty"}), 400
        conn.execute(
            "INSERT INTO comments (graph_slug, user_id, text, created_at) VALUES (?,?,?,?)",
            (graph_slug, session["user_id"], text, datetime.datetime.utcnow()),
        )
        conn.commit()
        conn.close()
        return jsonify({"ok": True})

    # DELETE – only owner may delete
    comment_id = request.json.get("id")
    conn.execute(
        "DELETE FROM comments WHERE id = ? AND user_id = ?",
        (comment_id, session["user_id"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})
'''
if __name__ == "__main__":
	app.run(host='0.0.0.0')