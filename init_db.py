import os
import sqlite3

DEFAULT_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.db")


def init(path=DEFAULT_DB):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS notes")
    cur.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    cur.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY, title TEXT, body TEXT)")
    cur.executemany(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        [("admin", "lab-admin-123"), ("ana", "lab-ana-456")],
    )
    cur.executemany(
        "INSERT INTO notes (title, body) VALUES (?, ?)",
        [
            ("Lista de compras", "Pan, leche, huevos"),
            ("Reunion del lunes", "Revisar avances del taller"),
            ("Ideas de proyecto", "App de notas con Flask"),
        ],
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init()
    print("Base de datos creada:", DEFAULT_DB)
