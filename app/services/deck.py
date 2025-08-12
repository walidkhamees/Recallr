from app.services.db import db


def get_decks():
    sql_stmt = """
SELECT name FROM deck
"""
    rows = db.fetch_all(sql_stmt)
    decks = [row[0] for row in rows]
    return decks

def delete_all_decks():
    sql_stmt = """
DELETE FROM deck
"""
    try:
        db.execute(sql_stmt)
        return ""
    except:
        return "Error: Could not delete all decks"

def create_deck(deck):
    sql_stmt = """
INSERT INTO deck (name)
VALUES (?)
"""

    deck = deck.strip()
    if deck == "":
        return "Error: Deck name cannot be empty"

    try:
        db.execute(sql_stmt, (deck,))
        return ""
    except:
        return "Error: Could not create deck"


def get_deck_id_from_name(deck):
    sql_stmt = """
SELECT id FROM deck WHERE name = ?
"""
    try:
        row = db.fetch_one(sql_stmt, (deck,))
        return row[0], ""
    except:
        return -1, "Error: Deck not found"

def get_deck(deck):
    deck_id, message = get_deck_id_from_name(deck)

    if message != "":
        return "", message

    if deck_id == "":
        return "", "Error: Deck not found"

    sql_stmt = """
SELECT card.id, card.question, card.answer, card.last_time_answered_epoch, card.correct
FROM card
INNER JOIN deck ON card.deck_id = deck.id
WHERE deck.id = ?
"""
    rows = db.fetch_all(sql_stmt, (deck_id,))

    deck = {
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
