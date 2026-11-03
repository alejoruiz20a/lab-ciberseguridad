import os
import sqlite3

import requests
from flask import Flask, jsonify, render_template_string, request, send_file
from werkzeug.security import safe_join

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")
FILES_DIR = os.path.join(BASE_DIR, "files")
STATUS_URL = os.environ.get("STATUS_URL", "http://127.0.0.1:5000/")

app = Flask(__name__)
app.secret_key = "n0t4s-pr0d-9f3a7c21e8b64d05a1c3f7e2"


def get_db():
    return sqlite3.connect(DB_PATH)


@app.route("/")
def index():
    return (
        "<h1>Notas (laboratorio)</h1>"
        "<ul><li>POST /login</li><li>GET /search?q=</li>"
        "<li>GET /greet?name=</li><li>GET /download?file=</li>"
        "<li>GET /status</li></ul>"
    )


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT username FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify({"mensaje": "Bienvenido, " + row[0]})
    return jsonify({"mensaje": "Credenciales invalidas"}), 401


@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM notes WHERE title LIKE ?", ("%" + q + "%",))
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "title": r[1]} for r in rows])


@app.route("/greet")
def greet():
    name = request.args.get("name", "mundo")
    return render_template_string("<h1>Hola, " + name + "</h1>")


@app.route("/download")
def download():
    filename = request.args.get("file", "")
    path = safe_join(FILES_DIR, filename)
    if path is None or not os.path.isfile(path):
        return jsonify({"error": "archivo no encontrado"}), 404
    return send_file(path)


@app.route("/status")
def status():
    resp = requests.get(STATUS_URL, timeout=3)
    return jsonify({"url": STATUS_URL, "codigo": resp.status_code})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
