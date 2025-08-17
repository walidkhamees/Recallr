from flask_login import current_user
from app.services.db import db
from app.services.deck import get_deck_by_id
from app.utils.functions import check_logged_in, get_current_epoch


def create_card(deck_id, question, answer):
    if not check_logged_in(current_user):
        return "Error: User not logged in"

    _, message = get_deck_by_id(deck_id)
    if message != "":
        return message

    last_answered = get_current_epoch()
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

def delete_card(deck_id, card_id):
    if not check_logged_in(current_user):
        return "Error: User not logged in"
    delete_card_stmt = """
        DELETE FROM card
        WHERE id = ? AND deck_id = ? and deck_id IN (
            SELECT id
            FROM deck
            WHERE id = ? AND user_id = ?
        )
    """

    try:
        db.execute(delete_card_stmt, (card_id, deck_id, deck_id, current_user.id))
        return ""
    except:
        return "Error: Could not delete card"


def update_card(deck_id, card_id, question, answer):
    if not check_logged_in(current_user):
        return "Error: User not logged in"

    update_card_stmt = """
        UPDATE card
        SET question = ?, answer = ?
        WHERE id = ? AND deck_id = ? AND deck_id IN (
            SELECT id
            FROM deck
            WHERE id = ? AND user_id = ?
        )
    """

    try:
        db.execute(update_card_stmt, (question, answer, card_id, deck_id, deck_id, current_user.id))
        return ""
    except:
        return "Error: Could not update card"

def delete_all_cards(deck_id):
    if not check_logged_in(current_user):
        return "Error: User not logged in"

    delete_all_cards_stmt = """
        DELETE FROM card
        WHERE deck_id IN (
            SELECT id
            FROM deck
            WHERE id = ? AND user_id = ?
        ) AND deck_id = ?
    """

    try:
        db.execute(delete_all_cards_stmt, (deck_id, current_user.id, deck_id))
        return ""
    except:
        return "Error: Could not delete all cards"

def get_card(deck_id, card_id):
    if not check_logged_in(current_user):
        return {}, "Error: User not logged in"

    get_card_stmt = """
        SELECT card.id, question, answer, last_time_answered_epoch, correct
        FROM card
        INNER JOIN deck ON deck.id = card.deck_id
        WHERE card.id = ? AND deck_id = ? AND deck.user_id = ?
    """

    try:
        row = db.fetch_one(get_card_stmt, (card_id, deck_id, current_user.id))
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
