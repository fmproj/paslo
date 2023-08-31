import os
import sqlite3

def open_db(path):
    conn = sqlite3.connect(path)
    return conn

def create_passrecs_table(conn):
    create_passrecs_query = '''
        CREATE TABLE IF NOT EXISTS password_records (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL,
            username TEXT,
            password TEXT NOT NULL,
            updated DATETIME,
            notes TEXT
        )
    '''

    cursor = conn.cursor()
    cursor.execute(create_passrecs_query)
    conn.commit()

if __name__ == "__main__":
    self_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = os.path.join(self_dir, "paslo.db")

    conn = open_db(db_name)
    create_passrecs_table(conn)
    conn.close()
