from app.services.db_interface import DB_interface
from app.utils import constants

from app.utils.functions import hash

db = DB_interface(constants.DB_PATH)

def init_db():
    user_table = """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    """

    deck_table = """
    CREATE TABLE IF NOT EXISTS deck (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
        UNIQUE(user_id, name)
    );
    """

    card_table = """
    CREATE TABLE IF NOT EXISTS card (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deck_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        last_time_answered_epoch INTEGER NOT NULL,
        correct BOOLEAN NOT NULL,
        FOREIGN KEY(deck_id) REFERENCES deck(id) ON DELETE CASCADE
    );

    """
    quiz_table = """
    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deck_id INTEGER NOT NULL,
        start_epoch INTEGER NOT NULL,
        end_epoch INTEGER NOT NULL,
        FOREIGN KEY(deck_id) REFERENCES deck(id) ON DELETE CASCADE
    );
    """

    quiz_card_table = """
    CREATE TABLE IF NOT EXISTS quiz_card (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        answer TEXT,
        answered BOOLEAN NOT NULL,
        FOREIGN KEY(quiz_id) REFERENCES quiz(id) ON DELETE CASCADE
    );
    """

    enable_foreign_keys = "PRAGMA foreign_keys = ON;"

    try:
        db.execute_without_commit(user_table)
        db.execute_without_commit(enable_foreign_keys)
        db.execute_without_commit(deck_table)
        db.execute_without_commit(card_table)
        db.execute_without_commit(quiz_table)
        db.execute_without_commit(quiz_card_table)

        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Error initializing database: {e}")

def init_db_data():

    if db.fetch_one("SELECT COUNT(*) FROM deck")[0] != 0:
        return

    password_hash = hash("waleed")

    user_inserts = """
        INSERT INTO user (username, password) VALUES
            ('waleed', ?)
    """
    cur = db.execute(user_inserts, (password_hash,))
    user_id = cur.lastrowid

    deck_table = "INSERT INTO deck (name, user_id) VALUES (?, ?)"
    cur = db.execute(deck_table, ("Default", user_id))
    deck_id = cur.lastrowid


    card_inserts = [
        (deck_id, 'What is the capital of France?', 'Paris', 1641010191, 0),
        (deck_id, 'Who is the current president of the United States?', 'Joe Biden', 1641010191, 0),
        (deck_id, 'What is the largest planet in our solar system?', 'Jupiter', 1641010191, 0),
        (deck_id, 'What is the smallest planet in our solar system?', 'Mercury', 1641010191, 0),
        (deck_id, 'What is the chemical symbol for gold?', 'Au', 1641010191, 0),
    ]

    for values in card_inserts:
        db.execute(
            "INSERT INTO card (deck_id, question, answer, last_time_answered_epoch, correct) VALUES (?, ?, ?, ?, ?)",
            values
        )
