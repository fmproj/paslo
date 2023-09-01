import datetime
import os
import sqlite3
import bcrypt

def open_db(path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    return conn

def create_passrecs_table(conn) -> None:
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

    cursor = conn.cursor()
    cursor.execute(create_passrecs_query)
    conn.commit()

def add_passrec(conn: sqlite3.Connection, url, username, password, notes) -> int:
    try:
        cursor = conn.cursor()
        date = datetime.datetime.now()
        insert_query = '''
            INSERT INTO password_records (url, username, password, updated, notes)
            VALUES (?, ?, ?, ?, ?)
        '''

        cursor.execute(insert_query, (url, username, hash_password(password), date, notes))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        # TODO: Log the error
        return None 

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pass

def get_passrec(conn: sqlite3.Connection, url) -> list[any]:
    try:
        cursor = conn.cursor()
        get_query = '''SELECT * FROM password_records WHERE url = ?'''

        cursor.execute(get_query, (url,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        # TODO: Log the error
        return []

def update_passrec(conn: sqlite3.Connection, url, username=None, password=None, notes=None) -> None:
    try:
        cursor = conn.cursor()
        date = datetime.datetime.now()
        update_query = '''
            UPDATE password_records
            SET username = COALESCE(?, username), password = COALESCE(?, password), updated = ?, notes = COALESCE(?, notes)
            WHERE url = ?
        '''
        
        cursor.execute(update_query, (username, password, date, notes, url))
        conn.commit()
    except sqlite3.Error as e:
        # TODO: Log the error
        pass

def delete_password(conn: sqlite3.Connection, url) -> None:
    try:
        cursor = conn.cursor()
        delete_query = '''DELETE FROM password_records WHERE url = ?'''

        cursor.execute(delete_query, (url,))
        conn.commit()
    except sqlite3.Error as e:
        # TODO: Log the error
        pass

if __name__ == "__main__":
    self_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = os.path.join(self_dir, "paslo.db")

    conn = open_db(db_name)
    create_passrecs_table(conn)

    print(add_passrec(conn, "LOL", "user", "heslo", "Login for LOL game"))
    print(get_passrec(conn, "LOL"))
    update_passrec(conn, "LOL", username="admin", notes="This is changed LOL note")
    print(get_passrec(conn, "LOL"))
    delete_password(conn, "LOL")
    print(get_passrec(conn, "LOL"))

    conn.close()
