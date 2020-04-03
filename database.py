import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
 
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

if __name__ == '__main__':
    sql_create_words_table = """CREATE TABLE IF NOT EXISTS words (
                                    word text,
                                    unique (word)
                                );"""

    conn = create_connection("decrypto.db")
    if conn is not None:
        create_table(conn,sql_create_words_table)
    else: 
        print("missing db")