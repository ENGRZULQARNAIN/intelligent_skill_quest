
# author: Zulqar Nain
# date: 12-june-2024
# project SkillQues

############################################################################

import sqlite3
import hashlib

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    username text NOT NULL,
                                    password text NOT NULL
                                );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_users_table)
    except sqlite3.Error as e:
        print(e)


def create_user(conn, username, password):
    sql = '''INSERT INTO users(username, password) VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (username, password))
    conn.commit()
    return cur.lastrowid

# def activate_user(conn, username):
#     """
#     Update the is_active status of a user to 0 based on the username.
#     :param conn: Connection object
#     :param username: username of the user
#     :return:
#     """
#     sql = '''UPDATE users SET is_active = 1 WHERE username = ?'''
#     try:
#         cur = conn.cursor()
#         cur.execute(sql, (username,))
#         conn.commit()
#         print(f"User with username {username} deactivated.")
#     except sqlite3.Error as e:
#         print(e)

# def is_user_active(conn, username):
#     """
#     Check if a user is active based on the username.
#     :param conn: Connection object
#     :param username: username of the user
#     :return: True if user is active, else False
#     """
#     sql = '''SELECT is_active FROM users WHERE username = ?'''
#     try:
#         cur = conn.cursor()
#         cur.execute(sql, (username,))
#         result = cur.fetchone()
#         if result and result[0] == 1:
#             return True
#         else:
#             return False
#     except sqlite3.Error as e:
#         print(e)
#         return False


def authenticate_user(conn, username, password):
    sql = '''SELECT * FROM users WHERE username=? AND password=?'''
    cur = conn.cursor()
    cur.execute(sql, (username, password))
    rows = cur.fetchall()
    return len(rows) > 0
