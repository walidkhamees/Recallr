from app.services.db_interface import DB_interface
from app.utils import constants

db = DB_interface(constants.DB_PATH)

def init_db(db_interface: DB_interface):
    deck_table = """
    CREATE TABLE IF NOT EXISTS deck (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
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
        quiz_start_epoch INTEGER NOT NULL,
        quiz_end_epoch INTEGER NOT NULL,
        FOREIGN KEY(deck_id) REFERENCES deck(id) ON DELETE CASCADE
    );
    """

    quiz_card_table = """
    CREATE TABLE IF NOT EXISTS quiz_card (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        card_id INTEGER NOT NULL,
        answered BOOLEAN NOT NULL,
        FOREIGN KEY(quiz_id) REFERENCES quiz(id) ON DELETE CASCADE,
        FOREIGN KEY(card_id) REFERENCES card(id) ON DELETE CASCADE
    );
    """

    enable_foreign_keys = "PRAGMA foreign_keys = ON;"

    try:
        db_interface.execute_without_commit(deck_table)
        db_interface.execute_without_commit(card_table)
        db_interface.execute_without_commit(quiz_table)
        db_interface.execute_without_commit(quiz_card_table)
        db_interface.execute_without_commit(enable_foreign_keys)

        db_interface.commit()
    except Exception as e:
        db_interface.rollback()
        raise Exception(f"Error initializing database: {e}")