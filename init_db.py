import sqlite3

con = sqlite3.connect('parties.db', check_same_thread=False)
db = con.cursor()
cmd = """
CREATE TABLE sessions (
        id INTEGER PRIMARY KEY,
        chat_id
        );
"""
db.execute(cmd)
cmd = """
CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        session_id,
        username
        );
"""
db.execute(cmd)
cmd = """
CREATE TABLE items (
        id INTEGER PRIMARY KEY,
        session_id,
        username,
        item_name,
        item_price INTEGER
        );
"""
db.execute(cmd)

con.close()