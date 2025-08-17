from datetime import datetime

from flask_login import current_user

from app.services.db import db
from app.services.deck import get_deck_by_id
from app.utils.functions import check_logged_in, get_current_epoch

def get_all_quiz_results(deck_id):
    get_all_quiz_results_stmt = """
        SELECT quiz.id, quiz.start_epoch,
        (
            select count(*) from quiz_card
            where quiz_card.quiz_id = quiz.id and quiz_card.answered = 1
        )
        as correct,
        (
            select count(*) from quiz_card
            where quiz_card.quiz_id = quiz.id and quiz_card.answered = -1
        ) as wrong,
        (
            select count(*) from quiz_card
            where quiz_card.quiz_id = quiz.id
        ) as total
        FROM quiz
        WHERE quiz.deck_id = ? and (quiz.end_epoch < ? or total = correct + wrong)
        AND quiz.deck_id IN (
            SELECT id
            FROM deck
            WHERE id = ? AND user_id = ?
        )
        ORDER BY quiz.start_epoch DESC;
    """
    now = int(datetime.now().timestamp())
    try:
        rows = db.fetch_all(get_all_quiz_results_stmt, (deck_id, now, deck_id, current_user.id))
    except:
        return {}, "Error: Could not get quiz results"

    results = {}
    for row in rows:
        time = datetime.fromtimestamp(row[1]).strftime("%B %d, %Y")
        results[row[0]] = {
            "time": time,
            "correct": row[2],
            "wrong": row[4] - row[2],
        }

    return results, ""

def get_quiz_result(deck_id, quiz_id):
    """
        gets the result of a quiz args: quiz_id: the id of the quiz returns:
            quiz_result(dict):
            {
                "correct": number of correct answers,
                "wrong": number of wrong answers,
                "unanswered": number of unanswered cards,
                "quiz_id": id of the quiz,
                "cards": {
                    "card_id": {
                        "question": question of the card,
                        "answer": answer of the card,
                        "correct": whether the card was answered correctly or not,
                        "user_answer": answer given by the user
                    }
                    ...
                }
            }
            message: error message if there was an error
    """

    if not check_logged_in(current_user):
        return {}, "Error: User not logged in"

    _, message = get_deck_by_id(deck_id)
    if message != "":
        return {}, message

    quiz_done_stmt = """
        SELECT
        (
            SELECT COUNT(*) FROM quiz_card
            WHERE quiz_card.quiz_id = ? AND quiz_card.answered = 1
        ) AS correct,
        (
            SELECT count(*) FROM quiz_card
            WHERE quiz_card.quiz_id = ? AND quiz_card.answered = -1
        ) AS wrong,
        (
            SELECT count(*) FROM quiz_card
            WHERE quiz_card.quiz_id = ?
        ) AS total
        FROM quiz_card
        INNER JOIN quiz ON quiz.id = quiz_card.quiz_id -- for end_epoch
        WHERE quiz_card.quiz_id = ?
        AND (total = (wrong + correct) or quiz.end_epoch < ?)
        AND quiz.deck_id IN (
            SELECT id
            FROM deck
            WHERE id = ? AND user_id = ?
        )
        LIMIT 1
    """

    now = get_current_epoch()
    row = db.fetch_one(quiz_done_stmt, (quiz_id, quiz_id, quiz_id, quiz_id, now, deck_id, current_user.id))
    if row == None or len(row) == 0:
        return {}, "Error: Could not get quiz result"

    result_stmt = """
        SELECT card.id, quiz_card.answered, quiz_card.answer, card.question, card.answer as user_answer,
        (
            SELECT COUNT(*) FROM quiz_card
            WHERE quiz_card.quiz_id = ? AND quiz_card.answered = 1
        ) AS correct,
        (
            select count(*) from quiz_card
            where quiz_card.quiz_id = ? and quiz_card.answered = -1
        ) as wrong,
        (
            select count(*) from quiz_card
            where quiz_card.quiz_id = ?
        ) as total
        FROM quiz_card
        INNER JOIN card ON quiz_card.card_id = card.id
        WHERE quiz_card.quiz_id = ?;
    """


    try:
        quiz_cards = db.fetch_all(result_stmt, (quiz_id, quiz_id, quiz_id, quiz_id))
    except:
        return {}, "Error: Could not get quiz result"

    if len(quiz_cards) == 0 or quiz_cards == None:
        return {}, "Error: Could not get quiz result"

    correct = quiz_cards[0][5]
    wrong = quiz_cards[0][6]
    total = quiz_cards[0][7]

    quiz_result = {
        "correct": correct,
        "wrong": wrong,
        "unanswered": total - correct - wrong,
        "quiz_id": quiz_id,
        "cards": {}
    }

    for card in quiz_cards:
        quiz_result["cards"][card[0]] = {
            "question": card[3],
            "answer": card[4],
            "correct": card[1] == 1,
            "user_answer": card[2],
        }

    return quiz_result, ""
