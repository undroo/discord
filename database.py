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
 
def create_table(conn):
    sql_create_words_table = """CREATE TABLE IF NOT EXISTS words (
                                    word text PRIMARY KEY NOT NULL,
                                    unique (word)
                                );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_words_table)
    except Error as e:
        print(e)

def insert_into_table(conn, word):
    sql_insert_words = '''INSERT INTO words
                        VALUES (?)'''
    try:
        c = conn.cursor()
        c.execute(sql_insert_words,(word,))
    except Error as e:
        print(e)

def delete_from_table(conn,word):
    sql_insert_words = '''DELETE FROM words
                        WHERE word = ?'''
    try:
        c = conn.cursor()
        c.execute(sql_insert_words,(word,))
    except Error as e:
        print(e)

def select_from_table(conn):
    sql_select_words = '''SELECT * FROM words'''
    try:
        c = conn.cursor()
        result = c.execute(sql_select_words).fetchall()
        return result
    except Error as e:
        print(e)

if __name__ == '__main__':
    sql_create_words_table = """CREATE TABLE IF NOT EXISTS words (
                                    word text PRIMARY KEY NOT NULL,
                                    unique (word)
                                );"""

    sql_insert_words = '''INSERT INTO words
                        VALUES (?)'''

    sql_select_words = '''SELECT * FROM words'''
    conn = create_connection("decrypto.db")
    if conn is not None:
        create_table(conn)
        # insert_into_table(conn,"potato")
        # insert_into_table(conn,"allan is gay")
        # result = select_from_table(conn)
        # for row in result:
        #     print(row[0])
        conn.commit()
        conn.close()
    else: 
        print("missing db")