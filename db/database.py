import datetime
import os
import sqlite3
import bcrypt

def open_db(path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    return conn

CONN = open_db(os.path.join(os.path.dirname(os.path.abspath(__file__)), "paslo.db"))

def create_passrecs_table() -> None:
    create_passrecs_query = '''
        CREATE TABLE IF NOT EXISTS password_records (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL UNIQUE,
            username TEXT,
            password TEXT NOT NULL,
            updated DATETIME NOT NULL,
            notes TEXT
        )
    '''

    cursor = CONN.cursor()
    cursor.execute(create_passrecs_query)
    CONN.commit()

create_passrecs_table()

def add_passrec(url, username, password, notes) -> int:
    try:
        cursor = CONN.cursor()
        date = datetime.datetime.now()
        insert_query = '''
            INSERT INTO password_records (url, username, password, updated, notes)
            VALUES (?, ?, ?, ?, ?)
        '''

        cursor.execute(insert_query, (url, username, hash_password(password), date, notes))
        CONN.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        # TODO: Log the error
        return None 

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pass

def get_passrec(url) -> list[any]:
    try:
        cursor = CONN.cursor()
        get_query = '''SELECT * FROM password_records WHERE url = ?'''

        cursor.execute(get_query, (url,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        # TODO: Log the error
        return []

def list_passrecs():
    cursor = CONN.cursor()
    list_all_query = '''
        SELECT * FROM password_records
    '''
    cursor.execute(list_all_query)
    return cursor.fetchall()

def update_passrec(url, username=None, password=None, notes=None) -> None:
    try:
        cursor = CONN.cursor()
        date = datetime.datetime.now()
        update_query = '''
            UPDATE password_records
            SET username = COALESCE(?, username), password = COALESCE(?, password), updated = ?, notes = COALESCE(?, notes)
            WHERE url = ?
        '''
        
        cursor.execute(update_query, (username, password, date, notes, url))
        CONN.commit()
    except sqlite3.Error as e:
        # TODO: Log the error
        pass

def delete_password(url) -> None:
    try:
        cursor = CONN.cursor()
        delete_query = '''DELETE FROM password_records WHERE url = ?'''

        cursor.execute(delete_query, (url,))
        CONN.commit()
    except sqlite3.Error as e:
        # TODO: Log the error
        pass

if __name__ == "__main__": 
    # print(add_passrec("LOL", "user", "heslo", "Login for LOL game"))
    # print(get_passrec("LOL"))
    # update_passrec("LOL", username="admin", notes="This is changed LOL note")
    # print(get_passrec("LOL"))
    # delete_password("LOL")
    # print(add_passrec("WOW", "druid", "Heslo123", "Credentials for WOW account"))
    # print(list_passrecs())

    CONN.close()
