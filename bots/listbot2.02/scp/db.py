import sqlite3
import logging
import datetime
from logging.handlers import RotatingFileHandler

date=f"{datetime.datetime.now():%Y-%m-%d}"
conn = sqlite3.connect("./db/listbot_2022-12-25.db", check_same_thread=False)
log2 = logging.getLogger(__name__)
log2.setLevel(logging.DEBUG)
handler2 = RotatingFileHandler('./log/db.log', maxBytes=1000000, backupCount=10)
log_format2 = f"%(asctime)s | [%(levelname)s] | %(name)s | (%(filename)s).%(funcName)s(%(lineno)d) | %(message)s"
handler2.setFormatter(logging.Formatter(log_format2))
log2.addHandler(handler2)

with conn:
    log2.debug("Initializing cursor")
    cursor = conn.cursor()   

    cursor.executescript("""CREATE TABLE IF NOT EXISTS users 
        (
            chat_id    INTEGER  PRIMARY KEY,
            username   VARCHAR,
            first_name  VARCHAR,
            last_name   VARCHAR,
            phone       VARCHAR,
            banned      INTEGER,
            last_number INTEGER,
            timeout     DATETIME
        );
         """)
    cursor.executescript("""CREATE TABLE IF NOT EXISTS question 
        (
            id    INTEGER  PRIMARY KEY,
            question   VARCHAR,
            answer_var VARCHAR,
            answer     VARCHAR
        );
         """)
    cursor.executescript("""CREATE TABLE IF NOT EXISTS lists 
        (
            list_name  VARCHAR,
            deadline   VARCHAR,
            active     INTEGER
        );
         """)
    conn.commit()

    cursor = conn.cursor()

    cursor.executescript("""INSERT OR IGNORE INTO question (id, question, answer_var, answer) VALUES (1, 'question1', 'answer_var1', 'answer');
                            INSERT OR IGNORE INTO question (id, question, answer_var, answer) VALUES (2, 'question2', 'answer_var2', 'answer');
                            INSERT OR IGNORE INTO question (id, question, answer_var, answer) VALUES (3, 'question3', 'answer_var3', 'answer');
                            """)
    conn.commit()

def if_user_exists(chat_id):
    try:
        cursor.execute("SELECT * FROM users WHERE chat_id = ?", [chat_id])
        user_g = cursor.fetchall()
        log2.debug(user_g[0][1] + " was checked on existing")
        return True
    except IndexError:
        return False

def if_user_ban(username):
    cursor.execute("SELECT banned FROM users WHERE username LIKE ?", [username])
    user_g = cursor.fetchall()
    return user_g[0][0]

def if_user_ban_2(chat_id):
    cursor.execute("SELECT banned FROM users WHERE chat_id = ?", [chat_id])
    user_g = cursor.fetchall()
    return user_g[0][0]

def banlist():
    cursor.execute("SELECT chat_id, username FROM users WHERE banned = 1",)
    result = cursor.fetchall()
    return result

def new_user(chat_id, username, first_name, last_name):
    cursor.execute("""INSERT INTO users (chat_id, username, first_name, last_name, phone, banned, timeout) VALUES (?, ?, ?, ?, ?, ?, ?)
""", (chat_id, username, first_name, last_name, 0, 0, 0))
    conn.commit()

def update_phone(chat_id, phone):
    cursor.executemany("""UPDATE users 
    SET phone = ? WHERE chat_id = ?""", ((phone, chat_id), ))
    conn.commit()

def update_ban(username):
    cursor.executemany("""UPDATE users 
    SET banned = 1 WHERE username LIKE ?""", ((username, ), ))
    conn.commit()

def update_unban(username):
    cursor.executemany("""UPDATE users 
    SET banned = 0 WHERE username = ?""", ((username, ), ))
    conn.commit()

def update_timeout_on(date, chat_id):
    cursor.executemany("""UPDATE users 
    SET timeout = ? WHERE chat_id = ?""", ((date, chat_id), ))
    conn.commit()

def get_timeout(chat_id):
    cursor.execute("SELECT timeout FROM users WHERE chat_id = ?", [chat_id])
    time_g = cursor.fetchall()
    return time_g[0][0]

def insert_list(list_name):
    cursor.execute("""INSERT INTO lists (list_name, deadline, active) VALUES (?, ?, ?)
""", (list_name, 150, 1))
    conn.commit()

def if_list_exists(list_name):
    try:
        cursor.execute("SELECT * FROM lists WHERE list_name like ?", (list_name,))
        list_g = cursor.fetchall()
        log2.debug(list_g[0][1] + " was checked on existing")
        return True
    except IndexError:
        return False

def get_lists():
    try:
        cursor.execute("SELECT list_name as list, deadline as deadline, active as active FROM lists ")
        __headers = [i[0] for i in cursor.description]
        __get_lists = cursor.fetchall()
        log2.debug(__get_lists[0][1] + " was checked on existing")
        return __get_lists, __headers
    except IndexError:
        return False

def close_list(list_name):
    cursor.execute("""UPDATE lists SET active = 0 WHERE list_name like ?""", (list_name,))
    conn.commit()

def open_list(list_name):
    cursor.execute("""UPDATE lists SET active = 1 WHERE list_name like ?""", (list_name,))
    conn.commit()

def delete_list(list_name):
    cursor.execute("""DELETE FROM lists WHERE list_name like ? """, (list_name,))
    conn.commit()

def update_deadline(list_name,deadline):
    cursor.execute("""UPDATE lists SET deadline = ? WHERE list_name like ?""", ((deadline,list_name,)))
    conn.commit()

def get_question():
    d = []
    cursor.execute("SELECT question FROM question")
    __question = cursor.fetchone()
    while __question is not None:
        d.append(__question[0])
        __question = cursor.fetchone()
    return d

def get_question_id(question):
    cursor.execute("SELECT id FROM question WHERE question = ?", [question])
    __question = cursor.fetchall()
    return __question[0][0]

def get_question_text(id):
    cursor.execute("SELECT question FROM question WHERE id = ?", [id])
    __question = cursor.fetchall()
    return __question[0][0]

def get_answer_text(id):
    cursor.execute("SELECT answer_var FROM question WHERE id = ?", [id])
    __question = cursor.fetchall()
    return __question[0][0]

def get_deadline(list_name):
    cursor.execute("SELECT deadline FROM lists WHERE list_name like ?", (list_name,))
    __deadline = cursor.fetchall()
    return __deadline[0][0]

def get_answer_list():
    d = []
    cursor.execute("SELECT answer FROM question")
    __question = cursor.fetchone()
    while __question is not None:
        d.append(__question[0])
        __question = cursor.fetchone()
    return d

def update_question(question,answer_var,answer,id):
    cursor.execute("""UPDATE question set question = ?, answer_var = ?, answer = ? WHERE id = ?""", (question, answer_var, answer,id))
    conn.commit()

def update_last_number(chat_id,number):
    cursor.executemany("""UPDATE users SET last_number = ? WHERE chat_id = ?""", ((number,chat_id ), ))
    conn.commit()