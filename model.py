import sqlite3

con = sqlite3.connect('parties.db', check_same_thread=False)
db = con.cursor()

def get_session_id(chat_id):
    session_id_query = db.execute('SELECT id FROM sessions WHERE chat_id = ?', (chat_id,)).fetchall()
    session_id = session_id_query[0][0]
    return session_id

def is_session_ongoing(chat_id):
    session_id_query = db.execute('SELECT id FROM sessions WHERE chat_id = ?', (chat_id,)).fetchall()
    return len(session_id_query) > 0

def start_session(chat_id):
    db.execute('INSERT INTO sessions (chat_id) VALUES (?)', (chat_id,))

def end_session(chat_id):
    session_id = get_session_id(chat_id)
    db.execute('DELETE FROM items WHERE session_id = ?', (session_id,))
    db.execute('DELETE FROM users WHERE session_id = ?', (session_id,))
    db.execute('DELETE FROM sessions WHERE chat_id = ?', (chat_id,))

def is_user_in_session(chat_id, username):
    session_id = get_session_id(chat_id)
    user_id_query = db.execute('SELECT id FROM users WHERE session_id = ? AND username = ?', (session_id, username)).fetchall()
    return len(user_id_query) > 0

def add_user_to_session(chat_id, username):
    session_id = get_session_id(chat_id)
    db.execute('INSERT INTO users (session_id, username) VALUES (?, ?)', (session_id, username))

def get_users_in_session(chat_id):
    session_id = get_session_id(chat_id)
    list_of_users = db.execute('SELECT username FROM users WHERE session_id = ?', (session_id,)).fetchall()
    return list_of_users

def delete_user_from_session(chat_id, username):
    session_id = get_session_id(chat_id)
    db.execute('DELETE FROM users WHERE session_id = ? AND username = ?', (session_id, username))

def add_item_to_session(chat_id, username, item_name, item_price):
    session_id = get_session_id(chat_id)
    db.execute('INSERT INTO items (session_id, username, item_name, item_price) VALUES (?, ?, ?, ?)', (session_id, username, item_name, item_price))

def get_items_in_session(chat_id):
    session_id = get_session_id(chat_id)
    list_of_items = db.execute('SELECT id, username, item_name, item_price FROM items WHERE session_id = ?', (session_id,)).fetchall()
    return list_of_items

def delete_item_from_session(chat_id, item_id):
    session_id = get_session_id(chat_id)
    db.execute('DELETE FROM items WHERE session_id = ? AND id = ?', (session_id, item_id))