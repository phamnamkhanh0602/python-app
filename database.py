import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_user(email,name,password):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('Insert into user(email,name,password) Values(?,?,?)',(email,name,password))
    conn.commit()
    conn.close()

def find_user_by_email(email):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('Select id, email, name, password, address, dob, gender From user Where email = ?',(email,))
    user = cursor.fetchone()
    conn.close()
    return user

def find_user_by_email_and_password(email,password):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('Select id, email,name,password,address,dob,gender From user Where email = ? And password =?',(email,password))
    user = cursor.fetchone()
    conn.close()
    return user

def find_user_by_id(user_id):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('SELECT id, email, name, password, address, dob, gender, avatar FROM user WHERE id = ?',(user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_avatar(user_id, avatar):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('UPDATE user SET avatar = ? WHERE id = ?',(avatar,user_id))
    conn.commit()
    conn.close()

def update_user(user_id, name, address, dob, gender):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE user SET name = ?, address = ?, dob = ?, gender = ? WHERE id = ?',(name,address,dob,gender,user_id))
    conn.commit()
    conn.close()

def create_note(user_id, note, timestamp):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO note(user_id, note, timestamp) VALUES(?,?,?)',(user_id,note,timestamp))
    conn.commit()
    conn.close()

def get_all_notes(user_id):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('SELECT id, note, timestamp FROM note WHERE user_id = ?',(user_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes

def get_note_by_id(note_id):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('SELECT id, note, timestamp FROM note WHERE id = ?',(note_id,))
    note = cursor.fetchone()
    conn.close()
    return note


def update_note(note_id, note, timestamp):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE note SET note = ?, timestamp = ? WHERE id = ?',(note,timestamp,note_id))
    conn.commit()
    conn.close()

def delete_note(note_id):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM note WHERE id = ?',(note_id,))
    conn.commit()
    conn.close()
    
def create_note_table():
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS note(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, note TEXT, timestamp TEXT)')
    conn.commit()
    conn.close()