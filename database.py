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
    cursor.execute('Select id, email, name, password From user Where email = ?',(email,))
    user = cursor.fetchone()
    conn.close()
    return user

def find_user_by_email_and_password(email,password):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('Select id, email,name,password From user Where email = ? And password =?',(email,password))
    user = cursor.fetchone()
    conn.close()
    return user