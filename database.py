import sqlite3

def create_user(email,name,password):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('Insert into user(email,name,password) Values(?,?,?)',(email,name,password))
    conn.commit()
    conn.close()

def find_user_by_email(email):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('Select email, name, password From user Where email = ?',(email,))
    user = cursor.fetchone()
    conn.close()
    return user

def find_user_by_email_and_password(email,password):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('Select email,name,password From user Where email = ? And password =?',(email,password))
    user = cursor.fetchone()
    conn.close()
    return user

create_user('khanhphamnam13@gmail.com','nam khanh','5476')
print(find_user_by_email('khanhphamnam13@gmail.com'))
print(find_user_by_email_and_password('khanhphamnam13@gmail.com','5476'))