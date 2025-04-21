from flask import Flask, render_template, url_for, request, redirect, session, jsonify, abort
import sqlite3
import hashlib
import functools, datetime

app = Flask(__name__)
app.secret_key = 'SquidwardT'
DB = "data.db"

# ─────────────────────────────  helpers ──────────────────────────────
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped

# ─────────────────────────────  routes  ──────────────────────────────
@app.route('/')
def root():
    return render_template('home.html')

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

@app.route('/test')
def test():
    return render_template('test.html')

# --------------------  auth  -------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        pw_hash = hashlib.sha256(request.form["password"].encode()).hexdigest()
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?,?)",
                (username, pw_hash),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Username taken")
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        pw_hash = hashlib.sha256(request.form["password"].encode()).hexdigest()
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, pw_hash),
        ).fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            return redirect(request.args.get("next", "/"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# --------------------  data APIs  --------------------
@app.route("/data/<pollutant>")
def data_api(pollutant):
    conn = get_db_connection()
    if pollutant == "congestion":
        rows = conn.execute(
            "SELECT year, state, congestion_index AS value FROM congestion ORDER BY year"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT year, state, value FROM airQuality WHERE pollutant = ? ORDER BY year",
            (pollutant,),
        ).fetchall()
    conn.close()
    return jsonify(data=[dict(r) for r in rows])

@app.route('/congestion_data')
def congestion_api():
    conn = get_db_connection()
    data = conn.execute("SELECT year, state, congestion_index FROM congestion ORDER BY year").fetchall()
    conn.close()
    return {'data': [dict(row) for row in data]}

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

if __name__ == "__main__":
	app.run(host='0.0.0.0')
