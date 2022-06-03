import sqlite3

database = sqlite3.connect('../db.sqlite3')
cursor = database


def get_word(chat_id: int, word: str):
    database = sqlite3.connect('../db.sqlite3')
    cursor = database.cursor()
    word = cursor.execute('''SELECT * FROM translator_app_profile WHERE chat_id = ? AND word = ?''',
                          (chat_id, word)).fetchone()
    database.close()
    return word


def save_word(chat_id: int, full_name: str, word: str):
    database = sqlite3.connect('../db.sqlite3')
    cursor = database.cursor()
    cursor.execute('''INSERT INTO translator_app_profile(chat_id, full_name, word)
    VALUES(?,?,?)
    ''', (chat_id, full_name, word))
    database.commit()
    database.close()


def create_profiles_table():
    # cursor.execute('''DROP TABLE IF EXISTS profiles''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS profiles(
        profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        full_name VARCHAR(200),
        word VARCHAR(255),
        UNIQUE(chat_id, word)
    )''')


def get_users_words(chat_id: int):
    database = sqlite3.connect('../db.sqlite3')
    cursor = database.cursor()
    words = cursor.execute('''SELECT word FROM translator_app_profile WHERE chat_id = ?''', (chat_id,)).fetchall()
    database.close()
    return [word[0] for word in words]


def clear_all_words(chat_id: int):
    database = sqlite3.connect('../db.sqlite3')
    cursor = database.cursor()
    cursor.execute('''DELETE FROM translator_app_profile WHERE chat_id = ?''', (chat_id,))
    database.commit()
    database.close()


create_profiles_table()

database.commit()
database.close()
