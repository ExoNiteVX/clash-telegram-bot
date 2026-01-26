import sqlite3


DB_NAME = "telegram.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    with connect() as con:
        con.execute('''
        CREATE TABLE IF NOT EXISTS users (
        tg_id INTEGER PRIMARY KEY,
        username TEXT,
        number TEXT
                        )''')


def add_users(tg_id, username, number):
    with connect() as con:
        con.execute('''
        INSERT OR REPLACE INTO users (tg_id, username, number) VALUES (?, ?, ?)
        ''', (tg_id, username, number))

def get_user(tg_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute('''Select * FROM users WHERE tg_id = ?''', (tg_id,))
        return cur.fetchone()