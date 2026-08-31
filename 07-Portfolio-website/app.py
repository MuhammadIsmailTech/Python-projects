from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "projects.db")

app = Flask(__name__)
app.secret_key = "change_this_to_a_secure_random_string"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        short_desc TEXT,
        long_desc TEXT,
        tech TEXT,
        repo_url TEXT,
        live_url TEXT,
        image TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    db.commit()

@app.before_request
def setup():
    init_db()
    # optional: seed sample project if table empty
    db = get_db()
    cur = db.execute("SELECT COUNT(*) as cnt FROM projects")
    if cur.fetchone()["cnt"] == 0:
        db.execute(
            "INSERT INTO projects (title, short_desc, long_desc, tech, repo_url, live_url, image) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("Sample Bank System", "Console bank management system using OOP",
             "A full console-based bank management demo that demonstrates OOP, file I/O and basic testing.",
             "Python, OOP, SQLite", "https://github.com/yourusername/Project1_BankSystem", "", "placeholder.png")
        )
        db.execute(
            "INSERT INTO projects (title, short_desc, long_desc, tech, repo_url, live_url, image) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("Data Analysis Dashboard", "Interactive dashboard using Dash and Plotly",
             "Dash app showing sales KPIs, filters and charts. Integrated with Pandas for data processing.",
             "Python, Dash, Plotly, Pandas", "https://github.com/yourusername/Project2_DataAnalysisDashboard", "", "placeholder.png")
        )
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    db = get_db()
    projects = db.execute("SELECT id, title, short_desc, image FROM projects ORDER BY id DESC LIMIT 3").fetchall()
    return render_template("index.html", projects=projects)

@app.route("/projects")
def projects():
    db = get_db()
    projects = db.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
    return render_template("projects.html", projects=projects)

@app.route("/project/<int:project_id>")
def project_detail(project_id):
    db = get_db()
    project = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if not project:
        flash("Project not found.", "warning")
        return redirect(url_for("projects"))
    return render_template("project_detail.html", project=project)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name").strip()
        email = request.form.get("email").strip()
        message = request.form.get("message").strip()
        if not name or not email or not message:
            flash("Please fill all fields.", "danger")
            return redirect(url_for("contact"))
        db = get_db()
        db.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
                   (name, email, message))
        db.commit()
        flash("Thanks! Your message was received.", "success")
        return redirect(url_for("index"))
    return render_template("contact.html")

if __name__ == "__main__":
    # Note: For production use a WSGI server. debug=False for production.
    app.run(debug=True, host="127.0.0.1", port=5000)
