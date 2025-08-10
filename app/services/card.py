import time
from app.services.deck import get_deck_id_from_name
from app.services.db import db


def create_card(deck, question, answer):

    deck_id, message = get_deck_id_from_name(deck)
    if message != "":
        return message

    last_answered = int(time.time())
    correct = False
    sql_stmt = """
INSERT INTO card (deck_id, question, answer, last_time_answered_epoch, correct)
VALUES (?, ?, ?, ?, ?)
"""

    try:
        db.execute(sql_stmt, (deck_id, question, answer, last_answered, correct))
        return ""
    except:
        return "Error: Could not create card"

def delete_card(deck, card_id):

    deck_id, message = get_deck_id_from_name(deck)
    if message != "":
        return message

    delete_card_stmt = """
DELETE FROM card
WHERE id = ? AND deck_id = ?
"""

    try:
        db.execute(delete_card_stmt, (card_id, deck_id))
        return ""
    except:
        return "Error: Could not delete card"


def update_card(deck, card_id, question, answer):

    deck_id, message = get_deck_id_from_name(deck)
    if message != "":
        return message

    update_card_stmt = """
UPDATE card
SET question = ?, answer = ?
WHERE id = ? AND deck_id = ?
"""

    try:
        db.execute(update_card_stmt, (question, answer, card_id, deck_id))
        return ""
    except:
        return "Error: Could not update card"

def delete_all_cards(deck):
    deck_id, message = get_deck_id_from_name(deck)
    if message != "":
        return message

    delete_all_cards_stmt = """
DELETE FROM card
WHERE deck_id = ?
"""

    try:
        db.execute(delete_all_cards_stmt, (deck_id,))
        return ""
    except:
        return "Error: Could not delete all cards"

def get_card(deck, card_id):
    deck_id, message = get_deck_id_from_name(deck)

    if message != "":
        return {}, message

    get_card_stmt = """
SELECT id, question, answer, last_time_answered_epoch, correct
FROM card
WHERE id = ? AND deck_id = ?
"""

    try:
        row = db.fetch_one(get_card_stmt, (card_id, deck_id))
        if not row:
            return {}, "Error: Card not found"

        card = {
            "id": row[0],
            "question": row[1],
            "answer": row[2],
            "last_time_answered_epoch": row[3],
            "correct": row[4]
        }
        return card, ""

    except:
        return {}, "Error: Could not get card"