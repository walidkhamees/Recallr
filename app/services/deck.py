import re

from flask_login import current_user

from app.services.db import db
from app.utils.functions import check_logged_in


def get_deck_by_id(deck_id):
    sql_stmt = """
        SELECT name FROM deck WHERE id = ? AND user_id = ?
    """

    try:
        row = db.fetch_one(sql_stmt, (deck_id, current_user.id))
        return row[0], ""
    except:
        return "", "Error: Deck not found"

def get_decks():
    if not check_logged_in(current_user):
        return {}, "Error: User not logged in"

    sql_stmt = """
        SELECT id, name FROM deck WHERE user_id = ?
    """
    try:
        rows = db.fetch_all(sql_stmt, (current_user.id,))
    except:
        return {}, "Error: Could not fetch decks"
    decks = {}
    for row in rows:
        decks[row[0]] = row[1]
    return decks, ""

def delete_all_decks():
    if not check_logged_in(current_user):
        return "Error: User not logged in"

    sql_stmt = """
        DELETE FROM deck WHERE user_id = ?
    """
    try:
        db.execute(sql_stmt, (current_user.id,))
        return ""
    except:
        return "Error: Could not delete all decks"

def create_deck(deck):
    if not check_logged_in(current_user):
        return "Error: User not logged in"


    special_characters_pattern = r"[^a-zA-Z0-9]+"

    if re.search(special_characters_pattern, deck):
        return "Error: Deck name cannot contain special characters"

    sql_stmt = """
        INSERT INTO deck (name, user_id)
        VALUES (?, ?)
    """

    existing_deck_stmt = """
        SELECT id FROM deck WHERE name = ? AND user_id = ?
    """

    existing_deck_row = db.fetch_one(existing_deck_stmt, (deck, current_user.id))
    if existing_deck_row:
        return "Error: Deck already exists"

    deck = deck.strip()
    if deck == "":
        return "Error: Deck name cannot be empty"

    try:
        db.execute(sql_stmt, (deck, current_user.id))
        return ""
    except:
        return "Error: Could not create deck"


def update_deck(deck_id, new_deck_name):
    if not check_logged_in(current_user):
        return "Error: User not logged in"

    special_characters_pattern = r"[^a-zA-Z0-9]+"
    deck_id = int(deck_id)

    new_deck_name = new_deck_name.strip()
    if new_deck_name == "":
        return "Error: New deck name cannot be empty"

    if re.search(special_characters_pattern, new_deck_name):
        return "Error: New deck name cannot contain special characters"

    sql_stmt = """
        UPDATE deck SET name = ? WHERE id = ? AND user_id = ?
    """
    try:
        db.execute(sql_stmt, (new_deck_name, deck_id, current_user.id))
        return ""
    except:
        return "Error: Could not rename deck"

def delete_deck(deck_id):
    sql_stmt = """
    DELETE FROM deck WHERE id = ? AND user_id = ?
    """
    try:
        db.execute(sql_stmt, (deck_id, current_user.id))
        return ""
    except:
        return "Error: Could not delete deck"

def get_deck(deck_id):
    if deck_id == "":
        return {}, "Error: Deck not found"

    deck, message = get_deck_by_id(deck_id)
    if message != "":
        return {}, message

    sql_stmt = """
        SELECT card.id, card.question, card.answer, card.last_time_answered_epoch, card.correct
        FROM card
        INNER JOIN deck ON card.deck_id = deck.id
        WHERE deck.id = ? AND deck.user_id = ?
    """

    rows = db.fetch_all(sql_stmt, (deck_id, current_user.id))

    deck = {
        "id": deck_id,
        "name": deck,
        "cards": {}
    }

    for row in rows:
        card_id = row[0]
        question = row[1]
        answer = row[2]
        last_answered_epoch = row[3]
        correct = row[4]

        deck["cards"][card_id] = {
            "question": question,
            "answer": answer,
            "last_time_answered_epoch": last_answered_epoch,
            "correct": correct
        }

    return deck, ""
